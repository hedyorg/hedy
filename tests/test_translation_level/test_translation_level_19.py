import textwrap
import hedy_translation
from tests.Tester import HedyTester

# tests should be ordered as follows:
# * Translation from English to Telugu
# * Translatoin from Telugu to English
# * Error handling


class TestsTranslationLevel18(HedyTester):
    level = 19

    def test_range_with_brackets(self):
        code = textwrap.dedent("""\
        for i in range(0, 10):
            print('hallo!')""")

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="te", level=self.level)
        expected = textwrap.dedent("""\
        కోసం i in పరిధి(0, 10):
            print('hallo!')""")

        self.assertEqual(expected, result)

    def test_input_empty_brackets(self):
        code = textwrap.dedent("""\
        nombre es entrada()
        ముద్రణ(nombre)""")

        result = hedy_translation.translate_keywords(code, from_lang="te", to_lang="en", level=self.level)

        expected = textwrap.dedent("""\
        nombre is input()
        print(nombre)""")

        self.assertEqual(expected, result)

    def test_print_empty_brackets(self):
        code = textwrap.dedent("ముద్రణ()")

        result = hedy_translation.translate_keywords(code, from_lang="te", to_lang="en", level=self.level)

        expected = textwrap.dedent("print()")

        self.assertEqual(expected, result)
