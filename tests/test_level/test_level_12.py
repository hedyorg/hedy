import textwrap

import hedy
from tests.Tester import HedyTester


class TestsLevel11(HedyTester):
    level = 11
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
    # for loop tests
    #
    def test_for_loop(self):
        code = textwrap.dedent("""\
            for i in range 1 to 10
                a is i + 1""")
        expected = self.dedent(
            self.for_loop('i', 1, 10),
            (f"a = Value({self.number_transpiled('i')} + {self.number_transpiled(1)}, num_sys=get_num_sys(i))", '  '),
            ("time.sleep(0.1)", '  '))

        self.single_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            expected_commands=['for', 'is', 'addition'])

    def test_for_loop_arabic(self):
        code = textwrap.dedent("""\
            for i in range ١ to ١١
                a is i + 1""")
        expected = self.dedent(
            self.for_loop('i', 1, 11, num_sys="'Arabic'"),
            (f"a = Value({self.number_transpiled('i')} + {self.number_transpiled(1)}, num_sys=get_num_sys(i))", '  '),
            ("time.sleep(0.1)", '  '))

        self.single_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            expected_commands=['for', 'is', 'addition'])

    def test_for_loop_with_int_vars(self):
        code = textwrap.dedent("""\
            begin = 1
            end = 10
            for i in range begin to end
                print i""")

        expected = self.dedent(
            "begin = Value('1', num_sys='Latin')",
            "end = Value('10', num_sys='Latin')",
            self.for_loop('i', 'begin', 'end', 'get_num_sys(begin)'),
            ("print(f'{i}')", '  '),
            ("time.sleep(0.1)", '  '))

        self.single_level_tester(code=code, expected=expected)

    def test_for_loop_with_keyword_vars(self):
        code = textwrap.dedent("""\
            sum = 1
            dir = 10
            for i in range sum to dir
                print i""")

        expected = self.dedent(
            "_sum = Value('1', num_sys='Latin')",
            "_dir = Value('10', num_sys='Latin')",
            self.for_loop('i', '_sum', '_dir', 'get_num_sys(_sum)'),
            ("print(f'{i}')", '  '),
            ("time.sleep(0.1)", '  '))

        self.single_level_tester(code=code, expected=expected)

    def test_for_loop_with_list_var_gives_type_error(self):
        code = textwrap.dedent("""\
        begin = 1, 2
        end = 3, 4
        for i in range begin to end
            print i""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_for_loop_with_string_var_gives_type_error(self):
        code = textwrap.dedent("""\
        begin = 'one'
        end = 'ten'
        for i in range begin to end
            print i""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_for_loop_without_in_var_gives_error(self):
        code = "for no_in range 1 to 5"

        self.multi_level_tester(
            code=code,
            max_level=16,
            exception=hedy.exceptions.MissingAdditionalCommand)

    def test_for_loop_without_to_var_gives_error(self):
        code = "for no_to in range 1 5"

        self.multi_level_tester(
            code=code,
            max_level=16,
            exception=hedy.exceptions.MissingAdditionalCommand)

    def test_for_loop_without_command_var_gives_error(self):
        code = "for no_command in range 1 to 5"

        self.multi_level_tester(
            code=code,
            max_level=16,
            exception=hedy.exceptions.IncompleteCommandException)

    def test_for_loop_multiline_body(self):
        code = textwrap.dedent("""\
            a is 2
            b is 3
            for a in range 2 to 4
                a is a + 2
                b is b + 2""")

        expected = self.dedent(
            "a = Value('2', num_sys='Latin')",
            "b = Value('3', num_sys='Latin')",
            self.for_loop('a', 2, 4),
            (f'a = Value({self.number_transpiled("a")} + {self.number_transpiled(2)}, num_sys=get_num_sys(a))', '  '),
            (f'b = Value({self.number_transpiled("b")} + {self.number_transpiled(2)}, num_sys=get_num_sys(b))', '  '),
            ('time.sleep(0.1)', '  '))

        self.single_level_tester(code=code, expected=expected)

    def test_for_loop_followed_by_print(self):
        code = textwrap.dedent("""\
            for i in range 1 to 10
                print i
            print 'wie niet weg is is gezien'""")

        expected = self.dedent(
            self.for_loop('i', 1, 10),
            ("print(f'{i}')", '  '),
            ("time.sleep(0.1)", '  '),
            "print(f'wie niet weg is is gezien')")

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

        self.single_level_tester(
            code=code,
            expected=expected,
            expected_commands=['for', 'print', 'print'],
            output=output)

    def test_for_loop_hindi_variable(self):
        code = textwrap.dedent("""\
            for काउंटर in range 1 to 5
                print काउंटर""")

        expected = self.dedent(
            self.for_loop('काउंटर', 1, 5),
            ("print(f'{काउंटर}')", '  '),
            ("time.sleep(0.1)", '  '))

        self.single_level_tester(
            code=code,
            expected=expected,
            expected_commands=['for', 'print'])

    def test_for_loop_arabic_range(self):
        code = textwrap.dedent("""\
            for دورة in range ١ to ٥
                print دورة""")

        expected = self.dedent(
            self.for_loop('دورة', 1, 5, "'Arabic'"),
            ("print(f'{دورة}')", '  '),
            ("time.sleep(0.1)", '  '))

        output = textwrap.dedent("""\
            ١
            ٢
            ٣
            ٤
            ٥""")

        self.single_level_tester(
            code=code,
            output=output,
            translate=False,
            expected=expected,
            expected_commands=['for', 'print'])

    def test_for_loop_reversed_range(self):
        code = textwrap.dedent("""\
            for i in range 10 to 1
                print i
            print 'wie niet weg is is gezien'""")

        expected = self.dedent(
            self.for_loop('i', 10, 1),
            ("print(f'{i}')", '  '),
            ("time.sleep(0.1)", '  '),
            "print(f'wie niet weg is is gezien')")

        self.single_level_tester(
            code=code,
            expected=expected,
            expected_commands=['for', 'print', 'print'])

    def test_for_loop_with_if_else_body(self):
        code = textwrap.dedent("""\
            for i in range 0 to 10
                antwoord is ask 'Wat is 5*5'
                if antwoord is 24
                    print 'Dat is fout!'
                else
                    print 'Dat is goed!'
                if antwoord is 25
                    i is 10""")

        expected = self.dedent(
            self.for_loop('i', 0, 10),
            (self.input_transpiled('antwoord', 'Wat is 5*5'), '  '),
            ("if localize(antwoord.data) == localize('24'):", '  '),
            ("print(f'Dat is fout!')", '    '),
            ("else:", '  '),
            ("print(f'Dat is goed!')", '    '),
            ("if localize(antwoord.data) == localize('25'):", '  '),
            ("i = Value('10', num_sys='Latin')", '    '),
            ("time.sleep(0.1)", '  '))

        self.single_level_tester(code=code, expected=expected)

    # issue 363
    def test_for_loop_if_followed_by_print(self):
        code = textwrap.dedent("""\
            for i in range 0 to 10
                antwoord is ask 'Wat is 5*5'
                if antwoord is 24
                    print 'fout'
            print 'klaar met for loop'""")

        expected = self.dedent(
            self.for_loop('i', 0, 10),
            (self.input_transpiled('antwoord', 'Wat is 5*5'), '  '),
            ("if localize(antwoord.data) == localize('24'):", '  '),
            ("print(f'fout')", '    '),
            ("time.sleep(0.1)", '  '),
            "print(f'klaar met for loop')")

        self.single_level_tester(code=code, expected=expected)

    # issue 599
    def test_for_loop_if(self):
        code = textwrap.dedent("""\
            for i in range 0 to 10
                if i is 2
                    print '2'""")

        expected = self.dedent(
            self.for_loop('i', 0, 10),
            ("if localize(i.data) == localize('2'):", '  '),
            ("print(f'2')", '    '),
            ("time.sleep(0.1)", '  '))

        self.single_level_tester(code=code, expected=expected)

    # issue 1209
    def test_for_loop_unindented_nested_for_loop(self):
        code = textwrap.dedent("""\
        for x in range 1 to 10
         for y in range 1 to 10
         print 'x*y'""")

        self.multi_level_tester(code, exception=hedy.exceptions.NoIndentationException)

    # issue 1209
    def test_for_loop_dedented_nested_loop(self):
        code = textwrap.dedent("""\
        for x in range 1 to 10
         for y in range 1 to 10
        print 'x*y'""")

        self.multi_level_tester(code, exception=hedy.exceptions.NoIndentationException)

    # issue 1209
    def test_nested_for_loop_with_zigzag_body(self):
        code = textwrap.dedent("""\
        for x in range 1 to 10
          for y in range 1 to 10
             print 'this number is'
            print x*y""")

        self.multi_level_tester(code, exception=hedy.exceptions.IndentationException)

    #
    # pressed with for loop tests
    #

    def test_if_pressed_works_in_for_loop(self):
        code = textwrap.dedent("""\
            for i in range 1 to 10
                if p is pressed
                    print 'press'
                else
                    print 'no!'""")

        expected = self.dedent(
            "global_scope_ = dict()",
            self.for_loop('i', 1, 10),
            ("""\
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['p'] = 'if_pressed_p_'
            def if_pressed_p_():
              print(f'press')
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_else_():
              print(f'no!')
            extensions.if_pressed(if_pressed_mapping)
            time.sleep(0.1)""", '  '))

        self.single_level_tester(
            code=code,
            expected=expected,
        )

    def test_if_pressed_in_for_loop(self):
        code = textwrap.dedent("""\
        for i in range 1 to 10
            print i
            if i is pressed
                r = 'Yes'
            else
                r = 'No'
            print r""")

        expected = self.dedent(
            "global_scope_ = dict()",
            self.for_loop('i', 1, 10),
            ("""\
            print(f'{global_scope_.get("i") or i}')
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping[(global_scope_.get("i") or i).data] = 'if_pressed_i_'
            def if_pressed_i_():
              global_scope_["r"] = Value('\\'Yes\\'')
            if_pressed_mapping['else'] = 'if_pressed_else_'
            def if_pressed_else_():
              global_scope_["r"] = Value('\\'No\\'')
            extensions.if_pressed(if_pressed_mapping)
            print(f'{global_scope_.get("r") or r}')
            time.sleep(0.1)""", '  '))

        self.single_level_tester(code=code, expected=expected)
