import hedy
from test_level_01 import HedyTester
import hedy_translation
from test_translating import check_local_lang_bool

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel11(HedyTester):
    level = 11
    keywords_from = hedy_translation.keywords_to_dict('en')
    keywords_to = hedy_translation.keywords_to_dict('nl')

    @check_local_lang_bool
    def test_for_in_english_dutch(self):
        code = "for counter in range 1 to 5\n" \
               "    print counter"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "voor counter in bereik 1 tot 5\n" \
                   "    print counter"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_for_in_dutch_english(self):
        code = "nummer is vraag 'hoe oud ben je'\n" \
               "voor counter in bereik 1 tot 5\n" \
               "    voor count in bereik nummer tot 0\n" \
               "        print 'hoi' counter"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "nummer is ask 'hoe oud ben je'\n" \
                   "for counter in range 1 to 5\n" \
                   "    for count in range nummer to 0\n" \
                   "        print 'hoi' counter"

        self.assertEqual(result, expected)