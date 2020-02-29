import unittest
import hedy
import json

class TestLevel1(unittest.TestCase):

    def test_transpile_other_1(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("abc felienne 123", 1)
        #misschien hier valideren dat de juiste optreedt?

    def test_transpile_print_1(self):
        result = hedy.transpile("print Hallo welkom bij Hedy!", 1)
        self.assertEqual(result, "print('Hallo welkom bij Hedy!')")

    def test_transpile_ask_1(self):
        result = hedy.transpile("ask wat is je lievelingskleur?", 1)
        self.assertEqual(result, "answer = input('wat is je lievelingskleur?')")

    def test_transpile_print_multiple_lines_1(self):
        result = hedy.transpile("print Hallo welkom bij Hedy\nprint Mooi hoor", 1)
        self.assertEqual(result, "print('Hallo welkom bij Hedy')\nprint('Mooi hoor')")

    def test_transpile_three_lines_1(self):
        input = """print Hallo
ask Wat is je lievelingskleur
echo je lievelingskleur is"""
        result = hedy.transpile(input, 1)
        self.assertEqual(result, "print('Hallo')\nanswer = input('Wat is je lievelingskleur')\nprint('je lievelingskleur is' + answer)")


    def test_transpile_echo_1(self):
        result = hedy.transpile("echo Jouw lievelingskleur is dus...", 1)
        self.assertEqual(result, "print('Jouw lievelingskleur is dus...' + answer)")

# ------ tests level 2 -------

    # some commands should not change:
    def test_transpile_other_2(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("abc felienne 123", 2)
        #ook hier is nog type check wel netjes



    def test_transpile_print_2(self):
        result = hedy.transpile("print Hallo welkom bij Hedy!", 2)
        self.assertEqual(result, "print('Hallo welkom bij Hedy!')")

    def test_transpile_ask_2(self):
        result = hedy.transpile("ask wat is je lievelingskleur?", 2)
        self.assertEqual(result, "answer = input('wat is je lievelingskleur?')")

    def test_transpile_print_multiple_lines_2(self):
        result = hedy.transpile("print Hallo welkom bij Hedy\nprint Mooi hoor", 2)
        self.assertEqual(result, "print('Hallo welkom bij Hedy')\nprint('Mooi hoor')")

    def test_transpile_echo_2(self):
        result = hedy.transpile("echo Jouw lievelingskleur is dus...", 2)
        self.assertEqual(result, "print('Jouw lievelingskleur is dus...' + answer)")

    def test_transpile_assign_2(self):
        result = hedy.transpile("naam is Felienne", 2)
        self.assertEqual(result, "naam = 'Felienne'")

    def test_transpile_assign_2_integer(self):
        result = hedy.transpile("naam is 14", 2)
        self.assertEqual(result, "naam = '14'")

    def test_transpile_assign_and_print_2(self):
        result = hedy.transpile("naam is Felienne\nprint naam", 2)
        self.assertEqual(result, "naam = 'Felienne'\nprint(naam)")

    def test_transpile_assign_and_print_something_else2(self):
        result = hedy.transpile("naam is Felienne\nprint Hallo", 2)
        self.assertEqual(result, "naam = 'Felienne'\nprint('Hallo')")


if __name__ == '__main__':
    unittest.main()



    # python = transpile(tree)
    # print(python)
    #
    # exec(python)
