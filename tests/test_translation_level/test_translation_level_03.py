import textwrap

import hedy
from parameterized import parameterized
from Tester import HedyTester
import hedy_translation


    # tests should be ordered as follows:
    # * Translation from English to Dutch
    # * Translation from Dutch to English
    # * Translation to several languages
    # * Error handling

class TestsTranslationLevel3(HedyTester):
    level = 3

    def test_assign_list(self):
        code = "animals is dog, cat, kangaroo"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "animals is dog, cat, kangaroo"

        self.assertEqual(expected, result)

    def test_at_random(self):
        code = "print animals at random"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "print animals op willekeurig"

        self.assertEqual(expected, result)

    def test_assign_list_nl_en(self):
        code = "actie is drukaf, echo, vraag"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "actie is drukaf, echo, vraag"

        self.assertEqual(expected, result)

    def test_at_random_nl_en(self):
        code = "print echo op willekeurig"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "print echo at random"

        self.assertEqual(expected, result)

    def test_issue_1856(self):
        code = textwrap.dedent("""\
        print Hoi Ik ben Hedy de Waarzegger
        vraag is ask Wat wil je weten?
        print vraag
        antwoorden is ja, nee, misschien
        print Mijn glazen bol zegt...
        sleep 2
        print antwoorden at random""")

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = textwrap.dedent("""\
        print Hoi Ik ben Hedy de Waarzegger
        vraag is vraag Wat wil je weten?
        print vraag
        antwoorden is ja, nee, misschien
        print Mijn glazen bol zegt...
        slaap 2
        print antwoorden op willekeurig""")

        self.assertEqual(expected, result)

    def test_issue_1856_reverse(self):
        code = textwrap.dedent("""\
        print Hoi Ik ben Hedy de Waarzegger
        vraag is vraag Wat wil je weten?
        print vraag
        antwoorden is ja, nee, misschien
        print Mijn glazen bol zegt...
        slaap 2
        print antwoorden op willekeurig""")

        expected = textwrap.dedent("""\
        print Hoi Ik ben Hedy de Waarzegger
        vraag is ask Wat wil je weten?
        print vraag
        antwoorden is ja, nee, misschien
        print Mijn glazen bol zegt...
        sleep 2
        print antwoorden at random""")

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)


        self.assertEqual(expected, result)

    def test_issue_1856_v3(self):
        code = textwrap.dedent("""\
        print Hoi Ik ben Hedy de Waarzegger
        vraag is ask Wat wil je weten?
        print vraag
        antwoorden is ja, nee, misschien
        print Mijn glazen bol zegt...
        slaap 2
        print antwoorden op willekeurig""")

        expected = textwrap.dedent("""\
        print Hoi Ik ben Hedy de Waarzegger
        vraag is ask Wat wil je weten?
        print vraag
        antwoorden is ja, nee, misschien
        print Mijn glazen bol zegt...
        sleep 2
        print antwoorden at random""")

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)

        self.assertEqual(expected, result)

    def test_add_remove_en_nl(self):
        code = textwrap.dedent("""\
        dieren is koe, kiep
        add muis to dieren
        remove koe from dieren
        print dieren at random""")

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = textwrap.dedent("""\
        dieren is koe, kiep
        voeg muis toe aan dieren
        verwijder koe uit dieren
        print dieren op willekeurig""")

        self.assertEqual(expected, result)

    @parameterized.expand([
        ('en', 'print'),
        ('es', 'imprimir'),
        ('es', 'print')])
    def test_print_type_error_translates_command(self, lang, command):
        code = textwrap.dedent(f"""\
            letters is a, b, b
            {command} letters""")

        self.multi_level_tester(
            lang=lang,
            code=code,
            max_level=11,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=self.exception_command(command)
        )

    @parameterized.expand([
        ('en', 'at'),
        ('es', 'en'),
        ('es', 'at')])
    def test_list_at_index_type_error_translates_command(self, lang, at):
        code = textwrap.dedent(f"""\
            letters is ask 'What are the letters?'
            print letters {at} 1""")

        self.multi_level_tester(
            lang=lang,
            code=code,
            max_level=11,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=self.exception_command(at)
        )

    @parameterized.expand([
        ('en', 'at random'),
        ('es', 'en aleatorio'),
        ('es', 'at aleatorio'),
        ('es', 'en random')])
    def test_list_at_random_type_error_translates_command(self, lang, at_random):
        code = textwrap.dedent(f"""\
            letters is ask 'What are the letters?'
            print letters {at_random}""")

        self.multi_level_tester(
            lang=lang,
            code=code,
            max_level=11,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=self.exception_command(at_random)
        )

    @parameterized.expand([
        ('en', 'add', 'to'),
        ('es', 'añadir', 'a'),
        ('es', 'añadir', 'to'),
        ('es', 'add', 'a')])
    def test_add_to_list_type_error_translates_command(self, lang, add, to):
        code = textwrap.dedent(f"""\
            color is yellow
            {add} blue {to} color""")

        self.multi_level_tester(
            lang=lang,
            code=code,
            max_level=11,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=self.exception_command(f'{add} {to}')
        )

    @parameterized.expand([
        ('en', 'add', 'to'),
        ('es', 'borrar', 'de'),
        ('es', 'borrar', 'from'),
        ('es', 'remove', 'de')])
    def test_remove_from_list_type_error_translates_command(self, lang, remove, from_):
        code = textwrap.dedent(f"""\
            color is yellow
            {remove} blue {from_} color""")

        self.multi_level_tester(
            lang=lang,
            code=code,
            max_level=11,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=self.exception_command(f'{remove} {from_}')
        )
