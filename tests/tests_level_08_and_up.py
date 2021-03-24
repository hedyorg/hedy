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
    with captured_output() as (out, err):
        exec(code)
    return out.getvalue().strip()

#
# Tests for helper functions
#

class TestsForMultipleLevels(unittest.TestCase):
    max_level = 7

    def test_print_with_list_var_random(self):
        min_level = 2
        max_level = 5
        for i in range(min_level, max_level + 1):
            result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint dieren at random", i)
            self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(random.choice(dieren))")
            self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])
            print('Passed at level ', i)

        min_level = 6
        max_level = 7
        for i in range(min_level, max_level + 1):
            result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint dieren at random", i)
            self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(str(random.choice(dieren)))")
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











class TestsLevel8(unittest.TestCase):
    def test_list(self):
        result = hedy.transpile("""
a is 1, 2
a is a at random
""", 8)
        self.assertEqual(result, """import random
a = [1, 2]
a = random.choice(a)
""")

    def test_valid_assignments(self):
        result = hedy.transpile("""
a is 8
a is 88
b is ""
b is 'string'
b is "string"
c is 1.2
c is 10e10
list is 1, 2, 3, 4
d is list at a
d is list at random
e is ask
e is ask "what " a " je lievelingskleur"
"""
, 8)
        self.assertEqual(result, """import random
a = 8
a = 88
b = ""
b = 'string'
b = "string"
c = 1.2
c = 10e10
list = [1, 2, 3, 4]
d = list[a]
d = random.choice(list)
e = input()
e = input("what " + a + " je lievelingskleur")
""")

    def test_calculations(self):
        result = hedy.transpile("""
a is 2 = 2
a is 2 < 2
a is 2 > 2
a is 2 <= 2
a is 2 >= 2
a is 2 + 2
a is 2 - 2
a is 2 * 2
a is 2 / 2
a is 2 % 2
a is 2 + 2 * 8
a is (2 + 2) * 8
a is 2 - -2
a is a - -a
a is a at a + 2 * 3
""", 8)
        self.assertEqual(result, """import random
a = 2 == 2
a = 2 < 2
a = 2 > 2
a = 2 <= 2
a = 2 >= 2
a = 2 + 2
a = 2 - 2
a = 2 * 2
a = 2 / 2
a = 2 % 2
a = 2 + 2 * 8
a = (2 + 2) * 8
a = 2 - -2
a = a - -a
a = a[a] + 2 * 3
""")

    # TODO: test echo
    def test_builtin_functions(self):
        result = hedy.transpile("""
print
print "string" 1 a -1 2.8
a is ask
a is ask "string" 1 a -1 2.8

""", 8)
        self.assertEqual(result, """import random
print()
print("string", 1, a, -1, 2.8)
a = input()
a = input("string" + 1 + a + -1 + 2.8)
""")


    def test_for_loop(self):
        result = hedy.transpile("""
for a in range 2 to 4
    a is a + 2
    b is b + 2
""", 8)
        self.assertEqual(result, """import random
for a in range(2, 4):
    a = a + 2
    b = b + 2
""")

    def test_if_elif_else(self):
        result = hedy.transpile("""
if a = 1
    x is 2
elif a = 2
    x is 22
else
    x is 222
""", 8)
        self.assertEqual(result, """import random
if a == 1:
    x = 2
elif a == 2:
    x = 22
else:
    x = 222
""")

