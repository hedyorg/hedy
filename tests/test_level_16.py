import hedy
import textwrap
from test_level_01 import HedyTester


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
            expected=expected,
            extra_check_function=check_in_list,
            test_name=self.name()
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
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            test_name=self.name()
        )

    def test_list_access_var(self):
        code = textwrap.dedent("""\
            fruit is ['banaan', 'appel', 'kers']
            eerstefruit is fruit[1]
            print eerstefruit""")
        expected = textwrap.dedent("""\
            fruit = ['banaan', 'appel', 'kers']
            eerstefruit = fruit[1-1]
            print(f'{eerstefruit}')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            test_name=self.name()
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
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            test_name=self.name()
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
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            test_name=self.name()
        )

    # ask tests
    def test_ask_with_list_var(self):
        code = textwrap.dedent("""\
        colors is ['orange', 'blue', 'green']
        favorite is ask 'Is your fav color' colors[1]""")

        expected = textwrap.dedent("""\
        colors = ['orange', 'blue', 'green']
        favorite = input('Is your fav color'+colors[1-1])
        try:
          favorite = int(favorite)
        except ValueError:
          try:
            favorite = float(favorite)
          except ValueError:
            pass""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            test_name=self.name()
        )

    def test_ask_with_list_gives_type_error(self):
        code = textwrap.dedent("""\
        colors is ['orange', 'blue', 'green']
        favorite is ask 'Is your fav color' colors""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            test_name=self.name()
        )

    #add/remove tests
    def test_add_to_list(self):
        code = textwrap.dedent("""\
        color is ask 'what is your favorite color? '
        colors is ['green', 'red', 'blue']
        add color to colors
        print colors[random]""")

        expected = textwrap.dedent("""\
        color = input('what is your favorite color? ')
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
          expected=expected,
          test_name=self.name()
        )

    def test_remove_from_list(self):
        code = textwrap.dedent("""\
        colors is ['green', 'red', 'blue']
        color is ask 'what color to remove?'
        remove color from colors
        print colors[random]""")

        expected = textwrap.dedent("""\
        colors = ['green', 'red', 'blue']
        color = input('what color to remove?')
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
          expected=expected,
          test_name=self.name()
        )