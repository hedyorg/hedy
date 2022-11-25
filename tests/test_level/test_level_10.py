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
    # for list command
    #
    def test_for_list(self):
        code = textwrap.dedent("""\
        dieren is hond, kat, papegaai
        for dier in dieren
            print dier""")

        expected = textwrap.dedent("""\
        dieren = ['hond', 'kat', 'papegaai']
        for dier in dieren:
          print(f'{dier}')
          time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=['is', 'for', 'print'],
            max_level=11
        )

    def test_for_list_hindi(self):
        code = textwrap.dedent("""\
        क is hond, kat, papegaai
        for काउंटर in क
            print काउंटर""")

        expected = textwrap.dedent("""\
        क = ['hond', 'kat', 'papegaai']
        for काउंटर in क:
          print(f'{काउंटर}')
          time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            expected_commands=['is', 'for', 'print'],
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
        familie = ['baby', 'mommy', 'daddy', 'grandpa', 'grandma']
        for shark in familie:
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
            exception=hedy.exceptions.InvalidArgumentTypeException)

    #
    # if pressed tests
    #

    def test_if_pressed_with_list_and_for(self):
        code = textwrap.dedent("""\
        lijstje is kip, haan, kuiken
        if x is pressed
            for dier in lijstje
                print 'dier'""")

        expected = HedyTester.dedent("""\
        lijstje = ['kip', 'haan', 'kuiken']
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              for dier in lijstje:
                print(f'dier')
                time.sleep(0.1)
              break""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11)
