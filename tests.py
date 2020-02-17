import unittest
import hedy
import json

class TestLevel1(unittest.TestCase):

    def test_parse_print_1(self):
        parser_level_1 = hedy.create_parser_level_1()
        tree = parser_level_1.parse("print felienne 123")
        self.assertEqual(tree.data, 'print')

    def test_parse_ask_1(self):
        parser_level_1 = hedy.create_parser_level_1()
        tree = parser_level_1.parse("ask felienne 123")
        self.assertEqual(tree.data, 'ask')

    def test_parse_other_1(self):
        parser_level_1 = hedy.create_parser_level_1()
        tree = parser_level_1.parse("abc felienne 123")
        self.assertEqual(tree.data, 'invalid')

    def test_transpile_print_1(self):
        result = hedy.transpile("print Hallo welkom bij Hedy")
        self.assertEqual(result, "print('Hallo welkom bij Hedy')")

    def json_tester(self):
        response = {}
        response["Code"]= "print(\\'Hallo wereld\\')"

        # convert into JSON:
        y = json.dumps(response)

        # the result is a JSON string:
        self.assertEqual(y, 'test')

if __name__ == '__main__':
    unittest.main()



    # python = transpile(tree)
    # print(python)
    #
    # exec(python)