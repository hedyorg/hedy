import hedy
from test_level_01 import HedyTester
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

        self.assertEqual(result, expected)

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

        self.assertEqual(result, expected)

    def test_repeat_indent_dutch_english(self):
        code = textwrap.dedent("""\
        herhaal 3 keer
            print 'Hedy is fun!'""")

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = textwrap.dedent("""\
        repeat 3 times
            print 'Hedy is fun!'""")

        self.assertEqual(result, expected)

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

        self.assertEqual(result, expected)

    def test_indent_translate_back(self):
        code = textwrap.dedent("""\
        naam is hedy
        if naam is hedy
            print 'Hallo Hedy'
            print 'Hoe gaat het?'
        repeat 5 times
            print '5 keer'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        result = hedy_translation.translate_keywords(result, from_lang="nl", to_lang="en", level=self.level)

        self.assertEqual(code, result)