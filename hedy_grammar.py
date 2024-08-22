import re
import warnings
from os import path
from functools import cache
import itertools

import lark

from hedy_translation import keywords_to_dict
from functools import lru_cache
from lark import Lark
import hashlib
import os
import pickle
import sys
import tempfile
import utils
import regex


"""
Because of the gradual nature of Hedy, the grammar of every level is just slightly different than the grammar of the
previous one. With the current approach every level only describes the grammar differences from its preceding level.
To get the grammar of level N, the grammar of level 1 is merged consecutively with the change definitions of all
levels up to N. To facilitate this approach, 2 features are added:

    - Preprocessing rules appear in grammar rule definitions and allow for custom python logic to be applied before the
    rule is merged. For example, `for:<needs_colon>` fetches the `for` rule from the base grammar and adds a colon at
    the end of its definition. Another example is `if_error:<old_rule_to_error ifs>` which fetches the definition of
    `ifs` from the base grammar. Preprocessors are also used to construct regular expressions which have to avoid
    specific translated keywords, e.g. `elses: /([^\n ]| (?!<expand_keyword else>))+/` is transformed to
    `elses: /([^\n ]| (?!else|ellers))+/` in Danish and `elses: /([^\n ]| (?!else|değilse))+/` in Turkish.

    - Grammar mering operators, i.e. +=, -= and >>, allow adding, removing and moving last parts of a rule definition.
    For example, if level 1 contains the following definition `command: repeat | while` and level 2 redefines the
    rule as `command += for -= while >> repeat`, then the merged grammar of level 2 will have the following
    definition `command: for | repeat`.
"""


def _get_parser_cache_directory():
    # TODO we should maybe store this to .test-cache so we can
    # re-use them in github actions caches for faster CI.
    # We can do this after #4574 is merged.
    return tempfile.gettempdir()


def _save_parser_to_file(lark, pickle_file):
    # Store the parser to a file, a bit hacky because it is not
    # pickle-able out of the box
    # See https://github.com/lark-parser/lark/issues/1348

    # Note that if Lark ever implements the cache for Earley parser
    # or if we switch to a LALR parser we don't need this hack anymore

    full_path = os.path.join(_get_parser_cache_directory(), pickle_file)

    # These attributes can not be pickled as they are a module
    lark.parser.parser.lexer_conf.re_module = None
    lark.parser.lexer_conf.re_module = None

    try:
        with utils.atomic_write_file(full_path) as fp:
            pickle.dump(lark, fp)
    except OSError:
        # Ignore errors if another process already moved the file
        # or if the destination already exist.
        # These scenarios can happen under concurrent execution.
        pass

    # Restore the unpickle-able bits.
    # Keep this in sync with the restore method!
    lark.parser.parser.lexer_conf.re_module = regex
    lark.parser.lexer_conf.re_module = regex


def _restore_parser_from_file_if_present(pickle_file):
    full_path = os.path.join(_get_parser_cache_directory(), pickle_file)
    if os.path.isfile(full_path):
        try:
            with open(full_path, "rb") as fp:
                lark = pickle.load(fp)
            # Restore the unpickle-able bits.
            # Keep this in sync with the save method!
            lark.parser.parser.lexer_conf.re_module = regex
            lark.parser.lexer_conf.re_module = regex
            return lark
        except Exception:
            # If anything goes wrong try to remove the file
            # and we will try again in the next cycle
            try:
                os.unlink(full_path)
            except Exception:
                pass
    return None


