import unittest
import hedy

class TestLevel1(unittest.TestCase):

    def test_print_1(self):
        parser_level_1 = hedy.create_parser_level_1()
        tree = parser_level_1.parse("print felienne 123")
        self.assertEqual(tree.data, 'print')

    def test_ask_1(self):
        parser_level_1 = hedy.create_parser_level_1()
        tree = parser_level_1.parse("ask felienne 123")
        self.assertEqual(tree.data, 'ask')

    def test_other_1(self):
        parser_level_1 = hedy.create_parser_level_1()
        tree = parser_level_1.parse("abc felienne 123")
        self.assertEqual(tree.data, 'invalid')


if __name__ == '__main__':
    unittest.main()



    # python = transpile(tree)
    # print(python)
    #
    # exec(python)