import textwrap
import hedy.translation as hedy_translation
from tests.Tester import HedyTester

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel7(HedyTester):
    level = 7
    keywords_from = hedy_translation.keywords_to_dict('en')
    keywords_to = hedy_translation.keywords_to_dict('nl')

    def test_translate_back(self):
        code = "repeat 4 times print 'Welcome to Hedy'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        result = hedy_translation.translate_keywords(result, from_lang="nl", to_lang="en", level=self.level)

        self.assertEqual(code, result)

    def test_ask_with_equals_spanish_english(self):
        code = "nombre = preguntar '¿Cual es tu nombre?'"

        result = hedy_translation.translate_keywords(code, from_lang="es", to_lang="en", level=self.level)

        expected = "nombre = ask '¿Cual es tu nombre?'"

        self.assertEqual(expected, result)

    def test_expression_type_error_uses_arith_operator(self):
        code = textwrap.dedent(f"""\
            a is test
            print a + 2""")

        self.verify_translation(code, "en", self.level)
