from tests.Tester import HedyTester
import runAST
import hedy

# These tests are used to ensure that the converter works for all Hedy levels.
# These tests are only necessary for levels where changes are required. These
# levels are: 1, 3, 7, 11, 15, 16, 17. The test converts the input program,
# and compares this to the expected output.
#
# A template for future levels:
#    def test_level_(self):
#        level =
#        input = ""
#        output = runAST.complete_tester(input, level)
#        expected = ""
#        self.assertEqual(output, expected)

class TestsUnparserHedy(HedyTester):
    def test_level_1(self):
        level = 1
        input = "ask wie ben jij?\necho oooh"
        output = runAST.complete_tester(input, level)
        expected = "var is ask wie ben jij?\nprint oooh var\n"
        self.assertEqual(output, expected)

    def test_level_3(self):
        level = 3
        input = "test is Hedy\nprint Hello I am test"
        output = runAST.complete_tester(input, level)
        expected = "test is Hedy\nprint 'Hello I am ' test\n"
        self.assertEqual(output, expected)

    def test_level_7(self):
        level = 7
        input = "amount is 5\nrepeat amount times print 'test!'\nif 20 is 20\nprint 'test'\nanswer is 20\nif answer is 20 print 'Yes!'"
        output = runAST.complete_tester(input, level)
        expected = "amount is 5\nrepeat amount times\n    print 'test!'\n\nif 20 is 20\n    print 'test'\n\nanswer is 20\nif answer is 20\n    print 'Yes!'\n\n"
        self.assertEqual(output, expected)

    def test_level_11(self):
        level = 11
        input = "superheroes = Spiderman, Batman, Iron Man\nprint superheroes at random\nif Batman in superheroes\n    print 'yay!'\nname = Hedy the Robot\nprint 'Hello ' name\nscore = 5+5\nprint 'You got ' score"
        output = runAST.complete_tester(input, level)
        expected = "superheroes = 'Spiderman', 'Batman', 'Iron Man'\nprint superheroes at random\nif 'Batman' in superheroes\n    print 'yay!'\n\nname = 'Hedy the Robot'\nprint 'Hello ' name\nscore = 5+5\nprint 'You got ' score\n"
        self.assertEqual(output, expected)

    def test_level_15(self):
        level = 15
        input = "antwoord is 0\nwhile antwoord != 25\n    antwoord is ask 'Wats is 5 keer 5?'\nprint 'Goed gedaan'\nfruit = 'apple', 'banana', 'cherry'\nprint fruit at random\nprint fruit at 2"
        output = runAST.complete_tester(input, level)
        expected = "antwoord is 0\nwhile antwoord != 25\n    antwoord is ask 'Wats is 5 keer 5?'\n\nprint 'Goed gedaan'\nfruit = ['apple', 'banana', 'cherry']\nprint fruit[random]\nprint fruit[2]\n"
        self.assertEqual(output, expected)

    def test_level_16(self):
        level = 16
        input = "numbers = [1, 2, 3]\nfor number in numbers\n    print number\nfruit = ['apple', 'banana']\nif 'apple' in fruit\n    print '2'\n    print 'test'\nelse\n    print 'failure'\nfor i in range 1 to 3\n    print 'testing ' i"
        output = runAST.complete_tester(input, level)
        expected = "numbers = [1, 2, 3]\nfor number in numbers:\n    print number\n\nfruit = ['apple', 'banana']\nif 'apple' in fruit:\n    print '2'\n    print 'test'\n\nelse:\n    print 'failure'\n\nfor i in range 1 to 3:\n    print 'testing ' i\n\n"
        self.assertEqual(output, expected)

    def test_level_17(self):
        level = 17
        input = "your_price = ask 'What is 5 times 5?'\nprint 'You win ' your_price"
        output = runAST.complete_tester(input, level)
        expected = "your_price = input ('What is 5 times 5?')\nprint ('You win ',your_price)\n"
        self.assertEqual(output, expected)
