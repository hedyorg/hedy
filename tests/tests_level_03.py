import unittest
import hedy
import sys
import io
from contextlib import contextmanager
import textwrap

# code = textwrap.dedent("""
# """)
#
# result = hedy.transpile(code, 3)
#
# expected = textwrap.dedent("""\
# """)
#
# self.assertEqual(expected, result)


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


class TestsLevel3(unittest.TestCase):
  def test_transpile_other(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("abc felienne 123", 3)
    self.assertEqual(str(context.exception), 'Invalid')

  def test_transpile_print_level_2(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("print felienne 123", 3)

    self.assertEqual('Unquoted Text', context.exception.args[0])  # hier moet nog we een andere foutmelding komen!

  def test_print(self):

    code = textwrap.dedent("""\
    print 'hallo wereld!'""")

    result = hedy.transpile(code, 3)

    expected = textwrap.dedent("""\
    print('hallo wereld!')""")

    self.assertEqual(expected, result)


  def test_print_with_comma(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet ,'""")

    result = hedy.transpile(code, 3)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet ,')""")

    self.assertEqual(expected, result)

  def test_print_with_single_quote(self):

    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet \\''""")

    result = hedy.transpile(code, 3)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet \\'')""")

    self.assertEqual(expected, result)

  def test_name_with_underscore(self):
    code = textwrap.dedent("""\
    voor_naam is Hedy
    print 'ik heet '""")

    result = hedy.transpile(code, 3)

    expected = textwrap.dedent("""\
    voor_naam = 'Hedy'
    print('ik heet ')""")

    self.assertEqual(expected, result)

  def test_name_that_is_keyword(self):
    code = textwrap.dedent("""\
    for is Hedy
    print 'ik heet ' for """)

    result = hedy.transpile(code, 3)

    expected = textwrap.dedent("""\
    _for = 'Hedy'
    print('ik heet '+_for)""")

    self.assertEqual(expected, result)

  def test_print_Spanish(self):

    code = textwrap.dedent("""\
    print 'Cuál es tu color favorito?'""")

    result = hedy.transpile(code, 3)

    expected = textwrap.dedent("""\
    print('Cuál es tu color favorito?')""")

    self.assertEqual(expected, result)

  def test_print_with_list_var(self):

    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print dieren at 1""")

    result = hedy.transpile(code, 3)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(dieren[1])""")

    self.assertEqual(expected, result)

    self.assertEqual(run_code(result), "Kat")

  def test_print_with_list_var_random(self):

    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print dieren at random""")

    result = hedy.transpile(code, 3)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(random.choice(dieren))""")

    self.assertEqual(expected, result)
    self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])

  def test_transpile_ask_Spanish(self):
    code = textwrap.dedent("""\
    color is ask Cuál es tu color favorito?""")

    result = hedy.transpile(code, 3)

    expected = textwrap.dedent("""\
    color = input('Cuál es tu color favorito?')""")

    self.assertEqual(expected, result)

  def test_print_2(self):

    code = textwrap.dedent("""\
    print 'ik heet henk'""")

    result = hedy.transpile(code, 3)

    expected = textwrap.dedent("""\
    print('ik heet henk')""")

    self.assertEqual(expected, result)

  def test_print_with_var(self):

    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam""")

    result = hedy.transpile(code, 3)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet'+naam)""")

    self.assertEqual(expected, result)

  def test_transpile_ask_with_print(self):

    code = textwrap.dedent("""
    kleur is ask wat is je lievelingskleur?
    print 'jouw lievelingskleur is dus' kleur '!'""")

    result = hedy.transpile(code, 3)

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur?')
    print('jouw lievelingskleur is dus'+kleur+'!')""")

    self.assertEqual(expected, result)

  def test_transpile_missing_opening_quote(self):
    code = textwrap.dedent("""
      print hallo wereld'""")

    with self.assertRaises(Exception) as context:
      result = hedy.transpile(code, 3)

    self.assertEqual('Unquoted Text', context.exception.args[0])  # hier moet nog we een andere foutmelding komen!

  def test_transpile_issue_375(self):
    code = textwrap.dedent("""
      is Foobar
      print welcome""")

    with self.assertRaises(Exception) as context:
      result = hedy.transpile(code, 3)

    self.assertEqual('Parse', context.exception.args[0])  # hier moet nog we een andere foutmelding komen!









