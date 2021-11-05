import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel12(HedyTester):
  level = 12

  def tests_smaller(self):
    code = textwrap.dedent("""\
      leeftijd is ask 'Hoe oud ben jij?'
      if leeftijd < 12
          print 'Dan ben je jonger dan ik!'""")
    expected = textwrap.dedent("""\
      leeftijd = input('Hoe oud ben jij?')
      try:
        prijs = int(leeftijd)
      except ValueError:
        try:
          prijs = float(leeftijd)
        except ValueError:
          pass
      if int(leeftijd) < int('12'):
        print(f'Dan ben je jonger dan ik!')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )
  def tests_bigger(self):
    code = textwrap.dedent("""\
      leeftijd is ask 'Hoe oud ben jij?'
      if leeftijd > 12
          print 'Dan ben je ouder dan ik!'""")
    expected = textwrap.dedent("""\
      leeftijd = input('Hoe oud ben jij?')
      try:
        prijs = int(leeftijd)
      except ValueError:
        try:
          prijs = float(leeftijd)
        except ValueError:
          pass
      if int(leeftijd) > int('12'):
        print(f'Dan ben je ouder dan ik!')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )
  def tests_big_and_small(self):
    code = textwrap.dedent("""\
      leeftijd is ask 'Hoe oud ben jij?'
      if leeftijd < 12
          print 'Dan ben je jonger dan ik!'
      else
          print 'Dan ben je ouder dan ik!'""")
    expected = textwrap.dedent("""\
      leeftijd = input('Hoe oud ben jij?')
      try:
        prijs = int(leeftijd)
      except ValueError:
        try:
          prijs = float(leeftijd)
        except ValueError:
          pass
      if int(leeftijd) < int('12'):
        print(f'Dan ben je jonger dan ik!')
      else:
        print(f'Dan ben je ouder dan ik!')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )