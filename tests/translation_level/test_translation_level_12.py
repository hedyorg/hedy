import hedy
from Tester import HedyTester
import hedy_translation
import textwrap


# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel12(HedyTester):
    level = 12

    def test_decimal_english_dutch(self):
        code = "print 2.5 + 2.5"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "print 2.5 + 2.5"

        self.assertEqual(expected, result)

    def test_text_in_quotes_english_dutch(self):
        code = "naam = 'hedy'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "naam = 'hedy'"

        self.assertEqual(expected, result)

    def test_text_in_quotes_ifs_english_dutch(self):
        code = textwrap.dedent("""\
        naam = 'hedy'
        if naam is 'hedy'
            print 'hallo ' naam""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        naam = 'hedy'
        als naam is 'hedy'
            print 'hallo ' naam""")

        self.assertEqual(expected, result)
