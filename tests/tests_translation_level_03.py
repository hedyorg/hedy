import hedy
from test_level_01 import HedyTester
import hedy_translation


def check_local_lang_bool(func):
    def inner(self):
        if not hedy.local_keywords_enabled:
            return

        return func(self)

    return inner


    # tests should be ordered as follows:
    # * Translation from English to Dutch
    # * Translation from Dutch to English
    # * Translation to several languages
    # * Error handling

class TestsTranslationLevel3(HedyTester):
    level = 3

    def test_print(self):
        result = hedy_translation.translate_keywords("print 'Hallo welkom bij Hedy!'", "en", "nl", self.level)
        expected = "print 'Hallo welkom bij Hedy!'"

        self.assertEqual(result, expected)

    def test_print2(self):
        result = hedy_translation.translate_keywords("print Hallo 'welkom bij Hedy!'", "en", "nl", self.level)
        expected = "print Hallo 'welkom bij Hedy!'"

        self.assertEqual(result, expected)

    def test_print2(self):
        result = hedy_translation.translate_keywords("print 'welkom bij Hedy!' Hallo", "en", "nl", self.level)
        expected = "print 'welkom bij Hedy!' Hallo"

        self.assertEqual(result, expected)


    def test_assign(self):
        result = hedy_translation.translate_keywords("Naam is 'Hedy'", "en", "nl", self.level)
        expected = "Naam is 'Hedy'"

        self.assertEqual(result, expected)

    def test_ask_assign(self):
        result = hedy_translation.translate_keywords("mens is ask 'Hallo'", "en", "nl", self.level)
        expected = "mens is vraag 'Hallo'"

        self.assertEqual(result, expected)