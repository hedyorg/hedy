import textwrap
from parameterized import parameterized
from test_level_01 import HedyTester
import hedy_translation


    # tests should be ordered as follows:
    # * Translation from English to Dutch
    # * Translation from Dutch to English
    # * Translation to several languages
    # * Error handling


class TestsTranslationLevel2(HedyTester):
    level = 2
    all_keywords = hedy_translation.all_keywords_to_dict()

    def test_print(self):
        code = "print Hallo welkom bij Hedy!"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "print Hallo welkom bij Hedy!"

        self.assertEqual(expected, result)

    def test_print_kewords(self):
        code = "print print ask echo"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "print print ask echo"

        self.assertEqual(expected, result)

    def test_ask_assign_english_dutch(self):
        code = "mens is ask Hallo welkom bij Hedy!"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "mens is vraag Hallo welkom bij Hedy!"

        self.assertEqual(expected, result)

    def test_forward_assigned_value_english_dutch(self):
        code = "value is 50\nforward value"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "value is 50\nvooruit value"

        self.assertEqual(expected, result)

    def test_sleep(self):
        code = "sleep"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "slaap"

        self.assertEqual(expected, result)


    def test_print_var_text(self):
        code = "welkom is Hallo welkom bij Hedy\nprint welkom Veel plezier"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "welkom is Hallo welkom bij Hedy\nprint welkom Veel plezier"

        self.assertEqual(expected, result)

    def test_ask_kewords(self):
        code = "hedy is vraag print ask echo"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "hedy is vraag print ask echo"

        self.assertEqual(expected, result)

    def test_ask_print(self):
        code = "hedy is hello\nprint hedy"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "hedy is hello\nprint hedy"

        self.assertEqual(expected, result)

    def test_ask_assign_dutch_english(self):
        code = "mens is vraag Hallo welkom bij Hedy!"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "mens is ask Hallo welkom bij Hedy!"

        self.assertEqual(expected, result)


    def test_translate_back(self):
        code = "print welkom bij Hedy\nnaam is ask what is your name\nprint naam"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)

        expected = "print welkom bij Hedy\nnaam is ask what is your name\nprint naam"

        self.assertEqual(expected, result)

    def test_invalid(self):
        code = "hallo"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "hallo"

        self.assertEqual(expected, result)

    def test_invalid_space(self):
        code = " print Hedy"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = " print Hedy"

        self.assertEqual(expected, result)

    def test_echo(self):
        code = "echo Hedy"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "echo Hedy"

        self.assertEqual(expected, result)

    @parameterized.expand(HedyTester.as_list_of_tuples(all_keywords["ask"], all_keywords["is"] ,all_keywords["print"], hedy_translation.KEYWORD_LANGUAGES))
    def test_ask_print_all_lang(self,ask_keyword, is_keyword, print_keyword, lang):
        code = textwrap.dedent(f"""\
        {print_keyword} Hello, tell us your name please
        name {is_keyword} {ask_keyword} Whats your name?
        {print_keyword} name is your name!""")
    
        result = hedy_translation.translate_keywords(code, from_lang=lang, to_lang="en", level=self.level)
        
        expected = textwrap.dedent(f"""\
        print Hello, tell us your name please
        name is ask Whats your name?
        print name is your name!""")

        self.assertEqual(expected, result)
    
    def no_argument_ask_english(self):
        code = "ask"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "vraag"

        self.assertEqual(expected, result)

    def no_argument_ask_dutch(self):
        code = "vraag"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "ask"

        self.assertEqual(expected, result)