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
        if convert_numerals('Latin', n) == convert_numerals('Latin', '1'):
          if convert_numerals('Latin', m) == convert_numerals('Latin', '2'):
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
        if convert_numerals('Latin', n) == convert_numerals('Latin', '1'):
          if convert_numerals('Latin', m) == convert_numerals('Latin', '2'):
            print(f'great!')
        else:
          if convert_numerals('Latin', m) == convert_numerals('Latin', '3'):
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
        if convert_numerals('Latin', n) == convert_numerals('Latin', '1'):
          if convert_numerals('Latin', m) == convert_numerals('Latin', '2'):
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
         if convert_numerals('Latin', n) == convert_numerals('Latin', '1'):
           if convert_numerals('Latin', m) == convert_numerals('Latin', '2'):
             print(f'great!')
           else:
             print(f'nice!')
         else:
           if convert_numerals('Latin', m) == convert_numerals('Latin', '3'):
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
          if convert_numerals('Latin', ingredient) == convert_numerals('Latin', 'appel'):
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
          if convert_numerals('Latin', ingredient) == convert_numerals('Latin', 'appel'):
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
        if convert_numerals('Latin', kleur) == convert_numerals('Latin', 'groen'):
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
          if convert_numerals('Latin', 'antwoord2') == convert_numerals('Latin', '10'):
            print(f'Goedzo')
          else:
            print(f'lalala')
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # if pressed repeat tests
    #

    def test_if_pressed_repeat(self):
        code = textwrap.dedent("""\
        if x is pressed
            repeat 5 times
                print 'doe het 5 keer!'""")

        expected = HedyTester.dedent("""\
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              for i in range(int('5')):
                print(f'doe het 5 keer!')
                time.sleep(0.1)
              break""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_pressed_repeat_turtle_moves_multiple_keys(self):
        code = textwrap.dedent("""\
        repeat 10 times
            if w is pressed
                forward 25
            if a is pressed
                turn -90
            if d is pressed
                turn 90
            if s is pressed
                turn 180""")

        expected = HedyTester.dedent("""\
        for i in range(int('10')):
          while not pygame_end:
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
              pygame_end = True
              pygame.quit()
              break
            if event.type == pygame.KEYDOWN:
              if event.unicode == 'w':
                trtl = 25
                try:
                  trtl = int(trtl)
                except ValueError:
                  raise Exception(f'While running your program the command <span class="command-highlighted">forward</span> received the value <span class="command-highlighted">{trtl}</span> which is not allowed. Try changing the value to a number.')
                t.forward(min(600, trtl) if trtl > 0 else max(-600, trtl))
                time.sleep(0.1)
                break
              if event.unicode == 'a':
                trtl = -90
                try:
                  trtl = int(trtl)
                except ValueError:
                  raise Exception(f'While running your program the command <span class="command-highlighted">turn</span> received the value <span class="command-highlighted">{trtl}</span> which is not allowed. Try changing the value to a number.')
                t.right(min(600, trtl) if trtl > 0 else max(-600, trtl))
                break
              if event.unicode == 'd':
                trtl = 90
                try:
                  trtl = int(trtl)
                except ValueError:
                  raise Exception(f'While running your program the command <span class="command-highlighted">turn</span> received the value <span class="command-highlighted">{trtl}</span> which is not allowed. Try changing the value to a number.')
                t.right(min(600, trtl) if trtl > 0 else max(-600, trtl))
                break
              if event.unicode == 's':
                trtl = 180
                try:
                  trtl = int(trtl)
                except ValueError:
                  raise Exception(f'While running your program the command <span class="command-highlighted">turn</span> received the value <span class="command-highlighted">{trtl}</span> which is not allowed. Try changing the value to a number.')
                t.right(min(600, trtl) if trtl > 0 else max(-600, trtl))
                break
          time.sleep(0.1)""")

        self.multi_level_tester(code=code, expected=expected, extra_check_function=self.is_turtle(), max_level=11)
