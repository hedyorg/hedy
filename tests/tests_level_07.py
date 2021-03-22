import unittest
import hedy
import sys
import io
import textwrap
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


class TestsLevel7(unittest.TestCase):
  def test_print(self):
    result = hedy.transpile("print 'ik heet'", 7)
    self.assertEqual("import random\nprint('ik heet')", result)

  def test_print_with_var(self):
    result = hedy.transpile("naam is Hedy\nprint 'ik heet' naam", 7)
    self.assertEqual("import random\nnaam = 'Hedy'\nprint('ik heet'+str(naam))", result)

  def test_print_with_calc_no_spaces(self):
    result = hedy.transpile("print '5 keer 5 is ' 5*5", 7)
    self.assertEqual("import random\nprint('5 keer 5 is '+str(int(5) * int(5)))", result)

  def test_print_calculation_times_directly(self):
    result = hedy.transpile("""nummer is 5
nummertwee is 6
print nummer * nummertwee""", 7)
    self.assertEqual("""import random
nummer = '5'
nummertwee = '6'
print(str(int(nummer) * int(nummertwee)))""", result)
    self.assertEqual(run_code(result), "30")

  def test_transpile_ask(self):
    result = hedy.transpile("antwoord is ask wat is je lievelingskleur?", 7)
    self.assertEqual(result, "import random\nantwoord = input('wat is je lievelingskleur?')")

  def test_if_with_indent(self):
    result = hedy.transpile("""naam is Hedy
if naam is Hedy
    print 'koekoek'""", 7)
    self.assertEqual("""import random
naam = 'Hedy'
if str(naam) == str('Hedy'):
    print('koekoek')""", result)

  def test_repeat_with_indent(self):
    result = hedy.transpile("""repeat 5 times
    print 'koekoek'""", 7)
    self.assertEqual("""import random
for i in range(int(5)):
    print('koekoek')""", result)

  def test_repeat_with_variable_print(self):
    result = hedy.transpile("n is 5\nrepeat n times\n    print 'me wants a cookie!'", 7)
    self.assertEqual(result, """import random
n = '5'
for i in range(int(n)):
    print('me wants a cookie!')""")
    self.assertEqual(run_code(result),
                     'me wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!')

  def test_repeat_nested_in_if(self):
    result = hedy.transpile("""kleur is groen
if kleur is groen
    repeat 3 times
        print 'mooi'""", 7)
    self.assertEqual(result, """import random
kleur = 'groen'
if str(kleur) == str('groen'):
    for i in range(int(3)):
        print('mooi')""")

  def test_if_else(self):
    result = hedy.transpile("""antwoord is ask Hoeveel is 10 plus 10?
if antwoord is 20
    print 'Goedzo!'
    print 'Het antwoord was inderdaad ' antwoord
else
    print 'Foutje'
    print 'Het antwoord moest zijn ' antwoord""", 7)

    self.assertEqual("""import random
antwoord = input('Hoeveel is 10 plus 10?')
if str(antwoord) == str('20'):
    print('Goedzo!')
    print('Het antwoord was inderdaad '+str(antwoord))
else:
    print('Foutje')
    print('Het antwoord moest zijn '+str(antwoord))""", result)

  def test_repeat_basic_print(self):
    result = hedy.transpile("""repeat 5 times
    print 'me wants a cookie!'""", 7)
    self.assertEqual(result, """import random
for i in range(int(5)):
    print('me wants a cookie!')""")
    self.assertEqual(run_code(result),
                     'me wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!')

  def test_print_random(self):
    result = hedy.transpile("""keuzes is steen, schaar, papier
computerkeuze is keuzes at random
print 'computer koos ' computerkeuze""", 7)
    self.assertEqual("""import random
keuzes = ['steen', 'schaar', 'papier']
computerkeuze = random.choice(keuzes)
print('computer koos '+str(computerkeuze))""", result)

  def test_repeat_basic_print_multiple_lines(self):
    result = hedy.transpile("""repeat 5 times
    print 'cookieeee!'
    print 'me wants a cookie!'""", 7)
    self.assertEqual(result, """import random
for i in range(int(5)):
    print('cookieeee!')
    print('me wants a cookie!')""")
    # self.assertEqual(run_code(result),'cookieeee!\nme wants a cookie!\ncookieeee!\nme wants a cookie!\ncookieeee!\nme wants a cookie!\ncookieeee!\nme wants a cookie!\ncookieeee!\nme wants a cookie!')


  def test_level_7_no_indentation(self):
    #test that we get a parse error here
    code = textwrap.dedent("""\
    antwoord is ask Hoeveel is 10 keer tien?
    if antwoord is 100
    print 'goed zo'
    else
    print 'bah slecht'""")

    with self.assertRaises(Exception) as context:
      result = hedy.transpile(code, 7)
    self.assertEqual(str(context.exception), 'Parse')



