import unittest
import hedy
import json

class TestLevel1(unittest.TestCase):

    def test_parse_print_1(self):
        parser_level_1 = hedy.create_parser(1)
        tree = parser_level_1.parse("print felienne 123")
        self.assertEqual(tree.data, 'print')

    def test_parse_ask_1(self):
        parser_level_1 = hedy.create_parser(1)
        tree = parser_level_1.parse("ask felienne 123")
        self.assertEqual(tree.data, 'ask')

    def test_transpile_ask_1(self):
        result = hedy.transpile("ask felienne 123", 1)
        self.assertEqual(result, "answer = input('felienne 123')")



    def test_parse_other_1(self):
        parser_level_1 = hedy.create_parser(1)
        tree = parser_level_1.parse("abc felienne 123")
        self.assertEqual(tree.data, 'invalid')

    def test_transpile_print_1(self):
        result = hedy.transpile("print Hallo welkom bij Hedy", 1)
        self.assertEqual(result, "print('Hallo welkom bij Hedy')")

    def test_transpile_echo_1(self):
        result = hedy.transpile("echo", 1)
        self.assertEqual(result, "print(answer)")


if __name__ == '__main__':
    unittest.main()



    # python = transpile(tree)
    # print(python)
    #
    # exec(python)
