from tests.Highlighter import HighlightTester,SimulatorAce

RULES = {
    "rules1" : {'start': [{'regex': 'b', 'token': 'keyword', 'next': 'StateB'}, {'regex': 'a', 'token': 'constant.character', 'next': 'StateA'}, {'regex': '[^abc]', 'token': 'comment', 'next': 'start'}], 'StateA': [{'regex': '[^c]', 'token': 'invalid', 'next': 'StateA'}, {'regex': 'c', 'token': 'keyword', 'next': 'StateA'}], 'StateB': [{'regex': '[^c]', 'token': 'variable', 'next': 'StateB'}]},
    "rules2" : {'start': [{'regex': 'b', 'token': 'keyword', 'next': 'StateB'}, {'regex': 'ba', 'token': 'constant.character', 'next': 'StateA'}, {'regex': '[^abcd]', 'token': 'comment', 'next': 'start'}], 'StateA': [{'regex': '[^c]', 'token': 'invalid', 'next': 'StateA'}, {'regex': 'c', 'token': 'keyword', 'next': 'StateA'}], 'StateB': [{'regex': '[^c]', 'token': 'variable', 'next': 'StateB'}]},
    "rules3" : {'start': [{'regex': 'ba', 'token': 'constant.character', 'next': 'StateA'}, {'regex': 'b', 'token': 'keyword', 'next': 'StateB'}, {'regex': '[^abcd]', 'token': 'comment', 'next': 'start'}], 'StateA': [{'regex': '[^c]', 'token': 'invalid', 'next': 'StateA'}, {'regex': 'c', 'token': 'keyword', 'next': 'StateA'}], 'StateB': [{'regex': '[^c]', 'token': 'variable', 'next': 'StateB'}]},
    "rules4" : {'start': [{'regex': '[ac]', 'token': 'keyword', 'next': 'StateB'}, {'regex': '[bc]', 'token': 'constant.character', 'next': 'StateA'}, {'regex': 'tie\nmen', 'token': 'variable', 'next': 'start'}, {'regex': '[^abcd]', 'token': 'comment', 'next': 'start'}], 'StateA': [{'regex': '[^c]', 'token': 'invalid', 'next': 'StateA'}, {'regex': 'c', 'token': 'keyword', 'next': 'StateA'}, {'regex': '$', 'token': 'invalid', 'next': 'StateE'}], 'StateB': [{'regex': '[^c]', 'token': 'variable', 'next': 'StateB'}, {'regex': '$', 'token': 'invalid', 'next': 'StateE'}], 'StateE': [{'regex': 'e', 'token': 'variable', 'next': 'start'}, {'regex': 'Test', 'token': 'comment'}]},
}


class HighlighterTestLeveLSimulation(HighlightTester):

    def assert_highlighted_chr(self, code, expected, rule_name):

        rules = RULES[rule_name]

        self.check(code, expected, rules)



    def test_1(self):
        self.assert_highlighted_chr(
            "qmczqdqaqmcqbadqcc",
            "CCTCCCCSIIKIIIIIKK",
            rule_name="rules1")

    def test_2(self):
        self.assert_highlighted_chr(
            "qmczqdqbqmcqbadqcc",
            "CCTCCCCKNNTNNNNNTT",
            rule_name="rules1")



    def test_3(self):
        self.assert_highlighted_chr(
            "qmaaqgbeveqmcbazqdqaqmcqbadqcc",
            "CCTTCCKNNNNNTNNNNNNNNNTNNNNNTT",
            rule_name="rules2")

    def test_4(self):
        self.assert_highlighted_chr(
            "qmaaqgbaeveqmcbazqdqaqmcqbadqcc",
            "CCTTCCKNNNNNNTNNNNNNNNNTNNNNNTT",
            rule_name="rules2")

    def test_5(self):
        self.assert_highlighted_chr(
            "qmaaqgbeveqmcbazqdqaqmcqbadqcc",
            "CCTTCCKNNNNNTNNNNNNNNNTNNNNNTT",
            rule_name="rules3")

    def test_6(self):
        self.assert_highlighted_chr(
            "qmaaqgbaeveqmcbazqdqaqmcqbadqcc",
            "CCTTCCSSIIIIIKIIIIIIIIIKIIIIIKK",
            rule_name="rules3")






    def test_7(self):
        self.assert_highlighted_chr(
            "qmczqdqaqmcqbadq\ngrbnorbTestananaeqwswsmsazqdqaqmcqbadqcc\ngrbnorbTestananaeqwswsmsazqdqaqmcqbadqcc\n\ngrbnorbTestananaeqwswsmsbzqdqaqmcqbadqcc\ngrbnorbTestananaeqwswsmsazqdqaqmcqbadqcc\n\ngrbnorbTestananaeqwswsmsbzqdqaqmcqbadqcc",
            "CCKNNNNNNNTNNNNN\nNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNTNNNNNTT\nTTTTTTTCCCCTTTTTNCCCCCCCKNNNNNNNTNNNNNTT\n\nTTTTTTTCCCCTTTTTNCCCCCCCSIIIIIIIKIIIIIKK\nIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIKIIIIIKK\n\nTTTTTTTCCCCTTTTTNCCCCCCCSIIIIIIIKIIIIIKK",
            rule_name="rules4")




