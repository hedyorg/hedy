import textwrap

import hedy
from tests.Tester import HedyTester


class TestsLevel10(HedyTester):
    level = 10
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
    # for list tests
    #
    def test_for_list(self):
        code = textwrap.dedent("""\
        dieren is hond, kat, papegaai
        for dier in dieren
            print dier""")

        expected = textwrap.dedent("""\
        dieren = Value([Value('hond'), Value('kat'), Value('papegaai')])
        for dier in dieren.data:
          print(f'{dier}')
          time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=['is', 'for', 'print'],
            max_level=11
        )

    def test_blanks(self):
        code = textwrap.dedent("""\
        players = Ann, John, Jesse
        choices = 1, 2, 3, 4, 5, 6
        _
            print player ' throws ' choices at random
            sleep
        """)

        self.multi_level_tester(
            max_level=16,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.CodePlaceholdersPresentException
        )

    def test_for_list_hindi(self):
        code = textwrap.dedent("""\
        क is hond, kat, papegaai
        for काउंटर in क
            print काउंटर""")

        expected = textwrap.dedent("""\
        क = Value([Value('hond'), Value('kat'), Value('papegaai')])
        for काउंटर in क.data:
          print(f'{काउंटर}')
          time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=['is', 'for', 'print'],
            max_level=11
        )

    def test_for_list_diff_num_sys(self):
        code = textwrap.dedent("""\
        digits is 1, 𑁨, ३, ૪, ੫
        for d in digits
            print d""")

        list_transpiled = ("Value([""Value('1', num_sys='Latin'), Value('2', num_sys='Brahmi'), "
                           "Value('3', num_sys='Devanagari'), Value('4', num_sys='Gujarati'), "
                           "Value('5', num_sys='Gurmukhi')])")
        expected = textwrap.dedent(f"""\
        digits = {list_transpiled}
        for d in digits.data:
          print(f'{{d}}')
          time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output="1\n𑁨\n३\n૪\n੫",
            max_level=11
        )

    def test_for_list_multiline_body(self):
        code = textwrap.dedent("""\
        familie is baby, mommy, daddy, grandpa, grandma
        for shark in familie
            print shark ' shark tudutudutudu'
            print shark ' shark tudutudutudu'
            print shark ' shark tudutudutudu'
            print shark ' shark'""")

        expected = textwrap.dedent("""\
        familie = Value([Value('baby'), Value('mommy'), Value('daddy'), Value('grandpa'), Value('grandma')])
        for shark in familie.data:
          print(f'{shark} shark tudutudutudu')
          print(f'{shark} shark tudutudutudu')
          print(f'{shark} shark tudutudutudu')
          print(f'{shark} shark')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_for_list_with_string_gives_type_error(self):
        code = textwrap.dedent("""\
        dieren is 'text'
        for dier in dieren
            print dier""")

        self.multi_level_tester(
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            max_level=16,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    def test_for_list_with_int_gives_type_error(self):
        code = textwrap.dedent("""\
        dieren is 5
        for dier in dieren
            print dier""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    #
    # if pressed tests
    #

    def test_if_pressed_with_list_and_for(self):
        code = textwrap.dedent("""\
        lijstje is kip, haan, kuiken
        if x is pressed
            for dier in lijstje
                print dier
        else
            print 'onbekend dier'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        global_scope_["lijstje"] = Value([Value('kip'), Value('haan'), Value('kuiken')])
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        def if_pressed_x_():
          for dier in (global_scope_.get("lijstje") or lijstje).data:
            print(f'{global_scope_.get("dier") or dier}')
            time.sleep(0.1)
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_else_():
          print(f'onbekend dier')
        extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11)

    def test_if_pressed_in_for_list(self):
        code = textwrap.dedent("""\
        buttons is a, s, d
        for button in buttons
            if button is pressed
                print 'correct! ' button
            else
                print 'not a match'""")

        expected = self.dedent("""\
        global_scope_ = dict()
        global_scope_["buttons"] = Value([Value('a'), Value('s'), Value('d')])
        for button in (global_scope_.get("buttons") or buttons).data:
          if_pressed_mapping = {"else": "if_pressed_default_else"}
          if_pressed_mapping[(global_scope_.get("button") or button).data] = 'if_pressed_button_'
          def if_pressed_button_():
            print(f'correct! {global_scope_.get("button") or button}')
          if_pressed_mapping['else'] = 'if_pressed_else_'
          def if_pressed_else_():
            print(f'not a match')
          extensions.if_pressed(if_pressed_mapping)
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)
