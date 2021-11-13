import hedy
import textwrap
from test_level_01 import HedyTester


class TestsTranslationLevel2(HedyTester):
    level = 2
    keywords = hedy.get_keywords_for_language('nl')

    def test_print(self):
        result = hedy.translate_keywords("print Hallo welkom bij Hedy!", "en", "nl", self.level)
        expected = "drukaf Hallo welkom bij Hedy!"

        self.assertEqual(result, expected)

    def test_print_multiple_lines(self):
        result = hedy.translate_keywords("print Hallo welkom bij Hedy!\nprint veel plezier", "en", "nl", self.level)
        expected = "drukaf Hallo welkom bij Hedy!\ndrukaf veel plezier"

        self.assertEqual(result, expected)

    def test_print_kewords(self):
        result = hedy.translate_keywords("print print ask echo", "en", "nl", self.level)
        expected = "drukaf print ask echo"

    def test_ask(self):
        result = hedy.translate_keywords("mens is ask Hallo welkom bij Hedy!", "en", "nl", self.level)
        expected = "mens is vraag Hallo welkom bij Hedy!"

        self.assertEqual(result, expected)

    def test_ask_multiple_lines(self):
        result = hedy.translate_keywords("welkom is ask Hallo welkom bij Hedy!\nplezier is ask veel plezier", "en", "nl", self.level)
        expected = "welkom is vraag Hallo welkom bij Hedy!\nplezier is vraag veel plezier"

        self.assertEqual(result, expected)

    def test_ask_kewords(self):
        result = hedy.translate_keywords("hedy is vraag print ask echo", "en", "nl", self.level)
        expected = "hedy is vraag print ask echo"
