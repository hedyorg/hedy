import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel22(HedyTester):
    level = 22

    def test_not_equal_one(self):
        code = textwrap.dedent("""\
        land = input('In welk land woon jij?')
        if land != Nederland:
            print('Cool!')
        else:
            print('Ik kom ook uit Nederland!')""")
        expected = textwrap.dedent("""\
        land = input('In welk land woon jij?')
        if str(land) != str('Nederland'):
          print(f'Cool!')
        else:
          print(f'Ik kom ook uit Nederland!')""")
        self.multi_level_tester(
          
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )

    def test_not_equal_two(self):
        code = textwrap.dedent("""\
        getal = input('Je mag geen 5 zeggen, wat is een leuk getal?')
        if getal != 5:
            print('Goed zo!')
        else:
            print('Fout! Je mocht geen 5 zeggen')""")
        expected = textwrap.dedent("""\
        getal = input('Je mag geen 5 zeggen, wat is een leuk getal?')
        if str(getal) != str('5'):
          print(f'Goed zo!')
        else:
          print(f'Fout! Je mocht geen 5 zeggen')""")
        self.multi_level_tester(
          
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
