import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel14(HedyTester):
    level = 14

    def test_bool_true(self):
        code = textwrap.dedent("""\
        ja is True
        if ja is True:
            print('ja')""")
        expected = textwrap.dedent("""\
        ja = True
        if ja == True:
          print(f'ja')""")

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
      print(f'ja')""")
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
      print(f'ja')""")

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
      print(f'ja')""")

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
      print(f'Hallo!')
    if jebenternog == False:
      print(f'Doei!')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)

