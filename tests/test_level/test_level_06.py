import hedy
import textwrap

from hedy_sourcemap import SourceRange
from tests.Tester import HedyTester, SkippedMapping
from parameterized import parameterized


class TestsLevel5(HedyTester):
    level = 5
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
    @parameterized.expand(HedyTester.commands_level_4)
    def test_if_equality_linebreak_print(self, hedy_, python):
        # line breaks after if-condition are allowed
        code = textwrap.dedent(f"""\
        naam is Hedy
        if naam is Hedy
        {hedy_}""")

        expected = textwrap.dedent(f"""\
        naam = 'Hedy'
        if localize(naam) == localize('Hedy'):
          {python}""")

        self.single_level_tester(code=code, expected=expected, unused_allowed=True)

    def test_if_equality_trailing_space_linebreak_print(self):
        value = 'trailing_space  '
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {value}
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if localize(naam) == localize('trailing_space'):
          print(f'shaken')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_unquoted_rhs_with_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if localize(naam) == localize('James Bond'):
          print(f'shaken')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_unquoted_rhs_with_space_and_trailing_space_linebreak_print(self):
        value = 'trailing space  '
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {value}
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if localize(naam) == localize('trailing space'):
          print(f'shaken')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_2_vars_equality_print(self):
        code = textwrap.dedent("""\
        jouwkeuze is schaar
        computerkeuze is schaar
        if computerkeuze is jouwkeuze print 'gelijkspel!'""")

        expected = textwrap.dedent("""\
        jouwkeuze = 'schaar'
        computerkeuze = 'schaar'
        if localize(computerkeuze) == localize(jouwkeuze):
          print(f'gelijkspel!')""")

        self.single_level_tester(code=code, expected=expected, output='gelijkspel!')

    def test_if_arabic_number_equals_latin_number(self):
        code = textwrap.dedent("""\
        if ١١ is 11 print 'correct'""")

        expected = textwrap.dedent("""\
        if localize('١١') == localize('11'):
          print(f'correct')""")

        self.single_level_tester(code=code, expected=expected, output='correct')

    def test_if_arabic_var_equals_latin_number(self):
        code = textwrap.dedent("""\
        a is ١١
        if a is 11 print 'correct'""")

        expected = textwrap.dedent("""\
        a = '١١'
        if localize(a) == localize('11'):
          print(f'correct')""")

        self.single_level_tester(code=code, expected=expected, output='correct')

    def test_if_equality_unquoted_rhs_with_space_print_gives_error(self):
        code = textwrap.dedent("""\
        prind skipping
        naam is James
        if naam is James Bond print 'shaken'""")

        expected = textwrap.dedent("""\
        pass
        naam = 'James'
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 15), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(3, 1, 3, 37), hedy.exceptions.UnquotedEqualityCheckException),
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    def test_if_equality_unquoted_rhs_with_space_and_following_command_print_gives_error(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond print 'shaken'
        print naam
        prind skipping""")

        expected = textwrap.dedent("""\
        naam = 'James'
        pass
        print(f'{naam}')
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(2, 1, 2, 58), hedy.exceptions.UnquotedEqualityCheckException),
            SkippedMapping(SourceRange(4, 1, 4, 15), hedy.exceptions.InvalidCommandException)
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    def test_if_equality_unquoted_rhs_with_space_assign_gives_error(self):
        code = textwrap.dedent("""\
        prind skipping
        naam is James
        if naam is James Bond naam is 'Pietjansma'""")

        expected = textwrap.dedent("""\
        pass
        naam = 'James'
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(3, 1, 3, 43), hedy.exceptions.UnquotedEqualityCheckException),
            SkippedMapping(SourceRange(1, 1, 1, 15), hedy.exceptions.InvalidCommandException)
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_space(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}James Bond{q} print {q}shaken{q}""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if localize(naam) == localize('James Bond'):
          print(f'shaken')""")

        self.single_level_tester(
            code=code,
            expected_commands=['is', 'if', 'print'],
            expected=expected)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_spaces(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}Bond James Bond{q} print 'shaken'""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if localize(naam) == localize('Bond James Bond'):
          print(f'shaken')""")

        self.single_level_tester(code=code, expected=expected)

    def test_ask_if(self):
        code = textwrap.dedent(f"""\
        name is ask 'what is your name?'
        if name is Hedy print 'nice' else print 'boo!'""")

        expected = textwrap.dedent(f"""\
        name = input(f'what is your name?')
        if localize(name) == localize('Hedy'):
          print(f'nice')
        else:
          print(f'boo!')""")

        self.single_level_tester(
            code=code,
            expected_commands=['ask', 'if', 'else', 'print', 'print'],
            expected=expected)

    def test_if_equality_single_quoted_rhs_with_inner_double_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is 'He said "no"' print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if localize(answer) == localize('He said "no"'):
          print(f'no')""")

        self.single_level_tester(
            code=code,
            expected_commands=['is', 'if', 'print'],
            expected=expected)

    def test_if_equality_double_quoted_rhs_with_inner_single_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is "He said 'no'" print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if localize(answer) == localize('He said \\'no\\''):
          print(f'no')""")

        self.single_level_tester(code=code, expected=expected)

    def test_equality_promotes_int_to_string(self):
        code = textwrap.dedent("""\
        a is test
        b is 15
        if a is b c is 1""")
        expected = textwrap.dedent("""\
        a = 'test'
        b = '15'
        if localize(a) == localize(b):
          c = '1'""")

        self.single_level_tester(code=code, expected=expected, unused_allowed=True)

    def test_quoted_ask(self):
        code = "szogek is ask 'Hello'"
        expected = "szogek = input(f'Hello')"

        self.single_level_tester(code=code, expected=expected, unused_allowed=True)

    def test_equality_with_lists_gives_error(self):
        # Lists can be compared for equality starting with level 14
        code = textwrap.dedent("""\
        n is 1, 2
        m is 1, 2
        if n is m print 'success!'""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand(HedyTester.in_not_in_list_commands)
    def test_if_not_in_and_in_list_with_string_var_gives_type_error(self, operator):
        code = textwrap.dedent(f"""\
        items is red
        if red {operator} items print 'found!'""")
        self.multi_level_tester(
            max_level=7,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand(HedyTester.in_not_in_list_commands)
    def test_if_not_in_and_in_list_with_input_gives_type_error(self, operator):
        code = textwrap.dedent(f"""\
        items is ask 'What are the items?'
        if red {operator} items print 'found!'""")
        self.multi_level_tester(
            max_level=7,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    #
    # if else tests
    #
    def test_if_assign_else_assign(self):
        code = textwrap.dedent("""\
        num is 0
        if num is 0 result is num else result is b
        print result""")

        expected = textwrap.dedent("""\
        num = '0'
        if localize(num) == localize('0'):
          result = num
        else:
          result = 'b'
        print(f'{result}')""")

        self.single_level_tester(code=code, expected=expected, output='0')

    @parameterized.expand(['ellers', 'else'])
    def test_if_assign_else_assign_danish(self, else_):
        code = textwrap.dedent(f"""\
        num is 0
        if num is 0 result is num {else_} result is b
        print result""")

        expected = textwrap.dedent("""\
        num = '0'
        if localize(num) == localize('0'):
          result = num
        else:
          result = 'b'
        print(f'{result}')""")

        self.single_level_tester(code=code, expected=expected, lang='da', output='0', translate=False)

    @parameterized.expand(['иначе', 'sinon'])
    def test_if_assign_danish(self, else_):
        # The supplied keywords are the values for `else` in other lang than Danish.
        # So, instead of an if-else, this is an if-statement with a assignment containing spaces.
        code = textwrap.dedent(f"""\
        num is 0
        if num is 0 result is num {else_} result is b
        print result""")

        expected = textwrap.dedent(f"""\
        num = '0'
        if localize(num) == localize('0'):
          result = 'num {else_} result is b'
        else:
          x__x__x__x = '5'
        print(f'{{result}}')""")

        self.single_level_tester(code=code, expected=expected, lang='da', translate=False,
                                 output=f'num {else_} result is b')

    def test_if_equality_print_else_print(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk' else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if localize(naam) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_ask_equality_print_else_print(self):
        code = textwrap.dedent("""\
        kleur is ask 'Wat is je lievelingskleur?'
        if kleur is groen print 'mooi!' else print 'niet zo mooi'""")

        expected = textwrap.dedent("""\
        kleur = input(f'Wat is je lievelingskleur?')
        if localize(kleur) == localize('groen'):
          print(f'mooi!')
        else:
          print(f'niet zo mooi')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_else_followed_by_print(self):
        code = textwrap.dedent("""\
        kleur is geel
        if kleur is groen antwoord is ok else antwoord is stom
        print antwoord""")

        expected = textwrap.dedent("""\
        kleur = 'geel'
        if localize(kleur) == localize('groen'):
          antwoord = 'ok'
        else:
          antwoord = 'stom'
        print(f'{antwoord}')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_trailing_space_linebreak_print_else(self):
        value = 'trailing space  '
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {value} 
        print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if localize(naam) == localize('trailing space'):
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_print_linebreak_else_print(self):
        # line break before else is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk'
        else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if localize(naam) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_print_linebreaks_else_print(self):
        # line break before else is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk'\n\n       
        else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if localize(naam) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_linebreak_print_else_print(self):
        # line break after if-condition is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk' else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if localize(naam) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_unquoted_with_space_linebreak_print_else_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond
        print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if localize(naam) == localize('James Bond'):
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.single_level_tester(code=code, expected=expected)

    def test_two_ifs_assign_no_following(self):
        code = textwrap.dedent("""\
        if order is fries price is 5
        drink is water""")

        expected = textwrap.dedent("""\
        if localize('order') == localize('fries'):
          price = '5'
        else:
          x__x__x__x = '5'
        drink = 'water'""")

        self.single_level_tester(code=code, expected=expected, translate=False, unused_allowed=True)

    def test_two_ifs_assign_following(self):
        code = textwrap.dedent("""\
        if order is fries price is 5
        drink is water
        print drink""")

        expected = textwrap.dedent("""\
        if localize('order') == localize('fries'):
          price = '5'
        else:
          x__x__x__x = '5'
        drink = 'water'
        print(f'{drink}')""")

        self.single_level_tester(code=code, expected=expected, translate=False, unused_allowed=True)

    def test_if_equality_print_else_linebreak_print(self):
        # line break after else is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk' else
        print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if localize(naam) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_with_negative_number(self):
        code = textwrap.dedent("""\
            antwoord is -10
            if antwoord is -10 print 'Nice' else print 'Oh no'""")

        expected = textwrap.dedent("""\
            antwoord = '-10'
            if localize(antwoord) == localize('-10'):
              print(f'Nice')
            else:
              print(f'Oh no')""")

        self.single_level_tester(code=code, expected=expected, output='Nice')

    def test_if_equality_linebreak_print_linebreak_else_print(self):
        # line breaks after if-condition and before else are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk'
        else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if localize(naam) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

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
        if localize(naam) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_linebreak_print_else_linebreak_print(self):
        # line breaks after if-condition and after else are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk' else
        print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if localize(naam) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_list_assignment_else_print(self):
        code = textwrap.dedent("""\
        people is mom, dad, Emma, Sophie
        dishwasher is people at random
        if dishwasher is Sophie
        print 'too bad I have to do the dishes'
        else
        print 'luckily no dishes because' dishwasher 'is already washing up'""")

        expected = self.dedent(
            "people = ['mom', 'dad', 'Emma', 'Sophie']",
            self.list_access_transpiled('random.choice(people)'),
            "dishwasher = random.choice(people)",
            "if localize(dishwasher) == localize('Sophie'):",
            ("print(f'too bad I have to do the dishes')", '  '),
            "else:",
            ("print(f'luckily no dishes because{dishwasher}is already washing up')", '  '))

        self.single_level_tester(code=code, expected=expected)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_space_else(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}James Bond{q} print {q}shaken{q} else print {q}biertje!{q}""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if localize(naam) == localize('James Bond'):
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_text_with_spaces_and_single_quotes_linebreak_print_else_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James 'Bond'
        print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if localize(naam) == localize('James \\'Bond\\''):
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_text_with_spaces_and_double_quotes_linebreak_print_else_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James "Bond"
        print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if localize(naam) == localize('James "Bond"'):
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_print_else_print_bengali(self):
        code = textwrap.dedent("""\
        নাম is ask 'আপনার নাম কি?'
        if নাম is হেডি print 'ভালো!' else print 'মন্দ'""")

        expected = textwrap.dedent("""\
        নাম = input(f'আপনার নাম কি?')
        if localize(নাম) == localize('হেডি'):
          print(f'ভালো!')
        else:
          print(f'মন্দ')""")

        self.single_level_tester(code=code, expected=expected)

    def test_else_without_if_gives_error(self):
        code = "else print 'wrong'"

        self.multi_level_tester(code=code, exception=hedy.exceptions.ElseWithoutIfException, max_level=7)

    def test_else_without_if_indentation_gives_error(self):
        code = textwrap.dedent("""\
            if answer is yes print 'great!'
            print 'correct'
            else print 'wrong'""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.ElseWithoutIfException,
            max_level=7,
            skip_faulty=False
        )

    #
    # in/not in tests
    #
    def test_if_var_in_list_print(self):
        code = textwrap.dedent("""\
        items is red, green
        selected is red
        if selected in items print 'found!'""")

        expected = textwrap.dedent(f"""\
        items = ['red', 'green']
        selected = 'red'
        if {self.in_list_transpiled('selected', 'items')}:
          print(f'found!')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            output='found!',
            expected_commands=['is', 'is', 'if', 'in', 'print']
        )

    def test_if_var_in_list_print_else(self):
        code = textwrap.dedent("""\
        items is red, green
        selected is red
        if selected in items print 'found!'
        else print 'not found'""")

        expected = textwrap.dedent(f"""\
        items = ['red', 'green']
        selected = 'red'
        if {self.in_list_transpiled('selected', 'items')}:
          print(f'found!')
        else:
          print(f'not found')""")

        self.single_level_tester(code=code, expected=expected, output='found!')

    def test_if_var_not_in_list_print_else(self):
        code = textwrap.dedent("""\
        items is red, green
        selected is purple
        if selected not in items print 'not found!'
        else print 'found'""")

        expected = textwrap.dedent(f"""\
        items = ['red', 'green']
        selected = 'purple'
        if {self.not_in_list_transpiled('selected', 'items')}:
          print(f'not found!')
        else:
          print(f'found')""")

        self.single_level_tester(code=code, expected=expected, output='not found!')

    def test_if_ar_number_list_with_latin_numbers(self):
        code = textwrap.dedent("""\
        a is 11, 22, 33
        if ١١ in a print 'correct'""")

        expected = textwrap.dedent(f"""\
        a = ['11', '22', '33']
        if {self.in_list_transpiled("'١١'", 'a')}:
          print(f'correct')""")

        self.single_level_tester(code=code, expected=expected, output='correct')

    def test_if_ar_number_not_list_with_latin_numbers(self):
        code = textwrap.dedent("""\
        a is 22, 33, 44
        if ١١ not in a print 'correct'""")

        expected = textwrap.dedent(f"""\
        a = ['22', '33', '44']
        if {self.not_in_list_transpiled("'١١'", 'a')}:
          print(f'correct')""")

        self.single_level_tester(code=code, expected=expected, output='correct')

    @parameterized.expand(HedyTester.quotes)
    def test_if_quoted_text_in_list_print(self, q):
        code = textwrap.dedent(f"""\
        items is red, green
        if {q}red{q} in items print 'found!'""")

        expected = textwrap.dedent(f"""\
        items = ['red', 'green']
        if {self.in_list_transpiled(f"'red'", 'items')}:
          print(f'found!')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            output='found!',
            expected_commands=['is', 'if', 'in', 'print']
        )

    @parameterized.expand(HedyTester.quotes)
    def test_if_quoted_text_not_in_list_print(self, q):
        code = textwrap.dedent(f"""\
        items is red, green
        if {q}blue{q} not in items print 'not found!'""")

        expected = textwrap.dedent(f"""\
        items = ['red', 'green']
        if {self.not_in_list_transpiled(f"'blue'", 'items')}:
          print(f'not found!')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            output='not found!'
        )

    def test_if_in_undefined_list(self):
        code = textwrap.dedent("""\
        selected is red
        if selected in items print 'found!'""")

        self.multi_level_tester(code=code, exception=hedy.exceptions.UndefinedVarException, max_level=7)

    #
    # combined tests
    #

    def test_consecutive_if_statements(self):
        code = textwrap.dedent("""\
        names is Hedy, Lamar
        name is ask 'What is a name you like?'
        if name is Hedy print 'nice!'
        if name in names print 'nice!'""")

        expected = textwrap.dedent(f"""\
        names = ['Hedy', 'Lamar']
        name = input(f'What is a name you like?')
        if localize(name) == localize('Hedy'):
          print(f'nice!')
        else:
          x__x__x__x = '5'
        if {self.in_list_transpiled('name', 'names')}:
          print(f'nice!')""")

        self.single_level_tester(code=code, expected=expected)

    def test_onno_3372(self):
        code = textwrap.dedent("""\
        antw is ask 'wat kies jij'
        if antw is schaar print 'gelijk spel!'
        print 'test'""")

        expected = textwrap.dedent("""\
        antw = input(f'wat kies jij')
        if localize(antw) == localize('schaar'):
          print(f'gelijk spel!')
        else:
          x__x__x__x = '5'
        print(f'test')""")

        self.single_level_tester(code=code,
                                 expected=expected)

    def test_restaurant_example(self):
        code = textwrap.dedent("""\
        print 'Welkom bij McHedy'
        eten is ask 'Wat wilt u eten?'
        if eten is friet saus is ask 'Welke saus wilt u bij de friet?'
        if eten is pizza topping is ask 'Welke topping wilt u op de pizza?'
        print eten""")

        expected = textwrap.dedent("""\
        print(f'Welkom bij McHedy')
        eten = input(f'Wat wilt u eten?')
        if localize(eten) == localize('friet'):
          saus = input(f'Welke saus wilt u bij de friet?')
        else:
          x__x__x__x = '5'
        if localize(eten) == localize('pizza'):
          topping = input(f'Welke topping wilt u op de pizza?')
        else:
          x__x__x__x = '5'
        print(f'{eten}')""")

        self.single_level_tester(code=code, expected=expected, translate=False, unused_allowed=True)

    def test_onno_3372_else(self):
        code = textwrap.dedent("""\
        antw is ask 'wat kies jij'
        if antw is schaar print 'gelijk spel!' else print ''
        print 'test'""")

        expected = textwrap.dedent("""\
        antw = input(f'wat kies jij')
        if localize(antw) == localize('schaar'):
          print(f'gelijk spel!')
        else:
          print(f'')
        print(f'test')""")

        self.single_level_tester(code=code,
                                 expected=expected)

    def test_consecutive_if_and_if_else_statements(self):
        code = textwrap.dedent("""\
        naam is ask 'hoe heet jij?'
        if naam is Hedy print 'leuk'
        if naam is Python print 'ook leuk'
        else print 'minder leuk!'""")

        expected = textwrap.dedent("""\
        naam = input(f'hoe heet jij?')
        if localize(naam) == localize('Hedy'):
          print(f'leuk')
        else:
          x__x__x__x = '5'
        if localize(naam) == localize('Python'):
          print(f'ook leuk')
        else:
          print(f'minder leuk!')""")

        self.single_level_tester(code=code,
                                 expected=expected)

    def test_consecutive_if_else_statements(self):
        code = textwrap.dedent("""\
        names is Hedy, Lamar
        name is ask 'What is a name you like?'
        if name is Hedy print 'nice!' else print 'meh'
        if name in names print 'nice!' else print 'meh'""")

        expected = textwrap.dedent(f"""\
        names = ['Hedy', 'Lamar']
        name = input(f'What is a name you like?')
        if localize(name) == localize('Hedy'):
          print(f'nice!')
        else:
          print(f'meh')
        if {self.in_list_transpiled('name', 'names')}:
          print(f'nice!')
        else:
          print(f'meh')""")

        self.single_level_tester(code=code, expected=expected)

    def test_turn_if_forward(self):
        code = textwrap.dedent("""\
            angle is 90, 180, 270
            direction is angle at random
            turn direction
            if direction is 180 forward 100""")

        expected = self.dedent(
            """\
            angle = ['90', '180', '270']""",
            self.list_access_transpiled('random.choice(angle)'),
            "direction = random.choice(angle)",
            self.turn_transpiled('direction'),
            "if localize(direction) == localize('180'):",
            (self.forward_transpiled(100), '  '))

        self.single_level_tester(code=code, expected=expected)

    def test_turn_if_forward_else_forward(self):
        code = textwrap.dedent("""\
            angle is 90, 180, 270
            direction is angle at random
            if direction is 180 forward direction
            else turn direction""")

        expected = self.dedent(
            """\
            angle = ['90', '180', '270']""",
            self.list_access_transpiled('random.choice(angle)'),
            "direction = random.choice(angle)",
            "if localize(direction) == localize('180'):",
            (self.forward_transpiled('direction'), '  '),
            "else:",
            (self.turn_transpiled('direction'), '  '))

        self.single_level_tester(code=code, expected=expected)

    def test_list_access_index(self):
        code = textwrap.dedent("""\
            friends is Hedy, Lola, Frida
            friend is friends at 2
            print friend""")

        expected = self.dedent(
            "friends = ['Hedy', 'Lola', 'Frida']",
            self.list_access_transpiled('friends[int(2)-1]'),
            "friend = friends[int(2)-1]",
            "print(f'{friend}')")

        self.single_level_tester(code=code, expected=expected)

    #
    # negative tests
    #
    def test_if_indent_gives_parse_error(self):
        code = textwrap.dedent("""\
        option is ask 'Rock Paper or Scissors?'
        if option is Scissors
            print 'Its a tie!'""")

        expected = textwrap.dedent("""\
        option = input(f'Rock Paper or Scissors?')
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(2, 1, 2, 22), hedy.exceptions.ParseException),
            SkippedMapping(SourceRange(3, 1, 3, 23), hedy.exceptions.InvalidSpaceException),
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    def test_line_with_if_with_space_gives_invalid(self):
        code = textwrap.dedent("""\
        prind skipping
        name is Hedy
         if name is 3 print 'leuk' else print 'stom'""")

        expected = textwrap.dedent("""\
        pass
        name = 'Hedy'
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 15), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(3, 1, 3, 45), hedy.exceptions.InvalidSpaceException),
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings)

    def test_pront_should_suggest_print(self):
        code = textwrap.dedent("""\
        pront 'Hedy is leuk!'
        prind skipping""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 22), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(2, 1, 2, 15), hedy.exceptions.InvalidCommandException)
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    def test_ask_with_unescaped_quote_gives_error(self):
        code = textwrap.dedent("""\
        name is ask 'what's your name?'
        print name""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.UnquotedTextException,
            extra_check_function=lambda c: c.exception.error_location[0] == 1,
            max_level=17
        )

    def test_print_backtick_text_gives_error(self):
        code = "print `nay`"

        self.multi_level_tester(
            max_level=17,
            code=code,
            exception=hedy.exceptions.UnquotedTextException
        )

    def test_if_fix_nl(self):
        code = textwrap.dedent("""\
            naam is 5
            als naam is 5 print 'leuk'
            print 'minder leuk!'""")

        expected = self.dedent("""\
            naam = '5'
            if localize(naam) == localize('5'):
              print(f'leuk')
            else:
              x__x__x__x = '5'
            print(f'minder leuk!')""")

        self.multi_level_tester(
            max_level=5,
            code=code,
            lang='nl',
            expected=expected,
            translate=False
        )

    #
    # if pressed tests
    #

    def test_if_pressed_x_is_letter_key(self):
        code = textwrap.dedent("""\
        if x is pressed print 'it is a letter key' else print 'it is another letter key'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          print(f'it is a letter key')
        def if_pressed_else_():
          print(f'it is another letter key')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_x_is_var(self):
        code = textwrap.dedent("""\
        x is a
        if x is pressed print 'it is a letter key' else print 'it is another letter key'
        print x""")

        expected = self.dedent("""\
        global_scope_ = dict()
        global_scope_["x"] = 'a'
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping[global_scope_.get("x") or x] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          print(f'it is a letter key')
        def if_pressed_else_():
          print(f'it is another letter key')
        extensions.if_pressed(if_pressed_mapping)
        print(f'{global_scope_.get("x") or x}')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_pressed_x_is_var_and_var_reassignment(self):
        code = textwrap.dedent("""\
        x is a
        if x is pressed x is great else x is not great
        print x""")

        expected = self.dedent("""\
        global_scope_ = dict()
        global_scope_["x"] = 'a'
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping[global_scope_.get("x") or x] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          global_scope_["x"] = 'great'
        def if_pressed_else_():
          global_scope_["x"] = 'not great'
        extensions.if_pressed(if_pressed_mapping)
        print(f'{global_scope_.get("x") or x}')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_pressed_x_is_var_and_new_var_assignment(self):
        code = textwrap.dedent("""\
        x is a
        if x is pressed m is great else m is not great
        print m""")

        expected = self.dedent("""\
        global_scope_ = dict()
        global_scope_["x"] = 'a'
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping[global_scope_.get("x") or x] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          global_scope_["m"] = 'great'
        def if_pressed_else_():
          global_scope_["m"] = 'not great'
        extensions.if_pressed(if_pressed_mapping)
        print(f'{global_scope_.get("m") or m}')""")

        self.single_level_tester(code=code, expected=expected)

    def test_double_if_pressed(self):
        code = textwrap.dedent("""\
        if x is pressed print 'first key' else print 'something else'
        if y is pressed print 'second key' else print 'something else'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          print(f'first key')
        def if_pressed_else_():
          print(f'something else')
        extensions.if_pressed(if_pressed_mapping)
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['y'] = 'if_pressed_y_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_y_():
          print(f'second key')
        def if_pressed_else_():
          print(f'something else')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_after_pressed(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'it is a letter key' else print 'something else'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          print(f'it is a letter key')
        def if_pressed_else_():
          print(f'something else')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_1_is_number_key(self):
        code = textwrap.dedent("""\
        if 1 is pressed print 'it is a number key' else print 'something else'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['1'] = 'if_pressed_1_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_1_():
          print(f'it is a number key')
        def if_pressed_else_():
          print(f'something else')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_with_trailing_spaces_after_key(self):
        code = textwrap.dedent("""\
        if x       is pressed print 'trailing spaces!' else print 'something else'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          print(f'trailing spaces!')
        def if_pressed_else_():
          print(f'something else')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_else(self):
        code = textwrap.dedent("""\
        if x is pressed print 'x is pressed!'
        else print 'x is not pressed!'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          print(f'x is pressed!')
        def if_pressed_else_():
          print(f'x is not pressed!')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_both_prints_and_else(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'x is pressed!'
        else
        print 'x is not pressed!'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          print(f'x is pressed!')
        def if_pressed_else_():
          print(f'x is not pressed!')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_first_print_and_else(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'x is pressed!'
        else print 'x is not pressed!'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          print(f'x is pressed!')
        def if_pressed_else_():
          print(f'x is not pressed!')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_second_print_and_else(self):
        code = textwrap.dedent("""\
        if x is pressed print 'x is pressed!'
        else
        print 'x is not pressed!'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          print(f'x is pressed!')
        def if_pressed_else_():
          print(f'x is not pressed!')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_both_prints(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'x is pressed!'
        else print 'x is not pressed!'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          print(f'x is pressed!')
        def if_pressed_else_():
          print(f'x is not pressed!')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_else_with_turtle(self):
        code = textwrap.dedent("""\
            if x is pressed forward 25 else turn 90""")

        expected = self.dedent(
            f"""\
            global_scope_ = dict()
            if_pressed_mapping = {{"else": "if_pressed_default_else"}}
            if_pressed_mapping['x'] = 'if_pressed_x_'
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_x_():""",
            (self.forward_transpiled(25), '  '),
            "def if_pressed_else_():",
            (self.turn_transpiled(90), '  '),
            "extensions.if_pressed(if_pressed_mapping)")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=7
        )

    def test_if_pressed_non_latin(self):
        code = textwrap.dedent("""\
        if ض is pressed print 'arabic' else print 'something else'
        if ש is pressed print 'hebrew' else print 'something else'
        if й is pressed print 'russian' else print 'something else'""")

        expected = textwrap.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['ض'] = 'if_pressed_ض_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_ض_():
          print(f'arabic')
        def if_pressed_else_():
          print(f'something else')
        extensions.if_pressed(if_pressed_mapping)
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['ש'] = 'if_pressed_ש_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_ש_():
          print(f'hebrew')
        def if_pressed_else_():
          print(f'something else')
        extensions.if_pressed(if_pressed_mapping)
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['й'] = 'if_pressed_й_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_й_():
          print(f'russian')
        def if_pressed_else_():
          print(f'something else')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_with_random_list_access(self):
        code = textwrap.dedent("""\
            letters is a, b, c, d, e
            print letters at random
            if x is pressed print 'great' else print 'not great'""")

        expected = textwrap.dedent('''\
            global_scope_ = dict()
            global_scope_["letters"] = ['a', 'b', 'c', 'd', 'e']
            try:
              random.choice(global_scope_.get("letters") or letters)
            except IndexError:
              raise Exception("""Runtime Index Error""")
            print(f'{random.choice(global_scope_.get("letters") or letters)}')
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['x'] = 'if_pressed_x_'
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_x_():
              print(f'great')
            def if_pressed_else_():
              print(f'not great')
            extensions.if_pressed(if_pressed_mapping)''')

        self.single_level_tester(code=code, expected=expected)

    def test_if_pressed_with_index_list_access(self):
        code = textwrap.dedent("""\
            letters is a, b, c, d, e
            print letters at 1
            if x is pressed print 'great' else print 'not great'""")

        expected = textwrap.dedent('''\
            global_scope_ = dict()
            global_scope_["letters"] = ['a', 'b', 'c', 'd', 'e']
            try:
              (global_scope_.get("letters") or letters)[int(1)-1]
            except IndexError:
              raise Exception("""Runtime Index Error""")
            print(f'{(global_scope_.get("letters") or letters)[int(1)-1]}')
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['x'] = 'if_pressed_x_'
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_x_():
              print(f'great')
            def if_pressed_else_():
              print(f'not great')
            extensions.if_pressed(if_pressed_mapping)''')

        self.single_level_tester(code=code, expected=expected)

    def test_if_pressed_with_index_var_list_access(self):
        code = textwrap.dedent("""\
            letters is a, b, c, d, e
            index is 3
            let is letters at index
            if x is pressed print 'x' else print 'y'""")

        expected = textwrap.dedent('''\
            global_scope_ = dict()
            global_scope_["letters"] = ['a', 'b', 'c', 'd', 'e']
            global_scope_["index"] = '3'
            try:
              (global_scope_.get("letters") or letters)[int(global_scope_.get("index") or index)-1]
            except IndexError:
              raise Exception("""Runtime Index Error""")
            global_scope_["let"] = (global_scope_.get("letters") or letters)[int(global_scope_.get("index") or index)-1]
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['x'] = 'if_pressed_x_'
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_x_():
              print(f'x')
            def if_pressed_else_():
              print(f'y')
            extensions.if_pressed(if_pressed_mapping)''')

        self.single_level_tester(code=code, expected=expected, unused_allowed=True)

    def test_if_pressed_with_ask(self):
        code = textwrap.dedent("""\
            a is ask 'question'
            if x is pressed print 'x' else print 'y'""")

        expected = textwrap.dedent('''\
            global_scope_ = dict()
            global_scope_["a"] = input(f'question')
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['x'] = 'if_pressed_x_'
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_x_():
              print(f'x')
            def if_pressed_else_():
              print(f'y')
            extensions.if_pressed(if_pressed_mapping)''')

        self.single_level_tester(code=code, expected=expected, unused_allowed=True)

    def test_if_pressed_missing_else_gives_error(self):
        code = textwrap.dedent("""\
        prind skipping
        if x is pressed print 'hi!'""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 15), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(2, 1, 2, 28), hedy.exceptions.MissingElseForPressitException)
        ]

        self.multi_level_tester(
            max_level=7,
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    def test_if_pressed_missing_else_gives_error_with_new_line(self):
        code = textwrap.dedent("""\
        prind skipping
        if x is pressed print 'hi!'\n""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 15), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(2, 1, 2, 28), hedy.exceptions.MissingElseForPressitException),
        ]

        self.multi_level_tester(
            max_level=7,
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    def test_source_map(self):
        code = textwrap.dedent("""\
        print 'Do you want a good (g) or bad (b) ending?'
        if g is pressed print 'They lived happily ever after ❤'
        else print 'The prince was eaten by a hippopotamus 😭'""")

        expected_code = textwrap.dedent("""\
        global_scope_ = dict()
        print(f'Do you want a good (g) or bad (b) ending?')
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['g'] = 'if_pressed_g_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_g_():
          print(f'They lived happily ever after ❤')
        def if_pressed_else_():
          print(f'The prince was eaten by a hippopotamus 😭')
        extensions.if_pressed(if_pressed_mapping)""")

        expected_source_map = {
            '1/1-1/50': '2/1-2/52',
            '1/1-3/55': '1/1-10/42',
            '2/1-3/54': '3/1-10/42',
            '2/17-2/56': '7/3-7/44',
            '3/6-3/54': '9/3-9/53'
        }

        self.single_level_tester(code, expected=expected_code)
        self.source_map_tester(code=code, expected_source_map=expected_source_map)

    def test_turn_if_play(self):
        code = textwrap.dedent("""\
            answer is ask 'What is the capital of Zimbabwe?'
            if answer is Harare play C6""")

        expected = self.dedent(
            f"""\
            answer = input(f'What is the capital of Zimbabwe?')
            if localize(answer) == localize('Harare'):""",
            (self.play_transpiled("'C6'"), '  '))

        self.single_level_tester(
            code=code,
            skip_faulty=True,
            expected=expected)

    def test_turn_if_else_play(self):
        code = textwrap.dedent("""\
            answer is ask 'What is the capital of Zimbabwe?'
            if answer is Harare play C6 else play C1""")

        expected = self.dedent(
            f"""\
            answer = input(f'What is the capital of Zimbabwe?')
            if localize(answer) == localize('Harare'):""",
            (self.play_transpiled("'C6'"), '  '),
            "else:",
            (self.play_transpiled("'C1'"), '  '))

        self.single_level_tester(
            code=code,
            skip_faulty=False,
            expected=expected)
