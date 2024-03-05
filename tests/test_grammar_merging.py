import unittest
from hedy import merge_rules_operator


class TestGrammarMerging(unittest.TestCase):

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
