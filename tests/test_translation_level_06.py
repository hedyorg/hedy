import hedy
from test_level_01 import HedyTester
from parameterized import parameterized
import hedy_translation
import textwrap

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel6(HedyTester):
    level = 6
    keywords_from = hedy_translation.keywords_to_dict('en')
    keywords_to = hedy_translation.keywords_to_dict('nl')

    def test_multiplication(self):
        code = "vermenigvuldiging is 3 * 8"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "vermenigvuldiging is 3 * 8"

        self.assertEqual(expected, result)

    def test_addition(self):
        code = "print 'Hallo welkom bij Hedy' 5 + 7"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "print 'Hallo welkom bij Hedy' 5 + 7"

        self.assertEqual(expected, result)

    def test_division_dutch_english(self):
        code = "angle is 360 / angles"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "angle is 360 / angles"

        self.assertEqual(expected, result)

    def test_division_with_equals_dutch_english(self):
        code = "angle = 360 / angles"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "angle = 360 / angles"
        self.assertEqual(expected, result)
    
    def test_translate_back_is(self):
        code ="breuk is 13 / 4"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        result = hedy_translation.translate_keywords(result, from_lang="nl", to_lang="en", level=self.level)

        self.assertEqual(code, result)

    def test_translate_back_equals(self):
        code = "breuk = 13 / 4"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        result = hedy_translation.translate_keywords(result, from_lang="nl", to_lang="en", level=self.level)

        self.assertEqual(code, result)

    def test_ask_with_equals_spanish_english(self):
        code = "nombre = preguntar '¿Cual es tu nombre?'"

        result = hedy_translation.translate_keywords(code, from_lang="es", to_lang="en", level=self.level)

        expected = "nombre = ask '¿Cual es tu nombre?'"

        self.assertEqual(expected, result)

    def test_ask_with_is_spanish_english(self):
        code = "nombre es preguntar '¿Cual es tu nombre?'"

        result = hedy_translation.translate_keywords(code, from_lang="es", to_lang="en", level=self.level)

        expected = "nombre is ask '¿Cual es tu nombre?'"

        self.assertEqual(expected, result)
    
    def test_assign_list_is_spanish_english(self):
        code = "lenguajes es Hedy, Python, C"

        result = hedy_translation.translate_keywords(code, from_lang="es", to_lang="en", level=self.level)

        expected = "lenguajes is Hedy, Python, C"

        self.assertEqual(result, expected)

    def test_assign_list_var_spanish_english(self):
        code = textwrap.dedent("""\
        lenguajes es Hedy, Python, C
        a = lenguajes en 0""")

        result = hedy_translation.translate_keywords(code, from_lang="es", to_lang="en", level=self.level)

        expected = textwrap.dedent("""\
        lenguajes is Hedy, Python, C
        a = lenguajes at 0""")

        self.assertEqual(result, expected)

    @parameterized.expand([('en', '='), ('es', '=')])
    def test_equality_type_error_translates_command(self, lang, is_):
        code = textwrap.dedent(f"""\
            letters is a, b, c
            if letters {is_} '10' print 'wrong!'""")

        self.multi_level_tester(
            lang=lang,
            code=code,
            max_level=7,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=self.exception_command(is_)
        )

    @parameterized.expand([('en', '+'), ('es', '+'), ('en', '-'), ('es', '-'), ('en', '*'), ('es', '*'), ('en', '/'), ('es', '/')])
    def test_expression_type_error_uses_arith_operator(self, lang, operator):
        code = textwrap.dedent(f"""\
            a is test
            print a {operator} 2""")

        self.multi_level_tester(
            lang=lang,
            code=code,
            max_level=7,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=self.exception_command(operator)
        )
