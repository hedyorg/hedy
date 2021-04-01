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

    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet,' naam""")

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet,'+naam)""")

    self.assertEqual(expected, result)


  def test_transpile_ask_with_print(self):
    code = textwrap.dedent("""\
    kleur is ask wat is je lievelingskleur?
    print 'jouw lievelingskleur is dus' kleur '!'""")

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur?')
    print('jouw lievelingskleur is dus'+kleur+'!')""")

    self.assertEqual(expected, result)

  def test_transpile_ask_Spanish(self):
    code = textwrap.dedent("""\
    color is ask Cuál es tu color favorito?""")

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    color = input('Cuál es tu color favorito?')""")

    self.assertEqual(expected, result)


  def test_save_list_access_to_var(self):
    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    dier is dieren at random
    print dier""")

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    dier=random.choice(dieren)
    print(dier)""")

    self.assertEqual(expected, result)
    self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])

  def test_print_Spanish(self):
    code = textwrap.dedent("""\
    print 'Cuál es tu color favorito?'""")

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    print('Cuál es tu color favorito?')""")

    self.assertEqual(expected, result)


  # now adds if
  def test_print_if_else(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam
    if naam is Hedy print 'leuk' else print 'minder leuk'""")

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet'+naam)
    if naam == 'Hedy':
      print('leuk')
    else:
      print('minder leuk')""")

    self.assertEqual(expected, result)

  def test_print_if_else_with_ask(self):


    code = textwrap.dedent("""\
    kleur is ask Wat is je lievelingskleur?
    if kleur is groen print 'mooi!' else print 'niet zo mooi'""")

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    kleur = input('Wat is je lievelingskleur?')
    if kleur == 'groen':
      print('mooi!')
    else:
      print('niet zo mooi')""")

    self.assertEqual(expected, result)

  # steen schaar papier
  def test_print_if_else_with_and_var(self):

    code = textwrap.dedent("""\
    jouwkeuze is steen
    computerkeuze is schaar
    if computerkeuze is schaar and jouwkeuze is steen print 'jij wint'""")

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    jouwkeuze = 'steen'
    computerkeuze = 'schaar'
    if computerkeuze == 'schaar' and jouwkeuze == 'steen':
      print('jij wint')""")

    self.assertEqual(expected, result)
    self.assertEqual(run_code(result), 'jij wint')

  def test_print_if_with_var(self):
    code = textwrap.dedent("""\
    jouwkeuze is schaar
    computerkeuze is schaar
    if computerkeuze is jouwkeuze print 'gelijkspel!'""")

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    jouwkeuze = 'schaar'
    computerkeuze = 'schaar'
    if computerkeuze == jouwkeuze:
      print('gelijkspel!')""")

    self.assertEqual(expected, result)
    self.assertEqual(run_code(result), 'gelijkspel!')

  def test_if_in_array(self):
    code = textwrap.dedent("""\
    items is red, green
    selected is red
    if selected in items print 'found!'""")

    expected = textwrap.dedent("""\
    items = ['red', 'green']
    selected = 'red'
    if selected in items:
      print('found!')""")

    result = hedy.transpile(code, 4)

    self.assertEqual(expected, result)
    self.assertEqual('found!', run_code(result))

  def test_pront_should_suggest_print(self):
    code = "pront 'Hedy is leuk!'"

    with self.assertRaises(Exception) as context:
      result = hedy.transpile(code, 4)
    self.assertEqual('Invalid', str(context.exception))
    self.assertEqual('print', str(context.exception.arguments['guessed_command']))

  def test_parser_errors_should_be_caught_and_beautified(self):
    code = textwrap.dedent("""\
    option is ask Rock Paper or Scissors?
    print 'Player 2 ' option
    if option is Scissors
        print 'Its a tie!'""")

    with self.assertRaises(Exception) as context:
      result = hedy.transpile(code, 4)
    self.assertEqual('Parse', str(context.exception))


  def test_single_quote_in_assign_should_not_break(self):
    code = """message is 'Hello welcome to Hedy.'"""
    expected = "message = '\\'Hello welcome to Hedy.\\''"

    result = hedy.transpile(code, 4)
    self.assertEqual(expected, result)


  def test_single_quote_in_ask_should_not_break(self):
    # Maybe this test can be skipped if we finally
    # bite the bullet and allow ask (or mandate ask) to also use ''
    code = """naam is ask 'Hello welcome to Hedy.'"""
    expected = "naam = input('\\'Hello welcome to Hedy.\\'')"

    result = hedy.transpile(code, 4)
    print(result)
    self.assertEqual(expected, result)


  # while this looks STRANGE it is in essence the same sting issue
  # at least we solve it with the same fix of escaping quotes
  def test_bad_input_should_be_caught(self):
    code = textwrap.dedent("""\
    naam is ask hoe heet jij?
    ifnaam is Hedy print 'leuk' else print 'minder leuk!'""")

    result = hedy.transpile(code, 4)

    expected = textwrap.dedent("""\
    naam = input('hoe heet jij?')
    ifnaam = 'Hedy print \\'leuk\\' else print \\'minder leuk!\\''""")

    self.assertEqual(expected, result)
