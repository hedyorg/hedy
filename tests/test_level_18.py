import hedy
import textwrap
from test_level_01 import HedyTester

class TestsLevel18(HedyTester):
    level = 18

    # def test_print_var_brackets(self):
    #     code = textwrap.dedent("""\
    #     naam is Hedy
    #     print('ik heet', naam)""")
    #
    #     expected = textwrap.dedent("""\
    #     naam = 'Hedy'
    #     print(f'ik heet{naam}')""")
    #
    #     self.multi_level_tester(
    #       code=code,
    #       expected=expected,
    #       extra_check_function=self.is_not_turtle(),
    #       test_name=self.name()
    #     )
    #
