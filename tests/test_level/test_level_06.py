import textwrap
from parameterized import parameterized
import hedy
from tests.Tester import HedyTester


class TestsLevel6(HedyTester):
    level = 6
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
    # ask tests
    #
    def test_ask_equals(self):
        code = "antwoord = ask 'wat is je lievelingskleur?'"
        expected = "antwoord = input(f'wat is je lievelingskleur?')"

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_ask_chained(self):
        code = textwrap.dedent("""\
        a is ask 'What is a?'
        b is ask 'Are you sure a is ' a '?'
        print a b""")

        expected = textwrap.dedent("""\
        a = input(f'What is a?')
        b = input(f'Are you sure a is {a}?')
        print(f'{a}{b}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # sleep tests
    #
    def test_sleep_with_calc(self):
        code = textwrap.dedent("""\
            n is 1 * 2 + 3
            sleep n""")
        expected = HedyTester.dedent(
            "n = int(1) * int(2) + int(3)",
            HedyTester.sleep_command_transpiled("n"))

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    #
    # assign tests
    #
    def test_assign_with_equals(self):
        code = "name = Hedy"
        expected = "name = 'Hedy'"

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            unused_allowed=True
        )

    def test_assign_with_equals_no_space(self):
        code = "name=Hedy"
        expected = "name = 'Hedy'"

        self.multi_level_tester(
            max_level=11,
            code=code,
            unused_allowed=True,
            expected=expected
        )

    def test_assign_list_with_equals(self):
        code = "name = Hedy, Lamar"
        expected = "name = ['Hedy', 'Lamar']"

        self.multi_level_tester(
            max_level=11,
            code=code,
            unused_allowed=True,
            expected=expected
        )

    def test_assign_text_with_space(self):
        code = textwrap.dedent("""\
        a is 'Hello World'
        print a

        a = 'Hello World'
        print a

        a is Hello World
        print a

        a = Hello World
        print a""")

        expected = textwrap.dedent("""\
        a = '\\'Hello World\\''
        print(f'{a}')
        a = '\\'Hello World\\''
        print(f'{a}')
        a = 'Hello World'
        print(f'{a}')
        a = 'Hello World'
        print(f'{a}')""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected
        )

    def test_assign_subtract_negative_number(self):
        code = textwrap.dedent("""\
            n = -3-4
            print n""")

        expected = textwrap.dedent(f"""\
            n = {self.int_cast_transpiled('-3', False)} - int(4)
            print(f'{{n}}')""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected
        )

    #
    # music tests
    #
    @parameterized.expand([
        ('*', '*'),
        ('/', '//'),
        ('+', '+'),
        ('-', '-')
    ])
    def test_play_calculation(self, op, expected_op):
        code = textwrap.dedent(f"""\
            note is 34
            play note {op} 1""")
        expected = HedyTester.dedent(
            "note = '34'",
            self.play_transpiled(
                f'{self.int_cast_transpiled("note", quotes=False)} {expected_op} int(1)', quotes=False
            ))

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected,
            max_level=11
        )

    #
    # if tests
    #
    def test_if_equality_linebreak_print(self):
        # line breaks after if-condition are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_trailing_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is trailing_space
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'trailing_space'):
          print(f'shaken')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_2_vars_equality_print(self):
        code = textwrap.dedent("""\
        jouwkeuze is schaar
        computerkeuze is schaar
        if computerkeuze is jouwkeuze print 'gelijkspel!'""")

        expected = textwrap.dedent("""\
        jouwkeuze = 'schaar'
        computerkeuze = 'schaar'
        if convert_numerals('Latin', computerkeuze) == convert_numerals('Latin', jouwkeuze):
          print(f'gelijkspel!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, output='gelijkspel!')

    def test_if_french(self):
        code = textwrap.dedent("""\
        plat_principal = demande "Quel plat principal souhaitez-vous?"
        prix = 0
        si plat_principal est lasagnes prix = 12
        affiche "Ce sera " prix""")

        expected = textwrap.dedent("""\
        plat_principal = input(f'Quel plat principal souhaitez-vous?')
        prix = '0'
        if convert_numerals('Latin', plat_principal) == convert_numerals('Latin', 'lasagnes'):
          prix = '12'
        else:
          x__x__x__x = '5'
        print(f'Ce sera {prix}')""")

        self.multi_level_tester(max_level=7,
                                code=code,
                                expected=expected,
                                lang='fr')

    def test_equality_arabic(self):
        code = textwrap.dedent("""\
        nummer1 is ٢
        nummer2 is 2
        if nummer1 is nummer2 print 'jahoor!'""")

        expected = textwrap.dedent("""\
        nummer1 = '٢'
        nummer2 = '2'
        if convert_numerals('Latin', nummer1) == convert_numerals('Latin', nummer2):
          print(f'jahoor!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, output='jahoor!')

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_space(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}James Bond{q} print {q}shaken{q}""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_spaces(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}Bond James Bond{q} print 'shaken'""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Bond James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_single_quoted_rhs_with_inner_double_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is 'He said "no"' print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if convert_numerals('Latin', answer) == convert_numerals('Latin', 'He said "no"'):
          print(f'no')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_equality_double_quoted_rhs_with_inner_single_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is "He said 'no'" print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if convert_numerals('Latin', answer) == convert_numerals('Latin', 'He said \\'no\\''):
          print(f'no')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_equality_promotes_int_to_string(self):
        code = textwrap.dedent("""\
        a is test
        b is 15
        if a is b c is 1""")

        expected = textwrap.dedent("""\
        a = 'test'
        b = '15'
        if convert_numerals('Latin', a) == convert_numerals('Latin', b):
          c = '1'""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, unused_allowed=True)

    def test_if_equality_assign_calc(self):
        code = textwrap.dedent("""\
        cmp is 1
        test is 2
        acu is 0
        if test is cmp acu is acu + 1""")

        expected = textwrap.dedent(f"""\
        cmp = '1'
        test = '2'
        acu = '0'
        if convert_numerals('Latin', test) == convert_numerals('Latin', cmp):
          acu = {self.int_cast_transpiled('acu', False)} + int(1)""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_with_is(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_with_equals_sign(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam = Hedy print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    #
    # if else tests
    #
    def test_if_equality_print_else_print(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk' else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_ask_equality_print_else_print(self):
        code = textwrap.dedent("""\
        kleur is ask 'Wat is je lievelingskleur?'
        if kleur is groen print 'mooi!' else print 'niet zo mooi'""")

        expected = textwrap.dedent("""\
        kleur = input(f'Wat is je lievelingskleur?')
        if convert_numerals('Latin', kleur) == convert_numerals('Latin', 'groen'):
          print(f'mooi!')
        else:
          print(f'niet zo mooi')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_else_followed_by_print(self):
        code = textwrap.dedent("""\
        kleur is geel
        if kleur is groen antwoord is ok else antwoord is stom
        print antwoord""")

        expected = textwrap.dedent("""\
        kleur = 'geel'
        if convert_numerals('Latin', kleur) == convert_numerals('Latin', 'groen'):
          antwoord = 'ok'
        else:
          antwoord = 'stom'
        print(f'{antwoord}')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_assign_else_assign(self):
        code = textwrap.dedent("""\
        cmp is 1
        test is 2
        acu is 0
        if test is cmp
        acu is acu + 1
        else
        acu is acu + 5""")

        expected = textwrap.dedent(f"""\
        cmp = '1'
        test = '2'
        acu = '0'
        if convert_numerals('Latin', test) == convert_numerals('Latin', cmp):
          acu = {self.int_cast_transpiled('acu', False)} + int(1)
        else:
          acu = {self.int_cast_transpiled('acu', False)} + int(5)""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_with_negative_number(self):
        code = textwrap.dedent("""\
      antwoord is -10
      if antwoord is -10 print 'Nice' else print 'Oh no'""")

        expected = textwrap.dedent("""\
      antwoord = '-10'
      if convert_numerals('Latin', antwoord) == convert_numerals('Latin', '-10'):
        print(f'Nice')
      else:
        print(f'Oh no')""")

        self.multi_level_tester(code=code, expected=expected, output='Nice', max_level=7)

    # Legal syntax:
    #
    # if name is Hedy print 'hello'
    # if name is 'Hedy' print 'hello'
    # if name is 'Hedy is het beste' print 'hello'
    # if name is Hedy c is 5

    # Illegal syntax:
    #
    # if name is Hedy is het beste print 'hello'
    # if name is Hedy is het beste x is 5

    def test_if_equality_print_linebreak_else_print(self):
        # line break before else is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk'
        else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            expected=expected,
            expected_commands=['is', 'if', 'else', 'print', 'print']
        )

    def test_if_equality_linebreak_print_else_print(self):
        # line break after if-condition is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk' else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_print_else_linebreak_print(self):
        # line break after else is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk' else
        print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_linebreak_print_linebreak_else_print(self):
        # line breaks after if-condition and before else are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk'
        else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_linebreak_print_linebreak_else_linebreak_print(self):
        # line breaks after if-condition, before else and after else are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk'
        else
        print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_linebreak_print_else_linebreak_print(self):
        # line breaks after if-condition and after else are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk' else
        print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_space_else(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}James Bond{q} print {q}shaken{q} else print {q}biertje!{q}""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'James Bond'):
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    #
    # arithmetic expressions tests
    #
    def test_print_multiplication(self):
        code = "print 5 * 5"
        expected = "print(f'{int(5) * int(5)}')"
        output = '25'

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    def test_print_addition(self):
        code = "print 5 + 5"
        expected = "print(f'{int(5) + int(5)}')"
        output = '10'

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    def test_print_subtraction_without_text(self):
        code = "print 5 - 5"
        expected = "print(f'{int(5) - int(5)}')"
        output = '0'

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    def test_print_subtraction_with_text(self):
        code = "print 'And the winner is ' 5 - 5"
        expected = "print(f'And the winner is {int(5) - int(5)}')"
        output = 'And the winner is 0'

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            output=output)

    def test_print_nested_calcs(self):
        code = "print 5 * 5 * 5"
        expected = "print(f'{int(5) * int(5) * int(5)}')"
        output = '125'

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    def test_assign_calc_print_var(self):
        code = textwrap.dedent("""\
        nummer is 4 + 5
        print nummer""")

        expected = textwrap.dedent("""\
        nummer = int(4) + int(5)
        print(f'{nummer}')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected, output='9')

    def test_assign_calc_no_space(self):
        code = "nummer is 4+5"
        expected = "nummer = int(4) + int(5)"

        self.multi_level_tester(max_level=11, code=code, expected=expected, unused_allowed=True)

    def test_print_calc_with_var(self):
        code = textwrap.dedent("""\
        var is 5
        print var + 5""")
        expected = textwrap.dedent(f"""\
        var = '5'
        print(f'{{{self.int_cast_transpiled('var', False)} + int(5)}}')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    @parameterized.expand(HedyTester.arithmetic_operations)
    # issue 2067
    def test_assign_calc_precedes_quoted_string(self, operation):
        code = f"a is '3{operation}10'"  # gets parsed to arithmetic operation of '3 and 10'

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand([
        ('*', '*', '16'),
        ('/', '//', '4'),
        ('+', '+', '10'),
        ('-', '-', '6')
    ])
    def test_assign_calc_with_vars(self, op, transpiled_op, output):
        code = textwrap.dedent(f"""\
        nummer is 8
        nummertwee is 2
        getal is nummer {op} nummertwee
        print getal""")

        expected = textwrap.dedent(f"""\
        nummer = '8'
        nummertwee = '2'
        getal = {self.int_cast_transpiled('nummer', False)} {transpiled_op} {self.int_cast_transpiled('nummertwee', False)}
        print(f'{{getal}}')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    @parameterized.expand([
        ('*', '*', '16'),
        ('/', '//', '4'),
        ('+', '+', '10'),
        ('-', '-', '6')
    ])
    def test_print_calc_with_vars(self, op, transpiled_op, output):
        code = textwrap.dedent(f"""\
        nummer is 8
        nummertwee is 2
        print nummer {op} nummertwee""")

        expected = textwrap.dedent(f'''\
        nummer = '8'
        nummertwee = '2'
        print(f'{{{self.int_cast_transpiled('nummer', False)} {transpiled_op} {self.int_cast_transpiled('nummertwee', False)}}}')''')

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    @parameterized.expand([
        ('*', '*', '16'),
        ('/', '//', '4'),
        ('+', '+', '10'),
        ('-', '-', '6')
    ])
    def test_print_calc_with_vars_arabic(self, op, transpiled_op, output):
        code = textwrap.dedent(f"""\
            nummer is ٨
            nummertwee is ٢
            print nummer {op} nummertwee""")

        expected = textwrap.dedent(f"""\
            nummer = '٨'
            nummertwee = '٢'
            print(f'{{{self.int_cast_transpiled('nummer', False)} {transpiled_op} {self.int_cast_transpiled('nummertwee', False)}}}')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    def test_print_calc_arabic_directly(self):
        # TODO: can also be generalized for other ops
        code = textwrap.dedent(f"""\
            قول "٥ ضرب ٥ يساوي " ٥*٥""")

        expected = textwrap.dedent("""\
            print(f'٥ ضرب ٥ يساوي {convert_numerals("Arabic",int(5) * int(5))}')""")

        output = '٥ ضرب ٥ يساوي ٢٥'

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            output=output,
            lang='ar')

    def test_print_calc_arabic_directly_in_en(self):
        # TODO: can also be generalized for other ops
        code = textwrap.dedent(f"""\
            print "nummers" ٥*٥""")

        expected = textwrap.dedent("""\
            print(f'nummers{int(5) * int(5)}')""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            translate=False)

    @parameterized.expand(HedyTester.arithmetic_operations)
    def test_calc_with_text_var_gives_type_error(self, operation):
        code = textwrap.dedent(f"""\
        a is test
        print a {operation} 2""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand(HedyTester.arithmetic_operations)
    def test_calc_with_quoted_string_gives_type_error(self, operation):
        code = textwrap.dedent(f"""\
        a is 1
        print a {operation} 'Test'""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand(HedyTester.arithmetic_operations)
    def test_calc_with_list_var_gives_type_error(self, operation):
        code = textwrap.dedent(f"""\
        a is one, two
        print a {operation} 2""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand(['1.5', '1,5'])
    def test_calculation_with_unsupported_float_gives_error(self, number):
        self.multi_level_tester(
            max_level=11,
            code=f"print {number} + 1",
            exception=hedy.exceptions.UnsupportedFloatException
        )

    def test_print_calc_chained_vars(self):
        code = textwrap.dedent("""\
        a is 5
        b is a + 1
        print a + b""")

        expected = textwrap.dedent(f"""\
        a = '5'
        b = {self.int_cast_transpiled('a', False)} + int(1)
        print(f'{{{self.int_cast_transpiled('a', False)} + {self.int_cast_transpiled('b', False)}}}')""")

        self.multi_level_tester(
            code=code,
            max_level=11,
            expected=expected,
            expected_commands=['is', 'is', 'addition', 'print', 'addition'],
            extra_check_function=lambda x: self.run_code(x) == "11"
        )

    def test_type_reassignment_to_proper_type_valid(self):
        code = textwrap.dedent("""\
        a is Hello
        a is 5
        b is a + 1
        print a + b""")

        expected = textwrap.dedent(f"""\
        a = 'Hello'
        a = '5'
        b = {self.int_cast_transpiled('a', False)} + int(1)
        print(f'{{{self.int_cast_transpiled('a', False)} + {self.int_cast_transpiled('b', False)}}}')""")

        self.multi_level_tester(
            code=code,
            max_level=11,
            expected=expected,
            expected_commands=['is', 'is', 'is', 'addition', 'print', 'addition'],
            extra_check_function=lambda x: self.run_code(x) == "11"
        )

    def test_type_reassignment_to_wrong_type_raises_error(self):
        code = textwrap.dedent("""\
        a is 5
        a is test
        print a + 2""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_cyclic_var_definition_gives_error(self):
        code = "b is b + 1"

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.CyclicVariableDefinitionException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1
        )

    #
    # combined tests
    #
    def test_if_calc_else_calc_print(self):
        code = textwrap.dedent("""\
        keuzes is 1, 2, 3, 4, 5, regenworm
        punten is 0
        worp is keuzes at random
        if worp is regenworm punten is punten + 5
        else punten is punten + worp
        print 'dat zijn dan ' punten""")

        expected = HedyTester.dedent("""\
        keuzes = ['1', '2', '3', '4', '5', 'regenworm']
        punten = '0'""",
                                     HedyTester.list_access_transpiled('random.choice(keuzes)'),
                                     "worp = random.choice(keuzes)",
                                     f"""\
        if convert_numerals('Latin', worp) == convert_numerals('Latin', 'regenworm'):
          punten = {self.int_cast_transpiled('punten', False)} + int(5)
        else:
          punten = {self.int_cast_transpiled('punten', False)} + {self.int_cast_transpiled('worp', False)}
        print(f'dat zijn dan {{punten}}')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_consecutive_if_statements(self):
        code = textwrap.dedent("""\
        names is Hedy, Lamar
        name is ask 'What is a name you like?'
        if name is Hedy print 'nice!'
        if name in names print 'nice!'""")

        expected = textwrap.dedent("""\
        names = ['Hedy', 'Lamar']
        name = input(f'What is a name you like?')
        if convert_numerals('Latin', name) == convert_numerals('Latin', 'Hedy'):
          print(f'nice!')
        else:
          x__x__x__x = '5'
        if name in names:
          print(f'nice!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_consecutive_if_and_if_else_statements(self):
        code = textwrap.dedent("""\
        naam is ask 'hoe heet jij?'
        if naam is Hedy print 'leuk'
        if naam is Python print 'ook leuk'
        else print 'minder leuk!'""")

        expected = textwrap.dedent("""\
        naam = input(f'hoe heet jij?')
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')
        else:
          x__x__x__x = '5'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Python'):
          print(f'ook leuk')
        else:
          print(f'minder leuk!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_two_ifs_assign(self):
        code = textwrap.dedent("""\
        order is fries
        if order is fries price is 5
        drink is water
        print drink""")

        expected = textwrap.dedent("""\
        order = 'fries'
        if convert_numerals('Latin', order) == convert_numerals('Latin', 'fries'):
          price = '5'
        else:
          x__x__x__x = '5'
        drink = 'water'
        print(f'{drink}')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, translate=False, unused_allowed=True)

    def test_consecutive_if_else_statements(self):
        code = textwrap.dedent("""\
        names is Hedy, Lamar
        name is ask 'What is a name you like?'
        if name is Hedy print 'nice!' else print 'meh'
        if name in names print 'nice!' else print 'meh'""")

        expected = textwrap.dedent("""\
        names = ['Hedy', 'Lamar']
        name = input(f'What is a name you like?')
        if convert_numerals('Latin', name) == convert_numerals('Latin', 'Hedy'):
          print(f'nice!')
        else:
          print(f'meh')
        if name in names:
          print(f'nice!')
        else:
          print(f'meh')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_print_single_number(self):
        code = textwrap.dedent("""\
                print 5""")

        expected = textwrap.dedent("""\
                print(f'5')""")

        self.multi_level_tester(max_level=6, code=code, expected=expected)

    def test_negative_variable(self):
        code = textwrap.dedent("""\
        a = -3
        b = a + 3
        print b""")
        expected = textwrap.dedent(f"""\
        a = '-3'
        b = {self.int_cast_transpiled('a', False)} + int(3)
        print(f'{{b}}')""")
        self.multi_level_tester(code=code, expected=expected, output='0', max_level=11)

    def test_turtle_with_expression(self):
        self.maxDiff = None
        code = textwrap.dedent("""\
        num = 10
        turn num + 10
        forward 10 + num""")

        expected = textwrap.dedent(f"""\
        num = '10'
        __trtl = {self.int_cast_transpiled(self.int_cast_transpiled('num', False) + ' + int(10)', False)}
        t.right(min(600, __trtl) if __trtl > 0 else max(-600, __trtl))
        __trtl = {self.int_cast_transpiled('int(10) + ' + self.int_cast_transpiled('num', False), False)}
        t.forward(min(600, __trtl) if __trtl > 0 else max(-600, __trtl))
        time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)
