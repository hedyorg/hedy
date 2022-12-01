from parameterized import parameterized

from tests.Highlighter import HighlightTester


class HighlighterTestTurtle(HighlightTester):

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
    ])
    def test_forward(self, level):
        self.assert_highlighted_chr(
            "forward 25",
            "KKKKKKK TT",
            level=level, lang="en")

    @parameterized.expand([
        ("level6"),
        ("level7"),
        ("level8"),
    ])
    def test_forward_number(self, level):
        self.assert_highlighted_chr(
            "forward 25",
            "KKKKKKK NN",
            level=level, lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
    ])
    def test_forward_alone(self, level):
        self.assert_highlighted_chr(
            "forward",
            "KKKKKKK",
            level=level, lang="en")

    def test_turn_left(self):
        self.assert_highlighted_chr(
            "turn left",
            "KKKK TTTT",
            level="level1", lang="en")

    def test_turn_right(self):
        self.assert_highlighted_chr(
            "turn right",
            "KKKK TTTTT",
            level="level1", lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
    ])
    def test_turn_alone(self, level):
        self.assert_highlighted_chr(
            "turn",
            "KKKK",
            level=level, lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
    ])
    def test_turn(self, level):
        self.assert_highlighted_chr(
            "turn 25",
            "KKKK TT",
            level=level, lang="en")

    @parameterized.expand([
        ("level6"),
        ("level7"),
        ("level8"),
    ])
    def test_turn_number(self, level):
        self.assert_highlighted_chr(
            "turn 25",
            "KKKK NN",
            level=level, lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
    ])
    def test_color_black(self, level):
        self.assert_highlighted_chr(
            "color black",
            "KKKKK TTTTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
    ])
    def test_color_blue(self, level):
        self.assert_highlighted_chr(
            "color blue",
            "KKKKK TTTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
    ])
    def test_color_brown(self, level):
        self.assert_highlighted_chr(
            "color brown",
            "KKKKK TTTTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
    ])
    def test_color_gray(self, level):
        self.assert_highlighted_chr(
            "color gray",
            "KKKKK TTTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
    ])
    def test_color_green(self, level):
        self.assert_highlighted_chr(
            "color green",
            "KKKKK TTTTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
    ])
    def test_color_orange(self, level):
        self.assert_highlighted_chr(
            "color orange",
            "KKKKK TTTTTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
    ])
    def test_color_pink(self, level):
        self.assert_highlighted_chr(
            "color pink",
            "KKKKK TTTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
    ])
    def test_color_purple(self, level):
        self.assert_highlighted_chr(
            "color purple",
            "KKKKK TTTTTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
    ])
    def test_color_red(self, level):
        self.assert_highlighted_chr(
            "color red",
            "KKKKK TTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
    ])
    def test_color_white(self, level):
        self.assert_highlighted_chr(
            "color white",
            "KKKKK TTTTT",
            level=level, lang="en")

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
        ("level4"),
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
    ])
    def test_color_yellow(self, level):
        self.assert_highlighted_chr(
            "color yellow",
            "KKKKK TTTTTT",
            level=level, lang="en")
