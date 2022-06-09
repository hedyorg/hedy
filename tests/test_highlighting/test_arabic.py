from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestPrintArabic(HighlightTester):

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
    ])
    def test_ar_print1(self, level):
        self.assert_highlighted_chr(
            "قول مرحبا أيها العالم!",
            "KKK TTTTTTTTTTTTTTTTTT",
            level=level, lang='ar')

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
    def test_ar_print2(self, level):
        self.assert_highlighted_chr(
            'قول "مرحبا أيها العالم"',
            "KKK SSSSSSSSSSSSSSSSSSS",
            level=level, lang='ar')



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
    def test_ar_print_random_alone(self, level):
        self.assert_highlighted_chr(
            "قول حيواناتي بشكل عشوائي",
            "KKK TTTTTTTT KKKK KKKKKK",
            level=level, lang='ar')



    def test_ar_print_random1(self):
        self.assert_highlighted_chr(
            "قول حيواناتي بشكل عشوائي مرحبا أيها العالم!",
            "KKK TTTTTTTT KKKK KKKKKK TTTTTTTTTTTTTTTTTT",
            level="level3", lang='ar')

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
    def test_ar_print_random2(self, level):
        self.assert_highlighted_chr(
            'قول حيواناتي بشكل عشوائي "مرحبا أيها العالم!"',
            "KKK TTTTTTTT KKKK KKKKKK SSSSSSSSSSSSSSSSSSSS",
            level=level, lang='ar')


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
    def test_ar_is_number_equal_plus(self, level):
        self.assert_highlighted_chr(
            "sword = ١٢٣٤٦ + ٧٨٥٦٤",
            "TTTTT K NNNNN K NNNNN",
            level=level, lang="ar")


    @parameterized.expand([
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_ar_is_number_equal_float_plus(self, level):
        self.assert_highlighted_chr(
            "sword = ١٢٣.٤٦ + ٧٩٤٩.٨",
            "TTTTT K NNNNNN K NNNNNN",
            level=level, lang="ar")


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
    def test_ar_print_mul(self, level):
        self.assert_highlighted_chr(
            'قول "مرحبا أيها العالم" ١٢٣٤٦ * ٧٩٤٩٨',
            "KKK SSSSSSSSSSSSSSSSSSS NNNNN K NNNNN",
            level=level, lang='ar')

    @parameterized.expand([
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_ar_print_div_float(self, level):
        self.assert_highlighted_chr(
            'قول "مرحبا أيها العالم" ١٢٣.٤٦ / ٧٩٤٩.٨',
            "KKK SSSSSSSSSSSSSSSSSSS NNNNNN K NNNNNN",
            level=level, lang='ar')

