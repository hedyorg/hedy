import hedy
import textwrap
from tests.Tester import HedyTester
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
    def test_if_equality_linebreak_print(self):
        # line breaks after if-condition are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if naam == 'Hedy':
          print(f'leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_trailing_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is trailing_space
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if naam == 'trailing_space':
          print(f'shaken')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_unquoted_rhs_with_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if naam == 'James Bond':
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_equality_unquoted_rhs_with_space_and_trailing_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is trailing space
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if naam == 'trailing space':
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_2_vars_equality_print(self):
        code = textwrap.dedent("""\
        jouwkeuze is schaar
        computerkeuze is schaar
        if computerkeuze is jouwkeuze print 'gelijkspel!'""")

        expected = textwrap.dedent("""\
        jouwkeuze = 'schaar'
        computerkeuze = 'schaar'
        if computerkeuze == jouwkeuze:
          print(f'gelijkspel!')""")

        self.single_level_tester(code=code, expected=expected, output='gelijkspel!')

    def test_if_in_list_print(self):
        code = textwrap.dedent("""\
        items is red, green
        selected is red
        if selected in items print 'found!'""")

        expected = textwrap.dedent("""\
        items = ['red', 'green']
        selected = 'red'
        if selected in items:
          print(f'found!')""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            expected=expected,
            output='found!',
            expected_commands=['is', 'is', 'if', 'in', 'print']
        )

    def test_if_in_undefined_list(self):
        code = textwrap.dedent("""\
        selected is red
        if selected in items print 'found!'""")

        self.multi_level_tester(code=code, exception=hedy.exceptions.UndefinedVarException, max_level=7)

    def test_if_equality_unquoted_rhs_with_space_print_gives_error(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond print 'shaken'""")

        self.multi_level_tester(code=code, exception=hedy.exceptions.UnquotedEqualityCheck, max_level=11)

    def test_if_equality_unquoted_rhs_with_space_assign_gives_error(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond naam is 'Pietjansma'""")

        self.multi_level_tester(code=code, exception=hedy.exceptions.UnquotedEqualityCheck, max_level=11)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_space(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}James Bond{q} print {q}shaken{q}""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if naam == 'James Bond':
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
        if naam == 'Bond James Bond':
          print(f'shaken')""")

        self.single_level_tester(code=code, expected=expected)

    def test_ask_if(self):
        code = textwrap.dedent(f"""\
        name is ask 'what is your name?'
        if name is Hedy print 'nice' else print 'boo!'""")

        expected = textwrap.dedent(f"""\
        name = input(f'what is your name?')
        if name == 'Hedy':
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
        if answer == 'He said "no"':
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
        if answer == 'He said \\'no\\'':
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
        if a == b:
          c = '1'""")

        self.single_level_tester(code=code, expected=expected)

    def test_equality_with_lists_gives_error(self):
        code = textwrap.dedent("""\
        n is 1, 2
        m is 1, 2
        if n is m print 'success!'""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_if_in_list_with_string_var_gives_type_error(self):
        code = textwrap.dedent("""\
        items is red
        if red in items print 'found!'""")
        self.multi_level_tester(
            max_level=7,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_if_in_list_with_input_gives_type_error(self):
        code = textwrap.dedent("""\
        items is ask 'What are the items?'
        if red in items print 'found!'""")
        self.multi_level_tester(
            max_level=7,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    #
    # if else tests
    #
    def test_if_equality_print_else_print(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk' else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if naam == 'Hedy':
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
        if kleur == 'groen':
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
        if kleur == 'groen':
          antwoord = 'ok'
        else:
          antwoord = 'stom'
        print(f'{antwoord}')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_trailing_space_linebreak_print_else(self):
        # this code has a space at the end of line 2
        code = textwrap.dedent("""\
        naam is James
        if naam is trailing space
        print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if naam == 'trailing space':
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_print_linebreak_else_print(self):
        # line break before else is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk'
        else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if naam == 'Hedy':
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
        if naam == 'Hedy':
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
        if naam == 'James Bond':
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_print_else_linebreak_print(self):
        # line break after else is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk' else
        print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if naam == 'Hedy':
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
      if antwoord == '-10':
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
        if naam == 'Hedy':
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
        if naam == 'Hedy':
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
        if naam == 'Hedy':
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

        expected = textwrap.dedent("""\
        people = ['mom', 'dad', 'Emma', 'Sophie']
        dishwasher = random.choice(people)
        if dishwasher == 'Sophie':
          print(f'too bad I have to do the dishes')
        else:
          print(f'luckily no dishes because{dishwasher}is already washing up')""")

        self.single_level_tester(code=code, expected=expected)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_space_else(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}James Bond{q} print {q}shaken{q} else print {q}biertje!{q}""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if naam == 'James Bond':
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
        if naam == 'James \\'Bond\\'':
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_text_with_spaces_and_double_quotes_linebreak_print_else_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James "Bond"
        print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if naam == 'James "Bond"':
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_print_else_print_bengali(self):
        code = textwrap.dedent("""\
        নাম is ask 'আপনার নাম কি?'
        if নাম is হেডি print 'ভালো!' else print 'মন্দ'""")

        expected = textwrap.dedent("""\
        নাম = input(f'আপনার নাম কি?')
        if নাম == 'হেডি':
          print(f'ভালো!')
        else:
          print(f'মন্দ')""")

        self.single_level_tester(code=code, expected=expected)

    #
    # combined tests
    #
    def test_consecutive_if_statements(self):
        code = textwrap.dedent("""\
        names is Hedy, Lamar
        name is ask 'What is a name you like?'
        if name is Hedy print 'nice!'
        if name in names print 'nice!'""")

        expected = textwrap.dedent("""\
        names = ['Hedy', 'Lamar']
        name = input(f'What is a name you like?')
        if name == 'Hedy':
          print(f'nice!')
        else:
          _ = 'x'
        if name in names:
          print(f'nice!')""")

        self.single_level_tester(code=code, expected=expected, translate=False)

    def test_onno_3372(self):
        code = textwrap.dedent("""\
        antw is ask 'wat kies jij'
        if antw is schaar print 'gelijk spel!'
        print 'test'""")

        expected = textwrap.dedent("""\
        antw = input(f'wat kies jij')
        if antw == 'schaar':
          print(f'gelijk spel!')
        else:
          _ = 'x'
        print(f'test')""")

        self.single_level_tester(code=code,
                                 expected=expected,
                                 translate=False)

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
        if eten == 'friet':
          saus = input(f'Welke saus wilt u bij de friet?')
        else:
          _ = 'x'
        if eten == 'pizza':
          topping = input(f'Welke topping wilt u op de pizza?')
        else:
          _ = 'x'
        print(f'{eten}')""")

        self.single_level_tester(code=code,
                                 expected=expected,
                                 translate=False)

    def test_onno_3372_else(self):
        code = textwrap.dedent("""\
        antw is ask 'wat kies jij'
        if antw is schaar print 'gelijk spel!' else print ''
        print 'test'""")

        expected = textwrap.dedent("""\
        antw = input(f'wat kies jij')
        if antw == 'schaar':
          print(f'gelijk spel!')
        else:
          print(f'')
        print(f'test')""")

        self.single_level_tester(code=code,
                                 expected=expected,
                                 translate=False)

    def test_consecutive_if_and_if_else_statements(self):
        code = textwrap.dedent("""\
        naam is ask 'hoe heet jij?'
        if naam is Hedy print 'leuk'
        if naam is Python print 'ook leuk'
        else print 'minder leuk!'""")

        expected = textwrap.dedent("""\
        naam = input(f'hoe heet jij?')
        if naam == 'Hedy':
          print(f'leuk')
        else:
          _ = 'x'
        if naam == 'Python':
          print(f'ook leuk')
        else:
          print(f'minder leuk!')""")

        self.single_level_tester(code=code,
                                 expected=expected,
                                 translate=False)

    def test_consecutive_if_else_statements(self):
        code = textwrap.dedent("""\
        names is Hedy, Lamar
        name is ask 'What is a name you like?'
        if name is Hedy print 'nice!' else print 'meh'
        if name in names print 'nice!' else print 'meh'""")

        expected = textwrap.dedent("""\
        names = ['Hedy', 'Lamar']
        name = input(f'What is a name you like?')
        if name == 'Hedy':
          print(f'nice!')
        else:
          print(f'meh')
        if name in names:
          print(f'nice!')
        else:
          print(f'meh')""")

        self.single_level_tester(code=code, expected=expected, translate=False)

    def test_turn_if_forward(self):
        code = textwrap.dedent("""\
        angle is 90, 180, 270
        direction is angle at random
        turn direction
        if direction is 180 forward 100""")

        expected = HedyTester.dedent(
            """\
            angle = ['90', '180', '270']
            direction = random.choice(angle)""",
            HedyTester.turn_transpiled('direction', self.level),
            "if direction == '180':",
            (HedyTester.forward_transpiled(100, self.level), '  '))

        self.single_level_tester(code=code, expected=expected)

    def test_turn_if_forward_else_forward(self):
        code = textwrap.dedent("""\
        angle is 90, 180, 270
        direction is angle at random
        if direction is 180 forward direction
        else turn direction""")

        expected = HedyTester.dedent(
            """\
            angle = ['90', '180', '270']
            direction = random.choice(angle)
            if direction == '180':""",
            (HedyTester.forward_transpiled('direction', self.level), '  '),
            "else:",
            (HedyTester.turn_transpiled('direction', self.level), '  '))

        self.single_level_tester(code=code, expected=expected)

    def test_list_access_index(self):
        code = textwrap.dedent("""\
        friends is Hedy, Lola, Frida
        friend is friends at 2
        print friend""")

        expected = textwrap.dedent("""\
        friends = ['Hedy', 'Lola', 'Frida']
        friend = friends[2-1]
        print(f'{friend}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # negative tests
    #

    def test_if_indent_gives_parse_error(self):
        code = textwrap.dedent("""\
        option is ask 'Rock Paper or Scissors?'
        if option is Scissors
            print 'Its a tie!'""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            exception=hedy.exceptions.ParseException,
            extra_check_function=lambda c: c.exception.error_location[0] == 3 and c.exception.error_location[1] == 1
        )

    def test_line_with_if_with_space_gives_invalid(self):
        code = textwrap.dedent("""\
        name is Hedy
         if name is 3 print 'leuk' else print 'stom'""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidSpaceException,
            max_level=7)

    def test_pront_should_suggest_print(self):
        code = "pront 'Hedy is leuk!'"

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidCommandException,
            extra_check_function=lambda c: str(c.exception.arguments['guessed_command']) == 'print'
        )

    def test_if_equality_print_backtick_text_gives_error(self):
        code = "if 1 is 1 print `yay!` else print `nay`"

        self.multi_level_tester(
            max_level=6,
            code=code,
            exception=hedy.exceptions.UnquotedTextException
        )

    @parameterized.expand(HedyTester.quotes)
    def test_meta_column_missing_quote(self, q):
        code = textwrap.dedent(f"""\
        name is ask 'what is your name?'
        if name is Hedy print nice{q} else print {q}boo!{q}""")

        line, column = self.codeToInvalidInfo(code)

        self.assertEqual(2, line)
        self.assertEqual(23, column)

    #
    # if pressed tests
    #
    def test_if_pressed_x_is_letter_key(self):
        code = textwrap.dedent("""\
        if x is pressed print 'it is a letter key'""")

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

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_double_if_pressed(self):
        code = textwrap.dedent("""\
        if x is pressed print 'first key'
        if y is pressed print 'second key'""")

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
            if event.unicode == 'y':
              print(f'second key')
              break""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_after_pressed(self):
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

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_1_is_number_key(self):
        code = textwrap.dedent("""\
        if 1 is pressed print 'it is a number key'""")

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

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_with_trailing_spaces_after_key(self):
        code = textwrap.dedent("""\
        if x       is pressed print 'trailing spaces!'""")

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
              print(f'trailing spaces!')
              break""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    #
    # if pressed else tests
    #
    def test_if_pressed_x_else(self):
        code = textwrap.dedent("""\
        if x is pressed print 'x is pressed!' else print 'x is not pressed!'""")

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
              break""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_else(self):
        code = textwrap.dedent("""\
        if x is pressed print 'x is pressed!'
        else print 'x is not pressed!'""")

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
              break""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_both_prints_and_else(self):
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
              break""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_first_print_and_else(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'x is pressed!'
        else print 'x is not pressed!'""")

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
              break""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_second_print_and_else(self):
        code = textwrap.dedent("""\
        if x is pressed print 'x is pressed!'
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
              break""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_both_prints(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'x is pressed!'
        else print 'x is not pressed!'""")

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
                break""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    #
    # pressed turtle tests
    #
    def test_if_pressed_with_turtleforward(self):
        code = textwrap.dedent("""\
        if x is pressed forward 50""")

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
                HedyTester.forward_transpiled(50, self.level),
                14, True)
              }
              break""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=7
        )

    def test_if_pressed_with_turtleturn(self):
        code = textwrap.dedent("""\
        if x is pressed turn 90""")

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
                HedyTester.turn_transpiled(90, self.level),
                14, True)
              }
              break""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=7
        )

    def test_if_pressed_with_turtlecolor(self):
        code = textwrap.dedent("""\
        if x is pressed color red""")

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
            max_level=7
        )

    def test_if_pressed_else_with_turtle(self):
        code = textwrap.dedent("""\
        if x is pressed forward 25 else turn 90""")

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
              break""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=7
        )

    def test_if_pressed_non_latin(self):
        code = textwrap.dedent("""\
        if ض is pressed print 'arabic'
        if ש is pressed print 'hebrew'
        if й is pressed print 'russian'""")

        expected = HedyTester.dedent("""\
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'ض':
              print(f'arabic')
              break
            if event.unicode == 'ש':
              print(f'hebrew')
              break
            if event.unicode == 'й':
              print(f'russian')
              break""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    #
    # pressed negative tests
    #

    def test_if_indent_after_pressed_gives_parse_error(self):
        code = textwrap.dedent("""\
        if x is pressed
            print 'a double indent!'""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            exception=hedy.exceptions.ParseException,
            extra_check_function=lambda c: c.exception.error_location[0] == 1 and c.exception.error_location[1] == 1
        )
