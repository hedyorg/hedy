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
    level = 14

    def test_bigger(self):
        code = textwrap.dedent("""\
        hedy is 5
        if hedy > 6
            print 'hedy'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy is 5
        als hedy > 6
            print 'hedy'""")

        self.assertEqual(result, expected)

    def test_smaller(self):
        code = textwrap.dedent("""\
        hedy is 5
        if hedy < 6
            print 'hedy'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy is 5
        als hedy < 6
            print 'hedy'""")

        self.assertEqual(result, expected)

    def test_bigger_equal(self):
        code = textwrap.dedent("""\
        hedy is 5
        if hedy >= 6
            print 'hedy'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy is 5
        als hedy >= 6
            print 'hedy'""")

        self.assertEqual(result, expected)

    def test_smaller_equal(self):
        code = textwrap.dedent("""\
        hedy is 5
        if hedy <= 6
            print 'hedy'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy is 5
        als hedy <= 6
            print 'hedy'""")

        self.assertEqual(result, expected)

    def test_not_equal(self):
        code = textwrap.dedent("""\
        hedy is 5
        if hedy != 6
            print 'hedy'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy is 5
        als hedy != 6
            print 'hedy'""")

        self.assertEqual(result, expected)