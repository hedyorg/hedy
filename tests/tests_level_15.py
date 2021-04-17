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


class TestsLevel15(unittest.TestCase):
  maxDiff = None
  def test_print(self):
    result = hedy.transpile("print('ik heet')", 15)
    self.assertEqual("print('ik heet')", result)

  def test_print_with_var(self):
    result = hedy.transpile("naam = Hedy\nprint('ik heet' naam)", 15)
    self.assertEqual("naam = 'Hedy'\nprint('ik heet'+str(naam))", result)

  def test_print_with_calc_no_spaces(self):
    result = hedy.transpile("print('5 keer 5 is ' 5*5)", 15)
    self.assertEqual("print('5 keer 5 is '+str(int(5) * int(5)))", result)

  def test_print_calculation_times_directly(self):
    result = hedy.transpile("""nummer = 5
nummertwee = 6
print(nummer * nummertwee)""", 15)
    self.assertEqual("""nummer = '5'
nummertwee = '6'
print(str(int(nummer) * int(nummertwee)))""", result)
    self.assertEqual(run_code(result), "30")

  def test_transpile_ask(self):
    result = hedy.transpile("antwoord = input('wat is je lievelingskleur?')", 15)
    self.assertEqual(result, "antwoord = input('wat is je lievelingskleur?')")

  def test_if_with_indent(self):
    result = hedy.transpile("""naam = Hedy
if naam == Hedy:
    print('koekoek')""", 15)
    self.assertEqual("""naam = 'Hedy'
if str(naam) == str('Hedy'):
  print('koekoek')""", result)

  def test_if_else(self):
    result = hedy.transpile("""antwoord = input('Hoeveel is 10 plus 10?')
if antwoord == 20:
    print('Goedzo!')
    print('Het antwoord was inderdaad ' antwoord)
else:
    print('Foutje')
    print('Het antwoord moest zijn ' antwoord)""", 15)

    self.assertEqual("""antwoord = input('Hoeveel is 10 plus 10?')
if str(antwoord) == str('20'):
  print('Goedzo!')
  print('Het antwoord was inderdaad '+str(antwoord))
else:
  print('Foutje')
  print('Het antwoord moest zijn '+str(antwoord))""", result)


  def test_print_random(self):
    result = hedy.transpile("""keuzes = ['steen', 'schaar', 'papier']
computerkeuze = keuzes[random]
print('computer koos ' computerkeuze)""", 15)
    self.assertEqual("""keuzes = ['steen', 'schaar', 'papier']
computerkeuze=random.choice(keuzes)
print('computer koos '+str(computerkeuze))""", result)

  def test_for_loop(self):
    result = hedy.transpile("""
a = 2
a = 3
for a in range(2,4):
  a = a + 2
  b = b + 2""", 15)
    self.assertEqual(result, """a = '2'
a = '3'
for a in range(int(2), int(4)+1):
  a = int(a) + int(2)
  b = int(b) + int(2)""")

  def test_if__else(self):
    result = hedy.transpile("""
a = 5
if a == 1:
  x = 2
else:
  x = 222""", 15)
    self.assertEqual(result, """a = '5'
if str(a) == str('1'):
  x = '2'
else:
  x = '222'""")

  def test_forloop(self):
    result = hedy.transpile("""
for i in range(1, 10):
  print(i)
print('wie niet weg is is gezien')""", 15)
    self.assertEqual(result, """for i in range(int(1), int(10)+1):
  print(str(i))
print('wie niet weg is is gezien')""")

  def test_for_nesting(self):
    result = hedy.transpile("""for i in range(1, 3):
  for j in range(1,4):
    print('rondje: ' i ' tel: ' j)""", 15)
    self.assertEqual(result,"""for i in range(int(1), int(3)+1):
  for j in range(int(1), int(4)+1):
    print('rondje: '+str(i)+' tel: '+str(j))""")

  def test_if_nesting(self):
    result = hedy.transpile("""kleur = blauw
kleurtwee = geel
if kleur == blauw:
  if kleurtwee == geel:
    print('Samen is dit groen!')""", 15)
    self.assertEqual(result, """kleur = 'blauw'
kleurtwee = 'geel'
if str(kleur) == str('blauw'):
  if str(kleurtwee) == str('geel'):
    print('Samen is dit groen!')""")

  def test_newprint(self):
    result = hedy.transpile("""leeftijd = input('Hoe oud ben jij?')
print('Dus jij hebt zo veel verjaardagen gehad:')
for i in range(0,leeftijd):
    print(i)""", 15)
    self.assertEqual(result, """leeftijd = input('Hoe oud ben jij?')
print('Dus jij hebt zo veel verjaardagen gehad:')
for i in range(int(0), int(leeftijd)+1):
  print(str(i))""")

  def test_list(self):
    result = hedy.transpile("""fruit = ['appel', 'banaan', 'kers']
print(fruit)""", 15)
    self.assertEqual(result, """fruit = ['appel', 'banaan', 'kers']
print(str(fruit))""")

  def test_random(self):
    result = hedy.transpile("""fruit = ['banaan', 'appel', 'kers']
randomfruit = fruit[random]
print(randomfruit)""", 15)
    self.assertEqual(result, """fruit = ['banaan', 'appel', 'kers']
randomfruit=random.choice(fruit)
print(str(randomfruit))""")

  def test_specific_access(self):
    result = hedy.transpile("""fruit = ['banaan', 'appel', 'kers']
eerstefruit = fruit[1]
print(eerstefruit)""", 15)
    self.assertEqual(result, """fruit = ['banaan', 'appel', 'kers']
eerstefruit=fruit[1-1]
print(str(eerstefruit))""")

