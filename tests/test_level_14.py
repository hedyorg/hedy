import textwrap
from test_level_01 import HedyTester


class TestsLevel14(HedyTester):
    level = 14

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