# @lru_cache(maxsize=0 if utils.is_production() else 100)
def get_parser(level, lang="en", keep_all_tokens=False, skip_faulty=False):
    """Return the Lark parser for a given level.
    Parser generation takes about 0.5 seconds depending on the level, so
    we want to cache it, or we have latency of 500ms on the calculations
    and a high server load, and CI runs of 5+ hours.

    We used to cache this to RAM but because of all the permutations we
    had 1000s of parsers and got into out-of-memory issue in the
    production environment.

    Now we cache a limited number of the parsers to RAM, but introduce
    a second tier of cache to disk.

    This is not implemented by Lark natively for the Earley parser.
    See https://github.com/lark-parser/lark/issues/1348.
    """
    unique_parser_hash = hashlib.sha1("_".join([str(e) for e in [
        skip_faulty,
        keep_all_tokens,
        sys.version_info[:2],
    ]]).encode()).hexdigest()

    langs = ['en', 'nl', 'bg', 'eo']  # TODO: For test purposes, let's set the langs to be static
    langs = sorted(list(set(langs)))

    cached_parser_file = f"cached-parser-{level}-{'-'.join(langs)}-{unique_parser_hash}.pkl"

    use_cache = False
    parser = None
    if use_cache:
        parser = _restore_parser_from_file_if_present(cached_parser_file)
    if parser is None:

        parser = create_parser(level, langs, skip_faulty, keep_all_tokens)
        if use_cache:
            _save_parser_to_file(parser, cached_parser_file)

    return parser


def create_parser(level, langs, skip_faulty, keep_all_tokens):
    grammar = create_grammar(level, langs, skip_faulty)

    translate = get_translated_keywords(langs)

    def edit_terminals(t):
        try:
            # TODO: not sure how to have a nice conversion between lark's terminal syntax (_PRINT_KEYWORD) and
            #  the keyword actual name in the yaml files (print). For now removing the _ prefix and the _KEYWORD suffix
            if '_KEYWORD' in t.name:
                keyword = t.name.strip('KEYWORD').strip('_').lower()
                if keyword in translate:
                    t.pattern.value = f"(?:{'|'.join(translate[keyword])})"
        except KeyError:
            pass

    parser_opts = {
        "regex": True,
        "propagate_positions": True,
        "keep_all_tokens": keep_all_tokens,
        "edit_terminals": edit_terminals
    }

    return Lark(grammar, **parser_opts)  # ambiguity='explicit'


# @cache
def create_grammar(level, langs, skip_faulty):
    """ Creates a grammar file for a chosen level and lang. Note that the language is required
    to generate regular expressions that escape keywords (with negative lookahead).
    Currently, it is only a couple of MB in total, so it is safe to cache. """
    # start with creating the grammar for level 1
    merged_grammars = get_full_grammar_for_level(1)

    # then keep merging new grammars in
    for lvl in range(2, level + 1):
        grammar_text_lvl = get_additional_rules_for_level(lvl)
        merged_grammars = merge_grammars(merged_grammars, grammar_text_lvl, langs)

    if skip_faulty:
        skip_faulty_grammar = read_skip_faulty_file(level)
        merged_grammars = merge_grammars(merged_grammars, skip_faulty_grammar, langs)

    # keyword and other terminals never have merge-able rules, so we can just add them at the end
    # keywords = get_keywords_for_language(lang)
    terminals = get_terminals()
    merged_grammars = merged_grammars + '\n' + terminals

    # ready? Save to file to ease debugging
    # this could also be done on each merge for performance reasons
    save_total_grammar_file(level, merged_grammars, langs)
    return merged_grammars


def merge_grammars(grammar_text_1, grammar_text_2, langs):
    """ Merges two grammar files into one.
    Rules that are redefined in the second file are overridden.
    Rules that are new in the second file are added."""
    merged_grammar = []
    rules_to_delete = []  # collects rules we no longer need

    base_grammar = parse_grammar(grammar_text_1)
    target_grammar = parse_grammar(grammar_text_2)

    apply_preprocessing_rules(target_grammar, base_grammar, langs)

    for base_rule in base_grammar.values():
        if base_rule.name in target_grammar:
            target_rule = target_grammar[base_rule.name]
            if base_rule.value.strip() == target_rule.value.strip():
                warnings.warn(f"The rule {base_rule.name} is duplicated: {base_rule.value}. Please check!")
            # computes the rules that use the merge operators in the grammar, namely +=, -= and >>
            merged_rule, to_delete = merge_rules_operator(base_rule.value, target_rule.value,
                                                          base_rule.name, target_rule.line)
            rules_to_delete.extend(to_delete)
            merged_grammar.append(merged_rule)
        else:
            merged_grammar.append(base_rule.line)

    for target_rule in target_grammar.values():
        if target_rule.name not in base_grammar:
            merged_grammar.append(target_rule.line)

    # filters rules that are no longer needed
    rules_to_keep = [rule for rule in merged_grammar if split_rule_name_and_value(rule)[0] not in rules_to_delete]
    return '\n'.join(sorted(rules_to_keep))


