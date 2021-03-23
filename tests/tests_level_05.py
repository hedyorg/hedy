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


class TestsLevel5(unittest.TestCase):
  # print should still work
  def test_print_with_var(self):
    result = hedy.transpile("naam is Hedy\nprint 'ik heet' naam", 5)
    self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet'+naam)")

  def test_print_with_comma(self):
    result = hedy.transpile("naam is Hedy\nprint 'ik heet,' naam", 5)
    self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet,'+naam)")

  def test_print_Spanish(self):
    result = hedy.transpile("print 'Cuál es tu color favorito?'", 5)
    self.assertEqual(result, "import random\nprint('Cuál es tu color favorito?')")

  def test_transpile_ask_Spanish(self):
    result = hedy.transpile("color is ask Cuál es tu color favorito?", 5)
    self.assertEqual(result, "import random\ncolor = input('Cuál es tu color favorito?')")

  def test_transpile_other(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("abc felienne 123", 5)
    self.assertEqual(str(context.exception), 'Invalid')

  # todo: a few more things repeated from 4 here?

  # now add repeat
  def test_repeat_basic_print(self):
    result = hedy.transpile("repeat 5 times print 'me wants a cookie!'", 5)
    self.assertEqual(result, """import random
for i in range(int('5')):
  print('me wants a cookie!')""")
    self.assertEqual(run_code(result),
                     'me wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!')

  def test_repeat_with_variable_print(self):
    result = hedy.transpile("n is 5\nrepeat n times print 'me wants a cookie!'", 5)
    self.assertEqual(result, """import random
n = '5'
for i in range(int(n)):
  print('me wants a cookie!')""")
    self.assertEqual(run_code(result),
                     'me wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!')

  def test_repeat_nested_in_if(self):
    result = hedy.transpile("kleur is ask Wat is je lievelingskleur?\nif kleur is groen repeat 3 times print 'mooi!'",
                            5)
    self.assertEqual(result, """import random
kleur = input('Wat is je lievelingskleur?')
if kleur == 'groen':
  for i in range(int('3')):
    print('mooi!')""")

  def test_repeat_over_9_times(self):
    result = hedy.transpile("repeat 10 times print 'me wants a cookie!'", 5)
    self.assertEqual(result, """import random
for i in range(int('10')):
  print('me wants a cookie!')""")
    self.assertEqual(run_code(result),
                     'me wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!')
