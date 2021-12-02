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


class TestsTranslationLevel5(HedyTester):
    level = 5
    keywords_from = hedy_translation.keywords_to_dict('en')
    keywords_to = hedy_translation.keywords_to_dict('nl')

    @check_local_lang_bool
    def test_print_english_dutch(self):
        code = "print 'Hallo welkom bij Hedy!'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "print 'Hallo welkom bij Hedy!'"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_print2_english_dutch(self):
        code = "print Hallo 'welkom bij Hedy!'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "print Hallo 'welkom bij Hedy!'"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_ask_assign_english_dutch(self):
        code = "answer is ask 'What is 10 plus 10?'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "answer is vraag 'What is 10 plus 10?'"

        self.assertEqual(result, expected)


    @check_local_lang_bool
    def test_if_else_english_dutch(self):
        code = "if answer is far forward 100 else forward 5"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "als answer is far vooruit 100 anders vooruit 5"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_in_list_english_dutch(self):
        code = "if color in pretty_colors print 'pretty!'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "als color in pretty_colors print 'pretty!'"

        self.assertEqual(result, expected)


    @check_local_lang_bool
    def test_print_dutch_english(self):
        code = "print 'Hallo welkom bij Hedy!'"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "print 'Hallo welkom bij Hedy!'"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_print2_dutch_english(self):
        code = "print Hallo 'welkom bij Hedy!'"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "print Hallo 'welkom bij Hedy!'"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_ask_assign_dutch_english(self):
        code = "answer is vraag 'What is 10 plus 10?'"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "answer is ask 'What is 10 plus 10?'"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_if_else_dutch_english(self):
        code = "als answer is far vooruit 100 anders vooruit 5"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "if answer is far forward 100 else forward 5"

        self.assertEqual(result, expected)

    @check_local_lang_bool
    def test_in_list_dutch_english(self):
        code = "als hond in dieren print 'Cute!'"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "if hond in dieren print 'Cute!'"

        self.assertEqual(result, expected)