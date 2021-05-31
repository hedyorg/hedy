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

class TestsLevel22(unittest.TestCase):
    maxDiff = None

    def test_print(self):
        result = hedy.transpile("print('ik heet')", 22)
        self.assertEqual("print('ik heet')", result)

    def test_print_with_var(self):
        result = hedy.transpile("naam = Hedy\nprint('ik heet' naam)", 22)
        self.assertEqual("naam = 'Hedy'\nprint('ik heet'+str(naam))", result)

    def test_print_with_calc_no_spaces(self):
        result = hedy.transpile("print('5 keer 5 is ' 5*5)", 22)
        self.assertEqual("print('5 keer 5 is '+str(int(5) * int(5)))", result)

    def test_print_calculation_times_directly(self):
        code = textwrap.dedent("""\
    nummer = 5
    nummertwee = 6
    print(nummer * nummertwee)""")

        result = hedy.transpile(code, 22)

        expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    print(str(int(nummer) * int(nummertwee)))""")

        self.assertEqual(expected, result)

        self.assertEqual("30", run_code(result))

    def test_transpile_ask(self):
        result = hedy.transpile("antwoord = input('wat is je lievelingskleur?')", 22)
        self.assertEqual(result, "antwoord = input('wat is je lievelingskleur?')")

    def test_if_with_indent(self):
        code = textwrap.dedent("""\
naam = Hedy
if naam == Hedy:
    print('koekoek')""")
        expected = textwrap.dedent("""\
