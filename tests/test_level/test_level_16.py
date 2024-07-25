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
            voor म in bereik 1 tot 3
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

    def test_if_pressed_with_list_and_for(self):
        code = textwrap.dedent("""\
        lijstje is ['kip', 'haan', 'kuiken']
        if x is pressed
            for dier in lijstje
                print 'dier'""")

        expected = self.dedent("""\
        lijstje = Value([Value('kip'), Value('haan'), Value('kuiken')])
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        def if_pressed_x_():
            for dier in lijstje.data:
              print(f'''dier''')
              time.sleep(0.1)
        extensions.if_pressed(if_pressed_mapping)""")

        self.single_level_tester(code=code, expected=expected)

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
        expected = ("cond = Value([Value(True, bools={True: 'True', False: 'False'}), "
                    "Value(False, bools={True: 'True', False: 'False'}), "
                    "Value(True, bools={True: 'true', False: 'false'}), "
                    "Value(False, bools={True: 'true', False: 'false'})])")

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
            cond = Value({exp}, bools={{True: '{exp_true}', False: '{exp_false}'}})
            if cond.data == {exp}:
              time.sleep(1)""")

        self.single_level_tester(
            code=code,
            expected=expected,
            translate=False
        )