#note that print(str(highscore)) will not print as it will compare 'score[i]' as str to a variable
  def test_everything_combined(self):
    result = hedy.transpile("""score = ['100', '300', '500']
highscore = score[random]
print('De highscore is: ' highscore)
for i in range(1,3):
    scorenu = score[i]
    print('Score is nu ' scorenu)
    if highscore == score[i]:
        print(highscore)""", 15)
    self.assertEqual(result, """score = ['100', '300', '500']
highscore=random.choice(score)
print('De highscore is: '+str(highscore))
for i in range(int(1), int(3)+1):
  scorenu=score[i-1]
  print('Score is nu '+str(scorenu))
  if str(highscore) == str('score[i]'):
    print(str(highscore))""")

  def test_not_equal_one(self):
    result = hedy.transpile("""land = input('In welk land woon jij?')
if land != Nederland:
    print('Cool!')
else:
    print('Ik kom ook uit Nederland!')"""
, 15)
    self.assertEqual(result, """land = input('In welk land woon jij?')
if str(land) != str('Nederland'):
  print('Cool!')
else:
  print('Ik kom ook uit Nederland!')""")

  def test_not_equal_two(self):
    result = hedy.transpile("""getal = input('Je mag geen 5 zeggen, wat is een leuk getal?')
if getal != 5:
    print('Goed zo!')
else:
    print('Fout! Je mocht geen 5 zeggen')""", 15)
    self.assertEqual(result, """getal = input('Je mag geen 5 zeggen, wat is een leuk getal?')
if str(getal) != str('5'):
  print('Goed zo!')
else:
  print('Fout! Je mocht geen 5 zeggen')""")

  def test_smaller(self):
      result = hedy.transpile("""leeftijd = input('Hoe oud ben jij?')
if leeftijd < 12:
    print('Dan ben je jonger dan ik!')""", 15)
      self.assertEqual(result, """leeftijd = input('Hoe oud ben jij?')
if str(leeftijd) < str('12'):
  print('Dan ben je jonger dan ik!')""")

  def test_bigger(self):
      result = hedy.transpile("""leeftijd = input('Hoe oud ben jij?')
if leeftijd > 12:
    print('Dan ben je ouder dan ik!')""", 15)
      self.assertEqual(result, """leeftijd = input('Hoe oud ben jij?')
if str(leeftijd) > str('12'):
  print('Dan ben je ouder dan ik!')""")

  def test_big_and_small(self):
      result = hedy.transpile("""leeftijd = input('Hoe oud ben jij?')
if leeftijd < 12:
    print('Dan ben je jonger dan ik!')
elif leeftijd > 12:
    print('Dan ben je ouder dan ik!')""", 15)
      self.assertEqual(result, """leeftijd = input('Hoe oud ben jij?')
if str(leeftijd) < str('12'):
  print('Dan ben je jonger dan ik!')
elif str(leeftijd) > str('12'):
  print('Dan ben je ouder dan ik!')""")
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
  #     result = hedy.transpile(code, 10)
  #   self.assertEqual(str(context.exception), 'Parse')


