from tests.Highlighter import HighlightTester
from parameterized import parameterized

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
            "KKKK KKKK",
            level="level1", lang="en")

    def test_turn_right(self):
        self.assert_highlighted_chr(
            "turn right",
            "KKKK KKKKK",
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