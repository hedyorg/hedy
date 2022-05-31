from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestComment(HighlightTester):

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
        ("level11"),
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
        ("level18"),
    ])
    def test_comment(self, level):
        self.assert_highlighted_chr(
            "# Maak jouw eigen code hier",
            "CCCCCCCCCCCCCCCCCCCCCCCCCCC",
            level=level, lang="en")