class TestsLevel9(unittest.TestCase):
    def test_list(self):
        result = hedy.transpile("""
a is 1, 2
a is a at random
""", 9)
        self.assertEqual(result, """import random
a = [1, 2]
a = random.choice(a)
""")

    def test_valid_assignments(self):
        result = hedy.transpile("""
a is 8
a is 88
b is ""
b is 'string'
b is "string"
c is 1.2
c is 10e10
list is 1, 2, 3, 4
d is list at a
d is list at random
e is ask
e is ask "what " a " je lievelingskleur"
"""
, 9)
        self.assertEqual(result, """import random
a = 8
a = 88
b = ""
b = 'string'
b = "string"
c = 1.2
c = 10e10
list = [1, 2, 3, 4]
d = list[a]
d = random.choice(list)
e = input()
e = input("what " + a + " je lievelingskleur")
""")

    def test_calculations(self):
        result = hedy.transpile("""
a is 2 = 2
a is 2 < 2
a is 2 > 2
a is 2 <= 2
a is 2 >= 2
a is 2 + 2
a is 2 - 2
a is 2 * 2
a is 2 / 2
a is 2 % 2
a is 2 + 2 * 8
a is (2 + 2) * 8
a is 2 - -2
a is a - -a
a is a at a + 2 * 3
""", 9)
        self.assertEqual(result, """import random
a = 2 == 2
a = 2 < 2
a = 2 > 2
a = 2 <= 2
a = 2 >= 2
a = 2 + 2
a = 2 - 2
a = 2 * 2
a = 2 / 2
a = 2 % 2
a = 2 + 2 * 8
a = (2 + 2) * 8
a = 2 - -2
a = a - -a
a = a[a] + 2 * 3
""")

    # TODO: test echo
    def test_builtin_functions(self):
        result = hedy.transpile("""
print
print "string" 1 a -1 2.8
a is ask
a is ask "string" 1 a -1 2.8
""", 9)
        self.assertEqual(result, """import random
print()
print("string", 1, a, -1, 2.8)
a = input()
a = input("string" + 1 + a + -1 + 2.8)
""")


    def test_for_loop(self):
        result = hedy.transpile("""
for a in range 2 to 4:
    a is a + 2
    b is b + 2
""", 9)
        self.assertEqual(result, """import random
for a in range(2, 4):
    a = a + 2
    b = b + 2
""")

    def test_if_elif_else(self):
        result = hedy.transpile("""
if a = 1:
    x is 2
elif a = 2:
    x is 22
else:
    x is 222
""", 9)
        self.assertEqual(result, """import random
if a == 1:
    x = 2
elif a == 2:
    x = 22
else:
    x = 222
""")

    def test_nesting(self):
        result = hedy.transpile("""
for b in range 1 to 2:
    for a in range 1 to 2:
        if a = 1:
            if a = 2:
                x is 2
            else:
                x is 22
        else:
            x is 222

""", 9)
        self.assertEqual(result, """import random
for b in range(1, 2):
    for a in range(1, 2):
        if a == 1:
            if a == 2:
                x = 2
            else:
                x = 22
        else:
            x = 222
""")

