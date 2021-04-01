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


class TestsLevel6(unittest.TestCase):
  def test_print_with_var(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam""")

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet'+str(naam))""")

    self.assertEqual(expected, result)


  def test_transpile_ask(self):
    code = textwrap.dedent("""\
    antwoord is ask wat is je lievelingskleur?""")

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""\
    antwoord = input('wat is je lievelingskleur?')""")

    self.assertEqual(expected, result)

  def test_repeat_nested_in_if(self):

    code = textwrap.dedent("""\
    kleur is ask Wat is je lievelingskleur?
    if kleur is groen repeat 3 times print 'mooi!'""")

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""\
    kleur = input('Wat is je lievelingskleur?')
    if str(kleur) == str('groen'):
      for i in range(int('3')):
        print('mooi!')""")

    self.assertEqual(expected, result)

  def test_repeat_with_variable_print(self):
    code = textwrap.dedent("""\
    n is 5
    repeat n times print 'me wants a cookie!'""")

    result = hedy.transpile(code, 6)

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

  # new tests for calculations
  def test_simple_calculation(self):
    code = "nummer is 4 + 5"
    result = hedy.transpile(code, 6)

    expected = "nummer = int(4) + int(5)"
    self.assertEqual(expected, result)

  def test_simple_calculation_without_space(self):
    code = "nummer is 4+5"
    result = hedy.transpile(code, 6)

    expected = "nummer = int(4) + int(5)"
    self.assertEqual(expected, result)


  def test_calculation_and_printing(self):

    code = textwrap.dedent("""\
    nummer is 4 + 5
    print nummer""")

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""\
    nummer = int(4) + int(5)
    print(str(nummer))""")

    self.assertEqual(expected, result)
    self.assertEqual("9", run_code(result))

  def test_calculation_with_vars(self):
    code = textwrap.dedent("""\
    nummer is 5
    nummertwee is 6
    getal is nummer * nummertwee
    print getal""")

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    getal = int(nummer) * int(nummertwee)
    print(str(getal))""")

    self.assertEqual(expected, result)
    self.assertEqual("30", run_code(result))

  def test_print_calculation_times_directly(self):
    code = textwrap.dedent("""\
    nummer is 5
    nummertwee is 6
    print nummer * nummertwee""")

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    print(str(int(nummer) * int(nummertwee)))""")

    self.assertEqual(expected, result)
    self.assertEqual("30", run_code(result))

  def test_print_calculation_divide_directly(self):
    code = textwrap.dedent("""\
    nummer is 5
    nummertwee is 6
    print nummer / nummertwee""")

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    print(str(int(nummer) // int(nummertwee)))""")

    self.assertEqual(expected, result)
    self.assertEqual("0", run_code(result))