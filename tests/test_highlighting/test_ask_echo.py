from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestAskEcho(HighlightTester):



    def test_echo_alone(self):
        self.assert_highlighted_chr(
            "echo",
            "KKKK",
            level="level1", lang="en")


    def test_echo1(self):
        self.assert_highlighted_chr(
            "echo aavhzrbz",
            "KKKK TTTTTTTT",
            level="level1", lang="en")


    def test_echo2(self):
        self.assert_highlighted_chr(
            "echo Jouw naam is",
            "KKKK TTTTTTTTTTTT",
            level="level1", lang="en")


    def test_ask1(self):
        self.assert_highlighted_chr(
            "ask aavhzrbz",
            "KKK TTTTTTTT",
            level="level1", lang="en")


    def test_ask2(self):
        self.assert_highlighted_chr(
            "ask What would you like to order?",
            "KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level1", lang="en")


