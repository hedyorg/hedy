import hedy
import hedy_translation
import textwrap
from parameterized import parameterized
from test_level_01 import HedyTester


# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel7(HedyTester):
    level = 7
    keywords_from = hedy_translation.keywords_to_dict('en')
    keywords_to = hedy_translation.keywords_to_dict('nl')

    def test_repeat_english_dutch(self):
        code = "repeat 3 times print 'Hedy is fun!'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "herhaal 3 keer print 'Hedy is fun!'"

        self.assertEqual(expected, result)

    def test_repeat2_english_dutch(self):
        code = "repeat 2 times print name"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "herhaal 2 keer print name"

        self.assertEqual(expected, result)

    def test_repeat_dutch_english(self):
        code = "herhaal 3 keer print 'Hedy is fun!'"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "repeat 3 times print 'Hedy is fun!'"

        self.assertEqual(expected, result)

    def test_repeat2_dutch_english(self):
        code = "herhaal 2 keer print ask"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "repeat 2 times print ask"

        self.assertEqual(expected, result)

    def test_translate_back(self):
        code = "repeat 4 times print 'Welcome to Hedy'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        result = hedy_translation.translate_keywords(result, from_lang="nl", to_lang="en", level=self.level)

        self.assertEqual(code, result)

    @parameterized.expand([('en', 'repeat', 'times'),
                           ('es', 'repetir', 'veces'),
                           ('es', 'repetir', 'times'),
                           ('es', 'repeat', 'veces')])
    def test_repeat_type_error_translates_command(self, lang, repeat, times):
        code = textwrap.dedent(f"""\
            a is 1, 2, 3
            {repeat} a {times} print 'n'""")

        self.single_level_tester(
            lang=lang,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=self.exception_command(f'{repeat} {times}')
        )
