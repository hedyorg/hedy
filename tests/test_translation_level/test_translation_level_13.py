import textwrap
from parameterized import parameterized
from hedy_content import ALL_KEYWORD_LANGUAGES
import hedy_translation
from tests.Tester import HedyTester

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel13(HedyTester):
    level = 13
    all_keywords = hedy_translation.all_keywords_to_dict()

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

    def test_for_in_english_dutch(self):
        code = textwrap.dedent("""\
        for counter in range (1, 5)
            print counter""")

        result = hedy_translation.translate_keywords(
            code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        voor counter in bereik (1, 5)
            print counter""")

        self.assertEqual(expected, result)

    @parameterized.expand(
        HedyTester.as_list_of_tuples(
            all_keywords["ask"],
            all_keywords["for"],
            all_keywords["in"],
            all_keywords["range"],
            all_keywords["to"],
            all_keywords["print"],
            list(ALL_KEYWORD_LANGUAGES.keys())))
    def test_for_in_all_lang(
            self,
            ask_keyword,
            for_keyword,
            in_keyword,
            range_keyword,
            to_keyword,
            print_keyword,
            lang):
        code = textwrap.dedent(f"""\
        nummer = {ask_keyword} 'hoe oud ben je'
        {for_keyword} counter {in_keyword} {range_keyword} (1, 5):
            {for_keyword} count {in_keyword} {range_keyword} (nummer, 0)
                {print_keyword} 'hoi' counter""")

        result = hedy_translation.translate_keywords(
            code, from_lang=lang, to_lang="en", level=self.level)
        expected = textwrap.dedent("""\
        nummer = ask 'hoe oud ben je'
        for counter in range (1, 5):
            for count in range (nummer, 0)
                print 'hoi' counter""")

        self.assertEqual(expected, result)

    def test_for_loop_type_error_translates_command(self):
        code = textwrap.dedent(f"""\
            end is 'text'
            for a in range (1, end)
                print end""")

        self.verify_translation(code, "en", self.level)

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
        code = textwrap.dedent("""\
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

    def test_elif_spanish_dutch(self):
        code = textwrap.dedent("""\
        hedy = 5
        si hedy es 4:
            imprimir 'hedy'
        sinosi hedy es 5:
            imprimir 5
        sino:
            imprimir 'nee'""")

        result = hedy_translation.translate_keywords(code, from_lang="es", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 5
        als hedy is 4:
            print 'hedy'
        alsanders hedy is 5:
            print 5
        anders:
            print 'nee'""")

        self.assertEqual(expected, result)

    def test_while_loop_english_dutch(self):
        code = textwrap.dedent("""\
        answer = 0
        while answer != 25
            answer = ask 'What is 5 * 5'
        print 'Good job!'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        answer = 0
        zolang answer != 25
            answer = vraag 'What is 5 * 5'
        print 'Good job!'""")

        self.assertEqual(expected, result)

    def test_while_loop_dutch_english(self):
        code = textwrap.dedent("""\
        answer = 0
        zolang answer != 25
            answer = vraag 'What is 5 * 5'
        print 'Good job!'""")

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = textwrap.dedent("""\
        answer = 0
        while answer != 25
            answer = ask 'What is 5 * 5'
        print 'Good job!'""")

        self.assertEqual(expected, result)

    def test_multiple_while_loop_english_dutch(self):
        code = textwrap.dedent("""\
        answer = 0
        while answer != 25
            while answer > 30
                answer = ask 'What is 5 * 5'
        print 'Good job!'""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        answer = 0
        zolang answer != 25
            zolang answer > 30
                answer = vraag 'What is 5 * 5'
        print 'Good job!'""")

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
        code = textwrap.dedent("""\
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

    def test_elif_spanish_dutch(self):
        code = textwrap.dedent("""\
        hedy = 5
        si hedy es 4:
            imprimir 'hedy'
        sinosi hedy es 5:
            imprimir 5
        sino:
            imprimir 'nee'""")

        result = hedy_translation.translate_keywords(code, from_lang="es", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 5
        als hedy is 4:
            print 'hedy'
        alsanders hedy is 5:
            print 5
        anders:
            print 'nee'""")

        self.assertEqual(expected, result)

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

    def test_input(self):
        code = textwrap.dedent("""\
        leeftijd is input('Hoe oud ben jij?')
        print(leeftijd)""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        leeftijd is invoer('Hoe oud ben jij?')
        print(leeftijd)""")

        self.assertEqual(expected, result)

    def test_range_with_brackets(self):
        code = textwrap.dedent("""\
        for i in range(0, 10):
            print('hallo!')""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        voor i in bereik(0, 10):
            print('hallo!')""")

        self.assertEqual(expected, result)

    def test_input_empty_brackets(self):
        code = textwrap.dedent("""\
        nombre es entrada()
        imprimir(nombre)""")

        result = hedy_translation.translate_keywords(code, from_lang="es", to_lang="en", level=self.level)

        expected = textwrap.dedent("""\
        nombre is input()
        print(nombre)""")

        self.assertEqual(expected, result)

    def test_print_empty_brackets(self):
        code = textwrap.dedent("imprimir()")

        result = hedy_translation.translate_keywords(code, from_lang="es", to_lang="en", level=self.level)

        expected = textwrap.dedent("print()")

        self.assertEqual(expected, result)

    def test_bigger(self):
        code = textwrap.dedent("""\
        hedy = 5
        if hedy > 6
            print 'hedy'""")

        result = hedy_translation.translate_keywords(
            code, from_lang="en", to_lang="nl", level=self.level)
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

        result = hedy_translation.translate_keywords(
            code, from_lang="en", to_lang="nl", level=self.level)
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

        result = hedy_translation.translate_keywords(
            code, from_lang="en", to_lang="nl", level=self.level)
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

        result = hedy_translation.translate_keywords(
            code, from_lang="en", to_lang="nl", level=self.level)
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

        result = hedy_translation.translate_keywords(
            code, from_lang="en", to_lang="nl", level=self.level)
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

        result = hedy_translation.translate_keywords(
            code, from_lang="en", to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 5
        als hedy == 6
            print 'hedy'""")

        self.assertEqual(expected, result)

    @parameterized.expand(
        HedyTester.as_list_of_tuples(
            all_keywords["if"],
            all_keywords["print"],
            list(ALL_KEYWORD_LANGUAGES.keys())))
    def test_double_equals_all_lang(self, if_keyword, print_keyword, lang):
        code = textwrap.dedent(f"""\
        hedy = 5
        {if_keyword} hedy == 6
            {print_keyword} 'hedy'""")

        result = hedy_translation.translate_keywords(
            code, from_lang=lang, to_lang="nl", level=self.level)
        expected = textwrap.dedent("""\
        hedy = 5
        als hedy == 6
            print 'hedy'""")

        self.assertEqual(expected, result)
