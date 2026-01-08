import textwrap
import unittest
from hedy_grammar import merge_rules_operator, parse_grammar_rule, merge_grammars, GrammarRule, RuleProcessor
from parameterized import parameterized
lang = 'en'


class TestGrammars(unittest.TestCase):
    def test_merge_grammars_adds_rule(self):
        grammar_level_1 = "start: program"
        grammar_level_2 = "command: play"
        result = merge_grammars(grammar_level_1, grammar_level_2, lang)

        expected = textwrap.dedent("""\
            command: play
            start: program""")
        self.assertEqual(expected, result)

    def test_merge_grammars_overrides_rule(self):
        grammar_level_1 = "start: program"
        grammar_level_2 = "start: another program"
        result = merge_grammars(grammar_level_1, grammar_level_2, lang)

        self.assertEqual("start: another program", result)

    def test_merge_grammars_removes_unused_rule(self):
        grammar_level_1 = "command: repeat | for\nrepeat: _repeat"
        grammar_level_2 = "command: -= repeat"
        result = merge_grammars(grammar_level_1, grammar_level_2, lang)

        self.assertEqual("command: for", result)

    def test_parse_rule(self):
        rule = parse_grammar_rule('start: program')
        self.assert_rule(rule, name='start', value=' program')

    def test_parse_rule_with_multiple_colons(self):
        rule = parse_grammar_rule('for: "FOR" ":" _iterator ":" command+')
        self.assert_rule(rule, name='for', value=' "FOR" ":" _iterator ":" command+')

    def test_parse_rule_with_priority(self):
        rule = parse_grammar_rule('error_invalid.-100: error')
        self.assert_rule(rule, name='error_invalid', value=' error')

    def test_parse_rule_with_preprocessor(self):
        rule = parse_grammar_rule('if_else:<needs_colon>')
        self.assert_rule(rule, name='if_else', value='<needs_colon>', processors=[('needs_colon', '')])

    def test_parse_rule_with_preprocessor_and_argument(self):
        rule = parse_grammar_rule('if_else_error:<old_rule_to_error if_else>')
        self.assert_rule(
            rule,
            name='if_else_error',
            value='<old_rule_to_error if_else>',
            processors=[('old_rule_to_error', 'if_else')])

    def test_parse_rule_with_priority_and_preprocessor(self):
        rule = parse_grammar_rule('if_else.20:<expand_keyword from>')
        self.assert_rule(
            rule,
            name='if_else',
            value='<expand_keyword from>',
            processors=[('expand_keyword', 'from')])

    def test_parse_rule_with_multiple_preprocessors(self):
        rule = parse_grammar_rule('if_else:/[^<expand_keyword_first to>]|<expand_keyword from>/')
        self.assert_rule(
            rule,
            name='if_else',
            value='/[^<expand_keyword_first to>]|<expand_keyword from>/',
            processors=[('expand_keyword', 'from'), ('expand_keyword_first', 'to')])

    def test_preprocess_needs_colon(self):
        base_grammar = {'command': GrammarRule(
            line='command: program _EOL (_SPACE command)',
            name='command',
            value=' program _EOL (_SPACE command)')}
        target_rule = GrammarRule(
            line='command:<needs_colon>',
            name='command',
            value='<needs_colon>',
            processors=[RuleProcessor('needs_colon', '')]
        )

        target_rule.apply_processors(base_grammar, lang)

        self.assertEqual('command: program  _COLON _EOL (_SPACE command)', target_rule.line)

    def test_preprocess_needs_colon_gives_error(self):
        target_rule = GrammarRule(
            line='command:<needs_colon>',
            name='command',
            value='<needs_colon>',
            processors=[RuleProcessor('needs_colon', '')]
        )

        with self.assertRaises(Exception):
            target_rule.apply_processors({}, lang)

    def test_preprocess_old_rule_to_error(self):
        base_grammar = {'command': parse_grammar_rule('command: program _EOL (_SPACE command)')}
        target_rule = GrammarRule(
            line='error_command:<old_rule_to_error command>',
            name='error_command',
            value='<old_rule_to_error command>',
            processors=[RuleProcessor('old_rule_to_error', ' command')]
        )

        target_rule.apply_processors(base_grammar, lang)

        self.assertEqual('error_command: program _EOL (_SPACE command)', target_rule.line)

    def test_preprocess_old_rule_to_error_gives_error(self):
        target_rule = GrammarRule(
            line='error_command:<old_rule_to_error command>',
            name='error_command',
            value='<old_rule_to_error command>',
            processors=[RuleProcessor('old_rule_to_error', ' command')]
        )

        with self.assertRaises(Exception):
            target_rule.apply_processors({}, lang)

    @parameterized.expand([('en', 'else'), ('da', 'ellers|else'), ('eo', 'alie|else')])
    def test_preprocess_expand_keyword(self, language, expected_value):
        target_rule = GrammarRule(
            line='ifs:<expand_keyword else>',
            name='ifs',
            value='<expand_keyword else>',
            processors=[RuleProcessor('expand_keyword', ' else')]
        )

        target_rule.apply_processors({}, language)

        self.assertEqual(f'ifs:{expected_value}', target_rule.line)

    @parameterized.expand([('en', 't'), ('nl', 't'), ('eo', 'at'), ('bg', 'tд')])
    def test_preprocess_expand_first_keyword(self, language, expected_value):
        target_rule = GrammarRule(
            line='ifs:<expand_keyword_first to_list>',
            name='ifs',
            value='<expand_keyword_first to_list>',
            processors=[RuleProcessor('expand_keyword_first', ' to_list')]
        )

        target_rule.apply_processors({}, language)

        self.assertEqual(f'ifs:{expected_value}', target_rule.line)

    @parameterized.expand([
        ('en', 'e(?!lse )'),
        ('da', 'e(?!llers |lse )'),
        ('nl', 'a(?!nders )|e(?!lse )')
    ])
    def test_expand_keyword_not_followed_by_space_keyword(self, language, expected_value):
        target_rule = GrammarRule(
            line='ifs:<expand_keyword_not_followed_by_space else>',
            name='ifs',
            value='<expand_keyword_not_followed_by_space else>',
            processors=[RuleProcessor('expand_keyword_not_followed_by_space', ' else')]
        )

        target_rule.apply_processors({}, language)

        self.assertEqual(f'ifs:{expected_value}', target_rule.line)

    @parameterized.expand(['expand_keyword', 'expand_keyword_first', 'expand_keyword_not_followed_by_space'])
    def test_preprocess_expand_keyword_gives_error_if_unknown_keyword(self, rule):
        target_rule = GrammarRule(
            line=f'ifs:<{rule} unknown>',
            name='ifs',
            value=f'<{rule} unknown>',
            processors=[RuleProcessor(rule, ' unknown')]
        )

        with self.assertRaises(Exception):
            target_rule.apply_processors({}, lang)

    def test_rule_merging_without_operators(self):
        prev_definition = ' _PRINT (text)?'
        new_definition = ' _PRINT (_print_argument)?'
        complete_line = f'print {new_definition}'

        result, deletable = merge_rules_operator(prev_definition, new_definition, 'print', complete_line)

        self.assertEqual(complete_line, result)
        self.assertEqual([], deletable)

    def test_rule_merging_override(self):
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

    def assert_rule(self, rule, name, value, processors=None):
        self.assertEqual(name, rule.name)
        self.assertEqual(value, rule.value)
        if processors:
            for i in range(0, len(processors)):
                self.assertEqual(processors[i][0], rule.processors[i].name)
                self.assertEqual(processors[i][1], rule.processors[i].arg)
        else:
            self.assertEqual([], rule.processors)
