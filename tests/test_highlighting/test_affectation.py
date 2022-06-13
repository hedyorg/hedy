from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestAffectation(HighlightTester):


    @parameterized.expand([
        ("level2"),
        ("level3"),
    ])
    def test_is(self, level):
        self.assert_highlighted_chr(
            "sword is lost",
            "TTTTT KK TTTT",
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
            "sword is 'lost'",
            "TTTTT KK SSSSSS",
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
            "sword = 'lost'",
            "TTTTT K SSSSSS",
            level=level, lang="en")





