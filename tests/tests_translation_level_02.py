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


class TestsTranslationLevel2(HedyTester):
    level = 2

    def test_print(self):
        code = "print Hallo welkom bij Hedy!"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "print Hallo welkom bij Hedy!"

        self.assertEqual(result, expected)

    def test_print_kewords(self):
        code = "print print ask echo"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "print print ask echo"

        self.assertEqual(result, expected)

    def test_ask_assign_dutch_english(self):
        code = "mens is vraag Hallo welkom bij Hedy!"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "mens is ask Hallo welkom bij Hedy!"

        self.assertEqual(result, expected)

    def test_ask_assign_english_dutch(self):
        code = "mens is ask Hallo welkom bij Hedy!"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "mens is vraag Hallo welkom bij Hedy!"

        self.assertEqual(result, expected)

    def test_ask_multiple_lines(self):
        code = "welkom is ask Hallo welkom bij Hedy!\nplezier is ask veel plezier"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "welkom is vraag Hallo welkom bij Hedy!\nplezier is vraag veel plezier"

        self.assertEqual(result, expected)

    def test_ask_kewords(self):
        code = "hedy is vraag print ask echo"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "hedy is vraag print ask echo"

        self.assertEqual(result, expected)

    def test_ask_print(self):
        code = "hedy is hello\nprint hedy"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "hedy is hello\nprint hedy"

        self.assertEqual(result, expected)

    def test_assign_list(self):
        code = "mens is papa mama oma"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "mens is papa mama oma"

        self.assertEqual(result, expected)

    def test_acces_list_english_dutch(self):
        code = "mens is papa mama oma\nprint mens at random"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "mens is papa mama oma\nprint mens opplek willekeurig"

        self.assertEqual(result, expected)

    def test_acces_list_dutch_english(self):
        code = "mens is papa mama oma\nprint mens opplek willekeurig"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "mens is papa mama oma\nprint mens at random"

        self.assertEqual(result, expected)

    def test_forward_assigned_value(self):
        code = "value is 50\nforward value"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "value is 50\nvooruit value"

        self.assertEqual(result, expected)

    def test_translate_back(self):
        code = "print welkom bij Hedy\nnaam is ask what is your name\nprint naam"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)

        expected = "print welkom bij Hedy\nnaam is ask what is your name\nprint naam"

        self.assertEqual(result, expected)

    def test_invalid(self):
        code = "hallo"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "hallo"

        self.assertEqual(result, expected)

    def test_invalid_space(self):
        code = " print Hedy"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = " print Hedy"

        self.assertEqual(result, expected)

    def no_argument_ask(self):
        code = "ask"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "vraag"

        self.assertEqual(result, expected)