naam = 'Hedy'
if str(naam) == str('Hedy'):
  print('koekoek')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_if_else(self):
        code = textwrap.dedent("""\
antwoord = input('Hoeveel is 10 plus 10?')
if antwoord == 22:
    print('Goedzo!')
    print('Het antwoord was inderdaad ' antwoord)
else:
    print('Foutje')
    print('Het antwoord moest zijn ' antwoord)""")

        expected = textwrap.dedent("""\
antwoord = input('Hoeveel is 10 plus 10?')
if str(antwoord) == str('22'):
  print('Goedzo!')
  print('Het antwoord was inderdaad '+str(antwoord))
else:
  print('Foutje')
  print('Het antwoord moest zijn '+str(antwoord))""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_print_random(self):
        code = textwrap.dedent("""\
    keuzes = ['steen', 'schaar', 'papier']
    computerkeuze = keuzes[random]
    print('computer koos ' computerkeuze)""")
        expected = textwrap.dedent("""\
    keuzes = ['steen', 'schaar', 'papier']
    computerkeuze=random.choice(keuzes)
    print('computer koos '+str(computerkeuze))""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_for_loop(self):
        code = textwrap.dedent("""\
    a = 2
    a = 3
    for a in range(2,4):
      a = a + 2
      b = b + 2""")
        expected = textwrap.dedent("""\
    a = '2'
    a = '3'
    for a in range(int(2), int(4)+1):
      a = int(a) + int(2)
      b = int(b) + int(2)""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_if__else(self):
        code = textwrap.dedent("""\
    a = 5
    if a == 1:
      x = 2
    else:
      x = 222""")
        expected = textwrap.dedent("""\
    a = '5'
    if str(a) == str('1'):
      x = '2'
    else:
      x = '222'""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_forloop(self):
        code = textwrap.dedent("""\
    for i in range(1, 10):
      print(i)
    print('wie niet weg is is gezien')""")
        expected = textwrap.dedent("""\
    for i in range(int(1), int(10)+1):
      print(str(i))
    print('wie niet weg is is gezien')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_for_nesting(self):
        code = textwrap.dedent("""\
    for i in range(1, 3):
      for j in range(1,4):
        print('rondje: ' i ' tel: ' j)""")
        expected = textwrap.dedent("""\
    for i in range(int(1), int(3)+1):
      for j in range(int(1), int(4)+1):
        print('rondje: '+str(i)+' tel: '+str(j))""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_if_nesting(self):
        code = textwrap.dedent("""\
    kleur = blauw
    kleurtwee = geel
    if kleur == blauw:
      if kleurtwee == geel:
        print('Samen is dit groen!')""")
        expected = textwrap.dedent("""\
    kleur = 'blauw'
    kleurtwee = 'geel'
    if str(kleur) == str('blauw'):
      if str(kleurtwee) == str('geel'):
        print('Samen is dit groen!')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_newprint(self):
        code = textwrap.dedent("""\
    leeftijd = input('Hoe oud ben jij?')
    print('Dus jij hebt zo veel verjaardagen gehad:')
    for i in range(0,leeftijd):
        print(i)""")
        expected = textwrap.dedent("""\
    leeftijd = input('Hoe oud ben jij?')
    print('Dus jij hebt zo veel verjaardagen gehad:')
    for i in range(int(0), int(leeftijd)+1):
      print(str(i))""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_list(self):
        code = textwrap.dedent("""\
    fruit = ['appel', 'banaan', 'kers']
    print(fruit)""")
        expected = textwrap.dedent("""\
    fruit = ['appel', 'banaan', 'kers']
    print(str(fruit))""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_random(self):
        code = textwrap.dedent("""\
    fruit = ['banaan', 'appel', 'kers']
    randomfruit = fruit[random]
    print(randomfruit)""")
        expected = textwrap.dedent("""\
    fruit = ['banaan', 'appel', 'kers']
    randomfruit=random.choice(fruit)
    print(str(randomfruit))""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_specific_access(self):
        code = textwrap.dedent("""\
    fruit = ['banaan', 'appel', 'kers']
    eerstefruit = fruit[1]
    print(eerstefruit)""")
        expected = textwrap.dedent("""\
    fruit = ['banaan', 'appel', 'kers']
    eerstefruit=fruit[1-1]
    print(str(eerstefruit))""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    # note that print(str(highscore)) will not print as it will compare 'score[i]' as str to a variable
    def test_everything_combined(self):
        code = textwrap.dedent("""\
    score = ['100', '300', '500']
    highscore = score[random]
    print('De highscore is: ' highscore)
    for i in range(1,3):
        scorenu = score[i]
        print('Score is nu ' scorenu)
        if highscore == score[i]:
            print(highscore)""")
        expected = textwrap.dedent("""\
    score = ['100', '300', '500']
    highscore=random.choice(score)
    print('De highscore is: '+str(highscore))
    for i in range(int(1), int(3)+1):
      scorenu=score[i-1]
      print('Score is nu '+str(scorenu))
      if str(highscore) == str('score[i]'):
        print(str(highscore))""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_if_under_else_in_for(self):
        code = textwrap.dedent("""\
    for i in range(0, 10):
      antwoord = input('Wat is 5*5')
      if antwoord == 24:
        print('Dat is fout!')
      else:
        print('Dat is goed!')
      if antwoord == 25:
        i = 10""")

        expected = textwrap.dedent("""\
    for i in range(int(0), int(10)+1):
      antwoord = input('Wat is 5*5')
      if str(antwoord) == str('24'):
        print('Dat is fout!')
      else:
        print('Dat is goed!')
      if str(antwoord) == str('25'):
        i = '10'""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_bool_true(self):
        code = textwrap.dedent("""\
    ja = True
    if ja == True:
        print('ja')""")
        expected = textwrap.dedent("""\
    ja = True
    if ja == True:
      print('ja')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_bool_false(self):
        code = textwrap.dedent("""\
    ja = False
    if ja == False:
        print('ja')""")
        expected = textwrap.dedent("""\
    ja = False
    if ja == False:
      print('ja')""")
        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_bool_true2(self):
        code = textwrap.dedent("""\
    ja = true
    if ja == True:
        print('ja')""")
        expected = textwrap.dedent("""\
    ja = True
    if ja == True:
      print('ja')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_bool_false2(self):
        code = textwrap.dedent("""\
    ja = false
    if ja == False:
        print('ja')""")
        expected = textwrap.dedent("""\
    ja = False
    if ja == False:
      print('ja')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_bool_total(self):
        code = textwrap.dedent("""\
    jebenternog = False
    benjeernog = input('ben je er nog? ja of nee?')
    if benjeernog == ja:
        jebenternog = True
    if jebenternog == True:
        print('Hallo!')
    if jebenternog == False:
        print('Doei!')""")
        expected = textwrap.dedent("""\
    jebenternog = False
    benjeernog = input('ben je er nog? ja of nee?')
    if str(benjeernog) == str('ja'):
      jebenternog = True
    if jebenternog == True:
      print('Hallo!')
    if jebenternog == False:
      print('Doei!')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_and(self):
        code = textwrap.dedent("""\
    if 5 == 5 and 4 == 4:
        print('hallo')""")
        expected = textwrap.dedent("""\
    if str('5') == str('5') and str('4') == str('4'):
      print('hallo')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_or(self):
        code = textwrap.dedent("""\
    if 5 == 5 or 4 == 4:
        print('hallo')""")
        expected = textwrap.dedent("""\
    if str('5') == str('5') or str('4') == str('4'):
      print('hallo')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_comment(self):
        code = textwrap.dedent("""\
    if 5 == 5 or 4 == 4:
        print('hallo')
        #comment""")
        expected = textwrap.dedent("""\
    if str('5') == str('5') or str('4') == str('4'):
      print('hallo')
      # ['comment']""")
        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_commentbegin(self):
        code = textwrap.dedent("""\
    # comment word
    if 5 == 5 or 4 == 4:
        print('hallo')
        """)
        expected = textwrap.dedent("""\
    # [' comment word']
    if str('5') == str('5') or str('4') == str('4'):
      print('hallo')""")
        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_commentresult(self):
        code = textwrap.dedent("""\
    # comment word
    if 5 == 5 or 4 == 4:
        print('hallo')
        """)
        expected = textwrap.dedent("""\
    # [' comment word']
    if str('5') == str('5') or str('4') == str('4'):
      print('hallo')""")
        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_smaller(self):
        code = textwrap.dedent("""\
    leeftijd = input('Hoe oud ben jij?')
    if leeftijd < 12:
        print('Dan ben je jonger dan ik!')""")
        expected = textwrap.dedent("""\
    leeftijd = input('Hoe oud ben jij?')
    if str(leeftijd) < str('12'):
      print('Dan ben je jonger dan ik!')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_bigger(self):
        code = textwrap.dedent("""\
    leeftijd = input('Hoe oud ben jij?')
    if leeftijd > 12:
        print('Dan ben je ouder dan ik!')""")
        expected = textwrap.dedent("""\
    leeftijd = input('Hoe oud ben jij?')
    if str(leeftijd) > str('12'):
      print('Dan ben je ouder dan ik!')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_big_and_small(self):
        code = textwrap.dedent("""\
    leeftijd = input('Hoe oud ben jij?')
    if leeftijd < 12:
        print('Dan ben je jonger dan ik!')
    elif leeftijd > 12:
        print('Dan ben je ouder dan ik!')""")
        expected = textwrap.dedent("""\
    leeftijd = input('Hoe oud ben jij?')
    if str(leeftijd) < str('12'):
      print('Dan ben je jonger dan ik!')
    elif str(leeftijd) > str('12'):
      print('Dan ben je ouder dan ik!')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_whileloop(self):
        code = textwrap.dedent("""\
    goedantwoord = False
    while goedantwoord == False:
        antwoord = input('Wat is 5 keer 5?')
        if antwoord == 25:
            goedantwoord = True""")
        expected = textwrap.dedent("""\
    goedantwoord = False
    while goedantwoord == False:
      antwoord = input('Wat is 5 keer 5?')
      if str(antwoord) == str('25'):
        goedantwoord = True""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_whileloop2(self):
        code = textwrap.dedent("""\
    tel = 1
    # we gaan door totdat tel 3 is!
    while tel < 3:
        print('Dit is de ' tel 'e keer')
        tel = tel + 1
    print('We zijn klaar')""")
        expected = textwrap.dedent("""\
    tel = '1'
    # [' we gaan door totdat tel 3 is!']
    while str(tel) < str('3'):
      print('Dit is de '+str(tel)+'e keer')
      tel = int(tel) + int(1)
    print('We zijn klaar')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_whileloop3(self):
        code = textwrap.dedent("""\
    goedantwoord = False
    # we gaan door totdat een goed antwoord is gegeven!
    while goedantwoord == False:
        antwoord = input('Wat is 5 keer 5?')
        if antwoord == 25:
            goedantwoord = True
            print('Er is een goed antwoord gegeven')""")
        expected = textwrap.dedent("""\
    goedantwoord = False
    # [' we gaan door totdat een goed antwoord is gegeven!']
    while goedantwoord == False:
      antwoord = input('Wat is 5 keer 5?')
      if str(antwoord) == str('25'):
        goedantwoord = True
        print('Er is een goed antwoord gegeven')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_access_plus(self):
        code = textwrap.dedent("""\
    lijst = ['1', '2', '3']
    optellen = lijst[1] + lijst[2]
    optellen = optellen + lijst[3]
    # we verwachten hier 6
    print(optellen)""")
        expected = textwrap.dedent("""\
    lijst = ['1', '2', '3']
    optellen = int(lijst[1-1]) + int(lijst[2-1])
    optellen = int(optellen) + int(lijst[3-1])
    # [' we verwachten hier 6']
    print(str(optellen))""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)
    def test_length(self):
        code = textwrap.dedent("""\
    fruit = ['appel', 'banaan', 'kers']
    hoi = length(fruit)
    print(hoi)""")
        expected = textwrap.dedent("""\
    fruit = ['appel', 'banaan', 'kers']
    hoi = len(fruit)
    print(str(hoi))""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_length2(self):
        code = textwrap.dedent("""\
    fruit = ['appel', 'banaan', 'kers']
    for i in range(1, length(fruit)):
        print(fruit[i])""")
        expected = textwrap.dedent("""\
    fruit = ['appel', 'banaan', 'kers']
    for i in range(int(1), int(len(fruit))+1):
      print(str(fruit[i-1]))""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_print_length(self):
        code = textwrap.dedent("""\
    fruit = ['appel', 'banaan', 'kers']
    print('lengte van de lijst is' length(fruit))
    for i in range(1, 3):
        print(fruit[i])""")
        expected = textwrap.dedent("""\
    fruit = ['appel', 'banaan', 'kers']
    print('lengte van de lijst is'+str(len(fruit)))
    for i in range(int(1), int(3)+1):
      print(str(fruit[i-1]))""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_not_equal_one(self):
        code = textwrap.dedent("""\
    land = input('In welk land woon jij?')
    if land != Nederland:
        print('Cool!')
    else:
        print('Ik kom ook uit Nederland!')""")
        expected = textwrap.dedent("""\
    land = input('In welk land woon jij?')
    if str(land) != str('Nederland'):
      print('Cool!')
    else:
      print('Ik kom ook uit Nederland!')""")
        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_not_equal_two(self):
        code = textwrap.dedent("""\
    getal = input('Je mag geen 5 zeggen, wat is een leuk getal?')
    if getal != 5:
        print('Goed zo!')
    else:
        print('Fout! Je mocht geen 5 zeggen')""")
        expected = textwrap.dedent("""\
    getal = input('Je mag geen 5 zeggen, wat is een leuk getal?')
    if str(getal) != str('5'):
      print('Goed zo!')
    else:
      print('Fout! Je mocht geen 5 zeggen')""")
        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_smaller_equal(self):
        code = textwrap.dedent("""\
    leeftijd = input('Ik ben 12 jaar, hoe oud ben jij?')
    if leeftijd <= 11:
        print('Dan ben je jonger dan ik!')""")
        expected = textwrap.dedent("""\
    leeftijd = input('Ik ben 12 jaar, hoe oud ben jij?')
    if str(leeftijd) <= str('11'):
      print('Dan ben je jonger dan ik!')""")
        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_bigger_equal(self):
        code = textwrap.dedent("""\
    leeftijd = input('Ik ben 12 jaar, hoe oud ben jij?')
    if leeftijd >= 11:
        print('Dan ben je jonger dan ik!')""")
        expected = textwrap.dedent("""\
    leeftijd = input('Ik ben 12 jaar, hoe oud ben jij?')
    if str(leeftijd) >= str('11'):
      print('Dan ben je jonger dan ik!')""")
        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_smaller_bigger_equal(self):
        code = textwrap.dedent("""\
    leeftijd = input('Ik ben 12 jaar, hoe oud ben jij?')
    if leeftijd <= 11:
        print('Dan ben je jonger dan ik!')
    elif leeftijd >= 13:
        print('Dan ben je ouder dan ik!')""")
        expected = textwrap.dedent("""\
    leeftijd = input('Ik ben 12 jaar, hoe oud ben jij?')
    if str(leeftijd) <= str('11'):
      print('Dan ben je jonger dan ik!')
    elif str(leeftijd) >= str('13'):
      print('Dan ben je ouder dan ik!')""")
        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_sum_in_if(self):
        code = textwrap.dedent("""\
    if 5+3 == 8:
        print('5+3 is inderdaad 8')
    else:
        print('Dit wordt niet geprint want 5+3 is 8!')""")
        expected = textwrap.dedent("""\
    if int(5) + int(3) == int(8):
      print('5+3 is inderdaad 8')
    else:
      print('Dit wordt niet geprint want 5+3 is 8!')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_sum_in_right_side_if(self):
        code = textwrap.dedent("""\
    if 8 == 5+3:
        print('5+3 is inderdaad 8')
    else:
        print('Dit wordt niet geprint want 5+3 is 8!')""")
        expected = textwrap.dedent("""\
    if int(8) == int(5) + int(3):
      print('5+3 is inderdaad 8')
    else:
      print('Dit wordt niet geprint want 5+3 is 8!')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_min_in_if(self):
        code = textwrap.dedent("""\
    if 5-3 == 2:
        print('5-3 is inderdaad 2')
    else:
        print('Dit wordt niet geprint want 5+3 is 8!')""")
        expected = textwrap.dedent("""\
    if int(5) - int(3) == int(2):
      print('5-3 is inderdaad 2')
    else:
      print('Dit wordt niet geprint want 5+3 is 8!')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)

    def test_multiply_in_if(self):
        code = textwrap.dedent("""\
    if 5*3 == 15:
        print('5*3 is inderdaad 15')
    else:
        print('Dit wordt niet geprint want 5+3 is 8!')""")
        expected = textwrap.dedent("""\
    if int(5) * int(3) == int(15):
      print('5*3 is inderdaad 15')
    else:
      print('Dit wordt niet geprint want 5+3 is 8!')""")

        result = hedy.transpile(code, 22)

        self.assertEqual(expected, result)
# programs with issues to see if we catch them properly
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


