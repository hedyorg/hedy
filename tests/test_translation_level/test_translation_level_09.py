import hedy
from tests.Tester import HedyTester
import hedy_translation
import textwrap

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel9(HedyTester):
    level = 9
    keywords_from = hedy_translation.keywords_to_dict('en')
    keywords_to = hedy_translation.keywords_to_dict('nl')

    def test_double_repeat_indent_english_dutch(self):
        code = textwrap.dedent("""\
        repeat 3 times
            repeat 5 times
                print 'hi'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        herhaal 3 keer
            herhaal 5 keer
                print 'hi'""")

        self.assertEqual(expected, result)

    def test_repeat_ifelse_english_dutch(self):
        code = textwrap.dedent("""\
        repeat 3 times
            if naam is hedy
                print 'hello'
            else
                repeat 2 times
                    print 'oh'""")


        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        herhaal 3 keer
            als naam is hedy
                print 'hello'
            anders
                herhaal 2 keer
                    print 'oh'""")

        self.assertEqual(expected, result)

    def test_multiple_ifelse_dutch_english(self):
        code = textwrap.dedent("""\
        als 10 is 10
            als 2 is 3
                print 'wat raar'
            anders
                print 'gelukkig'""")


        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = textwrap.dedent("""\
        if 10 is 10
            if 2 is 3
                print 'wat raar'
            else
                print 'gelukkig'""")

        self.assertEqual(expected, result)

    def test_indent_translate_back(self):
        code = textwrap.dedent("""\
        naam = hedy
        if naam is hedy
            repeat 4 times
                print 'Hallo Hedy'
                print 'Hoe gaat het?'
        else
            repeat 5 times
                print '5 keer'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        result = hedy_translation.translate_keywords(result, from_lang="nl", to_lang="en", level=self.level)

        self.assertEqual(code, result)