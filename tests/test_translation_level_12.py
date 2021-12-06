import hedy
from test_level_01 import HedyTester
import hedy_translation
from test_translating import check_local_lang_bool
import textwrap


# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel11(HedyTester):
    level = 12

    @check_local_lang_bool
    def test_decimal_english_dutch(self):
        code = "print 2.5 + 2.5"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "print 2.5 + 2.5"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_text_in_quotes_english_dutch(self):
        code = "naam is 'hedy'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "naam is 'hedy'"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_text_in_quotes_ifs_english_dutch(self):
        code = textwrap.dedent("naam is 'hedy'\n"
                               "if naam is 'hedy'\n"
                               "    print 'hallo ' naam")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("naam is 'hedy'\n"
                                   "als naam is 'hedy'\n"
                                   "    print 'hallo ' naam")

        self.assertEqual(result, expected)