class TestsLevel10(unittest.TestCase):
    def test_list(self):
        result = hedy.transpile("""
a is 1, 2
a is a at random
""", 10)
        self.assertEqual(result, """import random
a = [1, 2]
a = random.choice(a)
""")

    def test_valid_assignments(self):
        result = hedy.transpile("""
a is 8
a is 88
b is ""
b is 'string'
b is "string"
c is 1.2
c is 10e10
list is 1, 2, 3, 4
d is list at a
d is list at random
e is ask
e is ask "what " a " je lievelingskleur"
"""
, 10)
        self.assertEqual(result, """import random
a = 8
a = 88
b = ""
b = 'string'
b = "string"
c = 1.2
c = 10e10
list = [1, 2, 3, 4]
d = list[a]
d = random.choice(list)
e = input()
e = input("what " + a + " je lievelingskleur")
""")

    def test_calculations(self):
        result = hedy.transpile("""
a is 2 = 2
a is 2 < 2
a is 2 > 2
a is 2 <= 2
a is 2 >= 2
a is 2 + 2
a is 2 - 2
a is 2 * 2
a is 2 / 2
a is 2 % 2
a is 2 + 2 * 8
a is (2 + 2) * 8
a is 2 - -2
a is a - -a
a is a at a + 2 * 3
""", 10)
        self.assertEqual(result, """import random
a = 2 == 2
a = 2 < 2
a = 2 > 2
a = 2 <= 2
a = 2 >= 2
a = 2 + 2
a = 2 - 2
a = 2 * 2
a = 2 / 2
a = 2 % 2
a = 2 + 2 * 8
a = (2 + 2) * 8
a = 2 - -2
a = a - -a
a = a[a] + 2 * 3
""")

    # TODO: test echo
    def test_builtin_functions(self):
        result = hedy.transpile("""
print
print "string" 1 a -1 2.8
a is ask
a is ask "string" 1 a -1 2.8

""", 10)
        self.assertEqual(result, """import random
print()
print("string", 1, a, -1, 2.8)
a = input()
a = input("string" + 1 + a + -1 + 2.8)
""")

    def test_for_loop(self):
        result = hedy.transpile("""
for a in range 2 to 4:
    a is a + 2
    b is b + 2
""", 10)
        self.assertEqual(result, """import random
for a in range(2, 4):
    a = a + 2
    b = b + 2
""")

    def test_if_elif_else(self):
        result = hedy.transpile("""
if a = 1:
    x is 2
elif a = 2:
    x is 22
else:
    x is 222
""", 10)
        self.assertEqual(result, """import random
if a == 1:
    x = 2
elif a == 2:
    x = 22
else:
    x = 222
""")

    def test_nesting(self):
        result = hedy.transpile("""
for a in range 1 to 2:
    for b in range 1 to 2:
        if a = 1:
            if a = 2:
                x is 2
            else:
                x is 22
        else:
            x is 222

""", 10)
        self.assertEqual(result, """import random
for a in range(1, 2):
    for b in range(1, 2):
        if a == 1:
            if a == 2:
                x = 2
            else:
                x = 22
        else:
            x = 222
""")

class TestsLevel11(unittest.TestCase):
    def test_list(self):
        result = hedy.transpile("""
a is 1, 2
a is a at random
""", 11)
        self.assertEqual(result, """import random
a = [1, 2]
a = random.choice(a)
""")

    def test_valid_assignments(self):
        result = hedy.transpile("""
a is 8
a is 88
b is ""
b is 'string'
b is "string"
c is 1.2
c is 10e10
list is 1, 2, 3, 4
d is list at a
d is list at random
e is ask()
e is ask("what ", a, " je lievelingskleur")
"""
, 11)
        self.assertEqual(result, """import random
a = 8
a = 88
b = ""
b = 'string'
b = "string"
c = 1.2
c = 10e10
list = [1, 2, 3, 4]
d = list[a]
d = random.choice(list)
e = input()
e = input("what " + a + " je lievelingskleur")
""")

    def test_calculations(self):
        result = hedy.transpile("""
a is 2 = 2
a is 2 < 2
a is 2 > 2
a is 2 <= 2
a is 2 >= 2
a is 2 + 2
a is 2 - 2
a is 2 * 2
a is 2 / 2
a is 2 % 2
a is 2 + 2 * 8
a is (2 + 2) * 8
a is 2 - -2
a is a - -a
a is a at a + 2 * 3
""", 11)
        self.assertEqual(result, """import random
a = 2 == 2
a = 2 < 2
a = 2 > 2
a = 2 <= 2
a = 2 >= 2
a = 2 + 2
a = 2 - 2
a = 2 * 2
a = 2 / 2
a = 2 % 2
a = 2 + 2 * 8
a = (2 + 2) * 8
a = 2 - -2
a = a - -a
a = a[a] + 2 * 3
""")

    # TODO: test echo
    def test_builtin_functions(self):
        result = hedy.transpile("""
print()
print("string", 1, a, -1, 2.8)
a is ask()
a is ask("string", 1, a, -1, 2.8)

""", 11)
        self.assertEqual(result, """import random
print()
print("string", 1, a, -1, 2.8)
a = input()
a = input("string" + 1 + a + -1 + 2.8)
""")


    def test_for_loop(self):
        result = hedy.transpile("""
for a in range(2, 4):
    a is a + 2
    b is b + 2
""", 11)
        self.assertEqual(result, """import random
for a in range(2, 4):
    a = a + 2
    b = b + 2
""")

    def test_if_elif_else(self):
        result = hedy.transpile("""
if a = 1:
    x is 2
elif a = 2:
    x is 22
else:
    x is 222
""", 11)
        self.assertEqual(result, """import random
if a == 1:
    x = 2
elif a == 2:
    x = 22
else:
    x = 222
""")

    def test_nesting(self):
        result = hedy.transpile("""
for b in range(1, 2):
    for a in range(1, 2):
        if a = 1:
            if a = 2:
                x is 2
            else:
                x is 22
        else:
            x is 222

""", 11)
        self.assertEqual(result, """import random
for b in range(1, 2):
    for a in range(1, 2):
        if a == 1:
            if a == 2:
                x = 2
            else:
                x = 22
        else:
            x = 222
""")

