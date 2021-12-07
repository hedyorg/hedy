import hedy
from test_level_01 import HedyTester
import hedy_translation
from test_translating import check_local_lang_bool

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel9(HedyTester):
    level = 9
    keywords_from = hedy_translation.keywords_to_dict('en')
    keywords_to = hedy_translation.keywords_to_dict('nl')

    @check_local_lang_bool
    def test_double_repeat_indent_english_dutch(self):
        code = "repeat 3 times\n" \
               "    repeat 5 times\n" \
               "        print 'hi'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "herhaal 3 keer\n" \
                   "    herhaal 5 keer\n" \
                   "        print 'hi'"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_repeat_ifelse_english_dutch(self):
        code = "repeat 3 times\n" \
               "    if naam is hedy\n" \
               "        print 'hello'\n" \
               "    else\n" \
               "        repeat 2 times\n" \
               "            print 'oh'" \


        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "herhaal 3 keer\n" \
                   "    als naam is hedy\n" \
                   "        print 'hello'\n" \
                   "    anders\n" \
                   "        herhaal 2 keer\n" \
                   "            print 'oh'" \

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_multiple_ifelse_dutch_english(self):
        code = "als 10 is 10\n" \
               "    als 2 is 3\n" \
               "        print 'wat raar'\n" \
               "    anders\n" \
               "        print 'gelukkig'" \


        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "if 10 is 10\n" \
                   "    if 2 is 3\n" \
                   "        print 'wat raar'\n" \
                   "    else\n" \
                   "        print 'gelukkig'" \

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_indent_translate_back(self):
        code = "naam is hedy\n" \
               "if naam is hedy\n" \
               "    repeat 4 times\n" \
               "        print 'Hallo Hedy'\n" \
               "    print 'Hoe gaat het?'\n" \
               "else\n" \
               "    repeat 5 times\n" \
               "        print '5 keer'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        result = hedy_translation.translate_keywords(result, from_lang="nl", to_lang="en", level=self.level)

        self.assertEqual(code, result)