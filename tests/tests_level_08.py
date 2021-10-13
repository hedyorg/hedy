import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel8(HedyTester):
  level = 8
  
  def test_for_list(self):
    code = textwrap.dedent("""\
    dieren is hond, kat, papegaai
    for dier in dieren
      print dier""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = ['hond', 'kat', 'papegaai']
    for dier in dieren:
        print(str(dier))""")

    self.assertEqual(expected, result.code)
