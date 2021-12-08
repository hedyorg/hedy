import hedy
from test_level_01 import HedyTester
import hedy_translation
import textwrap


# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel11(HedyTester):
    level = 15

    def test_while_loop_english_dutch(self):
        code = textwrap.dedent("""\
        answer is 0
        while answer != 25
            answer is ask 'What is 5 * 5'
        print 'Good job!'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        answer is 0
        zolang answer != 25
            answer is vraag 'What is 5 * 5'
        print 'Good job!'""")

        self.assertEqual(result, expected)

    def test_while_loop_dutch_english(self):
        code = textwrap.dedent("""\
        answer is 0
        zolang answer != 25
            answer is vraag 'What is 5 * 5'
        print 'Good job!'""")

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = textwrap.dedent("""\
        answer is 0
        while answer != 25
            answer is ask 'What is 5 * 5'
        print 'Good job!'""")

        self.assertEqual(result, expected)

    def test_multiple_while_loop_english_dutch(self):
        code = textwrap.dedent("""\
        answer is 0
        while answer != 25
            while answer > 30
                answer is ask 'What is 5 * 5'
        print 'Good job!'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        answer is 0
        zolang answer != 25
            zolang answer > 30
                answer is vraag 'What is 5 * 5'
        print 'Good job!'""")

        self.assertEqual(result, expected)