class TestsLevel12(unittest.TestCase):
    def test_list(self):
        result = hedy.transpile("""
a is []
a is [1]
a is [1, 2]
a is a[random]
""", 12)
        self.assertEqual(result, """import random
a = []
a = [1]
a = [1, 2]
a = random.choice(a)
""")

    def test_valid_assignments(self):
        result = hedy.transpile("""
a is 8
a is 88
b is ""
b is 'string'
b is "string"
c is 1.2
c is 10e10
list is []
list is [1, 2, 3, 4]
d is list[a]
d is list[random]
e is ask()
e is ask("what ", a, " je lievelingskleur")
"""
, 12)
        self.assertEqual(result, """import random
a = 8
a = 88
b = ""
b = 'string'
b = "string"
c = 1.2
c = 10e10
list = []
list = [1, 2, 3, 4]
d = list[a]
d = random.choice(list)
e = input()
e = input("what " + a + " je lievelingskleur")
""")

    def test_calculations(self):
        result = hedy.transpile("""
a is 2 = 2
a is 2 < 2
a is 2 > 2
a is 2 <= 2
a is 2 >= 2
a is 2 + 2
a is 2 - 2
a is 2 * 2
a is 2 / 2
a is 2 % 2
a is 2 + 2 * 8
a is (2 + 2) * 8
a is 2 - -2
a is a - -a
a is a[a] + 2 * 3
""", 12)
        self.assertEqual(result, """import random
a = 2 == 2
a = 2 < 2
a = 2 > 2
a = 2 <= 2
a = 2 >= 2
a = 2 + 2
a = 2 - 2
a = 2 * 2
a = 2 / 2
a = 2 % 2
a = 2 + 2 * 8
a = (2 + 2) * 8
a = 2 - -2
a = a - -a
a = a[a] + 2 * 3
""")

    # TODO: test echo
    def test_builtin_functions(self):
        result = hedy.transpile("""
print()
print("string", 1, a, -1, 2.8)
a is ask()
a is ask("string", 1, a, -1, 2.8)

""", 12)
        self.assertEqual(result, """import random
print()
print("string", 1, a, -1, 2.8)
a = input()
a = input("string" + 1 + a + -1 + 2.8)
""")


    def test_for_loop(self):
        result = hedy.transpile("""
for a in range(2, 4):
    a is a + 2
    b is b + 2
""", 12)
        self.assertEqual(result, """import random
for a in range(2, 4):
    a = a + 2
    b = b + 2
""")

    def test_if_elif_else(self):
        result = hedy.transpile("""
if a = 1:
    x is 2
elif a = 2:
    x is 22
else:
    x is 222
""", 12)
        self.assertEqual(result, """import random
if a == 1:
    x = 2
elif a == 2:
    x = 22
else:
    x = 222
""")

    def test_nesting(self):
        result = hedy.transpile("""
for a in range(1, 2):
    for b in range(1, 2):
        if a = 1:
            if a = 2:
                x is 2
            else:
                x is 22
        else:
            x is 222

""", 12)
        self.assertEqual(result, """import random
for a in range(1, 2):
    for b in range(1, 2):
        if a == 1:
            if a == 2:
                x = 2
            else:
                x = 22
        else:
            x = 222
""")

