import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel14(HedyTester):
  level = 14

  def test_access_plus(self):
    code = textwrap.dedent("""\
      lijst is 1, 2, 3
      optellen is lijst[1] + lijst[2]
      optellen is optellen + lijst[3]
      print optellen""")
    expected = textwrap.dedent("""\
      lijst = [1, 2, 3]
      optellen = lijst[1-1] + lijst[2-1]
      optellen = optellen + lijst[3-1]
      print(f'{optellen}')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )