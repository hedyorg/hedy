import hedy
import textwrap
from test_level_01 import HedyTester

class TestsLevel8(HedyTester):
  level = 8

  def test_if_with_indent(self):
    # todo should be tested for all levels!
    code = textwrap.dedent("""\
    naam is Hedy
    if naam is Hedy
        print 'koekoek'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")

    self.assertEqual(expected, result.code)
  def test_repeat_with_indent(self):
    code = textwrap.dedent("""\
    repeat 5 times
      print 'koekoek'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    for i in range(int(5)):
      print(f'koekoek')""")

    self.assertEqual(expected, result.code)
  def test_repeat_with_variable_print(self):
    code = textwrap.dedent("""\
    n is 5
    repeat n times
        print 'me wants a cookie!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    n = '5'
    for i in range(int(n)):
      print(f'me wants a cookie!')""")

    self.assertEqual(expected, result.code)

    expected_output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.assertEqual(expected_output, HedyTester.run_code(result))

  # neesting

  def test_issue_902(self):
    code = textwrap.dedent("""\
    print 'kassabon'
    prijs is 0
    repeat 7 times
      ingredient is ask 'wat wil je kopen?'
      if ingredient is appel
        prijs is prijs + 1
    print 'Dat is in totaal ' prijs ' euro.'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'kassabon')
    prijs = '0'
    for i in range(int(7)):
      ingredient = input('wat wil je kopen?')
      if str(ingredient) == str('appel'):
        prijs = int(prijs) + int(1)
    print(f'Dat is in totaal {prijs} euro.')""")
    self.assertEqual(expected, result.code)

  def test_repeat_nested_in_if(self):
    code = textwrap.dedent("""\
    kleur is groen
    if kleur is groen
        repeat 3 times
            print 'mooi'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    kleur = 'groen'
    if str(kleur) == str('groen'):
      for i in range(int(3)):
        print(f'mooi')""")

    self.assertEqual(expected, result.code)

  def test_issue_396(self):
    code = textwrap.dedent("""\
    repeat 5 times
        if antwoord2 is 10
            print 'Goedzo'
        else
            print 'lalala'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    for i in range(int(5)):
      if str('antwoord2') == str('10'):
        print(f'Goedzo')
      else:
        print(f'lalala')""")

    self.assertEqual(expected, result.code)

  def test_empty_line_with_whitespace(self):
    code = textwrap.dedent("""\
    repeat 3 times
      food is ask 'What do you want?'
      if food is 'pizza'
        print 'nice!'
         
      else
        print 'pizza is better'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    for i in range(int(3)):
      food = input('What do you want?')
      if str(food) == str('pizza'):
        print(f'nice!')
      else:
        print(f'pizza is better')""")

    self.assertEqual(expected, result.code)




