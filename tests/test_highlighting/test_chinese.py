from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestPrintChinese(HighlightTester):

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
    ])
    def test_print1(self, level):
        self.assert_highlighted_chr(
            "打印 你好世界!",
            "KK TTTTT",
            level=level, lang='zh_Hans')

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
            "打印 '从现在开始你们需要使用引号！'",
            "KK SSSSSSSSSSSSSSSS",
            level=level, lang='zh_Hans')



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
    def test_print_random_alone(self, level):
        self.assert_highlighted_chr(
            "打印 动物们 在 随机",
            "KK TTT K KK",
            level=level, lang='zh_Hans')



    def test_print_random1(self):
        self.assert_highlighted_chr(
            "打印 从现在开始我们需要使用什么？ 答案 在 随机",
            "KK TTTTTTTTTTTTTT TT K KK",
            level="level3", lang='zh_Hans')

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
    def test_print_random2(self, level):
        self.assert_highlighted_chr(
            "打印 '从现在开始我们需要使用什么？' 答案 在 随机",
            "KK SSSSSSSSSSSSSSSS TT K KK",
            level=level, lang='zh_Hans')

