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


class TestsLevel3(unittest.TestCase):
  def test_transpile_other(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("abc felienne 123", 3)
    self.assertEqual(str(context.exception), 'Invalid')

  def test_transpile_print_level_2(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("print felienne 123", 3)
      self.assertEqual(str(context), 'First word is not a command')  # hier moet nog we een andere foutmelding komen!

  def test_print(self):
    result = hedy.transpile("print 'hallo wereld!'", 3)
    self.assertEqual(result, "import random\nprint('hallo wereld!')")

  def test_print_with_comma(self):
    result = hedy.transpile("naam is Hedy\nprint 'ik heet ,'", 3)
    self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet ,')")

  def test_print_with_single_quote(self):
    result = hedy.transpile("naam is Hedy\nprint 'ik heet \\''", 3)
    self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet \\'')")

  def test_name_with_underscore(self):
    result = hedy.transpile("voor_naam is Hedy\nprint 'ik heet '", 3)
    self.assertEqual(result, "import random\nvoor_naam = 'Hedy'\nprint('ik heet ')")

  def test_name_that_is_keyword(self):
    result = hedy.transpile("for is Hedy\nprint 'ik heet ' for ", 3)
    self.assertEqual(result, "import random\n_for = 'Hedy'\nprint('ik heet '+_for)")

  def test_print_Spanish(self):
    result = hedy.transpile("print 'Cuál es tu color favorito?'", 3)
    self.assertEqual(result, "import random\nprint('Cuál es tu color favorito?')")

  def test_print_with_list_var(self):
    result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint dieren at 1", 3)
    self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(dieren[1])")
    self.assertEqual(run_code(result), "Kat")

  def test_print_with_list_var_random(self):
    result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint dieren at random", 3)
    self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(random.choice(dieren))")
    self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])

  def test_transpile_ask_Spanish(self):
    result = hedy.transpile("color is ask Cuál es tu color favorito?", 3)
    self.assertEqual(result, "import random\ncolor = input('Cuál es tu color favorito?')")

  def test_print_2(self):
    result = hedy.transpile("print 'ik heet henk'", 3)
    self.assertEqual(result, """import random
print('ik heet henk')""")

  def test_print_with_var(self):
    result = hedy.transpile("naam is Hedy\nprint 'ik heet' naam", 3)
    self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet'+naam)")

  def test_transpile_ask_with_print(self):
    result = hedy.transpile("kleur is ask wat is je lievelingskleur?\nprint 'jouw lievelingskleur is dus' kleur '!'", 3)
    self.assertEqual(result,
                     "import random\nkleur = input('wat is je lievelingskleur?')\nprint('jouw lievelingskleur is dus'+kleur+'!')")
