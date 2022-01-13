import hedy
from test_level_01 import HedyTester
import hedy_translation
import textwrap
from parameterized import parameterized

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel11(HedyTester):
    level = 11
    keywords_from = hedy_translation.keywords_to_dict('en')
    keywords_to = hedy_translation.keywords_to_dict('nl')
    all_kwords = hedy_translation.all_keywords_to_dict()
    
    def test_for_in_english_dutch(self):
        code = textwrap.dedent("""\
        for counter in range 1 to 5
            print counter""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        voor counter in bereik 1 tot 5
            print counter""")

        self.assertEqual(expected, result)

    @parameterized.expand(HedyTester.as_list_of_tuples(all_kwords["ask"], all_kwords["for"], all_kwords["in"], all_kwords["range"], all_kwords["to"], all_kwords["print"],hedy_translation.KEYWORD_LANGUAGES))
    def test_for_in_all_lang(self, ask_kword, for_kword, in_kword, range_kword, to_kword, print_kword, lang):
        code = textwrap.dedent(f"""\
        nummer = {ask_kword} 'hoe oud ben je'
        {for_kword} counter {in_kword} {range_kword} 1 {to_kword} 5
            {for_kword} count {in_kword} {range_kword} nummer {to_kword} 0
                {print_kword} 'hoi' counter""")

        result = hedy_translation.translate_keywords(code, from_lang=lang, to_lang="en", level=self.level)
        expected = textwrap.dedent("""\
        nummer = ask 'hoe oud ben je'
        for counter in range 1 to 5
            for count in range nummer to 0
                print 'hoi' counter""")

        self.assertEqual(expected, result)
