from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestPrint(HighlightTester):

    @parameterized.expand([
        ("level1"),
        ("level2"),
        ("level3"),
    ])
    def test_print1(self, level):
        self.assert_highlighted_chr(
            "print hello world!",
            "KKKKK TTTTTTTTTTTT",
            level=level, lang='en')

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
            "print 'hello world!'",
            "KKKKK SSSSSSSSSSSSSS",
            level=level, lang='en')


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
    def test_print_incomplete1(self, level):
        self.assert_highlighted_chr(
            "print 'hello world!' var at random",
            "KKKKK SSSSSSSSSSSSSS TTT KK KKKKKK",
            level=level, lang='en')

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
    def test_print_incomplete2(self, level):
        self.assert_highlighted_chr(
            "print 'hello world! var at random",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
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
    def test_print_random_alone(self, level):
        self.assert_highlighted_chr(
            "print animals at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level=level, lang='en')



    def test_print_random1(self):
        self.assert_highlighted_chr(
            "print people at random does the dishes",
            "KKKKK TTTTTT KK KKKKKK TTTTTTTTTTTTTTT",
            level="level3", lang='en')

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
            "print 'The' people at random 'does the dishes'",
            "KKKKK SSSSS TTTTTT KK KKKKKK SSSSSSSSSSSSSSSSS",
            level=level, lang='en')


    def test_print_at1(self):
        self.assert_highlighted_chr(
            "print people at 3 does the dishes",
            "KKKKK TTTTTT KK T TTTTTTTTTTTTTTT",
            level="level3", lang='en')

    @parameterized.expand([
        ("level4"),
        ("level5"),
    ])
    def test_print_at2(self, level):
        self.assert_highlighted_chr(
            "print 'The' people at 3 'does the dishes'",
            "KKKKK SSSSS TTTTTT KK T SSSSSSSSSSSSSSSSS",
            level=level, lang='en')

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
    def test_print_at3(self, level):
        self.assert_highlighted_chr(
            "print 'The' people at 3 'does the dishes'",
            "KKKKK SSSSS TTTTTT KK N SSSSSSSSSSSSSSSSS",
            level=level, lang='en')


    def test_print_18_1(self):
        self.assert_highlighted_chr(
            "print ('Great job!!!')",
            "KKKKK KSSSSSSSSSSSSSSK",
            level="level18", lang='en')

    def test_print_18_2(self):
        self.assert_highlighted_chr(
            "print('my name is ', name, 'my name is ')",
            "KKKKKKSSSSSSSSSSSSSK TTTTK SSSSSSSSSSSSSK",
            level="level18", lang='en')

