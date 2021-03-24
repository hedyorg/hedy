import unittest
import hedy
import sys
import io
from contextlib import contextmanager

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
    with captured_output() as (out, err):
        exec(code)
    return out.getvalue().strip()

class TestsLevel1(unittest.TestCase):

  def test_transpile_other(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("abc felienne 123", 1)
    self.assertEqual(str(context.exception), 'Invalid')

  def test_transpile_incomplete(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("print", 1)
    self.assertEqual(str(context.exception), 'Incomplete')

  def test_transpile_incomplete_with_multiple_lines(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("print hallo allemaal\nprint", 1)
    self.assertEqual(str(context.exception), 'Incomplete')

  # def test_transpile_other_2(self):
  #   with self.assertRaises(Exception) as context:
  #     result = hedy.transpile("abc felienne 123", 1)
  #   self.assertEqual(str(context.exception), 'Invalid')
  #   self.assertEqual(str(context.exception.arguments),
  #                    "{'invalid_command': 'abc', 'level': 1, 'guessed_command': 'ask'}")

  def test_transpile_incomplete_not_a_keyword(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("groen", 1)
    self.assertEqual(str(context.exception), 'Invalid')

  def test_transpile_print(self):
    result = hedy.transpile("print Hallo welkom bij Hedy!", 1)
    self.assertEqual(result, "print('Hallo welkom bij Hedy!')")
    self.assertEqual(run_code(result), 'Hallo welkom bij Hedy!')

  def test_transpile_ask_Spanish(self):
    result = hedy.transpile("ask ask Cuál es tu color favorito?", 1)
    self.assertEqual(result, "answer = input('ask Cuál es tu color favorito?')")

  def test_lines_may_end_in_spaces(self):
    result = hedy.transpile("print Hallo welkom bij Hedy! ", 1)
    self.assertEqual(result, "print('Hallo welkom bij Hedy! ')")
    self.assertEqual(run_code(result), 'Hallo welkom bij Hedy!')

  def test_lines_may_not_start_with_spaces(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile(" print Hallo welkom bij Hedy! ", 1)
    self.assertEqual('Invalid Space', str(context.exception))

  def test_print_with_comma(self):
    result = hedy.transpile("print iedereen zegt tegen hem: NERD, omdat hij de slimste van de klas is.", 1)
    self.assertEqual(result, "print('iedereen zegt tegen hem: NERD, omdat hij de slimste van de klas is.')")

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
    self.assertEqual(result, "answer = input('wat is je lievelingskleur?')")

  def test_transpile_print_multiple_lines(self):
    result = hedy.transpile("print Hallo welkom bij Hedy\nprint Mooi hoor", 1)
    self.assertEqual(result, "print('Hallo welkom bij Hedy')\nprint('Mooi hoor')")

  def test_transpile_three_lines(self):
    input = """print Hallo
ask Wat is je lievelingskleur
echo je lievelingskleur is"""
    result = hedy.transpile(input, 1)
    self.assertEqual(result,
                     "print('Hallo')\nanswer = input('Wat is je lievelingskleur')\nprint('je lievelingskleur is'+answer)")

  def test_transpile_echo(self):
    result = hedy.transpile("echo Jouw lievelingskleur is dus...", 1)
    self.assertEqual(result, "print('Jouw lievelingskleur is dus...'+answer)")

  def test_transpile_echo_without_argument(self):
    result = hedy.transpile("echo", 1)
    self.assertEqual(result, "print(answer)")
