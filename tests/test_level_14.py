import exceptions
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
      leeftijd = input(f'Hoe oud ben jij?')
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
      leeftijd = input(f'Hoe oud ben jij?')
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
      expected=expected
    )

  @parameterized.expand(HedyTester.comparison_commands)
  def tests_smaller_no_spaces(self, comparison):
    code = textwrap.dedent(f"""\
    leeftijd is ask 'Hoe oud ben jij?'
    if leeftijd{comparison}12
      print 'Dan ben je jonger dan ik!'""")
    expected = textwrap.dedent(f"""\
    leeftijd = input(f'Hoe oud ben jij?')
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
      expected=expected
    )

  @parameterized.expand(HedyTester.number_comparisons_commands)
  def test_comparison_with_string_gives_type_error(self, comparison):
    code = textwrap.dedent(f"""\
      a is 'text'
      if a {comparison} 12
          b is 1""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )


  @parameterized.expand(HedyTester.number_comparisons_commands)
  def test_comparison_with_list_gives_type_error(self, comparison):
    code = textwrap.dedent(f"""\
      a is 1, 2, 3
      if a {comparison} 12
          b is 1""")

    self.multi_level_tester(
      code=code,
      max_level=15,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_not_equal_promotes_int_to_float(self):
    code = textwrap.dedent(f"""\
      a is 1
      b is 1.2
      if a != b
          b is 1""")

    expected = textwrap.dedent(f"""\
      a = 1
      b = 1.2
      if str(a).zfill(100)!=str(b).zfill(100):
        b = 1""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected
    )

  @parameterized.expand([
    ("'text'", "'text'"),
    ('1', '1'),
    ('1.3', '1.3'),
    ('1, 2', '[1, 2]')])
  def test_not_equal(self, arg, exp):
    code = textwrap.dedent(f"""\
      a is {arg}
      b is {arg}
      if a != b
        b is 1""")

    expected = textwrap.dedent(f"""\
      a = {exp}
      b = {exp}
      if str(a).zfill(100)!=str(b).zfill(100):
        b = 1""")

    self.multi_level_tester(
      code=code,
      max_level=15,
      expected=expected
    )

  @parameterized.expand([
    ("'text'", '1'),      # text and number
    ('1, 2', '1'),        # list and number
    ('1, 2', "'text'")])  # list and text
  def test_not_equal_with_diff_types_gives_error(self, left, right):
    code = textwrap.dedent(f"""\
      a is {left}
      b is {right}
      if a != b
          b is 1""")

    self.multi_level_tester(
      code=code,
      max_level=15,
      exception=exceptions.InvalidTypeCombinationException
    )