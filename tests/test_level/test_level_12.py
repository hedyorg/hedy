import textwrap

from parameterized import parameterized

import exceptions
import hedy
from hedy import Command
from hedy_sourcemap import SourceRange
from tests.Tester import HedyTester, SkippedMapping


class TestsLevel12(HedyTester):
    level = 12
    '''
    Tests should be ordered as follows:
     * commands in the order of hedy.py e.g. for level 1: ['print', 'ask', 'echo', 'turn', 'forward']
     * combined tests
     * markup tests
     * negative tests

    Naming conventions are like this:
     * single keyword positive tests are just keyword or keyword_special_case
     * multi keyword positive tests are keyword1_keywords_2
     * negative tests should be situation_gives_exception
    '''

    #
    # print tests
    #
    def test_print_var_number(self):
        code = textwrap.dedent("""\
            n is 10
            print n""")
        expected = textwrap.dedent("""\
            n = Value(10, num_sys='Latin')
            print(f'''{n}''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='10',
            max_level=17)

    def test_print_var_number_arabic(self):
        code = textwrap.dedent("""\
            n is ١١
            print n""")
        expected = textwrap.dedent("""\
            n = Value(11, num_sys='Arabic')
            print(f'''{n}''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='١١',
            max_level=17)

    def test_print_keyword_var(self):
        code = textwrap.dedent("""\
            sum is 10
            print sum""")
        expected = textwrap.dedent("""\
            _sum = Value(10, num_sys='Latin')
            print(f'''{_sum}''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='10',
            max_level=17)

    def test_print_multi_args(self):
        code = "print 'hello' 'Hedy' 4 ١١"
        expected = """print(f'''helloHedy4{localize(11, num_sys='Arabic')}''')"""

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='helloHedy4١١',
            max_level=17)

    def test_print_calc_with_var(self):
        code = textwrap.dedent("""\
            var is 5
            print var + 5""")
        expected = textwrap.dedent(f"""\
            var = Value(5, num_sys='Latin')
            print(f'''{{localize({self.sum_transpiled('var', 5)}, num_sys=get_num_sys(var))}}''')""")

        self.multi_level_tester(max_level=17, code=code, output='10', expected=expected)

    def test_print_calc_with_arabic_var(self):
        code = textwrap.dedent("""\
            var is ٨
            print var + ١""")
        expected = textwrap.dedent(f"""\
            var = Value(8, num_sys='Arabic')
            print(f'''{{localize({self.sum_transpiled('var', 1)}, num_sys=get_num_sys(var))}}''')""")

        self.multi_level_tester(max_level=17, code=code, output='٩', expected=expected)

    @parameterized.expand([
        ('*', '16'),
        ('/', '4.0'),
        ('+', '10'),
        ('-', '6')
    ])
    def test_print_calc_directly(self, op, output):
        code = f"print 8 {op} 2"
        expected = f"""print(f'''{{localize(8 {op} 2, num_sys='Latin')}}''')"""

        self.multi_level_tester(max_level=17, code=code, expected=expected, output=output)

    @parameterized.expand([
        ('*', '٢٥'),
        ('/', '١.٠'),
        ('+', '١٠'),
        ('-', '٠')])
    def test_print_calc_arabic_directly(self, op, out):
        code = f"""قول "٥ ضرب ٥ يساوي " ٥{op}٥"""
        expected = f"""print(f'''٥ ضرب ٥ يساوي {{localize(5 {op} 5, num_sys='Arabic')}}''')"""
        output = f'٥ ضرب ٥ يساوي {out}'

        self.multi_level_tester(
            max_level=17,
            code=code,
            expected=expected,
            output=output,
            lang='ar')

    def test_print_float_variable(self):
        code = textwrap.dedent("""\
            pi is 3.14
            print pi""")
        expected = textwrap.dedent("""\
            pi = Value(3.14, num_sys='Latin')
            print(f'''{pi}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    def test_print_float(self):
        code = "print 3.14"

        expected = "print(f'''3.14''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            output='3.14'
        )

    def test_print_division_float(self):
        code = "print 3 / 2"
        expected = f"print(f'''{{localize(3 / 2, num_sys='Latin')}}''')"
        output = "1.5"

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=17,
            output=output
        )

    def test_print_int_arabic(self):
        code = "print ١١"

        expected = "print(f'''{localize(11, num_sys='Arabic')}''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            output='١١'
        )

    def test_sleep_division_float(self):
        code = "sleep 1 / 20"
        expected = self.sleep_transpiled('1 / 20')

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=17
        )

    def test_sleep_division_float_with_var(self):
        code = textwrap.dedent("""\
            n = 1
            sleep n / 20""")
        expected = self.dedent(
            "n = Value(1, num_sys='Latin')",
            self.sleep_transpiled(f'{self.number_transpiled("n")} / {self.number_transpiled(20)}'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=17
        )

    def test_sleep_division_float_var(self):
        code = textwrap.dedent("""\
            time = 0.2
            sleep time""")

        expected = self.dedent(
            "_time = Value(0.2, num_sys='Latin')",
            self.sleep_transpiled('_time.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=17
        )

    def test_sleep_division_float_literal(self):
        code = "sleep 0.2"
        expected = self.sleep_transpiled('0.2')

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=15
        )

    def test_print_microbit(self):
        code = "print 'a'"
        expected = "display.scroll('a')"

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=17,
            microbit=True
        )

    def test_print_literal_strings(self):
        code = """print "It's " '"Hedy"!'"""
        expected = """print(f'''It\\'s "Hedy"!''')"""

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
        )

    def test_print_line_with_spaces_works(self):
        code = "print 'hallo'\n      \nprint 'hallo'"
        expected = "print(f'''hallo''')\nprint(f'''hallo''')"
        expected_commands = [Command.print, Command.print]

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=expected_commands,
            max_level=17)

    def test_print_string_with_triple_quotes_gives_error(self):
        code = textwrap.dedent("""\
            var = " is not allowed"
            print "'''" + var """)

        self.multi_level_tester(
            code=code,
            max_level=17,
            translate=False,
            exception=hedy.exceptions.UnsupportedStringValue
        )

    # issue #745
    def test_print_list_gives_type_error(self):
        code = textwrap.dedent("""\
            plaatsen is 1, 2, 3
            print plaatsen""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_print_subtraction_with_text(self):
        code = "print 'And the winner is ' 5 - 5"
        expected = f"print(f'''And the winner is {{localize(5 - 5, num_sys='Latin')}}''')"
        output = 'And the winner is 0'

        self.multi_level_tester(max_level=17, code=code, expected=expected, output=output)

    def test_print_list_random(self):
        code = textwrap.dedent("""\
            numbers is 1, 2, 4
            print numbers at random""")

        expected = self.dedent(
            "numbers = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(4, num_sys='Latin')])",
            self.list_access_transpiled('random.choice(numbers.data)'),
            "print(f'''{random.choice(numbers.data)}''')")

        self.multi_level_tester(
            code=code,
            max_level=15,
            expected=expected,
            expected_commands=['is', 'print', 'random'],
            skip_faulty=False
        )

    def test_print_list_access_index(self):
        code = textwrap.dedent("""\
            numbers is 5, 4, 3
            print numbers at 1""")

        expected = self.dedent(
            "numbers = Value([Value(5, num_sys='Latin'), Value(4, num_sys='Latin'), Value(3, num_sys='Latin')])",
            self.list_access_transpiled('numbers.data[int(1)-1]'),
            "print(f'''{numbers.data[int(1)-1]}''')")

        check_in_list = (lambda x: HedyTester.run_code(x) == '5')

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            extra_check_function=check_in_list
        )

    def test_print_single_quoted_text(self):
        code = "print 'hallo wereld!'"
        expected = "print(f'''hallo wereld!''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_chinese_quoted_text(self):
        code = "print “逃离鬼屋！”"
        expected = "print(f'''逃离鬼屋！''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_french_quoted_text(self):
        code = "print «bonjour tous le monde!»"
        expected = "print(f'''bonjour tous le monde!''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_chinese_double_quoted_text(self):
        code = "print ‘逃离鬼屋！’"
        expected = "print(f'''逃离鬼屋！''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_double_quoted_text(self):
        code = 'print "hallo wereld!"'
        expected = "print(f'''hallo wereld!''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_single_quoted_text_with_inner_double_quote(self):
        code = """print 'quote is "'"""
        expected = """print(f'''quote is "''')"""

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_double_quoted_text_with_inner_single_quote(self):
        code = '''print "It's me"'''
        expected = """print(f'''It\\'s me''')"""

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_no_space(self):
        code = "print'hallo wereld!'"
        expected = "print(f'''hallo wereld!''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected)

    def test_print_comma(self):
        code = "print 'Hi, I am Hedy'"
        expected = "print(f'''Hi, I am Hedy''')"
        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    def test_print_slash(self):
        code = "print 'Yes/No'"
        expected = "print(f'''Yes/No''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_backslash(self):
        code = "print 'Yes\\No'"
        expected = "print(f'''Yes\\\\No''')"
        output = "Yes\\No"

        self.multi_level_tester(
            code=code,
            expected=expected,
            output=output,
            max_level=17,
            translate=True
        )

    def test_print_with_backslash_at_end(self):
        code = "print 'Welcome to \\'"
        expected = "print(f'''Welcome to \\\\''')"
        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            translate=True
        )

    def test_print_with_spaces(self):
        code = "print        'hallo!'"
        expected = "print(f'''hallo!''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_asterisk(self):
        code = "print '*Jouw* favoriet is dus kleur'"
        expected = "print(f'''*Jouw* favoriet is dus kleur''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_hash(self):
        code = "print 'comments start with the # sign'"
        expected = "print(f'''comments start with the # sign''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_single_quoted_text_var(self):
        code = textwrap.dedent("""\
        naam is "'Hedy'"
        print 'ik heet ' naam""")

        expected = textwrap.dedent("""\
        naam = Value("'Hedy'")
        print(f'''ik heet {naam}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_double_quoted_text_var(self):
        code = textwrap.dedent("""\
        naam is '"Hedy"'
        print 'ik heet ' naam""")

        expected = textwrap.dedent("""\
        naam = Value('"Hedy"')
        print(f'''ik heet {naam}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    # issue 1795
    def test_print_quoted_var_reference(self):
        code = textwrap.dedent("""\
        naam is "'Daan'"
        woord1 is 'zomerkamp'
        print 'naam' ' is naar het' 'woord1'""")

        expected = textwrap.dedent("""\
        naam = Value("'Daan'")
        woord1 = Value('zomerkamp')
        print(f'''naam is naar hetwoord1''')""")

        self.multi_level_tester(code=code,
                                expected=expected,
                                unused_allowed=True,
                                max_level=17)

    @parameterized.expand(HedyTester.quotes)
    def test_print_concat_quoted_strings(self, q):
        code = f"""print {q}Hi {q} + {q}there{q}"""
        expected = f"""print(f'''{{localize('Hi ' + 'there')}}''')"""

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_concat_double_quoted_strings_with_inner_single_quotes(self):
        code = '''print "Hi there! " + "It's Hedy!"'''
        expected = f"""print(f'''{{localize('Hi there! ' + "It's Hedy!")}}''')"""

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.quotes)
    def test_print_concat_var_and_literal_string(self, q):
        code = textwrap.dedent(f"""\
        hi = {q}Hi{q}
        print hi + {q} there{q}""")
        expected = textwrap.dedent(f"""\
        hi = Value('Hi')
        print(f'''{{localize({self.sum_transpiled('hi', "' there'")}, num_sys=get_num_sys(hi))}}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_chained_assignments(self):
        code = textwrap.dedent("""\
            x is 1 + 2
            y is x + 3
            print y + 4""")

        expected = textwrap.dedent(f"""\
            x = Value(1 + 2, num_sys='Latin')
            y = Value({self.sum_transpiled('x', 3)}, num_sys=get_num_sys(x))
            print(f'''{{localize({self.sum_transpiled('y', 4)}, num_sys=get_num_sys(y))}}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_assign_to_list_access(self):
        code = textwrap.dedent("""\
            field = '.', '.', '.', '.', '.', '.'
            field at 1 = 'x'
            print field at 1""")

        expected = self.dedent(
            "field = Value([Value('.'), Value('.'), Value('.'), Value('.'), Value('.'), Value('.')])",
            "field.data[int(1)-1] = Value('x')",
            self.list_access_transpiled('field.data[int(1)-1]'),
            "print(f'''{field.data[int(1)-1]}''')")

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    def test_if_and_list_access(self):
        code = textwrap.dedent("""\
            player = 'x'
            choice = 1
            field = '.', '.', '.', '.', '.', '.', '.', '.', '.'
            if field at choice = '.'
                field at choice = player
            else
                print 'illegal move!'""")

        expected = self.dedent(
            f"""\
            player = Value('x')
            choice = Value(1, num_sys='Latin')
            field = {self.list_transpiled("'.'", "'.'", "'.'", "'.'", "'.'", "'.'", "'.'", "'.'", "'.'")}""",
            self.list_access_transpiled('field.data[int(choice.data)-1]'),
            """\
            if field.data[int(choice.data)-1].data == '.':
              field.data[int(choice.data)-1] = player
            else:
              print(f'''illegal move!''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    def test_print_calc(self):
        code = textwrap.dedent("""\
            var is 5
            print var + 5""")

        expected = textwrap.dedent(f"""\
            var = Value(5, num_sys='Latin')
            print(f'''{{localize({self.sum_transpiled('var', 5)}, num_sys=get_num_sys(var))}}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_var_before_assign_gives_error(self):
        code = textwrap.dedent("""\
        print 'the program is ' name
        name is 'Hedy'""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.AccessBeforeAssignException,
            skip_faulty=False,
            max_level=17
        )

    #
    # forward tests
    #
    def test_forward_int(self):
        code = "forward 50"
        expected = self.forward_transpiled(50)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_forward_arabic_numeral(self):
        code = "forward ١١١١١١١"
        expected = self.forward_transpiled(1111111)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_forward_hindi_numeral(self):
        code = "forward ५५५"
        expected = self.forward_transpiled(555)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_forward_float(self):
        code = "forward 50.5"
        expected = self.forward_transpiled(50.5)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_forward_with_int_var(self):
        code = textwrap.dedent("""\
            a is 50
            forward a""")
        expected = self.dedent(
            "a = Value(50, num_sys='Latin')",
            self.forward_transpiled('a.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_forward_with_hindi_int_var(self):
        code = textwrap.dedent("""\
            a is ५५५
            forward a""")
        expected = self.dedent(
            "a = Value(555, num_sys='Devanagari')",
            self.forward_transpiled('a.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle())

    def test_forward_with_keyword_variable(self):
        code = textwrap.dedent("""\
           sum is 50
           forward sum""")
        expected = self.dedent(
            "_sum = Value(50, num_sys='Latin')",
            self.forward_transpiled('_sum.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle())

    def test_forward_with_string_variable_gives_type_error(self):
        code = textwrap.dedent("""\
            a is "ten"
            forward a""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException,
        )

    def test_forward_with_list_access(self):
        code = textwrap.dedent("""\
            directions is 10, 100, 360
            forward directions at 1""")

        expected = self.dedent(
            f"directions = {self.list_transpiled(10, 100, 360)}",
            self.list_access_transpiled('directions.data[int(1)-1]'),
            self.forward_transpiled('directions.data[int(1)-1].data'))

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_forward_with_list_access_random(self):
        code = textwrap.dedent("""\
        directions is 10, 100, 360
        forward directions at random""")

        expected = self.dedent(
            f"directions = {self.list_transpiled(10, 100, 360)}",
            self.list_access_transpiled('random.choice(directions.data)'),
            self.forward_transpiled('random.choice(directions.data).data'))

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_forward_expression(self):
        code = "forward 50 / 2"
        expected = self.forward_transpiled('50 / 2')

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_forward_expression_with_var(self):
        code = textwrap.dedent("""\
            n = 50
            forward n / 2""")
        expected = self.dedent(
            "n = Value(50, num_sys='Latin')",
            self.forward_transpiled(f'{self.number_transpiled("n")} / {self.number_transpiled(2)}'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    #
    # turn
    #
    def test_turn_number(self):
        code = "turn 180"
        expected = self.turn_transpiled(180)

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_turn_expression(self):
        code = "turn 180 / 2"
        expected = self.turn_transpiled('180 / 2')

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_turn_expression_with_var(self):
        code = textwrap.dedent("""\
            n = 360
            turn n / 2""")
        expected = self.dedent(
            "n = Value(360, num_sys='Latin')",
            self.turn_transpiled(f'{self.number_transpiled("n")} / {self.number_transpiled(2)}'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_turn_with_number_var(self):
        code = textwrap.dedent("""\
            direction is 70
            turn direction""")
        expected = self.dedent(
            "direction = Value(70, num_sys='Latin')",
            self.turn_transpiled('direction.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_turn_with_keyword_var(self):
        code = textwrap.dedent("""\
            sum is 70
            turn sum""")
        expected = self.dedent(
            "_sum = Value(70, num_sys='Latin')",
            self.turn_transpiled('_sum.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=17
        )

    def test_turn_with_non_latin_float_number_var(self):
        code = textwrap.dedent("""\
            الزاوية هو ٩.٠
            استدر الزاوية
            تقدم ١٠.١٠""")

        expected = self.dedent(
            "الزاوية = Value(9.0, num_sys='Arabic')",
            self.turn_transpiled("الزاوية.data"),
            self.forward_transpiled("10.1")
        )

        self.multi_level_tester(
            code=code,
            lang='ar',
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_turtle_with_expression(self):
        code = textwrap.dedent("""\
            num = 10.6
            turn num + 10.5
            forward 10.5 + num""")

        expected = self.dedent(
            "num = Value(10.6, num_sys='Latin')",
            self.turn_transpiled(self.sum_transpiled('num', '10.5')),
            self.forward_transpiled(self.sum_transpiled('10.5', 'num'))
        )

        self.multi_level_tester(code=code, expected=expected)

    def test_turn_with_string_var_gives_type_error(self):
        code = textwrap.dedent("""\
            direction is 'ten'
            turn direction""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException,
        )

    def test_turn_with_non_ascii_var(self):
        code = textwrap.dedent("""\
            ángulo is 90
            turn ángulo""")
        expected = self.dedent(
            "ángulo = Value(90, num_sys='Latin')",
            self.turn_transpiled('ángulo.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            expected_commands=['is', 'turn']
        )

    def test_turn_with_list_access(self):
        code = textwrap.dedent("""\
            directions is 10, 100
            turn directions at 1""")

        expected = self.dedent(
            "directions = Value([Value(10, num_sys='Latin'), Value(100, num_sys='Latin')])",
            self.list_access_transpiled('directions.data[int(1)-1]'),
            self.turn_transpiled('directions.data[int(1)-1].data'))

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_turn_with_list_access_random(self):
        code = textwrap.dedent("""\
            directions is 10, 100, 360
            turn directions at random""")

        expected = self.dedent(
            f"directions = {self.list_transpiled(10, 100, 360)}",
            self.list_access_transpiled('random.choice(directions.data)'),
            self.turn_transpiled('random.choice(directions.data).data'))

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_ask_forward(self):
        code = textwrap.dedent("""\
        afstand is ask 'hoe ver dan?'
        forward afstand""")

        expected = self.dedent(
            self.input_transpiled('afstand', 'hoe ver dan?'),
            self.forward_transpiled('afstand.data'))

        self.multi_level_tester(
            max_level=14,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    #
    # Test comment
    #
    def test_print_comment(self):
        code = "print 'Hallo welkom bij Hedy!' # This is a comment"
        expected = "print(f'''Hallo welkom bij Hedy!''')"
        output = 'Hallo welkom bij Hedy!'

        self.multi_level_tester(
            max_level=17,
            code=code,
            expected=expected,
            output=output
        )

    def test_assign_comment(self):
        code = 'test = "Welkom bij Hedy" # This is a comment'
        expected = "test = Value('Welkom bij Hedy')"
        self.multi_level_tester(
            max_level=18,
            code=code,
            expected=expected,
            unused_allowed=True
        )

    #
    # ask tests
    #
    def test_ask_number(self):
        code = "n is ask 42"
        expected = self.input_transpiled('n', '42')

        self.multi_level_tester(code=code, expected=expected, max_level=14, unused_allowed=True)

    def test_ask_arabic_number(self):
        code = "n is ask ٢٣٤"
        expected = self.input_transpiled('n', "{localize(234, num_sys='Arabic')}")

        self.multi_level_tester(code=code, expected=expected, max_level=14, unused_allowed=True)

    def test_ask_multi_args(self):
        code = "n is ask 'hello' 'Hedy' 4 ١١"
        expected = self.input_transpiled('n', "helloHedy4{localize(11, num_sys='Arabic')}")

        self.multi_level_tester(code=code, expected=expected, max_level=14, unused_allowed=True)

    def test_ask_number_answer(self):
        code = textwrap.dedent("""\
            prijs is ask 'hoeveel?'
            gespaard is 7
            sparen is prijs - gespaard""")
        minus_op = f"{self.number_transpiled('prijs')} - {self.number_transpiled('gespaard')}"
        expected = self.dedent(
            self.input_transpiled('prijs', 'hoeveel?'),
            "gespaard = Value(7, num_sys='Latin')",
            f"sparen = Value({minus_op}, num_sys=get_num_sys(prijs))")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    def test_play(self):
        code = textwrap.dedent("""\
            n = 'C4' #
            play n""")

        expected = HedyTester.dedent(
            "n = Value('C4')",
            self.play_transpiled('n.data'))

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected,
            max_level=17
        )

    def test_ask_with_list_var(self):
        code = textwrap.dedent("""\
        colors is 'orange', 'blue', 'green'
        favorite is ask 'Is your fav color' colors at 1""")

        expected = self.dedent(
            "colors = Value([Value('orange'), Value('blue'), Value('green')])",
            self.list_access_transpiled('colors.data[int(1)-1]'),
            self.input_transpiled('favorite', 'Is your fav color{colors.data[int(1)-1]}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    def test_ask_literal_strings(self):
        code = """var is ask "It's " '"Hedy"!'"""
        expected = self.input_transpiled('var', """It\\'s "Hedy"!""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_with_string_var(self, q):
        code = textwrap.dedent(f"""\
        color is {q}orange{q}
        favorite is ask {q}Is your fav color{q} color""")

        expected = self.dedent(
            "color = Value('orange')",
            self.input_transpiled('favorite', 'Is your fav color{color}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    @parameterized.expand(['10', '10.0'])
    def test_ask_with_number_var(self, number):
        code = textwrap.dedent(f"""\
        number is {number}
        favorite is ask 'Is your fav number' number""")

        expected = self.dedent(
            f"number = Value({number}, num_sys='Latin')",
            self.input_transpiled('favorite', 'Is your fav number{number}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    def test_ask_with_keyword_var(self):
        code = textwrap.dedent("""\
            sum is 'Hedy'
            v is ask sum""")

        expected = self.dedent(
            "_sum = Value('Hedy')",
            self.input_transpiled('v', '{_sum}'))

        self.multi_level_tester(code=code, expected=expected, max_level=14, unused_allowed=True)

    def test_ask_list_gives_type_error(self):
        code = textwrap.dedent("""\
        numbers is 1, 2, 3
        favorite is ask 'Is your fav number' numbers""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_ask_single_quoted_text(self):
        code = "details is ask 'tell me more'"
        expected = self.input_transpiled('details', 'tell me more')

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    def test_ask_double_quoted_text(self):
        code = 'details is ask "tell me more"'
        expected = self.input_transpiled('details', 'tell me more')

        self.multi_level_tester(code=code, expected=expected, unused_allowed=True, max_level=14)

    def test_ask_single_quoted_text_with_inner_double_quote(self):
        code = """details is ask 'say "no"'"""
        expected = self.input_transpiled('details', 'say "no"')

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    def test_ask_double_quoted_text_with_inner_single_quote(self):
        code = f'''details is ask "say 'no'"'''
        expected = self.input_transpiled('details', "say \\'no\\'")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    def test_ask_with_comma(self):
        code = "dieren is ask 'hond, kat, kangoeroe'"
        expected = self.input_transpiled('dieren', 'hond, kat, kangoeroe')

        self.multi_level_tester(code=code, expected=expected, max_level=14, unused_allowed=True)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_es(self, q):
        code = f"""color is ask {q}Cuál es tu color favorito?{q}"""
        expected = self.input_transpiled('color', 'Cuál es tu color favorito?')

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_bengali_var(self, q):
        code = f"""রং is ask {q}আপনার প্রিয় রং কি?{q}"""
        expected = self.input_transpiled('রং', 'আপনার প্রিয় রং কি?')

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    def test_ask_list_random(self):
        code = textwrap.dedent("""\
            numbers is 1, 2, 3
            favorite is ask 'Is your fav number ' numbers at random""")
        expected = self.dedent(
            "numbers = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(3, num_sys='Latin')])",
            self.list_access_transpiled('random.choice(numbers.data)'),
            self.input_transpiled('favorite', 'Is your fav number {random.choice(numbers.data)}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    def test_ask_list_access_index(self):
        code = textwrap.dedent("""\
            numbers is 1, 2, 3
            favorite is ask 'Is your fav number ' numbers at 2""")

        expected = self.dedent(
            "numbers = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(3, num_sys='Latin')])",
            self.list_access_transpiled('numbers.data[int(2)-1]'),
            self.input_transpiled('favorite', 'Is your fav number {numbers.data[int(2)-1]}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    def test_ask_string_var(self):
        code = textwrap.dedent("""\
            color is "orange"
            favorite is ask 'Is your fav color ' color""")
        expected = self.dedent(
            "color = Value('orange')",
            self.input_transpiled('favorite', 'Is your fav color {color}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    def test_ask_integer_var(self):
        code = textwrap.dedent("""\
            number is 10
            favorite is ask 'Is your fav number ' number""")
        expected = self.dedent(
            "number = Value(10, num_sys='Latin')",
            self.input_transpiled('favorite', 'Is your fav number {number}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=14)

    def test_ask_var_before_assign_gives_error(self):
        code = textwrap.dedent("""\
        n is ask 'the program is ' name
        name is 'Hedy'""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.AccessBeforeAssignException,
            skip_faulty=False,
            max_level=17
        )

    def test_assign_another_var(self):
        code = textwrap.dedent("""\
            a is 10
            b = a""")
        expected = textwrap.dedent("""\
            a = Value(10, num_sys='Latin')
            b = a""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    #
    # sleep tests
    #
    def test_sleep_with_number(self):
        code = "sleep 20"
        expected = self.sleep_transpiled('20')

        self.multi_level_tester(code=code, expected=expected)

    def test_sleep_with_number_hi(self):
        code = "sleep २"
        expected = self.sleep_transpiled('2')

        self.multi_level_tester(code=code, expected=expected)

    def test_sleep_with_number_ar(self):
        code = "sleep ٣"
        expected = self.sleep_transpiled('3')

        self.multi_level_tester(code=code, expected=expected)

    def test_sleep_with_number_variable(self):
        code = textwrap.dedent("""\
            n is 2
            sleep n""")
        expected = self.dedent(
            "n = Value(2, num_sys='Latin')",
            self.sleep_transpiled("n.data"))

        self.multi_level_tester(code=code, expected=expected)

    def test_sleep_with_keyword_variable(self):
        code = textwrap.dedent("""\
            sum is 2
            sleep sum""")
        expected = self.dedent(
            "_sum = Value(2, num_sys='Latin')",
            self.sleep_transpiled("_sum.data"))

        self.multi_level_tester(max_level=17, code=code, expected=expected)

    def test_sleep_with_string_variable_gives_error(self):
        code = textwrap.dedent("""\
            n is "test"
            sleep n""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_sleep_with_list_access(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n at 1""")
        expected = self.dedent(
            "n = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(3, num_sys='Latin')])",
            self.list_access_transpiled('n.data[int(1)-1]'),
            self.sleep_transpiled('n.data[int(1)-1].data'))

        self.multi_level_tester(max_level=15, code=code, expected=expected)

    def test_sleep_with_list_random(self):
        self.maxDiff = None
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n at random""")
        expected = self.dedent(
            "n = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(3, num_sys='Latin')])",
            self.list_access_transpiled('random.choice(n.data)'),
            f"time.sleep({self.int_transpiled('random.choice(n.data).data')})")

        self.multi_level_tester(max_level=15, code=code, expected=expected)

    def test_sleep_with_list_gives_error(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_sleep_with_input_variable(self):
        code = textwrap.dedent("""\
            n is ask "how long"
            sleep n""")

        expected = self.dedent(
            self.input_transpiled('n', 'how long'),
            self.sleep_transpiled("n.data"))

        self.multi_level_tester(max_level=14, code=code, expected=expected)

    def test_sleep_with_calc(self):
        code = textwrap.dedent("""\
            n is 1 * 2 + 3
            sleep n""")

        expected = self.dedent(
            f"n = Value(1 * 2 + 3, num_sys='Latin')",
            self.sleep_transpiled("n.data"))

        self.multi_level_tester(code=code, expected=expected)

    #
    # assign tests
    #
    def test_assign_integer(self):
        code = "naam is 14"
        expected = "naam = Value(14, num_sys='Latin')"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected)

    def test_assign_keyword_var(self):
        code = "sum is 'Felienne'"
        expected = "_sum = Value('Felienne')"

        self.multi_level_tester(code=code, expected=expected, unused_allowed=True)

    def test_assign_list(self):
        code = "animals is 'duck', 'dog', 'penguin'"
        expected = "animals = Value([Value('duck'), Value('dog'), Value('penguin')])"

        self.multi_level_tester(code=code,
                                expected=expected,
                                unused_allowed=True,
                                max_level=15)

    def test_assign_list_random(self):
        code = textwrap.dedent("""\
        dieren is 'hond', 'kat', 'kangoeroe'
        dier is dieren at random""")

        expected = self.dedent("dieren = Value([Value('hond'), Value('kat'), Value('kangoeroe')])",
                               self.list_access_transpiled('random.choice(dieren.data)'),
                               "dier = random.choice(dieren.data)")

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            max_level=15)

    def test_assign_list_with_dutch_comma_arabic_lang(self):
        code = "صديقي هو 'احمد', 'خالد', 'حسن'"
        expected = "صديقي = Value([Value('احمد'), Value('خالد'), Value('حسن')])"

        self.multi_level_tester(
            code=code,
            expected=expected,
            lang='ar',
            max_level=15,
            unused_allowed=True,
            # translation must be off because the Latin commas will be converted to arabic commas and this is correct
            translate=False
        )

    def test_assign_list_with_arabic_comma_and_is(self):
        code = "animals هو 'cat'، 'dog'، 'platypus'"
        expected = "animals = Value([Value('cat'), Value('dog'), Value('platypus')])"

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            unused_allowed=True,
            lang='ar'
        )

    def test_assign_list_with_arabic_comma(self):
        code = "صديقي هو 'احمد'، 'خالد'، 'حسن'"
        expected = "صديقي = Value([Value('احمد'), Value('خالد'), Value('حسن')])"

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            unused_allowed=True,
            lang='ar'
        )

    def test_assign_string_without_quotes(self):
        code = "name is felienne"

        self.multi_level_tester(
            code=code,
            max_level=17,
            exception=hedy.exceptions.UnquotedAssignTextException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1
        )

    def test_assign_string_without_quotes_line_2(self):
        code = textwrap.dedent("""\
        print 'lalala'
        name is Harry""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            exception=hedy.exceptions.UnquotedAssignTextException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2
        )

    @parameterized.expand(HedyTester.quotes)
    def test_assign_string(self, q):
        code = f"name is {q}felienne{q}"
        expected = "name = Value('felienne')"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected)

    @parameterized.expand(HedyTester.quotes)
    def test_assign_empty_string(self, q):
        code = f"name = {q}{q}"
        expected = "name = Value('')"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected)

    def test_assign_text_with_inner_double_quote(self):
        code = """a is 'It says "Hedy"'"""
        expected = """a = Value('It says "Hedy"')"""

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected)

    def test_assign_text_with_inner_single_quote(self):
        code = '''a is "It's Hedy!"'''
        expected = '''a = Value("It's Hedy!")'''

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected)

    def test_assign_text_to_hungarian_var(self):
        code = "állatok is 'kutya'"
        expected = "állatok = Value('kutya')"

        self.multi_level_tester(code=code, expected=expected, unused_allowed=True)

    def test_assign_bengali_var(self):
        var = hedy.escape_var("নাম")
        code = "নাম is 'হেডি'"
        expected = f"{var} = Value('হেডি')"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected)

    def test_assign_python_keyword(self):
        code = "for is 'Hedy'"
        expected = "_for = Value('Hedy')"

        self.multi_level_tester(code=code, expected=expected, unused_allowed=True)

    def test_assign_concat(self):
        code = """a = "It's" + ' "Hedy"!'"""
        expected = f"""a = Value("It's" + ' "Hedy"!')"""

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected)

    #
    # add/remove tests
    #
    def test_add_ask_to_list(self):
        code = textwrap.dedent("""\
            color is ask 'what is your favorite color?'
            colors is 'green', 'red', 'blue'
            add color to colors""")

        expected = self.dedent(
            self.input_transpiled('color', 'what is your favorite color?'),
            "colors = Value([Value('green'), Value('red'), Value('blue')])",
            "colors.data.append(color)")

        self.multi_level_tester(code=code, expected=expected, max_level=14)

    def test_remove_ask_from_list(self):
        code = textwrap.dedent("""\
            colors is 'green', 'red', 'blue'
            color is ask 'what color to remove?'
            remove color from colors""")

        expected = self.dedent(
            "colors = Value([Value('green'), Value('red'), Value('blue')])",
            self.input_transpiled('color', 'what color to remove?'),
            self.remove_transpiled('colors', 'color'))

        self.multi_level_tester(code=code, expected=expected, max_level=14)

    def test_remove_from_list_random(self):
        code = textwrap.dedent("""\
            colors is 'green', 'red', 'blue'
            remove colors at random from colors""")

        expected = self.dedent(
            "colors = Value([Value('green'), Value('red'), Value('blue')])",
            self.remove_transpiled('colors', 'random.choice(colors.data)'))

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    def test_add_to_list_with_string_var_gives_error(self):
        code = textwrap.dedent("""\
        color is 'yellow'
        colors is 'green', 'red', 'blue'
        add colors to color""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_add_to_list_with_input_var_gives_error(self):
        code = textwrap.dedent("""\
        colors is ask 'What are the colors?'
        favorite is 'red'
        add favorite to colors""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_remove_from_list_with_string_var_gives_error(self):
        code = textwrap.dedent("""\
        color is 'yellow'
        colors is 'green', 'red', 'blue'
        remove colors from color""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_remove_from_list_with_input_var_gives_error(self):
        code = textwrap.dedent("""\
        colors is ask 'What are the colors?'
        favorite is 'red'
        remove favorite from colors""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_list_creation_with_numbers(self):
        code = textwrap.dedent("""\
            getallen is 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
            getal is getallen at random""")

        expected = self.dedent(
            f"getallen = {self.list_transpiled(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)}",
            self.list_access_transpiled('random.choice(getallen.data)'),
            "getal = random.choice(getallen.data)")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=15)

    def test_assign_list_with_spaces(self):
        code = "voorspellingen = 'je wordt rijk' , 'je wordt verliefd' , 'je glijdt uit over een bananenschil'"
        expected = f"""voorspellingen = {self.list_transpiled(
            "'je wordt rijk'",
            "'je wordt verliefd'",
            "'je glijdt uit over een bananenschil'")}"""

        self.multi_level_tester(code=code, expected=expected, max_level=15, unused_allowed=True)

    #
    # if tests
    #
    @parameterized.expand(HedyTester.equality_comparison_with_is)
    def test_if_equality_print(self, eq):
        code = textwrap.dedent(f"""\
        naam = 'Hedy'
        if naam {eq} 'Hedy'
            print 'koekoek'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if naam.data == 'Hedy':
          print(f'''koekoek''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=['is', 'if', 'print'],
            max_level=16)

    def test_if_equality_no_spaces_print(self):
        code = textwrap.dedent(f"""\
        naam = 'Hedy'
        if naam='Hedy'
            print 'koekoek'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if naam.data == 'Hedy':
          print(f'''koekoek''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=['is', 'if', 'print'],
            max_level=16)  # space between = is not preserved (but is needed for the test)

    def test_if_equality_rhs_with_space(self):
        code = textwrap.dedent("""\
           naam is 'James'
           if naam is 'James Bond'
               print 'shaken'""")

        expected = textwrap.dedent("""\
           naam = Value('James')
           if naam.data == 'James Bond':
             print(f'''shaken''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_equality_single_quoted_rhs_with_inner_double_quote(self):
        code = textwrap.dedent(f"""\
        answer is 'no'
        if answer is 'He said "no"'
          print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = Value('no')
        if answer.data == 'He said "no"':
          print(f'''no''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_equality_double_quoted_rhs_with_inner_single_quote(self):
        code = textwrap.dedent(f"""\
        answer is 'no'
        if answer is "He said 'no'"
          print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = Value('no')
        if answer.data == 'He said \\'no\\'':
          print(f'''no''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_equality_linebreak_comment_print(self):
        code = textwrap.dedent("""\
        naam is 'Hedy'
        if naam is 'Hedy'
            # comment
            print 'hedy'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if naam.data == 'Hedy':
          print(f'''hedy''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_equality_comment_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is 'Hedy'
        if naam is 'Hedy'  # this linebreak is allowed
            print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if naam.data == 'Hedy':
          print(f'''leuk''')""")

        self.multi_level_tester(max_level=16, code=code, expected=expected, output='leuk')

    def test_if_equality_linebreak_print_comment(self):
        code = textwrap.dedent("""\
        naam is 'Hedy'
        if naam is 'Hedy'
            print 'leuk'  # this linebreak is allowed""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if naam.data == 'Hedy':
          print(f'''leuk''')""")

        self.multi_level_tester(max_level=16, code=code, expected=expected, output='leuk')

    def test_if_equality_trailing_space_linebreak_print(self):
        value = "'trailing_space'  "
        code = textwrap.dedent(f"""\
        naam is 'James'
        if naam is {value}
            print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = Value('James')
        if naam.data == 'trailing_space':
          print(f'''shaken''')""")

        self.multi_level_tester(max_level=16, code=code, expected=expected)

    def test_if_equality_negative_number(self):
        code = textwrap.dedent("""\
        antwoord = -10
        if antwoord is -10
            print 'Nice'""")

        expected = textwrap.dedent("""\
        antwoord = Value(-10, num_sys='Latin')
        if antwoord.data == -10:
          print(f'''Nice''')""")

        self.multi_level_tester(code=code, expected=expected, output='Nice', max_level=16)

    def test_if_2_vars_equality_print(self):
        code = textwrap.dedent("""\
        jouwkeuze is 'schaar'
        computerkeuze is 'schaar'
        if computerkeuze is jouwkeuze
            print 'gelijkspel!'""")

        expected = textwrap.dedent("""\
        jouwkeuze = Value('schaar')
        computerkeuze = Value('schaar')
        if computerkeuze.data == jouwkeuze.data:
          print(f'''gelijkspel!''')""")

        self.multi_level_tester(max_level=16, code=code, expected=expected, output='gelijkspel!')

    # Lists can be compared for equality starting with level 14
    def test_if_equality_lists(self):
        # Lists can be compared for equality starting with level 14
        code = textwrap.dedent("""\
         m is 1, 2
         n is 1, 2
         if m is n
             print 'success!'""")
        self.multi_level_tester(
            max_level=13,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_if_equality_with_list_gives_error(self):
        code = textwrap.dedent("""\
        color is 5, 6, 7
        if 1 is color
            print 'success!'""")
        self.multi_level_tester(
            max_level=13,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_if_equality_with_incompatible_types_gives_error(self):
        code = textwrap.dedent("""\
        a is 'test'
        b is 15
        if a is b
          c is 1""")
        self.multi_level_tester(
            max_level=16,
            code=code,
            exception=hedy.exceptions.InvalidTypeCombinationException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3
        )

    def test_equality_arabic_and_latin_vars(self):
        code = textwrap.dedent("""\
            nummer1 is ٢
            nummer2 is 2
            if nummer1 = nummer2
                print 'jahoor!'
            else
                print 'neejoh!'""")

        expected = textwrap.dedent("""\
            nummer1 = Value(2, num_sys='Arabic')
            nummer2 = Value(2, num_sys='Latin')
            if nummer1.data == nummer2.data:
              print(f'''jahoor!''')
            else:
              print(f'''neejoh!''')""")

        self.multi_level_tester(
            max_level=16,
            code=code,
            expected=expected,
            output='jahoor!')

    def test_if_arabic_number_equals_latin_number(self):
        code = textwrap.dedent("""\
        if ١١ is 11
          print 'correct'""")

        expected = textwrap.dedent("""\
        if 11 == 11:
          print(f'''correct''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16, output='correct')

    def test_if_arabic_var_equals_latin_number(self):
        code = textwrap.dedent("""\
        a is ١١
        if a is 11
          print 'correct'""")

        expected = textwrap.dedent("""\
        a = Value(11, num_sys='Arabic')
        if a.data == 11:
          print(f'''correct''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16, output='correct')

    #
    # in/not-in list commands
    #
    @parameterized.expand([
        ('in', 'Found'),
        ('not in', 'Not found')
    ])
    def test_if_in_not_in_list_with_strings(self, command, expected_output):
        code = textwrap.dedent(f"""\
         letters is 'a', 'b', 'c'
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

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            output=expected_output,
            skip_faulty=False
        )

    @parameterized.expand([
        ('in', 'True'),
        ('not in', 'False')
    ])
    def test_if_number_in_not_in_list_with_numbers(self, operator, expected_output):
        code = textwrap.dedent(f"""\
        items is 1, 2, 3
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

        self.multi_level_tester(
            max_level=15,
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
            items is 1, 2, 3
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

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            output=expected_output
        )

    @parameterized.expand(['in', 'not in'])
    def test_unquoted_lhs_in_not_in_list_gives_error(self, operator):
        code = textwrap.dedent(f"""\
            items is 1, 2, 3
            if a {operator} items
              print 'True'""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            skip_faulty=False,
            exception=hedy.exceptions.UnquotedAssignTextException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2
        )

    @parameterized.expand(['in', 'not in'])
    def test_undefined_rhs_in_not_in_list_gives_error(self, operator):
        code = textwrap.dedent(f"""\
            items is 1, 2, 3
            if 1 {operator} list
              print 'True'""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            exception=hedy.exceptions.UndefinedVarException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2
        )

    @parameterized.expand([(c, q) for c in HedyTester.in_not_in_list_commands for q in HedyTester.quotes])
    def test_if_in_not_in_list_with_string_var_gives_type_error(self, command, q):
        code = textwrap.dedent(f"""\
        items is {q}red{q}
        if {q}red{q} {command} items
            print {q}found!{q}""")
        self.multi_level_tester(
            max_level=16,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand(HedyTester.in_not_in_list_commands)
    def test_if_not_in_and_in_list_with_input_gives_type_error(self, operator):
        code = textwrap.dedent(f"""\
            items is ask 'What are the items?'
            if 'red' {operator} items
              print 'found!'""")
        self.multi_level_tester(
            max_level=16,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand([('in', 'True'), ('not in', 'False')])
    def test_if_number_in_not_in_list_with_var(self, operator, output):
        code = textwrap.dedent(f"""\
        i = 2
        items is 1, 2, 3
        if i {operator} items
          print 'True'
        else
          print 'False'""")

        expected = textwrap.dedent(f"""\
        i = Value(2, num_sys='Latin')
        items = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(3, num_sys='Latin')])
        if i {operator} items.data:
          print(f'''True''')
        else:
          print(f'''False''')""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            output=output
        )

    @parameterized.expand([('in', 'True'), ('not in', 'False')])
    def test_if_number_in_not_in_list_with_list_access(self, operator, output):
        code = textwrap.dedent(f"""\
            i = 2, 3, 4
            items is 1, 2, 3
            if i at 2 {operator} items
              print 'True'
            else
              print 'False'""")

        expected = self.dedent(
            f"""\
            i = Value([Value(2, num_sys='Latin'), Value(3, num_sys='Latin'), Value(4, num_sys='Latin')])
            items = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(3, num_sys='Latin')])""",
            self.list_access_transpiled('i.data[int(2)-1]'),
            f"""\
            if i.data[int(2)-1] {operator} items.data:
              print(f'''True''')
            else:
              print(f'''False''')""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            expected=expected,
            output=output
        )

    def test_if_ar_number_list_with_latin_numbers(self):
        code = textwrap.dedent("""\
        a is 11, 22, 33
        if ١١ in a
          print 'correct'""")

        expected = textwrap.dedent(f"""\
        a = {self.list_transpiled("11", "22", "33")}
        if {self.in_list_transpiled("Value(11, num_sys='Arabic')", 'a')}:
          print(f'''correct''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=15, output='correct')

    def test_if_ar_number_not_list_with_latin_numbers(self):
        code = textwrap.dedent("""\
        a is 22, 33, 44
        if ١١ not in a
          print 'correct'""")

        expected = textwrap.dedent(f"""\
        a = {self.list_transpiled("22", "33", "44")}
        if {self.not_in_list_transpiled("Value(11, num_sys='Arabic')", 'a')}:
          print(f'''correct''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=15, output='correct')

    #
    # if else tests
    #
    def test_if_equality_print_else_print(self):
        code = textwrap.dedent("""\
        naam is 'Hedy'
        if naam is 'Hedy'
            print 'leuk'
        else
            print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if naam.data == 'Hedy':
          print(f'''leuk''')
        else:
          print(f'''minder leuk''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_equality_assign_else_assign(self):
        code = textwrap.dedent("""\
         a is 5
         if a is 1
             x is 2
         else
             x is 222""")
        expected = textwrap.dedent("""\
         a = Value(5, num_sys='Latin')
         if a.data == 1:
           x = Value(2, num_sys='Latin')
         else:
           x = Value(222, num_sys='Latin')""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=16)

    def test_if_else_followed_by_print(self):
        code = textwrap.dedent("""\
        kleur is 'geel'
        if kleur is 'groen'
            antwoord is 'ok'
        else
            antwoord is 'stom'
        print antwoord""")

        expected = textwrap.dedent("""\
        kleur = Value('geel')
        if kleur.data == 'groen':
          antwoord = Value('ok')
        else:
          antwoord = Value('stom')
        print(f'''{antwoord}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_else_trailing_space_after_else(self):
        else_with_space = 'else  '
        code = textwrap.dedent(f"""\
        a is 1
        if a is 1
            print a
        {else_with_space}
            print 'nee'""")

        expected = textwrap.dedent("""\
        a = Value(1, num_sys='Latin')
        if a.data == 1:
          print(f'''{a}''')
        else:
          print(f'''nee''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_empty_line_with_whitespace_else_print(self):
        code = textwrap.dedent("""\
        if 1 is 2
            sleep

        else
            sleep""")

        expected = textwrap.dedent("""\
        if 1 == 2:
          time.sleep(1)
        else:
          time.sleep(1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_if_else_with_multiple_lines(self):
        code = textwrap.dedent("""\
            antwoord is 10 + 10
            if antwoord is 20
                print 'Goedzo!'
                print 'Het antwoord was inderdaad ' antwoord
            else
                print 'Foutje'
                print 'Het antwoord moest zijn ' antwoord""")

        expected = self.dedent("""\
            antwoord = Value(10 + 10, num_sys='Latin')
            if antwoord.data == 20:
              print(f'''Goedzo!''')
              print(f'''Het antwoord was inderdaad {antwoord}''')
            else:
              print(f'''Foutje''')
              print(f'''Het antwoord moest zijn {antwoord}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    #
    # repeat tests
    #
    def test_repeat_print(self):
        code = textwrap.dedent("""\
        repeat 5 times
            print 'koekoek'""")

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_transpiled(5)}):
          print(f'''koekoek''')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_repeat_arabic_number_print(self):
        code = textwrap.dedent("""\
        repeat ٥ times
            print 'koekoek'""")

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_transpiled(5)}):
          print(f'''koekoek''')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_repeat_print_variable(self):
        code = textwrap.dedent("""\
        n is 5
        repeat n times
            print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
            n = Value(5, num_sys='Latin')
            for __i in range({self.int_transpiled('n.data')}):
              print(f'''me wants a cookie!''')
              time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=17)

    def test_repeat_arabic_var_print(self):
        code = textwrap.dedent("""\
            n is ٥
            repeat n times
                print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
            n = Value(5, num_sys='Arabic')
            for __i in range({self.int_transpiled('n.data')}):
              print(f'''me wants a cookie!''')
              time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=17)

    def test_repeat_keyword_variable(self):
        code = textwrap.dedent("""\
            sum is 2
            repeat sum times
              print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
            _sum = Value(2, num_sys='Latin')
            for __i in range({self.int_transpiled('_sum.data')}):
              print(f'''me wants a cookie!''')
              time.sleep(0.1)""")

        output = textwrap.dedent("""\
            me wants a cookie!
            me wants a cookie!""")

        self.multi_level_tester(code=code, expected=expected, max_level=17, output=output)

    # issue 297
    def test_repeat_print_assign_addition(self):
        code = textwrap.dedent("""\
        count is 1
        repeat 12 times
            print count ' times 12 is ' count * 12
            count is count + 1""")

        print_exp = f"{self.number_transpiled('count')} * {self.number_transpiled(12)}"
        expected = textwrap.dedent(f"""\
        count = Value(1, num_sys='Latin')
        for __i in range({self.int_transpiled(12)}):
          print(f'''{{count}} times 12 is {{localize({print_exp}, num_sys=get_num_sys(count))}}''')
          count = Value({self.sum_transpiled('count', 1)}, num_sys=get_num_sys(count))
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(['5', '𑁫', '५', '૫', '੫', '৫', '೫', '୫', '൫', '௫',
                           '౫', '၅', '༥', '᠕', '៥', '๕', '໕', '꧕', '٥', '۵'])
    def test_repeat_with_all_numerals(self, number):
        code = textwrap.dedent(f"""\
        repeat {number} times
            print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_transpiled(int(number))}):
          print(f'''me wants a cookie!''')
          time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.multi_level_tester(code=code, expected=expected, output=output, max_level=17)

    def test_repeat_nested_in_repeat(self):
        code = textwrap.dedent("""\
        repeat 2 times
            repeat 3 times
                print 'hello'""")

        expected = textwrap.dedent(f"""\
           for __i in range({self.int_transpiled(2)}):
             for __i in range({self.int_transpiled(3)}):
               print(f'''hello''')
               time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_repeat_nested_multi_commands(self):
        code = textwrap.dedent("""\
            repeat 3 times
                print 3
                repeat 5 times
                    print 5
                print 1""")

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
            max_level=17,
            skip_faulty=False
        )

    def test_repeat_empty_lines(self):
        code = textwrap.dedent("""\
            repeat 2 times


                sleep""")

        expected = textwrap.dedent(f"""\
            for __i in range({self.int_transpiled(2)}):
              time.sleep(1)
              time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected)

    def test_repeat_with_comment(self):
        code = textwrap.dedent("""\
        repeat 5 times #This should be ignored
            sleep""")

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_transpiled(5)}):
          time.sleep(1)
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected)

    def test_repeat_whole_line_comment_after(self):
        code = textwrap.dedent("""\
             repeat 2 times
                 sleep
             # let's print!""")

        expected = textwrap.dedent(f"""\
             for __i in range({self.int_transpiled(2)}):
               time.sleep(1)
               time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected)

    def test_repeat_end_line_comment(self):
        code = textwrap.dedent("""\
            repeat 2 times
                sleep # let's print!""")

        expected = textwrap.dedent(f"""\
            for __i in range({self.int_transpiled(2)}):
              time.sleep(1)
              time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected)

    def test_repeat_inner_whole_line_comment(self):
        code = textwrap.dedent("""\
            repeat 2 times
                # let's sleep!
                sleep""")

        expected = textwrap.dedent(f"""\
            for __i in range({self.int_transpiled(2)}):
              time.sleep(1)
              time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected)

    def test_repeat_nested_in_repeat_with_comments(self):
        code = textwrap.dedent("""\
        repeat 2 times # test
            repeat 2 times # test
                # test
                sleep # test
                # test""")

        expected = textwrap.dedent(f"""\
           for __i in range({self.int_transpiled(2)}):
             for __i in range({self.int_transpiled(2)}):
               time.sleep(1)
               time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected)

    #
    # for list tests
    #
    def test_for_list(self):
        code = textwrap.dedent("""\
         dieren is 'hond', 'kat', 'papegaai'
         for dier in dieren
             print dier""")

        expected = textwrap.dedent("""\
         dieren = Value([Value('hond'), Value('kat'), Value('papegaai')])
         for dier in dieren.data:
           print(f'''{dier}''')
           time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=['is', 'for', 'print'],
            max_level=15
        )

    def test_for_list_diff_num_sys(self):
        code = textwrap.dedent("""\
        digits is 1, 𑁨, ३, ૪, ੫
        for d in digits
            print d""")

        list_transpiled = ("Value([""Value(1, num_sys='Latin'), Value(2, num_sys='Brahmi'), "
                           "Value(3, num_sys='Devanagari'), Value(4, num_sys='Gujarati'), "
                           "Value(5, num_sys='Gurmukhi')])")
        expected = textwrap.dedent(f"""\
        digits = {list_transpiled}
        for d in digits.data:
          print(f'''{{d}}''')
          time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output="1\n𑁨\n३\n૪\n੫",
            max_level=15
        )

    def test_for_list_multiline_body(self):
        code = textwrap.dedent("""\
        familie is 'baby', 'mommy', 'daddy', 'grandpa', 'grandma'
        for shark in familie
            print shark ' shark tudutudutudu'
            print shark ' shark tudutudutudu'
            print shark ' shark tudutudutudu'
            print shark ' shark'""")

        expected = textwrap.dedent("""\
        familie = Value([Value('baby'), Value('mommy'), Value('daddy'), Value('grandpa'), Value('grandma')])
        for shark in familie.data:
          print(f'''{shark} shark tudutudutudu''')
          print(f'''{shark} shark tudutudutudu''')
          print(f'''{shark} shark tudutudutudu''')
          print(f'''{shark} shark''')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    #
    # for loop tests
    #
    def test_for_loop(self):
        code = textwrap.dedent("""\
            for i in range 1 to 10
                a is i + 1
                print a""")
        expected = self.dedent(
            self.for_loop('i', 1, 10),
            (f"""\
            a = Value({self.sum_transpiled('i', '1')}, num_sys=get_num_sys(i))
            print(f'''{{a}}''')
            time.sleep(0.1)""", '  '))

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=16,
            expected_commands=['for', 'is', 'addition', 'print'])

    def test_for_loop_arabic(self):
        code = textwrap.dedent("""\
            for دورة in range ١ to ٥
                print دورة""")

        expected = self.dedent(
            self.for_loop('دورة', 1, 5, "'Arabic'"),
            (f"""\
            print(f'''{{دورة}}''')
            time.sleep(0.1)""", '  '))

        self.multi_level_tester(
            max_level=16,
            code=code,
            expected=expected,
            expected_commands=['for', 'print'])

    def test_for_loop_with_int_vars(self):
        code = textwrap.dedent("""\
            begin = 1
            end = 10
            for i in range begin to end
                print i""")

        expected = self.dedent(
            "begin = Value(1, num_sys='Latin')",
            "end = Value(10, num_sys='Latin')",
            self.for_loop('i', 'begin', 'end', 'get_num_sys(begin)'),
            ("print(f'''{i}''')", '  '),
            ("time.sleep(0.1)", '  '))

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_for_loop_with_keyword_vars(self):
        code = textwrap.dedent("""\
            sum = 1
            dir = 10
            for i in range sum to dir
                print i""")

        expected = self.dedent(
            "_sum = Value(1, num_sys='Latin')",
            "_dir = Value(10, num_sys='Latin')",
            self.for_loop('i', '_sum', '_dir', 'get_num_sys(_sum)'),
            ("print(f'''{i}''')", '  '),
            ("time.sleep(0.1)", '  '))

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_for_loop_multiline_body(self):
        code = textwrap.dedent("""\
            a is 2
            b is 3
            for a in range 2 to 4
                a is a + 2
                b is b + 2""")

        expected = self.dedent(
            "a = Value(2, num_sys='Latin')",
            "b = Value(3, num_sys='Latin')",
            self.for_loop('a', 2, 4),
            (f"a = Value({self.sum_transpiled('a', '2')}, num_sys=get_num_sys(a))", "  "),
            (f"b = Value({self.sum_transpiled('b', '2')}, num_sys=get_num_sys(b))", "  "),
            ("time.sleep(0.1)", "  "))

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_for_loop_followed_by_print(self):
        code = textwrap.dedent("""\
            for i in range 1 to 10
                print i
            print 'wie niet weg is is gezien'""")

        expected = self.dedent(
            self.for_loop('i', 1, 10),
            ("print(f'''{i}''')", '  '),
            ("time.sleep(0.1)", '  '),
            "print(f'''wie niet weg is is gezien''')")

        output = textwrap.dedent("""\
            1
            2
            3
            4
            5
            6
            7
            8
            9
            10
            wie niet weg is is gezien""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=16,
            expected_commands=['for', 'print', 'print'],
            output=output)

    # issue 363
    def test_for_loop_if_followed_by_print(self):
        code = textwrap.dedent("""\
        for i in range 0 to 10
            antwoord is 5 * 5
            if antwoord is 24
                print 'fout'
        print 'klaar met for loop'""")

        expected = self.dedent(
            self.for_loop('i', 0, 10),
            """\
              antwoord = Value(5 * 5, num_sys='Latin')
              if antwoord.data == 24:
                print(f'''fout''')
              time.sleep(0.1)
            print(f'''klaar met for loop''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    # issue 599
    def test_for_loop_if(self):
        code = textwrap.dedent("""\
            for i in range 0 to 10
                if i is 2
                    print '2'""")

        expected = self.dedent(
            self.for_loop('i', 0, 10),
            ("if i.data == 2:", '  '),
            ("print(f'''2''')", '    '),
            ("time.sleep(0.1)", '  '))

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_nested_for_loops(self):
        code = textwrap.dedent("""\
            for i in range 1 to 3
                for j in range 1 to 4
                    print 'rondje: ' i ' tel: ' j""")

        expected = self.dedent(
            self.for_loop('i', 1, 3),
            (self.for_loop('j', 1, 4), '  '),
            ("print(f'''rondje: {i} tel: {j}''')", '    '),
            ("time.sleep(0.1)", '    '))

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    #
    # arithmetic expressions tests
    #
    @parameterized.expand([
        ('*', '*', '12'),
        ('/', '/', '3.0'),
        ('-', '-', '4')])
    def test_int_calc(self, op, transpiled_op, output):
        code = f"print 6 {op} 2"
        expected = textwrap.dedent(f"""\
            print(f'''{{localize(6 {transpiled_op} 2, num_sys='Latin')}}''')""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output=output, max_level=17)

    def test_int_sum(self):
        code = f"print 6 + ٢"
        expected = f"print(f'''{{localize(6 + 2, num_sys='Latin')}}''')"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output='8', max_level=17)

    @parameterized.expand([
        ('*', '*', '100'),
        ('/', '/', '1.0'),
        ('-', '-', '3')])
    def test_nested_int_calc(self, op, transpiled_op, output):
        code = f"print 10 {op} 5 {op} 2"
        left = self.number_transpiled(f'10 {transpiled_op} 5')
        right = self.number_transpiled(2)
        expected = f"print(f'''{{localize({left} {transpiled_op} {right}, num_sys='Latin')}}''')"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output=output, max_level=17)

    @parameterized.expand(['-', '*', '/'])
    def test_float_calc(self, op):
        code = f"print 2.5 {op} 2.5"
        expected = f"print(f'''{{localize(2.5 {op} 2.5, num_sys='Latin')}}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_float_sum(self):
        code = f"print 2.5 + 2.5"
        expected = "print(f'''{localize(2.5 + 2.5, num_sys='Latin')}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(['-', '*', '/'])
    def test_float_calc_arabic(self, op):
        code = f"print ١.٥ {op} ١.٥"
        expected = f"print(f'''{{localize(1.5 {op} 1.5, num_sys='Arabic')}}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_float_sum_arabic(self):
        code = f"print ١.٥ + ١.٥"
        expected = "print(f'''{localize(1.5 + 1.5, num_sys='Arabic')}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(['-', '*', '/'])
    def test_print_float_calc_with_string(self, op):
        code = f"print 'het antwoord is ' 2.5 {op} 2.5"
        expected = f"print(f'''het antwoord is {{localize(2.5 {op} 2.5, num_sys='Latin')}}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_float_sum_with_string(self):
        code = f"print 'het antwoord is ' 2.5 + 2.5"
        expected = "print(f'''het antwoord is {localize(2.5 + 2.5, num_sys='Latin')}''')"

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_print_add_negative_number(self):
        code = textwrap.dedent("""\
        n = -4 +3
        print n""")
        expected = textwrap.dedent("""\
        n = Value(-4 + 3, num_sys='Latin')
        print(f'''{n}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_nested_sum_with_ints(self):
        code = """print 1 + 2 + 3"""
        expected = "print(f'''{localize(1 + 2 + 3, num_sys='Latin')}''')"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output='6', max_level=17)

    def test_nested_sum_with_ints_arabic(self):
        code = """print ١ + 2 + 3"""
        expected = "print(f'''{localize(1 + 2 + 3, num_sys='Arabic')}''')"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output='٦', max_level=17)

    def test_nested_sum_with_var(self):
        code = textwrap.dedent("""\
            a = 1
            print a + 2 + 3""")

        expected = textwrap.dedent(f"""\
            a = Value(1, num_sys='Latin')
            print(f'''{{localize({self.sum_transpiled('a', 2)} + 3, num_sys=get_num_sys(a))}}''')""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output='6', max_level=17)

    def test_nested_sum_with_var_arabic(self):
        code = textwrap.dedent("""\
            a = ١
            print a + 2 + 3""")

        expected = textwrap.dedent(f"""\
            a = Value(1, num_sys='Arabic')
            print(f'''{{localize({self.sum_transpiled('a', 2)} + 3, num_sys=get_num_sys(a))}}''')""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output='٦', max_level=17)

    def test_nested_sum_with_floats(self):
        code = """print 1.25 + 2.25 + 3.5"""
        expected = "print(f'''{localize(1.25 + 2.25 + 3.5, num_sys='Latin')}''')"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output='7.0', max_level=17)

    def test_nested_sum_with_negative_nums(self):
        code = """print -1 + -2.5 + -3.25"""
        expected = "print(f'''{localize(-1 + -2.5 + -3.25, num_sys='Latin')}''')"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output='-6.75', max_level=17)

    def test_nested_concat(self):
        code = """print 'a' + 'b' + 'c'"""
        expected = "print(f'''{localize('a' + 'b' + 'c')}''')"

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output='abc', max_level=17)

    def test_nested_concat_with_var(self):
        code = textwrap.dedent("""\
            a = 'a'
            print a + 'b' + 'c'""")

        expected = textwrap.dedent(f"""\
            a = Value('a')
            print(f'''{{localize({self.sum_transpiled('a', "'b'")} + 'c', num_sys=get_num_sys(a))}}''')""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, output='abc', max_level=17)

    @parameterized.expand(['-', '*', '/'])
    def test_float_calc_with_var(self, op):
        code = textwrap.dedent(f"""\
        getal1 is 5
        getal2 is 4.3
        print 'dat is dan: ' getal1 {op} getal2""")
        calc = f"{self.number_transpiled('getal1')} {op} {self.number_transpiled('getal2')}"
        expected = textwrap.dedent(f"""\
        getal1 = Value(5, num_sys='Latin')
        getal2 = Value(4.3, num_sys='Latin')
        print(f'''dat is dan: {{localize({calc}, num_sys=get_num_sys(getal1))}}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    def test_float_sum_with_var(self):
        code = textwrap.dedent("""\
            getal1 is 5
            getal2 is 4.3
            print 'dat is dan: ' getal1 + getal2""")
        calc = self.sum_transpiled('getal1', 'getal2')
        expected = textwrap.dedent(f"""\
            getal1 = Value(5, num_sys='Latin')
            getal2 = Value(4.3, num_sys='Latin')
            print(f'''dat is dan: {{localize({calc}, num_sys=get_num_sys(getal1))}}''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=17)

    @parameterized.expand(['-', '*', '/'])
    def test_int_calc_with_var(self, op):
        code = textwrap.dedent(f"""\
        a is 1
        b is 2
        c is a {op} b""")
        expected = textwrap.dedent(f"""\
        a = Value(1, num_sys='Latin')
        b = Value(2, num_sys='Latin')
        c = Value({self.number_transpiled('a')} {op} {self.number_transpiled('b')}, num_sys=get_num_sys(a))""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_int_sum_with_var(self):
        code = textwrap.dedent(f"""\
        a is 1
        b is 2
        c is a + b""")
        expected = textwrap.dedent(f"""\
        a = Value(1, num_sys='Latin')
        b = Value(2, num_sys='Latin')
        c = Value({self.sum_transpiled('a', 'b')}, num_sys=get_num_sys(a))""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_concat_calc_with_var(self):
        code = textwrap.dedent("""\
        getal1 is '5'
        getal2 is '6'
        getal3 is '7'
        print 'dat is dan: ' getal1 + getal2 + getal3""")
        calc = self.sum_transpiled(self.sum_transpiled('getal1', 'getal2'), 'getal3')
        expected = textwrap.dedent(f"""\
        getal1 = Value('5')
        getal2 = Value('6')
        getal3 = Value('7')
        print(f'''dat is dan: {{localize({calc}, num_sys=get_num_sys(getal1))}}''')""")

        check_output = (lambda x: HedyTester.run_code(x) == 'dat is dan: 567')

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=check_output
        )

    def test_int_calc_chained_vars(self):
        code = textwrap.dedent("""\
        a is 5
        b is a + 1
        print a + b""")

        expected = textwrap.dedent(f"""\
        a = Value(5, num_sys='Latin')
        b = Value({self.sum_transpiled('a', 1)}, num_sys=get_num_sys(a))
        print(f'''{{localize({self.sum_transpiled('a', 'b')}, num_sys=get_num_sys(a))}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            extra_check_function=lambda x: self.run_code(x) == "11"
        )

    def test_calc_string_and_int_gives_type_error(self):
        code = textwrap.dedent("""\
        x is 'test1'
        y is x + 1""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidTypeCombinationException)

    def test_concat_quoted_string_and_int_gives_type_error(self):
        code = """y is 'test1' + 1"""

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1,
            exception=hedy.exceptions.InvalidTypeCombinationException)

    @parameterized.expand(['-', '*', '/'])
    def test_calc_with_single_quoted_strings_gives_type_error(self, operation):
        code = textwrap.dedent(f"""\
        a is 1 {operation} 'Test'""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    @parameterized.expand(['-', '*', '/'])
    def test_calc_with_double_quoted_strings_gives_type_error(self, operation):
        code = textwrap.dedent(f"""\
        a is 1 {operation} "Test\"""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_concat_promotes_ask_input_to_string(self):
        code = textwrap.dedent("""\
            answer is ask 'Yes or No?'
            print 'The answer is ' + answer""")

        expected = self.dedent(
            self.input_transpiled('answer', 'Yes or No?'),
            f"""print(f'''{{localize({self.sum_transpiled("'The answer is '", 'answer')})}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=14,
            expected=expected
        )

    def test_concat_promotes_ask_input_to_int(self):
        code = textwrap.dedent("""\
            answer is ask '1 or 2?'
            print 5 + answer""")

        expected = self.dedent(
            self.input_transpiled('answer', '1 or 2?'),
            f"""print(f'''{{localize({self.sum_transpiled('5', 'answer')}, num_sys='Latin')}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=14,
            expected=expected
        )

    def test_concat_promotes_ask_input_to_float(self):
        code = textwrap.dedent("""\
            answer is ask '1 or 2?'
            print 0.5 + answer""")

        expected = self.dedent(
            self.input_transpiled('answer', '1 or 2?'),
            f"""print(f'''{{localize({self.sum_transpiled('0.5', 'answer')}, num_sys='Latin')}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=14,
            expected=expected
        )

    # def test_access_variable_before_definition(self):
    #   code = textwrap.dedent("""\
    #           a is b
    #           b is 3
    #           print a""")
    #
    #   expected = textwrap.dedent("""\
    #           a = bx
    #           b = 3
    #           print(f'{a}')""")
    #
    #   self.multi_level_tester(
    #     code=code,
    #     max_level=17,
    #     expected=expected,
    #     extra_check_function=self.is_not_turtle(),
    #     test_name=self.name()
    #   )

    #
    # combined tests
    #

    def test_list_with_spaces_nested_for_loop(self):
        code = textwrap.dedent("""\
        actions is 'clap your hands', 'stomp your feet', 'shout Hurray'
        for action in actions
            for i in range 1 to 2
                print 'if youre happy and you know it'
                print action
            print 'if youre happy and you know it and you really want to show it'
            print 'if youre happy and you know it'
            print action""")
        expected = self.dedent(
            f"""\
            actions = Value([Value('clap your hands'), Value('stomp your feet'), Value('shout Hurray')])
            for action in actions.data:""",
            (self.for_loop('i', 1, 2), '  '),
            (f"""\
              print(f'''if youre happy and you know it''')
              print(f'''{{action}}''')
              time.sleep(0.1)
            print(f'''if youre happy and you know it and you really want to show it''')
            print(f'''if youre happy and you know it''')
            print(f'''{{action}}''')
            time.sleep(0.1)""", '  '))

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    #
    # if pressed tests
    #

    def test_if_pressed_with_list_and_for(self):
        code = textwrap.dedent("""\
        lijstje is 'kip', 'haan', 'kuiken'
        if x is pressed
            for dier in lijstje
                print 'dier'
        else
            print 'onbekend dier'""")

        expected = self.dedent("""\
        lijstje = Value([Value('kip'), Value('haan'), Value('kuiken')])
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        def if_pressed_x_():
            for dier in lijstje.data:
              print(f'''dier''')
              time.sleep(0.1)
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_else_():
            print(f'''onbekend dier''')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=15)

    #
    # function tests
    #
    def test_simple_function(self):
        code = textwrap.dedent("""\
        define simple_function_1 with parameter
            print "simple_function_1 - 1"
            m = "simple_function_1 - 2"
            print m
        define simple_function_2 with param
            print "simple_function_2 - 1"
            print param
        define simple_function_3 with param_a, param_b, param_c
            if param_a = "A"
                print "simple_function_3 - 1"
                print param_b
            else
                print "simple_function_3 - 2"
                if param_a = "B"
                    print "simple_function_3 - 2A"
                    print param_b
                else
                    print "simple_function_3 - 2B"
                    print param_c
        a = "test1"
        call simple_function_3 with "A", a, 1.0
        call simple_function_3 with "B", a, 1.0
        call simple_function_3 with "C", a, 1.0""")

        expected = textwrap.dedent("""\
        def simple_function_1(parameter):
          print(f'''simple_function_1 - 1''')
          m = Value('simple_function_1 - 2')
          print(f'''{m}''')
        def simple_function_2(param):
          print(f'''simple_function_2 - 1''')
          print(f'''{param}''')
        def simple_function_3(param_a, param_b, param_c):
          if param_a.data == 'A':
            print(f'''simple_function_3 - 1''')
            print(f'''{param_b}''')
          else:
            print(f'''simple_function_3 - 2''')
            if param_a.data == 'B':
              print(f'''simple_function_3 - 2A''')
              print(f'''{param_b}''')
            else:
              print(f'''simple_function_3 - 2B''')
              print(f'''{param_c}''')
        a = Value('test1')
        simple_function_3(Value('A'), a, Value(1.0, num_sys='Latin'))
        simple_function_3(Value('B'), a, Value(1.0, num_sys='Latin'))
        simple_function_3(Value('C'), a, Value(1.0, num_sys='Latin'))""")

        output = textwrap.dedent("""\
        simple_function_3 - 1
        test1
        simple_function_3 - 2
        simple_function_3 - 2A
        test1
        simple_function_3 - 2
        simple_function_3 - 2B
        1.0""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output=output,
            unused_allowed=True,
            max_level=16
        )

    def test_function_use(self):
        code = textwrap.dedent("""\
        define func with n1, n2
            return n1 + n2

        print call func with 1, 2""")

        expected = self.dedent(
            "def func(n1, n2):",
            (self.return_transpiled(
                f"{{localize({self.sum_transpiled('n1', 'n2')}, num_sys=get_num_sys(n1))}}"), '  '),
            "print(f'''{func(Value(1, num_sys='Latin'), Value(2, num_sys='Latin'))}''')")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            expected=expected
        )

    def test_function_with_arabic_var(self):
        code = textwrap.dedent(f"""\
             define test_function_1
                 i = ١
                 return "Test function " i
             print call test_function_1""")

        expected = self.dedent(
            "def test_function_1():",
            ("i = Value(1, num_sys='Arabic')", "  "),
            (self.return_transpiled('Test function {i}'), "  "),
            "print(f'''{test_function_1()}''')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output="Test function ١",
            max_level=16
        )

    def test_undefined_function_without_params(self):
        code = textwrap.dedent("""\
        call func""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            exception=hedy.exceptions.UndefinedFunctionException
        )

    def test_undefined_function_with_params(self):
        code = textwrap.dedent("""\
        print call func with 1, 2""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            exception=hedy.exceptions.UndefinedFunctionException
        )

    def test_function_use_builtin_name(self):
        code = textwrap.dedent("""\
            define sum with n1, n2
                return n1 + n2
    
            print call sum with 1, 2""")

        return_arg = f"{{localize({self.sum_transpiled('n1', 'n2')}, num_sys=get_num_sys(n1))}}"
        expected = self.dedent(
            "def sum(n1, n2):",
            (self.return_transpiled(return_arg), '  '),
            "print(f'''{sum(Value(1, num_sys='Latin'), Value(2, num_sys='Latin'))}''')")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            expected=expected
        )

    def test_function_returns_number(self):
        code = textwrap.dedent("""\
        define func with n1, n2
            return n1 + n2

        a = call func with 1, 2
        print a + 3""")

        return_arg = f"{{localize({self.sum_transpiled('n1', 'n2')}, num_sys=get_num_sys(n1))}}"
        expected = self.dedent(
            "def func(n1, n2):",
            (self.return_transpiled(return_arg), '  '),
            "a = func(Value(1, num_sys='Latin'), Value(2, num_sys='Latin'))",
            f"print(f'''{{localize({self.sum_transpiled('a', '3')}, num_sys=get_num_sys(a))}}''')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='6',
            max_level=16,
        )

    def test_function_returns_arabic_number(self):
        code = textwrap.dedent("""\
        define func with n1, n2
            return n1 + n2

        a = call func with ٣, ١
        print a + 3""")

        return_arg = f"{{localize({self.sum_transpiled('n1', 'n2')}, num_sys=get_num_sys(n1))}}"
        expected = self.dedent(
            "def func(n1, n2):",
            (self.return_transpiled(return_arg), '  '),
            "a = func(Value(3, num_sys='Arabic'), Value(1, num_sys='Arabic'))",
            f"print(f'''{{localize({self.sum_transpiled('a', '3')}, num_sys=get_num_sys(a))}}''')")

        self.multi_level_tester(
            code=code,
            max_level=16,
            output='٧',
            expected=expected,
        )

    def test_too_many_parameters(self):
        code = textwrap.dedent("""\
        define func with n1, n2
            return n1 + n2

        print call func with 1, 2, 3""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            exception=hedy.exceptions.WrongNumberofArguments
        )

    def test_too_few_parameters(self):
        code = textwrap.dedent("""\
        define func with n1, n2
            return n1 + n2

        print call func with 1""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            exception=hedy.exceptions.WrongNumberofArguments
        )

    def test_unused_function_use_builtin_name(self):
        code = textwrap.dedent("""\
        define sum with n1, n2
            return n1 + n2

        print 'hola!'""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            skip_faulty=False,
            exception=hedy.exceptions.UnusedVariableException
        )

    def test_addition(self):
        code = textwrap.dedent("""\
        a = 5
        b = 7
        print a + b""")

        expected = textwrap.dedent(f"""\
        a = Value(5, num_sys='Latin')
        b = Value(7, num_sys='Latin')
        print(f'''{{localize({self.sum_transpiled('a', 'b')}, num_sys=get_num_sys(a))}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            skip_faulty=False,
            expected=expected
        )

    def test_source_map(self):
        self.maxDiff = None
        code = textwrap.dedent("""\
            price = 0.0
            food = ask 'What would you like to order?'
            drink = ask 'What would you like to drink?'
            if food is 'hamburger'
                price = price + 6.50
            if food is 'pizza'
                price = price + 5.75
            if drink is 'water'
                price = price + 1.20
            if drink is 'soda'
                price = price + 2.35
            print 'That will be ' price ' dollar, please'""")

        expected_code = self.dedent(
            "price = Value(0.0, num_sys='Latin')",
            self.input_transpiled('food', 'What would you like to order?'),
            self.input_transpiled('drink', 'What would you like to drink?'),
            '''\
            if food.data == 'hamburger':
              price = Value(sum_with_error(price, 6.5, """Runtime Values Error"""), num_sys=get_num_sys(price))
            if food.data == 'pizza':
              price = Value(sum_with_error(price, 5.75, """Runtime Values Error"""), num_sys=get_num_sys(price))
            if drink.data == 'water':
              price = Value(sum_with_error(price, 1.2, """Runtime Values Error"""), num_sys=get_num_sys(price))
            if drink.data == 'soda':
              price = Value(sum_with_error(price, 2.35, """Runtime Values Error"""), num_sys=get_num_sys(price))
            print(f\'\'\'That will be {price} dollar, please\'\'\')''')

        expected_source_map = {
            '1/1-1/6': '1/1-1/6',
            '1/1-1/12': '1/1-1/36',
            '2/1-2/5': '2/1-2/5',
            '2/1-2/43': '2/1-11/33',
            '3/1-3/6': '12/1-12/6',
            '3/1-3/44': '12/1-21/35',
            '4/4-4/8': '3/20-3/24',
            '4/4-4/23': '22/4-22/28',
            '5/5-5/10': '25/1-25/6',
            '5/13-5/18': '27/1-27/6',
            '5/5-5/25': '23/1-23/98',
            '4/1-5/34': '22/1-23/100',
            '6/4-6/8': '5/3-5/7',
            '6/4-6/19': '24/4-24/24',
            '7/5-7/10': '29/1-29/6',
            '7/13-7/18': '1/1-1/6',
            '7/5-7/25': '25/1-25/99',
            '6/1-7/34': '24/1-25/101',
            '8/4-8/9': '12/42-12/47',
            '8/4-8/20': '26/4-26/25',
            '9/5-9/10': '23/1-23/6',
            '9/13-9/18': '25/1-25/6',
            '9/5-9/25': '27/1-27/98',
            '8/1-9/34': '26/1-27/100',
            '10/4-10/9': '13/20-13/25',
            '10/4-10/19': '28/4-28/24',
            '11/5-11/10': '27/1-27/6',
            '11/13-11/18': '29/1-29/6',
            '11/5-11/25': '29/1-29/99',
            '10/1-11/34': '28/1-29/101',
            '12/23-12/28': '27/93-27/98',
            '12/1-12/46': '30/1-30/50',
            '1/1-12/47': '1/1-30/50'
        }

        self.single_level_tester(code, expected=expected_code)
        self.source_map_tester(code=code, expected_source_map=expected_source_map)

    def test_nested_functions(self):
        code = textwrap.dedent("""\
        define simple_function
            define nested_function
                print 1
        call simple_function""")

        expected = textwrap.dedent("""\
        pass
        simple_function()""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 3, 34), hedy.exceptions.NestedFunctionException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            skipped_mappings=skipped_mappings,
            max_level=16
        )

    #
    # play tests / music tests
    #
    def test_play_var(self):
        code = textwrap.dedent("""\
            n = 'C4' #
            play n""")

        expected = self.dedent(
            "n = Value('C4')",
            self.play_transpiled('n.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=17)

    def test_play_arabic_number_var(self):
        code = textwrap.dedent("""\
            n is ١١
            play n""")

        expected = self.dedent(
            "n = Value(11, num_sys='Arabic')",
            self.play_transpiled('n.data'))

        self.multi_level_tester(code=code, expected=expected)

    def test_play_keyword_var(self):
        code = textwrap.dedent("""\
            sum is 'C4'
            play sum""")

        expected = self.dedent(
            "_sum = Value('C4')",
            self.play_transpiled('_sum.data'))

        self.multi_level_tester(code=code, expected=expected)

    def test_play_list_access_random(self):
        code = textwrap.dedent("""\
        notes = 'C4', 'E4', 'D4', 'F4', 'G4'
        play notes at random""")

        expected = self.dedent(
            f"notes = Value([Value('C4'), Value('E4'), Value('D4'), Value('F4'), Value('G4')])",
            self.play_transpiled("random.choice(notes.data).data"))

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=15
        )

    def test_play_list_access_random_repeat(self):
        code = textwrap.dedent("""\
        notes = 1, 2, 3

        repeat 10 times
            play notes at random""")

        expected = self.dedent(
            f"""\
            notes = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(3, num_sys='Latin')])
            for __i in range({self.int_transpiled(10)}):""",
            (self.play_transpiled('random.choice(notes.data).data'), '  '),
            ("time.sleep(0.1)", '  '))

        self.multi_level_tester(code=code, expected=expected, max_level=15)

    @parameterized.expand(['-', '*', '/'])
    def test_play_calculation(self, op):
        code = textwrap.dedent(f"""\
            note is 34
            play note {op} 1""")
        expected = self.dedent(
            "note = Value(34, num_sys='Latin')",
            self.play_transpiled(f"{self.number_transpiled('note')} {op} {self.number_transpiled(1)}"))

        self.multi_level_tester(code=code, expected=expected)

    @parameterized.expand(['-', '*', '/', '+'])
    def test_play_arabic_calc(self, op):
        code = f"play ٣١ {op} ١"
        expected = self.play_transpiled(f'31 {op} 1')

        self.multi_level_tester(code=code, expected=expected)

    def test_play_calc_with_var(self):
        code = textwrap.dedent(f"""\
            note is 34
            play note + 1""")
        expected = self.dedent(
            "note = Value(34, num_sys='Latin')",
            self.play_transpiled(self.sum_transpiled('note', 1)))

        self.multi_level_tester(code=code, expected=expected)

    def test_play_input(self):
        code = textwrap.dedent("""\
            note = ask 'Give me a note'
            play note""")

        expected = self.dedent(
            self.input_transpiled('note', 'Give me a note'),
            self.play_transpiled('note.data'))

        self.multi_level_tester(code=code, expected=expected, max_level=14)

    def test_play_unquoted_text_gives_error(self):
        code = "play undef"
        self.multi_level_tester(code=code, exception=exceptions.UnquotedAssignTextException)

    #
    # color tests
    #
    @parameterized.expand(hedy.english_colors)
    def test_all_colors(self, color):
        code = f'color {color}'
        expected = self.color_transpiled(f'"{color}"')

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_color_with_var(self):
        code = textwrap.dedent("""\
            foo is 'white'
            color foo""")
        expected = self.dedent(
            "foo = Value('white')",
            self.color_transpiled('{foo}')
        )

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_color_with_keyword_var(self):
        code = textwrap.dedent("""\
            sum is 'white'
            color sum""")
        expected = self.dedent(
            "_sum = Value('white')",
            self.color_transpiled('{_sum}')
        )

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=18
        )
