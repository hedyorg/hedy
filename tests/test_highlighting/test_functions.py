from parameterized import parameterized

from tests.Highlighter import HighlightTester


class HighlighterTestFunctions(HighlightTester):
    @parameterized.expand([
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
    ])
    def test_functions_1(self, level):
        self.assert_highlighted_chr_multi_line(
            "define function_1 with par1, par2",
            "FFFFFF TTTTTTTTTT KKKK TTTTK TTTT",
            "    return par1",
            "    KKKKKK TTTT",
            "call function_1 with 7, 'm'",
            "FFFF TTTTTTTTTT KKKK NK SSS",
            level=level, lang="en")

    def test_functions_2(self):
        self.assert_highlighted_chr_multi_line(
            "define function_1 with par1, par2:",
            "FFFFFF TTTTTTTTTT KKKK TTTTK TTTTK",
            "    return par1",
            "    KKKKKK TTTT",
            "call function_1 with 7, 'm'",
            "FFFF TTTTTTTTTT KKKK NK SSS",
            level='level17', lang="en")

    def test_functions_3(self):
        self.assert_highlighted_chr_multi_line(
            "def function_1(par1, par2):",
            "FFF TTTTTTTTTTKTTTTK TTTTKK",
            "    print(par1)",
            "    KKKKKKTTTTK",
            "function_1(7, 'df')",
            "TTTTTTTTTTKNK SSSSK",
            level='level18', lang="en")
