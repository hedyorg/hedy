
import hedy
import textwrap
from tests.Tester import HedyTester

class TestsLevel13(HedyTester):
  level = 13

  def test_and(self):
    code = textwrap.dedent("""\
      naam is ask 'hoe heet jij?'
      leeftijd is ask 'hoe oud ben jij?'
      if naam is 'Felienne' and leeftijd is 37
          print 'hallo jij!'""")
    expected = textwrap.dedent("""\
      naam = input(f'''hoe heet jij?''')
      try:
        naam = int(naam)
      except ValueError:
        try:
          naam = float(naam)
        except ValueError:
          pass
      leeftijd = input(f'''hoe oud ben jij?''')
      try:
        leeftijd = int(leeftijd)
      except ValueError:
        try:
          leeftijd = float(leeftijd)
        except ValueError:
          pass
      if str(naam) == str('Felienne') and str(leeftijd) == str('37'):
        print(f'''hallo jij!''')""")

    self.multi_level_tester(
      max_level=16,
      code=code,
      expected=expected
    )

  def test_equals(self):
    code = textwrap.dedent("""\
    name = ask 'what is your name?'
    age = ask 'what is your age?'
    if name is 'Hedy' and age is 2
        print 'You are the real Hedy!'""")

    expected = textwrap.dedent("""\
      name = input(f'''what is your name?''')
      try:
        name = int(name)
      except ValueError:
        try:
          name = float(name)
        except ValueError:
          pass
      age = input(f'''what is your age?''')
      try:
        age = int(age)
      except ValueError:
        try:
          age = float(age)
        except ValueError:
          pass
      if str(name) == str('Hedy') and str(age) == str('2'):
        print(f'''You are the real Hedy!''')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected,
      expected_commands=['ask', 'ask', 'if', 'and', 'print']
    )


  def test_or(self):
    code = textwrap.dedent("""\
      if 5 is 5 or 4 is 4
          print 'hallo'""")
    expected = textwrap.dedent("""\
      if str('5') == str('5') or str('4') == str('4'):
        print(f'''hallo''')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected,
      expected_commands=['if', 'or', 'print']
    )



