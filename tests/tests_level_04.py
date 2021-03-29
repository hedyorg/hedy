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
    with captured_output() as (out, err):
        exec(code)
    return out.getvalue().strip()


class TestsLevel4(unittest.TestCase):
  # invalid, ask and print should still work as in level 4
  def test_transpile_other(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("abc felienne 123", 4)
    self.assertEqual(str(context.exception), 'Invalid')

  def test_print_with_var(self):

    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam""")

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet'+naam)""")

    self.assertEqual(expected, result)

  def test_print_with_comma(self):
    result = hedy.transpile("naam is Hedy\nprint 'ik heet,' naam", 4)
    self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet,'+naam)")
    code = textwrap.dedent("""""")

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""""")

    self.assertEqual(expected, result)


  def test_transpile_ask_with_print(self):
    result = hedy.transpile("kleur is ask wat is je lievelingskleur?\nprint 'jouw lievelingskleur is dus' kleur '!'", 4)
    self.assertEqual(result,
                     "import random\nkleur = input('wat is je lievelingskleur?')\nprint('jouw lievelingskleur is dus'+kleur+'!')")
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    """)

    self.assertEqual(expected, result)

  def test_transpile_ask_Spanish(self):
    result = hedy.transpile("color is ask Cuál es tu color favorito?", 4)
    self.assertEqual(result, "import random\ncolor = input('Cuál es tu color favorito?')")
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    """)

    self.assertEqual(expected, result)


  def test_save_list_access_to_var(self):
    result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\ndier is dieren at random\nprint dier", 4)
    self.assertEqual(result,
                     "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']\ndier=random.choice(dieren)\nprint(dier)")
    self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    """)

    self.assertEqual(expected, result)


  def test_print_Spanish(self):
    result = hedy.transpile("print 'Cuál es tu color favorito?'", 4)
    self.assertEqual(result, "import random\nprint('Cuál es tu color favorito?')")
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    """)

    self.assertEqual(expected, result)


  # now adds if
  def test_print_if_else(self):
    result = hedy.transpile("""naam is Hedy
print 'ik heet' naam
if naam is Hedy print 'leuk' else print 'minder leuk'""", 4)

    expected_result = """import random
naam = 'Hedy'
print('ik heet'+naam)
if naam == 'Hedy':
  print('leuk')
else:
  print('minder leuk')"""
    self.assertEqual(expected_result, result)
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    """)

    self.assertEqual(expected, result)


  def test_print_if_else_with_ask(self):
    result = hedy.transpile("""kleur is ask Wat is je lievelingskleur?
if kleur is groen print 'mooi!' else print 'niet zo mooi'""", 4)

    expected_result = """import random
kleur = input('Wat is je lievelingskleur?')
if kleur == 'groen':
  print('mooi!')
else:
  print('niet zo mooi')"""

    self.assertEqual(expected_result, result)
    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    """)

    self.assertEqual(expected, result)


  # steen schaar papier
  def test_print_if_else_with_and_var(self):
    result = hedy.transpile("""jouwkeuze is steen
computerkeuze is schaar
if computerkeuze is schaar and jouwkeuze is steen print 'jij wint'""", 4)

    expected_result = """import random
jouwkeuze = 'steen'
computerkeuze = 'schaar'
if computerkeuze == 'schaar' and jouwkeuze == 'steen':
  print('jij wint')"""
    self.assertEqual(expected_result, result)
    self.assertEqual(run_code(result), 'jij wint')

  def test_print_if_with_var(self):
    result = hedy.transpile("""jouwkeuze is schaar
computerkeuze is schaar
if computerkeuze is jouwkeuze print 'gelijkspel!'""", 4)

    expected_result = """import random
jouwkeuze = 'schaar'
computerkeuze = 'schaar'
if computerkeuze == jouwkeuze:
  print('gelijkspel!')"""
    self.assertEqual(expected_result, result)
    self.assertEqual(run_code(result), 'gelijkspel!')

    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    """)

    self.assertEqual(expected, result)

  def test_if_in_array(self):
    actual = hedy.transpile("items is red, green\nselected is red\nif selected in items print 'found!'", 4)

    expected = """import random
items = ['red', 'green']
selected = 'red'
if selected in items:
  print('found!')"""

    self.assertEqual(expected, actual)
    self.assertEqual('found!', run_code(actual))

    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    """)

    self.assertEqual(expected, result)

  def test_pront_should_suggest_print(self):
    program = "pront 'Hedy is leuk!'"

    with self.assertRaises(Exception) as context:
      result = hedy.transpile(program, 4)
    self.assertEqual('Invalid', str(context.exception))
    self.assertEqual('print', str(context.exception.arguments['guessed_command']))

    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    """)

    self.assertEqual(expected, result)

  def test_parser_errors_should_be_caught_and_beautified(self):
    program = """option is ask Rock Paper or Scissors?
print 'Player 2 ' option
if option is Scissors
    print 'Its a tie!'"""

    with self.assertRaises(Exception) as context:
      result = hedy.transpile(program, 4)
    self.assertEqual('Parse', str(context.exception))

    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    """)

    self.assertEqual(expected, result)

  def test_single_quote_in_assign_should_not_break(self):
    program = """message is 'Hello welcome to Hedy.'"""

    result = hedy.transpile(program, 4)
    self.assertEqual("""import random
message = '\\'Hello welcome to Hedy.\\''""", result)

    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    """)

    self.assertEqual(expected, result)

  def test_single_quote_in_ask_should_not_break(self):
    # Maybe this test can be skipped if we finally
    # bite the bullet and allow ask (or mandate ask) to also use ''
    program = """naam is ask 'Hello welcome to Hedy.'"""

    result = hedy.transpile(program, 4)
    print(result)
    self.assertEqual("""import random
naam = input('\\'Hello welcome to Hedy.\\'')""", result)

    code = textwrap.dedent("""\
    """)

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    """)

    self.assertEqual(expected, result)

  # while this looks STRANGE it is in essence the same sting issue
  # at least we solve it with the same fix of escaping quotes
  def test_bad_input_should_be_caught(self):
    program = """naam is ask hoe heet jij?
ifnaam is Hedy print 'leuk' else print 'minder leuk!'"""

    result = hedy.transpile(program, 4)
    print(result)
    self.assertEqual("""import random
naam = input('hoe heet jij?')
ifnaam = 'Hedy print \\'leuk\\' else print \\'minder leuk!\\''""", result)

    code = textwrap.dedent("""""")

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    """)

    self.assertEqual(expected, result)