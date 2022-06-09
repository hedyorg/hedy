from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestNumbers(HighlightTester):


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
    def test_is_number(self, level):
        self.assert_highlighted_chr(
            "sword is 12346",
            "TTTTT KK NNNNN",
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
    def test_is_number_equal(self, level):
        self.assert_highlighted_chr(
            "sword = 12346",
            "TTTTT K NNNNN",
            level=level, lang="en")

    @parameterized.expand([
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_is_number_equal_float(self, level):
        self.assert_highlighted_chr(
            "sword = 123.46",
            "TTTTT K NNNNNN",
            level=level, lang="en")

    @parameterized.expand([
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_is_number_equal_float(self, level):
        self.assert_highlighted_chr(
            "sword is 123.46",
            "TTTTT KK NNNNNN",
            level=level, lang="en")

    @parameterized.expand([
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
        ("level11"),
    ])
    def test_is_number_equal_float_unknow(self, level):
        self.assert_highlighted_chr(
            "sword = 123.46",
            "TTTTT K NNNTTT",
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
    def test_is_number_equal_plus(self, level):
        self.assert_highlighted_chr(
            "sword = 12346 + 78564",
            "TTTTT K NNNNN K NNNNN",
            level=level, lang="en")


    @parameterized.expand([
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_is_number_equal_float_plus(self, level):
        self.assert_highlighted_chr(
            "sword = 123.46 + 7949.8",
            "TTTTT K NNNNNN K NNNNNN",
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
    def test_is_number_equal_minus(self, level):
        self.assert_highlighted_chr(
            "sword = 12346 - 78564",
            "TTTTT K NNNNN K NNNNN",
            level=level, lang="en")


    @parameterized.expand([
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_is_number_equal_float_minus(self, level):
        self.assert_highlighted_chr(
            "sword = 123.46 - 7949.8",
            "TTTTT K NNNNNN K NNNNNN",
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
    def test_is_number_equal_multi(self, level):
        self.assert_highlighted_chr(
            "sword = 12346 * 78564",
            "TTTTT K NNNNN K NNNNN",
            level=level, lang="en")


    @parameterized.expand([
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_is_number_equal_float_multi(self, level):
        self.assert_highlighted_chr(
            "sword = 123.46 * 7949.8",
            "TTTTT K NNNNNN K NNNNNN",
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
    def test_is_number_equal_div(self, level):
        self.assert_highlighted_chr(
            "sword = 12346 / 78564",
            "TTTTT K NNNNN K NNNNN",
            level=level, lang="en")


    @parameterized.expand([
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_is_number_equal_float_div(self, level):
        self.assert_highlighted_chr(
            "sword = 123.46 / 7949.8",
            "TTTTT K NNNNNN K NNNNNN",
            level=level, lang="en")