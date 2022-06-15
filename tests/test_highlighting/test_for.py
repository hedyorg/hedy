from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestFor(HighlightTester):

    @parameterized.expand([
        ("level10"),
        ("level11"),
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
        ("level18"),
    ])
    def test_for(self, level):
        self.assert_highlighted_chr(
            "for animal in animals",
            "KKK TTTTTT KK TTTTTTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level11"),
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
        ("level18"),
    ])
    def test_for_range1(self, level):
        self.assert_highlighted_chr(
            "for i in range 1 to 3",
            "KKK T KK KKKKK N KK N",
            level=level, lang="en")

    @parameterized.expand([
        ("level11"),
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
        ("level18"),
    ])
    def test_for_range2(self, level):
        self.assert_highlighted_chr(
            "for i in range 1 to people",
            "KKK T KK KKKKK N KK TTTTTT",
            level=level, lang="en")
