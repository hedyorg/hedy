from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestInput(HighlightTester):


    @parameterized.expand([
        ("level2"),
        ("level3"),
    ])
    def test_is(self, level):
        self.assert_highlighted_chr(
            "sword is ask l ost",
            "TTTTT KK KKK T TTT",
            level=level, lang="en")


    @parameterized.expand([
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
        ("level11"),
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_is_string(self, level):
        self.assert_highlighted_chr(
            "sword is ask 'lo R st'",
            "TTTTT KK KKK SSSSSSSSS",
            level=level, lang="en")


    @parameterized.expand([
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
        ("level11"),
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_is_string_equal(self, level):
        self.assert_highlighted_chr(
            "sword = ask 'lo st'",
            "TTTTT K KKK SSSSSSS",
            level=level, lang="en")

