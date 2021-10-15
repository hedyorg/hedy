import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel15(HedyTester):
    level = 15






    def test_bool_true(self):
        code = textwrap.dedent("""\
    ja is True
    if ja is True:
        print('ja')""")
        expected = textwrap.dedent("""\
    ja = True
    if ja == True:
      print('ja')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_bool_false(self):
        code = textwrap.dedent("""\
    ja is False
    if ja is False:
        print('ja')""")
        expected = textwrap.dedent("""\
    ja = False
    if ja == False:
      print('ja')""")
        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_bool_true2(self):
        code = textwrap.dedent("""\
    ja is true
    if ja is True:
        print('ja')""")
        expected = textwrap.dedent("""\
    ja = True
    if ja == True:
      print('ja')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_bool_false2(self):
        code = textwrap.dedent("""\
    ja is false
    if ja is False:
        print('ja')""")
        expected = textwrap.dedent("""\
    ja = False
    if ja == False:
      print('ja')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_bool_total(self):
        code = textwrap.dedent("""\
    jebenternog is False
    benjeernog is input('ben je er nog? ja of nee?')
    if benjeernog is ja:
        jebenternog is True
    if jebenternog is True:
        print('Hallo!')
    if jebenternog is False:
        print('Doei!')""")
        expected = textwrap.dedent("""\
    jebenternog = False
    benjeernog = input('ben je er nog? ja of nee?')
    if str(benjeernog) == str('ja'):
      jebenternog = True
    if jebenternog == True:
      print('Hallo!')
    if jebenternog == False:
      print('Doei!')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_and(self):
        code = textwrap.dedent("""\
    if 5 is 5 and 4 is 4:
        print('hallo')""")
        expected = textwrap.dedent("""\
    if str('5') == str('5') and str('4') == str('4'):
      print('hallo')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

    def test_or(self):
        code = textwrap.dedent("""\
    if 5 is 5 or 4 is 4:
        print('hallo')""")
        expected = textwrap.dedent("""\
    if str('5') == str('5') or str('4') == str('4'):
      print('hallo')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)


