import hedy
import textwrap
from test_level_01 import HedyTester
from test_translating import check_local_lang_bool

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
      print(f'{dier}')""")

    self.single_level_tester(code=code, expected=expected)
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
      print(f'{shark} shark')""")

    self.single_level_tester(code=code, expected=expected)
    
  @check_local_lang_bool
  def test_for_list_dutch(self):
    code = textwrap.dedent("""\
    dieren is hond, kat, papegaai
    voor dier in dieren
        print dier""")

    expected = textwrap.dedent("""\
    dieren = ['hond', 'kat', 'papegaai']
    for dier in dieren:
        print(f'{dier}')""")

    self.single_level_tester(code=code, expected=expected)
