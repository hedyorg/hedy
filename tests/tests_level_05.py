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


class TestsLevel5(unittest.TestCase):
  # print should still work
  def test_print_with_var(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam""")

    result = hedy.transpile(code, 5)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet'+naam)""")

    self.assertEqual(expected, result)


  def test_print_with_comma(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet,' naam""")

    result = hedy.transpile(code, 5)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet,'+naam)""")

    self.assertEqual(expected, result)

  def test_print_Spanish(self):
    code = textwrap.dedent("""\
    print 'Cuál es tu color favorito?'""")

    result = hedy.transpile(code, 5)

    expected = textwrap.dedent("""\
    print('Cuál es tu color favorito?')""")

    self.assertEqual(expected, result)

  def test_transpile_ask_Spanish(self):
    code = textwrap.dedent("""\
    color is ask Cuál es tu color favorito?""")

    result = hedy.transpile(code, 5)

    expected = textwrap.dedent("""\
    color = input('Cuál es tu color favorito?')""")

    self.assertEqual(expected, result)

  def test_transpile_other(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("abc felienne 123", 5)
    self.assertEqual(str(context.exception), 'Invalid')

  # todo: a few more things repeated from 4 here?


  # now add repeat
  def test_repeat_basic_print(self):
    code = textwrap.dedent("""\
    repeat 5 times print 'me wants a cookie!'""")

    result = hedy.transpile(code, 5)

    expected = textwrap.dedent("""\
    for i in range(int('5')):
      print('me wants a cookie!')""")

    self.assertEqual(expected, result)

    expected_output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.assertEqual(expected_output, run_code(result))


  def test_repeat_with_variable_print(self):

    code = textwrap.dedent("""\
    n is 5
    repeat n times print 'me wants a cookie!'""")

    result = hedy.transpile(code, 5)

    expected = textwrap.dedent("""\
    n = '5'
    for i in range(int(n)):
      print('me wants a cookie!')""")

    self.assertEqual(expected, result)

    expected_output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.assertEqual(expected_output, run_code(result))

  def test_repeat_nested_in_if(self):

    code = textwrap.dedent("""\
    kleur is ask Wat is je lievelingskleur?
    if kleur is groen repeat 3 times print 'mooi!'""")

    result = hedy.transpile(code, 5)

    expected = textwrap.dedent("""\
    kleur = input('Wat is je lievelingskleur?')
    if kleur == 'groen':
      for i in range(int('3')):
        print('mooi!')""")

    self.assertEqual(expected, result)

  def test_repeat_over_9_times(self):

    code = textwrap.dedent("""\
    repeat 10 times print 'me wants a cookie!'""")

    result = hedy.transpile(code, 5)

    expected = textwrap.dedent("""\
    for i in range(int('10')):
      print('me wants a cookie!')""")

    self.assertEqual(expected, result)

    expected_output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.assertEqual(expected_output, run_code(result))