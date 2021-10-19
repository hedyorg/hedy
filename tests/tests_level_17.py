import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel17(HedyTester):
    level = 17

    def test_smaller(self):
        code = textwrap.dedent("""\
        leeftijd is input('Hoe oud ben jij?')
        if leeftijd < 12:
            print('Dan ben je jonger dan ik!')""")
        expected = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        if int(leeftijd) < int('12'):
          print(f'Dan ben je jonger dan ik!')""")

        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )

    def test_bigger(self):
        code = textwrap.dedent("""\
        leeftijd is input('Hoe oud ben jij?')
        if leeftijd > 12:
            print('Dan ben je ouder dan ik!')""")
        expected = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        if int(leeftijd) > int('12'):
          print(f'Dan ben je ouder dan ik!')""")

        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )

    def test_big_and_small(self):
        code = textwrap.dedent("""\
        leeftijd is input('Hoe oud ben jij?')
        if leeftijd < 12:
            print('Dan ben je jonger dan ik!')
        elif leeftijd > 12:
            print('Dan ben je ouder dan ik!')""")
        expected = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        if int(leeftijd) < int('12'):
          print(f'Dan ben je jonger dan ik!')
        elif int(leeftijd) > int('12'):
          print(f'Dan ben je ouder dan ik!')""")

        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )

