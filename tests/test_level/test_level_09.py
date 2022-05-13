import hedy
import textwrap
from tests.Tester import HedyTester

class TestsLevel9(HedyTester):
  level = 9

  def test_if_with_indent(self):
    # todo should be tested for all levels!
    code = textwrap.dedent("""\
    naam is Hedy
    if naam is Hedy
        print 'koekoek'""")


    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")

    self.single_level_tester(code=code, expected=expected)
  def test_repeat_with_indent(self):
    code = textwrap.dedent("""\
    repeat 5 times
        print 'koekoek'""")


    expected = textwrap.dedent("""\
    for i in range(int(5)):
      print(f'koekoek')
      time.sleep(0.1)""")

    self.single_level_tester(code=code, expected=expected)
  def test_repeat_with_variable_print(self):
    code = textwrap.dedent("""\
    n is 5
    repeat n times
        print 'me wants a cookie!'""")

    expected = textwrap.dedent("""\
    n = '5'
    for i in range(int(n)):
      print(f'me wants a cookie!')
      time.sleep(0.1)""")

    output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.single_level_tester(code=code, expected=expected, output=output)

  # nesting

  def test_issue_902(self):
    code = textwrap.dedent("""\
    print 'kassabon'
    prijs is 0
    repeat 7 times
        ingredient is ask 'wat wil je kopen?'
        if ingredient is appel
            prijs is prijs + 1
    print 'Dat is in totaal ' prijs ' euro.'""")

    expected = textwrap.dedent("""\
    print(f'kassabon')
    prijs = '0'
    for i in range(int('7')):
      ingredient = input(f'wat wil je kopen?')
      if str(ingredient) == str('appel'):
        prijs = int(prijs) + int(1)
      time.sleep(0.1)
    print(f'Dat is in totaal {prijs} euro.')""")
    self.single_level_tester(code=code, expected=expected)

  def test_repeat_nested_in_if(self):
    code = textwrap.dedent("""\
    kleur is groen
    if kleur is groen
        repeat 3 times
            print 'mooi'""")


    expected = textwrap.dedent("""\
    kleur = 'groen'
    if str(kleur) == str('groen'):
      for i in range(int('3')):
        print(f'mooi')
        time.sleep(0.1)""")

    self.single_level_tester(
      code=code,
      expected=expected,
      expected_commands=['is', 'if', 'repeat', 'print'])
  
  def test_repeat_comment_nested_if(self):
    code = textwrap.dedent("""\
    print 'kassabon'
    prijs is 0
    repeat 7 times # Comment
        ingredient is ask 'wat wil je kopen?'
        if ingredient is appel
            prijs is prijs + 1
    print 'Dat is in totaal ' prijs ' euro.'""")

    expected = textwrap.dedent("""\
    print(f'kassabon')
    prijs = '0'
    for i in range(int('7')):
      ingredient = input(f'wat wil je kopen?')
      if str(ingredient) == str('appel'):
        prijs = int(prijs) + int(1)
      time.sleep(0.1)
    print(f'Dat is in totaal {prijs} euro.')""")
    self.single_level_tester(code=code, expected=expected)

  def test_issue_396(self):
    code = textwrap.dedent("""\
    repeat 5 times
        if antwoord2 is 10
            print 'Goedzo'
        else
            print 'lalala'""")


    expected = textwrap.dedent("""\
    for i in range(int('5')):
      if str('antwoord2') == str('10'):
        print(f'Goedzo')
      else:
        print(f'lalala')
      time.sleep(0.1)""")

    self.single_level_tester(code=code, expected=expected)

  def test_empty_line_with_whitespace(self):
    code = textwrap.dedent("""\
    repeat 3 times
      food is ask 'What do you want?'
      if food is 'pizza'
        print 'nice!'
         
      else
        print 'pizza is better'""")


    expected = textwrap.dedent("""\
    for i in range(int('3')):
      food = input(f'What do you want?')
      if str(food) == str('pizza'):
        print(f'nice!')
      else:
        print(f'pizza is better')
      time.sleep(0.1)""")

    self.single_level_tester(code=code, expected=expected)