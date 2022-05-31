from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestIfInline(HighlightTester):

    @parameterized.expand([
        ("level5"),
        ("level6"),
        ("level7"),
    ])
    def test_if_print(self, level):
        self.assert_highlighted_chr(
            "if cat is chat print 'Terrific!' var at random",
            "KK TTT KK TTTT KKKKK SSSSSSSSSSS TTT KK KKKKKK",
            level=level, lang="en")


    def test_if_affectation1(self):
        self.assert_highlighted_chr(
            "if cat is 666 price is 5",
            "KK TTT KK TTT TTTTT KK T",
            level="level5", lang="en")

    @parameterized.expand([
        ("level6"),
        ("level7"),
    ])
    def test_if_affectation2(self, level):
        self.assert_highlighted_chr(
            "if cat is 666 price is 5",
            "KK TTT KK NNN TTTTT KK N",
            level=level, lang="en")

    @parameterized.expand([
        ("level6"),
        ("level7"),
    ])
    def test_if_affectation3(self, level):
        self.assert_highlighted_chr(
            "if cat is 666 price = 5 + 42",
            "KK TTT KK NNN TTTTT K N K NN",
            level=level, lang="en")


    @parameterized.expand([
        ("level5"),
        ("level6"),
        ("level7"),
    ])
    def test_if_else_print(self, level):
        self.assert_highlighted_chr(
            "if anything is no print 'Thats it!' goodanswer at random else print 'One ' anything at random",
            "KK TTTTTTTT KK TT KKKKK SSSSSSSSSSS TTTTTTTTTT KK KKKKKK KKKK KKKKK SSSSSS TTTTTTTT KK KKKKKK",
            level=level, lang="en")




    @parameterized.expand([
        ("level5"),
        ("level6"),
        ("level7"),
    ])
    def test_if_else_is(self, level):
        self.assert_highlighted_chr(
            "if anything is no var is test else var is azerty",
            "KK TTTTTTTT KK TT TTT KK TTTT KKKK TTT KK TTTTTT",
            level=level, lang="en")






    @parameterized.expand([
        ("level5"),
        ("level6"),
        ("level7"),
    ])
    def test_else_print(self, level):
        self.assert_highlighted_chr(
            "else print 'Oh no! You are being eaten by a...' monsters at random",
            "KKKK KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTTTT KK KKKKKK",
            level=level, lang="en")


    @parameterized.expand([
        ("level6"),
        ("level7"),
    ])
    def test_else_math(self, level):
        self.assert_highlighted_chr(
            "else price = 5 + 42",
            "KKKK TTTTT K N K NN",
            level=level, lang="en")

    @parameterized.expand([
        ("level6"),
        ("level7"),
    ])
    def test_else_is(self, level):
        self.assert_highlighted_chr(
            "else price is 5",
            "KKKK TTTTT KK N",
            level=level, lang="en")








