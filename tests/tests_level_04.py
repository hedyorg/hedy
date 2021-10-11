import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel4(HedyTester):
  level = 4

  # invalid, ask and print should still work as in level 4
  def test_transpile_other(self):
    with self.assertRaises(hedy.InvalidCommandException) as context:
      result = hedy.transpile("abc felienne 123", self.level)
    self.assertEqual('Invalid', context.exception.error_code)

  def test_print_with_var(self):

    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet{naam}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_print_with_comma(self):

    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet,' naam""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet,{naam}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

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

  def test_transpile_turtle_basic(self):
    result = hedy.transpile("forward 50\nturn\nforward 100", self.level)
    expected = textwrap.dedent("""\
    t.forward(50)
    time.sleep(0.1)
    t.right(90)
    t.forward(100)
    time.sleep(0.1)""")
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

  def test_turtle_with_ask_has_turtle(self):
    code = textwrap.dedent("""\
    afstand is ask 'hoe ver dan?'
    forward afstand""")
    result = hedy.transpile_inner(code, self.level)
    self.assertEqual(True, result.has_turtle)

  def test_transpile_turtle_with_ask(self):
    code = textwrap.dedent("""\
    afstand is ask 'hoe ver dan?'
    forward afstand""")
    result = hedy.transpile(code, self.level)
    expected = textwrap.dedent("""\
    afstand = input('hoe ver dan?')
    t.forward(afstand)
    time.sleep(0.1)""")
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

  def test_transpile_ask_with_print(self):
    code = textwrap.dedent("""\
    kleur is ask 'wat is je lievelingskleur?'
    print 'jouw lievelingskleur is dus' kleur '!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur?')
    print(f'jouw lievelingskleur is dus{kleur}!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_transpile_ask_Spanish(self):
    code = textwrap.dedent("""\
    color is ask 'Cuál es tu color favorito?'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    color = input('Cuál es tu color favorito?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_save_list_access_to_var(self):
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

  def test_list_multiple_spaces(self):
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

  def test_print_Spanish(self):
    code = textwrap.dedent("""\
    print 'Cuál es tu color favorito?'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Cuál es tu color favorito?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  # now adds if
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


  def test_print_if_else_with_line_break(self):
    # line breaks should be allowed in if-elses until level 7 when we start with indentation

    max_level = 6
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam
    if naam is Hedy print 'leuk'
    else print 'minder leuk'""")

    for level in range(self.level, max_level + 1):
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

  def test_print_if_else_with_line_break_and_space(self):
    # line breaks should be allowed in if-elses until level 7 when we start with indentation

    max_level = 6
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam
    if naam is Hedy print 'leuk'     
    else print 'minder leuk'""")

    for level in range(self.level, max_level + 1):
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

  def test_print_if_else_with_ask(self):

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

  # steen schaar papier
  def test_print_if_else_with_and_var(self):

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

  def test_turtle_with_if_has_no_turtle(self):
    code = textwrap.dedent("""\
    jouwkeuze is schaar
    computerkeuze is schaar
    if computerkeuze is jouwkeuze print 'gelijkspel!'""")
    result = hedy.transpile_inner(code, self.level)
    self.assertEqual(False, result.has_turtle)

  def test_print_if_with_var(self):
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

  def test_if_in_array(self):
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

  def test_pront_should_suggest_print(self):
    code = "pront 'Hedy is leuk!'"

    with self.assertRaises(hedy.InvalidCommandException) as context:
      result = hedy.transpile(code, self.level)
    self.assertEqual('Invalid', context.exception.error_code)
    self.assertEqual('print', str(context.exception.arguments['guessed_command']))

  def test_parser_errors_should_be_caught_and_beautified(self):
    code = textwrap.dedent("""\
    option is ask 'Rock Paper or Scissors?'
    print 'Player 2 ' option
    if option is Scissors
        print 'Its a tie!'""")

    with self.assertRaises(hedy.ParseException) as context:
      result = hedy.transpile(code, self.level)
    self.assertEqual('Parse', context.exception.error_code)


  def test_single_quote_in_assign_should_not_break(self):
    code = """message is 'Hello welcome to Hedy.'"""
    expected = "message = '\\'Hello welcome to Hedy.\\''"

    result = hedy.transpile(code, self.level)
    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_ifelse_should_go_before_assign(self):
    maxlevel = 4
    code = textwrap.dedent("""\
    kleur is geel
    if kleur is groen antwoord is ok else antwoord is stom
    print antwoord""")

    for level in range(self.level, maxlevel+1):
      result = hedy.transpile(code, level)

      expected = textwrap.dedent("""\
      kleur = 'geel'
      if kleur == 'groen':
        antwoord = 'ok'
      else:
        antwoord = 'stom'
      print(f'{antwoord}')""")

      self.assertEqual(expected, result.code)
      self.assertEqual(False, result.has_turtle)
      print(f'{self.test_name()} level {level}')




  # while this looks STRANGE it is in essence a string issue like the one above
  # at least we solve it with the same fix of escaping quotes
  def test_bad_input_should_be_caught(self):
    code = textwrap.dedent("""\
    naam is ask 'hoe heet jij?'
    ifnaam is Hedy print 'leuk' else print 'minder leuk!'""")

    def test_transpile_other(self):
      with self.assertRaises(Exception) as context:
        result = hedy.transpile(code, self.level)
      self.assertEqual(str(context.exception), 'Invalid')


  def test_no_space_after_keyword(self):
    max_level = 22

    code = textwrap.dedent("""\
    print'test'""")

    expected = textwrap.dedent("""\
    print(f'test')""")

    self.multi_level_tester(
      code=code,
      expected=hedy.InvalidCommandException,
      exception=True,
      test_name=self.test_name()
    )

    # self.assertEqual('print', str(context.exception.arguments['guessed_command']))






  # def test_list_find_issue(self):
  #   #'list' object has no attribute 'find'
  #   # FH dd sept 2021 for later fixing!
  #   code = textwrap.dedent("""\
  #     নাম is ask আপনার নাম কি?
  #     if নাম is হেডি print 'ভালো!' else print 'মন্দ'\"""")
  #
  #
