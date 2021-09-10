import unittest
import hedy
import sys
import io
from contextlib import contextmanager
import textwrap

@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def run_code(parse_result):
  code = "import random\n" + parse_result.code
  with captured_output() as (out, err):
    exec(code)
  return out.getvalue().strip()

class TestsLevel2(unittest.TestCase):
  level = 2

  # some commands should not change:
  def test_transpile_other(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("abc felienne 123", self.level)
    self.assertEqual('Invalid', str(context.exception))

  def test_transpile_echo_at_level_2(self):
    code = textwrap.dedent("""\
    ask what is jouw lievelingskleur?
    echo Jouw lievelingskleur is dus...""")
    with self.assertRaises(Exception) as context:
      result = hedy.transpile(code, self.level)
    self.assertEqual('Wrong Level', str(context.exception))

  def test_spaces_in_arguments(self):
    result = hedy.transpile("print hallo      wereld", self.level)
    expected = textwrap.dedent("""\
    print('hallo'+' '+'wereld')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_transpile_print(self):
    result = hedy.transpile("print Hallo welkom bij Hedy!", self.level)
    expected = textwrap.dedent("""\
    print('Hallo'+' '+'welkom'+' '+'bij'+' '+'Hedy'+'!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_transpile_ask(self):
    result = hedy.transpile("kleur is ask wat is je lievelingskleur?", self.level)

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur'+'?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_transpile_ask_Spanish(self):
    result = hedy.transpile("color is ask ask Cuál es tu color favorito?", self.level)

    expected = textwrap.dedent("""\
    color = input('ask Cuál es tu color favorito'+'?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_transpile_ask_with_print(self):
    result = hedy.transpile("kleur is ask wat is je lievelingskleur?\nprint kleur!", self.level)

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur'+'?')
    print(kleur+'!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)



  def test_transpile_print_multiple_lines(self):
    result = hedy.transpile("print Hallo welkom bij Hedy!\nprint Mooi hoor", self.level)

    expected = textwrap.dedent("""\
    print('Hallo'+' '+'welkom'+' '+'bij'+' '+'Hedy'+'!')
    print('Mooi'+' '+'hoor')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = textwrap.dedent("""\
    Hallo welkom bij Hedy!
    Mooi hoor""")

    self.assertEqual(expected_output, run_code(result))

  def test_transpile_turtle_basic(self):
    result = hedy.transpile("forward 50\nturn\nforward 100", self.level)
    expected = textwrap.dedent("""\
    t.forward(50)
    t.right(90)
    t.forward(100)""")
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

  def test_transpile_turtle_with_ask(self):
    code = textwrap.dedent("""\
    afstand is ask hoe ver dan?
    forward afstand""")
    result = hedy.transpile(code, self.level)
    expected = textwrap.dedent("""\
    afstand = input('hoe ver dan'+'?')
    t.forward(afstand)""")
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

  def test_transpile_assign(self):
    result = hedy.transpile("naam is Felienne", self.level)

    expected = textwrap.dedent("""\
    naam = 'Felienne'""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_transpile_assign_2_integer(self):
    result = hedy.transpile("naam is 14", self.level)

    expected = textwrap.dedent("""\
    naam = '14'""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_transpile_assign_and_print(self):
    code = textwrap.dedent("""\
    naam is Felienne
    print naam""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Felienne'
    print(naam)""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_transpile_assign_and_print_more_words(self):
    code = textwrap.dedent("""\
    naam is Felienne
    print hallo naam""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Felienne'
    print('hallo'+' '+naam)""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_transpile_assign_and_print_punctuation(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print Hallo naam!""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('Hallo'+' '+naam+'!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)



  def test_transpile_assign_and_print_in_sentence(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print naam is jouw voornaam""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(naam+' '+'is'+' '+'jouw'+' '+'voornaam')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_transpile_assign_and_print_something_else(self):

    code = textwrap.dedent("""\
    naam is Felienne
    print Hallo""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Felienne'
    print('Hallo')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_set_list_var(self):

    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_print_with_list_var(self):
    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print dieren at 1""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(dieren[1])""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    self.assertEqual(run_code(result), "Kat")

  def test_failing_car_program(self):

    code = textwrap.dedent("""\
    naam is ask wat is de naam van de hoofdpersoon
    print naam doet mee aan een race hij krijgt een willekeurige auto""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = input('wat is de naam van de hoofdpersoon')
    print(naam+' '+'doet'+' '+'mee'+' '+'aan'+' '+'een'+' '+'race'+' '+'hij'+' '+'krijgt'+' '+'een'+' '+'willekeurige'+' '+'auto')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_windows_line_endings(self):

    code = textwrap.dedent("""\
    print hallo
    print allemaal""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('hallo')
    print('allemaal')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_allow_use_of_quotes_in_print(self):
    code = "print 'Welcome to OceanView!'"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('\\'Welcome'+' '+'to'+' '+'OceanView'+'!'+' '+'\\'')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = run_code(result)
    self.assertEqual("'Welcome to OceanView! '", expected_output)

  def test_allow_use_of_slashes_in_print(self):
    code = "print Welcome to O/ceanView"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('Welcome'+' '+'to'+' '+'O/ceanView')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = run_code(result)
    self.assertEqual("Welcome to O/ceanView", expected_output)

  def test_allow_use_of_backslashes_in_print(self):
    code = "print Welcome to O\ceanView"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('Welcome'+' '+'to'+' '+'O\ceanView')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = run_code(result)
    self.assertEqual("Welcome to O\ceanView", expected_output)

  def test_allow_use_of_quotes_in_ask(self):
    code = "print 'Welcome to OceanView!'"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('\\'Welcome'+' '+'to'+' '+'OceanView'+'!'+' '+'\\'')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = run_code(result)
    self.assertEqual("'Welcome to OceanView! '", expected_output)

  def test_allow_use_of_quotes_in_echo(self):
    code = "name is ask 'What restaurant'"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    name = input('\\'What restaurant\\'')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_allow_hungarian_vars(self):
    code = textwrap.dedent("""\
      állatok is kutya, macska, kenguru
      print állatok at random""")

    result = hedy.transpile(code, self.level)

  def test_ask_bengali_vars(self):
    code = textwrap.dedent("""\
      রং is ask আপনার প্রিয় রং কি?
      print রং is আপনার প্রিয""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    ve1760b6272d4c9f816e62af4882d874f = input('আপনার প্রিয় রং কি'+'?')
    print(ve1760b6272d4c9f816e62af4882d874f+' '+'is'+' '+'আপনার'+' '+'প্রিয')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_two_spaces_after_print(self):
    code = "print        hallo!"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('hallo'+'!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_print_asterisk(self):
    code = "print *Jouw* favoriet is dus kleur"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('*Jouw*'+' '+'favoriet'+' '+'is'+' '+'dus'+' '+'kleur')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_turn_number(self):
    code = textwrap.dedent("""\
    print Turtle race
    turn 90""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('Turtle'+' '+'race')
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
    print('Turtle'+' '+'race')
    direction = '70'
    t.right(direction)""")

    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

  def test_turn_ask(self):
    code = textwrap.dedent("""\
    print Turtle race
    direction is ask Where to turn?
    turn direction""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('Turtle'+' '+'race')
    direction = input('Where to turn'+'?')
    t.right(direction)""")

    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

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

