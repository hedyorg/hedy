import textwrap

from parameterized import parameterized

import hedy
from hedy import Command
from hedy_sourcemap import SourceRange
# from hedy_sourcemap import SourceRange
from tests.Tester import HedyTester, SkippedMapping  # , SkippedMapping


class TestsLevel12(HedyTester):
    level = 12
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
    def test_print_float_variable(self):
        code = textwrap.dedent("""\
            pi is 3.14
            print pi""")
        expected = textwrap.dedent("""\
            pi = 3.14
            print(f'''{pi}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    def test_print_float(self):
        code = "print 3.14"

        expected = "print(f'''3.14''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            output='3.14'
        )

    def test_print_division_float(self):
        code = "print 3 / 2"
        expected = f"print(f'''{{{self.number_cast_transpiled(3)} / {self.number_cast_transpiled(2)}}}''')"
        output = "1.5"

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=17,
            output=output
        )

    def test_sleep_division_float(self):
        code = "sleep 1 / 20"
        expected = HedyTester.sleep_command_transpiled(
            f'{self.number_cast_transpiled(1)} / {self.number_cast_transpiled(20)}')

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=17
        )

    def test_sleep_division_float_var(self):
        code = textwrap.dedent("""\
        time = 0.2
        sleep time""")

        expected = HedyTester.dedent("""\
            _time = 0.2""",
                                     HedyTester.sleep_command_transpiled('_time')
                                     )

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=17
        )

    def test_sleep_division_float_literal(self):
        code = textwrap.dedent("""\
        sleep 0.2""")

        expected = HedyTester.dedent(
            HedyTester.sleep_command_transpiled('0.2')
        )

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=15
        )

    def test_print_microbit(self):
        code = "print 'a'"
        expected = textwrap.dedent(f"""\
                display.scroll('a')""")

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            expected=expected,
            max_level=17,
            microbit=True
        )

    def test_print_literal_strings(self):
        code = """print "It's " '"Hedy"!'"""
        expected = """print(f'''It\\'s "Hedy"!''')"""

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
        )

    def test_print_line_with_spaces_works(self):
        code = "print 'hallo'\n      \nprint 'hallo'"
        expected = "print(f'''hallo''')\nprint(f'''hallo''')"
        expected_commands = [Command.print, Command.print]

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=expected_commands,
            max_level=17)

    def test_print_string_with_triple_quotes_gives_error(self):
        code = textwrap.dedent("""\
            var = " is not allowed"
            print "'''" + var """)

        self.multi_level_tester(
            code=code,
            max_level=17,
            translate=False,
            exception=hedy.exceptions.UnsupportedStringValue
        )

    # issue #745
    def test_print_list_gives_type_error(self):
        code = textwrap.dedent("""\
            plaatsen is 1, 2, 3
            print plaatsen""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_print_subtraction_with_text(self):
        code = "print 'And the winner is ' 5 - 5"
        five = self.number_cast_transpiled(5)
        expected = f"print(f'''And the winner is {{{five} - {five}}}''')"
        output = 'And the winner is 0'

        self.multi_level_tester(max_level=17, code=code, expected=expected, output=output)

    def test_print_list_random(self):
        code = textwrap.dedent("""\
            numbers is 1, 2, 4
            print numbers at random""")

        expected = HedyTester.dedent("""\
            numbers = [1, 2, 4]""",
                                     HedyTester.list_access_transpiled('random.choice(numbers)'),
                                     "print(f'''{random.choice(numbers)}''')")

        self.multi_level_tester(
            code=code,
            max_level=15,
            expected=expected,
            expected_commands=['is', 'print', 'random']
        )

    def test_print_list_access_index(self):
        code = textwrap.dedent("""\
        numbers is 5, 4, 3
        print numbers at 1""")

        expected = HedyTester.dedent("""\
        numbers = [5, 4, 3]""",
                                     HedyTester.list_access_transpiled('numbers[int(1)-1]'),
                                     "print(f'''{numbers[int(1)-1]}''')")

        check_in_list = (lambda x: HedyTester.run_code(x) == '5')

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            extra_check_function=check_in_list
        )

    def test_print_single_quoted_text(self):
        code = "print 'hallo wereld!'"
        expected = "print(f'''hallo wereld!''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_chinese_quoted_text(self):
        code = "print “逃离鬼屋！”"
        expected = "print(f'''逃离鬼屋！''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_french_quoted_text(self):
        code = "print «bonjour tous le monde!»"
        expected = "print(f'''bonjour tous le monde!''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_chinese_double_quoted_text(self):
        code = "print ‘逃离鬼屋！’"
        expected = "print(f'''逃离鬼屋！''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_double_quoted_text(self):
        code = 'print "hallo wereld!"'
        expected = "print(f'''hallo wereld!''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_single_quoted_text_with_inner_double_quote(self):
        code = """print 'quote is "'"""
        expected = """print(f'''quote is "''')"""

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_double_quoted_text_with_inner_single_quote(self):
        code = '''print "It's me"'''
        expected = """print(f'''It\\'s me''')"""

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_no_space(self):
        code = "print'hallo wereld!'"
        expected = "print(f'''hallo wereld!''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_comma(self):
        code = "print 'Hi, I am Hedy'"
        expected = "print(f'''Hi, I am Hedy''')"
        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    def test_print_slash(self):
        code = "print 'Yes/No'"
        expected = "print(f'''Yes/No''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_backslash(self):
        code = "print 'Yes\\No'"
        expected = "print(f'''Yes\\\\No''')"
        output = "Yes\\No"

        self.multi_level_tester(
            code=code,
            expected=expected,
            output=output,
            max_level=17,
            translate=True
        )

    def test_print_with_backslash_at_end(self):
        code = "print 'Welcome to \\'"
        expected = "print(f'''Welcome to \\\\''')"
        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            translate=True
        )

    def test_print_with_spaces(self):
        code = "print        'hallo!'"
        expected = "print(f'''hallo!''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_asterisk(self):
        code = "print '*Jouw* favoriet is dus kleur'"
        expected = "print(f'''*Jouw* favoriet is dus kleur''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_single_quoted_text_var(self):
        code = textwrap.dedent("""\
        naam is "'Hedy'"
        print 'ik heet ' naam""")

        expected = textwrap.dedent("""\
        naam = "'Hedy'"
        print(f'''ik heet {naam}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_double_quoted_text_var(self):
        code = textwrap.dedent("""\
        naam is '"Hedy"'
        print 'ik heet ' naam""")

        expected = textwrap.dedent("""\
        naam = '"Hedy"'
        print(f'''ik heet {naam}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    # issue 1795
    def test_print_quoted_var_reference(self):
        code = textwrap.dedent("""\
        naam is "'Daan'"
        woord1 is 'zomerkamp'
        print 'naam' ' is naar het' 'woord1'""")

        expected = textwrap.dedent("""\
        naam = "'Daan'"
        woord1 = 'zomerkamp'
        print(f'''naam is naar hetwoord1''')""")

        self.multi_level_tester(code=code,
                                expected=expected,
                                unused_allowed=True,
                                max_level=17)

    @parameterized.expand(HedyTester.quotes)
    def test_print_concat_quoted_strings(self, q):
        code = f"""print {q}Hi {q} + {q}there{q}"""
        expected = f"""print(f'''{{{self.addition_transpiled("'Hi '", "'there'")}}}''')"""

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_concat_double_quoted_strings_with_inner_single_quotes(self):
        code = '''print "Hi there! " + "It's Hedy!"'''
        left = "'Hi there! '"
        right = '"It\'s Hedy!"'
        expected = f"""print(f'''{{{self.addition_transpiled(left, right)}}}''')"""

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.quotes)
    def test_print_concat_var_and_literal_string(self, q):
        code = textwrap.dedent(f"""\
        hi = {q}Hi{q}
        print hi + {q} there{q}""")
        expected = textwrap.dedent(f"""\
        hi = 'Hi'
        print(f'''{{{self.addition_transpiled('hi', "' there'")}}}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_chained_assignments(self):
        code = textwrap.dedent("""\
            x is 1 + 2
            y is x + 3
            print y + 4""")

        expected = textwrap.dedent(f"""\
            x = 1 + 2
            y = {self.addition_transpiled('x', 3)}
            print(f'''{{{self.addition_transpiled('y', 4)}}}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_assign_to_list_access(self):
        code = textwrap.dedent("""\
            field = '.', '.', '.', '.', '.', '.'
            field at 1 = 'x'
            print field at 1""")

        expected = textwrap.dedent(f"""\
            field = ['.', '.', '.', '.', '.', '.']
            field[int(1)-1] = 'x'
            try:
              field[int(1)-1]
            except IndexError:
              raise Exception({self.index_exception_transpiled()})
            print(f'''{{field[int(1)-1]}}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    def test_if_and_list_access(self):
        code = textwrap.dedent("""\
        player = 'x'
        choice = 1
        field = '.', '.', '.', '.', '.', '.', '.', '.', '.'
        if field at choice = '.'
            field at choice = player
        else
            print 'illegal move!'""")

        expected = textwrap.dedent("""\
        player = 'x'
        choice = 1
        field = ['.', '.', '.', '.', '.', '.', '.', '.', '.']
        if convert_numerals('Latin', field[int(choice)-1]) == convert_numerals('Latin', '.'):
          field[int(choice)-1] = player
        else:
          print(f'''illegal move!''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    def test_print_calc(self):
        code = textwrap.dedent("""\
            var is 5
            print var + 5""")

        expected = textwrap.dedent(f"""\
            var = 5
            print(f'''{{{self.addition_transpiled('var', 5)}}}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_var_before_assign_gives_error(self):
        code = textwrap.dedent("""\
        print 'the program is ' name
        name is 'Hedy'""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.AccessBeforeAssignException,
            skip_faulty=False,
            max_level=17
        )

    #
    # forward tests
    #
    def test_forward_with_integer_variable(self):
        code = textwrap.dedent("""\
            a is 50
            forward a""")
        expected = HedyTester.dedent(
            "a = 50",
            HedyTester.forward_transpiled('a', self.level))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_forward_with_string_variable_gives_type_error(self):
        code = textwrap.dedent("""\
            a is "ten"
            forward a""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException,
        )

    def test_forward_with_list_access_random(self):
        code = textwrap.dedent("""\
        directions is 10, 100, 360
        forward directions at random""")

        expected = HedyTester.dedent("""\
        directions = [10, 100, 360]""",
                                     HedyTester.list_access_transpiled('random.choice(directions)'),
                                     HedyTester.forward_transpiled('random.choice(directions)', self.level))

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    #
    # turn
    #
    def test_turn_with_number_var(self):
        code = textwrap.dedent("""\
            direction is 70
            turn direction""")
        expected = HedyTester.dedent(
            "direction = 70",
            HedyTester.turn_transpiled('direction', self.level))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_turn_with_non_latin_float_number_var(self):
        code = textwrap.dedent("""\
            الزاوية هو ٩.٠
            استدر الزاوية
            تقدم ١٠.١٠""")

        expected = HedyTester.dedent(
            "الزاوية = 9.0",
            HedyTester.turn_transpiled("الزاوية", self.level),
            HedyTester.forward_transpiled("10.1", self.level)
        )

        self.multi_level_tester(
            code=code,
            lang='ar',
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_turtle_with_expression(self):
        code = textwrap.dedent("""\
            num = 10.6
            turn num + 10.5
            forward 10.5 + num""")

        expected = HedyTester.dedent(
            "num = 10.6",
            HedyTester.turn_transpiled(self.addition_transpiled('num', '10.5'), self.level),
            HedyTester.forward_transpiled(self.addition_transpiled('10.5', 'num'), self.level)
        )

        self.multi_level_tester(code=code, expected=expected)

    def test_turn_with_string_var_gives_type_error(self):
        code = textwrap.dedent("""\
            direction is 'ten'
            turn direction""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException,
        )

    def test_turn_with_non_ascii_var(self):
        code = textwrap.dedent("""\
            ángulo is 90
            turn ángulo""")
        expected = HedyTester.dedent(
            "ángulo = 90",
            HedyTester.turn_transpiled('ángulo', self.level))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            expected_commands=['is', 'turn']
        )

    def test_turn_with_list_access_random(self):
        code = textwrap.dedent("""\
        directions is 10, 100, 360
        turn directions at random""")

        expected = HedyTester.dedent("""\
        directions = [10, 100, 360]""",
                                     HedyTester.list_access_transpiled('random.choice(directions)'),
                                     HedyTester.turn_transpiled('random.choice(directions)', self.level))

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_ask_forward(self):
        code = textwrap.dedent("""\
        afstand is ask 'hoe ver dan?'
        forward afstand""")

        expected = HedyTester.dedent("""\
            afstand = input(f'''hoe ver dan?''')
            try:
              afstand = int(afstand)
            except ValueError:
              try:
                afstand = float(afstand)
              except ValueError:
                pass""",
                                     HedyTester.forward_transpiled('afstand', self.level))

        self.multi_level_tester(
            max_level=17,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    #
    # Test comment
    #
    def test_print_comment(self):
        code = "print 'Hallo welkom bij Hedy!' # This is a comment"
        expected = "print(f'''Hallo welkom bij Hedy!''')"
        output = 'Hallo welkom bij Hedy!'

        self.multi_level_tester(
            max_level=17,
            code=code,
            expected=expected,
            output=output
        )

    def test_assign_comment(self):
        code = 'test = "Welkom bij Hedy" # This is a comment'
        expected = "test = 'Welkom bij Hedy'"
        self.multi_level_tester(
            max_level=18,
            code=code,
            expected=expected,
            unused_allowed=True
        )

    #
    # ask tests
    #
    def test_ask_number_answer(self):
        code = textwrap.dedent("""\
        prijs is ask 'hoeveel?'
        gespaard is 7
        sparen is prijs - gespaard""")
        expected = textwrap.dedent(f"""\
        prijs = input(f'''hoeveel?''')
        try:
          prijs = int(prijs)
        except ValueError:
          try:
            prijs = float(prijs)
          except ValueError:
            pass
        gespaard = 7
        sparen = {self.number_cast_transpiled('prijs')} - {self.number_cast_transpiled('gespaard')}""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_play(self):
        code = textwrap.dedent("""\
            n = 'C4' #
            play n""")

        expected = HedyTester.dedent(
            "n = 'C4'",
            self.play_transpiled('n', quotes=False))

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected,
            max_level=17
        )

    def test_ask_with_list_var(self):
        code = textwrap.dedent("""\
        colors is 'orange', 'blue', 'green'
        favorite is ask 'Is your fav color' colors at 1""")

        expected = self.dedent(
            "colors = ['orange', 'blue', 'green']",
            self.list_access_transpiled('colors[int(1)-1]'),
            f"""\
            favorite = input(f'''Is your fav color{{colors[int(1)-1]}}''')
            try:
              favorite = int(favorite)
            except ValueError:
              try:
                favorite = float(favorite)
              except ValueError:
                pass""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    def test_ask_literal_strings(self):
        code = """var is ask "It's " '"Hedy"!'"""
        expected = textwrap.dedent("""\
        var = input(f'''It\\'s "Hedy"!''')
        try:
          var = int(var)
        except ValueError:
          try:
            var = float(var)
          except ValueError:
            pass""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_with_string_var(self, q):
        code = textwrap.dedent(f"""\
        color is {q}orange{q}
        favorite is ask {q}Is your fav color{q} color""")

        expected = textwrap.dedent("""\
        color = 'orange'
        favorite = input(f'''Is your fav color{color}''')
        try:
          favorite = int(favorite)
        except ValueError:
          try:
            favorite = float(favorite)
          except ValueError:
            pass""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    @parameterized.expand(['10', '10.0'])
    def test_ask_with_number_var(self, number):
        code = textwrap.dedent(f"""\
        number is {number}
        favorite is ask 'Is your fav number' number""")

        expected = textwrap.dedent(f"""\
        number = {number}
        favorite = input(f'''Is your fav number{{number}}''')
        try:
          favorite = int(favorite)
        except ValueError:
          try:
            favorite = float(favorite)
          except ValueError:
            pass""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_list_gives_type_error(self):
        code = textwrap.dedent("""\
        numbers is 1, 2, 3
        favorite is ask 'Is your fav number' numbers""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_ask_single_quoted_text(self):
        code = "details is ask 'tell me more'"
        expected = HedyTester.input_transpiled('details', 'tell me more')

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_double_quoted_text(self):
        code = 'details is ask "tell me more"'
        expected = HedyTester.input_transpiled('details', 'tell me more')

        self.multi_level_tester(code=code, expected=expected, unused_allowed=True, max_level=17)

    def test_ask_single_quoted_text_with_inner_double_quote(self):
        code = """details is ask 'say "no"'"""
        expected = HedyTester.input_transpiled('details', 'say "no"')

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_double_quoted_text_with_inner_single_quote(self):
        code = f'''details is ask "say 'no'"'''
        expected = HedyTester.input_transpiled('details', "say \\'no\\'")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_with_comma(self):
        code = "dieren is ask 'hond, kat, kangoeroe'"
        expected = HedyTester.input_transpiled('dieren', 'hond, kat, kangoeroe')

        self.multi_level_tester(code=code, expected=expected, max_level=17, unused_allowed=True)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_es(self, q):
        code = f"""color is ask {q}Cuál es tu color favorito?{q}"""
        expected = HedyTester.input_transpiled('color', 'Cuál es tu color favorito?')

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_bengali_var(self, q):
        code = f"""রং is ask {q}আপনার প্রিয় রং কি?{q}"""
        expected = HedyTester.input_transpiled('রং', 'আপনার প্রিয় রং কি?')

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_list_random(self):
        code = textwrap.dedent("""\
            numbers is 1, 2, 3
            favorite is ask 'Is your fav number ' numbers at random""")
        expected = HedyTester.dedent(
            "numbers = [1, 2, 3]",
            self.list_access_transpiled('random.choice(numbers)'),
            self.input_transpiled('favorite', 'Is your fav number {random.choice(numbers)}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=15)

    def test_ask_list_access_index(self):
        code = textwrap.dedent("""\
            numbers is 1, 2, 3
            favorite is ask 'Is your fav number ' numbers at 2""")
        expected = HedyTester.dedent(
            "numbers = [1, 2, 3]",
            self.list_access_transpiled('numbers[int(2)-1]'),
            self.input_transpiled('favorite', 'Is your fav number {numbers[int(2)-1]}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=15)

    def test_ask_string_var(self):
        code = textwrap.dedent("""\
            color is "orange"
            favorite is ask 'Is your fav color ' color""")
        expected = HedyTester.dedent(
            "color = 'orange'",
            HedyTester.input_transpiled('favorite', 'Is your fav color {color}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_integer_var(self):
        code = textwrap.dedent("""\
            number is 10
            favorite is ask 'Is your fav number ' number""")
        expected = HedyTester.dedent(
            "number = 10",
            HedyTester.input_transpiled('favorite', 'Is your fav number {number}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_var_before_assign_gives_error(self):
        code = textwrap.dedent("""\
        n is ask 'the program is ' name
        name is 'Hedy'""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.AccessBeforeAssignException,
            skip_faulty=False,
            max_level=17
        )

    #
    # sleep tests
    #
    def test_sleep_with_number_variable(self):
        code = textwrap.dedent("""\
            n is 2
            sleep n""")
        expected = HedyTester.dedent(
            "n = 2",
            HedyTester.sleep_command_transpiled("n"))

        self.multi_level_tester(code=code, expected=expected)

    def test_sleep_with_string_variable_gives_error(self):
        code = textwrap.dedent("""\
            n is "test"
            sleep n""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_sleep_with_list_access(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n at 1""")
        expected = textwrap.dedent(f"""\
        n = [1, 2, 3]
        try:
          n[int(1)-1]
        except IndexError:
          raise Exception({self.index_exception_transpiled()})
        time.sleep({self.int_cast_transpiled('n[int(1)-1]', quotes=False)})""")

        self.multi_level_tester(max_level=15, code=code, expected=expected)

    def test_sleep_with_list_random(self):
        self.maxDiff = None
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n at random""")
        expected = textwrap.dedent(f"""\
        n = [1, 2, 3]
        try:
          random.choice(n)
        except IndexError:
          raise Exception({self.index_exception_transpiled()})
        time.sleep({self.int_cast_transpiled('random.choice(n)', quotes=False)})""")

        self.multi_level_tester(max_level=15, code=code, expected=expected)

    def test_sleep_with_list_gives_error(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_sleep_with_input_variable(self):
        code = textwrap.dedent("""\
            n is ask "how long"
            sleep n""")
        expected = HedyTester.dedent("""\
            n = input(f'''how long''')
            try:
              n = int(n)
            except ValueError:
              try:
                n = float(n)
              except ValueError:
                pass""",
                                     HedyTester.sleep_command_transpiled("n"))

        self.multi_level_tester(max_level=17, code=code, expected=expected)

    def test_sleep_with_calc(self):
        code = textwrap.dedent("""\
            n is 1 * 2 + 3
            sleep n""")

        expected_multiply = f'{self.number_cast_transpiled(1)} * {self.number_cast_transpiled(2)}'
        expected = HedyTester.dedent(
            f"n = {self.addition_transpiled(expected_multiply, '3')}",
            HedyTester.sleep_command_transpiled("n"))

        self.multi_level_tester(code=code, expected=expected)

    #
    # assign tests
    #

    def test_assign_integer(self):
        code = "naam is 14"
        expected = "naam = 14"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected)

    def test_assign_list(self):
        code = "animals is 'duck', 'dog', 'penguin'"
        expected = "animals = ['duck', 'dog', 'penguin']"

        self.multi_level_tester(code=code,
                                expected=expected,
                                unused_allowed=True,
                                max_level=15)

    def test_assign_list_random(self):
        code = textwrap.dedent("""\
        dieren is 'hond', 'kat', 'kangoeroe'
        dier is dieren at random""")

        expected = HedyTester.dedent("dieren = ['hond', 'kat', 'kangoeroe']",
                                     HedyTester.list_access_transpiled('random.choice(dieren)'),
                                     "dier = random.choice(dieren)")

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            max_level=15)

    def test_assign_list_with_dutch_comma_arabic_lang(self):
        code = "صديقي هو 'احمد', 'خالد', 'حسن'"
        expected = "صديقي = ['احمد', 'خالد', 'حسن']"

        self.multi_level_tester(
            code=code,
            expected=expected,
            lang='ar',
            max_level=15,
            unused_allowed=True,
            # translation must be off because the Latin commas will be converted to arabic commas and this is correct
            translate=False
        )

    def test_assign_list_with_arabic_comma_and_is(self):
        code = "animals هو 'cat'، 'dog'، 'platypus'"
        expected = "animals = ['cat', 'dog', 'platypus']"

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            unused_allowed=True,
            lang='ar'
        )

    def test_assign_list_with_arabic_comma(self):
        code = "صديقي هو 'احمد'، 'خالد'، 'حسن'"
        expected = "صديقي = ['احمد', 'خالد', 'حسن']"

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            unused_allowed=True,
            lang='ar'
        )

    def test_assign_string_without_quotes(self):
        code = "name is felienne"

        self.multi_level_tester(
            code=code,
            max_level=17,
            exception=hedy.exceptions.UnquotedAssignTextException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1
        )

    def test_assign_string_without_quotes_line_2(self):
        code = textwrap.dedent("""\
        print 'lalala'
        name is Harry""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            exception=hedy.exceptions.UnquotedAssignTextException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2
        )

    @parameterized.expand(HedyTester.quotes)
    def test_assign_string(self, q):
        code = f"name is {q}felienne{q}"
        expected = "name = 'felienne'"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.quotes)
    def test_assign_empty_string(self, q):
        code = f"name = {q}{q}"
        expected = "name = ''"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected)

    def test_assign_text_with_inner_double_quote(self):
        code = """a is 'It says "Hedy"'"""
        expected = """a = 'It says "Hedy"'"""

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected)

    def test_assign_text_with_inner_single_quote(self):
        code = '''a is "It's Hedy!"'''
        expected = '''a = "It's Hedy!"'''

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected)

    def test_assign_text_to_hungarian_var(self):
        code = "állatok is 'kutya'"
        expected = "állatok = 'kutya'"

        self.multi_level_tester(code=code, expected=expected, unused_allowed=True)

    def test_assign_bengali_var(self):
        var = hedy.escape_var("নাম")
        code = "নাম is 'হেডি'"
        expected = f"{var} = 'হেডি'"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected)

    def test_assign_python_keyword(self):
        code = "for is 'Hedy'"
        expected = "_for = 'Hedy'"

        self.multi_level_tester(code=code, expected=expected, unused_allowed=True)

    def test_assign_concat(self):
        code = """a = "It's" + ' "Hedy"!'"""
        left = '''"It's"'''
        right = """' "Hedy"!'"""
        expected = f"""a = {self.addition_transpiled(left, right)}"""

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected)

    #
    # add/remove tests
    #
    def test_add_ask_to_list(self):
        code = textwrap.dedent("""\
            color is ask 'what is your favorite color?'
            colors is 'green', 'red', 'blue'
            add color to colors""")

        expected = HedyTester.dedent(
            HedyTester.input_transpiled('color', 'what is your favorite color?'),
            "colors = ['green', 'red', 'blue']",
            "colors.append(color)")

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    def test_remove_ask_from_list(self):
        code = textwrap.dedent("""\
            colors is 'green', 'red', 'blue'
            color is ask 'what color to remove?'
            remove color from colors""")

        expected = HedyTester.dedent(
            "colors = ['green', 'red', 'blue']",
            HedyTester.input_transpiled('color', 'what color to remove?'),
            HedyTester.remove_transpiled('colors', 'color'))

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    def test_add_to_list_with_string_var_gives_error(self):
        code = textwrap.dedent("""\
        color is 'yellow'
        colors is 'green', 'red', 'blue'
        add colors to color""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_add_to_list_with_input_var_gives_error(self):
        code = textwrap.dedent("""\
        colors is ask 'What are the colors?'
        favorite is 'red'
        add favorite to colors""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_remove_from_list_with_string_var_gives_error(self):
        code = textwrap.dedent("""\
        color is 'yellow'
        colors is 'green', 'red', 'blue'
        remove colors from color""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_remove_from_list_with_input_var_gives_error(self):
        code = textwrap.dedent("""\
        colors is ask 'What are the colors?'
        favorite is 'red'
        remove favorite from colors""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_list_creation_with_numbers(self):
        code = textwrap.dedent("""\
        getallen is 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
        getal is getallen at random""")
        expected = HedyTester.dedent("""\
        getallen = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]""",
                                     HedyTester.list_access_transpiled('random.choice(getallen)'),
                                     "getal = random.choice(getallen)")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=15)

    #
    # for loop tests
    #
    def test_for_loop_arabic(self):
        code = textwrap.dedent("""\
        for دورة in range ١ to ٥
            print دورة""")

        expected = textwrap.dedent("""\
        step = 1 if 1 < 5 else -1
        for دورة in range(1, 5 + step, step):
          print(f'''{دورة}''')
          time.sleep(0.1)""")

        self.multi_level_tester(
            max_level=16,
            code=code,
            expected=expected,
            expected_commands=['for', 'print'])

    def test_assign_list_with_spaces(self):
        code = "voorspellingen = 'je wordt rijk' , 'je wordt verliefd' , 'je glijdt uit over een bananenschil'"
        expected = "voorspellingen = ['je wordt rijk', 'je wordt verliefd', 'je glijdt uit over een bananenschil']"

        self.multi_level_tester(code=code, expected=expected, max_level=15, unused_allowed=True)

    #
    # if tests
    #
    @parameterized.expand(HedyTester.equality_comparison_with_is)
    def test_if_equality_print(self, eq):
        code = textwrap.dedent(f"""\
        naam = 'Hedy'
        if naam {eq} 'Hedy'
            print 'koekoek'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'''koekoek''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=['is', 'if', 'print'],
            max_level=16)

    def test_if_equality_no_spaces_print(self):
        code = textwrap.dedent(f"""\
        naam = 'Hedy'
        if naam='Hedy'
            print 'koekoek'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'''koekoek''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=['is', 'if', 'print'],
            max_level=16)  # space between = is not preserved (but is needed for the test)

    def test_if_equality_rhs_with_space(self):
        code = textwrap.dedent("""\
           naam is 'James'
           if naam is 'James Bond'
               print 'shaken'""")

        expected = textwrap.dedent("""\
           naam = 'James'
           if convert_numerals('Latin', naam) == convert_numerals('Latin', 'James Bond'):
             print(f'''shaken''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_equality_single_quoted_rhs_with_inner_double_quote(self):
        code = textwrap.dedent(f"""\
        answer is 'no'
        if answer is 'He said "no"'
          print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if convert_numerals('Latin', answer) == convert_numerals('Latin', 'He said "no"'):
          print(f'''no''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_equality_double_quoted_rhs_with_inner_single_quote(self):
        code = textwrap.dedent(f"""\
        answer is 'no'
        if answer is "He said 'no'"
          print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if convert_numerals('Latin', answer) == convert_numerals('Latin', 'He said \\'no\\''):
          print(f'''no''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_equality_negative_number(self):
        code = textwrap.dedent("""\
        antwoord = -10
        if antwoord is -10
            print 'Nice'""")

        expected = textwrap.dedent("""\
        antwoord = -10
        if convert_numerals('Latin', antwoord) == convert_numerals('Latin', '-10'):
          print(f'''Nice''')""")

        self.multi_level_tester(code=code, expected=expected, output='Nice', max_level=16)

    def test_if_2_vars_equality_print(self):
        code = textwrap.dedent("""\
        jouwkeuze is 'schaar'
        computerkeuze is 'schaar'
        if computerkeuze is jouwkeuze
            print 'gelijkspel!'""")

        expected = textwrap.dedent("""\
        jouwkeuze = 'schaar'
        computerkeuze = 'schaar'
        if convert_numerals('Latin', computerkeuze) == convert_numerals('Latin', jouwkeuze):
          print(f'''gelijkspel!''')""")

        self.multi_level_tester(max_level=16, code=code, expected=expected, output='gelijkspel!')

    # def test_if_equality_trailing_space_linebreak_print(self):
    #     code = textwrap.dedent("""\
    #     naam is 'James'
    #     if naam is 'trailing_space'
    #         print 'shaken'""")
    #
    #     expected = textwrap.dedent("""\
    #     naam = 'James'
    #     if convert_numerals('Latin', naam) == convert_numerals('Latin', 'trailing_space'):
    #       print(f'''shaken''')""")
    #
    #     self.multi_level_tester(max_level=18, code=code, expected=expected)

    # Lists can be compared for equality starting with level 14
    def test_if_equality_lists(self):
        code = textwrap.dedent("""\
         m is 1, 2
         n is 1, 2
         if m is n
             print 'success!'""")
        self.multi_level_tester(
            max_level=13,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_if_equality_with_list_gives_error(self):
        code = textwrap.dedent("""\
        color is 5, 6, 7
        if 1 is color
            print 'success!'""")
        self.multi_level_tester(
            max_level=13,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_if_equality_with_incompatible_types_gives_error(self):
        code = textwrap.dedent("""\
        a is 'test'
        b is 15
        if a is b
          c is 1""")
        self.multi_level_tester(
            max_level=16,
            code=code,
            exception=hedy.exceptions.InvalidTypeCombinationException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3
        )

    #
    # in/not-in list commands
    #
    @parameterized.expand([
        ('in', 'Found'),
        ('not in', 'Not found')
    ])
    def test_if_in_not_in_list_with_strings(self, command, expected_output):
        code = textwrap.dedent(f"""\
         letters is 'a', 'b', 'c'
         if 'a' {command} letters
           print 'Found'
         else
           print 'Not found'""")

        expected = textwrap.dedent(f"""\
         letters = ['a', 'b', 'c']
         if 'a' {command} letters:
           print(f'''Found''')
         else:
           print(f'''Not found''')""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            output=expected_output
        )

    @parameterized.expand([
        ('in', 'True'),
        ('not in', 'False')
    ])
    def test_if_number_in_not_in_list_with_numbers(self, operator, expected_output):
        code = textwrap.dedent(f"""\
        items is 1, 2, 3
        if 1 {operator} items
          print 'True'
        else
          print 'False'""")

        expected = textwrap.dedent(f"""\
        items = [1, 2, 3]
        if 1 {operator} items:
          print(f'''True''')
        else:
          print(f'''False''')""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            output=expected_output
        )

    @parameterized.expand([
        ('in', 'False'),
        ('not in', 'True')
    ])
    def test_if_text_in_not_in_list_with_numbers(self, operator, expected_output):
        code = textwrap.dedent(f"""\
            items is 1, 2, 3
            if '1' {operator} items
              print 'True'
            else
              print 'False'""")

        expected = textwrap.dedent(f"""\
            items = [1, 2, 3]
            if '1' {operator} items:
              print(f'''True''')
            else:
              print(f'''False''')""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            output=expected_output
        )

    @parameterized.expand(['in', 'not in'])
    def test_unquoted_lhs_in_not_in_list_gives_error(self, operator):
        code = textwrap.dedent(f"""\
            items is 1, 2, 3
            if a {operator} items
              print 'True'""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            skip_faulty=False,
            exception=hedy.exceptions.UnquotedAssignTextException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2
        )

    @parameterized.expand(['in', 'not in'])
    def test_undefined_rhs_in_not_in_list_gives_error(self, operator):
        code = textwrap.dedent(f"""\
            items is 1, 2, 3
            if 1 {operator} list
              print 'True'""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            exception=hedy.exceptions.UndefinedVarException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2
        )

    @parameterized.expand([(c, q) for c in HedyTester.in_not_in_list_commands for q in HedyTester.quotes])
    def test_if_in_not_in_list_with_string_var_gives_type_error(self, c, q):
        code = textwrap.dedent(f"""\
        items is {q}red{q}
        if {q}red{q} {c} items
            print {q}found!{q}""")
        self.multi_level_tester(
            max_level=16,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand(HedyTester.in_not_in_list_commands)
    def test_if_not_in_and_in_list_with_input_gives_type_error(self, operator):
        code = textwrap.dedent(f"""\
            items is ask 'What are the items?'
            if 'red' {operator} items
              print 'found!'""")
        self.multi_level_tester(
            max_level=16,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    #
    # if else tests
    #
    def test_if_equality_print_else_print(self):
        code = textwrap.dedent("""\
        naam is 'Hedy'
        if naam is 'Hedy'
            print 'leuk'
        else
            print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'''leuk''')
        else:
          print(f'''minder leuk''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_equality_assign_else_assign(self):
        code = textwrap.dedent("""\
         a is 5
         if a is 1
             x is 2
         else
             x is 222""")
        expected = textwrap.dedent("""\
         a = 5
         if convert_numerals('Latin', a) == convert_numerals('Latin', '1'):
           x = 2
         else:
           x = 222""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=16)

    def test_if_else_followed_by_print(self):
        code = textwrap.dedent("""\
        kleur is 'geel'
        if kleur is 'groen'
            antwoord is 'ok'
        else
            antwoord is 'stom'
        print antwoord""")

        expected = textwrap.dedent("""\
        kleur = 'geel'
        if convert_numerals('Latin', kleur) == convert_numerals('Latin', 'groen'):
          antwoord = 'ok'
        else:
          antwoord = 'stom'
        print(f'''{antwoord}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_else_trailing_space_after_else(self):
        code = textwrap.dedent("""\
        a is 1
        if a is 1
            print a
        else
            print 'nee'""")

        expected = textwrap.dedent("""\
        a = 1
        if convert_numerals('Latin', a) == convert_numerals('Latin', '1'):
          print(f'''{a}''')
        else:
          print(f'''nee''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_empty_line_with_whitespace_else_print(self):
        code = textwrap.dedent("""\
        if 1 is 2
            sleep

        else
            sleep""")

        expected = textwrap.dedent("""\
        if convert_numerals('Latin', '1') == convert_numerals('Latin', '2'):
          time.sleep(1)
        else:
          time.sleep(1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_else_with_multiple_lines(self):
        code = textwrap.dedent("""\
            antwoord is ask 'Hoeveel is 10 plus 10?'
            if antwoord is 20
                print 'Goedzo!'
                print 'Het antwoord was inderdaad ' antwoord
            else
                print 'Foutje'
                print 'Het antwoord moest zijn ' antwoord""")

        expected = HedyTester.dedent(
            HedyTester.input_transpiled('antwoord', 'Hoeveel is 10 plus 10?'), """\
            if convert_numerals('Latin', antwoord) == convert_numerals('Latin', '20'):
              print(f'''Goedzo!''')
              print(f'''Het antwoord was inderdaad {antwoord}''')
            else:
              print(f'''Foutje''')
              print(f'''Het antwoord moest zijn {antwoord}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    #
    # repeat tests
    #
    def test_repeat_print(self):
        code = textwrap.dedent("""\
        repeat 5 times
            print 'koekoek'""")

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_cast_transpiled(5)}):
          print(f'''koekoek''')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_repeat_print_variable(self):
        code = textwrap.dedent("""\
        n is 5
        repeat n times
            print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
            n = 5
            for __i in range({self.int_cast_transpiled('n', quotes=False)}):
              print(f'''me wants a cookie!''')
              time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=17)

    # issue 297
    def test_repeat_print_assign_addition(self):
        code = textwrap.dedent("""\
        count is 1
        repeat 12 times
            print count ' times 12 is ' count * 12
            count is count + 1""")

        expected = textwrap.dedent(f"""\
        count = 1
        for __i in range({self.int_cast_transpiled(12)}):
          print(f'''{{count}} times 12 is {{{self.number_cast_transpiled('count')} * {self.number_cast_transpiled(12)}}}''')
          count = {self.addition_transpiled('count', 1)}
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_repeat_with_comment(self):
        code = textwrap.dedent("""\
        repeat 5 times #This should be ignored
            sleep""")

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_cast_transpiled(5)}):
          time.sleep(1)
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(['5', '𑁫', '५', '૫', '੫', '৫', '೫', '୫', '൫', '௫',
                           '౫', '၅', '༥', '᠕', '៥', '๕', '໕', '꧕', '٥', '۵'])
    def test_repeat_with_all_numerals(self, number):
        code = textwrap.dedent(f"""\
        repeat {number} times
            print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_cast_transpiled(int(number))}):
          print(f'''me wants a cookie!''')
          time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=17)

    def test_repeat_nested_in_repeat(self):
        code = textwrap.dedent("""\
        repeat 2 times
            repeat 3 times
                print 'hello'""")

        expected = textwrap.dedent(f"""\
           for __i in range({self.int_cast_transpiled(2)}):
             for __i in range({self.int_cast_transpiled(3)}):
               print(f'''hello''')
               time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_repeat_nested_multi_commands(self):
        code = textwrap.dedent("""\
            repeat 3 times
                print 3
                repeat 5 times
                    print 5
                print 1""")

        expected = textwrap.dedent(f"""\
            for __i in range({self.int_cast_transpiled(3)}):
              print(f'''3''')
              for __i in range({self.int_cast_transpiled(5)}):
                print(f'''5''')
                time.sleep(0.1)
              print(f'''1''')
              time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=17,
            skip_faulty=False
        )

    #
    # for list command
    #
    def test_for_list(self):
        code = textwrap.dedent("""\
         dieren is 'hond', 'kat', 'papegaai'
         for dier in dieren
             print dier""")

        expected = textwrap.dedent("""\
         dieren = ['hond', 'kat', 'papegaai']
         for dier in dieren:
           print(f'''{dier}''')
           time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=['is', 'for', 'print'],
            max_level=15
        )

    def test_for_list_multiline_body(self):
        code = textwrap.dedent("""\
        familie is 'baby', 'mommy', 'daddy', 'grandpa', 'grandma'
        for shark in familie
            print shark ' shark tudutudutudu'
            print shark ' shark tudutudutudu'
            print shark ' shark tudutudutudu'
            print shark ' shark'""")

        expected = textwrap.dedent("""\
        familie = ['baby', 'mommy', 'daddy', 'grandpa', 'grandma']
        for shark in familie:
          print(f'''{shark} shark tudutudutudu''')
          print(f'''{shark} shark tudutudutudu''')
          print(f'''{shark} shark tudutudutudu''')
          print(f'''{shark} shark''')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    #
    # for loop
    #
    def test_for_loop(self):
        code = textwrap.dedent("""\
         for i in range 1 to 10
             a is i + 1
             print a""")
        expected = textwrap.dedent(f"""\
         step = 1 if 1 < 10 else -1
         for i in range(1, 10 + step, step):
           a = {self.addition_transpiled('i', '1')}
           print(f'''{{a}}''')
           time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=16,
            expected_commands=['for', 'is', 'addition', 'print'])

    def test_for_loop_with_int_vars(self):
        code = textwrap.dedent("""\
        begin = 1
        end = 10
        for i in range begin to end
            print i""")

        expected = textwrap.dedent("""\
        begin = 1
        end = 10
        step = 1 if begin < end else -1
        for i in range(begin, end + step, step):
          print(f'''{i}''')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_for_loop_multiline_body(self):
        code = textwrap.dedent("""\
        a is 2
        b is 3
        for a in range 2 to 4
            a is a + 2
            b is b + 2""")

        expected = textwrap.dedent(f"""\
        a = 2
        b = 3
        step = 1 if 2 < 4 else -1
        for a in range(2, 4 + step, step):
          a = {self.addition_transpiled('a', '2')}
          b = {self.addition_transpiled('b', '2')}
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_for_loop_followed_by_print(self):
        code = textwrap.dedent("""\
        for i in range 1 to 10
            print i
        print 'wie niet weg is is gezien'""")

        expected = textwrap.dedent("""\
        step = 1 if 1 < 10 else -1
        for i in range(1, 10 + step, step):
          print(f'''{i}''')
          time.sleep(0.1)
        print(f'''wie niet weg is is gezien''')""")

        output = textwrap.dedent("""\
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        wie niet weg is is gezien""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=16,
            expected_commands=['for', 'print', 'print'],
            output=output)

    # issue 363
    def test_for_loop_if_followed_by_print(self):
        code = textwrap.dedent("""\
        for i in range 0 to 10
            antwoord is ask 'Wat is 5*5'
            if antwoord is 24
                print 'fout'
        print 'klaar met for loop'""")

        expected = HedyTester.dedent("""\
        step = 1 if 0 < 10 else -1
        for i in range(0, 10 + step, step):""",
                                     (HedyTester.input_transpiled('antwoord', 'Wat is 5*5'), '  '), """\
          if convert_numerals('Latin', antwoord) == convert_numerals('Latin', '24'):
            print(f'''fout''')
          time.sleep(0.1)
        print(f'''klaar met for loop''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    # issue 599
    def test_for_loop_if(self):
        code = textwrap.dedent("""\
        for i in range 0 to 10
            if i is 2
                print '2'""")

        expected = textwrap.dedent("""\
        step = 1 if 0 < 10 else -1
        for i in range(0, 10 + step, step):
          if convert_numerals('Latin', i) == convert_numerals('Latin', '2'):
            print(f'''2''')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    #
    # arithmetic expressions tests
    #
    @parameterized.expand([
        ('*', '*', '12'),
        ('/', '/', '3.0'),
        ('-', '-', '4')])
    def test_int_calc(self, op, transpiled_op, output):
        code = f"print 6 {op} 2"
        expected = textwrap.dedent(f"""\
            print(f'''{{{self.number_cast_transpiled(6)} {transpiled_op} {self.number_cast_transpiled(2)}}}''')""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output=output, max_level=17)

    def test_int_sum(self):
        code = f"print 6 + 2"
        expected = f"print(f'''{{6 + 2}}''')"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output='8', max_level=17)

    @parameterized.expand([
        ('*', '*', '100'),
        ('/', '/', '1.0'),
        ('-', '-', '3')])
    def test_nested_int_calc(self, op, transpiled_op, output):
        code = f"print 10 {op} 5 {op} 2"
        ten = self.number_cast_transpiled(10)
        five = self.number_cast_transpiled(5)
        two = self.number_cast_transpiled(2)
        expected = f"print(f'''{{{ten} {transpiled_op} {five} {transpiled_op} {two}}}''')"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output=output, max_level=17)

    @parameterized.expand(['-', '*', '/'])
    def test_float_calc(self, op):
        code = f"print 2.5 {op} 2.5"
        expected = f"print(f'''{{{self.number_cast_transpiled('2.5')} {op} {self.number_cast_transpiled('2.5')}}}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_float_sum(self):
        code = f"print 2.5 + 2.5"
        expected = "print(f'''{2.5 + 2.5}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(['-', '*', '/'])
    def test_float_calc_arabic(self, op):
        code = f"print ١.٥ {op} ١.٥"
        expected = f"print(f'''{{{self.number_cast_transpiled('1.5')} {op} {self.number_cast_transpiled('1.5')}}}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_float_sum_arabic(self):
        code = f"print ١.٥ + ١.٥"
        expected = "print(f'''{1.5 + 1.5}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(['-', '*', '/'])
    def test_print_float_calc_with_string(self, op):
        code = f"print 'het antwoord is ' 2.5 {op} 2.5"
        twona_half = self.number_cast_transpiled('2.5')
        expected = f"print(f'''het antwoord is {{{twona_half} {op} {twona_half}}}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_float_sum_with_string(self):
        code = f"print 'het antwoord is ' 2.5 + 2.5"
        expected = "print(f'''het antwoord is {2.5 + 2.5}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_add_negative_number(self):
        code = textwrap.dedent("""\
        n = -4 +3
        print n""")
        expected = textwrap.dedent("""\
        n = -4 + 3
        print(f'''{n}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(['-', '*', '/'])
    def test_float_calc_with_var(self, op):
        code = textwrap.dedent(f"""\
        getal1 is 5
        getal2 is 4.3
        print 'dat is dan: ' getal1 {op} getal2""")
        expected = textwrap.dedent(f"""\
        getal1 = 5
        getal2 = 4.3
        print(f'''dat is dan: {{{self.number_cast_transpiled('getal1')} {op} {self.number_cast_transpiled('getal2')}}}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_float_sum_with_var(self):
        code = textwrap.dedent("""\
            getal1 is 5
            getal2 is 4.3
            print 'dat is dan: ' getal1 + getal2""")
        expected = textwrap.dedent(f"""\
            getal1 = 5
            getal2 = 4.3
            print(f'''dat is dan: {{{self.addition_transpiled('getal1', 'getal2')}}}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(['-', '*', '/'])
    def test_int_calc_with_var(self, op):
        code = textwrap.dedent(f"""\
        a is 1
        b is 2
        c is a {op} b""")
        expected = textwrap.dedent(f"""\
        a = 1
        b = 2
        c = {self.number_cast_transpiled('a')} {op} {self.number_cast_transpiled('b')}""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_int_sum_with_var(self):
        code = textwrap.dedent(f"""\
        a is 1
        b is 2
        c is a + b""")
        expected = textwrap.dedent(f"""\
        a = 1
        b = 2
        c = {self.addition_transpiled('a', 'b')}""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_concat_calc_with_var(self):
        code = textwrap.dedent("""\
        getal1 is '5'
        getal2 is '6'
        getal3 is '7'
        print 'dat is dan: ' getal1 + getal2 + getal3""")
        expected = textwrap.dedent(f"""\
        getal1 = '5'
        getal2 = '6'
        getal3 = '7'
        print(f'''dat is dan: {{{self.addition_transpiled(self.addition_transpiled('getal1', 'getal2'), 'getal3')}}}''')""")

        check_output = (lambda x: HedyTester.run_code(x) == 'dat is dan: 567')

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=check_output
        )

    def test_int_calc_chained_vars(self):
        code = textwrap.dedent("""\
        a is 5
        b is a + 1
        print a + b""")

        expected = textwrap.dedent(f"""\
        a = 5
        b = {self.addition_transpiled('a', 1)}
        print(f'''{{{self.addition_transpiled('a', 'b')}}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=lambda x: self.run_code(x) == "11"
        )

    def test_calc_string_and_int_gives_type_error(self):
        code = textwrap.dedent("""\
        x is 'test1'
        y is x + 1""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidTypeCombinationException)

    def test_concat_quoted_string_and_int_gives_type_error(self):
        code = """y is 'test1' + 1"""

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1,
            exception=hedy.exceptions.InvalidTypeCombinationException)

    @parameterized.expand(['-', '*', '/'])
    def test_calc_with_single_quoted_strings_gives_type_error(self, operation):
        code = textwrap.dedent(f"""\
        a is 1 {operation} 'Test'""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    @parameterized.expand(['-', '*', '/'])
    def test_calc_with_double_quoted_strings_gives_type_error(self, operation):
        code = textwrap.dedent(f"""\
        a is 1 {operation} "Test\"""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_concat_promotes_ask_input_to_string(self):
        code = textwrap.dedent("""\
            answer is ask 'Yes or No?'
            print 'The answer is ' + answer""")

        expected = textwrap.dedent(f"""\
            answer = input(f'''Yes or No?''')
            try:
              answer = int(answer)
            except ValueError:
              try:
                answer = float(answer)
              except ValueError:
                pass
            print(f'''{{{self.addition_transpiled("'The answer is '", 'answer')}}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    def test_concat_promotes_ask_input_to_int(self):
        code = textwrap.dedent("""\
            answer is ask '1 or 2?'
            print 5 + answer""")

        expected = textwrap.dedent(f"""\
            answer = input(f'''1 or 2?''')
            try:
              answer = int(answer)
            except ValueError:
              try:
                answer = float(answer)
              except ValueError:
                pass
            print(f'''{{{self.addition_transpiled('5', 'answer')}}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    def test_concat_promotes_ask_input_to_float(self):
        code = textwrap.dedent("""\
            answer is ask '1 or 2?'
            print 0.5 + answer""")

        expected = textwrap.dedent(f"""\
            answer = input(f'''1 or 2?''')
            try:
              answer = int(answer)
            except ValueError:
              try:
                answer = float(answer)
              except ValueError:
                pass
            print(f'''{{{self.addition_transpiled('0.5', 'answer')}}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    # def test_access_variable_before_definition(self):
    #   code = textwrap.dedent("""\
    #           a is b
    #           b is 3
    #           print a""")
    #
    #   expected = textwrap.dedent("""\
    #           a = b
    #           b = 3
    #           print(f'{a}')""")
    #
    #   self.multi_level_tester(
    #     code=code,
    #     max_level=17,
    #     expected=expected,
    #     extra_check_function=self.is_not_turtle(),
    #     test_name=self.name()
    #   )

    #
    # combined tests
    #

    def test_list_with_spaces_nested_for_loop(self):
        code = textwrap.dedent("""\
        actions is 'clap your hands', 'stomp your feet', 'shout Hurray'
        for action in actions
            for i in range 1 to 2
                print 'if youre happy and you know it'
                print action
            print 'if youre happy and you know it and you really want to show it'
            print 'if youre happy and you know it'
            print action""")
        expected = textwrap.dedent("""\
        actions = ['clap your hands', 'stomp your feet', 'shout Hurray']
        for action in actions:
          step = 1 if 1 < 2 else -1
          for i in range(1, 2 + step, step):
            print(f'''if youre happy and you know it''')
            print(f'''{action}''')
            time.sleep(0.1)
          print(f'''if youre happy and you know it and you really want to show it''')
          print(f'''if youre happy and you know it''')
          print(f'''{action}''')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    #
    # if pressed tests
    #

    def test_if_pressed_with_list_and_for(self):
        code = textwrap.dedent("""\
        lijstje is 'kip', 'haan', 'kuiken'
        if x is pressed
            for dier in lijstje
                print 'dier'
        else
            print 'onbekend dier'""")

        expected = HedyTester.dedent("""\
        lijstje = ['kip', 'haan', 'kuiken']
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        def if_pressed_x_():
            for dier in lijstje:
              print(f'''dier''')
              time.sleep(0.1)
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_else_():
            print(f'''onbekend dier''')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=15)

    #
    # button tests
    #
    def test_button(self):
        code = textwrap.dedent("""\
        x = 'knop'
        x is button""")

        expected = HedyTester.dedent(f"""\
        x = 'knop'
        create_button(x)""")

        self.multi_level_tester(code=code, expected=expected, max_level=18)

    def test_if_button_is_pressed_print(self):
        code = textwrap.dedent("""\
        x = 'PRINT'
        x is button
        if PRINT is pressed
            print 'The button got pressed!'
        else
            print 'Other button is pressed!'""")

        expected = HedyTester.dedent("""\
         x = 'PRINT'
         create_button(x)
         if_pressed_mapping = {"else": "if_pressed_default_else"}
         if_pressed_mapping['PRINT'] = 'if_pressed_PRINT_'
         def if_pressed_PRINT_():
             print(f'''The button got pressed!''')
         if_pressed_mapping['else'] = 'if_pressed_else_'
         def if_pressed_else_():
             print(f'''Other button is pressed!''')
         extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_equality_make_button(self):
        code = textwrap.dedent("""\
        x = 'knop1'
        if 'knop1' = x
            x is button""")

        expected = HedyTester.dedent(f"""\
        x = 'knop1'
        if convert_numerals('Latin', 'knop1') == convert_numerals('Latin', x):
          create_button(x)""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_button_is_pressed_print_in_repeat(self):
        code = textwrap.dedent("""\
        x = 'but'
        x is button
        repeat 3 times
            if but is pressed
                print 'wow'
            else
                print 'nah'""")

        expected = HedyTester.dedent(f"""\
         x = 'but'
         create_button(x)
         for __i in range({self.int_cast_transpiled(3)}):
           if_pressed_mapping = {{"else": "if_pressed_default_else"}}
           if_pressed_mapping['but'] = 'if_pressed_but_'
           def if_pressed_but_():
               print(f'''wow''')
           if_pressed_mapping['else'] = 'if_pressed_else_'
           def if_pressed_else_():
               print(f'''nah''')
           extensions.if_pressed(if_pressed_mapping)
           time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_simple_function(self):
        code = textwrap.dedent("""\
        define simple_function_1 with parameter
            print "simple_function_1 - 1"
            m = "simple_function_1 - 2"
            print m
        define simple_function_2 with param
            print "simple_function_2 - 1"
            print param
        define simple_function_3 with param_a, param_b, param_c
            if param_a = "A"
                print "simple_function_3 - 1"
                print param_b
            else
                print "simple_function_3 - 2"
                if param_a = "B"
                    print "simple_function_3 - 2A"
                    print param_b
                else
                    print "simple_function_3 - 2B"
                    print param_c
        a = "test1"
        call simple_function_3 with "A", a, 1.0
        call simple_function_3 with "B", a, 1.0
        call simple_function_3 with "C", a, 1.0""")

        expected = textwrap.dedent("""\
        def simple_function_1(parameter):
          print(f'''simple_function_1 - 1''')
          m = 'simple_function_1 - 2'
          print(f'''{m}''')
        def simple_function_2(param):
          print(f'''simple_function_2 - 1''')
          print(f'''{param}''')
        def simple_function_3(param_a, param_b, param_c):
          if convert_numerals('Latin', param_a) == convert_numerals('Latin', 'A'):
            print(f'''simple_function_3 - 1''')
            print(f'''{param_b}''')
          else:
            print(f'''simple_function_3 - 2''')
            if convert_numerals('Latin', param_a) == convert_numerals('Latin', 'B'):
              print(f'''simple_function_3 - 2A''')
              print(f'''{param_b}''')
            else:
              print(f'''simple_function_3 - 2B''')
              print(f'''{param_c}''')
        a = 'test1'
        simple_function_3('A', a, 1.0)
        simple_function_3('B', a, 1.0)
        simple_function_3('C', a, 1.0)""")

        output = textwrap.dedent("""\
        simple_function_3 - 1
        test1
        simple_function_3 - 2
        simple_function_3 - 2A
        test1
        simple_function_3 - 2
        simple_function_3 - 2B
        1.0""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output=output,
            unused_allowed=True,
            max_level=16
        )

    def test_function_use(self):
        code = textwrap.dedent("""\
        define func with n1, n2
            return n1 + n2

        print call func with 1, 2""")

        expected = self.dedent(
            "def func(n1, n2):",
            (self.return_transpiled(f"{{{self.addition_transpiled('n1', 'n2')}}}"), '  '),
            "print(f'''{func(1, 2)}''')")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            expected=expected
        )

    def test_undefined_function_without_params(self):
        code = textwrap.dedent("""\
        call func""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            exception=hedy.exceptions.UndefinedFunctionException
        )

    def test_undefined_function_with_params(self):
        code = textwrap.dedent("""\
        print call func with 1, 2""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            exception=hedy.exceptions.UndefinedFunctionException
        )

    def test_function_use_builtin_name(self):
        code = textwrap.dedent("""\
        define sum with n1, n2
            return n1 + n2

        print call sum with 1, 2""")

        expected = self.dedent(
            "def sum(n1, n2):",
            (self.return_transpiled(f"{{{self.addition_transpiled('n1', 'n2')}}}"), '  '),
            "print(f'''{sum(1, 2)}''')")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            expected=expected
        )

    def test_function_returns_number(self):
        code = textwrap.dedent("""\
        define func with n1, n2
            return n1 + n2

        a = call func with 1, 2
        print a + 3""")

        expected = self.dedent(
            "def func(n1, n2):",
            (self.return_transpiled(f"{{{self.addition_transpiled('n1', 'n2')}}}"), '  '),
            "a = func(1, 2)",
            f"print(f'''{{{self.addition_transpiled('a', '3')}}}''')")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            expected=expected
        )

    def test_too_many_parameters(self):
        code = textwrap.dedent("""\
        define func with n1, n2
            return n1 + n2

        print call func with 1, 2, 3""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            exception=hedy.exceptions.WrongNumberofArguments
        )

    def test_too_few_parameters(self):
        code = textwrap.dedent("""\
        define func with n1, n2
            return n1 + n2

        print call func with 1""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            exception=hedy.exceptions.WrongNumberofArguments
        )

    def test_unused_function_use_builtin_name(self):
        code = textwrap.dedent("""\
        define sum with n1, n2
            return n1 + n2

        print 'hola!'""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            exception=hedy.exceptions.UnusedVariableException
        )

    def test_addition(self):
        code = textwrap.dedent("""\
        a = 5
        b = 7
        print a + b""")

        expected = textwrap.dedent(f"""\
        a = 5
        b = 7
        print(f'''{{{self.addition_transpiled('a', 'b')}}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            skip_faulty=False,
            expected=expected
        )

    def test_source_map(self):
        code = textwrap.dedent("""\
        price = 0.0
        food = ask 'What would you like to order?'
        drink = ask 'What would you like to drink?'
        if food is 'hamburger'
            price = price + 6.50
        if food is 'pizza'
            price = price + 5.75
        if drink is 'water'
            price = price + 1.20
        if drink is 'soda'
            price = price + 2.35
        print 'That will be ' price ' dollar, please'""")

        expected_code = textwrap.dedent(f"""\
        price = 0.0
        food = input(f'''What would you like to order?''')
        try:
          food = int(food)
        except ValueError:
          try:
            food = float(food)
          except ValueError:
            pass
        drink = input(f'''What would you like to drink?''')
        try:
          drink = int(drink)
        except ValueError:
          try:
            drink = float(drink)
          except ValueError:
            pass
        if convert_numerals('Latin', food) == convert_numerals('Latin', 'hamburger'):
          price = {self.addition_transpiled('price', '6.5')}
        if convert_numerals('Latin', food) == convert_numerals('Latin', 'pizza'):
          price = {self.addition_transpiled('price', '5.75')}
        if convert_numerals('Latin', drink) == convert_numerals('Latin', 'water'):
          price = {self.addition_transpiled('price', '1.2')}
        if convert_numerals('Latin', drink) == convert_numerals('Latin', 'soda'):
          price = {self.addition_transpiled('price', '2.35')}
        print(f'''That will be {{price}} dollar, please''')""")

        expected_source_map = {
            '1/1-1/6': '1/1-1/6',
            '1/1-1/12': '1/1-1/12',
            '2/1-2/5': '2/1-2/5',
            '2/1-2/43': '2/1-9/9',
            '3/1-3/6': '10/1-10/6',
            '3/1-3/44': '10/1-17/9',
            '4/4-4/8': '4/3-4/7',
            '4/4-4/23': '18/4-18/77',
            '5/5-5/10': '21/1-21/6',
            '5/13-5/18': '23/1-23/6',
            '5/5-5/25': '19/1-19/63',
            '4/1-5/34': '18/1-19/65',
            '6/4-6/8': '4/14-4/18',
            '6/4-6/19': '20/4-20/73',
            '7/5-7/10': '25/1-25/6',
            '7/13-7/18': '1/1-1/6',
            '7/5-7/25': '21/1-21/64',
            '6/1-7/34': '20/1-21/66',
            '8/4-8/9': '10/42-10/47',
            '8/4-8/20': '22/4-22/74',
            '9/5-9/10': '19/1-19/6',
            '9/13-9/18': '21/1-21/6',
            '9/5-9/25': '23/1-23/63',
            '8/1-9/34': '22/1-23/65',
            '10/4-10/9': '12/3-12/8',
            '10/4-10/19': '24/4-24/73',
            '11/5-11/10': '23/1-23/6',
            '11/13-11/18': '25/1-25/6',
            '11/5-11/25': '25/1-25/64',
            '10/1-11/34': '24/1-25/66',
            '12/23-12/28': '26/25-26/30',
            '12/1-12/46': '26/1-26/50',
            '1/1-12/47': '1/1-26/50'
        }

        self.single_level_tester(code, expected=expected_code)
        self.source_map_tester(code=code, expected_source_map=expected_source_map)

    def test_nested_functions(self):
        code = textwrap.dedent("""\
        define simple_function
            define nested_function
                print 1
        call simple_function""")

        expected = textwrap.dedent("""\
        pass
        simple_function()""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 3, 34), hedy.exceptions.NestedFunctionException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            skipped_mappings=skipped_mappings,
            max_level=16
        )

    #
    # music tests
    #
    def test_play_random(self):
        code = textwrap.dedent("""\
        notes = 'C4', 'E4', 'D4', 'F4', 'G4'
        play notes at random""")

        expected = HedyTester.dedent(f"\
            notes = ['C4', 'E4', 'D4', 'F4', 'G4']",
                                     self.play_transpiled("random.choice(notes)", quotes=False))

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=15
        )

    def test_play_integers(self):
        code = textwrap.dedent("""\
        notes = 1, 2, 3

        repeat 10 times
            play notes at random""")

        expected = HedyTester.dedent(
            f"""\
            notes = [1, 2, 3]
            for __i in range({self.int_cast_transpiled(10)}):""",
            (self.play_transpiled('random.choice(notes)', quotes=False), '  '),
            ("time.sleep(0.1)", '  '))

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=15
        )

    @parameterized.expand(['-', '*', '/'])
    def test_play_calculation(self, op):
        code = textwrap.dedent(f"""\
            note is 34
            play note {op} 1""")
        expected = HedyTester.dedent(
            "note = 34",
            self.play_transpiled(
                f"{self.number_cast_transpiled('note')} {op} {self.number_cast_transpiled(1)}", quotes=False
            ))

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected
        )

    def test_play_sum(self):
        code = textwrap.dedent(f"""\
            note is 34
            play note + 1""")
        expected = HedyTester.dedent(
            "note = 34",
            self.play_transpiled(self.addition_transpiled('note', 1), quotes=False))

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected,
        )
