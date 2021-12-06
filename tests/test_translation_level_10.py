import hedy
from test_level_01 import HedyTester
import hedy_translation
from test_translating import check_local_lang_bool

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel10(HedyTester):
    level = 10

    @check_local_lang_bool
    def test_for_english_dutch(self):
        code = "dieren is hond, kat, vis\n" \
               "for dier in dieren\n" \
               "    print 'hallo' dier"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "dieren is hond, kat, vis\n" \
                   "voor dier in dieren\n" \
                   "    print 'hallo' dier"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_for_dutch_english(self):
        code = "dieren is hond, kat, vis\n" \
               "voor dier in dieren\n" \
               "    voor animal in dieren\n" \
               "        print 'hallo' dier"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "dieren is hond, kat, vis\n" \
                   "for dier in dieren\n" \
                   "    for animal in dieren\n" \
                   "        print 'hallo' dier"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_repeat_translate_back(self):
        code = "dieren is hond, kat, vis\n" \
               "voor dier in dieren\n" \
               "    voor animal in dieren\n" \
               "        print 'hallo' dier"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        result = hedy_translation.translate_keywords(result, from_lang="en", to_lang="nl", level=self.level)

        self.assertEqual(result, code)