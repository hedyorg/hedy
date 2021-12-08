import hedy
from test_level_01 import HedyTester
import hedy_translation
import textwrap


# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel11(HedyTester):
    level = 11
    keywords_from = hedy_translation.keywords_to_dict('en')
    keywords_to = hedy_translation.keywords_to_dict('nl')

    def test_for_in_english_dutch(self):
        code = textwrap.dedent("""\
        for counter in range 1 to 5
            print counter""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        voor counter in bereik 1 tot 5
            print counter""")

        self.assertEqual(result, expected)

    def test_for_in_dutch_english(self):
        code = textwrap.dedent("""\
        nummer is vraag 'hoe oud ben je'
        voor counter in bereik 1 tot 5
            voor count in bereik nummer tot 0
                print 'hoi' counter""")

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = textwrap.dedent("""\
        nummer is ask 'hoe oud ben je'
        for counter in range 1 to 5
            for count in range nummer to 0
                print 'hoi' counter""")

        self.assertEqual(result, expected)
