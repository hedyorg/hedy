import hedy
import textwrap
from tests_level_01 import HedyTester


class TestsTranslationLevel3(HedyTester):
    level = 1
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
        result = hedy.translate_keywords("ask Hallo welkom bij Hedy!", "en", "nl", self.level)
        expected = "vraag Hallo welkom bij Hedy!"

        self.assertEqual(result, expected)

    def test_ask_multiple_lines(self):
        result = hedy.translate_keywords("ask Hallo welkom bij Hedy!\nask veel plezier", "en", "nl", self.level)
        expected = "vraag Hallo welkom bij Hedy!\nvraag veel plezier"

        self.assertEqual(result, expected)

    def test_ask_kewords(self):
        result = hedy.translate_keywords("vraag print ask echo", "en", "nl", self.level)
        expected = "vraag print ask echo"

    def test_echo(self):
        result = hedy.translate_keywords("ask Hallo welkom bij Hedy!\necho", "en", "nl", self.level)
        expected = "vraag Hallo welkom bij Hedy!\nherhaal"

        self.assertEqual(result, expected)

    def test_echo_text(self):
        result = hedy.translate_keywords("ask stel je vraag\necho tekst", "en", "nl", self.level)
        expected = "vraag stel je vraag\nherhaal tekst"

        self.assertEqual(result, expected)