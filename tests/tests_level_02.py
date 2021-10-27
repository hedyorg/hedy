import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel2(HedyTester):
  level = 2

  # tests should be ordered as follows:
  # * commands in the order of hedy.py e..g for level 2: ['print', 'ask', 'echo', 'is', 'turn', 'forward']
  # * combined tests
  # * markup tests
  # * negative tests (inc. negative & multilevel)

  # test name conventions are like this:
  # * single keyword positive tests are just keyword or keyword_special_case
  # * multi keyword positive tests are keyword1_keywords_2
  # * negative tests should be
  # * situation_gives_exception


  #print tests
  def test_print(self):
    result = hedy.transpile("print Hallo welkom bij Hedy!", self.level)
    expected = textwrap.dedent("""\
    print(f'Hallo welkom bij Hedy!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_print_list(self):
    code = textwrap.dedent("""\
    plaatsen is een stad, een  dorp, een strand 
    print test plaatsen""")

    result = hedy.transpile(code, self.level)
    expected = textwrap.dedent("""\
    plaatsen = ['een stad', 'een  dorp', 'een strand ']
    print(f'test {plaatsen}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_print_multiple_lines(self):
    code = textwrap.dedent("""\
    print Hallo welkom bij Hedy!
    print Mooi hoor""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Hallo welkom bij Hedy!')
    print(f'Mooi hoor')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = textwrap.dedent("""\
    Hallo welkom bij Hedy!
    Mooi hoor""")

    self.assertEqual(expected_output, self.run_code(result))
  def test_print_spaces(self):
    code = "print        hallo!"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'hallo!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_print_asterisk(self):
    code = "print *Jouw* favoriet is dus kleur"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'*Jouw* favoriet is dus kleur')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_print_quotes(self):
    code = "print 'Welcome to OceanView!'"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'\\'Welcome to OceanView! \\'')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = self.run_code(result)
    self.assertEqual("'Welcome to OceanView! '", expected_output)
  def test_print_slashes(self):
    code = "print Welcome to O/ceanView"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Welcome to O/ceanView')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = self.run_code(result)
    self.assertEqual("Welcome to O/ceanView", expected_output)
  def test_print_backslashes(self):
    code = "print Welcome to O\ceanView"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Welcome to O\\\\ceanView')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = self.run_code(result)
    self.assertEqual("Welcome to O\ceanView", expected_output)
  def test_print_slash_end(self):
    code = "print Welcome to \\"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Welcome to \\\\')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = self.run_code(result)
    self.assertEqual("Welcome to \\", expected_output)

  #is tests
  def test_assign(self):
    result = hedy.transpile("naam is Felienne", self.level)

    expected = textwrap.dedent("""\
    naam = 'Felienne'""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_assign_integer(self):
    result = hedy.transpile("naam is 14", self.level)

    expected = textwrap.dedent("""\
    naam = '14'""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_assign_list(self):

    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_assign_list_exclamation_mark(self):
    code = textwrap.dedent("""\
    antwoorden is ja, NEE!, misschien
    print antwoorden at random""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    antwoorden = ['ja', 'NEE!', 'misschien']
    print(f'{random.choice(antwoorden)}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  #ask tests
  def test_ask(self):
    result = hedy.transpile("kleur is ask wat is je lievelingskleur?", self.level)

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur'+'?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_ask_quotes(self):
    code = "name is ask 'What restaurant'"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    name = input('\\'What restaurant\\'')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_ask_Spanish_text(self):
    result = hedy.transpile("color is ask ask Cuál es tu color favorito?", self.level)

    expected = textwrap.dedent("""\
    color = input('ask Cuál es tu color favorito'+'?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_ask_bengali_var(self):
    code = textwrap.dedent("""\
      রং is ask আপনার প্রিয় রং কি?
      print রং is আপনার প্রিয""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    ve1760b6272d4c9f816e62af4882d874f = input('আপনার প্রিয় রং কি'+'?')
    print(f'{ve1760b6272d4c9f816e62af4882d874f} is আপনার প্রিয')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_ask_Hungarian_var(self):
    code = textwrap.dedent("""\
      állatok is kutya, macska, kenguru
      print állatok at random""")

    result = hedy.transpile(code, self.level)
  def test_ask_with_comma(self):
    code = textwrap.dedent("""\
    dieren is ask hond, kat, kangoeroe
    print dieren""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = input('hond, kat, kangoeroe')
    print(f'{dieren}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  #turn tests
  def test_turn_number(self):
    code = textwrap.dedent("""\
    print Turtle race
    turn 90""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Turtle race')
    t.right(90)""")

    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)
  def test_turn_number_var(self):
    code = textwrap.dedent("""\
    print Turtle race
    direction is 70
    turn direction""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Turtle race')
    direction = '70'
    t.right(direction)""")

    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)


  #forward tests
  def test_forward_without_argument(self):
    code = textwrap.dedent("""\
    forward""")
    result = hedy.transpile(code, self.level)
    expected = textwrap.dedent("""\
    t.forward(50)
    time.sleep(0.1)""")

    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

  #markup tests
  def test_spaces_in_arguments(self):
    result = hedy.transpile("print hallo      wereld", self.level)
    expected = textwrap.dedent("""\
    print(f'hallo wereld')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  #combined tests
  def test_ask_print(self):
    result = hedy.transpile("kleur is ask wat is je lievelingskleur?\nprint kleur!", self.level)

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur'+'?')
    print(f'{kleur}!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_assign_print(self):
    code = textwrap.dedent("""\
    naam is Felienne
    print naam""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Felienne'
    print(f'{naam}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_forward_ask(self):
    code = textwrap.dedent("""\
    afstand is ask hoe ver dan?
    forward afstand""")
    result = hedy.transpile(code, self.level)
    expected = textwrap.dedent("""\
    afstand = input('hoe ver dan'+'?')
    t.forward(afstand)
    time.sleep(0.1)""")
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)
  def test_turn_ask(self):
    code = textwrap.dedent("""\
    print Turtle race
    direction is ask Where to turn?
    turn direction""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Turtle race')
    direction = input('Where to turn'+'?')
    t.right(direction)""")

    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)
  def test_random_turn(self):
    code = textwrap.dedent("""\
    print Turtle race
    directions is 10, 100, 360
    turn directions at random""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Turtle race')
    directions = ['10', '100', '360']
    t.right(random.choice(directions))""")

    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)
  def test_print_list_random(self):
    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print dieren at random""")

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(f'{random.choice(dieren)}')""")

    # check if result is in the expected list
    check_in_list = (lambda x: self.run_code(x) in ['Hond', 'Kat', 'Kangoeroe'])

    self.multi_level_tester(
      max_level=11,
      code=code,
      expected=expected,
      extra_check_function=check_in_list,
      test_name=self.name()
    )
  def test_assign_print_punctuation(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print Hallo naam!""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'Hallo {naam}!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_assign_print_sentence(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print naam is jouw voornaam""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'{naam} is jouw voornaam')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_assign_print_something_else(self):

    code = textwrap.dedent("""\
    naam is Felienne
    print Hallo""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Felienne'
    print(f'Hallo')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_print_list_var(self):
    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print dieren at 1""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(f'{dieren[1]}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    self.assertEqual(self.run_code(result), "Kat")

  #negative tests
  def test_echo(self):
    code = textwrap.dedent("""\
    ask what is jouw lievelingskleur?
    echo Jouw lievelingskleur is dus...""")
    with self.assertRaises(hedy.WrongLevelException) as context:
      result = hedy.transpile(code, self.level)
    self.assertEqual('Wrong Level', context.exception.error_code)
  def test_ask_without_argument_upto_22(self):
    self.multi_level_tester(
      code="name is ask",
      max_level=10,
      exception=hedy.IncompleteCommandException,
      test_name=self.name()
    )

  # test for 297 (not easy to fix, not giving prio now)
  # def test_print_space_after_excl(self):
  #   code = "print hello world!koekie!"
  #   result = hedy.transpile(code, self.level)
  #
  #   expected = textwrap.dedent("""\
  #   print('hello'+' '+'world'+'!'+'koekie'+'!')""")
  #
  #   self.assertEqual(expected, result.code)
  #   self.assertEqual(False, result.has_turtle)

