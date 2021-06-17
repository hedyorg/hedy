import unittest
import hedy
import sys
import io
from contextlib import contextmanager

#
# This code let's us capture std out to also execute the generated Python
# and check its output
#

@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

def run_code(code):
    code = "import random\n" + code
    with captured_output() as (out, err):
        exec(code)
    return out.getvalue().strip()

#
# Tests for helper functions
#

class TestsForMultipleLevels(unittest.TestCase):
    max_level = 10

    def test_print_with_list_var_random(self):
        min_level = 2
        max_level = 5
        for i in range(min_level, max_level + 1):
            result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint dieren at random", i)
            self.assertEqual(result, "dieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(random.choice(dieren))")
            self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])
            print('Passed at level ', i)

        min_level = 6
        max_level = 10
        for i in range(min_level, max_level + 1):
            result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint dieren at random", i)
            self.assertEqual(result, "dieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(str(random.choice(dieren)))")
            self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])
            print('Passed at level ', i)

        result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint(dieren at random)", 11)
        self.assertEqual(result, "dieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(str(random.choice(dieren)))")
        self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])
        print('Passed at level ', 11)

        min_level = 12
        max_level = 19
        for i in range(min_level, max_level + 1):
            result = hedy.transpile("dieren is ['Hond', 'Kat', 'Kangoeroe']\nprint(dieren[random])", i)
            self.assertEqual(result, "dieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(str(random.choice(dieren)))")
            self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])
            print('Passed at level ', i)

        min_level = 20
        max_level = 22
        for i in range(min_level, max_level + 1):
            result = hedy.transpile("dieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(dieren[random])", i)
            self.assertEqual(result, "dieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(str(random.choice(dieren)))")
            self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])
            print('Passed at level ', i)



    def test_parse_error_shows_right_level(self):
        """Check that a parse error that can't be fixed by downgrading the level is propagated properly."""

        # This isn't correct Hedy at level 5 nor level 4
        try:
            hedy.transpile("printHelloworld!", 5)
            self.fail('Should have thrown')
        except hedy.HedyException as e:
            self.assertEqual(e.error_code, 'Parse')
            self.assertEqual(e.arguments.get('level'), 5)

    # def test_print_undefined_var(self):
    #     min_level = 7
    #
    #     for i in range(min_level, self.max_level + 1):
    #         with self.assertRaises(Exception) as context:
    #             result = hedy.transpile("print naam", i)
    #         self.assertEqual(str(context.exception), 'VarUndefined')
    #         print('Passed at level ', i)




