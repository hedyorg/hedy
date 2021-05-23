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


def run_code(code):
  code = "import random\n" + code
  with captured_output() as (out, err):
    exec(code)
  return out.getvalue().strip()


class TestsLevel2(unittest.TestCase):

  # some commands should not change:
  def test_transpile_other(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("abc felienne 123", 2)
    self.assertEqual('Invalid', str(context.exception))

  def test_transpile_echo_at_level_2(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("echo Jouw lievelingskleur is dus...", 2)
    self.assertEqual('Wrong Level', str(context.exception))

  def test_spaces_in_arguments(self):
    result = hedy.transpile("print hallo      wereld", 2)
    expected = textwrap.dedent("""\
    print('hallo'+' '+'wereld')""")

    self.assertEqual(expected, result)

  def test_transpile_print(self):
    result = hedy.transpile("print Hallo welkom bij Hedy!", 2)
    expected = textwrap.dedent("""\
    print('Hallo'+' '+'welkom'+' '+'bij'+' '+'Hedy'+'!')""")

    self.assertEqual(expected, result)


  def test_transpile_ask(self):
    result = hedy.transpile("kleur is ask wat is je lievelingskleur?", 2)

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur'+'?')""")

    self.assertEqual(expected, result)


  def test_transpile_ask_Spanish(self):
    result = hedy.transpile("color is ask ask Cuál es tu color favorito?", 2)

    expected = textwrap.dedent("""\
    color = input('ask Cuál es tu color favorito'+'?')""")

    self.assertEqual(expected, result)


  def test_transpile_ask_with_print(self):
    result = hedy.transpile("kleur is ask wat is je lievelingskleur?\nprint kleur!", 2)

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur'+'?')
    print(kleur+'!')""")

    self.assertEqual(expected, result)



  def test_transpile_print_multiple_lines(self):
    result = hedy.transpile("print Hallo welkom bij Hedy!\nprint Mooi hoor", 2)

    expected = textwrap.dedent("""\
    print('Hallo'+' '+'welkom'+' '+'bij'+' '+'Hedy'+'!')
    print('Mooi'+' '+'hoor')""")

    self.assertEqual(expected, result)

    expected_output = textwrap.dedent("""\
    Hallo welkom bij Hedy!
    Mooi hoor""")

    self.assertEqual(expected_output, run_code(result))

  def test_transpile_assign(self):
    result = hedy.transpile("naam is Felienne", 2)

    expected = textwrap.dedent("""\
    naam = 'Felienne'""")

    self.assertEqual(expected, result)

  def test_transpile_assign_2_integer(self):
    result = hedy.transpile("naam is 14", 2)

    expected = textwrap.dedent("""\
    naam = '14'""")

    self.assertEqual(expected, result)

  def test_transpile_assign_and_print(self):
    code = textwrap.dedent("""\
    naam is Felienne
    print naam""")

    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    naam = 'Felienne'
    print(naam)""")

    self.assertEqual(expected, result)


  def test_transpile_assign_and_print_more_words(self):
    code = textwrap.dedent("""\
    naam is Felienne
    print hallo naam""")

    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    naam = 'Felienne'
    print('hallo'+' '+naam)""")

    self.assertEqual(expected, result)

  def test_transpile_assign_and_print_punctuation(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print Hallo naam!""")

    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('Hallo'+' '+naam+'!')""")

    self.assertEqual(expected, result)



  def test_transpile_assign_and_print_in_sentence(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print naam is jouw voornaam""")

    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(naam+' '+'is'+' '+'jouw'+' '+'voornaam')""")

    self.assertEqual(expected, result)


  def test_transpile_assign_and_print_something_else(self):

    code = textwrap.dedent("""\
    naam is Felienne
    print Hallo""")

    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    naam = 'Felienne'
    print('Hallo')""")

    self.assertEqual(expected, result)


  def test_set_list_var(self):

    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe""")

    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']""")

    self.assertEqual(expected, result)

  def test_print_with_list_var(self):
    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print dieren at 1""")

    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(dieren[1])""")

    self.assertEqual(expected, result)

    self.assertEqual(run_code(result), "Kat")

  def test_failing_car_program(self):

    code = textwrap.dedent("""\
    naam is ask wat is de naam van de hoofdpersoon
    print naam doet mee aan een race hij krijgt een willekeurige auto""")

    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    naam = input('wat is de naam van de hoofdpersoon')
    print(naam+' '+'doet'+' '+'mee'+' '+'aan'+' '+'een'+' '+'race'+' '+'hij'+' '+'krijgt'+' '+'een'+' '+'willekeurige'+' '+'auto')""")

    self.assertEqual(expected, result)

  def test_windows_line_endings(self):

    code = textwrap.dedent("""\
    print hallo
    print allemaal""")

    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    print('hallo')
    print('allemaal')""")

    self.assertEqual(expected, result)

  def test_allow_use_of_quotes_in_print(self):
    code = "print 'Welcome to OceanView!'"
    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    print('\\'Welcome'+' '+'to'+' '+'OceanView'+'!'+' '+'\\'')""")

    self.assertEqual(expected, result)

    expected_output = run_code(result)
    self.assertEqual("'Welcome to OceanView! '", expected_output)

  def test_allow_use_of_slashes_in_print(self):
    code = "print Welcome to O/ceanView"
    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    print('Welcome'+' '+'to'+' '+'O/ceanView')""")

    self.assertEqual(expected, result)

    expected_output = run_code(result)
    self.assertEqual("Welcome to O/ceanView", expected_output)

  def test_allow_use_of_backslashes_in_print(self):
    code = "print Welcome to O\ceanView"
    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    print('Welcome'+' '+'to'+' '+'O\ceanView')""")

    self.assertEqual(expected, result)

    expected_output = run_code(result)
    self.assertEqual("Welcome to O\ceanView", expected_output)

  def test_allow_use_of_quotes_in_ask(self):
    code = "print 'Welcome to OceanView!'"
    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    print('\\'Welcome'+' '+'to'+' '+'OceanView'+'!'+' '+'\\'')""")

    self.assertEqual(expected, result)

    expected_output = run_code(result)
    self.assertEqual("'Welcome to OceanView! '", expected_output)

  def test_allow_use_of_quotes_in_echo(self):
    code = "name is ask 'What restaurant'"
    result = hedy.transpile(code, 2)

    expected = textwrap.dedent("""\
    name = input('\\'What restaurant\\'')""")

    self.assertEqual(expected, result)
