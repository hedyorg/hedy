import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel4(HedyTester):
  level=4

  # test/command order: ['print', 'ask', 'is', 'if', 'turn', 'forward']

  # print & ask -> no changes, covered by tests of earlier levels

  # is
  def test_assign_list_access(self):
    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    dier is dieren at random
    print dier""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    dier=random.choice(dieren)
    print(f'{dier}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertIn(self.run_code(result), ['Hond', 'Kat', 'Kangoeroe'])
  def test_assign_list_multiple_spaces(self):
    code = textwrap.dedent("""\
    dieren is Hond,  Kat,       Kangoeroe
    dier is dieren at random
    print dier""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    dier=random.choice(dieren)
    print(f'{dier}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_assign_single_quote(self):
    code = """message is 'Hello welcome to Hedy.'"""
    expected = "message = '\\'Hello welcome to Hedy.\\''"

    result = hedy.transpile(code, self.level)
    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  # if
  def test_allow_space_after_else_line(self):
    #this code has a space at the end of line 2
    code = textwrap.dedent("""\
    a is 2
    if a is 1 print a 
    else print 'nee'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    a = '2'
    if a == '1':
      print(f'{a}')
    else:
      print(f'nee')""")

    self.assertEqual(expected, result.code)
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
      max_level=4,
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  def test_identifies_backtick_inside_conditional(self):
    self.assertRaises(hedy.UnquotedTextException, lambda: hedy.transpile("if 1 is 1 print `yay!` else print `nay`", self.level))


  # turn forward
  # no new tests, covered by lower levels.

  # combined tests
  def test_turn_forward(self):
    result = hedy.transpile("forward 50\nturn\nforward 100", self.level)
    expected = textwrap.dedent("""\
    t.forward(50)
    time.sleep(0.1)
    t.right(90)
    t.forward(100)
    time.sleep(0.1)""")
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)
  def test_ask_print(self):
    code = textwrap.dedent("""\
    kleur is ask 'wat is je lievelingskleur?'
    print 'jouw lievelingskleur is dus' kleur '!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur?')
    print(f'jouw lievelingskleur is dus{kleur}!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_print_if_else(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam
    if naam is Hedy print 'leuk' else print 'minder leuk'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet{naam}')
    if naam == 'Hedy':
      print(f'leuk')
    else:
      print(f'minder leuk')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_print_if_else_ask(self):

    code = textwrap.dedent("""\
    kleur is ask 'Wat is je lievelingskleur?'
    if kleur is groen print 'mooi!' else print 'niet zo mooi'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    kleur = input('Wat is je lievelingskleur?')
    if kleur == 'groen':
      print(f'mooi!')
    else:
      print(f'niet zo mooi')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
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
      max_level=4,
      code=code,
      expected=expected,
      test_name=self.name(),
      extra_check_function=self.is_not_turtle()
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
      max_level=4,
      code=code,
      expected=expected,
      test_name=self.name(),
      extra_check_function=self.is_not_turtle()
    )
  def test_print_if_else_and_var(self):

    code = textwrap.dedent("""\
    jouwkeuze is steen
    computerkeuze is schaar
    if computerkeuze is schaar and jouwkeuze is steen print 'jij wint'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    jouwkeuze = 'steen'
    computerkeuze = 'schaar'
    if computerkeuze == 'schaar' and jouwkeuze == 'steen':
      print(f'jij wint')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertEqual(self.run_code(result), 'jij wint')
  def test_print_if_assign(self):
    code = textwrap.dedent("""\
    jouwkeuze is schaar
    computerkeuze is schaar
    if computerkeuze is jouwkeuze print 'gelijkspel!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    jouwkeuze = 'schaar'
    computerkeuze = 'schaar'
    if computerkeuze == jouwkeuze:
      print(f'gelijkspel!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertEqual(self.run_code(result), 'gelijkspel!')
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

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertEqual('found!', self.run_code(result))
  # todo would be good to make combinations with if and turtle



  #negative tests
  def test_indent_gives_parse_error(self):
    code = textwrap.dedent("""\
    option is ask 'Rock Paper or Scissors?'
    print 'Player 2 ' option
    if option is Scissors
        print 'Its a tie!'""")

    with self.assertRaises(hedy.ParseException) as context:
      result = hedy.transpile(code, self.level)
    self.assertEqual('Parse', context.exception.error_code)
  def test_if_print_has_no_turtle(self):
    code = textwrap.dedent("""\
    jouwkeuze is schaar
    computerkeuze is schaar
    if computerkeuze is jouwkeuze print 'gelijkspel!'""")
    result = hedy.transpile_inner(code, self.level)
    self.assertEqual(False, result.has_turtle)
  def test_no_space_after_keyword_gives_invalid(self):
    code = textwrap.dedent("print'test'")

    self.multi_level_tester(
      max_level=22,
      code=code,
      exception=hedy.InvalidCommandException,
      test_name=self.name()
    )

    #we don't have a function now for testing more exceptoion logic
    # self.assertEqual('print', str(context.exception.arguments['guessed_command']))
  def test_pront_should_suggest_print(self):
    code = "pront 'Hedy is leuk!'"

    with self.assertRaises(hedy.InvalidCommandException) as context:
      result = hedy.transpile(code, self.level)
    self.assertEqual('Invalid', context.exception.error_code)
    self.assertEqual('print', str(context.exception.arguments['guessed_command']))
  def test_if_with_print_backtick(self):
    code = textwrap.dedent("""\
    name is ask 'ποιό είναι το όνομά σου;'
    if name is Hedy print `ωραία` else print `μπου!`""")

    self.multi_level_tester(
      max_level=4,
      code=code,
      exception=hedy.UnquotedTextException,
      test_name=self.name()
    )

  # def test_list_find_issue(self):
  #   #'list' object has no attribute 'find'
  #   # FH dd sept 2021 for later fixing!
  #   code = textwrap.dedent("""\
  #     নাম is ask আপনার নাম কি?
  #     if নাম is হেডি print 'ভালো!' else print 'মন্দ'\"""")
  #
  #
