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

class TestsTranslationLevel4(HedyTester):
    level = 4

    @check_local_lang_bool
    def test_print(self):
        code = "print 'Hello welcome to Hedy.'"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "print 'Hello welcome to Hedy.'"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_assign(self):
        code = "name is Hedy"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "name is Hedy"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_print_assign(self):
        code = "print 'my name is ' name"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "print 'my name is ' name"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_ask(self):
        code = "color is ask 'What is your favorite color?'"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "color is vraag 'What is your favorite color?'"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_print_nl_en(self):
        code = "print 'Hello welcome to Hedy.'"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "print 'Hello welcome to Hedy.'"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_assign_nl_en(self):
        code = "name is Hedy"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "name is Hedy"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_print_assign_nl_en(self):
        code = "print 'my name is ' name"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "print 'my name is ' name"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_ask_nl_en(self):
        code = "color is vraag 'What is your favorite color?'"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "color is ask 'What is your favorite color?'"

        self.assertEqual(result, expected)