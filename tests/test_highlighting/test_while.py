from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestWhile(HighlightTester):

    @parameterized.expand([
        ("level15"),
        ("level16"),
        ("level17"),
        ("level18"),
    ])
    def test_while_str(self, level):
        self.assert_highlighted_chr(
            "while keys == 'lost'",
            "KKKKK TTTT KK SSSSSS",
            level=level, lang="en")

    @parameterized.expand([
        ("level15"),
        ("level16"),
        ("level17"),
        ("level18"),
    ])
    def test_while_diff_str(self, level):
        self.assert_highlighted_chr(
            "while keys != 'lost'",
            "KKKKK TTTT KK SSSSSS",
            level=level, lang="en")


    @parameterized.expand([
        ("level15"),
        ("level16"),
        ("level17"),
        ("level18"),
    ])
    def test_while_number(self, level):
        self.assert_highlighted_chr(
            "while keys == 123",
            "KKKKK TTTT KK NNN",
            level=level, lang="en")

    @parameterized.expand([
        ("level15"),
        ("level16"),
        ("level17"),
        ("level18"),
    ])
    def test_while_diff_number(self, level):
        self.assert_highlighted_chr(
            "while keys != 123",
            "KKKKK TTTT KK NNN",
            level=level, lang="en")

    @parameterized.expand([
        ("level15"),
        ("level16"),
        ("level17"),
        ("level18"),
    ])
    def test_while_number(self, level):
        self.assert_highlighted_chr(
            "while keys == var",
            "KKKKK TTTT KK TTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level15"),
        ("level16"),
        ("level17"),
        ("level18"),
    ])
    def test_while_diff_number(self, level):
        self.assert_highlighted_chr(
            "while keys != var",
            "KKKKK TTTT KK TTT",
            level=level, lang="en")