def read_file(*paths):
    script_dir = path.abspath(path.dirname(__file__))
    path_ = path.join(script_dir, *paths)
    with open(path_, "r", encoding="utf-8") as file:
        return file.read()


def read_skip_faulty_file(level):
    script_dir = path.abspath(path.dirname(__file__))
    for lvl in range(level, 0, -1):
        file_path = path.join(script_dir, 'grammars', f'skip-faulty-level{lvl}.lark')
        if path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()


def write_file(content, *paths):
    script_dir = path.abspath(path.dirname(__file__))
    path_ = path.join(script_dir, *paths)
    with open(path_, "w", encoding="utf-8") as file:
        file.write(content)


def get_keywords_for_language(language):
    try:
        return read_file('grammars', f'keywords-{language}.lark')
    except FileNotFoundError:
        return read_file('grammars', 'keywords-en.lark')


def get_terminals():
    return read_file('grammars', 'terminals.lark')


def save_total_grammar_file(level, grammar, langs_):
    write_file(grammar, 'grammars-Total', f'level{level}.{"-".join(langs_)}-Total.lark')


def get_additional_rules_for_level(level):
    return read_file('grammars', f'level{level}-Additions.lark')


def get_full_grammar_for_level(level):
    return read_file('grammars', f'level{level}.lark')


def parse_grammar(grammar):
    lines = grammar.split('\n')
    rules = [parse_grammar_rule(line) for line in lines if line != '' and line[0] != '/']
    return {r.name: r for r in rules}


def parse_grammar_rule(line):
    processor_rules = [re.findall(fr'<({rule})( +[\w_]+)?>', line) for rule in PREPROCESS_RULES]
    processor_rules = [
        RuleProcessor(name, arg)
        for rules in processor_rules
        for name, arg in rules if rules
    ]

    name, value = split_rule_name_and_value(line)
    return GrammarRule(line=line, name=name, value=value, processors=processor_rules)


class GrammarRule:
    """Used to store information about parsed grammar rules when merging grammars.
    Valid examples of rules: name.-100: _DEFINITION, name<processor>, and name.1<processor argument>."""

    def __init__(self, line, name, value, processors=None):
        self.line = line
        self.name_with_priority = name
        self.name = strip_priority_suffix(name).strip()
        self.value = value
        self.processors = processors

    def apply_processors(self, base_grammar, langs):
        if self.processors:
            result = self.value
            for processor in self.processors:
                arg = processor.arg if processor.arg else self.name
                target_part = processor.func(arg=arg, langs=langs, base_grammar=base_grammar)
                result = result.replace(processor.match_string, target_part)
            self.value = result
            self.line = f'{self.name_with_priority}:{result}'

    def __str__(self):
        return f'{self.name}:{self.value}'

    def __repr__(self):
        return self.__str__()


class RuleProcessor:
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg.strip()
        self.match_string = f'<{name}{arg}>'
        self.func = PREPROCESS_RULES[name]


def split_rule_name_and_value(s):
    # splits the name and the definition of a rule
    parts = s.split(':')
    if len(parts) <= 1:
        return s, s
    # we join because the rule definition could contain :
    return parts[0], ':'.join(parts[1:])


def apply_preprocessing_rules(grammar, base_grammar, langs):
    for rule in grammar.values():
        rule.apply_processors(base_grammar, langs)


