import textwrap

from parameterized import parameterized

import exceptions
import hedy
from tests.Tester import HedyTester


class TestsLevel14(HedyTester):
    level = 14

    #
    # if tests / equality tests / equals tests
    #
    @parameterized.expand(HedyTester.equality_comparison_commands)
    def test_equality_with_var_and_string(self, comparison):
        code = textwrap.dedent(f"""\
            name is ask 'What is your name?'
            if name {comparison} 'Hedy'
                print 'meh'""")
        expected = self.dedent(
            self.input_transpiled('name', 'What is your name?'),
            f"""\
            if name.data == 'Hedy':
              print(f'''meh''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
        )

    @parameterized.expand(HedyTester.equality_comparison_commands)
    def test_equality_with_var_and_int(self, comparison):
        code = textwrap.dedent(f"""\
            age is ask 'How old are you?'
            if age {comparison} 18
                print 'congrats'""")
        expected = self.dedent(
            self.input_transpiled('age', 'How old are you?'),
            f"""\
            if age.data == 18:
              print(f'''congrats''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
        )

    @parameterized.expand(HedyTester.equality_comparison_commands)
    def test_equality_with_list_access_and_float(self, comparison):
        code = textwrap.dedent(f"""\
            numbers = 1.5, 2.9, 42.0
            if numbers at 1 {comparison} 1.5
                print 'meh'""")
        expected = self.dedent(
            "numbers = V([V(1.5, num_sys='Latin'), V(2.9, num_sys='Latin'), V(42.0, num_sys='Latin')])",
            self.list_access_transpiled('numbers.data[int(1)-1]'),
            f"""\
            if numbers.data[int(1)-1].data == 1.5:
              print(f'''meh''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=15)

    def test_equality_var_arabic(self):
        code = textwrap.dedent("""\
            nummer1 is ٢
            nummer2 is 2
            if nummer1 == nummer2
                print 'jahoor!'
            else
                print 'neejoh!'""")

        expected = textwrap.dedent("""\
            nummer1 = V(2, num_sys='Arabic')
            nummer2 = V(2, num_sys='Latin')
            if nummer1.data == nummer2.data:
              print(f'''jahoor!''')
            else:
              print(f'''neejoh!''')""")

        self.multi_level_tester(
            max_level=16,
            code=code,
            expected=expected,
            output='jahoor!')

    def test_equality_int_arabic(self):
        code = textwrap.dedent("""\
            if ٢ == 2
                print 'yes'
            else
                print 'no'""")

        expected = textwrap.dedent("""\
            if 2 == 2:
              print(f'''yes''')
            else:
              print(f'''no''')""")

        self.multi_level_tester(
            max_level=16,
            code=code,
            expected=expected,
            output='yes')

    @parameterized.expand(HedyTester.equality_comparison_commands)
    def test_equality_of_lists(self, comparison):
        code = textwrap.dedent(f"""\
            a = 1, 2
            b = 1, 2
            if a {comparison} b
                sleep""")

        expected = textwrap.dedent(f"""\
            a = V([V(1, num_sys='Latin'), V(2, num_sys='Latin')])
            b = V([V(1, num_sys='Latin'), V(2, num_sys='Latin')])
            if a.data == b.data:
              time.sleep(1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=15)

    #
    # inequality tests / not equals tests
    #
    def test_inequality_with_string(self):
        code = textwrap.dedent(f"""\
            name is ask 'What is your name?'
            if name != 'Hedy'
                print 'meh'""")
        expected = self.dedent(
            self.input_transpiled('name', 'What is your name?'),
            f"""\
            if name.data!='Hedy':
              print(f'''meh''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
        )

    def test_inequality_hindi(self):
        code = textwrap.dedent(f"""\
            उम्र is ask 'आप कितने साल के हैं?'
            if उम्र > 12
                print 'आप मुझसे छोटे हैं!'
            else
                print 'आप मुझसे बड़े हैं!'""")
        expected = self.dedent(
            self.input_transpiled('उम्र', 'आप कितने साल के हैं?'),
            f"""\
            if उम्र.data>12:
              print(f'''आप मुझसे छोटे हैं!''')
            else:
              print(f'''आप मुझसे बड़े हैं!''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    def test_inequality_int_arabic(self):
        code = textwrap.dedent("""\
            if ٢ != 2
                print 'yes'
            else
                print 'no'""")

        expected = textwrap.dedent("""\
            if 2!=2:
              print(f'''yes''')
            else:
              print(f'''no''')""")

        self.multi_level_tester(
            max_level=16,
            code=code,
            expected=expected,
            output='no')

    def test_inequality_promotes_int_to_float(self):
        code = textwrap.dedent(f"""\
            a is 1
            b is 1.2
            if a != b
                b is 1""")

        expected = textwrap.dedent(f"""\
            a = V(1, num_sys='Latin')
            b = V(1.2, num_sys='Latin')
            if a.data!=b.data:
              b = V(1, num_sys='Latin')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    @parameterized.expand([
        ('"text"', "V('text')"),
        ("'text'", "V('text')"),
        ('1', "V(1, num_sys='Latin')"),
        ('1.3', "V(1.3, num_sys='Latin')"),
        ('1, 2', "V([V(1, num_sys='Latin'), V(2, num_sys='Latin')])")])
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
              b = V(1, num_sys='Latin')""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            expected=expected
        )

    def test_inequality_list_access(self):
        code = textwrap.dedent("""\
            a = 1, 2
            b = 1, 2
            if a at 2 != b at 2
                sleep""")

        expected = self.dedent(
            "a = V([V(1, num_sys='Latin'), V(2, num_sys='Latin')])",
            "b = V([V(1, num_sys='Latin'), V(2, num_sys='Latin')])",
            self.list_access_transpiled('a.data[int(2)-1]'),
            self.list_access_transpiled('b.data[int(2)-1]'),
            f"""\
            if a.data[int(2)-1].data!=b.data[int(2)-1].data:
              time.sleep(1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=15)

    def test_inequality_of_lists(self):
        code = textwrap.dedent("""\
            a = 1, 2
            b = 1, 2
            if a != b
                sleep""")

        expected = textwrap.dedent("""\
            a = V([V(1, num_sys='Latin'), V(2, num_sys='Latin')])
            b = V([V(1, num_sys='Latin'), V(2, num_sys='Latin')])
            if a.data!=b.data:
              time.sleep(1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=15)

    @parameterized.expand([
        ('"text"', '1'),      # double-quoted text and number
        ("'text'", '1'),      # single-quoted text and number
        ('1, 2', '1'),        # list and number
        ('1, 2', "'text'"),   # list and single-quoted text
        ('1, 2', '"text"')])  # list and double-quoted text
    def test_inequality_with_diff_types_gives_error(self, left, right):
        code = textwrap.dedent(f"""\
        a is {left}
        b is {right}
        if a != b
            b is 1""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=exceptions.InvalidTypeCombinationException
        )

    #
    # comparison tests
    #
    @parameterized.expand(['8', '10', '100', '699', '700'])
    def test_greater_than_with_int_and_float(self, a):
        b = 7.0
        code = textwrap.dedent(f"""\
        var = {a}
        if var > {b}
          print 'Above {b}'
        else
          print 'Below'""")
        expected = textwrap.dedent(f"""\
        var = V({a}, num_sys='Latin')
        if var.data>{b}:
          print(f'''Above {b}''')
        else:
          print(f'''Below''')""")
        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
            output=f'Above {b}',
        )

    @parameterized.expand(str(float(i)) for i in range(2, 16))
    def test_not_greater_than_with_int_and_float(self, a):
        b = 15
        code = textwrap.dedent(f"""\
        var = {a}
        if var > {b}
          print 'Above {b}'
        else
          print 'Below'""")
        expected = textwrap.dedent(f"""\
        var = V({a}, num_sys='Latin')
        if var.data>{b}:
          print(f'''Above {b}''')
        else:
          print(f'''Below''')""")
        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=16,
            output='Below',
        )

    @parameterized.expand(HedyTester.comparison_commands)
    def test_comparison_with_int(self, comparison):
        code = textwrap.dedent(f"""\
            leeftijd is ask 'Hoe oud ben jij?'
            if leeftijd {comparison} 12
                print 'Dan ben je jonger dan ik!'""")
        expected = self.dedent(
            self.input_transpiled('leeftijd', 'Hoe oud ben jij?'),
            f"""\
            if leeftijd.data{comparison}12:
              print(f'''Dan ben je jonger dan ik!''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected)

    @parameterized.expand(HedyTester.comparison_commands)
    def test_comparison_with_list_access(self, comparison):
        code = textwrap.dedent(f"""\
            numbers = 1, 2, 10
            if numbers at 2 {comparison} numbers at 1
                print 'great!'""")
        expected = self.dedent(
            "numbers = V([V(1, num_sys='Latin'), V(2, num_sys='Latin'), V(10, num_sys='Latin')])",
            self.list_access_transpiled('numbers.data[int(2)-1]'),
            self.list_access_transpiled('numbers.data[int(1)-1]'),
            f"""\
            if numbers.data[int(2)-1].data{comparison}numbers.data[int(1)-1].data:
              print(f'''great!''')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=15)

    @parameterized.expand(HedyTester.comparison_commands)
    def test_comparison_else(self, comparison):
        code = textwrap.dedent(f"""\
            leeftijd is ask 'Hoe oud ben jij?'
            if leeftijd {comparison} 12
                print 'Dan ben je jonger dan ik!'
            else
                print 'Dan ben je ouder dan ik!'""")
        expected = self.dedent(
            self.input_transpiled('leeftijd', 'Hoe oud ben jij?'),
            f"""\
            if leeftijd.data{comparison}12:
              print(f'''Dan ben je jonger dan ik!''')
            else:
              print(f'''Dan ben je ouder dan ik!''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected
        )

    @parameterized.expand(HedyTester.comparison_commands)
    def tests_comparison_no_spaces(self, comparison):
        code = textwrap.dedent(f"""\
            leeftijd is ask 'Hoe oud ben jij?'
            if leeftijd{comparison}12
                print 'Dan ben je jonger dan ik!'""")
        expected = self.dedent(
            self.input_transpiled('leeftijd', 'Hoe oud ben jij?'),
            f"""\
            if leeftijd.data{comparison}12:
              print(f'''Dan ben je jonger dan ik!''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected
        )

    @parameterized.expand(HedyTester.number_comparison_commands)
    def test_comparison_with_string_gives_type_error(self, comparison):
        code = textwrap.dedent(f"""\
        a is 'text'
        if a {comparison} 12
            b is 1""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand(HedyTester.number_comparison_commands)
    def test_comparison_with_list_gives_type_error(self, comparison):
        code = textwrap.dedent(f"""\
        a is 1, 2, 3
        if a {comparison} 12
            b is 1""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand(HedyTester.comparison_commands)
    def test_comparison_with_boolean(self, comparison):
        code = textwrap.dedent(f"""\
            leeftijd is ask 'Hoe oud ben jij?'
            if leeftijd {comparison} 12 or leeftijd {comparison} 15
                print 'Dan ben je jonger dan ik!'
            if leeftijd {comparison} 12 and leeftijd {comparison} 15
                print 'Some other string!'""")

        expected = self.dedent(
            self.input_transpiled('leeftijd', 'Hoe oud ben jij?'),
            f"""\
            if leeftijd.data{comparison}12 or leeftijd.data{comparison}15:
              print(f'''Dan ben je jonger dan ik!''')
            if leeftijd.data{comparison}12 and leeftijd.data{comparison}15:
              print(f'''Some other string!''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
        )

    @parameterized.expand(HedyTester.comparison_commands)
    def test_comparison_with_trailing_spaces(self, comparison):
        value = '1  '
        code = textwrap.dedent(f"""\
            var is 5
            if var   {comparison} {value} 
                print 'seems correct'""")

        expected = textwrap.dedent(f"""\
            var = V(5, num_sys='Latin')
            if var.data{comparison}1:
              print(f'''seems correct''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    @parameterized.expand(HedyTester.comparison_commands)
    def test_comparison_with_leading_spaces(self, comparison):
        code = textwrap.dedent(f"""\
            var is 5
            if   var {comparison}  1 
                print 'seems correct'""")

        expected = textwrap.dedent(f"""\
            var = V(5, num_sys='Latin')
            if var.data{comparison}1:
              print(f'''seems correct''')""")

        self.multi_level_tester(code=code, expected=expected, max_level=16)

    @parameterized.expand(HedyTester.number_comparison_commands)
    def test_comparison_with_undef_var_gives_error(self, comparison):
        code = textwrap.dedent(f"""\
            if n {comparison} 12
                sleep""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            exception=exceptions.UndefinedVarException,
        )

    def test_comparison_with_missing_indent_else(self):
        code = textwrap.dedent(f"""\
        age = ask 'How old are you?'
        if age < 13
            print 'You are younger than me!'
        else
        print 'You are older than me!'""")

        self.multi_level_tester(code=code, exception=exceptions.NoIndentationException)

    #
    # function tests
    #
    def test_actually_simple_function(self):
        code = textwrap.dedent(f"""\
            define test_function_1
                int = ١
                return "Test function " int
            print call test_function_1""")

        expected = self.dedent(
            "def test_function_1():",
            ("_int = V(1, num_sys='Arabic')", "  "),
            (self.return_transpiled('Test function {_int.text()}'), "  "),
            "print(f'''{test_function_1().text()}''')")

        output = "Test function ١"
        self.multi_level_tester(
            code=code,
            expected=expected,
            output=output,
            max_level=16
        )

    def test_simple_function(self):
        code = textwrap.dedent(f"""\
        define test_function_1
            int = 1
            return "Test function " int
        define test_function_2 with int
            return "Test function " int
        define test_function_3 with input
            if input != 5
                print "NE5"
            if input < 5
                print "LT5"
            if input <= 5
                print "LTE5"
            if input > 5
                print "GT5"
            if input >= 5
                print "GTE5"
            if input = 5
                print "E5"
        print call test_function_1
        print call test_function_2 with 2
        m = 3
        print call test_function_2 with m
        print call test_function_2 with 4.0
        print call test_function_2 with "5"
        print call test_function_2 with 1.5 * 4
        print ""
        call test_function_3 with 4
        print ""
        call test_function_3 with 5
        print ""
        call test_function_3 with 6""")

        expected = self.dedent(
            """\
            def test_function_1():
              _int = V(1, num_sys='Latin')""",
            (self.return_transpiled("Test function {_int.text()}"), '  '),
            "def test_function_2(_int):",
            (self.return_transpiled("Test function {_int.text()}"), '  '),
            f"""\
            def test_function_3(_input):
              if _input.data!=5:
                print(f'''NE5''')
              if _input.data<5:
                print(f'''LT5''')
              if _input.data<=5:
                print(f'''LTE5''')
              if _input.data>5:
                print(f'''GT5''')
              if _input.data>=5:
                print(f'''GTE5''')
              if _input.data == 5:
                print(f'''E5''')
            print(f'''{{test_function_1().text()}}''')
            print(f'''{{test_function_2(V(2, num_sys='Latin')).text()}}''')
            m = V(3, num_sys='Latin')
            print(f'''{{test_function_2(m).text()}}''')
            print(f'''{{test_function_2(V(4.0, num_sys='Latin')).text()}}''')
            print(f'''{{test_function_2(V('5')).text()}}''')
            print(f'''{{test_function_2(V(1.5 * 4, num_sys='Latin')).text()}}''')
            print(f'''''')
            test_function_3(V(4, num_sys='Latin'))
            print(f'''''')
            test_function_3(V(5, num_sys='Latin'))
            print(f'''''')
            test_function_3(V(6, num_sys='Latin'))""")

        output = textwrap.dedent("""\
        Test function 1
        Test function 2
        Test function 3
        Test function 4.0
        Test function 5
        Test function 6.0

        NE5
        LT5
        LTE5

        LTE5
        GTE5
        E5

        NE5
        GT5
        GTE5""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output=output,
            max_level=16
        )

    def test_source_map(self):
        code = textwrap.dedent("""\
        age = ask 'How old are you?'
        if age < 13
            print 'You are younger than me!'
        else
            print 'You are older than me!'""")

        excepted_code = self.dedent(
            self.input_transpiled('age', 'How old are you?'),
            """\
            if age.data<13:
              print(f'''You are younger than me!''')
            else:
              print(f'''You are older than me!''')""")

        expected_source_map = {
            '1/1-1/4': '1/1-1/4',
            '1/1-1/29': '1/1-10/30',
            '2/4-2/7': '2/23-2/26',
            '2/4-2/12': '11/4-11/15',
            '3/5-3/37': '12/1-12/39',
            '2/1-3/46': '11/1-12/41',
            '5/5-5/35': '14/1-14/37',
            '3/46-5/44': '14/-256-2/8',
            '2/1-5/44': '11/1-14/39',
            '1/1-5/45': '1/1-14/39'
        }

        self.single_level_tester(code, expected=excepted_code)
        self.source_map_tester(code=code, expected_source_map=expected_source_map)
