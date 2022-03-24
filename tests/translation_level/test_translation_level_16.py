import hedy
from Tester import HedyTester
import hedy_translation
import textwrap


# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel16(HedyTester):
    level = 16

    def test_assign_list_english_dutch(self):
        code = "fruit = ['appel', 'banaan', 'kers']"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "fruit = ['appel', 'banaan', 'kers']"

        self.assertEqual(expected, result)

    def test_access_list_english_dutch(self):
        code = textwrap.dedent("""\
        fruit = ['appel', 'banaan', 'kers']
        print fruit[2]""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        fruit = ['appel', 'banaan', 'kers']
        print fruit[2]""")

        self.assertEqual(expected, result)

    def test_access_list_random_dutch_english(self):
        code = textwrap.dedent("""\
        fruit = ['appel', 'banaan', 'kers']
        print fruit[willekeurig]""")

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = textwrap.dedent("""\
        fruit = ['appel', 'banaan', 'kers']
        print fruit[random]""")

        self.assertEqual(expected, result)