import hedy
from test_level_01 import HedyTester
import hedy_translation
from test_translating import check_local_lang_bool

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel8(HedyTester):
    level = 8
    keywords_from = hedy_translation.keywords_to_dict('en')
    keywords_to = hedy_translation.keywords_to_dict('nl')

    @check_local_lang_bool
    def test_repeat_indent_english_dutch(self):
        code = "repeat 3 times\n" \
               "    print 'Hedy is fun!'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "herhaal 3 keer\n" \
                   "    print 'Hedy is fun!'"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_repeat_multiple_indent_english_dutch(self):
        code = "repeat 3 times\n" \
               "    print 'Hedy is fun!'\n" \
               "    print 'print 3 keer'\n" \
               "print 'print 1 keer'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "herhaal 3 keer\n" \
                   "    print 'Hedy is fun!'\n" \
                   "    print 'print 3 keer'\n" \
                   "print 'print 1 keer'"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_repeat_indent_dutch_english(self):
        code = "herhaal 3 keer\n" \
               "    print 'Hedy is fun!'"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "repeat 3 times\n" \
                   "    print 'Hedy is fun!'"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_ifelse_indent_dutch_english(self):
        code = "if naam is hedy\n" \
               "    print 'Hallo Hedy'\n" \
               "    print 'hoe gaat het?'\n" \
               "else\n" \
               "    print 'Hallo' hedy"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "als naam is hedy\n" \
                   "    print 'Hallo Hedy'\n" \
                   "    print 'hoe gaat het?'\n" \
                   "anders\n" \
                   "    print 'Hallo' hedy"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_indent_translate_back(self):
        code = "naam is hedy\n" \
               "if naam is hedy\n" \
               "    print 'Hallo Hedy'\n" \
               "    print 'Hoe gaat het?'\n" \
               "repeat 5 times\n" \
               "    print '5 keer'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        result = hedy_translation.translate_keywords(result, from_lang="nl", to_lang="en", level=self.level)

        self.assertEqual(code, result)