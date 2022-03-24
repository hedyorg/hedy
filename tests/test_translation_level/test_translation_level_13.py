import hedy
from Tester import HedyTester
import hedy_translation
import textwrap


# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel13(HedyTester):
    level = 13

    def test_and_condition_english_dutch(self):
        code = textwrap.dedent("""\
        naam = 'hedy'
        leeftijd = 2
        if naam is 'hedy' and leeftijd is 2
            print 'hallo'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        naam = 'hedy'
        leeftijd = 2
        als naam is 'hedy' en leeftijd is 2
            print 'hallo'""")

        self.assertEqual(expected, result)

    def test_or_condition_english_dutch(self):
        code = textwrap.dedent("""\
        naam = 'hedy'
        leeftijd = 2
        if naam is 'niet hedy' or leeftijd is 2
            print 'hallo'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        naam = 'hedy'
        leeftijd = 2
        als naam is 'niet hedy' of leeftijd is 2
            print 'hallo'""")

        self.assertEqual(expected, result)

    def test_and_condition_acces_list_english_dutch(self):
        code = textwrap.dedent("""\
        naam is 'hedy', 'niet hedy'
        if 'hedy' in naam and 'niet hedy' in naam
            print 'hallo'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        naam is 'hedy', 'niet hedy'
        als 'hedy' in naam en 'niet hedy' in naam
            print 'hallo'""")

        self.assertEqual(expected, result)

    def test_or_condition_acces_list_english_dutch(self):
        code = textwrap.dedent("""\
        naam is 'hedy', 'niet hedy'
        if 'hedy' in naam or 'niet hedy' in naam
            print 'hallo'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        naam is 'hedy', 'niet hedy'
        als 'hedy' in naam of 'niet hedy' in naam
            print 'hallo'""")

        self.assertEqual(expected, result)