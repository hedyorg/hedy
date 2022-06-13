import hedy
import exceptions
import textwrap
from tests.Tester import HedyTester

class TestsLevel15(HedyTester):
  level = 15


  def test_while_equals(self):
    code = textwrap.dedent("""\
      antwoord is 0
      while antwoord != 25
          antwoord is ask 'Wat is 5 keer 5?'
      print 'Goed gedaan!'""")
    expected = textwrap.dedent("""\
    antwoord = 0
    while str(antwoord).zfill(100)!=str(25).zfill(100):
      antwoord = input(f'''Wat is 5 keer 5?''')
      try:
        antwoord = int(antwoord)
      except ValueError:
        try:
          antwoord = float(antwoord)
        except ValueError:
          pass
      time.sleep(0.1)
    print(f'''Goed gedaan!''')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected,
      expected_commands=['is', 'while', 'ask', 'print']
    )

  def test_while_fr_equals(self):
    code = textwrap.dedent("""\
      antwoord est 0
      tant que antwoord != 25
          antwoord est demande 'Wat is 5 keer 5?'
      affiche 'Goed gedaan!'""")
    expected = textwrap.dedent("""\
    antwoord = 0
    while str(antwoord).zfill(100)!=str(25).zfill(100):
      antwoord = input(f'''Wat is 5 keer 5?''')
      try:
        antwoord = int(antwoord)
      except ValueError:
        try:
          antwoord = float(antwoord)
        except ValueError:
          pass
      time.sleep(0.1)
    print(f'''Goed gedaan!''')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected,
      expected_commands=['is', 'while', 'ask', 'print'],
      lang='fr'
    )

  def test_while_undefined_var(self):
    code = textwrap.dedent("""\
      while antwoord != 25
          print 'hoera'""")

    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.UndefinedVarException,
      max_level=16,
    )

  def test_while_smaller(self):
    code = textwrap.dedent("""\
      getal is 0
      while getal < 100000
          getal is ask 'HOGER!!!!!'
      print 'Hoog he?'""")
    expected = textwrap.dedent("""\
    getal = 0
    while str(getal).zfill(100)<str(100000).zfill(100):
      getal = input(f'''HOGER!!!!!''')
      try:
        getal = int(getal)
      except ValueError:
        try:
          getal = float(getal)
        except ValueError:
          pass
      time.sleep(0.1)
    print(f'''Hoog he?''')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected
    )

  def test_missing_indent_while(self):
    code = textwrap.dedent(f"""\
    answer = 0
    while answer != 25
    answer = ask 'What is 5 times 5?'
    print 'A correct answer has been given'""")

    self.multi_level_tester(
      code=code,
      max_level=15,
      exception=exceptions.NoIndentationException
    )