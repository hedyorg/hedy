import unittest
import hedy
import json

class TestsLevel1(unittest.TestCase):

    def test_transpile_other(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("abc felienne 123", 1)
            self.assertEqual(str(context), 'First word is not a command')

    def test_transpile_print(self):
        result = hedy.transpile("print Hallo welkom bij Hedy!", 1)
        self.assertEqual(result, "print('Hallo welkom bij Hedy!')")

    def test_transpile_ask(self):
        result = hedy.transpile("ask wat is je lievelingskleur?", 1)
        self.assertEqual(result, "answer = input('wat is je lievelingskleur?')")

    def test_transpile_print_multiple_lines(self):
        result = hedy.transpile("print Hallo welkom bij Hedy\nprint Mooi hoor", 1)
        self.assertEqual(result, "print('Hallo welkom bij Hedy')\nprint('Mooi hoor')")

    def test_transpile_three_lines(self):
        input = """print Hallo
ask Wat is je lievelingskleur
echo je lievelingskleur is"""
        result = hedy.transpile(input, 1)
        self.assertEqual(result, "print('Hallo')\nanswer = input('Wat is je lievelingskleur')\nprint('je lievelingskleur is ' + answer)")


    def test_transpile_echo(self):
        result = hedy.transpile("echo Jouw lievelingskleur is dus...", 1)
        self.assertEqual(result, "print('Jouw lievelingskleur is dus... ' + answer)")

class TestsLevel2(unittest.TestCase):
    # ------ tests level 2 -------

    # some commands should not change:
    def test_transpile_other(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("abc felienne 123", 2)
            self.assertEqual(str(context), 'First word is not a command')

    def test_transpile_print(self):
        result = hedy.transpile("print Hallo welkom bij Hedy!", 2)
        self.assertEqual(result, "print('Hallo '+'welkom '+'bij '+'Hedy '+'! ')")

    def test_transpile_ask(self):
        result = hedy.transpile("ask wat is je lievelingskleur?", 2)
        self.assertEqual(result, "answer = input('wat is je lievelingskleur?')")

    def test_transpile_print_multiple_lines(self):
        result = hedy.transpile("print Hallo welkom bij Hedy!\nprint Mooi hoor", 2)
        self.assertEqual(result, "print('Hallo '+'welkom '+'bij '+'Hedy '+'! ')\nprint('Mooi '+'hoor ')")

    def test_transpile_echo(self):
        result = hedy.transpile("echo Jouw lievelingskleur is dus...", 2)
        self.assertEqual(result, "print('Jouw lievelingskleur is dus... ' + answer)")

    def test_transpile_assign(self):
        result = hedy.transpile("naam is Felienne", 2)
        self.assertEqual(result, "naam = 'Felienne'")

    def test_transpile_assign_2_integer(self):
        result = hedy.transpile("naam is 14", 2)
        self.assertEqual(result, "naam = '14'")

    def test_transpile_assign_and_print(self):
        result = hedy.transpile("naam is Felienne\nprint naam", 2)
        self.assertEqual(result, "naam = 'Felienne'\nprint(naam+' ')")

    def test_transpile_assign_and_print_more_words(self):
        result = hedy.transpile("naam is Felienne\nprint hallo naam", 2)
        self.assertEqual(result, "naam = 'Felienne'\nprint('hallo '+naam+' ')")

    def test_transpile_assign_and_print_punctuation(self):
        result = hedy.transpile("naam is Hedy\nprint Hallo naam!", 2)
        self.assertEqual(result, "naam = 'Hedy'\nprint('Hallo '+naam+'! ')")

    def test_transpile_assign_and_print_in_sentence(self):
        result = hedy.transpile("naam is Hedy\nprint naam is jouw voornaam", 2)
        self.assertEqual(result, "naam = 'Hedy'\nprint(naam+' '+'is '+'jouw '+'voornaam ')")

    def test_transpile_assign_and_print_something_else(self):
        result = hedy.transpile("naam is Felienne\nprint Hallo", 2)
        self.assertEqual(result, "naam = 'Felienne'\nprint('Hallo ')")

class TestsLevel3(unittest.TestCase):
    def test_transpile_other(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("abc felienne 123", 3)
            self.assertEqual(str(context), 'First word is not a command')

    def test_transpile_print_level_2(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("print felienne 123", 3)
            self.assertEqual(str(context), 'First word is not a command') #hier moet nog we een andere foutmelding komen!

    def test_print_level_3(self):
        result = hedy.transpile("print 'ik heet henk'", 3)
        self.assertEqual(result, "print('ik heet henk ')")

    def test_print_with_var_level_3(self):
        result = hedy.transpile("naam is Hedy\nprint 'ik heet' naam", 3)
        self.assertEqual(result, "naam = 'Hedy'\nprint('ik heet '+naam)")

    def test_transpile_print(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("print Hallo welkom bij Hedy!", 3)
            self.assertEqual(str(result), "Don't forget the quotation marks around text in level 3!")

        # def test_assign_and_print(self):
        #     result = hedy.transpile('naam is Hedy\nprint "ik heet" naam', 3)
        #     self.assertEqual(result, "naam = 'Hedy'\nprint('ik heet'+naam)")

if __name__ == '__main__':
    unittest.main()



    # python = transpile(tree)
    # print(python)
    #
    # exec(python)
