import textwrap
import hedy
from hedy import Command
from hedy_sourcemap import SourceRange
from tests.Tester import HedyTester, SkippedMapping

from hypothesis import given, settings
import hypothesis.strategies


class TestsLevel1(HedyTester):
    level = 1
    '''
    Tests should be ordered as follows:
     * commands in the order of hedy.py e.g. for level 1: ['print', 'ask', 'echo', 'turn', 'forward']
     * combined tests
     * markup tests
     * negative tests
     * hypothesis tests

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
        expected = "print('Hallo welkom bij Hedy!')"
        output = 'Hallo welkom bij Hedy!'
        expected_commands = [Command.print]

        self.single_level_tester(
            code=code,
            expected=expected,
            output=output,
            expected_commands=expected_commands

        )

    def test_print_no_space(self):
        code = "printHallo welkom bij Hedy!"
        expected = "print('Hallo welkom bij Hedy!')"
        output = 'Hallo welkom bij Hedy!'
        expected_commands = [Command.print]

        self.single_level_tester(
            code=code,
            expected=expected,
            output=output,
            expected_commands=expected_commands
        )

    def test_print_line_with_spaces_works(self):
        code = "print hallo\n      \nprint hallo"
        expected = "print('hallo')\n\nprint('hallo')"
        expected_commands = [Command.print, Command.print]

        self.single_level_tester(code=code, expected=expected, expected_commands=expected_commands)

    def test_print_comma(self):
        code = "print one, two, three"
        expected = "print('one, two, three')"
        expected_commands = [Command.print]

        self.single_level_tester(code=code, expected=expected, expected_commands=expected_commands)

    def test_print_multiple_lines(self):
        code = textwrap.dedent("""\
        print Hallo welkom bij Hedy
        print Mooi hoor""")

        expected = textwrap.dedent("""\
        print('Hallo welkom bij Hedy')
        print('Mooi hoor')""")

        output = textwrap.dedent("""\
        Hallo welkom bij Hedy
        Mooi hoor""")

        self.single_level_tester(code=code, expected=expected, output=output)

    def test_print_single_quoted_text(self):
        code = "print 'Welcome to OceanView!'"
        expected = "print('\\'Welcome to OceanView!\\'')"
        output = "'Welcome to OceanView!'"

        self.single_level_tester(code=code, expected=expected, output=output)

    def test_print_double_quoted_text(self):
        code = 'print "Welcome to OceanView!"'
        expected = """print('"Welcome to OceanView!"')"""
        output = '"Welcome to OceanView!"'

        self.single_level_tester(code=code, expected=expected, output=output)

    def test_print_text_with_inner_single_quote(self):
        code = "print Welcome to Hedy's game!"
        expected = """print('Welcome to Hedy\\'s game!')"""

        self.single_level_tester(code=code, expected=expected)

    def test_print_text_with_inner_double_quote(self):
        code = 'print It says "Hedy"'
        expected = """print('It says "Hedy"')"""

        self.single_level_tester(code=code, expected=expected)

    def test_print_slash(self):
        code = "print Yes/No"
        expected = "print('Yes/No')"
        output = "Yes/No"

        self.single_level_tester(code=code, expected=expected, output=output)

    def test_print_backslash(self):
        code = "print Yes\\No"
        expected = "print('Yes\\\\No')"
        output = "Yes\\No"

        self.single_level_tester(code=code, expected=expected, output=output)

    def test_print_backslash_at_end(self):
        code = "print Welcome to \\"
        expected = "print('Welcome to \\\\')"
        output = "Welcome to \\"

        self.single_level_tester(code=code, expected=expected, output=output)

    def test_print_with_spaces(self):
        code = "print        hallo!"
        expected = "print('hallo!')"

        self.single_level_tester(code=code, expected=expected)

    def test_print_nl(self):
        code = "print Hallo welkom bij Hedy!"
        expected = "print('Hallo welkom bij Hedy!')"
        output = 'Hallo welkom bij Hedy!'

        self.single_level_tester(code=code, expected=expected, output=output, lang='nl')

    def test_print_ar(self):
        code = "قول أهلا ومرحبا بكم في هيدي!"
        expected = "print('أهلا ومرحبا بكم في هيدي!')"
        output = 'أهلا ومرحبا بكم في هيدي!'

        self.single_level_tester(code=code, expected=expected, output=output, lang='ar')

    def test_print_ar_tatweel_all_places(self):
        code = "ـــقــولـ أ"
        expected = "print('أ')"
        output = 'أ'

        self.single_level_tester(
            code=code,
            expected=expected,
            output=output,
            translate=False,  # translation will remove the tatweels, we will deal with that later
            lang='ar')

    def test_ask_ar_tatweel_all_places(self):
        code = "اســأل أ"
        expected = "answer = input('أ')"

        self.single_level_tester(
            code=code,
            expected=expected,
            translate=False,  # translation will remove the tatweels, we will deal with that later
            lang='ar')

    # def test_print_ar_tatweel_itself(self):
    # FH, May 2022, sadly beginning a string with tatweel does not work
    # would need complex changes to the grammar (documented further in the grammar of level 1)
    # so I am leaving this as it is for now
    #     code = "قول ـ"
    #     expected = "print('ـ')"
    #     output = 'ـ'
    #
    #     self.single_level_tester(
    #         code=code,
    #         expected=expected,
    #         output=output,
    #         translate=False, #translation will remove the tatweels, we will deal with that later
    #         lang='ar')

    def test_print_ar_tatweel_printing(self):
        code = "قول لــــ"
        expected = "print('لــــ')"
        output = 'لــــ'

        self.single_level_tester(
            code=code,
            expected=expected,
            output=output,
            translate=False,  # translation will remove the tatweels, we will deal with that later
            lang='ar')

    def test_print_ar_tatweel_begin(self):
        code = "ـــقول أ"
        expected = "print('أ')"
        output = 'أ'

        self.single_level_tester(
            code=code,
            expected=expected,
            output=output,
            translate=False,  # translation will remove the tatweels, we will deal with that later
            lang='ar')

    def test_print_ar_tatweel_multiple_end(self):
        code = "ـــقــوـلــــ أ"
        expected = "print('أ')"
        output = 'أ'

        self.single_level_tester(
            code=code,
            expected=expected,
            output=output,
            translate=False,  # translation will remove the tatweels, we will deal with that later
            lang='ar')

    def test_print_ar_2(self):
        code = "قول مرحبا أيها العالم!"
        expected = "print('مرحبا أيها العالم!')"
        output = 'مرحبا أيها العالم!'

        self.single_level_tester(code=code, expected=expected, output=output, lang='ar')

    #
    # ask tests
    #
    def test_ask(self):
        code = "ask wat is je lievelingskleur?"
        expected = "answer = input('wat is je lievelingskleur?')"

        self.single_level_tester(code=code, expected=expected)

    def test_ask_single_quoted_text(self):
        code = "ask 'Welcome to OceanView?'"
        expected = "answer = input('\\'Welcome to OceanView?\\'')"

        self.single_level_tester(code=code, expected=expected)

    def test_ask_double_quoted_text(self):
        code = 'ask "Welcome to OceanView?"'
        expected = "answer = input('\"Welcome to OceanView?\"')"

        self.single_level_tester(code=code, expected=expected)

    def test_ask_text_with_inner_single_quote(self):
        code = "ask Welcome to Hedy's game!"
        expected = """answer = input('Welcome to Hedy\\'s game!')"""

        self.single_level_tester(code=code, expected=expected)

    def test_ask_text_with_inner_double_quote(self):
        code = 'ask It says "Hedy"'
        expected = """answer = input('It says "Hedy"')"""

        self.single_level_tester(code=code, expected=expected)

    def test_ask_es(self):
        code = "ask ask Cuál es tu color favorito?"
        expected = "answer = input('ask Cuál es tu color favorito?')"

        self.single_level_tester(code=code, expected=expected)

    def test_ask_nl_code_transpiled_in_nl(self):
        code = "vraag Heb je er zin in?"
        expected = "answer = input('Heb je er zin in?')"

        self.single_level_tester(code=code, expected=expected, lang='nl')

    def test_ask_en_code_transpiled_in_nl(self):
        code = "ask Heb je er zin in?"
        expected = "answer = input('Heb je er zin in?')"

        self.single_level_tester(
            code=code,
            expected=expected,
            lang='nl',
            translate=False  # we are trying a Dutch keyword in en, can't be translated
        )

    def test_play_no_args(self):
        code = "play "
        expected = self.play_transpiled('C4')

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected,
            max_level=2
        )

    def test_play(self):
        code = "play A"
        expected = self.play_transpiled('A')

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected
        )

    def test_print_microbit(self):
        code = "print a"
        expected = textwrap.dedent(f"""\
                display.scroll('a')""")

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            expected=expected,
            max_level=3,
            microbit=True
        )

    def test_play_lowercase(self):
        code = "play a"
        expected = self.play_transpiled('A')

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected
        )

    def test_play_int(self):
        code = "play 34"
        expected = self.play_transpiled(34)

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected
        )

    def test_mixes_languages_nl_en(self):
        code = textwrap.dedent("""\
        vraag Heb je er zin in?
        echo
        ask are you sure?
        print mooizo!""")

        expected = textwrap.dedent("""\
        answer = input('Heb je er zin in?')
        print(answer)
        answer = input('are you sure?')
        print('mooizo!')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            expected_commands=['ask', 'echo', 'ask', 'print'],
            lang='nl',
            translate=False  # mixed codes will not translate back to their original form, sadly
        )

    #
    # echo tests
    #
    def test_echo_without_argument(self):
        code = "ask wat?\necho"
        expected = "answer = input('wat?')\nprint(answer)"

        self.single_level_tester(code=code, expected=expected)

    def test_echo_with_quotes(self):
        code = textwrap.dedent("""\
        ask waar?
        echo oma's aan de""")

        expected = textwrap.dedent("""\
        answer = input('waar?')
        print('oma\\'s aan de '+answer)""")

        self.single_level_tester(code=code, expected=expected)

    #
    # forward tests
    #
    def test_forward(self):
        code = "forward 50"
        expected = HedyTester.dedent(HedyTester.forward_transpiled(50, self.level))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    def test_forward_arabic_numeral(self):
        code = "forward ١١١١١١١"
        expected = HedyTester.forward_transpiled(1111111, self.level)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    def test_forward_hindi_numeral(self):
        code = "forward ५५५"
        expected = HedyTester.forward_transpiled(555, self.level)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    def test_forward_without_argument(self):
        code = 'forward'
        expected = textwrap.dedent("""\
        t.forward(50)
        time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    def test_forward_with_text_gives_type_error(self):
        code = "forward lalalala"

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1
        )

    def test_multiple_forward_without_arguments(self):
        code = textwrap.dedent("""\
        forward
        forward""")
        expected = textwrap.dedent("""\
        t.forward(50)
        time.sleep(0.1)
        t.forward(50)
        time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    #
    # color tests
    #
    def test_color_no_args(self):
        code = "color"
        expected = "t.pencolor('black')"
        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=10)

    def test_one_color_red(self):
        code = "color red"
        expected = "t.pencolor('red')"

        self.single_level_tester(code=code, expected=expected,
                                 extra_check_function=self.is_turtle())

    def test_one_color_purple(self):
        code = "color purple"
        expected = "t.pencolor('purple')"

        self.single_level_tester(code=code, expected=expected,
                                 extra_check_function=self.is_turtle())

    def test_one_color_purple_nl(self):
        code = "kleur paars"
        expected = "t.pencolor('purple')"

        self.single_level_tester(code=code, expected=expected,
                                 extra_check_function=self.is_turtle(), lang='nl')

    #
    # turn tests
    #
    def test_turn_no_args(self):
        code = "turn"
        expected = "t.right(90)"

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_turn_right(self):
        code = "turn right"
        expected = "t.right(90)"

        self.single_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_turn_left(self):
        code = "turn left"
        expected = "t.left(90)"

        self.single_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_turn_left_nl(self):
        code = "draai links"
        expected = "t.left(90)"

        self.single_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            lang='nl'
        )

    def test_turn_ar(self):
        # doesn't translate, I don't know why!!
        code = "استدر يسار"
        expected = "t.left(90)"

        self.single_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            lang='ar'
        )

    def test_turn_with_text_gives_error(self):
        code = textwrap.dedent("""\
        turn koekoek
        prind skipping""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        # We test the skipping of faulty code by checking if a certain range contains an error after executing
        # The source range consists of from_line, from_column, to_line, to_column
        # we can add multiple tests to the skipped_mappings list to test multiple error mappings

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 13), hedy.exceptions.InvalidArgumentException),
            SkippedMapping(SourceRange(2, 1, 2, 15), hedy.exceptions.InvalidCommandException),
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    #
    # comment tests
    #
    def test_comment(self):
        code = "# geen commentaar, helemaal geen!"
        expected = ""

        self.multi_level_tester(code=code, expected=expected)

    def test_print_comment(self):
        code = "print Hallo welkom bij Hedy! # This is a print"
        expected = "print('Hallo welkom bij Hedy! ')"
        output = 'Hallo welkom bij Hedy!'

        self.single_level_tester(
            code=code,
            expected=expected,
            output=output,
            expected_commands=[Command.print]
        )

    #
    # combined commands tests
    #
    def test_print_ask_echo(self):
        code = textwrap.dedent("""\
        print Hallo
        ask Wat is je lievelingskleur
        echo je lievelingskleur is""")

        expected = textwrap.dedent("""\
        print('Hallo')
        answer = input('Wat is je lievelingskleur')
        print('je lievelingskleur is '+answer)""")

        self.single_level_tester(
            code=code,
            expected=expected,
            expected_commands=[Command.print, Command.ask, Command.echo])

    def test_forward_turn_combined(self):
        code = textwrap.dedent("""\
            forward 50
            turn
            forward 100""")

        expected = HedyTester.dedent(
            HedyTester.forward_transpiled(50, self.level),
            't.right(90)',
            HedyTester.forward_transpiled(100, self.level))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            expected_commands=[Command.forward, Command.turn, Command.forward],
            max_level=11
        )

    #
    # markup tests
    #
    def test_lines_may_end_in_spaces(self):
        code = "print Hallo welkom bij Hedy! "
        expected = "print('Hallo welkom bij Hedy! ')"
        output = 'Hallo welkom bij Hedy!'

        self.single_level_tester(code=code, expected=expected, output=output, translate=False)

    def test_comments_may_be_empty(self):
        code = textwrap.dedent("""\
            #
            # This is a comment
            #
            print Привіт, Хейді!""")
        expected = "print('Привіт, Хейді!')"
        output = "Привіт, Хейді!"

        self.single_level_tester(code=code, expected=expected, output=output)

    #
    # negative tests
    #
    def test_print_with_space_gives_invalid(self):
        code = textwrap.dedent("""\
         print Hallo welkom bij Hedy!
        prind skipping""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 30), hedy.exceptions.InvalidSpaceException),
            SkippedMapping(SourceRange(2, 1, 2, 15), hedy.exceptions.InvalidCommandException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            max_level=1)

    def test_ask_with_space_gives_invalid(self):
        code = textwrap.dedent("""\
         ask Hallo welkom bij Hedy?
        prind skipping""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 28), hedy.exceptions.InvalidSpaceException),
            SkippedMapping(SourceRange(2, 1, 2, 15), hedy.exceptions.InvalidCommandException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            max_level=1)

    def test_lines_with_spaces_english_gives_invalid(self):
        code = textwrap.dedent("""\
         print Hallo welkom bij Hedy!
            print Hallo welkom bij Hedy!""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidSpaceException,
            skip_faulty=False,
            max_level=3)

    def test_lines_with_spaces_french_gives_invalid(self):
        code = textwrap.dedent("""\
         affiche Bonjour Hedy!
            affiche Bonjour Hedy!""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidSpaceException,
            skip_faulty=False,
            lang='fr',
            max_level=3)

    def test_lines_with_spaces_gives_invalid(self):
        code = " print Hallo welkom bij Hedy!\n print Hallo welkom bij Hedy!"
        expected = "pass\npass"

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 30), hedy.exceptions.InvalidSpaceException),
            SkippedMapping(SourceRange(1, 1, 1, 30), hedy.exceptions.InvalidSpaceException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            max_level=3)

    def test_word_plus_period_gives_invalid(self):
        code = textwrap.dedent("""\
        word.
        prind skipping""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 6), hedy.exceptions.MissingCommandException),
            SkippedMapping(SourceRange(2, 1, 2, 15), hedy.exceptions.InvalidCommandException),
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    def test_non_keyword_gives_invalid(self):
        code = textwrap.dedent("""\
        groen
        prind skipping""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 6), hedy.exceptions.MissingCommandException),
            SkippedMapping(SourceRange(2, 1, 2, 15), hedy.exceptions.InvalidCommandException),
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    def test_one_mistake_not_skipped(self):
        code = "prind wrong"

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidCommandException,
            max_level=3
        )

    def test_lonely_echo_gives_LonelyEcho(self):
        code = "echo wat dan?"
        self.single_level_tester(
            code,
            exception=hedy.exceptions.LonelyEchoException)

    def test_echo_before_ask_gives_lonely_echo(self):
        code = textwrap.dedent("""\
        echo what can't we do?
        ask time travel""")
        self.single_level_tester(code, exception=hedy.exceptions.LonelyEchoException)

    def test_pint_after_empty_line_gives_error_line_3(self):
        code = textwrap.dedent("""\
        print hallo

        prnt hallo
        prind skipping""")

        expected = textwrap.dedent("""\
        print('hallo')
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(3, 1, 3, 11), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(4, 1, 4, 15), hedy.exceptions.InvalidCommandException),
        ]

        self.single_level_tester(
            code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    def test_print_without_argument_gives_incomplete(self):
        self.multi_level_tester(
            code="print",
            exception=hedy.exceptions.IncompleteCommandException,
            extra_check_function=lambda c: c.exception.arguments['incomplete_command'] == 'print'
        )

    def test_print_without_argument_gives_incomplete_2(self):
        self.multi_level_tester(
            code="print lalalala\nprint",
            exception=hedy.exceptions.IncompleteCommandException,
            extra_check_function=lambda c: c.exception.arguments['incomplete_command'] == 'print',
            max_level=17,
        )

    def test_non_keyword_with_argument_gives_invalid(self):
        code = textwrap.dedent("""\
        aks felienne 123
        prind skipping""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 17), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(2, 1, 2, 15), hedy.exceptions.InvalidCommandException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            translate=False,
            extra_check_function=lambda c: c.arguments['invalid_command'] in ['aks', 'prind'],
            max_level=5,
        )

    def test_source_map(self):
        code = textwrap.dedent("""\
        print Hallo welkom bij Hedy!
        forward 50
        ask Wat is je lievelingskleur
        echo je lievelingskleur is""")

        expected_code = HedyTester.dedent(f"""\
        print('Hallo welkom bij Hedy!')
        {HedyTester.indent(
            HedyTester.forward_transpiled(50, self.level),
            8, True)
         }
        answer = input('Wat is je lievelingskleur')
        print('je lievelingskleur is '+answer)""")

        expected_source_map = {
            '1/1-1/29': '1/1-1/32',
            '2/1-2/11': '2/1-4/16',
            '3/1-3/30': '5/1-5/44',
            '4/1-4/27': '6/1-6/39',
            '1/1-4/28': '1/1-6/39'
        }

        self.single_level_tester(code, expected=expected_code)
        self.source_map_tester(code=code, expected_source_map=expected_source_map)

# hypothesis initialization starts here


# numbers define an order since some commands must be in a certain place (f.e. here: ask must go before echo)
templates = [
    ("print <P>", -1),
    ("print <P>", -1),
    ("print <P>", -1),
    ("turn left", -1),  # arguments for turn and forward could also be randomly sampled
    ("turn right", -1),
    ("forward 200", -1),
    ("forward -200", -1),
    ("ask <P>", 1),
    ("echo <P>", 2),
    ("ask <P>", 3),
    ("echo <P>", 4)
]


def valid_permutation(lines):
    orders = [order for _, order in lines]
    significant_orders = [x for x in orders if x > 0]  # -1 may be placed everywhere
    list = [significant_orders[i] <= significant_orders[i+1] for i in range(len(significant_orders)-1)]
    return all(list)


class TestsHypothesisLevel1(HedyTester):
    level = 1

    @given(code_tuples=hypothesis.strategies.permutations(templates), d=hypothesis.strategies.data())
    @settings(deadline=None, max_examples=100)
    # FH may 2023: we now always use a permutation, but a random sample which could potentially be smaller would be a nice addition!
    def test_template_combination(self, code_tuples, d):
        excluded_chars = ["_", "#", '\n', '\r']
        random_print_argument = hypothesis.strategies.text(
            alphabet=hypothesis.strategies.characters(blacklist_characters=excluded_chars),
            min_size=1,
            max_size=10)

        if valid_permutation(code_tuples):
            lines = [line.replace("<P>", d.draw(random_print_argument)) for line, _ in code_tuples]
            code = '\n'.join(lines)

            self.single_level_tester(
                code=code,
                translate=False
            )

            expected_commands = [Command.ask, Command.ask, Command.echo, Command.echo, Command.forward, Command.forward,
                                 Command.print, Command.print, Command.print, Command.turn, Command.turn]

            # TODO, FH sept 2023: all_commands parses and thus is expensive
            # we should get the commands list back from the parser instead (parseresult.commands)
            # since we don't use many single_level_tester features
            # we can transpile and check the python "manually"
            all_commands = sorted(hedy.all_commands(code, self.level, 'en'))
            self.assertEqual(expected_commands, all_commands)
