import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel19(HedyTester):
    level = 19

    def test_access_plus(self):
        code = textwrap.dedent("""\
    lijst is ['1', '2', '3']
    optellen is lijst[1] + lijst[2]
    optellen is optellen + lijst[3]
    # we verwachten hier 6
    print(optellen)""")
        expected = textwrap.dedent("""\
    lijst = ['1', '2', '3']
    optellen = int(lijst[1-1]) + int(lijst[2-1])
    optellen = int(optellen) + int(lijst[3-1])
    # [' we verwachten hier 6']
    print(f'{optellen}')""")

        result = hedy.transpile(code, self.level)
        self.assertEqual(expected, result.code)
        self.assertEqual(False, result.has_turtle)