class TestsLevel13(unittest.TestCase):
    def test_list(self):
        result = hedy.transpile("""
a = []
a = [1]
a = [1, 2]
a = a[random]
""", 13)
        self.assertEqual(result, """import random
a = []
a = [1]
a = [1, 2]
a = random.choice(a)
""")

    def test_valid_assignments(self):
        result = hedy.transpile("""
a = 8
a = 88
b = ""
b = 'string'
b = "string"
c = 1.2
c = 10e10
list = []
list = [1, 2, 3, 4]
d = list[a]
d = list[random]
e = ask()
e = ask("what ", a, " je lievelingskleur")
"""
, 13)
        self.assertEqual(result, """import random
a = 8
a = 88
b = ""
b = 'string'
b = "string"
c = 1.2
c = 10e10
list = []
list = [1, 2, 3, 4]
d = list[a]
d = random.choice(list)
e = input()
e = input("what " + a + " je lievelingskleur")
""")

    def test_calculations(self):
        result = hedy.transpile("""
a = 2 == 2
a = 2 < 2
a = 2 > 2
a = 2 <= 2
a = 2 >= 2
a = 2 + 2
a = 2 - 2
a = 2 * 2
a = 2 / 2
a = 2 % 2
a = 2 + 2 * 8
a = (2 + 2) * 8
a = 2 - -2
a = a - -a
a = a[a] + 2 * 3
""", 13)
        self.assertEqual(result, """import random
a = 2 == 2
a = 2 < 2
a = 2 > 2
a = 2 <= 2
a = 2 >= 2
a = 2 + 2
a = 2 - 2
a = 2 * 2
a = 2 / 2
a = 2 % 2
a = 2 + 2 * 8
a = (2 + 2) * 8
a = 2 - -2
a = a - -a
a = a[a] + 2 * 3
""")

    # TODO: test echo
    def test_builtin_functions(self):
        result = hedy.transpile("""
print()
print("string", 1, a, -1, 2.8)
a = ask()
a = ask("string", 1, a, -1, 2.8)

""", 13)
        self.assertEqual(result, """import random
print()
print("string", 1, a, -1, 2.8)
a = input()
a = input("string" + 1 + a + -1 + 2.8)
""")

    def test_for_loop(self):
        result = hedy.transpile("""
for a in range(2, 4):
    a = a + 2
    b = b + 2
""", 13)
        self.assertEqual(result, """import random
for a in range(2, 4):
    a = a + 2
    b = b + 2
""")

    def test_if_elif_else(self):
        result = hedy.transpile("""
if a == 1:
    x = 2
elif a == 2:
    x = 22
else:
    x = 222
""", 13)
        self.assertEqual(result, """import random
if a == 1:
    x = 2
elif a == 2:
    x = 22
else:
    x = 222
""")

    def test_nesting(self):
        result = hedy.transpile("""
for a in range(1, 2):
    for b in range(1, 2):
        if a == 1:
            if a == 2:
                x = 2
            else:
                x = 22
        else:
            x = 222
""", 13)
        self.assertEqual(result, """import random
for a in range(1, 2):
    for b in range(1, 2):
        if a == 1:
            if a == 2:
                x = 2
            else:
                x = 22
        else:
            x = 222
""")

if __name__ == '__main__':
    unittest.main()



    # python = transpile(tree)
    # print(python)
    #
    # exec(python)
