import textwrap

from parameterized import parameterized

import exceptions
import hedy
from hedy_sourcemap import SourceRange
from tests.Tester import HedyTester, SkippedMapping


class TestsLevel17(HedyTester):
    level = 17
    maxDiff = None

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
        ("'text'", '1'),        # text and number
        ('[1, 2]', '1'),        # list and number
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
            if_pressed_mapping = {{"else": "if_pressed_default_else"}}
            global if_pressed_x_
            if_pressed_mapping['x'] = 'if_pressed_x_'
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
         if_pressed_mapping = {"else": "if_pressed_default_else"}
         global if_pressed_a_
         if_pressed_mapping['a'] = 'if_pressed_a_'
         def if_pressed_a_():
           print(f'''A''')
         global if_pressed_b_
         if_pressed_mapping['b'] = 'if_pressed_b_'
         def if_pressed_b_():
           print(f'''B''')
         global if_pressed_else_
         if_pressed_mapping['else'] = 'if_pressed_else_'
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
