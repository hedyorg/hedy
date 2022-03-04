import hedy, lark
import textwrap
from test_level_01 import HedyTester

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

  def test_assign_single_quote(self):
    code = """message is 'Hello welcome to Hedy.'"""
    expected = "message = '\\'Hello welcome to Hedy.\\''"
    self.single_level_tester(code=code, expected=expected)

  # if
  def test_allow_space_after_else_line(self):
    #this code has a space at the end of line 2
    code = textwrap.dedent("""\
    a is 2
    if a is 1 print a  
    else print 'nee'""")

    expected = textwrap.dedent("""\
    a = '2'
    if a == '1':
      print(f'{a}')
    else:
      print(f'nee')""")

    self.single_level_tester(
      code=code,
      expected=expected,
      expected_commands=['is', 'else', 'print', 'print']
    )
  def test_ifelse_should_go_before_assign(self):
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

    self.multi_level_tester(
      max_level=5,
      code=code,
      expected=expected
    )

  def test_identifies_backtick_inside_conditional(self):
    self.assertRaises(hedy.exceptions.UnquotedTextException, lambda: hedy.transpile("if 1 is 1 print `yay!` else print `nay`", self.level))


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
  def test_print_if_else(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam
    if naam is Hedy print 'leuk' else print 'minder leuk'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet{naam}')
    if naam == 'Hedy':
      print(f'leuk')
    else:
      print(f'minder leuk')""")

    self.single_level_tester(code=code, expected=expected)

  def test_print_if_else_ask(self):

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

  def test_print_if_else_with_line_break(self):
    # line breaks should be allowed in if-elses until level 7 when we start with indentation
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam
    if naam is Hedy print 'leuk'
    else print 'minder leuk'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet{naam}')
    if naam == 'Hedy':
      print(f'leuk')
    else:
      print(f'minder leuk')""")

    self.multi_level_tester(
      max_level=5,
      code=code,
      expected=expected
    )
  def test_print_if_else_with_line_break_after_condition(self):
    # line breaks after conditional should be allowed in if-elses until level 7 when we start with indentation
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam
    if naam is Hedy
    print 'leuk'
    else print 'minder leuk'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet{naam}')
    if naam == 'Hedy':
      print(f'leuk')
    else:
      print(f'minder leuk')""")

    self.multi_level_tester(
      max_level=5,
      code=code,
      expected=expected
    )

  def test_if_else_newline_list_assigment_print(self):
    # line breaks after conditional should be allowed in if-elses until level 7 when we start with indentation
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

    self.single_level_tester(
      code=code,
      expected=expected
    )


  def test_print_if_else_line_break_and_space(self):
    # line breaks should be allowed in if-elses until level 7 when we start with indentation

    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam
    if naam is Hedy print 'leuk'
    else print 'minder leuk'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet{naam}')
    if naam == 'Hedy':
      print(f'leuk')
    else:
      print(f'minder leuk')""")

    self.multi_level_tester(
      max_level=5,
      code=code,
      expected=expected
    )

  def test_print_if_linebreak_statement(self):
    # Breaking an if statement and its following statement should be
    # permited until level 7

    code = textwrap.dedent("""\
    people is 1, 2, 3, 3
    dishwasher is people at random
    test is 1
    if dishwasher is test
    print 'too bad I have to do the dishes!'""")

    expected = textwrap.dedent("""\
    people = ['1', '2', '3', '3']
    dishwasher = random.choice(people)
    test = '1'
    if dishwasher == test:
      print(f'too bad I have to do the dishes!')""")

    self.single_level_tester(
      code=code,
      expected=expected,
      expected_commands=['is', 'random', 'is', 'if', 'print']
    )
  def test_print_if_assign(self):
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

  def test_if_in_list(self):
    code = textwrap.dedent("""\
    items is red, green
    selected is red
    if selected in items print 'found!'""")

    expected = textwrap.dedent("""\
    items = ['red', 'green']
    selected = 'red'
    if selected in items:
      print(f'found!')""")

    #todo: whould be tested for higher levels too (FH, dec 21)
    self.single_level_tester(code=code, expected=expected, output='found!', expected_commands=['is', 'is', 'if', 'in', 'print'])

  def test_undefined_list_if_in_list(self):
    code = textwrap.dedent("""\
    selected is red
    if selected in items print 'found!'""")

    self.single_level_tester(code=code, exception=hedy.exceptions.UndefinedVarException)

  def test_unquoted_space_rhs(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is James Bond print 'shaken' else print 'biertje!'""")

    self.single_level_tester(
      code=code,
      exception=hedy.exceptions.UnquotedEqualityCheck)

  def test_unquoted_space_rhs_no_else(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is James Bond print 'shaken'""")

    self.single_level_tester(
      code=code,
      exception=hedy.exceptions.UnquotedEqualityCheck)

  def test_unquoted_space_rhs_assign(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is James Bond naam is 'Pietjansma'""")

    self.single_level_tester(
      code=code,
      exception=hedy.exceptions.UnquotedEqualityCheck)

  def test_one_space_in_rhs_if(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is 'James Bond' print 'shaken'""")

    expected = textwrap.dedent("""\
    naam = 'James'
    if naam == 'James Bond':
      print(f'shaken')""")

    self.single_level_tester(code=code, expected=expected)

  def test_multiple_spaces_in_rhs_if(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is 'Bond James Bond' print 'shaken'""")

    expected = textwrap.dedent("""\
    naam = 'James'
    if naam == 'Bond James Bond':
      print(f'shaken')""")

    self.single_level_tester(code=code, expected=expected)

  def test_one_space_in_rhs_if_else(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is 'James Bond' print 'shaken' else print 'biertje!'""")

    expected = textwrap.dedent("""\
    naam = 'James'
    if naam == 'James Bond':
      print(f'shaken')
    else:
      print(f'biertje!')""")

    self.single_level_tester(code=code, expected=expected)


  # todo would be good to make combinations with if and turtle

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

  #negative tests
  def test_indent_gives_parse_error(self):
    code = textwrap.dedent("""\
    option is ask 'Rock Paper or Scissors?'
    print 'Player 2 ' option
    if option is Scissors
        print 'Its a tie!'""")

    with self.assertRaises(hedy.exceptions.ParseException) as context:
      result = hedy.transpile(code, self.level)
    self.assertEqual('Parse', context.exception.error_code)
    self.assertEqual(4, context.exception.error_location[0])
    self.assertEqual(1, context.exception.error_location[1])

  def test_if_print_has_no_turtle(self):
    code = textwrap.dedent("""\
    jouwkeuze is schaar
    computerkeuze is schaar
    if computerkeuze is jouwkeuze print 'gelijkspel!'""")
    result = hedy.transpile_inner(code, self.level)
    self.assertEqual(False, result.has_turtle)
  def test_no_space_after_keyword_gives_missing(self):
    # todo (7-dec-21) this of course should be handled better giving an error about
    # spaces missing (maybe with repair or in the grammar?)
    code = textwrap.dedent("print'test'")

    self.multi_level_tester(
      max_level=10,
      code=code,
      exception=hedy.exceptions.MissingCommandException
    )

    #we don't have a function now for testing more exceptoion logic
    # self.assertEqual('print', str(context.exception.arguments['guessed_command']))
  def test_pront_should_suggest_print(self):
    code = "pront 'Hedy is leuk!'"

    with self.assertRaises(hedy.exceptions.InvalidCommandException) as context:
        result = hedy.transpile(code, self.level)
    self.assertEqual('Invalid', context.exception.error_code)
    self.assertEqual('print', str(context.exception.arguments['guessed_command']))

  def test_if_with_print_backtick(self):
    code = textwrap.dedent("""\
    name is ask 'ποιό είναι το όνομά σου;'
    if name is Hedy print `ωραία` else print `μπου!`""")

    self.multi_level_tester(
      max_level=5,
      code=code,
      exception=hedy.exceptions.UnquotedTextException
    )

  # def test_list_find_issue(self):
  #   #'list' object has no attribute 'find'?
  # add 'TODO' for searchability, not sure this is still a thing?
  #   # FH dd sept 2021 for later fixing!
  #   code = textwrap.dedent("""\
  #     নাম is ask আপনার নাম কি?
  #     if নাম is হেডি print 'ভালো!' else print 'মন্দ'\"""")
  #
  #

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
