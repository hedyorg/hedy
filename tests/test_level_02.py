import hedy
import textwrap
from parameterized import parameterized
from test_level_01 import HedyTester

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
  def test_print_comma(self):
    result = hedy.transpile("print welkom bij steen, schaar, papier", self.level)
    expected = textwrap.dedent("""\
    print(f'welkom bij steen, schaar, papier')""")

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

    self.assertEqual(expected_output, HedyTester.run_code(result))
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

    expected_output = HedyTester.run_code(result)
    self.assertEqual("'Welcome to OceanView! '", expected_output)
  def test_print_slashes(self):
    code = "print Welcome to O/ceanView"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Welcome to O/ceanView')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = HedyTester.run_code(result)
    self.assertEqual("Welcome to O/ceanView", expected_output)
  def test_print_backslashes(self):
    code = "print Welcome to O\\ceanView"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Welcome to O\\\\ceanView')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = HedyTester.run_code(result)
    self.assertEqual("Welcome to O\\ceanView", expected_output)
  def test_print_slash_end(self):
    code = "print Welcome to \\"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Welcome to \\\\')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = HedyTester.run_code(result)
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
      állatok is kutya
      print állatok""")

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

  #sleep tests
  def test_sleep_with_number(self):
    code = "sleep 1"
    expected = "time.sleep(1)"

    self.multi_level_tester(
      code=code,
      expected=expected
    )
  def test_sleep_without_number(self):
    code = "sleep"
    expected = "time.sleep(1)"

    self.multi_level_tester(
      code=code,
      expected=expected
    )

  #turn tests
  def test_turn_with_number_var(self):
    code = textwrap.dedent("""\
      direction is 70
      turn direction""")
    expected = textwrap.dedent("""\
      direction = '70'
      t.right(direction)""")
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_turn_with_string_var_gives_type_error(self):
    code = textwrap.dedent("""\
      direction is ten
      turn direction""")
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  @parameterized.expand(['left', 'right'])
  def test_one_turn_with_literal_string_gives_type_error(self, arg):
    code = f"turn {arg}"
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  # issue #792
  def test_turn_right_number_gives_type_error(self):
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code="turn right 90",
      exception=hedy.exceptions.InvalidArgumentException
    )

  #forward tests
  def test_forward_with_integer_variable(self):
    code = textwrap.dedent("""\
      a is 50
      forward a""")
    expected = textwrap.dedent("""\
      a = '50'
      t.forward(a)
      time.sleep(0.1)""")
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_forward_with_string_variable_gives_type_error(self):
    code = textwrap.dedent("""\
      a is test
      forward a""")
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )


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


  #negative tests
  def test_echo_no_longer_in_use(self):
    code = textwrap.dedent("""\
    ask what is jouw lievelingskleur?
    echo Jouw lievelingskleur is dus...""")
    with self.assertRaises(hedy.exceptions.WrongLevelException) as context:
      result = hedy.transpile(code, self.level)
    self.assertEqual('Wrong Level', context.exception.error_code)
  def test_ask_without_argument(self):
    self.multi_level_tester(
      max_level=17,
      code="name is ask",
      exception=hedy.exceptions.IncompleteCommandException
    )

  def test_ask_level_2(self):
    code = textwrap.dedent("""\
    ask is de papier goed?""")
    self.multi_level_tester(
      code=code,
      max_level=2,
      exception=hedy.exceptions.WrongLevelException
    )

  def test_chained_assignments(self):
    code = textwrap.dedent("""\
    a is dog
    b is a
    print a b""")

    expected = textwrap.dedent("""\
    a = 'dog'
    b = 'a'
    print(f'{a} {b}')""")
    self.multi_level_tester(
      max_level=3,
      code=code,
      expected=expected
    )
