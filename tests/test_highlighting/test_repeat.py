from tests.Highlighter import HighlightTester
from parameterized import parameterized

class HighlighterTestRepeat(HighlightTester):


    @parameterized.expand([
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
    def test_repeat_print(self, lang):
        self.assert_highlighted_chr(
            "repeat 3 times print 'Hedy is fun!'",
            'KKKKKK N KKKKK KKKKK SSSSSSSSSSSSSS',
            level=lang, lang="en")

    @parameterized.expand([
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
    ])
    def test_repeat_ask(self, lang):
        self.assert_highlighted_chr(
            "repeat 3 times question is ask 'What do you want to know?'",
            'KKKKKK N KKKKK TTTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSS',
            level=lang, lang="en")



    @parameterized.expand([
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
    def test_repeat_alone(self, lang):
        self.assert_highlighted_chr(
            "repeat people times",
            'KKKKKK TTTTTT KKKKK',
            level=lang, lang="en")

    @parameterized.expand([
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
    def test_repeat_number(self, lang):
        self.assert_highlighted_chr(
            "repeat 99 times",
            'KKKKKK NN KKKKK',
            level=lang, lang="en")