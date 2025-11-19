import textwrap

from parameterized import parameterized

import exceptions
import hedy
from hedy_sourcemap import SourceRange
from tests.Tester import HedyTester, SkippedMapping


class TestsLevel16(HedyTester):
    level = 16

    def test_print_list_var(self):
        code = textwrap.dedent("""\
            dieren is ['Hond', 'Kat', 'Kangoeroe']
            print dieren[1]""")

        expected = self.dedent(
            "dieren = Value([Value('Hond'), Value('Kat'), Value('Kangoeroe')])",
            self.list_access_transpiled('dieren.data[int(1)-1]'),
            "print(f'''{dieren.data[int(1)-1]}''')")

        check_in_list = (lambda x: HedyTester.run_code(x) == 'Hond')

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=check_in_list
        )

    def test_create_empty_list(self):
        code = "friends = []"
        expected = "friends = Value([])"

        self.multi_level_tester(
            code=code,
            unused_allowed=True,
            expected=expected
        )

    @parameterized.expand([
        ('42', 42),
        ('-1', -1),
        ('1.5', 1.5),
        ('-0.7', -0.7)
    ])
    def test_create_list_single_number_item(self, item_code, expected_value):
        code = f"friends = [{item_code}]"
        expected = f"friends = Value([Value({item_code}, num_sys='Latin')])"

        check_in_list = (lambda x: HedyTester.run_code(x) == expected_value)

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            extra_check_function=check_in_list
        )

    @parameterized.expand([
        ("'Ashli'", "'Ashli'"),
        ("'\"Ashli\"'", "'\"Ashli\"'"),
        ('"Ashli"', "'Ashli'"),
        ('"Ashli\'s"', "'Ashli\\\'s'")
    ])
    def test_create_list_single_text_item(self, item_code, expected_value):
        code = f"friends = [{item_code}]"
        expected = f"friends = Value([Value({expected_value})])"

        check_in_list = (lambda x: HedyTester.run_code(x) == expected_value)

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            extra_check_function=check_in_list
        )

    @parameterized.expand([
        ("'Alice', 'Ben'", ["'Alice'", "'Ben'"]),
        ("'\"Alice\"', '\"Ben\"'", ["'\"Alice\"'", "'\"Ben\"'"]),
        ('"Alice", "Ben"', ["'Alice'", "'Ben'"]),
        ('"Alice\'s", "Ben\'s"', ["'Alice\\'s'", "'Ben\\'s'"]),
    ])
    def test_create_list_multi_text(self, items_code, expected_items):
        code = f"friends = [{items_code}]"
        expected = f"""friends = Value([{', '.join([f"Value({i})" for i in expected_items])}])"""

        check_in_list = (lambda x: HedyTester.run_code(x) in expected_items)

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            extra_check_function=check_in_list
        )

    @parameterized.expand([
        ('1, 3, 5', [1, 3, 5]),
        ('-1, -2, -5', [-1, -2, -5]),
        ('1.5, 2.6, 3.7', [1.5, 2.6, 3.7]),
        ('-0.1, -5.6', [-0.1, -5.6])
    ])
    def test_create_list_multi_numbers(self, items_code, expected_items):
        code = f"friends = [{items_code}]"
        expected = f"""friends = Value([{', '.join([f"Value({i}, num_sys='Latin')" for i in expected_items])}])"""

        check_in_list = (lambda x: HedyTester.run_code(x) in expected_items)

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            extra_check_function=check_in_list
        )

    def test_add_to_empty_list(self):
        code = textwrap.dedent("""\
            friends = []
            add 'Ashli' to friends
            print friends[1]""")

        expected = self.dedent(
            "friends = Value([])",
            "friends.data.append(Value('Ashli'))",
            self.list_access_transpiled('friends.data[int(1)-1]'),
            "print(f'''{friends.data[int(1)-1]}''')")

        check_in_list = (lambda x: HedyTester.run_code(x) == 'Ashli')

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=check_in_list
        )

    def test_print_list_var_arabic_number(self):
        code = textwrap.dedent("""\
            dieren is ['Hond', 'Kat', 'Kangoeroe']
            print dieren[١]""")

        expected = self.dedent(
            "dieren = Value([Value('Hond'), Value('Kat'), Value('Kangoeroe')])",
            self.list_access_transpiled('dieren.data[int(1)-1]'),
            "print(f'''{dieren.data[int(1)-1]}''')")

        check_in_list = (lambda x: HedyTester.run_code(x) == 'Hond')

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=check_in_list,
            skip_faulty=False
        )

    def test_print_list_commas(self):
        code = textwrap.dedent("""\
            szamok1 = ['1' , '2' , '3' , '4' , '5']
            print szamok1[random]""")

        expected = textwrap.dedent("""\
            szamok1 = Value([Value('1'), Value('2'), Value('3'), Value('4'), Value('5')])
            print(f'''{random.choice(szamok1.data)}''')""")

        szamok1 = ['1', '2', '3', '4', '5']
        check_in_list = (lambda x: HedyTester.run_code(x) in szamok1)

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=check_in_list
        )

    def test_list_access_space(self):
        code = textwrap.dedent("""\
            szamok1 = [ '1' , '2' , '3' , '4' , '5' ]
            print szamok1 [random]""")

        expected = textwrap.dedent("""\
            szamok1 = Value([Value('1'), Value('2'), Value('3'), Value('4'), Value('5')])
            print(f'''{random.choice(szamok1.data)}''')""")
        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    def test_print_list_access(self):
        code = textwrap.dedent("""\
            fruit is ['banaan', 'appel', 'kers']
            print fruit[1]""")
        expected = self.dedent(
            "fruit = Value([Value('banaan'), Value('appel'), Value('kers')])",
            self.list_access_transpiled('fruit.data[int(1)-1]'),
            "print(f'''{fruit.data[int(1)-1]}''')")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    def test_print_list_access_non_latin(self):
        code = textwrap.dedent("""\
            vrienden = ['Ahmed', 'Ben', 'Cayden']
            geluksgetallen = [15, 18, 6]
            voor म in bereik 1, 3
               print 'het geluksgetal van ' vrienden[म]
               print 'is ' geluksgetallen[म]""")
        expected = self.dedent(
            f"""vrienden = {self.list_transpiled("'Ahmed'", "'Ben'", "'Cayden'")}""",
            f"""geluksgetallen = {self.list_transpiled(15, 18, 6)}""",
            self.for_loop('म', 1, 3),
            (self.list_access_transpiled('vrienden.data[int(म.data)-1]'), '  '),
            ("print(f'''het geluksgetal van {vrienden.data[int(म.data)-1]}''')", '  '),
            (self.list_access_transpiled('geluksgetallen.data[int(म.data)-1]'), '  '),
            ("print(f'''is {geluksgetallen.data[int(म.data)-1]}''')", '  '),
            ("time.sleep(0.1)", '  '))

        self.single_level_tester(
            code=code,
            expected=expected,
            lang='nl',
            extra_check_function=self.is_not_turtle()
        )

    def test_list_access_var(self):
        code = textwrap.dedent("""\
            fruit = ['banaan', 'appel', 'kers']
            eerstefruit = fruit[1]
            print eerstefruit""")
        expected = self.dedent(
            "fruit = Value([Value('banaan'), Value('appel'), Value('kers')])",
            self.list_access_transpiled('fruit.data[int(1)-1]'),
            "eerstefruit = fruit.data[int(1)-1]",
            "print(f'''{eerstefruit}''')")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    def test_access_plus_2(self):
        code = textwrap.dedent("""\
            a = 1 + 2 + 3
            print a""")
        expected = textwrap.dedent("""\
            a = Value(1 + 2 + 3, num_sys='Latin')
            print(f'''{a}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    def test_access_plus(self):
        code = textwrap.dedent("""\
            lijst is [1, 2, 3]
            optellen is lijst[1] + lijst[2]
            optellen is optellen + lijst[3]
            print optellen""")
        expected = self.dedent(
            "lijst = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(3, num_sys='Latin')])",
            self.list_access_transpiled('lijst.data[int(1)-1]'),
            self.list_access_transpiled('lijst.data[int(2)-1]'),
            f"optellen = Value({self.sum_transpiled('lijst.data[int(1)-1]', 'lijst.data[int(2)-1]')}"
            f", num_sys=get_num_sys(lijst.data[int(1)-1]))",
            self.list_access_transpiled('lijst.data[int(3)-1]'),
            f"""\
            optellen = Value({self.sum_transpiled('optellen', 'lijst.data[int(3)-1]')}, num_sys=get_num_sys(optellen))
            print(f'''{{optellen}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    def test_list_access_random(self):
        code = textwrap.dedent("""\
            fruit is ['banaan', 'appel', 'kers']
            randomfruit is fruit[random]
            print randomfruit""")
        expected = self.dedent(
            "fruit = Value([Value('banaan'), Value('appel'), Value('kers')])",
            self.list_access_transpiled('random.choice(fruit.data)'),
            "randomfruit = random.choice(fruit.data)",
            "print(f'''{randomfruit}''')")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    def test_equality_list_access(self):
        code = textwrap.dedent("""\
            luiaard = 'luiaard'
            dieren is ['aap', 'goat', 'fish']
            if luiaard is dieren[1]
                print 'ja'""")

        expected = self.dedent(
            """\
            luiaard = Value('luiaard')
            dieren = Value([Value('aap'), Value('goat'), Value('fish')])""",
            self.list_access_transpiled('dieren.data[int(1)-1]'),
            """\
            if luiaard.data == dieren.data[int(1)-1].data:
              print(f'''ja''')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            skip_faulty=False
        )

    @parameterized.expand(HedyTester.comparison_commands)
    def test_comparison_with_list_access(self, comparison):
        code = textwrap.dedent(f"""\
            balletje = 0
            bingo_getallen is [11, 17, 21]
            if balletje {comparison} bingo_getallen[1]
                print 'ja'""")

        expected = self.dedent(
            f"""\
            balletje = Value(0, num_sys='Latin')
            bingo_getallen = {self.list_transpiled(11, 17, 21)}""",
            self.list_access_transpiled('bingo_getallen.data[int(1)-1]'),
            f"""\
            if balletje.data{comparison}bingo_getallen.data[int(1)-1].data:
              print(f'''ja''')""")

        self.single_level_tester(code=code, expected=expected)

    def test_access_empty(self):
        code = textwrap.dedent("""\
            luiaard = ''""")

        expected = HedyTester.dedent(
            """\
            luiaard = Value('')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            skip_faulty=False,
            unused_allowed=True
        )

    #
    # ask tests
    #
    def test_ask_with_list_var(self):
        code = textwrap.dedent("""\
            colors is ['orange', 'blue', 'green']
            favorite is ask 'Is your fav color' colors[1]""")

        expected = self.dedent(
            "colors = Value([Value('orange'), Value('blue'), Value('green')])",
            self.list_access_transpiled('colors.data[int(1)-1]'),
            self.input_transpiled('favorite', 'Is your fav color{colors.data[int(1)-1]}')
        )

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            unused_allowed=True,
            extra_check_function=self.is_not_turtle()
        )

    def test_ask_with_list(self):
        code = textwrap.dedent("""\
            colors is ['orange', 'blue', 'green']
            favorite is ask 'Is your fav color' colors""")

        expected = self.dedent(
            "colors = Value([Value('orange'), Value('blue'), Value('green')])",
            self.input_transpiled('favorite', f'Is your fav color{{colors}}'))

        self.multi_level_tester(
            code=code,
            max_level=17,
            unused_allowed=True,
            expected=expected
        )

    #
    # add/remove tests
    #
    def test_add_to_list(self):
        code = textwrap.dedent("""\
            color is ask 'what is your favorite color? '
            colors is ['green', 'red', 'blue']
            add color to colors
            print colors[random]""")

        expected = self.dedent(
            self.input_transpiled('color', 'what is your favorite color? '),
            "colors = Value([Value('green'), Value('red'), Value('blue')])",
            "colors.data.append(color)",
            self.list_access_transpiled('random.choice(colors.data)'),
            "print(f'''{random.choice(colors.data)}''')")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    def test_add_list_access_to_list(self):
        code = textwrap.dedent("""\
            colors1 is ['green', 'red', 'blue']
            colors2 is ['yellow', 'purple']
            add colors1[2] to colors2""")

        expected = self.dedent(
            """\
            colors1 = Value([Value('green'), Value('red'), Value('blue')])
            colors2 = Value([Value('yellow'), Value('purple')])
            colors2.data.append(colors1.data[int(2)-1])""")

        check_in_list = (lambda x: HedyTester.run_code(x) == 'red')  # check that 'red' was correctly appended

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=check_in_list
        )

    def test_remove_from_list(self):
        code = textwrap.dedent("""\
            colors is ['green', 'red', 'blue']
            color is ask 'what color to remove?'
            remove color from colors
            print colors[random]""")

        expected = self.dedent(
            "colors = Value([Value('green'), Value('red'), Value('blue')])",
            self.input_transpiled('color', 'what color to remove?'),
            self.remove_transpiled('colors', 'color'),
            self.list_access_transpiled('random.choice(colors.data)'),
            "print(f'''{random.choice(colors.data)}''')")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    def test_remove_list_access_from_list(self):
        code = textwrap.dedent("""\
        colors1 is ['green', 'red', 'blue']
        colors2 is ['red', 'purple']
        remove colors1[2] from colors2
        print colors2[1]""")

        expected = self.dedent(
            """\
            colors1 = Value([Value('green'), Value('red'), Value('blue')])
            colors2 = Value([Value('red'), Value('purple')])""",
            self.remove_transpiled('colors2', 'colors1.data[int(2)-1]'),
            self.list_access_transpiled('colors2.data[int(1)-1]'),
            "print(f'''{colors2.data[int(1)-1]}''')")

        check_removed_from_list = (lambda x: HedyTester.run_code(x) == 'purple')  # check that 'red' was removed

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=check_removed_from_list
        )

    def test_change_list_item_var(self):
        code = textwrap.dedent("""\
            l = [1, 2]
            x = 3
            l[1] = x""")

        expected = self.dedent(
            """\
            l = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])
            x = Value(3, num_sys='Latin')""",
            self.list_access_transpiled('l.data[int(1)-1]'),
            "l.data[int(1)-1] = x")

        self.single_level_tester(code=code, expected=expected)

    def test_change_list_item_number(self):
        code = textwrap.dedent("""\
        l = [1, 2]
        m = 2
        l[m] = 3""")

        expected = self.dedent(
            "l = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])",
            "m = Value(2, num_sys='Latin')",
            self.list_access_transpiled('l.data[int(m.data)-1]'),
            "l.data[int(m.data)-1] = Value(3, num_sys='Latin')")

        self.single_level_tester(code=code, expected=expected)

    def test_change_list_item_to_list_access(self):
        code = textwrap.dedent("""\
        a = [1, 2]
        b = [3, 4]
        a[1] = b[2]""")

        expected = self.dedent(
            "a = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])",
            "b = Value([Value(3, num_sys='Latin'), Value(4, num_sys='Latin')])",
            self.list_access_transpiled('a.data[int(1)-1]'),
            "a.data[int(1)-1] = b.data[int(2)-1]")

        self.multi_level_tester(code=code, expected=expected)

    def test_change_list_item_to_random_list_access(self):
        code = textwrap.dedent("""\
        a = [1, 2]
        b = [3, 4]
        a[1] = b[random]""")

        expected = self.dedent(
            "a = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])",
            "b = Value([Value(3, num_sys='Latin'), Value(4, num_sys='Latin')])",
            self.list_access_transpiled('a.data[int(1)-1]'),
            "a.data[int(1)-1] = random.choice(b.data)")

        self.multi_level_tester(code=code, expected=expected)

    def test_assign_list_missing_brackets_gives_error(self):
        code = textwrap.dedent("""\
        animals = 'chicken', 'horse', 'cow'
        print animals[random]""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.MissingBracketsException,
            max_level=17
        )

    def test_assign_list_missing_bracket_gives_error(self):
        code = textwrap.dedent("""\
        animals = ['chicken', 'horse', 'cow'
        print animals[random]""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.MissingBracketsException,
            max_level=17
        )

    def test_color_with_list_variable_runtime_gives_error(self):
        code = textwrap.dedent("""\
            c = ['red', 'green', 'blue']
            color c""")

        expected = self.dedent(
            "c = Value([Value('red'), Value('green'), Value('blue')])",
            self.color_transpiled('{c}')
        )

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            expected=expected,
        )

    def test_color_with_list_access_random(self):
        code = textwrap.dedent("""\
        colors = ['red', 'green', 'blue']
        color colors[random]""")

        expected = self.dedent(
            "colors = Value([Value('red'), Value('green'), Value('blue')])",
            self.color_transpiled('{random.choice(colors.data)}')
        )

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_equality_of_lists(self):
        code = textwrap.dedent("""\
        m is [1, 2]
        n is [1, 2]
        if m is n
            print 'success!'""")

        expected = textwrap.dedent("""\
        m = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])
        n = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])
        if m.data == n.data:
          print(f'''success!''')""")

        self.single_level_tester(code=code, expected=expected)

    @parameterized.expand(HedyTester.equality_comparison_commands)
    def test_equality_with_list_access_and_float(self, comparison):
        code = textwrap.dedent(f"""\
            numbers = [1.5, 2.9, 42.0]
            if numbers[1] {comparison} 1.5
                print 'meh'""")
        expected = self.dedent(
            "numbers = Value([Value(1.5, num_sys='Latin'), Value(2.9, num_sys='Latin'), Value(42.0, num_sys='Latin')])",
            self.list_access_transpiled('numbers.data[int(1)-1]'),
            f"""\
            if numbers.data[int(1)-1].data == 1.5:
              print(f'''meh''')""")

        self.single_level_tester(code=code, expected=expected)

    def test_equality_with_number_and_list_gives_error(self):
        code = textwrap.dedent("""\
        color is [5, 6, 7]
        if 1 is color
            print 'success!'""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidTypeCombinationException,
            max_level=16,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2
        )

    @parameterized.expand([
        ('"text"', "Value('text')"),
        ("'text'", "Value('text')"),
        ('1', "Value(1, num_sys='Latin')"),
        ('1.3', "Value(1.3, num_sys='Latin')"),
        ('[1, 2]', "Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])")])
    def test_inequality_vars(self, arg, exp):
        code = textwrap.dedent(f"""\
            a is {arg}
            b is {arg}
            if a != b
                b is 1""")

        expected = textwrap.dedent(f"""\
            a = {exp}
            b = {exp}
            if a.data!=b.data:
              b = Value(1, num_sys='Latin')""")

        self.single_level_tester(code=code, expected=expected)

    def test_inequality_list_access(self):
        code = textwrap.dedent("""\
            a = [1, 2]
            b = [1, 2]
            if a[2] != b[2]
                sleep""")

        expected = self.dedent(
            "a = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])",
            "b = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])",
            self.list_access_transpiled('a.data[int(2)-1]'),
            self.list_access_transpiled('b.data[int(2)-1]'),
            """\
            if a.data[int(2)-1].data!=b.data[int(2)-1].data:
              time.sleep(1)""")

        self.single_level_tester(code=code, expected=expected)

    def test_inequality_of_lists(self):
        code = textwrap.dedent(f"""\
            a = [1, 2]
            b = [1, 2]
            if a != b
                b = 1""")

        expected = textwrap.dedent(f"""\
            a = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])
            b = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])
            if a.data!=b.data:
              b = Value(1, num_sys='Latin')""")

        self.single_level_tester(code, expected=expected)

    @parameterized.expand([
        ('"text"', '1'),        # double-quoted text and number
        ("'text'", '1'),        # single-quoted text and number
        ('[1, 2]', '1'),        # list and number
        ('[1, 2]', "'text'")])  # list and text
    def test_inequality_with_diff_types_gives_error(self, left, right):
        code = textwrap.dedent(f"""\
            a = {left}
            b = {right}
            if a != b
                b = 1""")

        self.single_level_tester(code, exception=exceptions.InvalidTypeCombinationException)

    #
    # and/or commands
    #
    @parameterized.expand(['and', 'or'])
    def test_if_list_access_lhs_and_or(self, op):
        code = textwrap.dedent(f"""\
            colors = ['red', 'green', 'blue']
            if colors[1] == colors[2] {op} 1 == 1
                print 'red'""")

        expected = self.dedent(
            "colors = Value([Value('red'), Value('green'), Value('blue')])",
            self.list_access_transpiled('colors.data[int(1)-1]'),
            self.list_access_transpiled('colors.data[int(2)-1]'),
            f"""\
            if colors.data[int(1)-1].data == colors.data[int(2)-1].data {op} 1 == 1:
              print(f'''red''')""")

        self.single_level_tester(
            code=code,
            expected=expected,
        )

    #
    # in/not-in list commands
    #
    @parameterized.expand([
        ('in', 'Found'),
        ('not in', 'Not found')
    ])
    def test_if_in_not_in_list_with_strings(self, command, expected_output):
        code = textwrap.dedent(f"""\
            letters = ['a', 'b', 'c']
            if 'a' {command} letters
              print 'Found'
            else
              print 'Not found'""")

        expected = textwrap.dedent(f"""\
            letters = Value([Value('a'), Value('b'), Value('c')])
            if Value('a') {command} letters.data:
              print(f'''Found''')
            else:
              print(f'''Not found''')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            output=expected_output
        )

    @parameterized.expand([
        ('in', 'True'),
        ('not in', 'False')
    ])
    def test_if_number_in_not_in_list_with_numbers(self, operator, expected_output):
        code = textwrap.dedent(f"""\
        items is [1, 2, 3]
        if 1 {operator} items
          print 'True'
        else
          print 'False'""")

        expected = textwrap.dedent(f"""\
        items = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(3, num_sys='Latin')])
        if Value(1, num_sys='Latin') {operator} items.data:
          print(f'''True''')
        else:
          print(f'''False''')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            output=expected_output
        )

    @parameterized.expand([
        ('in', 'False'),
        ('not in', 'True')
    ])
    def test_if_text_in_not_in_list_with_numbers(self, operator, expected_output):
        code = textwrap.dedent(f"""\
            items is [1, 2, 3]
            if '1' {operator} items
              print 'True'
            else
              print 'False'""")

        expected = textwrap.dedent(f"""\
            items = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(3, num_sys='Latin')])
            if Value('1') {operator} items.data:
              print(f'''True''')
            else:
              print(f'''False''')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            output=expected_output
        )

    @parameterized.expand(['in', 'not in'])
    def test_unquoted_lhs_in_not_in_list_gives_error(self, operator):
        code = textwrap.dedent(f"""\
            items is [1, 2, 3]
            if a {operator} items
              print 'True'""")

        self.single_level_tester(
            code=code,
            skip_faulty=False,
            exception=hedy.exceptions.UnquotedAssignTextException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2
        )

    @parameterized.expand(['in', 'not in'])
    def test_undefined_rhs_in_not_in_list_gives_error(self, operator):
        code = textwrap.dedent(f"""\
            items is [1, 2, 3]
            if 1 {operator} list
              print 'True'""")

        self.single_level_tester(
            code=code,
            exception=hedy.exceptions.UndefinedVarException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2
        )

    def test_if_ar_number_list_with_latin_numbers(self):
        code = textwrap.dedent("""\
           a = [11, 22, 33]
           if ١١ in a
             print 'correct'""")

        expected = textwrap.dedent(f"""\
           a = {self.list_transpiled("11", "22", "33")}
           if {self.in_list_transpiled("Value(11, num_sys='Arabic')", 'a')}:
             print(f'''correct''')""")

        self.single_level_tester(code=code, expected=expected, output='correct')

    def test_if_ar_number_not_list_with_latin_numbers(self):
        code = textwrap.dedent("""\
           a is [22, 33, 44]
           if ١١ not in a
             print 'correct'""")

        expected = textwrap.dedent(f"""\
           a = {self.list_transpiled("22", "33", "44")}
           if {self.not_in_list_transpiled("Value(11, num_sys='Arabic')", 'a')}:
             print(f'''correct''')""")

        self.single_level_tester(code=code, expected=expected, output='correct')

    #
    # forward tests
    #
    def test_forward_with_list_variable_gives_error(self):
        code = textwrap.dedent("""\
        a = [1, 2, 3]
        forward a""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_forward_with_list_access_random(self):
        code = textwrap.dedent("""\
        directions = [10, 100, 360]
        forward directions[random]""")

        expected = self.dedent(
            f"directions = {self.list_transpiled(10, 100, 360)}",
            self.list_access_transpiled('random.choice(directions.data)'),
            self.forward_transpiled('random.choice(directions.data).data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    #
    # turn tests
    #
    def test_turn_with_list_variable_gives_error(self):
        code = textwrap.dedent("""\
        a = [45, 90, 180]
        turn a""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_turn_with_list_access_random(self):
        code = textwrap.dedent("""\
        directions = [10, 100, 360]
        turn directions[random]""")

        expected = self.dedent(
            f"directions = {self.list_transpiled(10, 100, 360)}",
            self.list_access_transpiled('random.choice(directions.data)'),
            self.turn_transpiled('random.choice(directions.data).data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    # TODO: if pressed tests failing for now
    # def test_if_pressed_with_list_and_for(self):
    #     code = textwrap.dedent("""\
    #     lijstje is ['kip', 'haan', 'kuiken']
    #     if x is pressed
    #         for dier in lijstje
    #             print dier""")

    #     expected = self.dedent("""\
    #     global_scope_ = dict()
    #     global_scope_["lijstje"] = Value([Value('kip'), Value('haan'), Value('kuiken')])
    #     if_pressed_mapping = {"else": "if_pressed_default_else"}
    #     if_pressed_mapping['x'] = 'if_pressed_x_'
    #     global if_pressed_x_
    #     def if_pressed_x_():
    #       for dier in (global_scope_.get("lijstje") or lijstje).data:
    #         print(f'''{global_scope_.get("dier") or dier}''')
    #         time.sleep(0.1)
    #     extensions.if_pressed(if_pressed_mapping)""")

    #     self.single_level_tester(code=code, expected=expected)

    @parameterized.expand(['number is', 'print', 'forward', 'turn'])
    def test_at_random_express(self, command):
        code = textwrap.dedent(f"""\
            numbers is [1, 2, 3]
            {command} numbers at random""")
        self.single_level_tester(code=code, exception=hedy.exceptions.InvalidAtCommandException, skip_faulty=False)

    def test_at_random_express_sleep(self):
        code = textwrap.dedent(f"""\
            prind skipping
            numbers is [1, 2, 3]
            sleep numbers at random""")

        expected = self.dedent(f"""\
            pass
            numbers = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(3, num_sys='Latin')])
            pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 15), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(3, 1, 3, 24), hedy.exceptions.InvalidAtCommandException)
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
        )

    # music tests
    def test_play_random(self):
        code = textwrap.dedent("""\
        notes = ['C4', 'E4', 'D4', 'F4', 'G4']
        play notes[random]""")

        expected = self.dedent(
            "notes = Value([Value('C4'), Value('E4'), Value('D4'), Value('F4'), Value('G4')])",
            self.play_transpiled('random.choice(notes.data).data')
        )

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=17
        )

    #
    # boolean values
    #
    def test_assign_list_var_boolean(self):
        code = "cond = [True, False, true, false]"
        expected = ("cond = Value([Value(True, bool_sys={True: 'True', False: 'False'}), "
                    "Value(False, bool_sys={True: 'True', False: 'False'}), "
                    "Value(True, bool_sys={True: 'true', False: 'false'}), "
                    "Value(False, bool_sys={True: 'true', False: 'false'})])")

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True
        )

    @parameterized.expand([('True', True, 'True', 'False'), ('true', True, 'true', 'false')])
    def test_cond_boolean(self, value, exp, exp_true, exp_false):
        code = textwrap.dedent(f"""\
            cond = {value}
            if cond is {value}
                sleep""")
        expected = textwrap.dedent(f"""\
            cond = Value({exp}, bool_sys={{True: '{exp_true}', False: '{exp_false}'}})
            if cond.data == {exp}:
              time.sleep(1)""")

        self.single_level_tester(
            code=code,
            expected=expected,
            translate=False
        )

# -----old level 17-----

        def test_if_with_indent(self):
            code = textwrap.dedent("""\
                naam is 'Hedy'
                if naam is 'Hedy':
                    print 'koekoek'""")
            expected = textwrap.dedent("""\
                naam = Value('Hedy')
                if naam.data == 'Hedy':
                  print(f'''koekoek''')""")

            self.single_level_tester(code=code, expected=expected)

        def test_if_with_equals_sign(self):
            code = textwrap.dedent("""\
                naam is 'Hedy'
                if naam == 'Hedy':
                    print 'koekoek'""")

            expected = textwrap.dedent("""\
                naam = Value('Hedy')
                if naam.data == 'Hedy':
                  print(f'''koekoek''')""")

            self.single_level_tester(code=code, expected=expected)

        def test_if_else(self):
            code = textwrap.dedent("""\
                antwoord is ask 'Hoeveel is 10 plus 10?'
                if antwoord is 20:
                    print 'Goedzo!'
                    print 'Het antwoord was inderdaad ' antwoord
                else:
                    print 'Foutje'
                    print 'Het antwoord moest zijn ' antwoord""")

            expected = self.dedent(
                self.input_transpiled('antwoord', 'Hoeveel is 10 plus 10?'),
                """\
                if antwoord.data == 20:
                  print(f'''Goedzo!''')
                  print(f'''Het antwoord was inderdaad {antwoord}''')
                else:
                  print(f'''Foutje''')
                  print(f'''Het antwoord moest zijn {antwoord}''')""")

            self.single_level_tester(code=code, expected=expected)

        #
        # boolean values
        #

        def test_cond_boolean(self):
            code = textwrap.dedent("""\
                cond = False
                if cond is True:
                    sleep""")
            expected = textwrap.dedent("""\
                cond = Value(False, bool_sys={True: 'True', False: 'False'})
                if cond.data == True:
                  time.sleep(1)""")

            self.multi_level_tester(
                code=code,
                expected=expected
            )

        def test_if_elif_boolean(self):
            code = textwrap.dedent("""\
                computerc = 'PC'
                userc = 'Hedy'
                print 'Pilihan komputer: ' computerc
                if userc is computerc and userc is 'Hedy':
                    print 'SERI'
                elif userc is 'PC' and userc is 'Hedy':
                    print 'HARI'
                else:
                    print 'Komputer'""")

            expected = textwrap.dedent("""\
                computerc = Value('PC')
                userc = Value('Hedy')
                print(f'''Pilihan komputer: {computerc}''')
                if userc.data == computerc.data and userc.data == 'Hedy':
                  print(f'''SERI''')
                elif userc.data == 'PC' and userc.data == 'Hedy':
                  print(f'''HARI''')
                else:
                  print(f'''Komputer''')""")

            self.single_level_tester(code=code, expected=expected)

        def test_snippet(self):
            code = textwrap.dedent("""\
                prijzen = ['1 miljoen', 'een appeltaart', 'niks']
                jouw_prijs = prijzen [random]
                print 'Je wint ' jouw_prijs
                if jouw_prijs== '1 miljoen' :
                    print 'Yess! Je bent rijk!'
                elif jouw_prijs == 'een appeltaart' :
                    print 'Heerlijk, een appeltaart!'
                else:
                    print 'Meer geluk volgende keer..'""")
            expected = self.dedent(
                "prijzen = Value([Value('1 miljoen'), Value('een appeltaart'), Value('niks')])",
                self.list_access_transpiled("random.choice(prijzen.data)"),
                """\
                jouw_prijs = random.choice(prijzen.data)
                print(f'''Je wint {jouw_prijs}''')
                if jouw_prijs.data == '1 miljoen':
                  print(f'''Yess! Je bent rijk!''')
                elif jouw_prijs.data == 'een appeltaart':
                  print(f'''Heerlijk, een appeltaart!''')
                else:
                  print(f'''Meer geluk volgende keer..''')"""
            )

            self.single_level_tester(code=code, expected=expected)

        def test_if_else_boolean(self):
            code = textwrap.dedent("""\
                computerc = 'PC'
                userc = 'Hedy'
                print 'Pilihan komputer: ' computerc
                if userc is computerc and userc is 'Hedy':
                    print 'SERI'
                else:
                    print 'Komputer'""")

            expected = textwrap.dedent("""\
                computerc = Value('PC')
                userc = Value('Hedy')
                print(f'''Pilihan komputer: {computerc}''')
                if userc.data == computerc.data and userc.data == 'Hedy':
                  print(f'''SERI''')
                else:
                  print(f'''Komputer''')""")

            self.single_level_tester(code=code, expected=expected)

        def test_for_loop_arabic(self):
            code = textwrap.dedent("""\
                for دورة in range ١ to ٥:
                    print دورة""")

            expected = self.dedent(
                self.for_loop('دورة', 1, 5, "'Arabic'"),
                (f"print(f'''{{دورة}}''')", '  '),
                ("time.sleep(0.1)", '  '))

            self.single_level_tester(
                code=code,
                expected=expected,
                expected_commands=['for', 'print'])

        @parameterized.expand(['and', 'or'])
        def test_if_list_access_lhs_and_or(self, op):
            code = textwrap.dedent(f"""\
                colors = ['red', 'green', 'blue']
                if colors[1] == colors[2] {op} 1 == 1:
                    print 'red'""")

            expected = self.dedent(
                "colors = Value([Value('red'), Value('green'), Value('blue')])",
                self.list_access_transpiled('colors.data[int(1)-1]'),
                self.list_access_transpiled('colors.data[int(2)-1]'),
                f"""\
                if colors.data[int(1)-1].data == colors.data[int(2)-1].data {op} 1 == 1:
                  print(f'''red''')""")

            self.single_level_tester(
                code=code,
                expected=expected,
            )

        def test_for_loop(self):
            code = textwrap.dedent("""\
                a is 2
                b is 3
                for a in range 2 to 4:
                    a is a + 2
                    b is b + 2""")
            expected = self.dedent(
                "a = Value(2, num_sys='Latin')",
                "b = Value(3, num_sys='Latin')",
                self.for_loop('a', 2, 4),
                (f"a = Value({self.sum_transpiled('a', 2)}, num_sys=get_num_sys(a))", '  '),
                (f"b = Value({self.sum_transpiled('b', 2)}, num_sys=get_num_sys(b))", '  '),
                ("time.sleep(0.1)", '  '))

            self.single_level_tester(code=code, expected=expected)

        def test_for_loop_no_colon_after_pressed_gives_error(self):
            code = textwrap.dedent("""\
            for a in range 2 to 4
                a = 1""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('for in range', 1)
            )

        def test_for_list_without_colon_gives_error(self):
            code = textwrap.dedent("""\
            dieren = ['cat', 'dog', 'parrot']
            for dier in dieren
                a = 1""")

            self.multi_level_tester(
                code=code,
                exception=exceptions.MissingColonException,
                extra_check_function=missing_colon_check('for in', 2)
            )

        def test_if__else(self):
            code = textwrap.dedent("""\
                a is 5
                if a is 1:
                    a is 2
                else:
                    a is 222""")
            expected = textwrap.dedent("""\
                a = Value(5, num_sys='Latin')
                if a.data == 1:
                  a = Value(2, num_sys='Latin')
                else:
                  a = Value(222, num_sys='Latin')""")
            self.single_level_tester(code=code, expected=expected)

        def test_forloop(self):
            code = textwrap.dedent("""\
                for i in range 1 to 10:
                    print i
                print 'wie niet weg is is gezien'""")
            expected = self.dedent(
                self.for_loop('i', 1, 10),
                (f"print(f'''{{i}}''')", '  '),
                ("time.sleep(0.1)", '  '),
                "print(f'''wie niet weg is is gezien''')")

            self.single_level_tester(code=code, expected=expected)

        def test_allow_space_after_else_line(self):
            code = textwrap.dedent("""\
                a is 1
                if a is 1:
                    print a
                else:
                    print 'nee'""")

            expected = textwrap.dedent("""\
                a = Value(1, num_sys='Latin')
                if a.data == 1:
                  print(f'''{a}''')
                else:
                  print(f'''nee''')""")

            self.multi_level_tester(
                max_level=17,
                code=code,
                expected=expected,
                expected_commands=['is', 'if', 'print', 'print']
            )

        #
        # while loop
        #

        def test_while_undefined_var(self):
            code = textwrap.dedent("""\
            while antwoord != 25:
                print 'hoera'""")

            self.single_level_tester(
                code=code,
                exception=hedy.exceptions.UndefinedVarException
            )

        def test_while_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            a = 1
            while a != 5
                a = a + 1""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('while', 2)
            )

        def test_while_equals_boolean(self):
            code = textwrap.dedent("""\
                cond is True
                while cond != False:
                  cond is False""")
            expected = textwrap.dedent("""\
                cond = Value(True, bool_sys={True: 'True', False: 'False'})
                while cond.data!=False:
                  cond = Value(False, bool_sys={True: 'True', False: 'False'})
                  time.sleep(0.1)""")

            self.multi_level_tester(
                code=code,
                expected=expected,
                skip_faulty=False
            )

        def test_allow_space_before_colon(self):
            code = textwrap.dedent("""\
                a is 1
                if a is 1  :
                    print a
                else:
                    print 'nee'""")

            expected = textwrap.dedent("""\
                a = Value(1, num_sys='Latin')
                if a.data == 1:
                  print(f'''{a}''')
                else:
                  print(f'''nee''')""")

            self.multi_level_tester(
                code=code,
                max_level=17,
                expected=expected
            )

        def test_if_under_else_in_for(self):
            # todo can me multitester with higher levels!
            code = textwrap.dedent("""\
                for i in range 0 to 10:
                    antwoord is ask 'Wat is 5*5'
                    if antwoord is 24:
                        print 'Dat is fout!'
                    else:
                        print 'Dat is goed!'
                    if antwoord is 25:
                        i is 10""")

            expected = self.dedent(
                self.for_loop('i', 0, 10),
                (self.input_transpiled('antwoord', 'Wat is 5*5'), '  '),
                ("""\
                if antwoord.data == 24:
                  print(f'''Dat is fout!''')
                else:
                  print(f'''Dat is goed!''')
                if antwoord.data == 25:
                  i = Value(10, num_sys='Latin')
                time.sleep(0.1)""", '  '))

            self.single_level_tester(code=code, expected=expected)

        def test_if_elif(self):
            code = textwrap.dedent("""\
                a is 5
                if a is 1:
                    a is 2
                elif a is 2:
                    a is 222""")
            expected = textwrap.dedent("""\
                a = Value(5, num_sys='Latin')
                if a.data == 1:
                  a = Value(2, num_sys='Latin')
                elif a.data == 2:
                  a = Value(222, num_sys='Latin')""")

            self.single_level_tester(code=code, expected=expected)

        def test_if_elif_french(self):
            code = textwrap.dedent("""\
                a est 5
                si a est 1:
                    a est 2
                sinon si a est 2:
                    a est 222""")
            expected = textwrap.dedent("""\
                a = Value(5, num_sys='Latin')
                if a.data == 1:
                  a = Value(2, num_sys='Latin')
                elif a.data == 2:
                  a = Value(222, num_sys='Latin')""")

            self.single_level_tester(code=code, expected=expected, lang='fr')

        def test_if_with_multiple_elifs(self):
            code = textwrap.dedent("""\
                a is 5
                if a is 1:
                    a is 2
                elif a is 4:
                    a is 3
                elif a is 2:
                    a is 222""")
            expected = textwrap.dedent("""\
                a = Value(5, num_sys='Latin')
                if a.data == 1:
                  a = Value(2, num_sys='Latin')
                elif a.data == 4:
                  a = Value(3, num_sys='Latin')
                elif a.data == 2:
                  a = Value(222, num_sys='Latin')""")

            self.single_level_tester(
                code=code, expected=expected, expected_commands=[
                    'is', 'if', 'is', 'elif', 'is', 'elif', 'is'])

        def test_if_in_list_with_string_var_gives_type_error(self):
            code = textwrap.dedent("""\
            items is 'red'
            if 'red' in items:
                a is 1""")
            self.multi_level_tester(
                code=code,
                extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
                exception=hedy.exceptions.InvalidArgumentTypeException
            )

        #
        # in/not in tests
        #
        def test_if_ar_number_list_with_latin_numbers(self):
            code = textwrap.dedent("""\
               a = [11, 22, 33]
               if ١١ in a:
                 print 'correct'""")

            expected = textwrap.dedent(f"""\
               a = {self.list_transpiled("11", "22", "33")}
               if {self.in_list_transpiled("Value(11, num_sys='Arabic')", 'a')}:
                 print(f'''correct''')""")

            self.single_level_tester(code=code, expected=expected, output='correct')

        def test_if_ar_number_not_list_with_latin_numbers(self):
            code = textwrap.dedent("""\
               a is [22, 33, 44]
               if ١١ not in a:
                 print 'correct'""")

            expected = textwrap.dedent(f"""\
               a = {self.list_transpiled("22", "33", "44")}
               if {self.not_in_list_transpiled("Value(11, num_sys='Arabic')", 'a')}:
                 print(f'''correct''')""")

            self.single_level_tester(code=code, expected=expected, output='correct')

        def test_equality_with_lists(self):
            code = textwrap.dedent("""\
                m is [1, 2]
                n is [1, 2]
                if m is n:
                    print 'JA!'""")

            expected = textwrap.dedent("""\
                m = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])
                n = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])
                if m.data == n.data:
                  print(f'''JA!''')""")

            self.multi_level_tester(
                code=code,
                expected=expected,
                max_level=17
            )

        def test_equality_with_incompatible_types_gives_error(self):
            code = textwrap.dedent("""\
            a is 'test'
            b is 15
            if a is b:
              c is 1""")
            self.multi_level_tester(
                code=code,
                extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
                exception=hedy.exceptions.InvalidTypeCombinationException
            )

        @parameterized.expand(HedyTester.comparison_commands)
        def test_comparisons(self, comparison):
            code = textwrap.dedent(f"""\
                leeftijd is ask 'Hoe oud ben jij?'
                if leeftijd {comparison} 12:
                    print 'Dan ben je jonger dan ik!'""")
            expected = self.dedent(
                self.input_transpiled('leeftijd', 'Hoe oud ben jij?'),
                f"""\
                if leeftijd.data{comparison}12:
                  print(f'''Dan ben je jonger dan ik!''')""")

            self.single_level_tester(code=code, expected=expected)

        @parameterized.expand(HedyTester.number_comparison_commands)
        def test_smaller_with_string_gives_type_error(self, comparison):
            code = textwrap.dedent(f"""\
            a is 'text'
            if a {comparison} 12:
                b is 1""")

            self.multi_level_tester(
                code=code,
                extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
                exception=hedy.exceptions.InvalidArgumentTypeException
            )

        def test_not_equal_string_literal(self):
            code = textwrap.dedent(f"""\
            if 'quoted' != 'string':
              sleep""")
            expected = textwrap.dedent(f"""\
            if 'quoted'!='string':
              time.sleep(1)""")

            self.multi_level_tester(
                code=code,
                expected=expected
            )

        @parameterized.expand([
            ("'text'", "Value('text')"),
            ('1', "Value(1, num_sys='Latin')"),
            ('1.3', "Value(1.3, num_sys='Latin')"),
            ('[1, 2]', "Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])")])
        def test_not_equal(self, arg, exp):
            code = textwrap.dedent(f"""\
                a = {arg}
                b = {arg}
                if a != b:
                    b = 1""")

            expected = textwrap.dedent(f"""\
                a = {exp}
                b = {exp}
                if a.data!=b.data:
                  b = Value(1, num_sys='Latin')""")

            self.multi_level_tester(
                code=code,
                expected=expected
            )

        @parameterized.expand([
            ("'text'", '1'),  # text and number
            ('[1, 2]', '1'),  # list and number
            ('[1, 2]', "'text'")])  # list and text
        def test_not_equal_with_diff_types_gives_error(self, left, right):
            code = textwrap.dedent(f"""\
            a = {left}
            b = {right}
            if a != b:
                b = 1""")

            self.multi_level_tester(
                code=code,
                extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
                exception=exceptions.InvalidTypeCombinationException
            )

        def test_if_pressed_with_color(self):
            code = textwrap.dedent("""\
                if x is pressed:
                    color 'red'""")

            expected = self.dedent(
                f"""\
                global_scope_ = dict()
                if_pressed_mapping = {{"else": "if_pressed_default_else"}}
                if_pressed_mapping['x'] = 'if_pressed_x_'
                global if_pressed_x_
                def if_pressed_x_():""",
                (self.color_transpiled('red'), '  '),
                "extensions.if_pressed(if_pressed_mapping)")

            self.multi_level_tester(
                code=code,
                expected=expected,
                extra_check_function=self.is_turtle()
            )

        def test_if_pressed_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if x is pressed
                a = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('if', 1)
            )

        def test_pressed_elif_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if x is pressed:
                a = 'correct'
            elif m is pressed
                a = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('elif', 3)
            )

        def test_pressed_if_else_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if x is pressed:
                a = 'correct'
            else
                a = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('else', 3)
            )

        def test_pressed_if_elif_else_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if x is pressed:
                a = 'correct'
            elif m is pressed:
                a = 'correct'
            else
                a = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('else', 5)
            )

        def test_if_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if 'a' is 'a'
                b = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('if', 1)
            )

        def test_elif_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if 'a' is 'a':
                b = 'colon!'
            elif 'a' is 'b'
                b = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('elif', 3)
            )

        def test_else_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if 'a' is 'a':
                b = 'colon!'
            else
                b = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('else', 3)
            )

        def test_if_elif_else_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if 'a' is 'a':
                b = 'colon!'
            elif 'a' is 'b':
                b = 'colon!'
            else
                b = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('else', 5)
            )

        def test_pressed_elif(self):
            code = textwrap.dedent("""\
            if a is pressed:
                print 'A'
            elif b is pressed:
                print 'B'
            else:
                print 'Other'""")

            expected = self.dedent("""\
            global_scope_ = dict()
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['a'] = 'if_pressed_a_'
            global if_pressed_a_
            def if_pressed_a_():
              print(f'''A''')
            if_pressed_mapping['b'] = 'if_pressed_b_'
            global if_pressed_b_
            def if_pressed_b_():
              print(f'''B''')
            if_pressed_mapping['else'] = 'if_pressed_else_'
            global if_pressed_else_
            def if_pressed_else_():
              print(f'''Other''')
            extensions.if_pressed(if_pressed_mapping)""")

            self.single_level_tester(code=code, expected=expected)

        def test_nested_functions(self):
            code = textwrap.dedent("""\
            define simple_function:
                define nested_function:
                    print 1
            call simple_function""")

            expected = textwrap.dedent("""\
            pass
            simple_function()""")

            skipped_mappings = [
                SkippedMapping(SourceRange(1, 1, 3, 34), hedy.exceptions.NestedFunctionException),
            ]

            self.single_level_tester(
                code=code,
                expected=expected,
                skipped_mappings=skipped_mappings,
            )

        def test_define_no_colon_gives_error(self):
            code = textwrap.dedent("""\
                define simple_function
                    a = 1
                call simple_function""")

            self.single_level_tester(
                code=code,
                exception=exceptions.MissingColonException,
                extra_check_function=missing_colon_check('define', 1)
            )

        def test_source_map(self):
            code = textwrap.dedent("""\
                for i in range 1 to 10:
                    print i
                print 'Ready or not, here I come!'""")

            excepted_code = self.dedent(
                self.for_loop('i', 1, 10),
                (f"print(f'''{{i}}''')", '  '),
                ("time.sleep(0.1)", '  '),
                "print(f'''Ready or not, here I come!''')")

            expected_source_map = {
                '1/5-1/6': '1/12-1/13',
                '2/11-2/12': '1/1-1/2',
                '2/5-2/12': '3/1-3/18',
                '1/1-2/21': '1/1-4/18',
                '3/1-3/35': '5/1-5/41',
                '1/1-3/36': '1/1-5/41'
            }

            self.single_level_tester(code, expected=excepted_code)
            self.source_map_tester(code=code, expected_source_map=expected_source_map)

    def missing_colon_check(command, line_number):
        return lambda c: (c.exception.arguments['line_number'] == line_number and
                          c.exception.arguments['command'] == command)

        def test_if_with_indent(self):
            code = textwrap.dedent("""\
                naam is 'Hedy'
                if naam is 'Hedy':
                    print 'koekoek'""")
            expected = textwrap.dedent("""\
                naam = Value('Hedy')
                if naam.data == 'Hedy':
                  print(f'''koekoek''')""")

            self.single_level_tester(code=code, expected=expected)

        def test_if_with_equals_sign(self):
            code = textwrap.dedent("""\
                naam is 'Hedy'
                if naam == 'Hedy':
                    print 'koekoek'""")

            expected = textwrap.dedent("""\
                naam = Value('Hedy')
                if naam.data == 'Hedy':
                  print(f'''koekoek''')""")

            self.single_level_tester(code=code, expected=expected)

        def test_if_else(self):
            code = textwrap.dedent("""\
                antwoord is ask 'Hoeveel is 10 plus 10?'
                if antwoord is 20:
                    print 'Goedzo!'
                    print 'Het antwoord was inderdaad ' antwoord
                else:
                    print 'Foutje'
                    print 'Het antwoord moest zijn ' antwoord""")

            expected = self.dedent(
                self.input_transpiled('antwoord', 'Hoeveel is 10 plus 10?'),
                """\
                if antwoord.data == 20:
                  print(f'''Goedzo!''')
                  print(f'''Het antwoord was inderdaad {antwoord}''')
                else:
                  print(f'''Foutje''')
                  print(f'''Het antwoord moest zijn {antwoord}''')""")

            self.single_level_tester(code=code, expected=expected)

        #
        # boolean values
        #

        def test_cond_boolean(self):
            code = textwrap.dedent("""\
                cond = False
                if cond is True:
                    sleep""")
            expected = textwrap.dedent("""\
                cond = Value(False, bool_sys={True: 'True', False: 'False'})
                if cond.data == True:
                  time.sleep(1)""")

            self.multi_level_tester(
                code=code,
                expected=expected
            )

        def test_if_elif_boolean(self):
            code = textwrap.dedent("""\
                computerc = 'PC'
                userc = 'Hedy'
                print 'Pilihan komputer: ' computerc
                if userc is computerc and userc is 'Hedy':
                    print 'SERI'
                elif userc is 'PC' and userc is 'Hedy':
                    print 'HARI'
                else:
                    print 'Komputer'""")

            expected = textwrap.dedent("""\
                computerc = Value('PC')
                userc = Value('Hedy')
                print(f'''Pilihan komputer: {computerc}''')
                if userc.data == computerc.data and userc.data == 'Hedy':
                  print(f'''SERI''')
                elif userc.data == 'PC' and userc.data == 'Hedy':
                  print(f'''HARI''')
                else:
                  print(f'''Komputer''')""")

            self.single_level_tester(code=code, expected=expected)

        def test_snippet(self):
            code = textwrap.dedent("""\
                prijzen = ['1 miljoen', 'een appeltaart', 'niks']
                jouw_prijs = prijzen [random]
                print 'Je wint ' jouw_prijs
                if jouw_prijs== '1 miljoen' :
                    print 'Yess! Je bent rijk!'
                elif jouw_prijs == 'een appeltaart' :
                    print 'Heerlijk, een appeltaart!'
                else:
                    print 'Meer geluk volgende keer..'""")
            expected = self.dedent(
                "prijzen = Value([Value('1 miljoen'), Value('een appeltaart'), Value('niks')])",
                self.list_access_transpiled("random.choice(prijzen.data)"),
                """\
                jouw_prijs = random.choice(prijzen.data)
                print(f'''Je wint {jouw_prijs}''')
                if jouw_prijs.data == '1 miljoen':
                  print(f'''Yess! Je bent rijk!''')
                elif jouw_prijs.data == 'een appeltaart':
                  print(f'''Heerlijk, een appeltaart!''')
                else:
                  print(f'''Meer geluk volgende keer..''')"""
            )

            self.single_level_tester(code=code, expected=expected)

        def test_if_else_boolean(self):
            code = textwrap.dedent("""\
                computerc = 'PC'
                userc = 'Hedy'
                print 'Pilihan komputer: ' computerc
                if userc is computerc and userc is 'Hedy':
                    print 'SERI'
                else:
                    print 'Komputer'""")

            expected = textwrap.dedent("""\
                computerc = Value('PC')
                userc = Value('Hedy')
                print(f'''Pilihan komputer: {computerc}''')
                if userc.data == computerc.data and userc.data == 'Hedy':
                  print(f'''SERI''')
                else:
                  print(f'''Komputer''')""")

            self.single_level_tester(code=code, expected=expected)

        def test_for_loop_arabic(self):
            code = textwrap.dedent("""\
                for دورة in range ١ to ٥:
                    print دورة""")

            expected = self.dedent(
                self.for_loop('دورة', 1, 5, "'Arabic'"),
                (f"print(f'''{{دورة}}''')", '  '),
                ("time.sleep(0.1)", '  '))

            self.single_level_tester(
                code=code,
                expected=expected,
                expected_commands=['for', 'print'])

        @parameterized.expand(['and', 'or'])
        def test_if_list_access_lhs_and_or(self, op):
            code = textwrap.dedent(f"""\
                colors = ['red', 'green', 'blue']
                if colors[1] == colors[2] {op} 1 == 1:
                    print 'red'""")

            expected = self.dedent(
                "colors = Value([Value('red'), Value('green'), Value('blue')])",
                self.list_access_transpiled('colors.data[int(1)-1]'),
                self.list_access_transpiled('colors.data[int(2)-1]'),
                f"""\
                if colors.data[int(1)-1].data == colors.data[int(2)-1].data {op} 1 == 1:
                  print(f'''red''')""")

            self.single_level_tester(
                code=code,
                expected=expected,
            )

        def test_for_loop(self):
            code = textwrap.dedent("""\
                a is 2
                b is 3
                for a in range 2 to 4:
                    a is a + 2
                    b is b + 2""")
            expected = self.dedent(
                "a = Value(2, num_sys='Latin')",
                "b = Value(3, num_sys='Latin')",
                self.for_loop('a', 2, 4),
                (f"a = Value({self.sum_transpiled('a', 2)}, num_sys=get_num_sys(a))", '  '),
                (f"b = Value({self.sum_transpiled('b', 2)}, num_sys=get_num_sys(b))", '  '),
                ("time.sleep(0.1)", '  '))

            self.single_level_tester(code=code, expected=expected)

        def test_for_loop_no_colon_after_pressed_gives_error(self):
            code = textwrap.dedent("""\
            for a in range 2 to 4
                a = 1""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('for in range', 1)
            )

        def test_for_list_without_colon_gives_error(self):
            code = textwrap.dedent("""\
            dieren = ['cat', 'dog', 'parrot']
            for dier in dieren
                a = 1""")

            self.multi_level_tester(
                code=code,
                exception=exceptions.MissingColonException,
                extra_check_function=missing_colon_check('for in', 2)
            )

        def test_if__else(self):
            code = textwrap.dedent("""\
                a is 5
                if a is 1:
                    a is 2
                else:
                    a is 222""")
            expected = textwrap.dedent("""\
                a = Value(5, num_sys='Latin')
                if a.data == 1:
                  a = Value(2, num_sys='Latin')
                else:
                  a = Value(222, num_sys='Latin')""")
            self.single_level_tester(code=code, expected=expected)

        def test_forloop(self):
            code = textwrap.dedent("""\
                for i in range 1 to 10:
                    print i
                print 'wie niet weg is is gezien'""")
            expected = self.dedent(
                self.for_loop('i', 1, 10),
                (f"print(f'''{{i}}''')", '  '),
                ("time.sleep(0.1)", '  '),
                "print(f'''wie niet weg is is gezien''')")

            self.single_level_tester(code=code, expected=expected)

        def test_allow_space_after_else_line(self):
            code = textwrap.dedent("""\
                a is 1
                if a is 1:
                    print a
                else:
                    print 'nee'""")

            expected = textwrap.dedent("""\
                a = Value(1, num_sys='Latin')
                if a.data == 1:
                  print(f'''{a}''')
                else:
                  print(f'''nee''')""")

            self.multi_level_tester(
                max_level=17,
                code=code,
                expected=expected,
                expected_commands=['is', 'if', 'print', 'print']
            )

        #
        # while loop
        #

        def test_while_undefined_var(self):
            code = textwrap.dedent("""\
            while antwoord != 25:
                print 'hoera'""")

            self.single_level_tester(
                code=code,
                exception=hedy.exceptions.UndefinedVarException
            )

        def test_while_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            a = 1
            while a != 5
                a = a + 1""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('while', 2)
            )

        def test_while_equals_boolean(self):
            code = textwrap.dedent("""\
                cond is True
                while cond != False:
                  cond is False""")
            expected = textwrap.dedent("""\
                cond = Value(True, bool_sys={True: 'True', False: 'False'})
                while cond.data!=False:
                  cond = Value(False, bool_sys={True: 'True', False: 'False'})
                  time.sleep(0.1)""")

            self.multi_level_tester(
                code=code,
                expected=expected,
                skip_faulty=False
            )

        def test_allow_space_before_colon(self):
            code = textwrap.dedent("""\
                a is 1
                if a is 1  :
                    print a
                else:
                    print 'nee'""")

            expected = textwrap.dedent("""\
                a = Value(1, num_sys='Latin')
                if a.data == 1:
                  print(f'''{a}''')
                else:
                  print(f'''nee''')""")

            self.multi_level_tester(
                code=code,
                max_level=17,
                expected=expected
            )

        def test_if_under_else_in_for(self):
            # todo can me multitester with higher levels!
            code = textwrap.dedent("""\
                for i in range 0 to 10:
                    antwoord is ask 'Wat is 5*5'
                    if antwoord is 24:
                        print 'Dat is fout!'
                    else:
                        print 'Dat is goed!'
                    if antwoord is 25:
                        i is 10""")

            expected = self.dedent(
                self.for_loop('i', 0, 10),
                (self.input_transpiled('antwoord', 'Wat is 5*5'), '  '),
                ("""\
                if antwoord.data == 24:
                  print(f'''Dat is fout!''')
                else:
                  print(f'''Dat is goed!''')
                if antwoord.data == 25:
                  i = Value(10, num_sys='Latin')
                time.sleep(0.1)""", '  '))

            self.single_level_tester(code=code, expected=expected)

        def test_if_elif(self):
            code = textwrap.dedent("""\
                a is 5
                if a is 1:
                    a is 2
                elif a is 2:
                    a is 222""")
            expected = textwrap.dedent("""\
                a = Value(5, num_sys='Latin')
                if a.data == 1:
                  a = Value(2, num_sys='Latin')
                elif a.data == 2:
                  a = Value(222, num_sys='Latin')""")

            self.single_level_tester(code=code, expected=expected)

        def test_if_elif_french(self):
            code = textwrap.dedent("""\
                a est 5
                si a est 1:
                    a est 2
                sinon si a est 2:
                    a est 222""")
            expected = textwrap.dedent("""\
                a = Value(5, num_sys='Latin')
                if a.data == 1:
                  a = Value(2, num_sys='Latin')
                elif a.data == 2:
                  a = Value(222, num_sys='Latin')""")

            self.single_level_tester(code=code, expected=expected, lang='fr')

        def test_if_with_multiple_elifs(self):
            code = textwrap.dedent("""\
                a is 5
                if a is 1:
                    a is 2
                elif a is 4:
                    a is 3
                elif a is 2:
                    a is 222""")
            expected = textwrap.dedent("""\
                a = Value(5, num_sys='Latin')
                if a.data == 1:
                  a = Value(2, num_sys='Latin')
                elif a.data == 4:
                  a = Value(3, num_sys='Latin')
                elif a.data == 2:
                  a = Value(222, num_sys='Latin')""")

            self.single_level_tester(
                code=code, expected=expected, expected_commands=[
                    'is', 'if', 'is', 'elif', 'is', 'elif', 'is'])

        def test_if_in_list_with_string_var_gives_type_error(self):
            code = textwrap.dedent("""\
            items is 'red'
            if 'red' in items:
                a is 1""")
            self.multi_level_tester(
                code=code,
                extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
                exception=hedy.exceptions.InvalidArgumentTypeException
            )

        #
        # in/not in tests
        #
        def test_if_ar_number_list_with_latin_numbers(self):
            code = textwrap.dedent("""\
               a = [11, 22, 33]
               if ١١ in a:
                 print 'correct'""")

            expected = textwrap.dedent(f"""\
               a = {self.list_transpiled("11", "22", "33")}
               if {self.in_list_transpiled("Value(11, num_sys='Arabic')", 'a')}:
                 print(f'''correct''')""")

            self.single_level_tester(code=code, expected=expected, output='correct')

        def test_if_ar_number_not_list_with_latin_numbers(self):
            code = textwrap.dedent("""\
               a is [22, 33, 44]
               if ١١ not in a:
                 print 'correct'""")

            expected = textwrap.dedent(f"""\
               a = {self.list_transpiled("22", "33", "44")}
               if {self.not_in_list_transpiled("Value(11, num_sys='Arabic')", 'a')}:
                 print(f'''correct''')""")

            self.single_level_tester(code=code, expected=expected, output='correct')

        def test_equality_with_lists(self):
            code = textwrap.dedent("""\
                m is [1, 2]
                n is [1, 2]
                if m is n:
                    print 'JA!'""")

            expected = textwrap.dedent("""\
                m = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])
                n = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])
                if m.data == n.data:
                  print(f'''JA!''')""")

            self.multi_level_tester(
                code=code,
                expected=expected,
                max_level=17
            )

        def test_equality_with_incompatible_types_gives_error(self):
            code = textwrap.dedent("""\
            a is 'test'
            b is 15
            if a is b:
              c is 1""")
            self.multi_level_tester(
                code=code,
                extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
                exception=hedy.exceptions.InvalidTypeCombinationException
            )

        @parameterized.expand(HedyTester.comparison_commands)
        def test_comparisons(self, comparison):
            code = textwrap.dedent(f"""\
                leeftijd is ask 'Hoe oud ben jij?'
                if leeftijd {comparison} 12:
                    print 'Dan ben je jonger dan ik!'""")
            expected = self.dedent(
                self.input_transpiled('leeftijd', 'Hoe oud ben jij?'),
                f"""\
                if leeftijd.data{comparison}12:
                  print(f'''Dan ben je jonger dan ik!''')""")

            self.single_level_tester(code=code, expected=expected)

        @parameterized.expand(HedyTester.number_comparison_commands)
        def test_smaller_with_string_gives_type_error(self, comparison):
            code = textwrap.dedent(f"""\
            a is 'text'
            if a {comparison} 12:
                b is 1""")

            self.multi_level_tester(
                code=code,
                extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
                exception=hedy.exceptions.InvalidArgumentTypeException
            )

        def test_not_equal_string_literal(self):
            code = textwrap.dedent(f"""\
            if 'quoted' != 'string':
              sleep""")
            expected = textwrap.dedent(f"""\
            if 'quoted'!='string':
              time.sleep(1)""")

            self.multi_level_tester(
                code=code,
                expected=expected
            )

        @parameterized.expand([
            ("'text'", "Value('text')"),
            ('1', "Value(1, num_sys='Latin')"),
            ('1.3', "Value(1.3, num_sys='Latin')"),
            ('[1, 2]', "Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin')])")])
        def test_not_equal(self, arg, exp):
            code = textwrap.dedent(f"""\
                a = {arg}
                b = {arg}
                if a != b:
                    b = 1""")

            expected = textwrap.dedent(f"""\
                a = {exp}
                b = {exp}
                if a.data!=b.data:
                  b = Value(1, num_sys='Latin')""")

            self.multi_level_tester(
                code=code,
                expected=expected
            )

        @parameterized.expand([
            ("'text'", '1'),  # text and number
            ('[1, 2]', '1'),  # list and number
            ('[1, 2]', "'text'")])  # list and text
        def test_not_equal_with_diff_types_gives_error(self, left, right):
            code = textwrap.dedent(f"""\
            a = {left}
            b = {right}
            if a != b:
                b = 1""")

            self.multi_level_tester(
                code=code,
                extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
                exception=exceptions.InvalidTypeCombinationException
            )

        def test_if_pressed_with_color(self):
            code = textwrap.dedent("""\
                if x is pressed:
                    color 'red'""")

            expected = self.dedent(
                f"""\
                global_scope_ = dict()
                if_pressed_mapping = {{"else": "if_pressed_default_else"}}
                if_pressed_mapping['x'] = 'if_pressed_x_'
                global if_pressed_x_
                def if_pressed_x_():""",
                (self.color_transpiled('red'), '  '),
                "extensions.if_pressed(if_pressed_mapping)")

            self.multi_level_tester(
                code=code,
                expected=expected,
                extra_check_function=self.is_turtle()
            )

        def test_if_pressed_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if x is pressed
                a = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('if', 1)
            )

        def test_pressed_elif_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if x is pressed:
                a = 'correct'
            elif m is pressed
                a = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('elif', 3)
            )

        def test_pressed_if_else_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if x is pressed:
                a = 'correct'
            else
                a = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('else', 3)
            )

        def test_pressed_if_elif_else_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if x is pressed:
                a = 'correct'
            elif m is pressed:
                a = 'correct'
            else
                a = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('else', 5)
            )

        def test_if_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if 'a' is 'a'
                b = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('if', 1)
            )

        def test_elif_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if 'a' is 'a':
                b = 'colon!'
            elif 'a' is 'b'
                b = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('elif', 3)
            )

        def test_else_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if 'a' is 'a':
                b = 'colon!'
            else
                b = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('else', 3)
            )

        def test_if_elif_else_no_colon_gives_error(self):
            code = textwrap.dedent("""\
            if 'a' is 'a':
                b = 'colon!'
            elif 'a' is 'b':
                b = 'colon!'
            else
                b = 'no colon!'""")

            self.multi_level_tester(
                code=code,
                exception=hedy.exceptions.MissingColonException,
                extra_check_function=missing_colon_check('else', 5)
            )

        def test_pressed_elif(self):
            code = textwrap.dedent("""\
            if a is pressed:
                print 'A'
            elif b is pressed:
                print 'B'
            else:
                print 'Other'""")

            expected = self.dedent("""\
            global_scope_ = dict()
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['a'] = 'if_pressed_a_'
            global if_pressed_a_
            def if_pressed_a_():
              print(f'''A''')
            if_pressed_mapping['b'] = 'if_pressed_b_'
            global if_pressed_b_
            def if_pressed_b_():
              print(f'''B''')
            if_pressed_mapping['else'] = 'if_pressed_else_'
            global if_pressed_else_
            def if_pressed_else_():
              print(f'''Other''')
            extensions.if_pressed(if_pressed_mapping)""")

            self.single_level_tester(code=code, expected=expected)

        def test_nested_functions(self):
            code = textwrap.dedent("""\
            define simple_function:
                define nested_function:
                    print 1
            call simple_function""")

            expected = textwrap.dedent("""\
            pass
            simple_function()""")

            skipped_mappings = [
                SkippedMapping(SourceRange(1, 1, 3, 34), hedy.exceptions.NestedFunctionException),
            ]

            self.single_level_tester(
                code=code,
                expected=expected,
                skipped_mappings=skipped_mappings,
            )

        def test_define_no_colon_gives_error(self):
            code = textwrap.dedent("""\
                define simple_function
                    a = 1
                call simple_function""")

            self.single_level_tester(
                code=code,
                exception=exceptions.MissingColonException,
                extra_check_function=missing_colon_check('define', 1)
            )

        def test_source_map(self):
            code = textwrap.dedent("""\
                for i in range 1 to 10:
                    print i
                print 'Ready or not, here I come!'""")

            excepted_code = self.dedent(
                self.for_loop('i', 1, 10),
                (f"print(f'''{{i}}''')", '  '),
                ("time.sleep(0.1)", '  '),
                "print(f'''Ready or not, here I come!''')")

            expected_source_map = {
                '1/5-1/6': '1/12-1/13',
                '2/11-2/12': '1/1-1/2',
                '2/5-2/12': '3/1-3/18',
                '1/1-2/21': '1/1-4/18',
                '3/1-3/35': '5/1-5/41',
                '1/1-3/36': '1/1-5/41'
            }

            self.single_level_tester(code, expected=excepted_code)
            self.source_map_tester(code=code, expected_source_map=expected_source_map)

    # -----old level 18-----

    @parameterized.expand([['(', ')'], ['（', '）']])
    def test_print_brackets(self, bracket_open, bracket_close):
        code = textwrap.dedent(f"""\
      print{bracket_open}'Hallo!'{bracket_close}""")

        expected = textwrap.dedent("""\
      print(f'''Hallo!''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            expected_commands=['print']
        )

    def test_print_var_brackets(self):
        code = textwrap.dedent("""\
        naam is 'Hedy'
        print('ik heet', naam)""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        print(f'''ik heet{naam}''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    def test_print_comma(self):
        code = "print('ik heet ,')"
        expected = "print(f'''ik heet ,''')"
        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle())

    @parameterized.expand(['=', 'is'])
    def test_input(self, assigment):
        code = textwrap.dedent(f"""\
            leeftijd {assigment} input('Hoe oud ben jij?')
            print(leeftijd)""")
        expected = self.dedent(
            self.input_transpiled('leeftijd', 'Hoe oud ben jij?'),
            "print(f'''{leeftijd}''')")

        self.multi_level_tester(
            max_level=20,
            code=code,
            expected=expected,
            translate=False,
            extra_check_function=self.is_not_turtle()
        )

    @parameterized.expand([':', '：'])
    def test_if_with_dequals_sign_colon(self, colon):
        code = textwrap.dedent(f"""\
            naam is 'Hedy'
            if naam == 'Hedy'{colon}
                print('koekoek')""")

        expected = textwrap.dedent("""\
            naam = Value('Hedy')
            if naam.data == 'Hedy':
              print(f'''koekoek''')""")

        self.single_level_tester(code=code, expected=expected)

    # issue also in level 17, leaving for now.
    # def test_bigger(self):
    #     code = textwrap.dedent("""\
    #     leeftijd is input('Hoe oud ben jij?')
    #     if leeftijd > 12:
    #         print('Dan ben je ouder dan ik!')""")
    #     expected = textwrap.dedent("""\
    #     leeftijd = input('Hoe oud ben jij?')
    #     if int(leeftijd) > int('12'):
    #       print(f'Dan ben je ouder dan ik!')""")
    #
    #     self.multi_level_tester(
    #       code=code,
    #       expected=expected,
    #       extra_check_function=self.is_not_turtle(),
    #       test_name=self.name()
    #     )
    # def test_big_and_small(self):
    #     code = textwrap.dedent("""\
    #     leeftijd is input('Hoe oud ben jij?')
    #     if leeftijd < 12:
    #         print('Dan ben je jonger dan ik!')
    #     elif leeftijd > 12:
    #         print('Dan ben je ouder dan ik!')""")
    #     expected = textwrap.dedent("""\
    #     leeftijd = input('Hoe oud ben jij?')
    #     if int(leeftijd) < int('12'):
    #       print(f'Dan ben je jonger dan ik!')
    #     elif int(leeftijd) > int('12'):
    #       print(f'Dan ben je ouder dan ik!')""")
    #
    #     self.multi_level_tester(
    #       max_level=20,
    #       code=code,
    #       expected=expected,
    #       extra_check_function=self.is_not_turtle(),
    #       test_name=self.name()
    #     )

    def test_if_else(self):
        code = textwrap.dedent("""\
            antwoord is input('Hoeveel is 10 plus 10?')
            if antwoord is 20:
                print('Goedzo!')
                print('Het antwoord was inderdaad', antwoord)
            else:
                print('Foutje')
                print('Het antwoord moest zijn', antwoord)""")

        expected = self.dedent(
            self.input_transpiled('antwoord', "Hoeveel is 10 plus 10?"),
            """\
            if antwoord.data == 20:
              print(f'''Goedzo!''')
              print(f'''Het antwoord was inderdaad{antwoord}''')
            else:
              print(f'''Foutje''')
              print(f'''Het antwoord moest zijn{antwoord}''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            translate=False,
            expected_commands=['input', 'if', 'print', 'print', 'print', 'print'],
            extra_check_function=self.is_not_turtle()
        )

    def test_for_loop(self):
        code = textwrap.dedent("""\
            a is 2
            b is 3
            for a in range(2, 4):
                a is a + 2
                b is b + 2""")
        expected = self.dedent(
            "a = Value(2, num_sys='Latin')",
            "b = Value(3, num_sys='Latin')",
            self.for_loop('a', 2, 4),
            (f"a = Value({self.sum_transpiled('a', 2)}, num_sys=get_num_sys(a))", '  '),
            (f"b = Value({self.sum_transpiled('b', 2)}, num_sys=get_num_sys(b))", '  '),
            ("time.sleep(0.1)", '  '))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    def test_for_nesting(self):
        code = textwrap.dedent("""\
            for i in range(1, 3):
                for j in range(1, 4):
                    print('rondje: ', i, ' tel: ', j)""")
        expected = self.dedent(
            self.for_loop('i', 1, 3),
            (self.for_loop('j', 1, 4), '  '),
            ("print(f'''rondje: {i} tel: {j}''')", '    '),
            ("time.sleep(0.1)", '    '))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    def test_for_loop_arabic(self):
        code = textwrap.dedent("""\
            for دورة in range(١, ٥):
                print(دورة)""")

        expected = self.dedent(
            self.for_loop('دورة', 1, 5, "'Arabic'"),
            (f"print(f'''{{دورة}}''')", '  '),
            ("time.sleep(0.1)", '  '))

        self.single_level_tester(
            code=code,
            expected=expected,
            expected_commands=['for', 'print'])

    def test_input_with_list(self):
        code = textwrap.dedent("""\
            color is ['green', 'blue']
            choice is input('Is your favorite color one of: ', color)""")

        expected = self.dedent(
            "color = Value([Value('green'), Value('blue')])",
            self.input_transpiled('choice', 'Is your favorite color one of: {color}'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            extra_check_function=self.is_not_turtle()
        )

    def test_input_without_text_inside(self):
        code = "x = input()"
        expected = self.input_transpiled('x', '')
        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            extra_check_function=self.is_not_turtle()
        )

    # TODO: is failing now but not sure we would want an empty print
    # def test_print_without_text_inside(self):
    #    self.multi_level_tester(
    #        code="print()",
    #        expected="print(f'''''')",
    #        extra_check_function=self.is_not_turtle()
    #    )

    # negative tests

    def test_while_undefined_var(self):
        code = textwrap.dedent("""\
        while antwoord != 25:
            print('hoera')""")

        self.single_level_tester(
            code=code,
            exception=hedy.exceptions.UndefinedVarException
        )

    def test_var_undefined_error_message(self):
        code = textwrap.dedent("""\
        naam is 'Hedy'
        print('ik heet ', name)""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.UndefinedVarException
        )

        # deze extra check functie kan nu niet mee omdat die altijd op result werkt
        # evt toch splitsen in 2 (pos en neg?)
        # self.assertEqual('name', context.exception.arguments['name'])

    #
    # Test comment
    #
    def test_print_comment(self):
        code = "print('Hallo welkom bij Hedy!') # This is a comment"
        expected = "print(f'''Hallo welkom bij Hedy!''')"
        output = 'Hallo welkom bij Hedy!'

        self.multi_level_tester(
            code=code,
            expected=expected,
            output=output
        )

    def test_nested_functions(self):
        code = textwrap.dedent("""\
        def simple_function():
            def nested_function():
                print(1)
        simple_function()""")

        expected = textwrap.dedent("""\
        pass
        simple_function()""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 3, 35), hedy.exceptions.NestedFunctionException),
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
        )

    @parameterized.expand(['and', 'or'])
    def test_if_list_access_lhs_and_or(self, op):
        code = textwrap.dedent(f"""\
            colors = ['red', 'green', 'blue']
            if colors[1] == colors[2] {op} 1 == 1:
                print('red')""")

        expected = self.dedent(
            "colors = Value([Value('red'), Value('green'), Value('blue')])",
            self.list_access_transpiled('colors.data[int(1)-1]'),
            self.list_access_transpiled('colors.data[int(2)-1]'),
            f"""\
                if colors.data[int(1)-1].data == colors.data[int(2)-1].data {op} 1 == 1:
                  print(f'''red''')""")

        self.single_level_tester(
            code=code,
            expected=expected,
        )

    #
    # repeat
    #
    def test_repeat_nested_multi_commands(self):
        code = textwrap.dedent("""\
            repeat 3 times
                print(3)
                repeat 5 times
                    print(5)
                print(1)""")

        expected = textwrap.dedent(f"""\
            for __i in range({self.int_transpiled(3)}):
              print(f'''3''')
              for __i in range({self.int_transpiled(5)}):
                print(f'''5''')
                time.sleep(0.1)
              print(f'''1''')
              time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            skip_faulty=False
        )

    def missing_colon_check(command, line_number):
        return lambda c: (c.exception.arguments['line_number'] == line_number and
                          c.exception.arguments['command'] == command)
