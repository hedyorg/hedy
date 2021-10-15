import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel20(HedyTester):
    level = 20












    def test_bool_true(self):
        code = textwrap.dedent("""\
    ja is True
    if ja is True:
        print('ja')""")
        expected = textwrap.dedent("""\
    ja = True
    if ja == True:
      print('ja')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_bool_false(self):
        code = textwrap.dedent("""\
    ja is False
    if ja is False:
        print('ja')""")
        expected = textwrap.dedent("""\
    ja = False
    if ja == False:
      print('ja')""")
        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_bool_true2(self):
        code = textwrap.dedent("""\
    ja is true
    if ja is True:
        print('ja')""")
        expected = textwrap.dedent("""\
    ja = True
    if ja == True:
      print('ja')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_bool_false2(self):
        code = textwrap.dedent("""\
    ja is false
    if ja is False:
        print('ja')""")
        expected = textwrap.dedent("""\
    ja = False
    if ja == False:
      print('ja')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_bool_total(self):
        code = textwrap.dedent("""\
    jebenternog is False
    benjeernog is input('ben je er nog? ja of nee?')
    if benjeernog is ja:
        jebenternog is True
    if jebenternog is True:
        print('Hallo!')
    if jebenternog is False:
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

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_and(self):
        code = textwrap.dedent("""\
    if 5 is 5 and 4 is 4:
        print('hallo')""")
        expected = textwrap.dedent("""\
    if str('5') == str('5') and str('4') == str('4'):
      print('hallo')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_or(self):
        code = textwrap.dedent("""\
    if 5 is 5 or 4 is 4:
        print('hallo')""")
        expected = textwrap.dedent("""\
    if str('5') == str('5') or str('4') == str('4'):
      print('hallo')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_comment(self):
        code = textwrap.dedent("""\
    if 5 is 5 or 4 is 4:
        print('hallo')
        #comment""")
        expected = textwrap.dedent("""\
    if str('5') == str('5') or str('4') == str('4'):
      print('hallo')
      # ['comment']""")
        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_commentbegin(self):
        code = textwrap.dedent("""\
    # comment word
    if 5 is 5 or 4 is 4:
        print('hallo')
        """)
        expected = textwrap.dedent("""\
    # [' comment word']
    if str('5') == str('5') or str('4') == str('4'):
      print('hallo')""")
        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_commentresult(self):
        code = textwrap.dedent("""\
    # comment word
    if 5 is 5 or 4 is 4:
        print('hallo')
        """)
        expected = textwrap.dedent("""\
    # [' comment word']
    if str('5') == str('5') or str('4') == str('4'):
      print('hallo')""")
        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_smaller(self):
        code = textwrap.dedent("""\
    leeftijd is input('Hoe oud ben jij?')
    if leeftijd < 12:
        print('Dan ben je jonger dan ik!')""")
        expected = textwrap.dedent("""\
    leeftijd = input('Hoe oud ben jij?')
    if int(leeftijd) < int('12'):
      print('Dan ben je jonger dan ik!')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_bigger(self):
        code = textwrap.dedent("""\
    leeftijd is input('Hoe oud ben jij?')
    if leeftijd > 12:
        print('Dan ben je ouder dan ik!')""")
        expected = textwrap.dedent("""\
    leeftijd = input('Hoe oud ben jij?')
    if int(leeftijd) > int('12'):
      print('Dan ben je ouder dan ik!')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_big_and_small(self):
        code = textwrap.dedent("""\
    leeftijd is input('Hoe oud ben jij?')
    if leeftijd < 12:
        print('Dan ben je jonger dan ik!')
    elif leeftijd > 12:
        print('Dan ben je ouder dan ik!')""")
        expected = textwrap.dedent("""\
    leeftijd = input('Hoe oud ben jij?')
    if int(leeftijd) < int('12'):
      print('Dan ben je jonger dan ik!')
    elif int(leeftijd) > int('12'):
      print('Dan ben je ouder dan ik!')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_whileloop(self):
        code = textwrap.dedent("""\
    goedantwoord is False
    while goedantwoord is False:
        antwoord is input('Wat is 5 keer 5?')
        if antwoord is 25:
            goedantwoord is True""")
        expected = textwrap.dedent("""\
    goedantwoord = False
    while goedantwoord == False:
      antwoord = input('Wat is 5 keer 5?')
      if str(antwoord) == str('25'):
        goedantwoord = True""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_whileloop2(self):
        code = textwrap.dedent("""\
    tel is 1
    # we gaan door totdat tel 3 is!
    while tel < 3:
        print('Dit is de ' tel 'e keer')
        tel is tel + 1
    print('We zijn klaar')""")
        expected = textwrap.dedent("""\
    tel = '1'
    # [' we gaan door totdat tel 3 is!']
    while int(tel) < int('3'):
      print('Dit is de '+str(tel)+'e keer')
      tel = int(tel) + int(1)
    print('We zijn klaar')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_whileloop3(self):
        code = textwrap.dedent("""\
    goedantwoord is False
    # we gaan door totdat een goed antwoord is gegeven!
    while goedantwoord is False:
        antwoord is input('Wat is 5 keer 5?')
        if antwoord is 25:
            goedantwoord is True
            print('Er is een goed antwoord gegeven')""")
        expected = textwrap.dedent("""\
    goedantwoord = False
    # [' we gaan door totdat een goed antwoord is gegeven!']
    while goedantwoord == False:
      antwoord = input('Wat is 5 keer 5?')
      if str(antwoord) == str('25'):
        goedantwoord = True
        print('Er is een goed antwoord gegeven')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_access_plus(self):
        code = textwrap.dedent("""\
    lijst is ['1', '2', '3']
    optellen is lijst[1] + lijst[2]
    optellen is optellen + lijst[3]
    # we verwachten hier 6
    print(optellen)""")
        expected = textwrap.dedent("""\
    lijst = ['1', '2', '3']
    optellen = int(lijst[1-1]) + int(lijst[2-1])
    optellen = int(optellen) + int(lijst[3-1])
    # [' we verwachten hier 6']
    print(str(optellen))""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)
    def test_length(self):
        code = textwrap.dedent("""\
    fruit is ['appel', 'banaan', 'kers']
    hoi is length(fruit)
    print(hoi)""")
        expected = textwrap.dedent("""\
    fruit = ['appel', 'banaan', 'kers']
    hoi = len(fruit)
    print(str(hoi))""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_length2(self):
        code = textwrap.dedent("""\
    fruit is ['appel', 'banaan', 'kers']
    for i in range(1, length(fruit)):
        print(fruit[i])""")
        expected = textwrap.dedent("""\
    fruit = ['appel', 'banaan', 'kers']
    step = 1 if int(1) < int(len(fruit)) else -1
    for i in range(int(1), int(len(fruit)) + step, step):
      print(str(fruit[i-1]))""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_print_length(self):
        code = textwrap.dedent("""\
    fruit is ['appel', 'banaan', 'kers']
    print('lengte van de lijst is' length(fruit))
    for i in range(1, 3):
        print(fruit[i])""")
        expected = textwrap.dedent("""\
    fruit = ['appel', 'banaan', 'kers']
    print('lengte van de lijst is'+str(len(fruit)))
    step = 1 if int(1) < int(3) else -1
    for i in range(int(1), int(3) + step, step):
      print(str(fruit[i-1]))""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)


