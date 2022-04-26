from tests.Highlighter import HighlightTester

class HighlighterTestLeveLbis(HighlightTester):


    def test_1(self):
        self.assertHighlighted2(
            "{print|kw} {hello world!|txt}",
            level="level1",lang='en')


    def test_2(self):
        self.assertHighlightedMultiLine2(
            "{print|kw} {Hello!|txt}",
            "{print|kw} {Welcome to Hedy!|txt}",
            level="level1",lang='en')


    def test_3(self):
        self.assertHighlightedMultiLine2(
            "{ask|kw} {What is your name?|txt}",
            "{echo|kw} {hello|txt}",
            level="level1",lang='en')
