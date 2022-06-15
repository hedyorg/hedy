from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestIfBlock(HighlightTester):



    @parameterized.expand([
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
    def test_if_is1(self, level):
        self.assert_highlighted_chr(
            "if answer is yes",
            "KK TTTTTT KK TTT",
            level=level, lang="en")

    @parameterized.expand([
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
    def test_if_is2(self, level):
        self.assert_highlighted_chr(
            "if answer is 'yes'",
            "KK TTTTTT KK SSSSS",
            level=level, lang="en")

    @parameterized.expand([
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
    def test_if_is3(self, level):
        self.assert_highlighted_chr(
            "if answer is 4242",
            "KK TTTTTT KK NNNN",
            level=level, lang="en")


    @parameterized.expand([
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
    def test_if_eq1(self, level):
        self.assert_highlighted_chr(
            "if answer == yes",
            "KK TTTTTT KK TTT",
            level=level, lang="en")

    @parameterized.expand([
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
    def test_if_eq2(self, level):
        self.assert_highlighted_chr(
            "if answer == 'yes'",
            "KK TTTTTT KK SSSSS",
            level=level, lang="en")

    @parameterized.expand([
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
    def test_if_eq3(self, level):
        self.assert_highlighted_chr(
            "if answer == 4242",
            "KK TTTTTT KK NNNN",
            level=level, lang="en")


    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_diff1(self, level):
        self.assert_highlighted_chr(
            "if answer != yes",
            "KK TTTTTT KK TTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_diff2(self, level):
        self.assert_highlighted_chr(
            "if answer != 'yes'",
            "KK TTTTTT KK SSSSS",
            level=level, lang="en")

    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_diff3(self, level):
        self.assert_highlighted_chr(
            "if answer != 4242",
            "KK TTTTTT KK NNNN",
            level=level, lang="en")



    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_sup1(self, level):
        self.assert_highlighted_chr(
            "if answer <= yes",
            "KK TTTTTT KK TTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_sup2(self, level):
        self.assert_highlighted_chr(
            "if answer <= 'yes'",
            "KK TTTTTT KK SSSSS",
            level=level, lang="en")

    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_sup3(self, level):
        self.assert_highlighted_chr(
            "if answer <= 4242",
            "KK TTTTTT KK NNNN",
            level=level, lang="en")



    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_inf1(self, level):
        self.assert_highlighted_chr(
            "if answer >= yes",
            "KK TTTTTT KK TTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_inf2(self, level):
        self.assert_highlighted_chr(
            "if answer >= 'yes'",
            "KK TTTTTT KK SSSSS",
            level=level, lang="en")

    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_inf3(self, level):
        self.assert_highlighted_chr(
            "if answer >= 4242",
            "KK TTTTTT KK NNNN",
            level=level, lang="en")


    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_in1(self, level):
        self.assert_highlighted_chr(
            "if answer in yes",
            "KK TTTTTT KK TTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_in2(self, level):
        self.assert_highlighted_chr(
            "if answer in 'yes'",
            "KK TTTTTT KK SSSSS",
            level=level, lang="en")

    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_in3(self, level):
        self.assert_highlighted_chr(
            "if answer in 4242",
            "KK TTTTTT KK NNNN",
            level=level, lang="en")






    @parameterized.expand([
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
    def test_else(self, level):
        self.assert_highlighted_chr(
            "else",
            "KKKK",
            level=level, lang="en")









    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_is1_or(self, level):
        self.assert_highlighted_chr(
            "if answer is var or answer is 'yes'",
            "KK TTTTTT KK TTT KK TTTTTT KK SSSSS",
            level=level, lang="en")


    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_is2_and(self, level):
        self.assert_highlighted_chr(
            "if answer is 246 and answer is 'yes'",
            "KK TTTTTT KK NNN KKK TTTTTT KK SSSSS",
            level=level, lang="en")


    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_eq1_or(self, level):
        self.assert_highlighted_chr(
            "if answer == var or answer != 'yes'",
            "KK TTTTTT KK TTT KK TTTTTT KK SSSSS",
            level=level, lang="en")


    @parameterized.expand([
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_if_eq2_and(self, level):
        self.assert_highlighted_chr(
            "if answer != 246 and answer == 'yes'",
            "KK TTTTTT KK NNN KKK TTTTTT KK SSSSS",
            level=level, lang="en")


