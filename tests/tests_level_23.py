import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel23(HedyTester):
    level = 23

    def test_smaller_equal(self):
        code = textwrap.dedent("""\
    leeftijd = input('Ik ben 12 jaar, hoe oud ben jij?')
    if leeftijd <= 11:
        print('Dan ben je jonger dan ik!')""")
        expected = textwrap.dedent("""\
    leeftijd = input('Ik ben 12 jaar, hoe oud ben jij?')
    if int(leeftijd) <= int('11'):
      print(f'Dan ben je jonger dan ik!')""")
        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)
    def test_bigger_equal(self):
        code = textwrap.dedent("""\
    leeftijd = input('Ik ben 12 jaar, hoe oud ben jij?')
    if leeftijd >= 11:
        print('Dan ben je jonger dan ik!')""")
        expected = textwrap.dedent("""\
    leeftijd = input('Ik ben 12 jaar, hoe oud ben jij?')
    if int(leeftijd) >= int('11'):
      print(f'Dan ben je jonger dan ik!')""")
        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)
    def test_smaller_bigger_equal(self):
        code = textwrap.dedent("""\
    leeftijd = input('Ik ben 12 jaar, hoe oud ben jij?')
    if leeftijd <= 11:
        print('Dan ben je jonger dan ik!')
    elif leeftijd >= 13:
        print('Dan ben je ouder dan ik!')""")
        expected = textwrap.dedent("""\
    leeftijd = input('Ik ben 12 jaar, hoe oud ben jij?')
    if int(leeftijd) <= int('11'):
      print(f'Dan ben je jonger dan ik!')
    elif int(leeftijd) >= int('13'):
      print(f'Dan ben je ouder dan ik!')""")
        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)
