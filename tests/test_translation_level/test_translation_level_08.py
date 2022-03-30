import hedy
from tests.Tester import HedyTester
from parameterized import parameterized
import hedy_translation
import textwrap

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel8(HedyTester):
    level = 8
    keywords_from = hedy_translation.keywords_to_dict('en')
    keywords_to = hedy_translation.keywords_to_dict('nl')

    def test_repeat_indent_english_dutch(self):
        code = textwrap.dedent("""\
        repeat 3 times
            print 'Hedy is fun!'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        herhaal 3 keer
            print 'Hedy is fun!'""")

        self.assertEqual(expected, result)

    def test_repeat_multiple_indent_english_dutch(self):
        code = textwrap.dedent("""\
        repeat 3 times
            print 'Hedy is fun!'
            print 'print 3 keer'
        print 'print 1 keer'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        herhaal 3 keer
            print 'Hedy is fun!'
            print 'print 3 keer'
        print 'print 1 keer'""")

        self.assertEqual(expected, result)

    def test_repeat_indent_dutch_english(self):
        code = textwrap.dedent("""\
        herhaal 3 keer
            print 'Hedy is fun!'""")

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = textwrap.dedent("""\
        repeat 3 times
            print 'Hedy is fun!'""")

        self.assertEqual(expected, result)

    def test_ifelse_indent_dutch_english(self):
        code = textwrap.dedent("""\
        if naam is hedy
            print 'Hallo Hedy'
            print 'hoe gaat het?'
        else
            print 'Hallo' hedy""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        als naam is hedy
            print 'Hallo Hedy'
            print 'hoe gaat het?'
        anders
            print 'Hallo' hedy""")

        self.assertEqual(expected, result)

    def test_indent_translate_back(self):
        code = textwrap.dedent("""\
        naam = hedy
        if naam is hedy
            print 'Hallo Hedy'
            print 'Hoe gaat het?'
        repeat 5 times
            print '5 keer'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        result = hedy_translation.translate_keywords(result, from_lang="nl", to_lang="en", level=self.level)

        self.assertEqual(code, result)

    @parameterized.expand([('en', 'is'), ('es', 'es'), ('es', 'is'), ('en', '='), ('es', '=')])
    def test_equality_type_error_translates_command(self, lang, is_):
        code = textwrap.dedent(f"""\
            letters is a, b, c
            if letters {is_} '10'
                print 'wrong!'""")

        self.multi_level_tester(
            lang=lang,
            code=code,
            max_level=11,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=self.exception_command(is_)
        )
