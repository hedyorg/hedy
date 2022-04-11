import hedy
import textwrap
from tests.Tester import HedyTester
from parameterized import parameterized

class TestsLevel5(HedyTester):
  level=5

  # test/command order: ['print', 'ask', 'is', 'if', 'turn', 'forward']

  # print & ask -> no changes, covered by tests of earlier levels

  # is

  def test_print_var_1795(self):
    code = textwrap.dedent("""\
    naam is 'Daan'
    woord1 is zomerkamp
    print 'naam' ' is naar het' 'woord1'""")

    expected = textwrap.dedent("""\
    naam = '\\'Daan\\''
    woord1 = 'zomerkamp'
    print(f'naam is naar hetwoord1')""")

    self.single_level_tester(code=code, expected=expected)

  def test_assign_list_multiple_spaces(self):
    code = textwrap.dedent("""\
    dieren is Hond,  Kat,       Kangoeroe
    dier is dieren at random
    print dier""")

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    dier = random.choice(dieren)
    print(f'{dier}')""")

    self.single_level_tester(code=code,
                             expected=expected)

  @parameterized.expand(HedyTester.quotes)
  def test_assign_quotes(self, q):
    code = f"""message is {q}Hello welcome to Hedy.{q}"""
    eq = "\\'" if q == "'" else '"'
    expected = f"message = '{eq}Hello welcome to Hedy.{eq}'"
    self.single_level_tester(code=code, expected=expected)

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

    self.single_level_tester(code=code, expected=expected)

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

  def test_if_equality_single_quoted_rhs_with_inner_double_quote(self):
    code = textwrap.dedent(f"""\
    answer is no
    if answer is 'He said "no"' print 'no'""")

    expected = textwrap.dedent(f"""\
    answer = 'no'
    if answer == 'He said "no"':
      print(f'no')""")

    self.single_level_tester(code=code, expected=expected)

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

  def test_if_equality_print_else_print_bengali(self):
    code = textwrap.dedent("""\
    নাম is ask 'আপনার নাম কি?'
    if নাম is হেডি print 'ভালো!' else print 'মন্দ'""")

    expected = textwrap.dedent("""\
    veb9b5c786e8cde0910df4197f630ee75 = input(f'আপনার নাম কি?')
    if veb9b5c786e8cde0910df4197f630ee75 == 'হেডি':
      print(f'ভালো!')
    else:
      print(f'মন্দ')""")

    self.single_level_tester(code=code, expected=expected)

  # todo would be good to make combinations with if and turtle

  # turn forward
  # no new tests, covered by lower levels.

  # combined tests
  def test_turn_forward(self):
    result = hedy.transpile("forward 50\nturn\nforward 100", self.level)
    expected = HedyTester.dedent(
      HedyTester.forward_transpiled(50),
      "t.right(90)",
      HedyTester.forward_transpiled(100))
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)
  def test_ask_print(self):
    code = textwrap.dedent("""\
    kleur is ask 'wat is je lievelingskleur?'
    print 'jouw lievelingskleur is dus' kleur '!'""")

    expected = textwrap.dedent("""\
    kleur = input(f'wat is je lievelingskleur?')
    print(f'jouw lievelingskleur is dus{kleur}!')""")

    self.single_level_tester(code=code, expected=expected)

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
    if name in names:
      print(f'nice!')""")

    self.single_level_tester(code=code, expected=expected)

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

    self.single_level_tester(code=code, expected=expected)

  #negative tests
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

  def test_meta_column_missing_quote(self):
    code = textwrap.dedent("""\
        name is ask 'what is your name?'
        if name is Hedy print nice' else print 'boo!'""")

    instance = hedy.IsValid()
    instance.level = self.level
    program_root = hedy.parse_input(code, self.level, 'en')
    is_valid = instance.transform(program_root)
    _, invalid_info = is_valid

    invalid_info = invalid_info[0]

    line = invalid_info.line
    column = invalid_info.column

    self.assertEqual(2, line)
    self.assertEqual(23, column)
