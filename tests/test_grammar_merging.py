import textwrap
import unittest
from hedy_grammar import merge_rules_operator, parse_grammar_rule, merge_grammars, preprocess_rules


class TestGrammarMerging(unittest.TestCase):

    def test_merge_grammars_adds_rule(self):
        grammar_level_1 = "start: program"
        grammar_level_2 = "command: play"
        result = merge_grammars(grammar_level_1, grammar_level_2)

        expected = textwrap.dedent("""\
            command: play
            start: program""")
        self.assertEqual(expected, result)

    def test_merge_grammars_overrides_rule(self):
        grammar_level_1 = "start: program"
        grammar_level_2 = "start: another program"
        result = merge_grammars(grammar_level_1, grammar_level_2)

        self.assertEqual("start: another program", result)

    def test_merge_grammars_removes_unused_rule(self):
        grammar_level_1 = "command: repeat | for\nrepeat: _repeat"
        grammar_level_2 = "command: -= repeat"
        result = merge_grammars(grammar_level_1, grammar_level_2)

        self.assertEqual("command: for", result)

    def test_parse_rule(self):
        rule = parse_grammar_rule('start: program')
        self.assert_rule(rule, name='start', definition=' program')

    def test_parse_rule_with_multiple_colons(self):
        rule = parse_grammar_rule('for: "FOR" ":" _iterator ":" command+')
        self.assert_rule(rule, name='for', definition=' "FOR" ":" _iterator ":" command+')

    def test_parse_rule_with_priority(self):
        rule = parse_grammar_rule('error_invalid.-100: error')
        self.assert_rule(rule, name='error_invalid', definition=' error')

    def test_parse_rule_with_preprocessor(self):
        rule = parse_grammar_rule('if_else<change_func>')
        self.assert_rule(rule, name='if_else', definition='', processor='change_func', argument='if_else')

    def test_parse_rule_with_preprocessor_and_argument(self):
        rule = parse_grammar_rule('if_else<change_func old_rule>')
        self.assert_rule(rule, name='if_else', definition='', processor='change_func', argument='old_rule')

    def test_parse_rule_with_priority_and_preprocessor(self):
        rule = parse_grammar_rule('if_else.20<change_func old_rule>')
        self.assert_rule(rule, name='if_else', definition='', processor='change_func', argument='old_rule')

    def test_preprocess_needs_colon(self):
        base_grammar = {'command': parse_grammar_rule('command: program _EOL (_SPACE command)')}
        target_grammar = {'command': parse_grammar_rule('command<needs_colon>')}

        preprocess_rules(target_grammar, base_grammar)

        self.assertEqual(' program  _COLON _EOL (_SPACE command)', target_grammar['command'].definition)

    def test_preprocess_old_rule_to_error(self):
        base_grammar = {'command': parse_grammar_rule('command: program _EOL (_SPACE command)')}
        target_grammar = {'error_command': parse_grammar_rule('error_command<old_rule_to_error command>')}

        preprocess_rules(target_grammar, base_grammar)

        self.assertEqual(' program _EOL (_SPACE command)', target_grammar['error_command'].definition)

    def test_rule_merging_without_operators(self):
        prev_definition = ' _PRINT (text)?'
        new_definition = ' _PRINT (_print_argument)?'
        complete_line = f'print {new_definition}'

        result, deletable = merge_rules_operator(prev_definition, new_definition, 'print', complete_line)

        self.assertEqual(complete_line, result)
        self.assertEqual([], deletable)

    def test_rule_merging_with_greater_than_sign(self):
        prev_definition = ' /([^\\n#ـ])([^\\n#]*)/ -> text //comment'
        new_definition = ' /([^\\n#]+)/ -> text'
        complete_line = 'text: /([^\\n#]+)/ -> text'

        result, deletable = merge_rules_operator(prev_definition, new_definition, 'text', complete_line)

        self.assertEqual(complete_line, result)
        self.assertEqual([], deletable)

    def test_rule_merging_add(self):
        prev_definition = 'print'
        new_definition = '+= assign | sleep'

        result, deletable = merge_rules_operator(prev_definition, new_definition, 'command', '')

        self.assertEqual('command: print | assign | sleep', result)
        self.assertEqual([], deletable)

    def test_rule_merging_add_and_remove(self):
        prev_definition = 'print | play | test '
        new_definition = '+= assign | sleep -= play | print'

        result, deletable = merge_rules_operator(prev_definition, new_definition, 'command', '')

        self.assertEqual('command: test | assign | sleep', result)
        self.assertEqual(['play', 'print'], deletable)

    def test_rule_merging_add_and_last(self):
        prev_definition = 'print | play | test '
        new_definition = '+= assign | sleep >> play | print'

        result, deletable = merge_rules_operator(prev_definition, new_definition, 'command', '')

        self.assertEqual('command: test | assign | sleep | play | print', result)
        self.assertEqual([], deletable)

    def test_rule_merging_add_remove_and_last(self):
        prev_definition = ' print | error | echo | test '
        new_definition = '+= assign | sleep -= echo | print >> test | error'

        result, deletable = merge_rules_operator(prev_definition, new_definition, 'command', new_definition)

        self.assertEqual('command: assign | sleep | test | error', result)
        self.assertEqual(['echo', 'print'], deletable)

    def test_rule_merging_remove(self):
        prev_definition = 'print | test | assign'
        new_definition = '-= assign | print'

        result, deletable = merge_rules_operator(prev_definition, new_definition, 'command', '')

        self.assertEqual('command: test', result)
        self.assertEqual(['assign', 'print'], deletable)

    def test_rule_merging_remove_non_existent_gives_error(self):
        prev_definition = 'print | test | assign'
        new_definition = '-= prin'

        with self.assertRaises(Exception):
            merge_rules_operator(prev_definition, new_definition, 'command', '')

    def test_rule_merging_remove_and_last(self):
        prev_definition = 'play | print | test | assign'
        new_definition = '-= assign | print >> play'

        result, deletable = merge_rules_operator(prev_definition, new_definition, 'command', '')

        self.assertEqual('command: test | play', result)
        self.assertEqual(['assign', 'print'], deletable)

    def test_rule_merging_last(self):
        prev_definition = 'print | test | assign | play'
        new_definition = '>> print | play'

        result, deletable = merge_rules_operator(prev_definition, new_definition, 'command', '')

        self.assertEqual('command: test | assign | print | play', result)
        self.assertEqual([], deletable)

    def test_rule_merging_last_non_existent_gives_error(self):
        prev_definition = 'print | test | assign'
        new_definition = '-= prin'

        with self.assertRaises(Exception):
            merge_rules_operator(prev_definition, new_definition, 'command', '')

    def assert_rule(self, rule, name, definition, processor=None, argument=None):
        self.assertEqual(name, rule.name)
        self.assertEqual(definition, rule.definition)
        self.assertEqual(processor, rule.processor)
        self.assertEqual(argument, rule.processor_arg)
