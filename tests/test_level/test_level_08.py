import hedy
import textwrap
from tests.Tester import HedyTester
from parameterized import parameterized


class TestsLevel8(HedyTester):
    level = 8
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
    # if command
    #
    def test_if_no_indentation(self):
        code = textwrap.dedent("""\
        antwoord is ask Hoeveel is 10 keer tien?
        if antwoord is 100
        print 'goed zo'""")

        # gives the right exception for all levels even though it misses brackets
        # because the indent check happens before parsing
        self.multi_level_tester(code=code, exception=hedy.exceptions.NoIndentationException)

    def test_if_equality_with_is(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
            print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if str(naam) == str('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_with_equals_sign(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam = Hedy
            print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if str(naam) == str('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_trailing_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is trailing_space 
            print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if str(naam) == str('trailing_space'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_unquoted_rhs_with_space(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond
            print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if str(naam) == str('James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_unquoted_rhs_with_space_and_trailing_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is trailing space  
            print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if str(naam) == str('trailing space'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_space(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}James Bond{q}
            print {q}shaken{q}""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if str(naam) == str('James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_spaces(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}Bond James Bond{q}
            print 'shaken'""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if str(naam) == str('Bond James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_single_quoted_rhs_with_inner_double_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is 'He said "no"'
          print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if str(answer) == str('He said "no"'):
          print(f'no')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_double_quoted_rhs_with_inner_single_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is "He said 'no'"
          print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if str(answer) == str('He said \\'no\\''):
          print(f'no')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_2_vars_equality_print(self):
        code = textwrap.dedent("""\
        jouwkeuze is schaar
        computerkeuze is schaar
        if computerkeuze is jouwkeuze
            print 'gelijkspel!'""")

        expected = textwrap.dedent("""\
        jouwkeuze = 'schaar'
        computerkeuze = 'schaar'
        if str(computerkeuze) == str(jouwkeuze):
          print(f'gelijkspel!')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected, output='gelijkspel!')

    def test_if_in_list_print(self):
        code = textwrap.dedent("""\
        items is red, green
        selected is red
        if selected in items
            print 'found!'""")

        expected = textwrap.dedent("""\
        items = ['red', 'green']
        selected = 'red'
        if selected in items:
          print(f'found!')""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            output='found!',
            expected_commands=['is', 'is', 'if', 'in', 'print']
        )

    def test_if_equality_assign_calc(self):
        code = textwrap.dedent("""\
        cmp is 1
        test is 2
        acu is 0
        if test is cmp
            acu is acu + 1""")

        expected = textwrap.dedent("""\
        cmp = '1'
        test = '2'
        acu = '0'
        if str(test) == str(cmp):
          acu = int(acu) + int(1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_in_undefined_list_gives_error(self):
        code = textwrap.dedent("""\
        selected is 5
        if selected in items
            print 'found!'""")

        self.multi_level_tester(code=code, exception=hedy.exceptions.UndefinedVarException, max_level=16)

    def test_equality_promotes_int_to_string(self):
        code = textwrap.dedent("""\
        a is test
        b is 15
        if a is b
            c is 1""")

        expected = textwrap.dedent("""\
        a = 'test'
        b = '15'
        if str(a) == str(b):
          c = '1'""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_equality_with_lists_gives_error(self):
        code = textwrap.dedent("""\
        m is 1, 2
        n is 1, 2
        if m is n
          print 'success!'""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_if_in_list_with_string_var_gives_type_error(self):
        code = textwrap.dedent("""\
        items is red
        if red in items
            print 'found!'""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_if_in_list_with_input_gives_type_error(self):
        code = textwrap.dedent("""\
        items is ask 'What are the items?'
        if red in items
            print 'found!'""")
        self.multi_level_tester(
            max_level=16,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_equality_with_list_gives_error(self):
        code = textwrap.dedent("""\
        color is 5, 6, 7
        if red is color
            print 'success!'""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    #
    # if else command
    #
    def test_if_else_no_indentation(self):
        code = textwrap.dedent("""\
        antwoord is ask Hoeveel is 10 keer tien?
        if antwoord is 100
        print 'goed zo'
        else
        print 'bah slecht'""")

        # gives the right exception for all levels even though it misses brackets
        # because the indent check happens before parsing
        self.multi_level_tester(code=code, exception=hedy.exceptions.NoIndentationException)

    def test_if_equality_print_else_print(self):
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

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_else_followed_by_print(self):
        code = textwrap.dedent("""\
        kleur is geel
        if kleur is groen
            antwoord is ok
        else
            antwoord is stom
        print antwoord""")

        expected = textwrap.dedent("""\
        kleur = 'geel'
        if str(kleur) == str('groen'):
          antwoord = 'ok'
        else:
          antwoord = 'stom'
        print(f'{antwoord}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_else_trailing_space_after_else(self):
        code = textwrap.dedent("""\
        a is 1
        if a is 1
            print a
        else    
            print 'nee'""")

        expected = textwrap.dedent("""\
        a = '1'
        if str(a) == str('1'):
          print(f'{a}')
        else:
          print(f'nee')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_list_assignment_else_print(self):
        code = textwrap.dedent("""\
        people is mom, dad, Emma, Sophie
        dishwasher is people at random
        if dishwasher is Sophie
            print 'too bad I have to do the dishes'
        else
            print 'luckily no dishes because' dishwasher 'is already washing up'""")

        expected = textwrap.dedent("""\
        people = ['mom', 'dad', 'Emma', 'Sophie']
        dishwasher = random.choice(people)
        if str(dishwasher) == str('Sophie'):
          print(f'too bad I have to do the dishes')
        else:
          print(f'luckily no dishes because{dishwasher}is already washing up')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_empty_line_with_whitespace_else_print(self):
        code = textwrap.dedent("""\
        if 1 is 2
            print 'nice!'
               
        else
            print 'pizza is better'""")

        expected = textwrap.dedent("""\
        if str('1') == str('2'):
          print(f'nice!')
        else:
          print(f'pizza is better')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # repeat command
    #
    def test_repeat_no_indentation(self):
        code = textwrap.dedent("""\
          repeat 3 times
          print 'hooray!'""")

        self.multi_level_tester(code=code, exception=hedy.exceptions.NoIndentationException)

    def test_repeat_repair_too_few_indents(self):
        code = textwrap.dedent("""\
        repeat 5 times
             print('repair')
          print('me')""")

        fixed_code = textwrap.dedent("""\
        repeat 5 times
             print('repair')
             print('me')""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.NoIndentationException,
            extra_check_function=(lambda x: x.exception.fixed_code == fixed_code)
        )

    def test_repeat_repair_too_many_indents(self):
        code = textwrap.dedent("""\
        repeat 5 times
          print('repair')
             print('me')""")
        fixed_code = textwrap.dedent("""\
        repeat 5 times
          print('repair')
          print('me')""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.IndentationException,
            extra_check_function=(lambda x: x.exception.fixed_code == fixed_code)
        )

    def test_repeat_turtle(self):
        code = textwrap.dedent("""\
            repeat 3 times
                forward 100""")

        expected = HedyTester.dedent(
            "for i in range(int('3')):",
            (HedyTester.forward_transpiled(100), '  '))

        self.multi_level_tester(
            max_level=self.max_turtle_level,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_repeat_print(self):
        code = textwrap.dedent("""\
        repeat 5 times
            print 'koekoek'""")

        expected = textwrap.dedent("""\
        for i in range(int('5')):
          print(f'koekoek')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_print_variable(self):
        code = textwrap.dedent("""\
        n is 5
        repeat n times
            print 'me wants a cookie!'""")

        expected = textwrap.dedent("""\
        n = '5'
        for i in range(int(n)):
          print(f'me wants a cookie!')
          time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=11)

    def test_repeat_arabic(self):
        code = textwrap.dedent("""\
        repeat ٥ times
            print 'koekoek'""")

        expected = textwrap.dedent("""\
        for i in range(int('5')):
          print(f'koekoek')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_with_arabic_variable_print(self):
        code = textwrap.dedent("""\
        n is ٥
        repeat ٥ times
            print 'me wants a cookie!'""")

        expected = textwrap.dedent("""\
        n = '٥'
        for i in range(int('5')):
          print(f'me wants a cookie!')
          time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=11)

    def test_repeat_with_non_latin_variable_print(self):
        code = textwrap.dedent("""\
        állatok is 5
        repeat állatok times
            print 'me wants a cookie!'""")

        expected = textwrap.dedent("""\
        v79de0191e90551f058d466c5e8c267ff = '5'
        for i in range(int(v79de0191e90551f058d466c5e8c267ff)):
          print(f'me wants a cookie!')
          time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=11)

    def test_repeat_undefined_variable_gives_error(self):
        code = textwrap.dedent("""\
        repeat n times
            print 'me wants a cookie!'""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.UndefinedVarException,
            max_level=17)

    # issue 297
    def test_repeat_print_assign_addition(self):
        code = textwrap.dedent("""\
        count is 1
        repeat 12 times
            print count ' times 12 is ' count * 12
            count is count + 1""")

        expected = textwrap.dedent("""\
        count = '1'
        for i in range(int('12')):
          print(f'{count} times 12 is {int(count) * int(12)}')
          count = int(count) + int(1)
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_with_comment(self):
        code = textwrap.dedent("""\
        repeat 5 times #This should be ignored
            print 'koekoek'
            print 'koekoek'""")

        expected = textwrap.dedent("""\
        for i in range(int('5')):
          print(f'koekoek')
          print(f'koekoek')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_with_string_variable_gives_type_error(self):
        code = textwrap.dedent("""\
        n is 'test'
        repeat n times
            print 'n'""")

        self.multi_level_tester(code=code, exception=hedy.exceptions.InvalidArgumentTypeException, max_level=17)

    def test_repeat_with_list_variable_gives_type_error(self):
        code = textwrap.dedent("""\
        n is 1, 2, 3
        repeat n times
            print 'n'""")

        self.multi_level_tester(code=code, exception=hedy.exceptions.InvalidArgumentTypeException, max_level=15)

    def test_repeat_ask(self):
        code = textwrap.dedent("""\
        n is ask 'How many times?'
        repeat n times
            print 'n'""")

        expected = textwrap.dedent("""\
        n = input(f'How many times?')
        for i in range(int(n)):
          print(f'n')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    @parameterized.expand(['5', '𑁫', '५', '૫', '੫', '৫', '೫', '୫', '൫', '௫', '౫', '၅', '༥', '᠕', '៥', '๕', '໕', '꧕', '٥', '۵'])
    def test_repeat_with_all_numerals(self, number):
        code = textwrap.dedent(f"""\
        repeat {number} times
            print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
        for i in range(int('{int(number)}')):
          print(f'me wants a cookie!')
          time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=11)

    def test_repeat_over_9_times(self):
        code = textwrap.dedent("""\
        repeat 10 times
            print 'me wants a cookie!'""")

        expected = textwrap.dedent("""\
        for i in range(int('10')):
          print(f'me wants a cookie!')
          time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=['repeat', 'print'],
            output=output,
            max_level=11
        )

    def test_repeat_with_variable_name_collision(self):
        code = textwrap.dedent("""\
        i is hallo!
        repeat 5 times
            print 'me wants a cookie!'
        print i""")

        expected = textwrap.dedent("""\
        i = 'hallo!'
        for _i in range(int('5')):
          print(f'me wants a cookie!')
          time.sleep(0.1)
        print(f'{i}')""")

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
            max_level=11
        )

    #
    # negative tests
    #

    # issue 902
    def test_repeat_if_gives_error(self):
        code = textwrap.dedent("""\
           print 'kassabon'
           prijs is 0
           repeat 7 times # TEST
               ingredient is ask 'wat wil je kopen?'
               if ingredient is appel
                   prijs is prijs + 1
           print 'Dat is in totaal ' prijs ' euro.'""")

        self.single_level_tester(code=code, exception=hedy.exceptions.LockedLanguageFeatureException)

    def test_if_repeat_gives_error(self):
        code = textwrap.dedent("""\
        kleur is groen
        if kleur is groen
            repeat 3 times
                print 'mooi'""")

        self.single_level_tester(code=code, exception=hedy.exceptions.LockedLanguageFeatureException)
