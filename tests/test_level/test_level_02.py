import textwrap
import hedy
from hedy import Keyword
from hedy_sourcemap import SourceRange
from parameterized import parameterized
from tests.Tester import HedyTester, SkippedMapping


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

    def test_print_line_with_spaces_works(self):
        code = "print hallo\n      \nprint hallo"
        expected = "print(f'hallo')\n\nprint(f'hallo')"
        expected_commands = [Keyword.print, Keyword.print]

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=expected_commands,
            max_level=3)

    def test_print_exclamation_mark_and_quote(self):
        # test for issue 279
        code = "print hello world!'"
        expected = "print(f'hello world!\\'')"
        output = "hello world!\'"

        self.multi_level_tester(code=code,
                                expected=expected,
                                output=output,
                                max_level=3)

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

    def test_print_number(self):
        code = "print 10"
        expected = "print(f'10')"

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='10',
            expected_commands=[Keyword.print],
            max_level=3)

    def test_print_number_arabic(self):
        code = "print ١١"
        expected = "print(f'١١')"

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='١١',
            expected_commands=[Keyword.print],
            max_level=3)

    def test_print_var_number(self):
        code = textwrap.dedent("""\
            n is 10
            print n""")
        expected = textwrap.dedent("""\
            n = '10'
            print(f'{n}')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='10',
            max_level=5)

    def test_print_var_number_arabic(self):
        code = textwrap.dedent("""\
            n is ١١
            print n""")
        expected = textwrap.dedent("""\
            n = '١١'
            print(f'{n}')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='١١',
            max_level=5)

    def test_print_keyword_var(self):
        code = textwrap.dedent("""\
            sum is 10
            print sum""")
        expected = textwrap.dedent("""\
            _sum = '10'
            print(f'{_sum}')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='10',
            max_level=5)

    def test_print_var_with_comma(self):
        # test for issue 2549
        code = textwrap.dedent("""\
        name is test
        print name, heya!""")

        expected = textwrap.dedent("""\
        name = 'test'
        print(f'{name}, heya!')""")

        output = textwrap.dedent("""\
        test, heya!""")

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=3)

    #
    # Test comment
    #
    def test_print_comment(self):
        code = "print Hallo welkom bij Hedy! # This is a comment"
        expected = "print(f'Hallo welkom bij Hedy!')"
        output = 'Hallo welkom bij Hedy!'

        self.multi_level_tester(
            max_level=3,
            code=code,
            expected=expected,
            output=output,
            expected_commands=[Keyword.print]
        )

    def test_assign_comment(self):
        code = "test is Welkom bij Hedy # This is a comment"
        expected = "test = 'Welkom bij Hedy'"
        self.multi_level_tester(
            max_level=3,
            code=code,
            expected=expected,
            unused_allowed=True
        )

    #
    # ask tests
    #
    def test_ask(self):
        code = "kleur is ask wat is je lievelingskleur?"
        expected = "kleur = input(f'wat is je lievelingskleur?')"

        self.multi_level_tester(code=code, expected=expected, max_level=3, unused_allowed=True)

    def test_ask_single_quoted_text(self):
        code = "name is ask 'Who's that'"
        expected = """name = input(f'\\'Who\\'s that\\'')"""

        self.multi_level_tester(code=code, expected=expected, max_level=3, unused_allowed=True)

    def test_ask_double_quoted_text(self):
        code = 'var is ask "Welcome to OceanView"'
        expected = "var = input(f'\"Welcome to OceanView\"')"

        self.multi_level_tester(code=code, expected=expected, max_level=3, unused_allowed=True)

    def test_ask_text_with_inner_single_quote(self):
        code = "var is ask Welcome to Hedy's game"
        expected = """var = input(f'Welcome to Hedy\\'s game')"""

        self.multi_level_tester(code=code, expected=expected, max_level=3, unused_allowed=True)

    def test_ask_text_with_inner_double_quote(self):
        code = 'var is ask It says "Hedy"'
        expected = """var = input(f'It says "Hedy"')"""

        self.multi_level_tester(code=code, expected=expected, max_level=3, unused_allowed=True)

    def test_ask_with_comma(self):
        code = textwrap.dedent("""\
        dieren is ask hond, kat, kangoeroe
        print dieren""")

        expected = textwrap.dedent("""\
        dieren = input(f'hond, kat, kangoeroe')
        print(f'{dieren}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_ask_with_number_only(self):
        code = "kleur is ask 42"
        expected = "kleur = input(f'42')"

        self.multi_level_tester(code=code, expected=expected, max_level=3, unused_allowed=True)

    def test_is_ask_without_var_gives_error(self):
        code = "is ask did you forget a var?"

        self.multi_level_tester(
            code=code,
            max_level=3,
            exception=hedy.exceptions.MissingVariableException
        )

    def test_ask_without_assign_gives_error(self):
        code = "ask did you forget a var is?"

        self.multi_level_tester(
            code=code,
            max_level=3,
            exception=hedy.exceptions.WrongLevelException
        )

    def test_ask_is_without_assign_gives_error(self):
        code = "ask is did you forget a var is?"

        self.multi_level_tester(
            code=code,
            max_level=3,
            exception=hedy.exceptions.WrongLevelException
        )

    def test_ask_without_var_gives_error(self):
        code = textwrap.dedent("""\
        prind skipping
        ask is de papier goed?""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 15), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(2, 1, 2, 23), hedy.exceptions.WrongLevelException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            max_level=3,
        )

    def test_ask_without_argument_gives_error(self):
        code = "name is ask"
        self.multi_level_tester(
            max_level=17,
            code=code,
            exception=hedy.exceptions.IncompleteCommandException
        )

    def test_ask_with_var(self):
        code = textwrap.dedent("""\
            name is Hedy
            v is ask are you name?""")

        expected = textwrap.dedent("""\
           name = 'Hedy'
           v = input(f'are you {name}?')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3, unused_allowed=True)

    def test_ask_with_keyword_var(self):
        code = textwrap.dedent("""\
            def is Hedy
            v is ask def""")

        expected = textwrap.dedent("""\
           _def = 'Hedy'
           v = input(f'{_def}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True)

    def test_ask_var_with_comma(self):
        # test for issue 2549
        code = textwrap.dedent("""\
           name is Hedy
           v is ask name, hello!""")

        expected = textwrap.dedent("""\
           name = 'Hedy'
           v = input(f'{name}, hello!')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3, unused_allowed=True)

    def test_ask_number(self):
        code = "n is ask 42"
        expected = "n = input(f'42')"

        self.multi_level_tester(code=code, expected=expected, max_level=3, unused_allowed=True)

    def test_ask_arabic_number(self):
        code = "n is ask ٢٣٤"
        expected = "n = input(f'٢٣٤')"

        self.multi_level_tester(code=code, expected=expected, max_level=3, unused_allowed=True)

    def test_ask_using_defined_var_becomes_literal_string(self):
        code = textwrap.dedent("""\
            name is ask what is your name?""")

        expected = textwrap.dedent("""\
            name = input(f'what is your name?')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3, unused_allowed=True)

    def test_ask_using_defined_var_becomes_literal_string_es(self):
        code = "color is ask ask Cuál es tu color favorito?"
        expected = "color = input(f'ask Cuál es tu color favorito?')"

        self.multi_level_tester(code=code, expected=expected, max_level=3, unused_allowed=True)

    def test_ask_using_defined_var_becomes_literal_string_bengali(self):
        code = textwrap.dedent("""\
        রং is ask আপনার প্রিয় রং কি?
        print রং is আপনার প্রিয""")

        expected = textwrap.dedent("""\
        রং = input(f'আপনার প্রিয় রং কি?')
        print(f'{রং} is আপনার প্রিয')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    #
    # forward tests
    #
    def test_forward_with_number_variable(self):
        code = textwrap.dedent("""\
            a is 50
            forward a""")
        expected = self.dedent(
            "a = '50'",
            self.forward_transpiled('a'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=5)

    def test_forward_with_hindi_number_variable(self):
        code = textwrap.dedent("""\
            a is ५५५
            forward a""")
        expected = self.dedent(
            "a = '५५५'",
            self.forward_transpiled('a'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=5)

    def test_forward_with_keyword_variable(self):
        code = textwrap.dedent("""\
           sum is 50
           forward sum""")
        expected = self.dedent(
            "_sum = '50'",
            self.forward_transpiled('_sum'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=5)

    def test_forward_with_string_variable_gives_type_error(self):
        code = textwrap.dedent("""\
            a is test
            forward a""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            max_level=11)

    #
    # turn tests
    #
    def test_turn_number(self):
        code = "turn 180"
        expected = self.turn_transpiled(180)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    def test_turn_hindi_number(self):
        code = "turn ५५५"
        expected = self.turn_transpiled(555)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    def test_turn_negative_number(self):
        code = "turn -180"
        expected = self.turn_transpiled(-180)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    def test_turn_negative_arabic_number(self):
        code = "turn -١١"
        expected = self.turn_transpiled(-11)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    def test_turn_with_number_var(self):
        code = textwrap.dedent("""\
            direction is 70
            turn direction""")
        expected = self.dedent(
            "direction = '70'",
            self.turn_transpiled('direction'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=5
        )

    def test_turn_with_non_latin_number_var(self):
        code = textwrap.dedent("""\
            الزاوية هو ٩٠
            استدر الزاوية
            تقدم ١٠٠""")
        expected = self.dedent(
            "الزاوية = '٩٠'",
            self.turn_transpiled('الزاوية'),
            self.forward_transpiled(100))

        self.multi_level_tester(
            code=code,
            lang='ar',
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=5,
        )

    def test_one_turn_with_text_gives_type_error(self):
        code = "turn koekoek"

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1
        )

    @parameterized.expand(['left', 'right'])
    def test_one_turn_with_left_or_right_gives_type_error(self, arg):
        code = f"turn {arg}"
        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1,
            max_level=11
        )

    def test_misspelled_command(self):
        code = "prind skipping"

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidCommandException,
            max_level=3,
        )

    def test_access_before_assign_converts_to_literal_string(self):
        code = textwrap.dedent("""\
        print the name program
        name is Hedy""")

        expected = textwrap.dedent("""\
        print(f'the name program')
        name = 'Hedy'""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            max_level=3,
        )

    def test_turn_with_string_var_gives_type_error(self):
        code = textwrap.dedent("""\
            direction is ten
            turn direction""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            max_level=11,
        )

    def test_turn_with_non_ascii_var(self):
        code = textwrap.dedent("""\
            ángulo is 90
            turn ángulo""")
        expected = self.dedent(
            "ángulo = '90'",
            self.turn_transpiled('ángulo'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            expected_commands=['is', 'turn'],
            max_level=5,
        )

    def test_turn_with_keyword_var(self):
        code = textwrap.dedent("""\
            sum is 70
            turn sum""")
        expected = self.dedent(
            "_sum = '70'",
            self.turn_transpiled('_sum'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=5
        )

    # issue #792
    def test_turn_right_number_gives_type_error(self):
        code = textwrap.dedent("""\
        turn right 90
        prind skipping""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 14), hedy.exceptions.InvalidArgumentException),
            SkippedMapping(SourceRange(2, 1, 2, 15), hedy.exceptions.InvalidCommandException)
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            max_level=5,
        )

    #
    # color tests
    #
    @parameterized.expand(hedy.english_colors)
    def test_all_colors(self, color):
        code = f'color {color}'
        expected = self.color_transpiled(color)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=3
        )

    def test_color_red_ar(self):
        code = 'لون احمر'
        expected = self.color_transpiled('red', lang='ar')

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=3,
            lang='ar'
        )

    def test_one_color_nl(self):
        lang = 'nl'
        code = "kleur blauw"
        expected = self.color_transpiled('blue', lang)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            lang=lang,
            max_level=3
        )

    def test_color_with_var(self):
        code = textwrap.dedent("""\
            foo is white
            color foo""")
        expected = self.dedent(
            "foo = 'white'",
            self.color_transpiled('{foo}')
        )

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=5
        )

    def test_color_with_keyword_var(self):
        code = textwrap.dedent("""\
            sum is white
            color sum""")
        expected = self.dedent(
            "_sum = 'white'",
            self.color_transpiled('{_sum}')
        )

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=5
        )

    def test_color_with_number_gives_type_error(self):
        code = "color 14"
        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1,
            max_level=10,
        )

    #
    # sleep tests
    #
    def test_sleep(self):
        code = "sleep"
        expected = "time.sleep(1)"

        self.multi_level_tester(code=code, expected=expected)

    def test_sleep_micro_bit_argument(self):
        code = "sleep 2"
        expected = "sleep(2000)"

        self.multi_level_tester(code=code, expected=expected, max_level=11, microbit=True)

    def test_sleep_micro_bit_no_argument(self):
        code = "sleep"
        expected = "sleep(1000)"

        self.multi_level_tester(code=code, expected=expected, max_level=18, microbit=True)

    def test_sleep_micro_bit_variable_argument(self):
        code = textwrap.dedent("""\
            duration is 2
            sleep duration""")
        expected = textwrap.dedent("""\
            duration = 2
            sleep(duration * 1000)""")

        self.multi_level_tester(code=code, expected=expected, max_level=5, microbit=True)

    def test_sleep_with_default_number(self):
        code = "sleep 1"
        expected = self.sleep_transpiled('"1"')

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_sleep_with_number(self):
        code = "sleep 20"
        expected = self.sleep_transpiled('"20"')

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_sleep_with_number_hi(self):
        code = "sleep २"
        expected = self.sleep_transpiled('"2"')

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_sleep_with_number_ar(self):
        code = "sleep ٣"
        expected = self.sleep_transpiled('"3"')

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_sleep_with_non_decimal_gives_error(self):
        code = "sleep ፼"

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.NonDecimalVariable
        )

    def test_sleep_with_number_variable(self):
        code = textwrap.dedent("""\
            n is 2
            sleep n""")
        expected = self.dedent(
            "n = '2'",
            self.sleep_transpiled("n"))

        self.multi_level_tester(max_level=5, code=code, expected=expected)

    def test_sleep_with_keyword_variable(self):
        code = textwrap.dedent("""\
            sum is 2
            sleep sum""")
        expected = self.dedent(
            "_sum = '2'",
            self.sleep_transpiled("_sum"))

        self.multi_level_tester(max_level=5, code=code, expected=expected)

    def test_sleep_with_number_variable_hi(self):
        code = textwrap.dedent("""\
            n is २
            sleep n""")
        expected = self.dedent(
            "n = '२'",
            self.sleep_transpiled("n"))

        self.multi_level_tester(max_level=5, code=code, expected=expected)

    def test_sleep_with_input_variable(self):
        code = textwrap.dedent("""\
            n is ask how long
            sleep n""")
        expected = self.dedent(
            "n = input(f'how long')",
            self.sleep_transpiled("n"))

        self.multi_level_tester(max_level=3, code=code, expected=expected)

    def test_sleep_with_string_variable_gives_error(self):
        code = textwrap.dedent("""\
            n is test
            sleep n""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    #
    # assign tests
    #

    def test_assign_with_space_gives_invalid(self):
        code = textwrap.dedent("""\
         naam is Hedy
        prind skipping""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 14), hedy.exceptions.UnusedVariableException),
            SkippedMapping(SourceRange(2, 1, 2, 15), hedy.exceptions.InvalidCommandException)
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            unused_allowed=True,
            max_level=5
        )

    def test_assign(self):
        code = "naam is Felienne"
        expected = "naam = 'Felienne'"

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True)

    def test_assign_with_var_starting_with_ask(self):
        code = "asks is Felienne"
        expected = "asks = 'Felienne'"

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True)

    def test_assign_keyword_var(self):
        code = "sum is Felienne"
        expected = "_sum = 'Felienne'"

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True)

    def test_assign_micro_bit(self):
        code = "naam is Felienne"
        expected = "naam = 'Felienne'"

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True, microbit=True)

    def test_assign_catalan_var_name(self):
        code = textwrap.dedent("""\
            print És hora una nit de Netflix
            pel·lícula is Sonic the Hedgehog 2
            print Veurem una pel·lícula""")

        expected = textwrap.dedent("""\
            print(f'És hora una nit de Netflix')
            pel·lícula = 'Sonic the Hedgehog 2'
            print(f'Veurem una {pel·lícula}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=3)

    def test_assign_integer(self):
        code = "naam is 14"
        expected = "naam = '14'"

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True)

    def test_assign_unused(self):
        code = textwrap.dedent("""\
            x is 10""")

        self.multi_level_tester(max_level=3, code=code, exception=hedy.exceptions.UnusedVariableException)

    def test_assign_single_quoted_text(self):
        code = "naam is 'Felienne'"
        expected = "naam = '\\'Felienne\\''"

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True)

    def test_assign_double_quoted_string(self):
        code = 'naam is "Felienne"'
        expected = """naam = '"Felienne"'"""

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True)

    def test_assign_text_with_inner_single_quote(self):
        code = "var is Hedy's"
        expected = "var = 'Hedy\\'s'"

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True)

    def test_assign_text_with_inner_double_quote(self):
        code = 'var is It says "Hedy"'
        expected = """var = 'It says "Hedy"'"""

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True)

    def test_assign_text_to_hungarian_var(self):
        code = textwrap.dedent("""\
        állatok is kutya
        print állatok""")

        expected = textwrap.dedent("""\
        állatok = 'kutya'
        print(f'{állatok}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=5)

    def test_assign_bengali_var(self):
        var = hedy.escape_var("নাম")
        code = "নাম is হেডি"
        expected = f"{var} = 'হেডি'"

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True)

    def test_assign_python_keyword(self):
        code = "for is Hedy"
        expected = "_for = 'Hedy'"

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True)

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
        kleur = input(f'wat is je lievelingskleur?')
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
        expected = self.dedent(
            "afstand = input(f'hoe ver dan?')",
            self.forward_transpiled('afstand'))

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

        expected = self.dedent(
            "print(f'Turtle race')",
            "direction = input(f'Where to turn?')",
            self.turn_transpiled('direction'))

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

        self.multi_level_tester(code=code, expected=expected, max_level=3, unused_allowed=True)

    #
    # negative tests
    #
    def test_echo_gives_error(self):
        code = textwrap.dedent("""\
        ask what is jouw lievelingskleur?
        echo Jouw lievelingskleur is dus...""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 34), hedy.exceptions.WrongLevelException),
            SkippedMapping(SourceRange(2, 1, 2, 36), hedy.exceptions.WrongLevelException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            extra_check_function=lambda c: c.error_code == 'Wrong Level',
            max_level=3
        )

    #
    # play tests / music tests
    #
    def test_play_var(self):
        code = textwrap.dedent("""\
            n is C4
            play n""")

        expected = self.dedent(
            "n = 'C4'",
            self.play_transpiled('n'))

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected,
            max_level=5
        )

    def test_play_keyword_var(self):
        code = textwrap.dedent("""\
            return is C4
            play return""")

        expected = self.dedent(
            "_return = 'C4'",
            self.play_transpiled('_return'))

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected,
            max_level=5
        )

    def test_play_arabic_number_var(self):
        code = textwrap.dedent("""\
            n is ١١
            play n""")

        expected = self.dedent(
            "n = '١١'",
            self.play_transpiled('n'))

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected,
            max_level=5
        )

    def test_play_undefined(self):
        code = textwrap.dedent("""\
            play n""")

        self.multi_level_tester(
            code=code,
            translate=False,
            exception=hedy.exceptions.UndefinedVarException,
            max_level=11
        )
