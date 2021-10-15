import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel20(HedyTester):
    level = 20

    def test_length(self):
        code = textwrap.dedent("""\
        fruit is ['appel', 'banaan', 'kers']
        hoi is length(fruit)
        print(hoi)""")
        expected = textwrap.dedent("""\
        fruit = ['appel', 'banaan', 'kers']
        hoi = len(fruit)
        print(f'{hoi}')""")

        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_length2(self):
        code = textwrap.dedent("""\
        fruit is ['appel', 'banaan', 'kers']
        for i in range(1, length(fruit)):
            print(fruit[i])""")
        expected = textwrap.dedent("""\
        fruit = ['appel', 'banaan', 'kers']
        step = 1 if int(1) < int(len(fruit)) else -1
        for i in range(int(1), int(len(fruit)) + step, step):
          print(f'{fruit[i-1]}')""")

        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_print_length(self):
        code = textwrap.dedent("""\
        fruit is ['appel', 'banaan', 'kers']
        print('lengte van de lijst is' length(fruit))
        for i in range(1, 3):
            print(fruit[i])""")
        expected = textwrap.dedent("""\
        fruit = ['appel', 'banaan', 'kers']
        print(f'lengte van de lijst is{len(fruit)}')
        step = 1 if int(1) < int(3) else -1
        for i in range(int(1), int(3) + step, step):
          print(f'{fruit[i-1]}')""")

        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )


