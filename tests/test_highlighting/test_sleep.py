from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestSleep(HighlightTester):


    @parameterized.expand([
        ("level2"),
        ("level3"),
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
    def test_sleep_alone(self, level):
        self.assert_highlighted_chr(
            "sleep",
            "KKKKK",
            level=level, lang="en")



    @parameterized.expand([
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
    ])
    def test_sleep(self, level):
        self.assert_highlighted_chr(
            "sleep 12",
            "KKKKK TT",
            level=level, lang="en")


    @parameterized.expand([
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
    def test_sleep_number(self, level):
        self.assert_highlighted_chr(
            "sleep 12",
            "KKKKK NN",
            level=level, lang="en")


    @parameterized.expand([
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
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
    def test_sleep_var(self, level):
        self.assert_highlighted_chr(
            "sleep var",
            "KKKKK TTT",
            level=level, lang="en")
