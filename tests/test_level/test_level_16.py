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

        expected = HedyTester.dedent(
            "dieren = ['Hond', 'Kat', 'Kangoeroe']",
            HedyTester.list_access_transpiled('dieren[int(1)-1]'),
            "print(f'''{dieren[int(1)-1]}''')")

        check_in_list = (lambda x: HedyTester.run_code(x) == 'Hond')

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=check_in_list
        )

    def test_create_empty_list(self):
        code = "friends = []"
        expected = "friends = []"

        self.multi_level_tester(
            code=code,
            unused_allowed=True,
            expected=expected
        )

    @parameterized.expand([
        ("'Ashli'", 'Ashli'),
        ("'\"Ashli\"'", '"Ashli"'),
        ('"Ashli"', 'Ashli'),
        ('"Ashli\'s"', 'Ashli\'s'),
        ('42', 42),
        ('-1', -1),
        ('1.5', 1.5),
        ('-0.7', -0.7)
    ])
    def test_create_list_single_item(self, item_code, expected_value):
        code = f"friends = [{item_code}]"
        expected = f"friends = [{item_code}]"

        check_in_list = (lambda x: HedyTester.run_code(x) == expected_value)

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            extra_check_function=check_in_list
        )

    @parameterized.expand([
        ("'Alice', 'Ben'", ['Alice', 'Ben']),
        ("'\"a\"', '\"Ben\"'", ['"Alice"', '"Ben"']),
        ('"Alice", "Ben"', ['Alice', 'Ben']),
        ('"Alice\'s", "Ben\'s"', ["Alice's", "Ben's"]),
        ('1, 3, 5', [1, 3, 5]),
        ('-1, -2, -5', [-1, -2, -5]),
        ('1.5, 2.6, 3.7', [1.5, 2.6, 3.7]),
        ('-0.1, -5.6', [-0.1, -5.6])
    ])
    def test_create_list_multi_items(self, items_code, expected_items):
        code = f"friends = [{items_code}]"
        expected = f"friends = [{items_code}]"

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

        expected = HedyTester.dedent("""\
                friends = []
                friends.append('Ashli')""",
                                     HedyTester.list_access_transpiled('friends[int(1)-1]'),
                                     "print(f'''{friends[int(1)-1]}''')")

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

        expected = HedyTester.dedent(
            "dieren = ['Hond', 'Kat', 'Kangoeroe']",
            HedyTester.list_access_transpiled('dieren[int(1)-1]'),
            "print(f'''{dieren[int(1)-1]}''')")

        check_in_list = (lambda x: HedyTester.run_code(x) == 'Hond')

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=check_in_list
        )

    def test_print_list_commas(self):
        code = textwrap.dedent("""\
            szamok1 = ['1' , '2' , '3' , '4' , '5']
            print szamok1[random]""")

        expected = textwrap.dedent("""\
            szamok1 = ['1', '2', '3', '4', '5']
            print(f'''{random.choice(szamok1)}''')""")

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
            szamok1 = ['1', '2', '3', '4', '5']
            print(f'''{random.choice(szamok1)}''')""")
        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    def test_print_list_access(self):
        code = textwrap.dedent("""\
            fruit is ['banaan', 'appel', 'kers']
            print fruit[1]""")
        expected = HedyTester.dedent(
            "fruit = ['banaan', 'appel', 'kers']",
            HedyTester.list_access_transpiled('fruit[int(1)-1]'),
            "print(f'''{fruit[int(1)-1]}''')")

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
        expected = HedyTester.dedent("""\
        vrienden = ['Ahmed', 'Ben', 'Cayden']
        geluksgetallen = [15, 18, 6]
        step = 1 if 1 < 3 else -1
        for म in range(1, 3 + step, step):""",
                                     (HedyTester.list_access_transpiled('vrienden[int(म)-1]'), '  '),
                                     ("print(f'''het geluksgetal van {vrienden[int(म)-1]}''')", '  '),
                                     (HedyTester.list_access_transpiled('geluksgetallen[int(म)-1]'), '  '),
                                     ("print(f'''is {geluksgetallen[int(म)-1]}''')", '  '),
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
        expected = HedyTester.dedent(
            "fruit = ['banaan', 'appel', 'kers']",
            HedyTester.list_access_transpiled('fruit[int(1)-1]'),
            "eerstefruit = fruit[int(1)-1]",
            "print(f'''{eerstefruit}''')")

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
        expected = HedyTester.dedent(
            "lijst = [1, 2, 3]",
            HedyTester.list_access_transpiled('lijst[int(1)-1]'),
            HedyTester.list_access_transpiled('lijst[int(2)-1]'),
            f"optellen = {self.addition_transpiled('lijst[int(1)-1]', 'lijst[int(2)-1]')}",
            HedyTester.list_access_transpiled('lijst[int(3)-1]'),
            f"""\
            optellen = {self.addition_transpiled('optellen', 'lijst[int(3)-1]')}
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
        expected = HedyTester.dedent(
            "fruit = ['banaan', 'appel', 'kers']",
            HedyTester.list_access_transpiled('random.choice(fruit)'),
            "randomfruit = random.choice(fruit)",
            "print(f'''{randomfruit}''')")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    def test_access_in_equality_check(self):
        code = textwrap.dedent("""\
            luiaard = 'luiaard'
            dieren is ['aap', 'goat', 'fish']
            if luiaard is dieren[1]
                print 'ja'""")

        expected = HedyTester.dedent("""\
            luiaard = 'luiaard'
            dieren = ['aap', 'goat', 'fish']""",
                                     HedyTester.list_access_transpiled('dieren[int(1)-1]'),
                                     """\
            if convert_numerals('Latin', luiaard) == convert_numerals('Latin', dieren[int(1)-1]):
              print(f'''ja''')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    @parameterized.expand(HedyTester.comparison_commands)
    def test_access_smaller_check(self, comparison):
        code = textwrap.dedent(f"""\
            balletje = 0
            bingo_getallen is [11, 17, 21]
            if balletje {comparison} bingo_getallen[1]
                print 'ja'""")

        expected = HedyTester.dedent(f"""\
            balletje = 0
            bingo_getallen = [11, 17, 21]""",
                                     HedyTester.list_access_transpiled('bingo_getallen[int(1)-1]'),
                                     f"""\
            if convert_numerals('Latin', balletje){comparison}convert_numerals('Latin', bingo_getallen[int(1)-1]):
              print(f'''ja''')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    # ask tests
    def test_ask_with_list_var(self):
        code = textwrap.dedent("""\
            colors is ['orange', 'blue', 'green']
            favorite is ask 'Is your fav color' colors[1]""")

        expected = self.dedent(
            "colors = ['orange', 'blue', 'green']",
            self.list_access_transpiled('colors[int(1)-1]'),
            """\
            favorite = input(f'''Is your fav color{colors[int(1)-1]}''')
            try:
              favorite = int(favorite)
            except ValueError:
              try:
                favorite = float(favorite)
              except ValueError:
                pass"""
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

        expected = textwrap.dedent("""\
        colors = ['orange', 'blue', 'green']
        favorite = input(f'''Is your fav color{colors}''')
        try:
          favorite = int(favorite)
        except ValueError:
          try:
            favorite = float(favorite)
          except ValueError:
            pass""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            unused_allowed=True,
            expected=expected
        )

    # add/remove tests

    def test_add_to_list(self):
        code = textwrap.dedent("""\
        color is ask 'what is your favorite color? '
        colors is ['green', 'red', 'blue']
        add color to colors
        print colors[random]""")

        expected = HedyTester.dedent("""\
        color = input(f'''what is your favorite color? ''')
        try:
          color = int(color)
        except ValueError:
          try:
            color = float(color)
          except ValueError:
            pass
        colors = ['green', 'red', 'blue']
        colors.append(color)""",
                                     HedyTester.list_access_transpiled('random.choice(colors)'),
                                     "print(f'''{random.choice(colors)}''')")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    def test_add_list_access_to_list(self):
        code = textwrap.dedent("""\
        colors1 is ['green', 'red', 'blue']
        colors2 is ['yellow', 'purple']
        add colors1[2] to colors2
        print colors2[3]""")

        expected = HedyTester.dedent("""\
        colors1 = ['green', 'red', 'blue']
        colors2 = ['yellow', 'purple']
        colors2.append(colors1[2-1])""",
                                     HedyTester.list_access_transpiled("colors2[int(3)-1]"),
                                     "print(f'''{colors2[int(3)-1]}''')")

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

        expected = HedyTester.dedent("""\
        colors = ['green', 'red', 'blue']
        color = input(f'''what color to remove?''')
        try:
          color = int(color)
        except ValueError:
          try:
            color = float(color)
          except ValueError:
            pass
        try:
          colors.remove(color)
        except:
          pass""",
                                     HedyTester.list_access_transpiled('random.choice(colors)'),
                                     "print(f'''{random.choice(colors)}''')")

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

        expected = HedyTester.dedent("""\
        colors1 = ['green', 'red', 'blue']
        colors2 = ['red', 'purple']
        try:
          colors2.remove(colors1[2-1])
        except:
          pass""",
                                     HedyTester.list_access_transpiled('colors2[int(1)-1]'),
                                     "print(f'''{colors2[int(1)-1]}''')")

        check_removed_from_list = (lambda x: HedyTester.run_code(x) == 'purple')  # check that 'red' was removed

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=check_removed_from_list
        )

    def test_equality_with_lists(self):
        code = textwrap.dedent("""\
        m is [1, 2]
        n is [1, 2]
        if m is n
            print 'success!'""")

        expected = textwrap.dedent("""\
        m = [1, 2]
        n = [1, 2]
        if convert_numerals('Latin', m) == convert_numerals('Latin', n):
          print(f'''success!''')""")

        self.single_level_tester(code=code, expected=expected)

    def test_change_list_item_var(self):
        # Must be updated with 1 -> int(1), see note in 4047
        code = textwrap.dedent("""\
        l = [1, 2]
        x = 3
        l[1] = x""")

        expected = HedyTester.dedent("""\
        l = [1, 2]
        x = 3""",
                                     HedyTester.list_access_transpiled('l[1-1]'),
                                     "l[1-1] = x")

        self.single_level_tester(code=code, expected=expected)

    def test_change_list_item_number(self):
        code = textwrap.dedent("""\
        l = [1, 2]
        m = 2
        l[m] = 3""")

        expected = HedyTester.dedent("""\
        l = [1, 2]
        m = 2""",
                                     HedyTester.list_access_transpiled('l[m-1]'),
                                     "l[m-1] = 3")

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

    @parameterized.expand(["'text'", '1', '1.3', '[1, 2]'])
    def test_not_equal(self, arg):
        code = textwrap.dedent(f"""\
            a = {arg}
            b = {arg}
            if a != b
                b = 1""")

        expected = textwrap.dedent(f"""\
            a = {arg}
            b = {arg}
            if convert_numerals('Latin', a)!=convert_numerals('Latin', b):
              b = 1""")

        self.single_level_tester(code, expected=expected)

    @parameterized.expand([
        ('"text"', '1'),        # double-quoted text and number
        ("'text'", '1'),        # single-quoted text and number
        ('[1, 2]', '1'),        # list and number
        ('[1, 2]', "'text'")])  # list and text
    def test_not_equal_with_diff_types_gives_error(self, left, right):
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

        expected = HedyTester.dedent(
            "c = ['red', 'green', 'blue']",
            HedyTester.turtle_color_command_transpiled('{c}')
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

        expected = HedyTester.dedent(
            "colors = ['red', 'green', 'blue']",
            HedyTester.turtle_color_command_transpiled('{random.choice(colors)}')
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

        expected = HedyTester.dedent(
            "colors = ['red', 'green', 'blue']",
            self.list_access_transpiled('colors[int(1)-1]'),
            self.list_access_transpiled('colors[int(2)-1]'),
            f"""\
            if convert_numerals('Latin', colors[int(1)-1]) == convert_numerals('Latin', colors[int(2)-1]) {op} convert_numerals('Latin', '1') == convert_numerals('Latin', '1'):
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
            letters = ['a', 'b', 'c']
            if 'a' {command} letters:
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
        items = [1, 2, 3]
        if 1 {operator} items:
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
            items = [1, 2, 3]
            if '1' {operator} items:
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

        expected = HedyTester.dedent("""\
        directions = [10, 100, 360]""",
                                     HedyTester.list_access_transpiled('random.choice(directions)'),
                                     HedyTester.forward_transpiled('random.choice(directions)', self.level))

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

        expected = HedyTester.dedent("""\
        directions = [10, 100, 360]""",
                                     HedyTester.list_access_transpiled('random.choice(directions)'),
                                     HedyTester.turn_transpiled('random.choice(directions)', self.level))

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

        expected = HedyTester.dedent("""\
        lijstje = ['kip', 'haan', 'kuiken']
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        def if_pressed_x_():
            for dier in lijstje:
              print(f'''dier''')
              time.sleep(0.1)
        extensions.if_pressed(if_pressed_mapping)""")

        self.single_level_tester(code=code, expected=expected)

    @parameterized.expand(['number is', 'print', 'forward', 'turn'])
    def test_at_random_express(self, command):
        code = textwrap.dedent(f"""\
            numbers is [1, 2, 3]
            {command} numbers at random""")
        self.single_level_tester(code=code, exception=hedy.exceptions.InvalidAtCommandException)

    def test_at_random_express_sleep(self):
        code = textwrap.dedent(f"""\
            prind skipping
            numbers is [1, 2, 3]
            sleep numbers at random""")

        expected = HedyTester.dedent(f"""\
        pass
        numbers = [1, 2, 3]
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

        expected = HedyTester.dedent(
            "notes = ['C4', 'E4', 'D4', 'F4', 'G4']",
            self.play_transpiled('random.choice(notes)', quotes=False)
        )

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=17
        )
