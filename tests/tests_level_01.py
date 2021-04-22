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

class TestsLevel1(unittest.TestCase):

  def test_transpile_other(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("abc felienne 123", 1)
    self.assertEqual('Invalid', str(context.exception))

  def test_transpile_incomplete(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("print", 1)
    self.assertEqual('Incomplete', str(context.exception))

  def test_transpile_incomplete_with_multiple_lines(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("print hallo allemaal\nprint", 1)
    self.assertEqual('Incomplete', str(context.exception))

  # def test_transpile_other_2(self):
  #   with self.assertRaises(Exception) as context:
  #     result = hedy.transpile("abc felienne 123", 1)
  #   self.assertEqual(str(context.exception), 'Invalid')
  #   self.assertEqual(str(context.exception.arguments),
  #                    "{'invalid_command': 'abc', 'level': 1, 'guessed_command': 'ask'}")

  def test_transpile_incomplete_not_a_keyword(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("groen", 1)
    self.assertEqual('Invalid', str(context.exception))

  def test_transpile_print(self):
    result = hedy.transpile("print Hallo welkom bij Hedy!", 1)
    self.assertEqual("print('Hallo welkom bij Hedy!')", result)
    self.assertEqual('Hallo welkom bij Hedy!', run_code(result))

  def test_transpile_ask_Spanish(self):
    result = hedy.transpile("ask ask Cuál es tu color favorito?", 1)
    self.assertEqual("answer = input('ask Cuál es tu color favorito?')", result)

  def test_lines_may_end_in_spaces(self):
    result = hedy.transpile("print Hallo welkom bij Hedy! ", 1)
    self.assertEqual("print('Hallo welkom bij Hedy! ')", result)
    self.assertEqual('Hallo welkom bij Hedy!', run_code(result))

  def test_lines_may_not_start_with_spaces(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile(" print Hallo welkom bij Hedy! ", 1)
    self.assertEqual('Invalid Space', str(context.exception))

  def test_print_with_comma(self):
    result = hedy.transpile("print iedereen zegt tegen hem: NERD, omdat hij de slimste van de klas is.", 1)
    self.assertEqual("print('iedereen zegt tegen hem: NERD, omdat hij de slimste van de klas is.')", result)

  def test_word_plus_period(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("word.", 1)
    self.assertEqual('Invalid', str(context.exception))

  def test_two_lines_start_with_spaces(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile(" print Hallo welkom bij Hedy!\n print Hallo welkom bij Hedy!", 1)
    self.assertEqual('Invalid Space', str(context.exception))

  def test_transpile_empty(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("", 1)

  def test_transpile_ask(self):
    result = hedy.transpile("ask wat is je lievelingskleur?", 1)
    self.assertEqual("answer = input('wat is je lievelingskleur?')", result)

  def test_transpile_print_multiple_lines(self):
    result = hedy.transpile("print Hallo welkom bij Hedy\nprint Mooi hoor", 1)
    self.assertEqual("print('Hallo welkom bij Hedy')\nprint('Mooi hoor')", result)

  def test_transpile_three_lines(self):
    input = textwrap.dedent("""\
    print Hallo
    ask Wat is je lievelingskleur
    echo je lievelingskleur is""")

    expected = textwrap.dedent("""\
    print('Hallo')
    answer = input('Wat is je lievelingskleur')
    print('je lievelingskleur is'+answer)""")

    result = hedy.transpile(input, 1)
    self.assertEqual(expected, result)
                     
  def test_transpile_echo(self):
    result = hedy.transpile("echo Jouw lievelingskleur is dus...", 1)
    self.assertEqual("print('Jouw lievelingskleur is dus...'+answer)", result)

  def test_transpile_echo_without_argument(self):
    result = hedy.transpile("echo", 1)
    self.assertEqual("print(answer)", result)

  def test_use_quotes_in_print_allowed(self):
    code = "print 'Welcome to OceanView!'"
    result = hedy.transpile(code, 1)

    expected = textwrap.dedent("""\
    print('\\'Welcome to OceanView!\\'')""")

    self.assertEqual(expected, result)

    expected_output = run_code(result)
    self.assertEqual("'Welcome to OceanView!'", expected_output)

  def test_use_slashes_in_print_allowed(self):
    code = "print 'Welcome to \O/ceanView!'"
    result = hedy.transpile(code, 1)

    expected = textwrap.dedent("""\
    print('\\'Welcome to \O/ceanView!\\'')""")

    self.assertEqual(expected, result)

    expected_output = run_code(result)
    self.assertEqual("'Welcome to \O/ceanView!'", expected_output)

  def test_use_quotes_in_ask_allowed(self):
    code = "ask 'Welcome to OceanView?'"
    result = hedy.transpile(code, 1)

    expected = textwrap.dedent("""\
    answer = input('\\'Welcome to OceanView?\\'')""")

    self.assertEqual(expected, result)

  def test_use_quotes_in_echo_allowed(self):
    code = "echo oma's aan de"
    result = hedy.transpile(code, 1)

    expected = textwrap.dedent("""\
    print('oma\\'s aan de'+answer)""")

    self.assertEqual(expected, result)
