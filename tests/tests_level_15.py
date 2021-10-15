import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel15(HedyTester):
    level = 15

    def test_and(self):
        code = textwrap.dedent("""\
    if 5 is 5 and 4 is 4:
        print('hallo')""")
        expected = textwrap.dedent("""\
    if str('5') == str('5') and str('4') == str('4'):
      print(f'hallo')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)
    def test_or(self):
        code = textwrap.dedent("""\
    if 5 is 5 or 4 is 4:
        print('hallo')""")
        expected = textwrap.dedent("""\
    if str('5') == str('5') or str('4') == str('4'):
      print(f'hallo')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)


