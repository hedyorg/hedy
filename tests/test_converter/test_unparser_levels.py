from tests.Tester import HedyTester
import runAST

# These tests are used to ensure that the unparser works for all Hedy levels.
# This is accomplished by comparing the parsing results of the input and output.
# The input should contain the new or updated commands, to test wether they
# work properly.
#
# If a test fails, this either means there is a problem with the unparser or
# with the grammar. Problems with the grammar will need to be specifically
# handled in the unparser.
#
# A template for future levels:
#    def test_level_(self):
#        level =
#        input = ""
#        output = runAST.unparser_tester(input, level)
#        expected = runAST.parser(input, level)
#        result = runAST.parser(output, level)
#        self.assertEqual(expected, result)


class TestsUnparserHedy(HedyTester):
    def test_level_1(self):
        level = 1
        input = "print hallo\nask wie ben jij?\necho oooh"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_2(self):
        level = 2
        input = "naam is Hedy\nprint hallo naam\nnaam2 is ask wie ben jij?\nprint ooooh naam2"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_3(self):
        level = 3
        input = "dieren is hond, kat, kangoeroe\nprint dieren at random"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_4(self):
        level = 4
        input = "print 'hallo tester'\nkleur is ask 'Wat is je lievelingskleur?'\nprint 'oh ' kleur\nnaam is 'Hedy'\nprint 'doei ' naam"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_5(self):
        level = 5
        input = "print 'hallo tester'\nmooie_kleuren is groen, paars\nkleur is ask 'Wat is je lievelingskleur?'\nif kleur is groen print 'Mooi zo' else print 'sucker'\nif kleur in mooie_kleuren print 'Mooi' else print 'meh'\n"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_6(self):
        level = 6
        input = "print '5 keer 5 is ' 5 * 5\nanswer is ask 'wat is 10 plus 10?'\nif answer is 20 print 'Yes!' else print 'Oeps'"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_7(self):
        level = 7
        input = "keer is 5\nrepeat keer times print 'test1!'"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_8(self):
        level = 8
        input = "keer is 5\nrepeat keer times\n    print 'test1!'\n    print 'test2'\nif keer is 5\n    print 'vijf keer!'\nelse\n    print 'oepsie'"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_9(self):
        level = 9
        input = "repeat 3 times\n    eten is ask 'Wat wil je bestellen?'\n    if eten is pizza\n        print 'lekker'\n    else\n        print 'pizza is lekkerder'"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_10(self):
        level = 10
        input = "dieren is hond, kat, papagaai\nfor dier in dieren\n    print dier ' is een leuk dier!'"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_11(self):
        level = 11
        input = "for i in range 1 to 10\n    print i\nprint 'Wie niet weg is is gezien'"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_12(self):
        level = 12
        input = "print 'Rekenen maar!'\nprint 'Tweeenhalf plus tweeenhalf is...'\nprint 2.5 * 2.5 * 2"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_13(self):
        level = 13
        input = "naam is ask 'hoe heet jij?'\nleeftijd is ask 'hoe oud ben jij?'\nif naam is 'Hedy' and leeftijd is 2\n    print 'Jij bent de echte Hedy!'"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_14(self):
        level = 14
        input = "leeftijd is ask 'Hoe oud ben jij?'\nif leeftijd < 13\n    print 'Dan ben je jonger dan ik!'"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_15(self):
        level = 15
        input = "antwoord is 0\nwhile antwoord != 25\n    antwoord is ask 'Wats is 5 keer 5?'\nprint 'Goed gedaan'"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)

    def test_level_16(self):
        level = 16
        input = "vrienden is ['Ahmed', 'Ben', 'Cayden']\ngeluksgetallen is [15, 18, 6]\nfor i in range 1 to 3\n    print 'het geluksgetal van ' vrienden[i]\n    print 'is ' geluksgetallen[i]"
        output = runAST.unparser_tester(input, level)
        expected = runAST.parser(input, level)
        result = runAST.parser(output, level)
        self.assertEqual(expected, result)
