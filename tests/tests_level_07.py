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
  code = "import random\n" + code
  with captured_output() as (out, err):
    exec(code)
  return out.getvalue().strip()


class TestsLevel7(unittest.TestCase):
  def test_print(self):
    code = textwrap.dedent("""\
    print 'ik heet'""")

    result = hedy.transpile(code, 7)

    expected = textwrap.dedent("""\
    print('ik heet')""")

    self.assertEqual(expected, result)

  def test_print_with_var(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam""")

    result = hedy.transpile(code, 7)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet'+str(naam))""")

    self.assertEqual(expected, result)

  def test_print_with_calc_no_spaces(self):
    code = textwrap.dedent("""\
    print '5 keer 5 is ' 5*5""")

    result = hedy.transpile(code, 7)

    expected = textwrap.dedent("""\
    print('5 keer 5 is '+str(int(5) * int(5)))""")

    self.assertEqual(expected, result)

  def test_print_calculation_times_directly(self):
    code = textwrap.dedent("""\
    nummer is 5
    nummertwee is 6
    print nummer * nummertwee""")

    result = hedy.transpile(code, 7)

    expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    print(str(int(nummer) * int(nummertwee)))""")

    self.assertEqual(expected, result)

    self.assertEqual("30", run_code(result))

  def test_transpile_ask(self):
    code = textwrap.dedent("""\
    antwoord is ask wat is je lievelingskleur?""")

    result = hedy.transpile(code, 7)

    expected = textwrap.dedent("""\
    antwoord = input('wat is je lievelingskleur?')""")

    self.assertEqual(expected, result)

  def test_if_with_indent(self):
    code = textwrap.dedent("""\
    naam is Hedy
    if naam is Hedy
        print 'koekoek'""")

    result = hedy.transpile(code, 7)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print('koekoek')""")

    self.assertEqual(expected, result)

  def test_repeat_with_indent(self):
    code = textwrap.dedent("""\
    repeat 5 times
      print 'koekoek'""")

    result = hedy.transpile(code, 7)

    expected = textwrap.dedent("""\
    for i in range(int(5)):
      print('koekoek')""")

    self.assertEqual(expected, result)

  def test_repeat_with_variable_print(self):
    code = textwrap.dedent("""\
    n is 5
    repeat n times
        print 'me wants a cookie!'""")

    result = hedy.transpile(code, 7)

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
    kleur is groen
    if kleur is groen
        repeat 3 times
            print 'mooi'""")

    result = hedy.transpile(code, 7)

    expected = textwrap.dedent("""\
    kleur = 'groen'
    if str(kleur) == str('groen'):
      for i in range(int(3)):
        print('mooi')""")

    self.assertEqual(expected, result)

  def test_if_else(self):
    code = textwrap.dedent("""\
    antwoord is ask Hoeveel is 10 plus 10?
    if antwoord is 20
        print 'Goedzo!'
        print 'Het antwoord was inderdaad ' antwoord
    else
        print 'Foutje'
        print 'Het antwoord moest zijn ' antwoord""")

    result = hedy.transpile(code, 7)

    expected = textwrap.dedent("""\
    antwoord = input('Hoeveel is 10 plus 10?')
    if str(antwoord) == str('20'):
      print('Goedzo!')
      print('Het antwoord was inderdaad '+str(antwoord))
    else:
      print('Foutje')
      print('Het antwoord moest zijn '+str(antwoord))""")

    self.assertEqual(expected, result)

  def test_repeat_basic_print(self):
    code = textwrap.dedent("""\
    repeat 5 times
      print 'me wants a cookie!'""")

    result = hedy.transpile(code, 7)

    expected = textwrap.dedent("""\
    for i in range(int(5)):
      print('me wants a cookie!')""")

    self.assertEqual(expected, result)

    expected_output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.assertEqual(expected_output, run_code(result))



  def test_print_random(self):

    code = textwrap.dedent("""\
    keuzes is steen, schaar, papier
    computerkeuze is keuzes at random
    print 'computer koos ' computerkeuze""")

    result = hedy.transpile(code, 7)

    expected = textwrap.dedent("""\
    keuzes = ['steen', 'schaar', 'papier']
    computerkeuze=random.choice(keuzes)
    print('computer koos '+str(computerkeuze))""")

    self.assertEqual(expected, result)

  def test_addition_simple(self):

    code = textwrap.dedent("""\
    var is 5
    print var + 5""")

    result = hedy.transpile(code, 7)

    expected = textwrap.dedent("""\
    var = '5'
    print(str(int(var) + int(5)))""")

    self.assertEqual(expected, result)

  def test_issue_297(self):

    code = textwrap.dedent("""\
    count is 1
    repeat 12 times
      print count ' times 12 is ' count*12
      count is count + 1""")

    result = hedy.transpile(code, 7)

    expected = textwrap.dedent("""\
    count = '1'
    for i in range(int(12)):
      print(str(count)+' times 12 is '+str(int(count) * int(12)))
      count = int(count) + int(1)""")

    self.assertEqual(expected, result)


    
#programs with issues to see if we catch them properly
# (so this should fail, for now)
# at one point we want a real "Indent" error and a better error message
# for this!

  # def test_level_7_no_indentation(self):
  #   #test that we get a parse error here
  #   code = textwrap.dedent("""\
  #   antwoord is ask Hoeveel is 10 keer tien?
  #   if antwoord is 100
  #   print 'goed zo'
  #   else
  #   print 'bah slecht'""")
  #
  #   with self.assertRaises(Exception) as context:
  #     result = hedy.transpile(code, 7)
  #   self.assertEqual(str(context.exception), 'Parse')


