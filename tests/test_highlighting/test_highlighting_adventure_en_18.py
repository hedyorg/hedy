from tests.Highlighter import HighlightTester

class HighlighterTestLeveL18(HighlightTester):

    def test_1(self):
        self.assertHighlightedMultiLine(
            "naam = 'Hedy'",
            "TTTT K SSSSSS",
            "print('My name is ', naam)",
            "KKKKKKSSSSSSSSSSSSSK TTTTK",
            level="level18",lang='en')


    def test_2(self):
        self.assertHighlightedMultiLine(
            "print('my name is Hedy!')",
            "KKKKKKSSSSSSSSSSSSSSSSSSK",
            "name = 'Hedy'",
            "TTTT K SSSSSS",
            "print('my name is ', name)",
            "KKKKKKSSSSSSSSSSSSSK TTTTK",
            level="level18",lang='en')


    def test_3(self):
        self.assertHighlighted(
            "print ('Great job!!!')",
            "KKKKK KSSSSSSSSSSSSSSK",
            level="level18",lang='en')
