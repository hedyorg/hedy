import hedy
from test_level_01 import HedyTester
import hedy_translation
import textwrap

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel10(HedyTester):
    level = 10

    def test_for_english_dutch(self):
        code = textwrap.dedent("""\
        dieren is hond, kat, vis
        for dier in dieren
            print 'hallo' dier""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        dieren is hond, kat, vis
        voor dier in dieren
            print 'hallo' dier""")

        self.assertEqual(result, expected)

    def test_for_dutch_english(self):
        code = textwrap.dedent("""\
        dieren is hond, kat, vis
        voor dier in dieren
            voor animal in dieren
                print 'hallo' dier""")

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = textwrap.dedent("""\
        dieren is hond, kat, vis
        for dier in dieren
            for animal in dieren
                print 'hallo' dier""")

        self.assertEqual(result, expected)

    def test_repeat_translate_back(self):
        code = textwrap.dedent("""\
        dieren is hond, kat, vis
        voor dier in dieren
            voor animal in dieren
                print 'hallo' dier""")

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        result = hedy_translation.translate_keywords(result, from_lang="en", to_lang="nl", level=self.level)

        self.assertEqual(result, code)