import hedy
import textwrap
from parameterized import parameterized
from Tester import HedyTester

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
    code = "print Hallo welkom bij Hedy!"
    expected = textwrap.dedent("""\
    print(f'Hallo welkom bij Hedy!')""")
    self.single_level_tester(code=code, expected=expected)

  def test_print_comma(self):
    code = "print welkom bij steen, schaar, papier"
    expected = textwrap.dedent("""\
    print(f'welkom bij steen, schaar, papier')""")

    self.single_level_tester(code=code, expected=expected)

  def test_print_multiple_lines(self):
    code = textwrap.dedent("""\
    print Hallo welkom bij Hedy!
    print Mooi hoor""")

    expected = textwrap.dedent("""\
    print(f'Hallo welkom bij Hedy!')
    print(f'Mooi hoor')""")

    output = textwrap.dedent("""\
    Hallo welkom bij Hedy!
    Mooi hoor""")

    self.single_level_tester(code=code, expected=expected, output=output)
  def test_print_spaces(self):
    code = "print        hallo!"
    expected = textwrap.dedent("""\
    print(f'hallo!')""")

    self.single_level_tester(code=code, expected=expected)
  def test_print_asterisk(self):
    code = "print *Jouw* favoriet is dus kleur"
    expected = textwrap.dedent("""\
    print(f'*Jouw* favoriet is dus kleur')""")

    self.single_level_tester(code=code, expected=expected)
  def test_print_quotes(self):
    code = "print 'Welcome to OceanView!'"
    expected = textwrap.dedent("""\
    print(f'\\'Welcome to OceanView! \\'')""")
    self.single_level_tester(code=code, expected=expected)

  def test_print_slashes(self):
    code = "print Welcome to O/ceanView"
    expected = textwrap.dedent("""\
    print(f'Welcome to O/ceanView')""")

    self.single_level_tester(code=code, expected=expected)
  def test_print_backslashes(self):
    code = "print Welcome to O\\ceanView"
    expected = textwrap.dedent("""\
    print(f'Welcome to O\\\\ceanView')""")

    output = "Welcome to O\\ceanView"

    self.single_level_tester(code=code, expected=expected, output=output)
  def test_print_slash_end(self):
    code = "print Welcome to \\"
    expected = textwrap.dedent("""\
    print(f'Welcome to \\\\')""")

    output = "Welcome to \\"

    self.single_level_tester(code=code, expected=expected, output=output)
  #is tests
  def test_assign(self):
    code = "naam is Felienne"

    expected = textwrap.dedent("""\
    naam = 'Felienne'""")

    self.single_level_tester(code=code, expected=expected)
  def test_assign_integer(self):
    code = "naam is 14"

    expected = textwrap.dedent("""\
    naam = '14'""")

    self.single_level_tester(code=code, expected=expected)

  #ask tests
  def test_ask(self):
    code = "kleur is ask wat is je lievelingskleur?"

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur'+'?')""")

    self.single_level_tester(code=code, expected=expected)
  def test_ask_quotes(self):
    code = "name is ask 'What restaurant'"
    expected = textwrap.dedent("""\
    name = input('\\'What restaurant\\'')""")

    self.single_level_tester(code=code, expected=expected)
  def test_ask_Spanish_text(self):
    code = "color is ask ask Cuál es tu color favorito?"
    expected = textwrap.dedent("""\
    color = input('ask Cuál es tu color favorito'+'?')""")

    self.single_level_tester(code=code, expected=expected)
  def test_ask_bengali_var(self):
    code = textwrap.dedent("""\
      রং is ask আপনার প্রিয় রং কি?
      print রং is আপনার প্রিয""")

    expected = textwrap.dedent("""\
    ve1760b6272d4c9f816e62af4882d874f = input('আপনার প্রিয় রং কি'+'?')
    print(f'{ve1760b6272d4c9f816e62af4882d874f} is আপনার প্রিয')""")

    self.single_level_tester(code=code, expected=expected)
  def test_ask_Hungarian_var(self):
    code = textwrap.dedent("""\
      állatok is kutya
      print állatok""")

    expected = textwrap.dedent("""\
    v79de0191e90551f058d466c5e8c267ff = 'kutya'
    print(f'{v79de0191e90551f058d466c5e8c267ff}')""")

    self.single_level_tester(code=code, expected=expected)
  def test_ask_with_comma(self):
    code = textwrap.dedent("""\
    dieren is ask hond, kat, kangoeroe
    print dieren""")

    expected = textwrap.dedent("""\
    dieren = input('hond, kat, kangoeroe')
    print(f'{dieren}')""")

    self.single_level_tester(code=code, expected=expected)

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
    expected = HedyTester.dedent(
      "direction = '70'",
      HedyTester.turn_transpiled('direction'))
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_turn_number(self):
    code = "turn 180"
    expected = HedyTester.turn_transpiled(180)
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_turn_negative_number(self):
    code = "turn -180"
    expected = HedyTester.turn_transpiled(-180)
    self.multi_level_tester(
      max_level=10,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_one_turn_with_text_gives_type_error(self):
    code = "turn koekoek"
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
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

  def test_turn_with_non_ascii_var(self):
    code = textwrap.dedent("""\
      ángulo is 90
      turn ángulo""")
    expected = HedyTester.dedent(
      "vefd88f42b64136f16e8f305dd375a921 = '90'",
      HedyTester.turn_transpiled('vefd88f42b64136f16e8f305dd375a921'))
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle(),
      expected_commands=['is', 'turn']
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
    expected = HedyTester.dedent(
      "a = '50'",
      HedyTester.forward_transpiled('a'))
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
    code = "print hallo      wereld"
    expected = textwrap.dedent("""\
    print(f'hallo wereld')""")

    self.single_level_tester(code=code, expected=expected)

  #combined tests
  def test_ask_print(self):
    code = "kleur is ask wat is je lievelingskleur?\nprint kleur!"
    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur'+'?')
    print(f'{kleur}!')""")

    self.single_level_tester(code=code, expected=expected)
  def test_assign_print(self):
    code = textwrap.dedent("""\
    naam is Felienne
    print naam""")
    expected = textwrap.dedent("""\
    naam = 'Felienne'
    print(f'{naam}')""")

    self.single_level_tester(code=code, expected=expected)

  def test_forward_ask(self):
    code = textwrap.dedent("""\
      afstand is ask hoe ver dan?
      forward afstand""")

    expected = HedyTester.dedent(
      "afstand = input('hoe ver dan'+'?')",
      HedyTester.forward_transpiled('afstand'))
    self.single_level_tester(code=code, expected=expected, extra_check_function=self.is_turtle())

  def test_turn_ask(self):
    code = textwrap.dedent("""\
      print Turtle race
      direction is ask Where to turn?
      turn direction""")

    expected = HedyTester.dedent("""\
      print(f'Turtle race')
      direction = input('Where to turn'+'?')""",
      HedyTester.turn_transpiled('direction'))

    self.single_level_tester(code=code, expected=expected, extra_check_function=self.is_turtle())
  def test_assign_print_punctuation(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print Hallo naam!""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'Hallo {naam}!')""")

    self.single_level_tester(code=code, expected=expected)
  def test_assign_print_sentence(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print naam is jouw voornaam""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'{naam} is jouw voornaam')""")

    self.single_level_tester(code=code, expected=expected)
  def test_assign_print_something_else(self):

    code = textwrap.dedent("""\
    naam is Felienne
    print Hallo""")

    expected = textwrap.dedent("""\
    naam = 'Felienne'
    print(f'Hallo')""")

    self.single_level_tester(code=code, expected=expected)


  #negative tests
  def test_echo_no_longer_in_use(self):
    code = textwrap.dedent("""\
    ask what is jouw lievelingskleur?
    echo Jouw lievelingskleur is dus...""")
    with self.assertRaises(hedy.exceptions.WrongLevelException) as context:
      hedy.transpile(code, self.level)
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
