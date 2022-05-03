from tests.Highlighter import HighlightTester

RULES = {
    "rules1" : {'start': [{'regex': 'b', 'token': 'keyword', 'next': 'StateB'}, {'regex': 'a', 'token': 'constant.character', 'next': 'StateA'}, {'regex': '[^abc]', 'token': 'comment', 'next': 'start'}], 'StateA': [{'regex': '[^c]', 'token': 'invalid', 'next': 'StateA'}, {'regex': 'c', 'token': 'keyword', 'next': 'StateA'}], 'StateB': [{'regex': '[^c]', 'token': 'variable', 'next': 'StateB'}]},
    "rules2" : {'start': [{'regex': 'b', 'token': 'keyword', 'next': 'StateB'}, {'regex': 'ba', 'token': 'constant.character', 'next': 'StateA'}, {'regex': '[^abcd]', 'token': 'comment', 'next': 'start'}], 'StateA': [{'regex': '[^c]', 'token': 'invalid', 'next': 'StateA'}, {'regex': 'c', 'token': 'keyword', 'next': 'StateA'}], 'StateB': [{'regex': '[^c]', 'token': 'variable', 'next': 'StateB'}]},
    "rules3" : {'start': [{'regex': 'ba', 'token': 'constant.character', 'next': 'StateA'}, {'regex': 'b', 'token': 'keyword', 'next': 'StateB'}, {'regex': '[^abcd]', 'token': 'comment', 'next': 'start'}], 'StateA': [{'regex': '[^c]', 'token': 'invalid', 'next': 'StateA'}, {'regex': 'c', 'token': 'keyword', 'next': 'StateA'}], 'StateB': [{'regex': '[^c]', 'token': 'variable', 'next': 'StateB'}]},
    "rules4" : {'start': [{'regex': '[ac]', 'token': 'keyword', 'next': 'StateB'}, {'regex': '[bc]', 'token': 'constant.character', 'next': 'StateA'}, {'regex': 'tie\nmen', 'token': 'variable', 'next': 'start'}, {'regex': '[^abcd]', 'token': 'comment', 'next': 'start'}], 'StateA': [{'regex': '[^c]', 'token': 'invalid', 'next': 'StateA'}, {'regex': 'c', 'token': 'keyword', 'next': 'StateA'}, {'regex': '$', 'token': 'invalid', 'next': 'StateE'}], 'StateB': [{'regex': '[^c]', 'token': 'variable', 'next': 'StateB'}, {'regex': '$', 'token': 'invalid', 'next': 'StateE'}], 'StateE': [{'regex': 'e', 'token': 'variable', 'next': 'start'}, {'regex': 'Test', 'token': 'comment'}]},
}


class HighlighterTestLeveLSimulation(HighlightTester):

    def assertHighlightedChr(self,code,expected,ruleName):

        rules = RULES[ruleName]
        
        result = self.applyRules(rules,code)

        valid, indError = self.check(result,expected)
        if not valid:
            print("ERROR with the set of rule : {}".format(ruleName))
            print("In this code :",code.replace("\n","\\n"))
            print("We want      :",expected.replace("\n","\\n"))
            print("We have      :",result.replace("\n","\\n"))
            print("At           :"," " * indError + "^")
        self.assertTrue(valid)



    def test_1(self):
        self.assertHighlightedChr(
            "qmczqdqaqmcqbadqcc",
            "CCTCCCCSIIKIIIIIKK",
            ruleName="rules1")

    def test_2(self):
        self.assertHighlightedChr(
            "qmczqdqbqmcqbadqcc",
            "CCTCCCCKNNTNNNNNTT",
            ruleName="rules1")




    def test_3(self):
        self.assertHighlightedChr(
            "qmaaqgbeveqmcbazqdqaqmcqbadqcc",
            "CCTTCCKNNNNNTNNNNNNNNNTNNNNNTT",
            ruleName="rules2")

    def test_4(self):
        self.assertHighlightedChr(
            "qmaaqgbaeveqmcbazqdqaqmcqbadqcc",
            "CC  CCKNNNNNN NNNNNNNNN NNNNN  ",
            ruleName="rules2")

    def test_5(self):
        self.assertHighlightedChr(
            "qmaaqgbeveqmcbazqdqaqmcqbadqcc",
            "CCTTCCKNNNNNTNNNNNNNNNTNNNNNTT",
            ruleName="rules3")

    def test_6(self):
        self.assertHighlightedChr(
            "qmaaqgbaeveqmcbazqdqaqmcqbadqcc",
            "CCTTCCSSIIIIIKIIIIIIIIIKIIIIIKK",
            ruleName="rules3")






    def test_7(self):
        self.assertHighlightedChr(
            "qmczqdqaqmcqbadq\ngrbnorbTestananaeqwswsmsazqdqaqmcqbadqcc\ngrbnorbTestananaeqwswsmsazqdqaqmcqbadqcc\n\ngrbnorbTestananaeqwswsmsbzqdqaqmcqbadqcc\ngrbnorbTestananaeqwswsmsazqdqaqmcqbadqcc\n\ngrbnorbTestananaeqwswsmsbzqdqaqmcqbadqcc",
            "CCKNNNNNNN NNNNN\nNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN NNNNN  \n       CCCC     NCCCCCCCKNNNNNNN NNNNN  \n\n       CCCC     NCCCCCCCSIIIIIIIKIIIIIKK\nIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIKIIIIIKK\n\n       CCCC     NCCCCCCCSIIIIIIIKIIIIIKK",
            ruleName="rules4")




