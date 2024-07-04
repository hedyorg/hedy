import re
import warnings


# Hedy's grammar merging supports multiple operators which allow adding, removing and moving
# last parts of a rule definition. For example, if level 1 contains the following definition
# `command: repeat | while` and level 2 redefines the rule as `command += for -= while >> repeat`,
# then the merged grammar of level 2 will have the following definition `command: for | repeat`
ADD_GRAMMAR_MERGE_OP = '+='
REMOVE_GRAMMAR_MERGE_OP = '-='
LAST_GRAMMAR_MERGE_OP = '>>'
GRAMMAR_MERGE_OPERATORS = [ADD_GRAMMAR_MERGE_OP, REMOVE_GRAMMAR_MERGE_OP, LAST_GRAMMAR_MERGE_OP]


def needs_colon(rule):
    pos = rule.find('_EOL (_SPACE command)')
    return f'{rule[0:pos]} _COLON {rule[pos:]}'


def old_rule_to_error(rule):
    return rule


# Preprocess rules specify a change that could be reused to alter several rules, e.g. for<needs_colon>
# adds a colon to the old `for` definition, instead of defining the whole rule again with a colon.
PREPROCESS_RULES = {
    'needs_colon': needs_colon,
    'old_rule_to_error': old_rule_to_error,
}


class GrammarRule:
    """Used to store information about parsed grammar rules when merging grammars.
    Valid examples of rules: name.-100: _DEFINITION, name<processor>, and name.1<processor argument>."""

    def __init__(self, line, name, definition, processor=None, processor_arg=None):
        self.line = line
        self.name_with_priority = name
        self.name = strip_priority_suffix(name).strip(' ')
        self.definition = definition
        self.processor = processor
        self.processor_arg = processor_arg

    def is_processed(self):
        # If there is no definition, then we have not processed the rule yet
        return self.definition != ''

    def process(self, value):
        self.definition = value
        self.line = f'{self.name_with_priority}:{value}'

    def __str__(self):
        return f'{self.name}:{self.definition}'

    def __repr__(self):
        return self.__str__()


def merge_grammars(grammar_text_1, grammar_text_2):
    """Merges two grammar files into one.
    Rules that are redefined in the second file are overridden.
    Rules that are new in the second file are added."""
    merged_grammar = []
    rules_to_delete = []  # collects rules we no longer need

    base_grammar = extract_grammar_rules(grammar_text_1)
    target_grammar = extract_grammar_rules(grammar_text_2)

    preprocess_rules(target_grammar, base_grammar)

    for base_rule in base_grammar.values():
        if base_rule.name in target_grammar:
            target_rule = target_grammar[base_rule.name]
            if base_rule.definition.strip() == target_rule.definition.strip():
                warnings.warn(f"The rule {base_rule.name} is duplicated: {base_rule.definition}. Please check!")
            # Computes the rules that use the merge operators in the grammar, namely +=, -= and >>
            merged_rule, to_delete = merge_rules_operator(base_rule.definition, target_rule.definition,
                                                          base_rule.name, target_rule.line)
            rules_to_delete.extend(to_delete)
            merged_grammar.append(merged_rule)
        else:
            merged_grammar.append(base_rule.line)

    for target_rule in target_grammar.values():
        if target_rule.name not in base_grammar:
            merged_grammar.append(target_rule.line)

    # filters rules that are no longer needed
    rules_to_keep = [rule for rule in merged_grammar if get_rule_from_string(rule)[0] not in rules_to_delete]
    return '\n'.join(sorted(rules_to_keep))


def extract_grammar_rules(grammar):
    lines = grammar.split('\n')
    rules = [parse_grammar_rule(line) for line in lines if line != '' and line[0] != '/']
    return {r.name: r for r in rules}


def parse_grammar_rule(line):
    needs_processing = re.match(r'((\w|_)+(\.-?\d+)?)<((\w|_)+)( (\w|_)+)?>', line)
    if needs_processing:
        name = needs_processing.group(1)
        processor = needs_processing.group(4)
        has_arg = needs_processing.re.groups > 5 and needs_processing.group(6)
        processor_arg = needs_processing.group(6).strip(' ') if has_arg else name
        return GrammarRule(line=line, name=name, definition='', processor=processor, processor_arg=processor_arg)

    name, definition = get_rule_from_string(line)
    return GrammarRule(line=line, name=name, definition=definition)


def get_rule_from_string(s):
    # splits the name and the definition of a rule
    parts = s.split(':')
    if len(parts) <= 1:
        return s, s
    # we join because the rule definition could contain :
    return parts[0], ':'.join(parts[1:])


def preprocess_rules(grammar, base_grammar):
    for rule in grammar.values():
        if not rule.is_processed():
            base_definition = get_base_rule_definition(rule, base_grammar)
            rule.process(PREPROCESS_RULES[rule.processor](base_definition))


def get_base_rule_definition(rule, base_grammar):
    base_rule_name = rule.processor_arg
    if base_rule_name not in base_grammar:
        raise Exception(f'Rule {rule.name} references rule {base_rule_name} but it is not in the base grammar.')
    return base_grammar[base_rule_name].definition


def merge_rules_operator(prev_definition, new_definition, name, complete_line):
    op_to_arg = get_operator_to_argument(new_definition)

    add_arg = op_to_arg.get(ADD_GRAMMAR_MERGE_OP, '')
    remove_arg = op_to_arg.get(REMOVE_GRAMMAR_MERGE_OP, '')
    last_arg = op_to_arg.get(LAST_GRAMMAR_MERGE_OP, '')
    remaining_commands = get_remaining_rules(prev_definition, remove_arg, last_arg)
    ordered_commands = split_rule(remaining_commands, add_arg, last_arg)

    new_rule = f"{name}: {' | '.join(ordered_commands)}" if bool(op_to_arg) else complete_line
    deletable = split_rule(remove_arg)
    return new_rule, deletable


def get_operator_to_argument(definition):
    """Creates a map of all used operators and their respective arguments e.g. {'+=': 'print | play', '>>': 'echo'}"""
    operator_to_index = [(op, definition.find(op)) for op in GRAMMAR_MERGE_OPERATORS if op in definition]
    result = {}
    for i, (op, index) in enumerate(operator_to_index):
        start_index = index + len(op)
        if i + 1 < len(operator_to_index):
            _, next_index = operator_to_index[i + 1]
            result[op] = definition[start_index:next_index].strip()
        else:
            result[op] = definition[start_index:].strip()
    return result


def get_remaining_rules(orig_def, *sub_def):
    original_commands = split_rule(orig_def)
    commands_after_minus = split_rule(*sub_def)
    misses = [c for c in commands_after_minus if c not in original_commands]
    if misses:
        raise Exception(f"Command(s) {'|'.join(misses)} do not exist in the previous definition")
    remaining_commands = [cmd for cmd in original_commands if cmd not in commands_after_minus]
    remaining_commands = ' | '.join(remaining_commands)  # turn the result list into a string
    return remaining_commands


def split_rule(*rules):
    return [c.strip() for rule in rules for c in rule.split('|') if c.strip() != '']


def strip_priority_suffix(rule):
    if re.match(r"\w+\.\-?\d+", rule):
        return rule.split('.')[0]
    return rule
