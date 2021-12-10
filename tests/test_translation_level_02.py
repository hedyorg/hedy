from test_translating import check_local_lang_bool
from test_level_01 import HedyTester
import hedy_translation


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

    def test_ask_assign_english_dutch(self):
        code = "mens is ask Hallo welkom bij Hedy!"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "mens is vraag Hallo welkom bij Hedy!"

        self.assertEqual(result, expected)

    def test_forward_assigned_value_english_dutch(self):
        code = "value is 50\nforward value"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "value is 50\nvooruit value"

        self.assertEqual(result, expected)

    def test_print_var_text(self):
        code = "welkom is Hallo welkom bij Hedy\nprint welkom Veel plezier"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "welkom is Hallo welkom bij Hedy\nprint welkom Veel plezier"

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

    def test_ask_assign_dutch_english(self):
        code = "mens is vraag Hallo welkom bij Hedy!"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "mens is ask Hallo welkom bij Hedy!"

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

    def test_echo(self):
        code = "echo Hedy"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "echo Hedy"

        self.assertEqual(result, expected)

    def no_argument_ask_english(self):
        code = "ask"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "vraag"

        self.assertEqual(result, expected)

    def no_argument_ask_dutch(self):
        code = "vraag"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "ask"

        self.assertEqual(result, expected)