import hedy
import textwrap
from parameterized import parameterized
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

        self.multi_level_tester(code=code, expected=expected, max_level=11)

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
    # assign tests
    #
    def test_assign_with_equals(self):
        code = "name = Hedy"
        expected = "name = 'Hedy'"

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected
        )

    def test_assign_with_equals_no_space(self):
        code = "name=Hedy"
        expected = "name = 'Hedy'"

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected
        )

    def test_assign_list_with_equals(self):
        code = "name = Hedy, Lamar"
        expected = "name = ['Hedy', 'Lamar']"

        self.multi_level_tester(
            max_level=11,
            code=code,
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
        if str(naam) == str('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_trailing_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is trailing_space 
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if str(naam) == str('trailing_space'):
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
        if str(computerkeuze) == str(jouwkeuze):
          print(f'gelijkspel!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, output='gelijkspel!')

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_space(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}James Bond{q} print {q}shaken{q}""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if str(naam) == str('James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_spaces(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}Bond James Bond{q} print 'shaken'""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if str(naam) == str('Bond James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_single_quoted_rhs_with_inner_double_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is 'He said "no"' print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if str(answer) == str('He said "no"'):
          print(f'no')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_equality_double_quoted_rhs_with_inner_single_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is "He said 'no'" print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if str(answer) == str('He said \\'no\\''):
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
        if str(a) == str(b):
          c = '1'""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_assign_calc(self):
        code = textwrap.dedent("""\
        cmp is 1
        test is 2
        acu is 0
        if test is cmp acu is acu + 1""")

        expected = textwrap.dedent("""\
        cmp = '1'
        test = '2'
        acu = '0'
        if str(test) == str(cmp):
          acu = int(acu) + int(1)""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_with_is(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if str(naam) == str('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_with_equals_sign(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam = Hedy print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if str(naam) == str('Hedy'):
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
        if str(naam) == str('Hedy'):
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
        if str(kleur) == str('groen'):
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
        if str(kleur) == str('groen'):
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

        expected = textwrap.dedent("""\
        cmp = '1'
        test = '2'
        acu = '0'
        if str(test) == str(cmp):
          acu = int(acu) + int(1)
        else:
          acu = int(acu) + int(5)""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

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
        if str(naam) == str('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            expected=expected,
            expected_commands=['is', 'else', 'print', 'print']
        )

    def test_if_equality_linebreak_print_else_print(self):
        # line break after if-condition is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk' else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if str(naam) == str('Hedy'):
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
        if str(naam) == str('Hedy'):
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
        if str(naam) == str('Hedy'):
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
        if str(naam) == str('Hedy'):
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
        if str(naam) == str('Hedy'):
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
        if str(naam) == str('James Bond'):
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    #
    # arithmetic expressions tests
    #
    def test_print_calc(self):
        code = "print 5 * 5"
        expected = "print(f'{int(5) * int(5)}')"
        output = '25'

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

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

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_print_calc_with_var(self):
        code = textwrap.dedent("""\
        var is 5
        print var + 5""")
        expected = textwrap.dedent("""\
        var = '5'
        print(f'{int(var) + int(5)}')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    @parameterized.expand(HedyTester.arithmetic_operations)
    # issue 2067
    def test_assign_calc_precedes_quoted_string(self, operation):
        code = f"a is '3{operation}10'"  # gets parsed to arithmetic operation of '3 and 10'

        self.multi_level_tester(
            max_level=11,
            code=code,
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
        getal = int(nummer) {transpiled_op} int(nummertwee)
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

        expected = textwrap.dedent(f"""\
        nummer = '8'
        nummertwee = '2'
        print(f'{{int(nummer) {transpiled_op} int(nummertwee)}}')""")

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
            print(f'{{int(nummer) {transpiled_op} int(nummertwee)}}')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    @parameterized.expand(HedyTester.arithmetic_operations)
    def test_calc_with_text_var_gives_type_error(self, operation):
        code = textwrap.dedent(f"""\
        a is test
        print a {operation} 2""")

        self.multi_level_tester(
            max_level=11,
            code=code,
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

        expected = textwrap.dedent("""\
        a = '5'
        b = int(a) + int(1)
        print(f'{int(a) + int(b)}')""")

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

        expected = textwrap.dedent("""\
        a = 'Hello'
        a = '5'
        b = int(a) + int(1)
        print(f'{int(a) + int(b)}')""")

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
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_cyclic_var_definition_gives_error(self):
        code = "b is b + 1"

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.CyclicVariableDefinitionException
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

        expected = textwrap.dedent("""\
        keuzes = ['1', '2', '3', '4', '5', 'regenworm']
        punten = '0'
        worp = random.choice(keuzes)
        if str(worp) == str('regenworm'):
          punten = int(punten) + int(5)
        else:
          punten = int(punten) + int(worp)
        print(f'dat zijn dan {punten}')""")

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
        if str(name) == str('Hedy'):
          print(f'nice!')
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
        if str(naam) == str('Hedy'):
          print(f'leuk')
        if str(naam) == str('Python'):
          print(f'ook leuk')
        else:
          print(f'minder leuk!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_consecutive_if_else_statements(self):
        code = textwrap.dedent("""\
        names is Hedy, Lamar
        name is ask 'What is a name you like?'
        if name is Hedy print 'nice!' else print 'meh'
        if name in names print 'nice!' else print 'meh'""")

        expected = textwrap.dedent("""\
        names = ['Hedy', 'Lamar']
        name = input(f'What is a name you like?')
        if str(name) == str('Hedy'):
          print(f'nice!')
        else:
          print(f'meh')
        if name in names:
          print(f'nice!')
        else:
          print(f'meh')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)
