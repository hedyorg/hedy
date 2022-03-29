import hedy
from tests.Tester import HedyTester
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
    all_keywords = hedy_translation.all_keywords_to_dict()
    
    def test_for_in_english_dutch(self):
        code = textwrap.dedent("""\
        for counter in range 1 to 5
            print counter""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        voor counter in bereik 1 tot 5
            print counter""")

        self.assertEqual(expected, result)

    @parameterized.expand(HedyTester.as_list_of_tuples(all_keywords["ask"], all_keywords["for"], all_keywords["in"], all_keywords["range"], all_keywords["to"], all_keywords["print"],hedy_translation.KEYWORD_LANGUAGES))
    def test_for_in_all_lang(self, ask_keyword, for_keyword, in_keyword, range_keyword, to_keyword, print_keyword, lang):
        code = textwrap.dedent(f"""\
        nummer = {ask_keyword} 'hoe oud ben je'
        {for_keyword} counter {in_keyword} {range_keyword} 1 {to_keyword} 5
            {for_keyword} count {in_keyword} {range_keyword} nummer {to_keyword} 0
                {print_keyword} 'hoi' counter""")

        result = hedy_translation.translate_keywords(code, from_lang=lang, to_lang="en", level=self.level)
        expected = textwrap.dedent("""\
        nummer = ask 'hoe oud ben je'
        for counter in range 1 to 5
            for count in range nummer to 0
                print 'hoi' counter""")

        self.assertEqual(expected, result)

    @parameterized.expand([('en', 'in', 'range', 'to'),
                           ('es', 'en', 'rango', 'a'),
                           ('es', 'in', 'rango', 'a'),
                           ('es', 'en', 'rango', 'a')])
    def test_for_loop_type_error_translates_command(self, lang, in_, range_, to):
        code = textwrap.dedent(f"""\
            end is 'text'
            for a {in_} {range_} 1 {to} end
                print end""")

        self.multi_level_tester(
            lang=lang,
            code=code,
            max_level=11,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=self.exception_command(f'{in_} {range_} {to}'))
