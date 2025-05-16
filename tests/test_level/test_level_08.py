import textwrap

from parameterized import parameterized

import hedy
from hedy_sourcemap import SourceRange
from tests.Tester import HedyTester, SkippedMapping


class TestsLevel7(HedyTester):
    level = 7
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
    # repeat tests
    #
    def test_repeat_turtle(self):
        code = "repeat 3 times forward 100"

        expected = self.dedent(
            f"for __i in range({self.int_transpiled(3)}):",
            (self.forward_transpiled(100), '  '))

        self.single_level_tester(code=code, expected=expected, extra_check_function=self.is_turtle())

    def test_repeat_print(self):
        code = "repeat 5 times print 'me wants a cookie!'"

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_transpiled(5)}):
          print(f'me wants a cookie!')
          time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.single_level_tester(code=code, expected=expected, output=output)

    def test_repeat_arabic_number_print(self):
        code = "repeat ٣ times print 'hooray!'"

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_transpiled(3)}):
          print(f'hooray!')
          time.sleep(0.1)""")

        output = textwrap.dedent("""\
            hooray!
            hooray!
            hooray!""")

        self.single_level_tester(code=code, expected=expected, output=output)

    def test_repeat_print_variable(self):
        code = textwrap.dedent("""\
            n is 5
            repeat n times print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
            n = Value('5', num_sys='Latin')
            for __i in range({self.int_transpiled('n.data')}):
              print(f'me wants a cookie!')
              time.sleep(0.1)""")

        output = textwrap.dedent("""\
            me wants a cookie!
            me wants a cookie!
            me wants a cookie!
            me wants a cookie!
            me wants a cookie!""")

        self.single_level_tester(code=code, expected=expected, output=output)

    def test_repeat_arabic_var_print(self):
        code = textwrap.dedent("""\
            n is ٣
            repeat n times print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
            n = Value('3', num_sys='Arabic')
            for __i in range({self.int_transpiled('n.data')}):
              print(f'me wants a cookie!')
              time.sleep(0.1)""")

        output = textwrap.dedent("""\
            me wants a cookie!
            me wants a cookie!
            me wants a cookie!""")

        self.single_level_tester(code=code, expected=expected, output=output)

    def test_repeat_keyword_variable(self):
        code = textwrap.dedent("""\
            sum is 2
            repeat sum times print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
            _sum = Value('2', num_sys='Latin')
            for __i in range({self.int_transpiled('_sum.data')}):
              print(f'me wants a cookie!')
              time.sleep(0.1)""")

        output = textwrap.dedent("""\
            me wants a cookie!
            me wants a cookie!""")

        self.single_level_tester(code=code, expected=expected, output=output)

    def test_repeat_print_undefined_variable_gives_error(self):
        code = "repeat n times print 'me wants a cookie!'"

        self.single_level_tester(code=code, exception=hedy.exceptions.UndefinedVarException)

    def test_missing_body(self):
        code = textwrap.dedent("""\
        prind skipping
        repeat 5 times""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 15), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(2, 1, 2, 15), hedy.exceptions.MissingInnerCommandException)
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            max_level=8
        )

    def test_repeat_with_string_variable_gives_type_error(self):
        code = textwrap.dedent("""\
        n is 'test'
        repeat n times print 'n'""")

        self.single_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_repeat_with_list_variable_gives_type_error(self):
        code = textwrap.dedent("""\
        n is 1, 2, 3
        repeat n times print 'n'""")

        self.single_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_repeat_with_missing_print_gives_error(self):
        code = textwrap.dedent("""\
        repeat 3 print 'x'""")

        self.single_level_tester(
            code=code,
            exception=hedy.exceptions.IncompleteRepeatException
        )

    def test_repeat_with_missing_times_gives_error_skip(self):
        code = textwrap.dedent("""\
        x is 3
        repeat 3 print 'x'""")

        expected = textwrap.dedent("""\
        x = Value('3', num_sys='Latin')
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(2, 1, 2, 19), hedy.exceptions.IncompleteRepeatException),
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
        )

    def test_repeat_with_missing_print_gives_lonely_text_exc(self):
        code = textwrap.dedent("""\
        prind skipping
        repeat 3 times 'n'""")

        expected = textwrap.dedent(f"""\
        pass
        for __i in range({self.int_transpiled(3)}):
          pass
          time.sleep(0.1)""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 15), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(2, 16, 2, 19), hedy.exceptions.LonelyTextException)
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
        )

    def test_repeat_with_missing_times_gives_error(self):
        code = textwrap.dedent("""\
        prind skipping
        repeat 3 print 'n'""")

        expected = textwrap.dedent("""\
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 15), hedy.exceptions.InvalidCommandException),
            SkippedMapping(SourceRange(2, 1, 2, 19), hedy.exceptions.IncompleteRepeatException),
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
        )

    def test_repeat_with_missing_times_gives_error_2(self):
        code = "repeat 5"

        self.multi_level_tester(
            code=code,
            max_level=8,
            exception=hedy.exceptions.IncompleteRepeatException
        )

    def test_repeat_ask(self):
        code = textwrap.dedent("""\
            n is ask 'How many times?'
            repeat n times print 'n'""")

        expected = self.dedent(
            self.input_transpiled('n', 'How many times?'),
            f"""\
            for __i in range({self.int_transpiled('n.data')}):
              print(f'n')
              time.sleep(0.1)""")

        self.single_level_tester(code=code, expected=expected)

    @parameterized.expand(['5', '𑁫', '५', '૫', '੫', '৫', '೫', '୫', '൫', '௫',
                           '౫', '၅', '༥', '᠕', '៥', '๕', '໕', '꧕', '٥', '۵'])
    def test_repeat_with_all_numerals(self, number):
        code = textwrap.dedent(f"repeat {number} times print 'me wants a cookie!'")

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_transpiled(int(number))}):
          print(f'me wants a cookie!')
          time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.single_level_tester(code=code, expected=expected, output=output)

    def test_repeat_over_9_times(self):
        code = textwrap.dedent("""\
        repeat 10 times print 'me wants a cookie!'""")

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_transpiled(10)}):
          print(f'me wants a cookie!')
          time.sleep(0.1)""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!""")

        self.single_level_tester(
            code=code,
            expected=expected,
            expected_commands=['repeat', 'print'],
            output=output)

    def test_repeat_with_variable_name_collision(self):
        code = textwrap.dedent("""\
        i is hallo!
        repeat 5 times print 'me wants a cookie!'
        print i""")

        expected = textwrap.dedent(f"""\
        i = Value('hallo!')
        for __i in range({self.int_transpiled(5)}):
          print(f'me wants a cookie!')
          time.sleep(0.1)
        print(f'{{i}}')""")

        output = textwrap.dedent("""\
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        me wants a cookie!
        hallo!""")

        self.single_level_tester(
            code=code,
            expected=expected,
            expected_commands=['is', 'repeat', 'print', 'print'],
            output=output)

    def test_repeat_if(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy repeat 3 times print 'Hallo Hedy!'""")

        expected = textwrap.dedent(f"""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          for __i in range({self.int_transpiled('3')}):
            print(f'Hallo Hedy!')
            time.sleep(0.1)""")

        self.single_level_tester(
            code=code,
            expected=expected)

    def test_if_pressed_repeat(self):
        code = "if x is pressed repeat 5 times print 'doe het 5 keer!' else print 'iets anders'"

        expected = self.dedent(f"""\
        global_scope_ = dict()
        if_pressed_mapping = {{"else": "if_pressed_default_else"}}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          for __i in range(int_with_error('5', {self.value_exception_transpiled()})):
            print(f'doe het 5 keer!')
            time.sleep(0.1)
        def if_pressed_else_():
          print(f'iets anders')
        extensions.if_pressed(if_pressed_mapping)""")

        self.single_level_tester(
            code=code,
            expected=expected)

    def test_if_pressed_multiple(self):
        code = textwrap.dedent("""\
            if x is pressed print 'doe het 1 keer!' else print 'iets anders'
            if y is pressed print 'doe het 1 keer!' else print 'iets anders'
            if z is pressed print 'doe het 1 keer!' else print 'iets anders'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          print(f'doe het 1 keer!')
        def if_pressed_else_():
          print(f'iets anders')
        extensions.if_pressed(if_pressed_mapping)
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['y'] = 'if_pressed_y_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_y_():
          print(f'doe het 1 keer!')
        def if_pressed_else_():
          print(f'iets anders')
        extensions.if_pressed(if_pressed_mapping)
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['z'] = 'if_pressed_z_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_z_():
          print(f'doe het 1 keer!')
        def if_pressed_else_():
          print(f'iets anders')
        extensions.if_pressed(if_pressed_mapping)""")

        self.single_level_tester(
            code=code,
            expected=expected,
            skip_faulty=False,
            translate=False)

    def test_repeat_if_pressed_multiple(self):
        code = textwrap.dedent("""\
            repeat 3 times if x is pressed forward 15 else forward -15
            repeat 3 times if y is pressed forward 15 else forward -15
            repeat 3 times if z is pressed forward 15 else forward -15""")

        expected = self.dedent(
            f"""\
            global_scope_ = dict()
            for __i in range({self.int_transpiled(3)}):
              if_pressed_mapping = {{"else": "if_pressed_default_else"}}
              if_pressed_mapping['x'] = 'if_pressed_x_'
              if_pressed_mapping['else'] = 'if_pressed_else_'
              def if_pressed_x_():""",
            (self.forward_transpiled('15'), '    '),
            ("def if_pressed_else_():", '  '),
            (self.forward_transpiled('-15'), '    '),
            f"""\
              extensions.if_pressed(if_pressed_mapping)
              time.sleep(0.1)
            for __i in range({self.int_transpiled(3)}):
              if_pressed_mapping = {{"else": "if_pressed_default_else"}}
              if_pressed_mapping['y'] = 'if_pressed_y_'
              if_pressed_mapping['else'] = 'if_pressed_else_'
              def if_pressed_y_():""",
            (self.forward_transpiled('15'), '    '),
            ("def if_pressed_else_():", '  '),
            (self.forward_transpiled('-15'), '    '),
            f"""\
              extensions.if_pressed(if_pressed_mapping)
              time.sleep(0.1)
            for __i in range({self.int_transpiled(3)}):
              if_pressed_mapping = {{"else": "if_pressed_default_else"}}
              if_pressed_mapping['z'] = 'if_pressed_z_'
              if_pressed_mapping['else'] = 'if_pressed_else_'
              def if_pressed_z_():""",
            (self.forward_transpiled('15'), '    '),
            ("def if_pressed_else_():", '  '),
            (self.forward_transpiled('-15'), '    '),
            (f"""\
              extensions.if_pressed(if_pressed_mapping)
              time.sleep(0.1)""", '  '))

        self.single_level_tester(
            code=code,
            expected=expected,
            translate=False)

    def test_repeat_if_multiple(self):
        code = textwrap.dedent("""\
            aan is ja
            repeat 3 times if aan is ja print 'Hedy is leuk!'
            repeat 3 times if aan is ja print 'Hedy is leuk!'""")

        expected = self.dedent(f"""\
            aan = Value('ja')
            for __i in range({self.int_transpiled(3)}):
              if localize(aan.data) == localize('ja'):
                print(f'Hedy is leuk!')
              else:
                x__x__x__x = Value('5', num_sys='Latin')
              time.sleep(0.1)
            for __i in range({self.int_transpiled(3)}):
              if localize(aan.data) == localize('ja'):
                print(f'Hedy is leuk!')
              time.sleep(0.1)""")

        output = textwrap.dedent("""\
            Hedy is leuk!
            Hedy is leuk!
            Hedy is leuk!
            Hedy is leuk!
            Hedy is leuk!
            Hedy is leuk!""")

        self.single_level_tester(
            code=code,
            expected=expected,
            output=output)

    def test_source_map(self):
        code = textwrap.dedent("""\
        print 'The prince kept calling for help'
        repeat 5 times print 'Help!'
        print 'Why is nobody helping me?'""")

        expected_code = textwrap.dedent(f"""\
        print(f'The prince kept calling for help')
        for __i in range({self.int_transpiled(5)}):
          print(f'Help!')
          time.sleep(0.1)
        print(f'Why is nobody helping me?')""")

        expected_source_map = {
            '1/1-1/41': '1/1-1/43',
            '2/16-2/29': '3/3-3/18',
            '2/1-2/29': '2/1-4/18',
            '3/1-3/34': '5/1-5/36',
            '1/1-3/35': '1/1-5/36'
        }

        self.single_level_tester(code, expected=expected_code)
        self.source_map_tester(code=code, expected_source_map=expected_source_map)

# music tests

    def test_play_repeat(self):
        code = textwrap.dedent("""\
            repeat 3 times play C4""")

        expected = self.dedent(
            f"for __i in range({self.int_transpiled(3)}):",
            (self.play_transpiled("'C4'"), '  '),
            ("time.sleep(0.1)", '  '))

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=7
        )

    def test_play_repeat_random(self):
        code = textwrap.dedent("""\
            notes is C4, E4, D4, F4, G4
            repeat 3 times play notes at random""")

        expected = self.dedent(
            "notes = Value([Value('C4'), Value('E4'), Value('D4'), Value('F4'), Value('G4')])",
            f"for __i in range({self.int_transpiled(3)}):",
            (self.play_transpiled('random.choice(notes.data).data'), '  '),
            ("time.sleep(0.1)", '  '))

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=7
        )
