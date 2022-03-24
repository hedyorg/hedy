import exceptions
import hedy
import textwrap
from Tester import HedyTester
from parameterized import parameterized


class TestsLevel16(HedyTester):
    level = 16

    def test_print_list_var(self):
        code = textwrap.dedent("""\
            dieren is ['Hond', 'Kat', 'Kangoeroe']
            print dieren[1]""")

        expected = textwrap.dedent("""\
            dieren = ['Hond', 'Kat', 'Kangoeroe']
            print(f'{dieren[1-1]}')""")

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
            szamok2 = ['6' , '7' , '8' , '9']
            print szamok1[random]""")

        expected = textwrap.dedent("""\
            szamok1 = ['1', '2', '3', '4', '5']
            szamok2 = ['6', '7', '8', '9']
            print(f'{random.choice(szamok1)}')""")

        szamok1 = ['1', '2', '3', '4', '5']
        check_in_list = (lambda x: HedyTester.run_code(x) in szamok1)

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=check_in_list
        )

    def test_print_list_access(self):
        code = textwrap.dedent("""\
            fruit is ['banaan', 'appel', 'kers']
            print fruit[1]""")
        expected = textwrap.dedent("""\
            fruit = ['banaan', 'appel', 'kers']
            print(f'{fruit[1-1]}')""")

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
        expected = textwrap.dedent("""\
        vrienden = ['Ahmed', 'Ben', 'Cayden']
        geluksgetallen = [15, 18, 6]
        step = 1 if int(1) < int(3) else -1
        for v7dd7ec2093c0f55999a450adc7e4fe49 in range(int(1), int(3) + step, step):
          print(f'het geluksgetal van {vrienden[v7dd7ec2093c0f55999a450adc7e4fe49-1]}')
          print(f'is {geluksgetallen[v7dd7ec2093c0f55999a450adc7e4fe49-1]}')
          time.sleep(0.1)""")

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
        expected = textwrap.dedent("""\
            fruit = ['banaan', 'appel', 'kers']
            eerstefruit = fruit[1-1]
            print(f'{eerstefruit}')""")

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
        expected = textwrap.dedent("""\
            lijst = [1, 2, 3]
            optellen = lijst[1-1] + lijst[2-1]
            optellen = optellen + lijst[3-1]
            print(f'{optellen}')""")

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
        expected = textwrap.dedent("""\
            fruit = ['banaan', 'appel', 'kers']
            randomfruit = random.choice(fruit)
            print(f'{randomfruit}')""")

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

        expected = textwrap.dedent("""\
            luiaard = 'luiaard'
            dieren = ['aap', 'goat', 'fish']
            if str(luiaard) == str(dieren[1-1]):
              print(f'ja')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    @parameterized.expand(HedyTester.comparison_commands)
    def test_access_smaller_check(self,comparison):
        code = textwrap.dedent(f"""\
            balletje = 0
            bingo_getallen is [11, 17, 21]
            if balletje {comparison} bingo_getallen[1]
                print 'ja'""")

        expected = textwrap.dedent(f"""\
            balletje = 0
            bingo_getallen = [11, 17, 21]
            if str(balletje).zfill(100){comparison}str(bingo_getallen[1-1]).zfill(100):
              print(f'ja')""")

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

        expected = textwrap.dedent("""\
        colors = ['orange', 'blue', 'green']
        favorite = input(f'Is your fav color{colors[1-1]}')
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
            expected=expected,
            extra_check_function=self.is_not_turtle()
        )

    def test_ask_with_list(self):
        code = textwrap.dedent("""\
        colors is ['orange', 'blue', 'green']
        favorite is ask 'Is your fav color' colors""")

        expected = textwrap.dedent("""\
        colors = ['orange', 'blue', 'green']
        favorite = input(f'Is your fav color{colors}')
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
            expected=expected
        )

    #add/remove tests
    def test_add_to_list(self):
        code = textwrap.dedent("""\
        color is ask 'what is your favorite color? '
        colors is ['green', 'red', 'blue']
        add color to colors
        print colors[random]""")

        expected = textwrap.dedent("""\
        color = input(f'what is your favorite color? ')
        try:
          color = int(color)
        except ValueError:
          try:
            color = float(color)
          except ValueError:
            pass
        colors = ['green', 'red', 'blue']
        colors.append(color)
        print(f'{random.choice(colors)}')""")

        self.multi_level_tester(
          code=code,
          max_level=17,
          expected=expected
        )

    def test_remove_from_list(self):
        code = textwrap.dedent("""\
        colors is ['green', 'red', 'blue']
        color is ask 'what color to remove?'
        remove color from colors
        print colors[random]""")

        expected = textwrap.dedent("""\
        colors = ['green', 'red', 'blue']
        color = input(f'what color to remove?')
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
           pass
        print(f'{random.choice(colors)}')""")

        self.multi_level_tester(
          code=code,
          max_level=17,
          expected=expected
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
        if str(m) == str(n):
          print(f'success!')""")

        self.single_level_tester(code=code, expected=expected)

    def test_equality_with_number_and_list_gives_error(self):
        code = textwrap.dedent("""\
        color is [5, 6, 7]
        if 1 is color
            print 'success!'""")

        with self.assertRaises(hedy.exceptions.InvalidTypeCombinationException):
            hedy.transpile(code, self.level)

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
            if str(a).zfill(100)!=str(b).zfill(100):
              b = 1""")

        self.single_level_tester(code, expected=expected)

    @parameterized.expand([
        ("'text'", '1'),        # text and number
        ('[1, 2]', '1'),        # list and number
        ('[1, 2]', "'text'")])  # list and text
    def test_not_equal_with_diff_types_gives_error(self, left, right):
        code = textwrap.dedent(f"""\
            a = {left}
            b = {right}
            if a != b
                b = 1""")

        self.single_level_tester(code, exception=exceptions.InvalidTypeCombinationException)
