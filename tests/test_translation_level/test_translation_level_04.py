import textwrap

import hedy
from parameterized import parameterized
from tests.Tester import HedyTester
import hedy_translation

    # tests should be ordered as follows:
    # * Translation from English to Dutch
    # * Translation from Dutch to English
    # * Translation to several languages
    # * Error handling

class TestsTranslationLevel4(HedyTester):
    level = 4

    def test_print(self):
        code = "print 'Hello welcome to Hedy.'"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "print 'Hello welcome to Hedy.'"

        self.assertEqual(expected, result)

    def test_assign(self):
        code = "name is Hedy"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "name is Hedy"

        self.assertEqual(expected, result)

    def test_print_assign(self):
        code = "print 'my name is ' name"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "print 'my name is ' name"

        self.assertEqual(expected, result)

    def test_ask(self):
        code = "color is ask 'What is your favorite color?'"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "color is vraag 'What is your favorite color?'"

        self.assertEqual(expected, result)

    def test_ask_vraag_var_name(self):
        code = "vraag is ask 'What is your favorite color?'"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "vraag is vraag 'What is your favorite color?'"

        self.assertEqual(expected, result)

    def test_ask_vraag_var_name_reverse(self):
        code = "ask is ask 'What is your favorite color?'"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "ask is vraag 'What is your favorite color?'"

        self.assertEqual(expected, result)


    def test_print_nl_en(self):
        code = "print 'Hello welcome to Hedy.'"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "print 'Hello welcome to Hedy.'"

        self.assertEqual(expected, result)

    def test_assign_nl_en(self):
        code = "name is Hedy"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "name is Hedy"

        self.assertEqual(expected, result)

    def test_print_assign_nl_en(self):
        code = "print 'my name is ' name"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "print 'my name is ' name"

        self.assertEqual(expected, result)

    @parameterized.expand([('en', 'ask'), ('es', 'preguntar'), ('es', 'ask')])
    def test_ask_type_error_translates_command(self, lang, ask):
        code = textwrap.dedent(f"""\
            colors is orange, blue, green
            favorite is {ask} 'Is your fav color' colors""")

        self.multi_level_tester(
            lang=lang,
            code=code,
            max_level=11,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=self.exception_command(ask)
        )
