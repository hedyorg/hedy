from parameterized import parameterized

from tests.Highlighter import HighlightTester


class HighlighterTestOverCol(HighlightTester):

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
    ])
    def test_is1(self, level):
        self.assert_highlighted_chr(
            "ask is lost",
            "TTT KK TTTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_is2(self, level):
        self.assert_highlighted_chr(
            "ask is 'lost'",
            "TTT KK SSSSSS",
            level=level, lang="en")

    @parameterized.expand([
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
        ("level11"),
    ])
    def test_Eq1(self, level):
        self.assert_highlighted_chr(
            "ask = lost",
            "TTT K TTTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_Eq2(self, level):
        self.assert_highlighted_chr(
            "ask = 'lost'",
            "TTT K SSSSSS",
            level=level, lang="en")

    @parameterized.expand([
        ("level2"),
        ("level3"),
    ])
    def test_print1(self, level):
        self.assert_highlighted_chr(
            "print hello world! ask",
            "KKKKK TTTTTTTTTTTTTTTT",
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
    def test_print2(self, level):
        self.assert_highlighted_chr(
            "print 'hello world!' ask",
            "KKKKK SSSSSSSSSSSSSS TTT",
            level=level, lang="en")

    @parameterized.expand([
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
    def test_at_prefix(self, level):
        self.assert_highlighted_chr(
            "print atoptis at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level=level, lang='en')

    @parameterized.expand([
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
    def test_at_prefix_nl(self, level):
        self.assert_highlighted_chr(
            "print optis at random",
            "KKKKK TTTTT KK KKKKKK",
            level=level, lang='nl')

    @parameterized.expand([
        ("level3"),
        ("level4"),
    ])
    def test_from_prefix(self, level):
        self.assert_highlighted_chr(
            "remove fromyour_name from people",
            "KKKKKK TTTTTTTTTTTTT KKKK TTTTTT",
            level=level, lang='en')

    @parameterized.expand([
        ("level3"),
        ("level4"),
    ])
    def test_from_prefix_nl(self, level):
        self.assert_highlighted_chr(
            "remove uitfromyour_name from people",
            "KKKKKK TTTTTTTTTTTTTTTT KKKK TTTTTT",
            level=level, lang='nl')

    @parameterized.expand([
        ("level3"),
        ("level4"),
    ])
    def test_to_prefix(self, level):
        self.assert_highlighted_chr(
            "add toanimal to animals",
            "KKK TTTTTTTT KK TTTTTTT",
            level=level, lang='en')
