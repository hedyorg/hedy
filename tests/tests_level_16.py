import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel16(HedyTester):
    level = 16

    def test_comment(self):
        code = textwrap.dedent("""\
        #comment""")
        expected = textwrap.dedent("""\
        # ['comment']""")
        self.multi_level_tester(
          
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )

    def test_comment_indented(self):
        code = textwrap.dedent("""\
        if 5 is 5 or 4 is 4:
            print('hallo')
            #comment""")
        expected = textwrap.dedent("""\
        if str('5') == str('5') or str('4') == str('4'):
          print(f'hallo')
          # ['comment']""")
        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_comment_with_comma(self):
        code = textwrap.dedent("""\
        if 5 is 5 or 4 is 4:
            print('hallo')
            # comment1, comment2""")

        expected = textwrap.dedent("""\
        if str('5') == str('5') or str('4') == str('4'):
          print(f'hallo')
          # [' comment1', ' comment2']""")
        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_commentbegin(self):
        code = textwrap.dedent("""\
    # comment word
    if 5 is 5 or 4 is 4:
        print('hallo')
        """)
        expected = textwrap.dedent("""\
    # [' comment word']
    if str('5') == str('5') or str('4') == str('4'):
      print(f'hallo')""")
        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)
    def test_commentresult(self):
        code = textwrap.dedent("""\
        # comment word
        if 5 is 5 or 4 is 4:
            print('hallo')
            """)
        expected = textwrap.dedent("""\
        # [' comment word']
        if str('5') == str('5') or str('4') == str('4'):
          print(f'hallo')""")

        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )


