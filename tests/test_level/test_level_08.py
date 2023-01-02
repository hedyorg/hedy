import textwrap

from parameterized import parameterized

import hedy
from hedy import Command
from tests.Tester import HedyTester


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
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_with_equals_sign(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam = Hedy
            print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_trailing_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is trailing_space
            print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'trailing_space'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_unquoted_rhs_with_space(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond
            print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_unquoted_rhs_with_space_and_trailing_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is trailing space
            print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'trailing space'):
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
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'James Bond'):
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
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Bond James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_single_quoted_rhs_with_inner_double_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is 'He said "no"'
          print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if convert_numerals('Latin', answer) == convert_numerals('Latin', 'He said "no"'):
          print(f'no')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_double_quoted_rhs_with_inner_single_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is "He said 'no'"
          print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if convert_numerals('Latin', answer) == convert_numerals('Latin', 'He said \\'no\\''):
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
        if convert_numerals('Latin', computerkeuze) == convert_numerals('Latin', jouwkeuze):
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
        if convert_numerals('Latin', test) == convert_numerals('Latin', cmp):
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
        if convert_numerals('Latin', a) == convert_numerals('Latin', b):
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

    def test_if_with_negative_number(self):
        code = textwrap.dedent("""\
        antwoord = -10
        if antwoord is -10
            print 'Nice'""")

        expected = textwrap.dedent("""\
        antwoord = '-10'
        if convert_numerals('Latin', antwoord) == convert_numerals('Latin', '-10'):
          print(f'Nice')""")

        self.multi_level_tester(code=code, expected=expected, output='Nice', max_level=11)

    #
    # if else tests
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
        if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_assign_else_assign(self):
        code = textwrap.dedent("""\
        a is 5
        if a is 1
            x is 2
        else
            x is 222""")
        expected = textwrap.dedent("""\
        a = '5'
        if convert_numerals('Latin', a) == convert_numerals('Latin', '1'):
          x = '2'
        else:
          x = '222'""")

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
        if convert_numerals('Latin', kleur) == convert_numerals('Latin', 'groen'):
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
        if convert_numerals('Latin', a) == convert_numerals('Latin', '1'):
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
        if convert_numerals('Latin', dishwasher) == convert_numerals('Latin', 'Sophie'):
          print(f'too bad I have to do the dishes')
        else:
          print(f'luckily no dishes because{dishwasher}is already washing up')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_print_line_with_spaces_works(self):
        code = "print 'hallo'\n      \nprint 'hallo'"
        expected = "print(f'hallo')\nprint(f'hallo')"
        expected_commands = [Command.print, Command.print]

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=expected_commands,
            max_level=11)

    def test_if_empty_start_line_with_whitespace_else_print(self):
        code = "        \n"
        code += textwrap.dedent("""\
        if 1 is 2
            print 'nice!'
        else
            print 'pizza is better'""")

        expected = textwrap.dedent("""\
        if convert_numerals('Latin', '1') == convert_numerals('Latin', '2'):
          print(f'nice!')
        else:
          print(f'pizza is better')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11, translate=False)

    def test_if_empty_middle_line_with_whitespace_else_print(self):
        code = textwrap.dedent("""\
        if 1 is 2
            print 'nice!'""")
        code += "\n        \n"
        code += textwrap.dedent("""\
        else
            print 'pizza is better'""")

        expected = textwrap.dedent("""\
        if convert_numerals('Latin', '1') == convert_numerals('Latin', '2'):
          print(f'nice!')
        else:
          print(f'pizza is better')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_else_with_multiple_lines(self):
        code = textwrap.dedent("""\
        antwoord is ask 'Hoeveel is 10 plus 10?'
        if antwoord is 20
            print 'Goedzo!'
            print 'Het antwoord was inderdaad ' antwoord
        else
            print 'Foutje'
            print 'Het antwoord moest zijn ' antwoord""")

        expected = textwrap.dedent("""\
        antwoord = input(f'Hoeveel is 10 plus 10?')
        if convert_numerals('Latin', antwoord) == convert_numerals('Latin', '20'):
          print(f'Goedzo!')
          print(f'Het antwoord was inderdaad {antwoord}')
        else:
          print(f'Foutje')
          print(f'Het antwoord moest zijn {antwoord}')""")

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

    def test_unexpected_indent(self):
        code = textwrap.dedent("""\
        print('repair')
           print('me')""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.IndentationException
        )

    def test_repeat_turtle(self):
        code = textwrap.dedent("""\
            repeat 3 times
                forward 100""")

        expected = HedyTester.dedent(
            "for i in range(int('3')):",
            (HedyTester.forward_transpiled(100, self.level), '  '))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
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
        állatok = '5'
        for i in range(int(állatok)):
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

    @parameterized.expand(['5', '𑁫', '५', '૫', '੫', '৫', '೫', '୫', '൫', '௫',
                           '౫', '၅', '༥', '᠕', '៥', '๕', '໕', '꧕', '٥', '۵'])
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

    #
    # if pressed tests
    #

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
                print(f'it is a letter key')
                break""")
        self.multi_level_tester(code=code, expected=expected, max_level=11)

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
                print(f'first key')
                break
            if event.type == pygame.KEYDOWN:
              if event.unicode == 'y':
                print(f'second key')
                break""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

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
                print(f'it is a number key')
                break""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # if pressed else tests
    #

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
                print(f'x is pressed!')
                break    
              else:
                print(f'x is not pressed!')
                break\n""") + "    "

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # pressed turtle tests
    #

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
            max_level=11
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
                HedyTester.forward_transpiled(25, self.level),
                14, True)
              }
              break    
            else:
              {HedyTester.indent(
                HedyTester.turn_transpiled(90, self.level),
                14, True)
              }
              break\n""") + "    "

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    #
    # pressed negative tests
    #

    def test_if_no_indent_after_pressed_gives_noindent_error(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'no indent!'""")

        self.multi_level_tester(code=code, exception=hedy.exceptions.NoIndentationException)

    def test_if_no_indent_after_pressed_and_else_gives_noindent_error(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'no indent!'
        else
        print 'no indent again!'""")

        # gives the right exception for all levels even though it misses brackets
        # because the indent check happens before parsing
        self.multi_level_tester(code=code, exception=hedy.exceptions.NoIndentationException)

    #
    # button tests
    #
    def test_if_button_is_pressed_print(self):
        code = textwrap.dedent("""\
        PRINT is button
        if PRINT is pressed 
          print 'The button got pressed!'""")

        expected = HedyTester.dedent(f"""\
        create_button('PRINT')
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.USEREVENT:
            if event.key == 'PRINT':
              print(f'The button got pressed!')
              break""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_button_is_pressed_make_button(self):
        code = textwrap.dedent("""\
        BUTTON1 is button
        if BUTTON1 is pressed 
          BUTTON2 is button""")

        expected = HedyTester.dedent(f"""\
        create_button('BUTTON1')
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.USEREVENT:
            if event.key == 'BUTTON1':
              create_button('BUTTON2')
              break""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_button_is_pressed_print_else_print(self):
        code = textwrap.dedent("""\
        PRINT is button
        PRINT2 is button
        if PRINT is pressed
            print 'The button got pressed!'
        else
            print 'oof :('""")

        expected = HedyTester.dedent(f"""\
        create_button('PRINT')
        create_button('PRINT2')
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.USEREVENT:
            if event.key == 'PRINT':
              print(f'The button got pressed!')
              break    
            else:
              print(f'oof :(')
              break\n""") + "    "

        self.multi_level_tester(code=code, expected=expected, max_level=11)
