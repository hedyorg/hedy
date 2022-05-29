from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestList(HighlightTester):


    def test_list(self):
        self.assert_highlighted_chr(
            "sword is l ost, 12, aver i",
            "TTTTT KK TTTTTT TTT TTTTTT",
            level="level3", lang="en")


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
    def test_list_string(self, level):
        self.assert_highlighted_chr(
            "sword is 'l ost', '12', 'aver i'",
            "TTTTT KK SSSSSSSK SSSSK SSSSSSSS",
            level=level, lang="en")


    @parameterized.expand([
        ("level5"),
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
        ("level11"),
    ])
    def test_list_string_smiley(self, level):
        self.assert_highlighted_chr(
            "variable is 🦔, 🦉, 🐿, 🦇",
            "TTTTTTTT KK TK TK TK T",
            level=level, lang="en")



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
    def test_list_string_equ(self, level):
        self.assert_highlighted_chr(
            "sword = 'lost', '1 2', 'ave ri'",
            "TTTTT K SSSSSSK SSSSSK SSSSSSSS",
            level=level, lang="en")


    @parameterized.expand([
        ("level6"),
        ("level7"),
        ("level8"),
        ("level9"),
        ("level10"),
        ("level11"),
    ])
    def test_list_string_equ_smiley(self, level):
        self.assert_highlighted_chr(
            "variable = 🦔, 🦉, 🐿, 🦇",
            "TTTTTTTT K TK TK TK T",
            level=level, lang="en")



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
    def test_list_number(self, level):
        self.assert_highlighted_chr(
            "sword is 'l ost', 12, 'aver i', 1 , 3, 3",
            "TTTTT KK SSSSSSSK NNK SSSSSSSSK N K NK N",
            level=level, lang="en")

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
    def test_list_number_equ(self, level):
        self.assert_highlighted_chr(
            "sword = 'l ost', 12, 'aver i', 1 , 3, 3",
            "TTTTT K SSSSSSSK NNK SSSSSSSSK N K NK N",
            level=level, lang="en")


    @parameterized.expand([
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_list_number_float(self, level):
        self.assert_highlighted_chr(
            "sword is 'l ost', 12, 'aver i', 1.97 , 3.5, 3",
            "TTTTT KK SSSSSSSK NNK SSSSSSSSK NNNN K NNNK N",
            level=level, lang="en")

    @parameterized.expand([
        ("level12"),
        ("level13"),
        ("level14"),
        ("level15"),
        ("level16"),
        ("level17"),
    ])
    def test_list_number_equ_float(self, level):
        self.assert_highlighted_chr(
            "sword = 'l ost', 12, 'aver i', 1.97 , 3.5, 3",
            "TTTTT K SSSSSSSK NNK SSSSSSSSK NNNN K NNNK N",
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
    def test_list_add(self, level):
        self.assert_highlighted_chr(
            "add penguin to animals",
            "KKK TTTTTTT KK TTTTTTT",
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
    def test_list_remove(self, level):
        self.assert_highlighted_chr(
            "remove allergies from flavors",
            "KKKKKK TTTTTTTTT KKKK TTTTTTT",
            level=level, lang="en")
