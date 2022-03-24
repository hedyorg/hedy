from parameterized import parameterized
import hedy
from Tester import HedyTester
import hedy_translation
import textwrap


# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel14(HedyTester):
    level = 14    
    all_keywords_dict = hedy_translation.all_keywords_to_dict()

    def test_bigger(self):
        code = textwrap.dedent("""\
        hedy = 5
        if hedy > 6
            print 'hedy'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 5
        als hedy > 6
            print 'hedy'""")

        self.assertEqual(expected, result)

    def test_smaller(self):
        code = textwrap.dedent("""\
        hedy = 5
        if hedy < 6
            print 'hedy'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 5
        als hedy < 6
            print 'hedy'""")

        self.assertEqual(expected, result)

    def test_bigger_equal(self):
        code = textwrap.dedent("""\
        hedy = 5
        if hedy >= 6
            print 'hedy'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 5
        als hedy >= 6
            print 'hedy'""")

        self.assertEqual(expected, result)

    def test_smaller_equal(self):
        code = textwrap.dedent("""\
        hedy = 5
        if hedy <= 6
            print 'hedy'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 5
        als hedy <= 6
            print 'hedy'""")

        self.assertEqual(expected, result)

    def test_not_equal(self):
        code = textwrap.dedent("""\
        hedy = 5
        if hedy != 6
            print 'hedy'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 5
        als hedy != 6
            print 'hedy'""")

        self.assertEqual(expected, result)
    
    def test_double_equals(self):
        code = textwrap.dedent("""\
        hedy = 5
        if hedy == 6
            print 'hedy'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 5
        als hedy == 6
            print 'hedy'""")

        self.assertEqual(expected, result)

    @parameterized.expand(HedyTester.as_list_of_tuples(all_keywords_dict["if"], all_keywords_dict["print"], hedy_translation.KEYWORD_LANGUAGES))   
    def test_double_equals_all_lang(self, if_keyword, print_keyword, lang):
        code = textwrap.dedent(f"""\
        hedy = 5
        {if_keyword} hedy == 6
            {print_keyword} 'hedy'""")

        result = hedy_translation.translate_keywords(code, from_lang=lang, to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 5
        als hedy == 6
            print 'hedy'""")

        self.assertEqual(expected, result)   