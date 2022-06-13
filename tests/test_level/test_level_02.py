import hedy
import textwrap
from parameterized import parameterized
from tests.Tester import HedyTester


class TestsLevel2(HedyTester):
    level = 2
    '''
    Tests should be ordered as follows:
     * commands in the order of hedy.py e.g. for level 1: ['print', 'ask', 'echo', 'turn', 'forward']
     * combined tests
     * markup tests
     * negative tests

    Naming conventions are like this:
     * single keyword positive tests are just keyword or keyword_special_case
     * multi keyword positive tests are keyword1_keywords_2
     * negative tests should be situation_gives_exception
    '''

    #
    # print tests
    #
    def test_print(self):
        code = "print Hallo welkom bij Hedy!"
        expected = "print(f'Hallo welkom bij Hedy!')"
        output = 'Hallo welkom bij Hedy!'

        self.multi_level_tester(
            code=code,
            expected=expected,
            output=output,
            max_level=3
        )

    def test_print_no_space(self):
        code = "printHallo welkom bij Hedy!"
        expected = "print(f'Hallo welkom bij Hedy!')"
        output = 'Hallo welkom bij Hedy!'

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=3)

    def test_print_comma(self):
        code = "print welkom bij steen, schaar, papier"
        expected = "print(f'welkom bij steen, schaar, papier')"
        output = "welkom bij steen, schaar, papier"

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=3)

    def test_print_multiple_lines(self):
        code = textwrap.dedent("""\
        print Hallo welkom bij Hedy!
        print Mooi hoor""")

        expected = textwrap.dedent("""\
        print(f'Hallo welkom bij Hedy!')
        print(f'Mooi hoor')""")

        output = textwrap.dedent("""\
        Hallo welkom bij Hedy!
        Mooi hoor""")

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=3)

    def test_print_single_quoted_text(self):
        code = "print 'Welcome to OceanView'"
        expected = "print(f'\\'Welcome to OceanView\\'')"
        output = "'Welcome to OceanView'"

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=3)

    def test_print_double_quoted_text(self):
        code = 'print "Welcome to OceanView"'
        expected = "print(f'\"Welcome to OceanView\"')"
        output = '"Welcome to OceanView"'

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=3)

    def test_print_text_with_inner_single_quote(self):
        code = "print Welcome to Hedy's game!"
        expected = """print(f'Welcome to Hedy\\'s game!')"""

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_print_text_with_inner_double_quote(self):
        code = 'print It says "Hedy"'
        expected = """print(f'It says "Hedy"')"""

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_print_slash(self):
        code = "print Yes/No"
        expected = "print(f'Yes/No')"

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_print_backslash(self):
        code = "print Yes\\No"
        expected = "print(f'Yes\\\\No')"
        output = "Yes\\No"

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=3)

    def test_print_backslash_at_end(self):
        code = "print Welcome to \\"
        expected = "print(f'Welcome to \\\\')"
        output = "Welcome to \\"

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=3)

    def test_print_with_spaces(self):
        code = "print        hallo!"
        expected = "print(f'hallo!')"

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_print_asterisk(self):
        code = "print *Jouw* favoriet is dus kleur"
        expected = "print(f'*Jouw* favoriet is dus kleur')"

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    #
    # ask tests
    #
    def test_ask(self):
        code = "kleur is ask wat is je lievelingskleur?"
        expected = "kleur = input('wat is je lievelingskleur'+'?')"

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_ask_single_quoted_text(self):
        code = "name is ask 'Who's that'"
        expected = """name = input('\\'Who\\'s that\\'')"""

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_ask_double_quoted_text(self):
        code = 'var is ask "Welcome to OceanView"'
        expected = "var = input('\"Welcome to OceanView\"')"

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_ask_text_with_inner_single_quote(self):
        code = "var is ask Welcome to Hedy's game"
        expected = """var = input('Welcome to Hedy\\'s game')"""

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_ask_text_with_inner_double_quote(self):
        code = 'var is ask It says "Hedy"'
        expected = """var = input('It says "Hedy"')"""

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_ask_with_comma(self):
        code = textwrap.dedent("""\
        dieren is ask hond, kat, kangoeroe
        print dieren""")

        expected = textwrap.dedent("""\
        dieren = input('hond, kat, kangoeroe')
        print(f'{dieren}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_ask_es(self):
        code = "color is ask ask Cuál es tu color favorito?"
        expected = "color = input('ask Cuál es tu color favorito'+'?')"

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_ask_bengali_var(self):
        code = textwrap.dedent("""\
        রং is ask আপনার প্রিয় রং কি?
        print রং is আপনার প্রিয""")

        expected = textwrap.dedent("""\
        ve1760b6272d4c9f816e62af4882d874f = input('আপনার প্রিয় রং কি'+'?')
        print(f'{ve1760b6272d4c9f816e62af4882d874f} is আপনার প্রিয')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    #
    # forward tests
    #
    def test_forward_with_integer_variable(self):
        code = textwrap.dedent("""\
            a is 50
            forward a""")
        expected = HedyTester.dedent(
            "a = '50'",
            HedyTester.forward_transpiled('a'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=self.max_turtle_level,
        )

    def test_forward_with_string_variable_gives_type_error(self):
        code = textwrap.dedent("""\
            a is test
            forward a""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            max_level=self.max_turtle_level,
        )

    #
    # turn tests
    #
    def test_turn_number(self):
        code = "turn 180"
        expected = HedyTester.turn_transpiled(180)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=self.max_turtle_level,
        )

    def test_turn_negative_number(self):
        code = "turn -180"
        expected = HedyTester.turn_transpiled(-180)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=self.max_turtle_level,
        )

    def test_turn_with_number_var(self):
        code = textwrap.dedent("""\
            direction is 70
            turn direction""")
        expected = HedyTester.dedent(
            "direction = '70'",
            HedyTester.turn_transpiled('direction'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=self.max_turtle_level,
        )

    def test_turn_with_non_latin_number_var(self):
        code = textwrap.dedent("""\
        الزاوية هي ٩٠
        استدر الزاوية
        تقدم ١٠٠
        """)
        expected = HedyTester.dedent(
            "direction = '٩٠'",
            HedyTester.turn_transpiled('direction'))

        self.multi_level_tester(
            code=code,
            lang='ar',
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=self.max_turtle_level,
        )

    def test_one_turn_with_text_gives_type_error(self):
        code = "turn koekoek"

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            max_level=self.max_turtle_level,
        )

    @parameterized.expand(['left', 'right'])
    def test_one_turn_with_left_or_right_gives_type_error(self, arg):
        code = f"turn {arg}"
        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            max_level=self.max_turtle_level,
        )

    def test_turn_with_string_var_gives_type_error(self):
        code = textwrap.dedent("""\
            direction is ten
            turn direction""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            max_level=self.max_turtle_level,
        )

    def test_turn_with_non_ascii_var(self):
        code = textwrap.dedent("""\
            ángulo is 90
            turn ángulo""")
        expected = HedyTester.dedent(
            "vefd88f42b64136f16e8f305dd375a921 = '90'",
            HedyTester.turn_transpiled('vefd88f42b64136f16e8f305dd375a921'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            expected_commands=['is', 'turn'],
            max_level=self.max_turtle_level,
        )

    # issue #792
    def test_turn_right_number_gives_type_error(self):
        code = "turn right 90"
        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentException,
            max_level=self.max_turtle_level,
        )

    #
    # sleep tests
    #

    def test_sleep(self):
        code = "sleep"
        expected = "time.sleep(1)"

        self.multi_level_tester(code=code, expected=expected)

    def test_sleep_with_default_number(self):
        code = "sleep 1"
        expected = HedyTester.sleep_command_transpiled('"1"')

        self.multi_level_tester(code=code, expected=expected)

    def test_sleep_with_number(self):
        code = "sleep 20"
        expected = HedyTester.sleep_command_transpiled('"20"')

        self.multi_level_tester(code=code, expected=expected)

    def test_sleep_with_number_hi(self):
        code = "sleep २"
        expected = HedyTester.sleep_command_transpiled('"2"')

        self.multi_level_tester(code=code, expected=expected)

    def test_sleep_with_number_ar(self):
        code = "sleep ٣"
        expected = HedyTester.sleep_command_transpiled('"3"')

        self.multi_level_tester(code=code, expected=expected)

    def test_sleep_with_number_variable(self):
        code = textwrap.dedent("""\
            n is 2
            sleep n""")
        expected = HedyTester.dedent(
            "n = '2'",
            HedyTester.sleep_command_transpiled("n"))

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_sleep_with_number_variable_hi(self):
        code = textwrap.dedent("""\
            n is २
            sleep n""")
        expected = HedyTester.dedent(
            "n = '२'",
            HedyTester.sleep_command_transpiled("n"))

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_sleep_with_input_variable(self):
        code = textwrap.dedent("""\
            n is ask how long
            sleep n""")
        expected = HedyTester.dedent(
            "n = input('how long')",
            HedyTester.sleep_command_transpiled("n"))

        self.multi_level_tester(max_level=3, code=code, expected=expected)

    def test_sleep_with_string_variable_gives_error(self):
        code = textwrap.dedent("""\
            n is test
            sleep n""")

        self.multi_level_tester(max_level=11, code=code, exception=hedy.exceptions.InvalidArgumentTypeException)

    #
    # is tests
    #
    def test_assign(self):
        code = "naam is Felienne"
        expected = "naam = 'Felienne'"

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_integer(self):
        code = "naam is 14"
        expected = "naam = '14'"

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_single_quoted_text(self):
        code = "naam is 'Felienne'"
        expected = "naam = '\\'Felienne\\''"

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_double_quoted_string(self):
        code = 'naam is "Felienne"'
        expected = """naam = '"Felienne"'"""

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_text_with_inner_single_quote(self):
        code = "var is Hedy's"
        expected = "var = 'Hedy\\'s'"

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_text_with_inner_double_quote(self):
        code = 'var is It says "Hedy"'
        expected = """var = 'It says "Hedy"'"""

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_text_to_hungarian_var(self):
        code = textwrap.dedent("""\
        állatok is kutya
        print állatok""")

        expected = textwrap.dedent("""\
        v79de0191e90551f058d466c5e8c267ff = 'kutya'
        print(f'{v79de0191e90551f058d466c5e8c267ff}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_bengali_var(self):
        hashed_var = hedy.hash_var("নাম")
        code = "নাম is হেডি"
        expected = f"{hashed_var} = 'হেডি'"

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_python_keyword(self):
        code = "for is Hedy"
        expected = "vd55669822f1a8cf72ec1911e462a54eb = 'Hedy'"

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # markup tests
    #
    def test_spaces_in_arguments(self):
        code = "print hallo      wereld"
        expected = textwrap.dedent("""\
        print(f'hallo wereld')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    #
    # combined tests
    #
    def test_ask_print(self):
        code = textwrap.dedent("""\
        kleur is ask wat is je lievelingskleur?
        print kleur!""")
        expected = textwrap.dedent("""\
        kleur = input('wat is je lievelingskleur'+'?')
        print(f'{kleur}!')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_assign_print(self):
        code = textwrap.dedent("""\
        naam is Felienne
        print naam""")
        expected = textwrap.dedent("""\
        naam = 'Felienne'
        print(f'{naam}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_forward_ask(self):
        code = textwrap.dedent("""\
            afstand is ask hoe ver dan?
            forward afstand""")
        expected = HedyTester.dedent(
            "afstand = input('hoe ver dan'+'?')",
            HedyTester.forward_transpiled('afstand'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=3
        )

    def test_ask_turn(self):
        code = textwrap.dedent("""\
        print Turtle race
        direction is ask Where to turn?
        turn direction""")

        expected = HedyTester.dedent("""\
        print(f'Turtle race')
        direction = input('Where to turn'+'?')""",
                                     HedyTester.turn_transpiled('direction'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=3
        )

    def test_assign_print_punctuation(self):
        code = textwrap.dedent("""\
        naam is Hedy
        print Hallo naam!""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        print(f'Hallo {naam}!')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_assign_print_sentence(self):
        code = textwrap.dedent("""\
        naam is Hedy
        print naam is jouw voornaam""")
        expected = textwrap.dedent("""\
        naam = 'Hedy'
        print(f'{naam} is jouw voornaam')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_assign_print_something_else(self):
        code = textwrap.dedent("""\
        naam is Felienne
        print Hallo""")
        expected = textwrap.dedent("""\
        naam = 'Felienne'
        print(f'Hallo')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    #
    # negative tests
    #
    def test_echo_gives_error(self):
        code = textwrap.dedent("""\
        ask what is jouw lievelingskleur?
        echo Jouw lievelingskleur is dus...""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.WrongLevelException,
            extra_check_function=lambda c: c.exception.error_code == 'Wrong Level',
            max_level=3
        )

    def test_ask_without_var_gives_error(self):
        code = "ask is de papier goed?"
        self.multi_level_tester(
            code=code,
            max_level=3,
            exception=hedy.exceptions.WrongLevelException
        )

    def test_ask_without_argument_gives_error(self):
        code = "name is ask"
        self.multi_level_tester(
            max_level=17,
            code=code,
            exception=hedy.exceptions.IncompleteCommandException
        )
