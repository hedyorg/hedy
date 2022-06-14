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
        n = '1'
        m = '2'
        if str(n) == str('1'):
          if str(m) == str('2'):
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
        n = '1'
        m = '2'
        if str(n) == str('1'):
          if str(m) == str('2'):
            print(f'great!')
        else:
          if str(m) == str('3'):
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
        n = '1'
        m = '2'
        if str(n) == str('1'):
          if str(m) == str('2'):
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
         n = '1'
         m = '2'
         if str(n) == str('1'):
           if str(m) == str('2'):
             print(f'great!')
           else:
             print(f'nice!')
         else:
           if str(m) == str('3'):
             print(f'awesome!')
           else:
             print(f'amazing!')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # repeat nesting
    #
    def test_repeat_nested_in_repeat(self):
        code = textwrap.dedent("""\
        repeat 2 times
            repeat 3 times
                print 'hello'""")

        expected = textwrap.dedent("""\
           for i in range(int('2')):
             for i in range(int('3')):
               print(f'hello')
               time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # if and repeat nesting
    #
    def test_if_nested_in_repeat(self):
        code = textwrap.dedent("""\
        prijs is 0
        repeat 7 times
            ingredient is ask 'wat wil je kopen?'
            if ingredient is appel
                prijs is prijs + 1
        print 'Dat is in totaal ' prijs ' euro.'""")

        expected = textwrap.dedent("""\
        prijs = '0'
        for i in range(int('7')):
          ingredient = input(f'wat wil je kopen?')
          if str(ingredient) == str('appel'):
            prijs = int(prijs) + int(1)
          time.sleep(0.1)
        print(f'Dat is in totaal {prijs} euro.')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_nested_in_repeat_with_comment(self):
        code = textwrap.dedent("""\
        prijs is 0
        repeat 7 times # comment
            ingredient is ask 'wat wil je kopen?'
            if ingredient is appel # another comment
                prijs is prijs + 1
        print 'Dat is in totaal ' prijs ' euro.'""")

        expected = textwrap.dedent("""\
        prijs = '0'
        for i in range(int('7')):
          ingredient = input(f'wat wil je kopen?')
          if str(ingredient) == str('appel'):
            prijs = int(prijs) + int(1)
          time.sleep(0.1)
        print(f'Dat is in totaal {prijs} euro.')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_repeat_nested_in_if(self):
        code = textwrap.dedent("""\
        kleur is groen
        if kleur is groen
            repeat 3 times
                print 'mooi'""")

        expected = textwrap.dedent("""\
        kleur = 'groen'
        if str(kleur) == str('groen'):
          for i in range(int('3')):
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

        expected = textwrap.dedent("""\
        for i in range(int('5')):
          if str('antwoord2') == str('10'):
            print(f'Goedzo')
          else:
            print(f'lalala')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)
