import hedy
import textwrap
from Tester import HedyTester

class TestsLevel10(HedyTester):
  level = 10
  
  def test_for_list(self):
    code = textwrap.dedent("""\
    dieren is hond, kat, papegaai
    for dier in dieren
        print dier""")

    expected = textwrap.dedent("""\
    dieren = ['hond', 'kat', 'papegaai']
    for dier in dieren:
      print(f'{dier}')
      time.sleep(0.1)""")

    self.single_level_tester(
      code=code,
      expected=expected,
      expected_commands=['is', 'for', 'print'])

  def test_for_list_hindi(self):
    code = textwrap.dedent("""\
    क is hond, kat, papegaai
    for काउंटर in क
        print काउंटर""")

    expected = textwrap.dedent("""\
    v920cc330837bbd206f02b0d9660af196 = ['hond', 'kat', 'papegaai']
    for v7693a3e5c7a942bd47bf4b5af10576ac in v920cc330837bbd206f02b0d9660af196:
      print(f'{v7693a3e5c7a942bd47bf4b5af10576ac}')
      time.sleep(0.1)""")

    self.single_level_tester(
      code=code,
      expected=expected,
      expected_commands=['is', 'for', 'print'])

  def test_for_list_multiple_lines(self):
    code = textwrap.dedent("""\
    familie is baby, mommy, daddy, grandpa, grandma
    for shark in familie
        print shark ' shark tudutudutudu'
        print shark ' shark tudutudutudu'
        print shark ' shark tudutudutudu'
        print shark ' shark'""")

    expected = textwrap.dedent("""\
    familie = ['baby', 'mommy', 'daddy', 'grandpa', 'grandma']
    for shark in familie:
      print(f'{shark} shark tudutudutudu')
      print(f'{shark} shark tudutudutudu')
      print(f'{shark} shark tudutudutudu')
      print(f'{shark} shark')
      time.sleep(0.1)""")

    self.single_level_tester(code=code, expected=expected)

  def test_for_list_with_string_gives_type_error(self):
    code = textwrap.dedent("""\
    dieren is 'text'
    for dier in dieren
        print dier""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      exception=hedy.exceptions.InvalidArgumentTypeException)

  def test_for_list_with_int_gives_type_error(self):
    code = textwrap.dedent("""\
      dieren is 5
      for dier in dieren
        print dier""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      exception=hedy.exceptions.InvalidArgumentTypeException)
