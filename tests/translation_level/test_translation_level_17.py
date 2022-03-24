import hedy
from Tester import HedyTester
import hedy_translation
import textwrap


# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel17(HedyTester):
    level = 17

    def test_indent_for_loop_english_dutch(self):
        code = textwrap.dedent("""\
        for i in range 1 to 12:
            print 'Hedy' i""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        voor i in bereik 1 tot 12:
            print 'Hedy' i""")

        self.assertEqual(expected, result)

    def test_indent_while_loop_english_dutch(self):
        code = textwrap.dedent("""\
        i = 3
        while i < 2:
            print 'Hedy' i""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        i = 3
        zolang i < 2:
            print 'Hedy' i""")

        self.assertEqual(expected, result)

    def test_indent_for_list_english_dutch(self):
        code = textwrap.dedent("""\
        hedy = ['hedy', 'andre', 'luca']
        for naam in hedy:
            print naam""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = ['hedy', 'andre', 'luca']
        voor naam in hedy:
            print naam""")

        self.assertEqual(expected, result)

    def test_indent_ifs_english_dutch(self):
        code = textwrap.dedent("""\
        hedy = 4
        if hedy is 4:
            print 'hedy'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 4
        als hedy is 4:
            print 'hedy'""")

        self.assertEqual(expected, result)

    def test_indent_elses_english_dutch(self):
        code = textwrap.dedent("""\
        hedy = 4
        if hedy is 4:
            print 'hedy'
        else:
            print 'nee'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 4
        als hedy is 4:
            print 'hedy'
        anders:
            print 'nee'""")

        self.assertEqual(expected, result)

    def test_elif_english_dutch(self):
        code = textwrap.dedent("""\n
        hedy = 4
        if hedy is 4:
            print 'hedy'
        elif hedy is 5:
            print 5
        else:
            print 'nee'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 4
        als hedy is 4:
            print 'hedy'
        alsanders hedy is 5:
            print 5
        anders:
            print 'nee'""")

        self.assertEqual(expected, result)