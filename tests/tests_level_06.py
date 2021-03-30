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
    result = hedy.transpile("naam is Hedy\nprint 'ik heet' naam", 6)
    self.assertEqual("import random\nnaam = 'Hedy'\nprint('ik heet'+str(naam))", result)
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""
    """)

    self.assertEqual(expected, result)


  def test_transpile_ask(self):
    result = hedy.transpile("antwoord is ask wat is je lievelingskleur?", 6)
    self.assertEqual(result, "import random\nantwoord = input('wat is je lievelingskleur?')")
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""
    """)

    self.assertEqual(expected, result)

  def test_repeat_nested_in_if(self):
    result = hedy.transpile("kleur is ask Wat is je lievelingskleur?\nif kleur is groen repeat 3 times print 'mooi!'",
                            6)
    self.assertEqual(result, """import random
kleur = input('Wat is je lievelingskleur?')
if str(kleur) == str('groen'):
  for i in range(int('3')):
    print('mooi!')""")
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""
    """)

    self.assertEqual(expected, result)

  def test_repeat_with_variable_print(self):
    result = hedy.transpile("n is 5\nrepeat n times print 'me wants a cookie!'", 6)
    self.assertEqual(result, """import random
n = '5'
for i in range(int(n)):
  print('me wants a cookie!')""")
    self.assertEqual(run_code(result),
                     'me wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!')
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""
    """)

    self.assertEqual(expected, result)

  # new tests for calculations
  def test_simple_calculation(self):
    result = hedy.transpile("nummer is 4 + 5", 6)
    self.assertEqual('import random\nnummer = int(4) + int(5)', result)
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""
    """)

    self.assertEqual(expected, result)

  def test_simple_calculation(self):
    result = hedy.transpile("nummer is 4+5", 6)
    self.assertEqual('import random\nnummer = int(4) + int(5)', result)
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""
    """)

    self.assertEqual(expected, result)

  def test_calculation_and_printing(self):
    result = hedy.transpile("nummer is 4 + 5\nprint nummer", 6)
    self.assertEqual('import random\nnummer = int(4) + int(5)\nprint(str(nummer))', result)
    self.assertEqual(run_code(result), "9")
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""
    """)

    self.assertEqual(expected, result)

  def test_calculation_with_vars(self):
    result = hedy.transpile("""nummer is 5
  nummertwee is 6
  getal is nummer * nummertwee
  print getal""", 6)
    self.assertEqual("""import random
  nummer = '5'
  nummertwee = '6'
  getal = int(nummer) * int(nummertwee)
  print(str(getal))""", result)
    self.assertEqual(run_code(result), "30")
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""
    """)

    self.assertEqual(expected, result)

  def test_print_calculation_times_directly(self):
    result = hedy.transpile("""nummer is 5
  nummertwee is 6
  print nummer * nummertwee""", 6)
    self.assertEqual("""import random
  nummer = '5'
  nummertwee = '6'
  print(str(int(nummer) * int(nummertwee)))""", result)
    self.assertEqual(run_code(result), "30")
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""
    """)

    self.assertEqual(expected, result)

  def test_print_calculation_divide_directly(self):
    result = hedy.transpile("""nummer is 5
  nummertwee is 6
  print nummer / nummertwee""", 6)
    self.assertEqual("""import random
  nummer = '5'
  nummertwee = '6'
  print(str(int(nummer) // int(nummertwee)))""", result)
    self.assertEqual(run_code(result), "0")
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 6)

    expected = textwrap.dedent("""
    """)

    self.assertEqual(expected, result)