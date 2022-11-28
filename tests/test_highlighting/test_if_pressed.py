from parameterized import parameterized

from tests.Highlighter import HighlightTester


class HighlighterTestIfPressed(HighlightTester):

    @parameterized.expand([
        ("level5"),
        ("level6"),
        ("level7"),
    ])
    def test_if_is_pressed(self, level):
        self.assert_highlighted_chr(
            "if x is pressed",
            "KK T KK EEEEEEE",
            level=level, lang="en")

    @parameterized.expand([
        ("level5"),
        ("level6"),
        ("level7"),
    ])
    def test_if_is_pressed_print(self, level):
        self.assert_highlighted_chr(
            "if x is pressed print 'Yay!'",
            "KK T KK EEEEEEE KKKKK SSSSSS",
            level=level, lang="en")

    @parameterized.expand([
        ("level5"),
        ("level6"),
        ("level7"),
    ])
    def test_if_is_pressed_print_else_print(self, level):
        self.assert_highlighted_chr(
            "if x is pressed print 'Yay!' else print 'Boo!'",
            "KK T KK EEEEEEE KKKKK SSSSSS KKKK KKKKK SSSSSS",
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
    def test_if_is_pressed1(self, level):
        self.assert_highlighted_chr(
            "if x is pressed",
            "KK T KK EEEEEEE",
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
    def test_if_is_pressed_print1(self, level):
        self.assert_highlighted_chr_multi_line(
            "if x is pressed",
            "KK T KK EEEEEEE",
            "    print 'Yay!'",
            "    KKKKK SSSSSS",
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
    def test_if_is_pressed_print_else_print1(self, level):
        self.assert_highlighted_chr_multi_line(
            "if x is pressed",
            "KK T KK EEEEEEE",
            "    print 'Yay!'",
            "    KKKKK SSSSSS",
            "else",
            "KKKK",
            "    print 'Boo!'",
            "    KKKKK SSSSSS",
            level=level, lang="en")
