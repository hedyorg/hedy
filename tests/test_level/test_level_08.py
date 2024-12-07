import textwrap

from parameterized import parameterized

import hedy
from hedy import Command
from hedy_sourcemap import SourceRange
from tests.Tester import HedyTester, SkippedMapping


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
    # if tests
    #
    def test_if_one_line(self):
        code = textwrap.dedent("""\
        prind skipping
        antwoord is 25
        if antwoord is 100 print 'goed zo' else print 'neenee'""")

        expected = textwrap.dedent("""\
        pass
        antwoord = Value('25', num_sys='Latin')
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 15), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(3, 1, 3, 55), hedy.exceptions.WrongLevelException)
        ]

        # one line if's are no longer allowed
        self.multi_level_tester(
            code=code,
            max_level=11,
            expected=expected,
            skipped_mappings=skipped_mappings,
        )

    def test_if_no_indentation(self):
        code = textwrap.dedent("""\
        antwoord is ask Hoeveel is 10 keer tien?
        if antwoord is 100
        print 'goed zo'""")

        # gives the right exception for all levels even though it misses brackets
        # because the indent check happens before parsing
        self.single_level_tester(code=code, exception=hedy.exceptions.TooFewIndentsStartLevelException)

    def test_if_equality_with_is(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
            print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_with_equals_sign(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam = Hedy
            print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_linebreak_comment_print(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
            # comment
            print 'hedy'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'hedy')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_comment_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy  # this linebreak is allowed
            print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected, output='leuk')

    def test_if_equality_linebreak_print_comment(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
            print 'leuk'  # this linebreak is allowed""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected, output='leuk')

    def test_if_equality_trailing_space_linebreak_print(self):
        value = 'trailing_space  '
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {value}
            print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = Value('James')
        if localize(naam.data) == localize('trailing_space'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_unquoted_rhs_with_space(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond
            print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = Value('James')
        if localize(naam.data) == localize('James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_unquoted_rhs_with_multi_space(self):
        code = textwrap.dedent("""\
        v is three   spaces
        if v is three   spaces
            print '3'""")

        expected = textwrap.dedent("""\
        v = Value('three   spaces')
        if localize(v.data) == localize('three   spaces'):
          print(f'3')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11, output='3')

    def test_if_equality_unquoted_rhs_with_space_and_trailing_space_linebreak_print(self):
        value = 'trailing space  '
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {value}
            print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = Value('James')
        if localize(naam.data) == localize('trailing space'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_space(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}James Bond{q}
            print {q}shaken{q}""")

        expected = textwrap.dedent(f"""\
        naam = Value('James')
        if localize(naam.data) == localize('James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_spaces(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}Bond James Bond{q}
            print 'shaken'""")

        expected = textwrap.dedent(f"""\
        naam = Value('James')
        if localize(naam.data) == localize('Bond James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_single_quoted_rhs_with_inner_double_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is 'He said "no"'
          print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = Value('no')
        if localize(answer.data) == localize('He said "no"'):
          print(f'no')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_equality_double_quoted_rhs_with_inner_single_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is "He said 'no'"
          print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = Value('no')
        if localize(answer.data) == localize('He said \\'no\\''):
          print(f'no')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_2_vars_equality_print(self):
        code = textwrap.dedent("""\
        jouwkeuze is schaar
        computerkeuze is schaar
        if computerkeuze is jouwkeuze
            print 'gelijkspel!'""")

        expected = textwrap.dedent("""\
        jouwkeuze = Value('schaar')
        computerkeuze = Value('schaar')
        if localize(computerkeuze.data) == localize(jouwkeuze.data):
          print(f'gelijkspel!')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected, output='gelijkspel!')

    def test_unquoted_print_in_body(self):
        code = textwrap.dedent("""\
        svar = ask 'Vad är 5 plus 5?'
        if svar is 10
            print 'Bra jobbat!
            print 'Svaret var faktiskt ' svar""")

        self.multi_level_tester(code=code,
                                skip_faulty=False,
                                exception=hedy.exceptions.UnquotedTextException,
                                max_level=16)

    def test_wrongly_quoted_print_in_body(self):
        code = textwrap.dedent("""\
        svar = ask 'Vad är 5 plus 5?'
        if svar is 10
            print 'Bra jobbat!"
            print 'Svaret var faktiskt ' svar""")

        self.multi_level_tester(code=code,
                                skip_faulty=False,
                                exception=hedy.exceptions.UnquotedTextException,
                                max_level=16)

    def test_if_equality_assign_calc(self):
        code = textwrap.dedent("""\
        cmp is 1
        test is 2
        acu is 0
        if test is cmp
            acu is acu + 1""")

        expected = textwrap.dedent(f"""\
        cmp = Value('1', num_sys='Latin')
        test = Value('2', num_sys='Latin')
        acu = Value('0', num_sys='Latin')
        if localize(test.data) == localize(cmp.data):
          acu = Value({self.number_transpiled('acu')} + {self.number_transpiled(1)}, num_sys=get_num_sys(acu))""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_equality_promotes_int_to_string(self):
        code = textwrap.dedent("""\
        a is test
        b is 15
        if a is b
            b is 1""")

        expected = textwrap.dedent("""\
        a = Value('test')
        b = Value('15', num_sys='Latin')
        if localize(a.data) == localize(b.data):
          b = Value('1', num_sys='Latin')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_equality_with_lists_gives_error(self):
        # Lists can be compared for equality starting with level 14
        code = textwrap.dedent("""\
        m is 1, 2
        n is 1, 2
        if m is n
          print 'success!'""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
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
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_if_with_negative_number(self):
        code = textwrap.dedent("""\
        antwoord = -10
        if antwoord is -10
            print 'Nice'""")

        expected = textwrap.dedent("""\
        antwoord = Value('-10', num_sys='Latin')
        if localize(antwoord.data) == localize('-10'):
          print(f'Nice')""")

        self.multi_level_tester(code=code, expected=expected, output='Nice', max_level=11)

    def test_if_arabic_number_equals_latin_number(self):
        code = textwrap.dedent("""\
        if ١١ is 11
          print 'correct'""")

        expected = textwrap.dedent("""\
        if localize('١١') == localize('11'):
          print(f'correct')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11, output='correct')

    def test_if_arabic_var_equals_latin_number(self):
        code = textwrap.dedent("""\
        a is ١١
        if a is 11
          print 'correct'""")

        expected = textwrap.dedent("""\
        a = Value('11', num_sys='Arabic')
        if localize(a.data) == localize('11'):
          print(f'correct')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11, output='correct')

    def test_equality_arabic_and_latin_vars(self):
        code = textwrap.dedent("""\
        nummer1 is ٢
        nummer2 is 2
        if nummer1 is nummer2
          print 'jahoor!'""")

        expected = textwrap.dedent(f"""\
        nummer1 = {self.value(2, "Arabic")}
        nummer2 = {self.value(2)}
        if localize(nummer1.data) == localize(nummer2.data):
          print(f'jahoor!')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11, output='jahoor!')

    def test_assign_var_in_if_trims_spaces(self):
        code = self.dedent(
            "if 1 = 1",
            ("j = 4   ", "  "),
            ("    print '[' j ']'", "  "))

        expected = textwrap.dedent(f"""\
        if localize('1') == localize('1'):
          j = Value('4', num_sys='Latin')
          print(f'[{{j}}]')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11, output='[4]')

    def test_assign_var_in_if_trims_spaces_with_comment(self):
        code = textwrap.dedent("""\
        if 1 = 1
            j = 4    # met comment
            print '[' j ']'""")

        expected = textwrap.dedent(f"""\
        if localize('1') == localize('1'):
          j = Value('4', num_sys='Latin')
          print(f'[{{j}}]')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11, output='[4]')

    #
    # in/not in list
    #
    def test_if_in_list_print(self):
        code = textwrap.dedent("""\
        items is red, green
        selected is red
        if selected in items
            print 'found!'""")

        expected = textwrap.dedent(f"""\
        items = Value([Value('red'), Value('green')])
        selected = Value('red')
        if {self.in_list_transpiled('selected.data', 'items')}:
          print(f'found!')""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            output='found!',
            expected_commands=['is', 'is', 'if', 'in', 'print']
        )

    def test_if_not_in_list_print(self):
        code = textwrap.dedent("""\
         letters is a, b, c
         if d not in letters
             print 'Not found'""")

        expected = textwrap.dedent(f"""\
         letters = Value([Value('a'), Value('b'), Value('c')])
         if {self.not_in_list_transpiled("'d'", 'letters')}:
           print(f'Not found')""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            output='Not found'
        )

    @parameterized.expand(HedyTester.in_not_in_list_commands)
    def test_if_not_in_and_in_list_with_string_var_gives_type_error(self, operator):
        code = textwrap.dedent(f"""\
        items is red
        if red {operator} items
          print 'found!'""")
        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand(HedyTester.in_not_in_list_commands)
    def test_if_not_in_and_in_list_with_input_gives_type_error(self, operator):
        code = textwrap.dedent(f"""\
            items is ask 'What are the items?'
            if red {operator} items
              print 'found!'""")
        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_if_in_undefined_list_gives_error(self):
        code = textwrap.dedent("""\
        selected is 5
        if selected in items
            print 'found!'""")

        self.multi_level_tester(code=code, exception=hedy.exceptions.UndefinedVarException, max_level=16)

    def test_if_in_list_with_string_var_gives_type_error(self):
        code = textwrap.dedent("""\
        items is red
        if red in items
            print 'found!'""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
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
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_if_ar_number_list_with_latin_numbers(self):
        code = textwrap.dedent("""\
        a is 11, 22, 33
        if ١١ in a
          print 'correct'""")

        expected = textwrap.dedent(f"""\
        a = {self.list_transpiled("11", "22", "33")}
        if {self.in_list_transpiled("'١١'", 'a')}:
          print(f'correct')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11, output='correct')

    def test_if_ar_number_not_list_with_latin_numbers(self):
        code = textwrap.dedent("""\
        a is 22, 33, 44
        if ١١ not in a
          print 'correct'""")

        expected = textwrap.dedent(f"""\
        a = {self.list_transpiled("22", "33", "44")}
        if {self.not_in_list_transpiled("'١١'", 'a')}:
          print(f'correct')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11, output='correct')

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

        self.single_level_tester(code=code,
                                 exception=hedy.exceptions.TooFewIndentsStartLevelException)

    def test_if_equality_print_else_print(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
            print 'leuk'
        else
            print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
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
        a = Value('5', num_sys='Latin')
        if localize(a.data) == localize('1'):
          x = Value('2', num_sys='Latin')
        else:
          x = Value('222', num_sys='Latin')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_if_else_followed_by_print(self):
        code = textwrap.dedent("""\
        kleur is geel
        if kleur is groen
            antwoord is ok
        else
            antwoord is stom
        print antwoord""")

        expected = textwrap.dedent("""\
        kleur = Value('geel')
        if localize(kleur.data) == localize('groen'):
          antwoord = Value('ok')
        else:
          antwoord = Value('stom')
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
        a = Value('1', num_sys='Latin')
        if localize(a.data) == localize('1'):
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

        expected = self.dedent(
            "people = Value([Value('mom'), Value('dad'), Value('Emma'), Value('Sophie')])",
            self.list_access_transpiled('random.choice(people.data)'),
            """\
            dishwasher = random.choice(people.data)
            if localize(dishwasher.data) == localize('Sophie'):
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
        if localize('1') == localize('2'):
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
        if localize('1') == localize('2'):
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

        expected = self.dedent(
            self.input_transpiled('antwoord', 'Hoeveel is 10 plus 10?'),
            """\
            if localize(antwoord.data) == localize('20'):
              print(f'Goedzo!')
              print(f'Het antwoord was inderdaad {antwoord}')
            else:
              print(f'Foutje')
              print(f'Het antwoord moest zijn {antwoord}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_equality_arabic(self):
        code = textwrap.dedent("""\
        nummer1 is ٢
        nummer2 is 2
        if nummer1 is nummer2
          print 'jahoor!'""")

        expected = textwrap.dedent(f"""\
        nummer1 = Value('2', num_sys='Arabic')
        nummer2 = Value('2', num_sys='Latin')
        if localize(nummer1.data) == localize(nummer2.data):
          print(f'jahoor!')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected, output='jahoor!')

    #
    # repeat tests
    #
    def test_repeat_no_indentation(self):
        code = textwrap.dedent("""\
          repeat 3 times
          print 'hooray!'""")

        self.single_level_tester(code=code, exception=hedy.exceptions.TooFewIndentsStartLevelException)

    def test_repeat_repair_too_few_indents(self):
        code = textwrap.dedent("""\
        repeat 5 times
             print 'repair'
          print 'me'""")

        fixed_code = textwrap.dedent("""\
        repeat 5 times
             print 'repair'
             print 'me'""")

        self.single_level_tester(
            code=code,
            exception=hedy.exceptions.TooFewIndentsStartLevelException,
            extra_check_function=(lambda x: x.exception.fixed_code == fixed_code)
        )

    def test_repeat_repair_too_many_indents(self):
        code = textwrap.dedent("""\
        repeat 5 times
          print 'repair'
             print 'me'""")
        fixed_code = textwrap.dedent("""\
        repeat 5 times
          print 'repair'
          print 'me'""")

        self.single_level_tester(
            code=code,
            exception=hedy.exceptions.TooManyIndentsStartLevelException,
            extra_check_function=(lambda x: x.exception.fixed_code == fixed_code),
            skip_faulty=False
        )

    def test_unexpected_indent(self):
        code = textwrap.dedent("""\
        print 'repair'
           print 'me'""")

        self.single_level_tester(
            code=code,
            exception=hedy.exceptions.TooManyIndentsStartLevelException
        )

    def test_repeat_empty_lines(self):
        code = textwrap.dedent("""\
            repeat 2 times
                
                
                sleep""")

        expected = textwrap.dedent(f"""\
            for __i in range({self.int_transpiled(2)}):
              time.sleep(1)
              time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_with_comment(self):
        code = textwrap.dedent("""\
        repeat 5 times #This should be ignored
            sleep""")

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_transpiled(5)}):
          time.sleep(1)
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_inner_whole_line_comment(self):
        code = textwrap.dedent("""\
            repeat 2 times
                # let's sleep!
                sleep""")

        expected = textwrap.dedent(f"""\
            for __i in range({self.int_transpiled(2)}):
              time.sleep(1)
              time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_end_line_comment(self):
        code = textwrap.dedent("""\
            repeat 2 times
                sleep # let's print!""")

        expected = textwrap.dedent(f"""\
            for __i in range({self.int_transpiled(2)}):
              time.sleep(1)
              time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_whole_line_comment_after(self):
        code = textwrap.dedent("""\
            repeat 2 times
                sleep
            # let's print!""")

        expected = textwrap.dedent(f"""\
            for __i in range({self.int_transpiled(2)}):
              time.sleep(1)
              time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_turtle(self):
        code = textwrap.dedent("""\
            repeat 3 times
                forward 100""")

        expected = self.dedent(
            f"for __i in range({self.int_transpiled(3)}):",
            (self.forward_transpiled(100), '  '))

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

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_transpiled(5)}):
          print(f'koekoek')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_arabic_number_print(self):
        code = textwrap.dedent("""\
        repeat ٥ times
            print 'koekoek'""")

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_transpiled(5)}):
          print(f'koekoek')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_print_variable(self):
        code = textwrap.dedent("""\
            n is 5
            repeat n times
                print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
            n = Value('5', num_sys='Latin')
            for __i in range({self.int_transpiled('n.data')}):
              print(f'me wants a cookie!')
              time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=11)

    def test_repeat_arabic_var_print(self):
        code = textwrap.dedent("""\
            n is ٥
            repeat n times
                print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
            n = Value('5', num_sys='Arabic')
            for __i in range({self.int_transpiled('n.data')}):
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

        expected = textwrap.dedent(f"""\
            állatok = Value('5', num_sys='Latin')
            for __i in range({self.int_transpiled('állatok.data')}):
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

    def test_repeat_keyword_variable(self):
        code = textwrap.dedent("""\
            sum is 2
            repeat sum times
              print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
            _sum = Value('2', num_sys='Latin')
            for __i in range({self.int_transpiled('_sum.data')}):
              print(f'me wants a cookie!')
              time.sleep(0.1)""")

        output = textwrap.dedent("""\
            me wants a cookie!
            me wants a cookie!""")

        self.multi_level_tester(code=code, expected=expected, max_level=11, output=output)

    # issue 297
    def test_repeat_print_assign_addition(self):
        code = textwrap.dedent("""\
        count is 1
        repeat 12 times
            print count ' times 12 is ' count * 12
            count is count + 1""")

        print_op = f"{self.number_transpiled('count')} * {self.number_transpiled(12)}"
        expected = textwrap.dedent(f"""\
        count = Value('1', num_sys='Latin')
        for __i in range({self.int_transpiled(12)}):
          print(f'{{count}} times 12 is {{localize({print_op}, num_sys=get_num_sys(count))}}')
          count = Value({self.number_transpiled('count')} + {self.number_transpiled(1)}, num_sys=get_num_sys(count))
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_with_string_variable_gives_type_error(self):
        code = textwrap.dedent("""\
        n is 'test'
        repeat n times
            print 'n'""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            max_level=17)

    def test_repeat_with_list_variable_gives_type_error(self):
        code = textwrap.dedent("""\
        n is 1, 2, 3
        repeat n times
            print 'n'""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            max_level=15)

    def test_repeat_deprecated_gives_deprecated_error(self):
        code = "repeat 5 times print 'In the next tab you can repeat multiple lines of code at once!'"

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.WrongLevelException,
            max_level=17)

    def test_repeat_ask(self):
        code = textwrap.dedent("""\
            n is ask 'How many times?'
            repeat n times
                print 'n'""")

        expected = self.dedent(
            self.input_transpiled('n', 'How many times?'),
            f"""\
            for __i in range({self.int_transpiled('n.data')}):
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
        for __i in range({self.int_transpiled(int(number))}):
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

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_transpiled(10)}):
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

        expected = textwrap.dedent(f"""\
        i = Value('hallo!')
        for __i in range({self.int_transpiled(5)}):
          print(f'me wants a cookie!')
          time.sleep(0.1)
        print(f'{{i}}')""")

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

    def test_repeat_without_body_gives_error(self):
        code = "repeat 5 times"

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.MissingInnerCommandException,
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

        self.single_level_tester(code=code, exception=hedy.exceptions.TooManyIndentsStartLevelException)

    def test_if_repeat_gives_error(self):
        code = textwrap.dedent("""\
        kleur is groen
        if kleur is groen
            repeat 3 times
                print 'mooi'""")

        self.single_level_tester(code=code, exception=hedy.exceptions.TooManyIndentsStartLevelException)

    #
    # if pressed tests
    #

    def test_if_pressed_x_print(self):
        code = textwrap.dedent("""\
        if x is pressed
            print 'it is a letter key'
        else
            print 'other key'""")
        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        def if_pressed_x_():
          print(f'it is a letter key')
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_else_():
          print(f'other key')
        extensions.if_pressed(if_pressed_mapping)""")
        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_pressed_x_is_var(self):
        code = textwrap.dedent("""\
        x is a
        if x is pressed
          print 'it is a letter key'
        else
          print 'it is another letter key'
        print x""")

        expected = self.dedent("""\
        global_scope_ = dict()
        global_scope_["x"] = Value('a')
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping[(global_scope_.get("x") or x).data] = 'if_pressed_x_'
        def if_pressed_x_():
          print(f'it is a letter key')
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_else_():
          print(f'it is another letter key')
        extensions.if_pressed(if_pressed_mapping)
        print(f'{global_scope_.get("x") or x}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_pressed_x_is_var_and_var_reassignment(self):
        code = textwrap.dedent("""\
        x is a
        if x is pressed
          x is great
        else
          x is not great
        print x""")

        expected = self.dedent("""\
        global_scope_ = dict()
        global_scope_["x"] = Value('a')
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping[(global_scope_.get("x") or x).data] = 'if_pressed_x_'
        def if_pressed_x_():
          global_scope_["x"] = Value('great')
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_else_():
          global_scope_["x"] = Value('not great')
        extensions.if_pressed(if_pressed_mapping)
        print(f'{global_scope_.get("x") or x}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_pressed_x_is_var_and_new_var_assignment(self):
        code = textwrap.dedent("""\
        x is a
        if x is pressed
          m is great
        else
          m is not great
        print m""")

        expected = self.dedent("""\
        global_scope_ = dict()
        global_scope_["x"] = Value('a')
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping[(global_scope_.get("x") or x).data] = 'if_pressed_x_'
        def if_pressed_x_():
          global_scope_["m"] = Value('great')
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_else_():
          global_scope_["m"] = Value('not great')
        extensions.if_pressed(if_pressed_mapping)
        print(f'{global_scope_.get("m") or m}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_double_if_pressed(self):
        code = textwrap.dedent("""\
        if x is pressed
          print 'first key'
        else
          print 'other key'
        if y is pressed
          print 'second key'
        else
          print 'other key'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        def if_pressed_x_():
          print(f'first key')
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_else_():
          print(f'other key')
        extensions.if_pressed(if_pressed_mapping)
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['y'] = 'if_pressed_y_'
        def if_pressed_y_():
          print(f'second key')
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_else_():
          print(f'other key')
        extensions.if_pressed(if_pressed_mapping)""")

        self.maxDiff = None
        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_pressed_is_number_key_print(self):
        code = textwrap.dedent("""\
        if 1 is pressed
            print 'it is a number key'
        else
            print 'it is something else'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['1'] = 'if_pressed_1_'
        def if_pressed_1_():
          print(f'it is a number key')
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_else_():
          print(f'it is something else')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_pressed_command_in_between(self):
        code = textwrap.dedent("""\
        if a is pressed
          print 'A is pressed'
        else
          print 'other'
        print 'Press another button'
        if b is pressed
          print 'B is pressed'
        else
          print 'other'""")

        expected = textwrap.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['a'] = 'if_pressed_a_'
        def if_pressed_a_():
          print(f'A is pressed')
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_else_():
          print(f'other')
        extensions.if_pressed(if_pressed_mapping)
        print(f'Press another button')
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['b'] = 'if_pressed_b_'
        def if_pressed_b_():
          print(f'B is pressed')
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_else_():
          print(f'other')
        extensions.if_pressed(if_pressed_mapping)""")

        self.maxDiff = None
        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_pressed_with_random_list_access(self):
        code = textwrap.dedent("""\
            letters is a, b, c, d, e
            print letters at random
            if x is pressed
                print 'great'
            else
                print 'not great'""")

        expected = textwrap.dedent('''\
            global_scope_ = dict()
            global_scope_["letters"] = Value([Value('a'), Value('b'), Value('c'), Value('d'), Value('e')])
            try:
              random.choice((global_scope_.get("letters") or letters).data)
            except IndexError:
              raise Exception("""Runtime Index Error""")
            print(f'{random.choice((global_scope_.get("letters") or letters).data)}')
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['x'] = 'if_pressed_x_'
            def if_pressed_x_():
              print(f'great')
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_else_():
              print(f'not great')
            extensions.if_pressed(if_pressed_mapping)''')

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_pressed_with_index_list_access(self):
        code = textwrap.dedent("""\
            letters is a, b, c, d, e
            print letters at 1
            if x is pressed
                print 'great'
            else
                print 'not great'""")

        expected = textwrap.dedent('''\
            global_scope_ = dict()
            global_scope_["letters"] = Value([Value('a'), Value('b'), Value('c'), Value('d'), Value('e')])
            try:
              (global_scope_.get("letters") or letters).data[int(1)-1]
            except IndexError:
              raise Exception("""Runtime Index Error""")
            print(f'{(global_scope_.get("letters") or letters).data[int(1)-1]}')
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['x'] = 'if_pressed_x_'
            def if_pressed_x_():
              print(f'great')
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_else_():
              print(f'not great')
            extensions.if_pressed(if_pressed_mapping)''')

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_pressed_with_index_var_list_access(self):
        code = textwrap.dedent("""\
            opt is a, b, c
            i is 3
            a is opt at i
            if x is pressed
                print 'x'
            else
                print 'y'""")

        expected = textwrap.dedent('''\
            global_scope_ = dict()
            global_scope_["opt"] = Value([Value('a'), Value('b'), Value('c')])
            global_scope_["i"] = Value('3', num_sys='Latin')
            try:
              (global_scope_.get("opt") or opt).data[int((global_scope_.get("i") or i).data)-1]
            except IndexError:
              raise Exception("""Runtime Index Error""")
            global_scope_["a"] = (global_scope_.get("opt") or opt).data[int((global_scope_.get("i") or i).data)-1]
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['x'] = 'if_pressed_x_'
            def if_pressed_x_():
              print(f'x')
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_else_():
              print(f'y')
            extensions.if_pressed(if_pressed_mapping)''')

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_if_pressed_add_to_list(self):
        code = textwrap.dedent("""\
            colors is red, blue
            if g is pressed
                answer is green
            else
                answer is wrong
            add answer to colors""")

        expected = textwrap.dedent('''\
            global_scope_ = dict()
            global_scope_["colors"] = Value([Value('red'), Value('blue')])
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['g'] = 'if_pressed_g_'
            def if_pressed_g_():
              global_scope_["answer"] = Value('green')
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_else_():
              global_scope_["answer"] = Value('wrong')
            extensions.if_pressed(if_pressed_mapping)
            (global_scope_.get("colors") or colors).data.append(global_scope_.get("answer") or answer)''')

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_pressed_remove_from_list(self):
        code = textwrap.dedent("""\
            colors is red, blue
            if g is pressed
                answer is green
            else
                answer is wrong
            remove answer from colors""")

        expected = textwrap.dedent('''\
            global_scope_ = dict()
            global_scope_["colors"] = Value([Value('red'), Value('blue')])
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['g'] = 'if_pressed_g_'
            def if_pressed_g_():
              global_scope_["answer"] = Value('green')
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_else_():
              global_scope_["answer"] = Value('wrong')
            extensions.if_pressed(if_pressed_mapping)
            try:
              (global_scope_.get("colors") or colors).data.remove(global_scope_.get("answer") or answer)
            except:
              pass''')

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_pressed_with_ask(self):
        code = textwrap.dedent("""\
            a is ask 'question'
            if x is pressed
                print 'x'
            else
                print 'y'""")

        expected = textwrap.dedent('''\
            global_scope_ = dict()
            global_scope_["a"] = input(f'question')
            __ns = get_num_sys(global_scope_.get("a") or a)
            global_scope_["a"] = Value(global_scope_.get("a") or a, num_sys=__ns)
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['x'] = 'if_pressed_x_'
            def if_pressed_x_():
              print(f'x')
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_else_():
              print(f'y')
            extensions.if_pressed(if_pressed_mapping)''')

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_if_pressed_with_calc(self):
        code = textwrap.dedent("""\
            points = 0
            if x is pressed
                points = 1 + 1
            else
                points = 5 - 2
            print points""")

        p = 'global_scope_.get("points") or points'
        expected = textwrap.dedent(f'''\
            global_scope_ = dict()
            global_scope_["points"] = Value('0', num_sys='Latin')
            if_pressed_mapping = {{"else": "if_pressed_default_else"}}
            if_pressed_mapping['x'] = 'if_pressed_x_'
            def if_pressed_x_():
              global_scope_["points"] = Value(1 + 1, num_sys='Latin')
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_else_():
              global_scope_["points"] = Value(5 - 2, num_sys='Latin')
            extensions.if_pressed(if_pressed_mapping)
            print(f'{{{p}}}')''')

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_pressed_with_calc_var(self):
        code = textwrap.dedent("""\
            points = 0
            if x is pressed
                points = points + 1
            else
                points = points - 2
            print points""")

        p = 'global_scope_.get("points") or points'
        points = f'number_with_error({p}, """Runtime Value Error""")'
        one = 'number_with_error(1, """Runtime Value Error""")'
        two = 'number_with_error(2, """Runtime Value Error""")'
        expected = textwrap.dedent(f'''\
            global_scope_ = dict()
            global_scope_["points"] = Value('0', num_sys='Latin')
            if_pressed_mapping = {{"else": "if_pressed_default_else"}}
            if_pressed_mapping['x'] = 'if_pressed_x_'
            def if_pressed_x_():
              global_scope_["points"] = Value({points} + {one}, num_sys=get_num_sys({p}))
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_else_():
              global_scope_["points"] = Value({points} - {two}, num_sys=get_num_sys({p}))
            extensions.if_pressed(if_pressed_mapping)
            print(f'{{{p}}}')''')

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_pressed_missing_else_gives_error(self):
        code = textwrap.dedent("""\
        prind skipping
        if x is pressed
          print 'missing else!'""")

        expected = textwrap.dedent("""\
        global_scope_ = dict()
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 15), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(2, 1, 3, 33), hedy.exceptions.MissingElseForPressitException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            max_level=14
        )

    def test_if_no_indent_after_pressed_and_else_gives_error(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'no indent!'
        else
        print 'no indent again!'""")

        self.single_level_tester(code=code, exception=hedy.exceptions.TooFewIndentsStartLevelException)

    def test_source_map(self):
        self.maxDiff = None
        code = textwrap.dedent("""\
            print 'Welcome to Restaurant Chez Hedy!'
            people = ask 'How many people will be joining us today?'
            print 'Great!'
            repeat people times
                food = ask 'What would you like to order?'
                print food
            print 'Thank you for ordering!'
            print 'Enjoy your meal!'""")

        expected_code = self.dedent(
            "print(f'Welcome to Restaurant Chez Hedy!')",
            self.input_transpiled('people', 'How many people will be joining us today?'),
            f"""\
            print(f'Great!')
            for __i in range({self.int_transpiled('people.data')}):""",
            (self.input_transpiled('food', 'What would you like to order?'), '  '),
            f"""\
              print(f'{{food}}')
              time.sleep(0.1)
            print(f'Thank you for ordering!')
            print(f'Enjoy your meal!')""")

        expected_source_map = {
            '1/1-1/41': '1/1-1/43',
            '2/1-2/7': '2/1-2/7',
            '2/1-2/57': '2/1-4/37',
            '3/1-3/15': '5/1-5/17',
            '4/8-4/14': '2/27-2/33',
            '5/5-5/9': '7/1-7/5',
            '5/5-5/47': '7/1-9/29',
            '6/11-6/15': '9/1-9/5',
            '6/5-6/15': '10/1-10/17',
            '4/1-6/24': '6/1-11/18',
            '7/1-7/32': '12/1-12/34',
            '8/1-8/25': '13/1-13/27',
            '1/1-8/26': '1/1-13/27',
        }

        self.single_level_tester(code, expected=expected_code)
        self.source_map_tester(code=code, expected_source_map=expected_source_map)

    def test_play_repeat_random(self):
        code = textwrap.dedent("""\
            repeat 10 times
                notes is C4, E4, D4, F4, G4
                note is notes at random
                print note
                play note""")

        expected = self.dedent(
            f"for __i in range({self.int_transpiled(10)}):",
            ("notes = Value([Value('C4'), Value('E4'), Value('D4'), Value('F4'), Value('G4')])", '  '),
            (self.list_access_transpiled('random.choice(notes.data)'), '  '),
            ("note = random.choice(notes.data)", '  '),
            ("print(f'{note}')", '  '),
            (self.play_transpiled('note.data'), '  '),
            ("time.sleep(0.1)", '  '))

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=11
        )

    def test_play_integers(self):
        code = textwrap.dedent("""\
        notes = 1, 2, 3

        repeat 10 times
            play notes at random""")

        expected = self.dedent(
            "notes = Value([Value('1', num_sys='Latin'), Value('2', num_sys='Latin'), Value('3', num_sys='Latin')])",
            f"for __i in range({self.int_transpiled(10)}):",
            (self.play_transpiled('random.choice(notes.data).data'), '  '),
            ("time.sleep(0.1)", '  '))

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=11
        )

    def test_play_repeat_with_calc(self):
        code = textwrap.dedent("""\
            note is 34
            repeat 3 times
                play note
                note is note + 1""")

        sum_op = f"{self.number_transpiled('note')} + {self.number_transpiled(1)}"
        expected = self.dedent(
            f"""\
            note = Value('34', num_sys='Latin')
            for __i in range({self.int_transpiled(3)}):""",
            (self.play_transpiled('note.data'), '  '),
            (f"note = Value({sum_op}, num_sys=get_num_sys(note))", '  '),
            ("time.sleep(0.1)", '  '))

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=11
        )