def get_rule_from_grammar(rule_name, grammar):
    if rule_name not in grammar:
        raise Exception(f'There is a reference to rule {rule_name} but it is not in the base grammar.')
    return grammar[rule_name]


#
# Grammar rule preprocessing functions
#
def needs_colon(**kwargs):
    """ Returns the definition of the rule in the base grammar modified so that it is followed by a `:` """
    rule_name = kwargs['arg']
    base_grammar = kwargs['base_grammar']

    rule = get_rule_from_grammar(rule_name, base_grammar)
    value = rule.value
    pos = value.find('_EOL (_SPACE command)')
    return f'{value[0:pos]} _COLON {value[pos:]}'


def old_rule_to_error(**kwargs):
    """ Returns the 'old' version of the rule, i.e. the definition of the rule in the base grammar """
    arg = kwargs['arg']
    base_grammar = kwargs['base_grammar']

    rule = get_rule_from_grammar(arg, base_grammar)
    return rule.value


def expand_keyword(**kwargs):
    """ Creates a list of all values of a keyword. The keyword `else` produces `else|ellers` for Danish"""
    keyword = kwargs['arg']
    langs = kwargs['langs']

    values = get_translated_keyword(keyword, langs)
    values = sorted(list(set(values)))
    return '|'.join(values)


def expand_keyword_first(**kwargs):
    """ Creates a list of the first letter of all values of a keyword.
    The keyword `else` produces `ei` for Ukrainian """
    keyword = kwargs['arg']
    langs = kwargs['langs']

    values = get_translated_keyword(keyword, langs)
    values = sorted(list(set([v[0] for v in values])))
    return ''.join(values)


def expand_keyword_not_followed_by_space(**kwargs):
    """ Creates a negative lookahead for all values of a keyword (except their first letter) followed by a space.
    The keyword `else` produces `e(?!lse |llers )` for Danish and `e(?!lse )|и(?!наче)` for Bulgarian"""
    keyword = kwargs['arg']
    lang = kwargs['lang']

    values = get_translated_keyword(keyword, lang)
    first_to_rest = dict()
    for v in values:
        first, rest = v[0], f'{v[1:]} '
        if first in first_to_rest:
            first_to_rest[first].append(rest)
        else:
            first_to_rest[first] = [rest]

    result = [f'{k}(?!{"|".join(v)})' for k, v in first_to_rest.items()]
    return '|'.join(result)


def get_translated_keywords(langs):
    result = dict()
    for lang in langs:
        keywords = keywords_to_dict(lang)
        for k in keywords:
            if k not in result:
                result[k] = keywords[k]
            else:
                result[k].extend(keywords[k])
    return result


def get_translated_keyword(keyword, langs):
    def get_keyword_value_from_lang(keyword_, lang_):
        keywords = keywords_to_dict(lang_)
        if keyword_ in keywords:
            return [k for k in keywords[keyword_] if k]
        else:
            raise Exception(f"The keywords yaml file for language '{lang_}' has no definition for '{keyword_}'.")

    return list(itertools.chain([get_keyword_value_from_lang(keyword, lang) for lang in langs]))


PREPROCESS_RULES = {
    'needs_colon': needs_colon,
    'old_rule_to_error': old_rule_to_error,
    'expand_keyword': expand_keyword,
    'expand_keyword_first': expand_keyword_first,
    'expand_keyword_not_followed_by_space': expand_keyword_not_followed_by_space,
}


#
# Grammar merging operators: +=, -=, >>
#
ADD_GRAMMAR_MERGE_OP = '+='
REMOVE_GRAMMAR_MERGE_OP = '-='
LAST_GRAMMAR_MERGE_OP = '>>'
GRAMMAR_MERGE_OPERATORS = [ADD_GRAMMAR_MERGE_OP, REMOVE_GRAMMAR_MERGE_OP, LAST_GRAMMAR_MERGE_OP]


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
    if re.match(r"\w+\.-?\d+", rule):
        return rule.split('.')[0]
    return rule
