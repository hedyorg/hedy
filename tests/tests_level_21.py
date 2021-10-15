import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel21(HedyTester):
    level = 21

    def test_sum_in_if(self):
        code = textwrap.dedent("""\
    if 5+3 == 8:
        print('5+3 is inderdaad 8')
    else:
        print('Dit wordt niet geprint want 5+3 is 8!')""")
        expected = textwrap.dedent("""\
    if int(5) + int(3) == int(8):
      print(f'5+3 is inderdaad 8')
    else:
      print(f'Dit wordt niet geprint want 5+3 is 8!')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)
    def test_sum_in_right_side_if(self):
        code = textwrap.dedent("""\
    if 8 == 5+3:
        print('5+3 is inderdaad 8')
    else:
        print('Dit wordt niet geprint want 5+3 is 8!')""")
        expected = textwrap.dedent("""\
    if int(8) == int(5) + int(3):
      print(f'5+3 is inderdaad 8')
    else:
      print(f'Dit wordt niet geprint want 5+3 is 8!')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)
    def test_min_in_if(self):
        code = textwrap.dedent("""\
    if 5-3 == 2:
        print('5-3 is inderdaad 2')
    else:
        print('Dit wordt niet geprint want 5+3 is 8!')""")
        expected = textwrap.dedent("""\
    if int(5) - int(3) == int(2):
      print(f'5-3 is inderdaad 2')
    else:
      print(f'Dit wordt niet geprint want 5+3 is 8!')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)
    def test_multiply_in_if(self):
        code = textwrap.dedent("""\
    if 5*3 == 15:
        print('5*3 is inderdaad 15')
    else:
        print('Dit wordt niet geprint want 5+3 is 8!')""")
        expected = textwrap.dedent("""\
    if int(5) * int(3) == int(15):
      print(f'5*3 is inderdaad 15')
    else:
      print(f'Dit wordt niet geprint want 5+3 is 8!')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)


