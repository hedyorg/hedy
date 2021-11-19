import hedy
import textwrap
from test_level_01 import HedyTester


class TestsTranslationLevel3(HedyTester):
    level = 3
    keywords = hedy.get_keywords_for_language('nl')

    def test_print(self):
        result = hedy.translate_keywords("print 'Hallo welkom bij Hedy!'", "en", "nl", self.level)
        expected = "drukaf 'Hallo welkom bij Hedy!'"

        self.assertEqual(result, expected)

    def test_print2(self):
        result = hedy.translate_keywords("print Hallo 'welkom bij Hedy!'", "en", "nl", self.level)
        expected = "drukaf Hallo 'welkom bij Hedy!'"

        self.assertEqual(result, expected)

    def test_print2(self):
        result = hedy.translate_keywords("print 'welkom bij Hedy!' Hallo", "en", "nl", self.level)
        expected = "drukaf 'welkom bij Hedy!' Hallo"

        self.assertEqual(result, expected)


    def test_assign(self):
        result = hedy.translate_keywords("Naam is 'Hedy'", "en", "nl", self.level)
        expected = "Naam is 'Hedy'"

        self.assertEqual(result, expected)

    def test_ask_assign(self):
        result = hedy.translate_keywords("mens is ask 'Hallo'", "en", "nl", self.level)
        expected = "mens is vraag 'Hallo'"

        self.assertEqual(result, expected)