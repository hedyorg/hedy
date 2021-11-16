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

    def test_ask_assign(self):
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

        self.assertEqual(result, expected)

    def test_ask_print(self):
        result = hedy.translate_keywords("hedy is hello\nprint hedy", "en", "nl", self.level)
        expected = "hedy is hello\ndrukaf hedy"

        self.assertEqual(result, expected)

    def test_assign_list(self):
        result = hedy.translate_keywords("mens is papa mama oma", "en", "nl", self.level)
        expected = "mens is papa mama oma"

        self.assertEqual(result, expected)

    def test_acces_list(self):
        result = hedy.translate_keywords("mens is papa mama oma\nprint mens at random", "en", "nl", self.level)
        expected = "mens is papa mama oma\ndrukaf mens opplek willekeurig"

        self.assertEqual(result, expected)

    def test_forward(self):
        result = hedy.translate_keywords("forward 50", "en", "nl", self.level)
        expected = "vooruit 50"

        self.assertEqual(result, expected)

    def test_turn(self):
        result = hedy.translate_keywords("turn left", "en", "nl", self.level)
        expected = "draai left"

        self.assertEqual(result, expected)

    def test_turn_value(self):
        result = hedy.translate_keywords("turn 50", "en", "nl", self.level)
        expected = "draai 50"

        self.assertEqual(result, expected)

    def test_forward_assigned_value(self):
        result = hedy.translate_keywords("value is 50\nforward value", "en", "nl", self.level)
        expected = "value is 50\nvooruit value"

        self.assertEqual(result, expected)
