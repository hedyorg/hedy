import hedy
import textwrap
from test_level_01 import HedyTester

class TestsLevel9(HedyTester):
  level = 9
  
  def test_for_list(self):
    code = textwrap.dedent("""\
    dieren is hond, kat, papegaai
    for dier in dieren
      print dier""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = ['hond', 'kat', 'papegaai']
    for dier in dieren:
      print(f'{dier}')""")

    self.assertEqual(expected, result.code)
  def test_for_list_multiple_lines(self):
    code = textwrap.dedent("""\
    familie is baby, mommy, daddy, grandpa, grandma
    for shark in familie
      print shark ' shark tudutudutudu'
      print shark ' shark tudutudutudu'
      print shark ' shark tudutudutudu'
      print shark ' shark'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    familie = ['baby', 'mommy', 'daddy', 'grandpa', 'grandma']
    for shark in familie:
      print(f'{shark} shark tudutudutudu')
      print(f'{shark} shark tudutudutudu')
      print(f'{shark} shark tudutudutudu')
      print(f'{shark} shark')""")

    self.assertEqual(expected, result.code)
  def test_for_list_dutch(self):
    code = textwrap.dedent("""\
    dieren is hond, kat, papegaai
    voor dier in dieren
      drukaf dier""")

    result = hedy.transpile(code, self.level, lang="nl")

    expected = textwrap.dedent("""\
    dieren = ['hond', 'kat', 'papegaai']
    for dier in dieren:
      print(f'{dier}')""")

    self.assertEqual(expected, result.code)
