import textwrap

from parameterized import parameterized

import hedy
from hedy import Command
from tests.Tester import HedyTester


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
        expected = "print(f'''{3 / 2}''')"
        output = "1.5"

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=17,
            output=output
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
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_print_subtraction_with_text(self):
        code = "print 'And the winner is ' 5 - 5"
        expected = "print(f'''And the winner is {5 - 5}''')"
        output = 'And the winner is 0'

        self.multi_level_tester(max_level=17, code=code, expected=expected, output=output)

    def test_print_list_random(self):
        code = textwrap.dedent("""\
            numbers is 1, 2, 4
            print numbers at random""")

        expected = textwrap.dedent("""\
            numbers = [1, 2, 4]
            print(f'''{random.choice(numbers)}''')""")

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

        expected = textwrap.dedent("""\
        numbers = [5, 4, 3]
        print(f'''{numbers[1-1]}''')""")

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

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.quotes)
    def test_print_concat_quoted_strings(self, q):
        code = f"""print {q}Hi {q} + {q}there{q}"""
        expected = """print(f'''{'Hi ' + 'there'}''')"""

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_concat_double_quoted_strings_with_inner_single_quotes(self):
        code = '''print "Hi there! " + "It's Hedy!"'''
        expected = """print(f'''{'Hi there! ' + "It's Hedy!"}''')"""

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.quotes)
    def test_print_concat_var_and_literal_string(self, q):
        code = textwrap.dedent(f"""\
        hi = {q}Hi{q}
        print hi + {q} there{q}""")
        expected = textwrap.dedent("""\
        hi = 'Hi'
        print(f'''{hi + ' there'}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_chained_assignments(self):
        code = textwrap.dedent("""\
            x is 1 + 2
            y is x + 3
            print y + 4""")

        expected = textwrap.dedent("""\
            x = 1 + 2
            y = x + 3
            print(f'''{y + 4}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_calc(self):
        code = textwrap.dedent("""\
            var is 5
            print var + 5""")

        expected = textwrap.dedent("""\
            var = 5
            print(f'''{var + 5}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

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
            exception=hedy.exceptions.InvalidArgumentTypeException,
        )

    def test_forward_with_list_access_random(self):
        code = textwrap.dedent("""\
        directions is 10, 100, 360
        forward directions at random""")

        expected = HedyTester.dedent("""\
        directions = [10, 100, 360]""",
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
            HedyTester.turn_transpiled('num + 10.5', self.level),
            HedyTester.forward_transpiled('10.5 + num', self.level)
        )

        self.multi_level_tester(code=code, expected=expected)

    def test_turn_with_string_var_gives_type_error(self):
        code = textwrap.dedent("""\
            direction is 'ten'
            turn direction""")

        self.multi_level_tester(
            code=code,
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
            expected=expected
        )

    #
    # ask tests
    #
    def test_ask_number_answer(self):
        code = textwrap.dedent("""\
        prijs is ask 'hoeveel?'
        gespaard is 7
        sparen is prijs - gespaard""")
        expected = textwrap.dedent("""\
        prijs = input(f'''hoeveel?''')
        try:
          prijs = int(prijs)
        except ValueError:
          try:
            prijs = float(prijs)
          except ValueError:
            pass
        gespaard = 7
        sparen = prijs - gespaard""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_ask_with_list_var(self):
        code = textwrap.dedent("""\
        colors is 'orange', 'blue', 'green'
        favorite is ask 'Is your fav color' colors at 1""")

        expected = textwrap.dedent("""\
        colors = ['orange', 'blue', 'green']
        favorite = input(f'''Is your fav color{colors[1-1]}''')
        try:
          favorite = int(favorite)
        except ValueError:
          try:
            favorite = float(favorite)
          except ValueError:
            pass""")

        self.multi_level_tester(code=code, expected=expected, max_level=14)

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

        self.multi_level_tester(code=code, expected=expected, max_level=17)

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

        self.multi_level_tester(code=code, expected=expected, max_level=17)

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

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_ask_list_gives_type_error(self):
        code = textwrap.dedent("""\
        numbers is 1, 2, 3
        favorite is ask 'Is your fav number' numbers""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_ask_single_quoted_text(self):
        code = "details is ask 'tell me more'"
        expected = HedyTester.input_transpiled('details', 'tell me more')

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_ask_double_quoted_text(self):
        code = 'details is ask "tell me more"'
        expected = HedyTester.input_transpiled('details', 'tell me more')

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_ask_single_quoted_text_with_inner_double_quote(self):
        code = """details is ask 'say "no"'"""
        expected = HedyTester.input_transpiled('details', 'say "no"')

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_ask_double_quoted_text_with_inner_single_quote(self):
        code = f'''details is ask "say 'no'"'''
        expected = HedyTester.input_transpiled('details', "say \\'no\\'")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_ask_with_comma(self):
        code = "dieren is ask 'hond, kat, kangoeroe'"
        expected = HedyTester.input_transpiled('dieren', 'hond, kat, kangoeroe')

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_es(self, q):
        code = f"""color is ask {q}Cuál es tu color favorito?{q}"""
        expected = HedyTester.input_transpiled('color', 'Cuál es tu color favorito?')

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_bengali_var(self, q):
        code = f"""রং is ask {q}আপনার প্রিয় রং কি?{q}"""
        expected = HedyTester.input_transpiled('রং', 'আপনার প্রিয় রং কি?')

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_ask_list_random(self):
        code = textwrap.dedent("""\
            numbers is 1, 2, 3
            favorite is ask 'Is your fav number ' numbers at random""")
        expected = HedyTester.dedent(
            "numbers = [1, 2, 3]",
            HedyTester.input_transpiled('favorite', 'Is your fav number {random.choice(numbers)}'))

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    def test_ask_list_access_index(self):
        code = textwrap.dedent("""\
            numbers is 1, 2, 3
            favorite is ask 'Is your fav number ' numbers at 2""")
        expected = HedyTester.dedent(
            "numbers = [1, 2, 3]",
            HedyTester.input_transpiled('favorite', 'Is your fav number {numbers[2-1]}'))

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    def test_ask_string_var(self):
        code = textwrap.dedent("""\
            color is "orange"
            favorite is ask 'Is your fav color ' color""")
        expected = HedyTester.dedent(
            "color = 'orange'",
            HedyTester.input_transpiled('favorite', 'Is your fav color {color}'))

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_ask_integer_var(self):
        code = textwrap.dedent("""\
            number is 10
            favorite is ask 'Is your fav number ' number""")
        expected = HedyTester.dedent(
            "number = 10",
            HedyTester.input_transpiled('favorite', 'Is your fav number {number}'))

        self.multi_level_tester(code=code, expected=expected, max_level=17)

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

        self.multi_level_tester(code=code, exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_sleep_with_list_access(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n at 1""")
        expected = HedyTester.dedent(
            "n = [1, 2, 3]",
            HedyTester.sleep_command_transpiled("n[1-1]"))

        self.multi_level_tester(max_level=15, code=code, expected=expected)

    def test_sleep_with_list_random(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n at random""")
        expected = HedyTester.dedent(
            "n = [1, 2, 3]",
            HedyTester.sleep_command_transpiled("random.choice(n)"))

        self.multi_level_tester(max_level=15, code=code, expected=expected)

    def test_sleep_with_list_gives_error(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n""")

        self.multi_level_tester(max_level=15, code=code, exception=hedy.exceptions.InvalidArgumentTypeException)

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
        expected = HedyTester.dedent(
            "n = 1 * 2 + 3",
            HedyTester.sleep_command_transpiled("n"))

        self.multi_level_tester(code=code, expected=expected)

    def test_sleep_with_float_gives_error(self):
        code = textwrap.dedent("""\
            n is 1.5
            sleep n""")

        self.multi_level_tester(code=code, exception=hedy.exceptions.InvalidArgumentTypeException)

    #
    # assign tests
    #
    def test_assign_integer(self):
        code = "naam is 14"
        expected = "naam = 14"

        self.multi_level_tester(code=code, expected=expected)

    def test_assign_list(self):
        code = "animals is 'duck', 'dog', 'penguin'"
        expected = "animals = ['duck', 'dog', 'penguin']"

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    def test_assign_list_random(self):
        code = textwrap.dedent("""\
        dieren is 'hond', 'kat', 'kangoeroe'
        dier is dieren at random""")

        expected = textwrap.dedent("""\
        dieren = ['hond', 'kat', 'kangoeroe']
        dier = random.choice(dieren)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=15)

    def test_assign_list_with_dutch_comma_arabic_lang(self):
        code = "صديقي هو 'احمد', 'خالد', 'حسن'"
        expected = "صديقي = ['احمد', 'خالد', 'حسن']"

        self.multi_level_tester(
            code=code,
            expected=expected,
            lang='ar',
            max_level=15,
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
            lang='ar'
        )

    def test_assign_list_with_arabic_comma(self):
        code = "صديقي هو 'احمد'، 'خالد'، 'حسن'"
        expected = "صديقي = ['احمد', 'خالد', 'حسن']"

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            lang='ar'
        )

    def test_assign_string_without_quotes(self):
        code = "name is felienne"

        self.multi_level_tester(
            code=code,
            max_level=17,
            exception=hedy.exceptions.UnquotedAssignTextException
        )

    @parameterized.expand(HedyTester.quotes)
    def test_assign_string(self, q):
        code = f"name is {q}felienne{q}"
        expected = "name = 'felienne'"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_assign_text_with_inner_double_quote(self):
        code = """a is 'It says "Hedy"'"""
        expected = """a = 'It says "Hedy"'"""

        self.multi_level_tester(code=code, expected=expected)

    def test_assign_text_with_inner_single_quote(self):
        code = '''a is "It's Hedy!"'''
        expected = '''a = "It's Hedy!"'''

        self.multi_level_tester(code=code, expected=expected)

    def test_assign_text_to_hungarian_var(self):
        code = "állatok is 'kutya'"
        expected = "állatok = 'kutya'"

        self.multi_level_tester(code=code, expected=expected)

    def test_assign_bengali_var(self):
        var = hedy.escape_var("নাম")
        code = "নাম is 'হেডি'"
        expected = f"{var} = 'হেডি'"

        self.multi_level_tester(code=code, expected=expected)

    def test_assign_python_keyword(self):
        code = "for is 'Hedy'"
        expected = "_for = 'Hedy'"

        self.multi_level_tester(code=code, expected=expected)

    def test_assign_concat(self):
        code = """a = "It's" + ' "Hedy"!'"""
        expected = """a = "It's" + ' "Hedy"!'"""

        self.multi_level_tester(code=code, expected=expected)

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
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_list_creation_with_numbers(self):
        code = textwrap.dedent("""\
        getallen is 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
        getal is getallen at random""")
        expected = textwrap.dedent("""\
        getallen = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        getal = random.choice(getallen)""")

        self.multi_level_tester(code=code, expected=expected, max_level=15)

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

        self.multi_level_tester(code=code, expected=expected, max_level=15)

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

    def test_if_equality_lists(self):
        code = textwrap.dedent("""\
        m is 1, 2
        n is 1, 2
        if m is n
            print 'success!'""")

        self.multi_level_tester(
            max_level=13,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    @parameterized.expand(HedyTester.quotes)
    def test_if_in_list_with_string_var_gives_type_error(self, q):
        code = textwrap.dedent(f"""\
        items is {q}red{q}
        if {q}red{q} in items
            print {q}found!{q}""")
        self.multi_level_tester(
            max_level=16,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_if_equality_with_list_gives_error(self):
        code = textwrap.dedent("""\
        color is 5, 6, 7
        if 1 is color
            print 'success!'""")
        self.multi_level_tester(
            max_level=13,
            code=code,
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
            exception=hedy.exceptions.InvalidTypeCombinationException
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

        self.multi_level_tester(code=code, expected=expected, max_level=16)

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

        expected = textwrap.dedent("""\
        for i in range(int('5')):
          print(f'''koekoek''')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_repeat_print_variable(self):
        code = textwrap.dedent("""\
        n is 5
        repeat n times
            print 'me wants a cookie!'""")

        expected = textwrap.dedent("""\
        n = 5
        for i in range(int(n)):
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

        expected = textwrap.dedent("""\
        count = 1
        for i in range(int('12')):
          print(f'''{count} times 12 is {count * 12}''')
          count = count + 1
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_repeat_with_comment(self):
        code = textwrap.dedent("""\
        repeat 5 times #This should be ignored
            sleep""")

        expected = textwrap.dedent("""\
        for i in range(int('5')):
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
        for i in range(int('{int(number)}')):
          print(f'''me wants a cookie!''')
          time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=17)

    def test_repeat_with_variable_name_collision(self):
        code = textwrap.dedent("""\
        i is 'hallo!'
        repeat 5 times
            print 'me wants a cookie!'
        print i""")

        expected = textwrap.dedent("""\
        i = 'hallo!'
        for _i in range(int('5')):
          print(f'''me wants a cookie!''')
          time.sleep(0.1)
        print(f'''{i}''')""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        hallo!""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=['is', 'repeat', 'print', 'print'],
            output=output,
            max_level=17
        )

    def test_repeat_nested_in_repeat(self):
        code = textwrap.dedent("""\
        repeat 2 times
            repeat 3 times
                print 'hello'""")

        expected = textwrap.dedent("""\
           for i in range(int('2')):
             for i in range(int('3')):
               print(f'''hello''')
               time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

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
             a is i + 1""")
        expected = textwrap.dedent("""\
         step = 1 if 1 < 10 else -1
         for i in range(1, 10 + step, step):
           a = i + 1
           time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=16,
            expected_commands=['for', 'is', 'addition'])

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

        expected = textwrap.dedent("""\
        a = 2
        b = 3
        step = 1 if 2 < 4 else -1
        for a in range(2, 4 + step, step):
          a = a + 2
          b = b + 2
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
        ('+', '+', '8'),
        ('-', '-', '4')])
    def test_int_calc(self, op, transpiled_op, output):
        code = f"print 6 {op} 2"
        expected = f"print(f'''{{6 {transpiled_op} 2}}''')"

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=17)

    @parameterized.expand([
        ('*', '*', '100'),
        ('/', '/', '1.0'),
        ('+', '+', '17'),
        ('-', '-', '3')])
    def test_nested_int_calc(self, op, transpiled_op, output):
        code = f"print 10 {op} 5 {op} 2"
        expected = f"print(f'''{{10 {transpiled_op} 5 {transpiled_op} 2}}''')"

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=17)

    @parameterized.expand(HedyTester.arithmetic_operations)
    def test_float_calc(self, op):
        code = f"print 2.5 {op} 2.5"
        expected = f"print(f'''{{2.5 {op} 2.5}}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.arithmetic_operations)
    def test_float_calc_arabic(self, op):
        code = f"print ١.٥ {op} ١.٥"
        expected = f"print(f'''{{1.5 {op} 1.5}}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.arithmetic_operations)
    def test_print_float_calc_with_string(self, op):
        code = f"print 'het antwoord is ' 2.5 {op} 2.5"
        expected = f"print(f'''het antwoord is {{2.5 {op} 2.5}}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_add_negative_number(self):
        code = textwrap.dedent("""\
        n = -4 +3
        print n""")
        expected = textwrap.dedent("""\
        n = -4 + 3
        print(f'''{n}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.arithmetic_operations)
    def test_float_calc_with_var(self, op):
        code = textwrap.dedent(f"""\
        getal1 is 5
        getal2 is 4.3
        print 'dat is dan: ' getal1 {op} getal2""")
        expected = textwrap.dedent(f"""\
        getal1 = 5
        getal2 = 4.3
        print(f'''dat is dan: {{getal1 {op} getal2}}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.arithmetic_operations)
    def test_int_calc_with_var(self, op):
        code = textwrap.dedent(f"""\
        a is 1
        b is 2
        c is a {op} b""")
        expected = textwrap.dedent(f"""\
        a = 1
        b = 2
        c = a {op} b""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_concat_calc_with_var(self):
        code = textwrap.dedent("""\
        getal1 is '5'
        getal2 is '6'
        getal3 is '7'
        print 'dat is dan: ' getal1 + getal2 + getal3""")
        expected = textwrap.dedent("""\
        getal1 = '5'
        getal2 = '6'
        getal3 = '7'
        print(f'''dat is dan: {getal1 + getal2 + getal3}''')""")

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

        expected = textwrap.dedent("""\
        a = 5
        b = a + 1
        print(f'''{a + b}''')""")

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
            exception=hedy.exceptions.InvalidTypeCombinationException)

    def test_concat_quoted_string_and_int_gives_type_error(self):
        code = """y is 'test1' + 1"""

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidTypeCombinationException)

    @parameterized.expand(['-', '*', '/'])
    def test_calc_with_single_quoted_strings_gives_type_error(self, operation):
        code = textwrap.dedent(f"""\
        a is 1 {operation} 'Test'""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    @parameterized.expand(['-', '*', '/'])
    def test_calc_with_double_quoted_strings_gives_type_error(self, operation):
        code = textwrap.dedent(f"""\
        a is 1 {operation} "Test\"""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException)

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
                print 'dier'""")

        expected = HedyTester.dedent("""\
        lijstje = ['kip', 'haan', 'kuiken']
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              for dier in lijstje:
                print(f'''dier''')
                time.sleep(0.1)
              break""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=15)

    #
    # if pressed else tests
    #

    def test_if_pressed_repeat(self):
        code = textwrap.dedent("""\
        if x is pressed 
            repeat 5 times 
                print 'doe het 5 keer!'""")

        expected = HedyTester.dedent("""\
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              for i in range(int('5')):
                print(f'''doe het 5 keer!''')
                time.sleep(0.1)
              break""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_pressed_x_else(self):
        code = textwrap.dedent("""\
        if x is pressed
            print 'x is pressed!'
        else
            print 'x is not pressed!'""")

        expected = HedyTester.dedent("""\
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              print(f'''x is pressed!''')
              break    
            else:
              print(f'''x is not pressed!''')
              break\n""") + "    "

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_pressed_x_print(self):
        code = textwrap.dedent("""\
        if x is pressed
            print 'it is a letter key'""")
        expected = HedyTester.dedent("""\
          while not pygame_end:
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
              pygame_end = True
              pygame.quit()
              break
            if event.type == pygame.KEYDOWN:
              if event.unicode == 'x':
                print(f'''it is a letter key''')
                break""")
        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_double_if_pressed(self):
        code = textwrap.dedent("""\
        if x is pressed
            print 'first key'
        if y is pressed
            print 'second key'""")

        expected = HedyTester.dedent("""\
          while not pygame_end:
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
              pygame_end = True
              pygame.quit()
              break
            if event.type == pygame.KEYDOWN:
              if event.unicode == 'x':
                print(f'''first key''')
                break
            if event.type == pygame.KEYDOWN:
              if event.unicode == 'y':
                print(f'''second key''')
                break""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_pressed_is_number_key_print(self):
        code = textwrap.dedent("""\
        if 1 is pressed
            print 'it is a number key'""")

        expected = HedyTester.dedent("""\
          while not pygame_end:
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
              pygame_end = True
              pygame.quit()
              break
            if event.type == pygame.KEYDOWN:
              if event.unicode == '1':
                print(f'''it is a number key''')
                break""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    #
    # if pressed turtle tests
    #

    def test_if_pressed_repeat_multiple_x_turtle_move(self):
        code = textwrap.dedent("""\
        repeat 10 times
            if w is pressed
                forward 25
            if a is pressed
                turn -90
            if d is pressed
                turn 90
            if s is pressed
                turn 180""")

        expected = HedyTester.dedent(f"""\
        for i in range(int('10')):
          while not pygame_end:
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
              pygame_end = True
              pygame.quit()
              break
            if event.type == pygame.KEYDOWN:
              if event.unicode == 'w':
                {HedyTester.indent(
                  HedyTester.forward_transpiled(25.0, self.level),
                  16, True)
                }
                break
            if event.type == pygame.KEYDOWN:
              if event.unicode == 'a':
                {HedyTester.indent(
                  HedyTester.turn_transpiled(-90.0, self.level),
                  16, True)
                }
                break
            if event.type == pygame.KEYDOWN:
              if event.unicode == 'd':
                {HedyTester.indent(
                  HedyTester.turn_transpiled(90.0, self.level),
                  16, True)
                }
                break
            if event.type == pygame.KEYDOWN:
              if event.unicode == 's':
                {HedyTester.indent(
                  HedyTester.turn_transpiled(180.0, self.level),
                  16, True)
                }
                break
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, extra_check_function=self.is_turtle(), max_level=16)

    def test_if_pressed_with_turtlecolor(self):
        code = textwrap.dedent("""\
        if x is pressed 
            color red""")

        expected = HedyTester.dedent(f"""\
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              {HedyTester.indent(
                HedyTester.turtle_color_command_transpiled('red'), 
                14, True)
              }
              break""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=16
        )

    def test_if_pressed_else_with_turtle(self):
        code = textwrap.dedent("""\
        if x is pressed
            forward 25
        else
            turn 90""")

        expected = HedyTester.dedent(f"""\
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              {HedyTester.indent(
                HedyTester.forward_transpiled(25.0, self.level),
                14, True)
              }
              break    
            else:
              {HedyTester.indent(
                HedyTester.turn_transpiled(90.0, self.level), 
                14, True)
              }
              break\n""") + "    "

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=16
        )

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
            print 'The button got pressed!'""")

        expected = HedyTester.dedent(f"""\
        x = 'PRINT'
        create_button(x)
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.USEREVENT:
            if event.key == 'PRINT':
              print(f'''The button got pressed!''')
              break""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_button_is_pressed_make_button(self):
        code = textwrap.dedent("""\
        x = 'PRESS'
        x is button
        if PRESS is pressed
            y = 'BUT'
            y is button""")

        expected = HedyTester.dedent(f"""\
        x = 'PRESS'
        create_button(x)
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.USEREVENT:
            if event.key == 'PRESS':
              y = 'BUT'
              create_button(y)
              break""")

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
                print 'wow'""")

        expected = HedyTester.dedent(f"""\
        x = 'but'
        create_button(x)
        for i in range(int('3')):
          while not pygame_end:
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
              pygame_end = True
              pygame.quit()
              break
            if event.type == pygame.USEREVENT:
              if event.key == 'but':
                print(f'''wow''')
                break
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)
