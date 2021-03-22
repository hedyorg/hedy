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


class TestsLevel2(unittest.TestCase):

  # some commands should not change:
  def test_transpile_other(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("abc felienne 123", 2)
    self.assertEqual(str(context.exception), 'Invalid')

  def test_transpile_ask_Spanish(self):
    result = hedy.transpile("ask ask Cuál es tu color favorito?", 2)
    self.assertEqual(result, "answer = input('ask Cuál es tu color favorito?')")

  def test_transpile_echo_at_level_2(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("echo Jouw lievelingskleur is dus...", 2)
    self.assertEqual(str(context.exception), 'Wrong Level')

  def test_spaces_in_arguments(self):
    result = hedy.transpile("print hallo      wereld", 2)
    self.assertEqual(result, "import random\nprint('hallo'+' '+'wereld')")

  def test_transpile_print(self):
    result = hedy.transpile("print Hallo welkom bij Hedy!", 2)
    self.assertEqual(result, "import random\nprint('Hallo'+' '+'welkom'+' '+'bij'+' '+'Hedy'+'!')")

  def test_transpile_ask(self):
    result = hedy.transpile("kleur is ask wat is je lievelingskleur?", 2)
    self.assertEqual(result, "import random\nkleur = input('wat is je lievelingskleur'+'?')")

  def test_transpile_ask_Spanish(self):
    result = hedy.transpile("color is ask ask Cuál es tu color favorito?", 2)
    self.assertEqual(result, "import random\ncolor = input('ask Cuál es tu color favorito'+'?')")

  def test_transpile_ask_with_print(self):
    result = hedy.transpile("kleur is ask wat is je lievelingskleur?\nprint kleur!", 2)
    self.assertEqual(result, "import random\nkleur = input('wat is je lievelingskleur'+'?')\nprint(kleur+'!')")

  def test_transpile_print_multiple_lines(self):
    result = hedy.transpile("print Hallo welkom bij Hedy!\nprint Mooi hoor", 2)
    self.assertEqual(result,
                     "import random\nprint('Hallo'+' '+'welkom'+' '+'bij'+' '+'Hedy'+'!')\nprint('Mooi'+' '+'hoor')")
    self.assertEqual(run_code(result), "Hallo welkom bij Hedy!\nMooi hoor")

  def test_transpile_assign(self):
    result = hedy.transpile("naam is Felienne", 2)
    self.assertEqual(result, "import random\nnaam = 'Felienne'")

  def test_transpile_assign_2_integer(self):
    result = hedy.transpile("naam is 14", 2)
    self.assertEqual(result, "import random\nnaam = '14'")

  def test_transpile_assign_and_print(self):
    result = hedy.transpile("naam is Felienne\nprint naam", 2)
    self.assertEqual(result, "import random\nnaam = 'Felienne'\nprint(naam)")

  def test_transpile_assign_and_print_more_words(self):
    result = hedy.transpile("naam is Felienne\nprint hallo naam", 2)
    self.assertEqual(result, "import random\nnaam = 'Felienne'\nprint('hallo'+' '+naam)")

  def test_transpile_assign_and_print_punctuation(self):
    result = hedy.transpile("naam is Hedy\nprint Hallo naam!", 2)
    self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('Hallo'+' '+naam+'!')")

  def test_transpile_assign_and_print_in_sentence(self):
    result = hedy.transpile("naam is Hedy\nprint naam is jouw voornaam", 2)
    self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint(naam+' '+'is'+' '+'jouw'+' '+'voornaam')")

  def test_transpile_assign_and_print_something_else(self):
    result = hedy.transpile("naam is Felienne\nprint Hallo", 2)
    self.assertEqual(result, "import random\nnaam = 'Felienne'\nprint('Hallo')")

  def test_set_list_var(self):
    result = hedy.transpile("dieren is Hond, Kat, Kangoeroe", 2)
    self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']")

  def test_print_with_list_var(self):
    result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint dieren at 1", 2)
    self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(dieren[1])")
    self.assertEqual(run_code(result), "Kat")

  def test_failing_car_program(self):
    # note: this the right order for assert: expected, actual
    result = hedy.transpile("""naam is ask wat is de naam van de hoofdpersoon
print naam doet mee aan een race hij krijgt een willekeurige auto""", 2)
    self.assertEqual(
      "import random\nnaam = input('wat is de naam van de hoofdpersoon')\nprint(naam+' '+'doet'+' '+'mee'+' '+'aan'+' '+'een'+' '+'race'+' '+'hij'+' '+'krijgt'+' '+'een'+' '+'willekeurige'+' '+'auto')",
      result)

  def test_windows_line_endings(self):
    result = hedy.transpile("print hallo\r\nprint allemaal", 2)
    self.assertEqual("import random\nprint('hallo')\nprint('allemaal')", result)
