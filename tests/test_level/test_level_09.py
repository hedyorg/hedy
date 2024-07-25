import hedy
import textwrap

from tests.Tester import HedyTester


class TestsLevel9(HedyTester):
    level = 9
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
    # if nesting
    #
    def test_if_nested_in_if(self):
        code = textwrap.dedent("""\
        n is 1
        m is 2
        if n is 1
            if m is 2
                print 'great!'""")

        expected = textwrap.dedent("""\
        n = Value('1', num_sys='Latin')
        m = Value('2', num_sys='Latin')
        if localize(n.data) == localize('1'):
          if localize(m.data) == localize('2'):
            print(f'great!')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_ifs_nested_in_if_else(self):
        code = textwrap.dedent("""\
        n is 1
        m is 2
        if n is 1
            if m is 2
                print 'great!'
        else
            if m is 3
                print 'awesome'""")

        expected = textwrap.dedent("""\
        n = Value('1', num_sys='Latin')
        m = Value('2', num_sys='Latin')
        if localize(n.data) == localize('1'):
          if localize(m.data) == localize('2'):
            print(f'great!')
        else:
          if localize(m.data) == localize('3'):
            print(f'awesome')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_else_nested_in_if(self):
        code = textwrap.dedent("""\
        n is 1
        m is 2
        if n is 1
            if m is 2
                print 'great!'
            else
                print 'awesome'""")

        expected = textwrap.dedent("""\
        n = Value('1', num_sys='Latin')
        m = Value('2', num_sys='Latin')
        if localize(n.data) == localize('1'):
          if localize(m.data) == localize('2'):
            print(f'great!')
          else:
            print(f'awesome')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_else_statements_nested_in_if_else(self):
        code = textwrap.dedent("""\
         n is 1
         m is 2
         if n is 1
             if m is 2
                 print 'great!'
             else
                 print 'nice!'
         else
             if m is 3
                 print 'awesome!'
             else
                 print 'amazing!'""")

        expected = textwrap.dedent("""\
         n = Value('1', num_sys='Latin')
         m = Value('2', num_sys='Latin')
         if localize(n.data) == localize('1'):
           if localize(m.data) == localize('2'):
             print(f'great!')
           else:
             print(f'nice!')
         else:
           if localize(m.data) == localize('3'):
             print(f'awesome!')
           else:
             print(f'amazing!')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_else_no_indentation(self):
        code = textwrap.dedent("""\
        antwoord is ask Hoeveel is 10 keer tien?
        if antwoord is 100
        print 'goed zo'
        else
        print 'bah slecht'""")

        # gives the right exception for all levels even though it misses brackets
        # because the indent check happens before parsing
        self.multi_level_tester(code=code,
                                exception=hedy.exceptions.NoIndentationException)

    def test_if_no_indent_after_pressed_and_else_gives_error(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'no indent!'
        else
        print 'no indent again!'""")

        # gives the right exception for all levels even though it misses brackets
        # because the indent check happens before parsing
        self.multi_level_tester(code=code, exception=hedy.exceptions.NoIndentationException)

    def test_if_no_indentation(self):
        code = textwrap.dedent("""\
        antwoord is ask Hoeveel is 10 keer tien?
        if antwoord is 100
        print 'goed zo'""")

        # gives the right exception for all levels even though it misses brackets
        # because the indent check happens before parsing
        self.multi_level_tester(code=code, exception=hedy.exceptions.NoIndentationException)

    #
    # repeat nesting
    #
    def test_repeat_nested_in_repeat(self):
        code = textwrap.dedent("""\
        repeat 2 times
            repeat 3 times
                print 'hello'""")

        expected = textwrap.dedent(f"""\
           for __i in range({self.int_transpiled(2)}):
             for __i in range({self.int_transpiled(3)}):
               print(f'hello')
               time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

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

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_nested_multi_commands(self):
        code = textwrap.dedent("""\
            repeat 3 times
                print 3
                repeat 5 times
                    print 5
                print 1""")

        expected = textwrap.dedent(f"""\
            for __i in range({self.int_transpiled(3)}):
              print(f'3')
              for __i in range({self.int_transpiled(5)}):
                print(f'5')
                time.sleep(0.1)
              print(f'1')
              time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11,
            skip_faulty=False
        )

    def test_repeat_no_indentation(self):
        code = textwrap.dedent("""\
          repeat 3 times
          print 'hooray!'""")

        self.multi_level_tester(code=code, exception=hedy.exceptions.NoIndentationException)

    def test_repeat_repair_too_few_indents(self):
        code = textwrap.dedent("""\
        repeat 5 times
             print('repair')
          print('me')""")

        fixed_code = textwrap.dedent("""\
        repeat 5 times
             print('repair')
             print('me')""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.NoIndentationException,
            extra_check_function=(lambda x: x.exception.fixed_code == fixed_code)
        )

    def test_repeat_repair_too_many_indents(self):
        code = textwrap.dedent("""\
        repeat 5 times
          print('repair')
             print('me')""")
        fixed_code = textwrap.dedent("""\
        repeat 5 times
          print('repair')
          print('me')""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.IndentationException,
            extra_check_function=(lambda x: x.exception.fixed_code == fixed_code)
        )

    #
    # if and repeat nesting
    #
    def test_if_nested_in_repeat(self):
        code = textwrap.dedent("""\
            p is 0
            repeat 7 times
                ingredient is ask 'wat wil je kopen?'
                if ingredient is appel
                    p is p + 1
            print 'Dat is in totaal ' p ' euro.'""")

        expected = self.dedent(
            "p = Value('0', num_sys='Latin')",
            f"for __i in range({self.int_transpiled(7)}):",
            (self.input_transpiled('ingredient', 'wat wil je kopen?'), '  '),
            f"""\
              if localize(ingredient.data) == localize('appel'):
                p = Value({self.number_transpiled('p')} + {self.number_transpiled(1)}, num_sys=get_num_sys(p))
              time.sleep(0.1)
            print(f'Dat is in totaal {{p}} euro.')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_nested_in_repeat_with_comment(self):
        code = textwrap.dedent("""\
            p is 0
            repeat 7 times # comment
                ingredient is ask 'wat wil je kopen?'
                if ingredient is appel # another comment
                    p is p + 1
            print 'Dat is in totaal ' p ' euro.'""")

        expected = self.dedent(
            "p = Value('0', num_sys='Latin')",
            f"for __i in range({self.int_transpiled(7)}):",
            (self.input_transpiled('ingredient', f'wat wil je kopen?'), '  '),
            f"""\
              if localize(ingredient.data) == localize('appel'):
                p = Value({self.number_transpiled('p')} + {self.number_transpiled(1)}, num_sys=get_num_sys(p))
              time.sleep(0.1)
            print(f'Dat is in totaal {{p}} euro.')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_nested_in_if(self):
        code = textwrap.dedent("""\
        kleur is groen
        if kleur is groen
            repeat 3 times
                print 'mooi'""")

        expected = textwrap.dedent(f"""\
        kleur = Value('groen')
        if localize(kleur.data) == localize('groen'):
          for __i in range({self.int_transpiled(3)}):
            print(f'mooi')
            time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11,
            expected_commands=['is', 'if', 'repeat', 'print'])

    def test_if_else_nested_in_repeat(self):
        code = textwrap.dedent("""\
        repeat 5 times
            if antwoord2 is 10
                print 'Goedzo'
            else
                print 'lalala'""")

        expected = textwrap.dedent(f"""\
        for __i in range({self.int_transpiled(5)}):
          if localize('antwoord2') == localize('10'):
            print(f'Goedzo')
          else:
            print(f'lalala')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_without_body_nested_in_if_gives_error(self):
        code = textwrap.dedent("""\
        if 1 is 1
          repeat 5 times""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.MissingInnerCommandException,
            max_level=16,
            skip_faulty=False)

    def test_repeat_without_body_nested_in_else_gives_error(self):
        code = textwrap.dedent("""\
        if 1 is 1
          print 'test'
        else
          repeat 5 times""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.MissingInnerCommandException,
            max_level=16,
            skip_faulty=False)

    #
    # if pressed repeat tests
    #

    def test_if_pressed_repeat(self):
        code = textwrap.dedent("""\
        if x is pressed
            repeat 5 times
                print 'doe het 5 keer!'
        else
            print '1 keertje'""")

        expected = self.dedent(f"""\
         if_pressed_mapping = {{"else": "if_pressed_default_else"}}
         if_pressed_mapping['x'] = 'if_pressed_x_'
         def if_pressed_x_():
             for __i in range({self.int_transpiled(5)}):
               print(f'doe het 5 keer!')
               time.sleep(0.1)
         if_pressed_mapping['else'] = 'if_pressed_else_'
         def if_pressed_else_():
             print(f'1 keertje')
         extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # button tests
    #

    def test_if_button_is_pressed_print_in_repeat(self):
        code = textwrap.dedent("""\
        button1 is button
        repeat 3 times
          if button1 is pressed
            print 'wow'
          else
            print 'nah'""")

        expected = self.dedent(f"""\
         create_button('button1')
         for __i in range({self.int_transpiled(3)}):
           if_pressed_mapping = {{"else": "if_pressed_default_else"}}
           if_pressed_mapping['button1'] = 'if_pressed_button1_'
           def if_pressed_button1_():
               print(f'wow')
           if_pressed_mapping['else'] = 'if_pressed_else_'
           def if_pressed_else_():
               print(f'nah')
           extensions.if_pressed(if_pressed_mapping)
           time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_unexpected_indent(self):
        code = textwrap.dedent("""\
         print('repair')
            print('me')""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.IndentationException
        )

    def test_source_map(self):
        code = textwrap.dedent("""\
        repeat 3 times
            food = ask 'What do you want?'
            if food is pizza
                print 'nice!'
            else
                print 'pizza is better'""")

        expected_source_map = {
            '2/5-2/9': '2/1-2/5',
            '2/5-2/35': '2/1-4/29',
            '3/8-3/21': '9/-270-1/40',
            '4/9-4/22': '6/1-6/16',
            '3/5-4/31': '5/1-6/16',
            '6/9-6/32': '8/1-8/26',
            '4/31-6/41': '9/-270-1/34',
            '3/5-6/41': '5/1-8/22',
            '1/1-6/50': '1/1-9/18',
            '1/1-6/51': '1/1-9/18'
        }

        self.source_map_tester(
            code=code,
            expected_source_map=expected_source_map,
        )
