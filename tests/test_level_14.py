import hedy
import textwrap
from parameterized import parameterized
from test_level_01 import HedyTester

class TestsLevel14(HedyTester):
  level = 14

  @parameterized.expand(HedyTester.comparison_commands)
  def test_comparisons(self, comparison):
    code = textwrap.dedent(f"""\
      leeftijd is ask 'Hoe oud ben jij?'
      if leeftijd {comparison} 12
          print 'Dan ben je jonger dan ik!'""")
    expected = textwrap.dedent(f"""\
      leeftijd = input('Hoe oud ben jij?')
      try:
        leeftijd = int(leeftijd)
      except ValueError:
        try:
          leeftijd = float(leeftijd)
        except ValueError:
          pass
      if str(leeftijd).zfill(100){comparison}str(12).zfill(100):
        print(f'Dan ben je jonger dan ik!')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  @parameterized.expand(HedyTester.comparison_commands)
  def test_comparisons_else(self, comparison):
    code = textwrap.dedent(f"""\
      leeftijd is ask 'Hoe oud ben jij?'
      if leeftijd {comparison} 12
          print 'Dan ben je jonger dan ik!'
      else
          print 'Dan ben je ouder dan ik!'""")
    expected = textwrap.dedent(f"""\
      leeftijd = input('Hoe oud ben jij?')
      try:
        leeftijd = int(leeftijd)
      except ValueError:
        try:
          leeftijd = float(leeftijd)
        except ValueError:
          pass
      if str(leeftijd).zfill(100){comparison}str(12).zfill(100):
        print(f'Dan ben je jonger dan ik!')
      else:
        print(f'Dan ben je ouder dan ik!')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  @parameterized.expand(HedyTester.comparison_commands)
  def test_comparison_with_string_gives_type_error(self, comparison):
    code = textwrap.dedent(f"""\
      a is 'text'
      if a {comparison} 12
          b is 1""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      exception=hedy.exceptions.InvalidArgumentTypeException,
      test_name=self.name()
    )

  @parameterized.expand(HedyTester.comparison_commands)
  def test_comparison_with_list_gives_type_error(self, comparison):
    code = textwrap.dedent(f"""\
      a is 1, 2, 3
      if a {comparison} 12
          b is 1""")

    self.multi_level_tester(
      code=code,
      max_level=15,
      exception=hedy.exceptions.InvalidArgumentTypeException,
      test_name=self.name()
    )
