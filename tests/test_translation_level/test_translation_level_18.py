from cmath import exp
import hedy
from tests.Tester import HedyTester
import hedy_translation
import textwrap

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling

class TestsTranslationLevel18(HedyTester):
    level = 18

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

