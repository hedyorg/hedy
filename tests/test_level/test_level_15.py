import textwrap

from parameterized import parameterized

import exceptions
import hedy
from tests.Tester import HedyTester


class TestsLevel15(HedyTester):
    level = 15

    def test_while_equals(self):
        code = textwrap.dedent("""\
      antwoord is 0
      while antwoord != 25
          antwoord is ask 'Wat is 5 keer 5?'
      print 'Goed gedaan!'""")
        expected = textwrap.dedent("""\
    antwoord = 0
    while convert_numerals('Latin', antwoord)!=convert_numerals('Latin', 25):
      antwoord = input(f'''Wat is 5 keer 5?''')
      try:
        antwoord = int(antwoord)
      except ValueError:
        try:
          antwoord = float(antwoord)
        except ValueError:
          pass
      time.sleep(0.1)
    print(f'''Goed gedaan!''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
            expected_commands=['is', 'while', 'ask', 'print']
        )

    @parameterized.expand(['and', 'or'])
    def test_while_and_or(self, op):
        code = textwrap.dedent(f"""\
      answer = 7
      while answer > 5 {op} answer < 10
        answer = ask 'What is 5 times 5?'
      print 'A correct answer has been given'""")

        # Splitting like this to wrap the line around 120 characters max
        expected = textwrap.dedent(f"""\
        answer = 7
        while convert_numerals('Latin', answer)>convert_numerals('Latin', 5) {op} convert_numerals('Latin', answer)<convert_numerals('Latin', 10):
          answer = input(f'''What is 5 times 5?''')
          try:
            answer = int(answer)
          except ValueError:
            try:
              answer = float(answer)
            except ValueError:
              pass
          time.sleep(0.1)
        print(f'''A correct answer has been given''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
            expected_commands=['is', 'while', op, 'ask', 'print']
        )

    def test_while_fr_equals(self):
        # note to self: we need to pass in lang!!
        code = textwrap.dedent("""\
        antwoord est 0
        tant que antwoord != 25
            antwoord est demande 'Wat is 5 keer 5?'
        affiche 'Goed gedaan!'""")
        expected = textwrap.dedent("""\
      antwoord = 0
      while convert_numerals('Latin', antwoord)!=convert_numerals('Latin', 25):
        antwoord = input(f'''Wat is 5 keer 5?''')
        try:
          antwoord = int(antwoord)
        except ValueError:
          try:
            antwoord = float(antwoord)
          except ValueError:
            pass
        time.sleep(0.1)
      print(f'''Goed gedaan!''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
            expected_commands=['is', 'while', 'ask', 'print'],
            lang='fr'
        )

    def test_while_undefined_var(self):
        code = textwrap.dedent("""\
      while antwoord != 25
          print 'hoera'""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.UndefinedVarException,
            max_level=16,
        )

    def test_while_smaller(self):
        code = textwrap.dedent("""\
      getal is 0
      while getal < 100000
          getal is ask 'HOGER!!!!!'
      print 'Hoog he?'""")
        expected = textwrap.dedent("""\
    getal = 0
    while convert_numerals('Latin', getal)<convert_numerals('Latin', 100000):
      getal = input(f'''HOGER!!!!!''')
      try:
        getal = int(getal)
      except ValueError:
        try:
          getal = float(getal)
        except ValueError:
          pass
      time.sleep(0.1)
    print(f'''Hoog he?''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected
        )

    def test_missing_indent_while(self):
        code = textwrap.dedent(f"""\
    answer = 0
    while answer != 25
    answer = ask 'What is 5 times 5?'
    print 'A correct answer has been given'""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            exception=exceptions.NoIndentationException
        )

    def test_if_pressed_without_else_works(self):
        code = textwrap.dedent("""\
        if p is pressed
            print 'press'""")

        expected = textwrap.dedent("""\
         if_pressed_mapping = {"else": "if_pressed_default_else"}
         if_pressed_mapping['p'] = 'if_pressed_p_'
         def if_pressed_p_():
             print(f'''press''')
         extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code, expected=expected, max_level=16)

    def test_if_pressed_works_in_while_loop(self):
        code = textwrap.dedent("""\
      stop is 0
      while stop != 1
          if p is pressed
              print 'press'
          if s is pressed
              stop = 1
      print 'Uit de loop!'""")

        expected = textwrap.dedent("""\
         stop = 0
         while convert_numerals('Latin', stop)!=convert_numerals('Latin', 1):
           if_pressed_mapping = {"else": "if_pressed_default_else"}
           if_pressed_mapping['p'] = 'if_pressed_p_'
           def if_pressed_p_():
               print(f'''press''')
           extensions.if_pressed(if_pressed_mapping)
           if_pressed_mapping = {"else": "if_pressed_default_else"}
           if_pressed_mapping['s'] = 'if_pressed_s_'
           def if_pressed_s_():
               stop = 1
           extensions.if_pressed(if_pressed_mapping)
           time.sleep(0.1)
         print(f'''Uit de loop!''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
        )

    def test_if_pressed_multiple_lines_body(self):
        code = textwrap.dedent("""\
        if x is pressed
            print 'x'
            print 'lalalalala'
        else
            print 'not x'
            print 'lalalalala'""")

        expected = textwrap.dedent("""\
         if_pressed_mapping = {"else": "if_pressed_default_else"}
         if_pressed_mapping['x'] = 'if_pressed_x_'
         def if_pressed_x_():
             print(f'''x''')
             print(f'''lalalalala''')
         if_pressed_mapping['else'] = 'if_pressed_else_'
         def if_pressed_else_():
             print(f'''not x''')
             print(f'''lalalalala''')
         extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
        )

    def test_source_map(self):
        code = textwrap.dedent("""\
        answer = 0
        while answer != 25
            answer = ask 'What is 5 times 5?'
        print 'A correct answer has been given'""")

        excepted_code = textwrap.dedent("""\
        answer = 0
        while convert_numerals('Latin', answer)!=convert_numerals('Latin', 25):
          answer = input(f'''What is 5 times 5?''')
          try:
            answer = int(answer)
          except ValueError:
            try:
              answer = float(answer)
            except ValueError:
              pass
          time.sleep(0.1)
        print(f'''A correct answer has been given''')""")

        expected_source_map = {
            '1/1-1/7': '1/1-1/7',
            '1/1-1/11': '1/1-1/11',
            '2/7-2/13': '2/33-2/39',
            '2/7-2/19': '2/7-2/71',
            '3/5-3/11': '8/5-8/11',
            '3/5-3/38': '3/1-9/18',
            '2/1-3/47': '2/1-11/18',
            '4/1-4/40': '12/1-12/46',
            '1/1-4/41': '1/1-12/46'
        }

        self.single_level_tester(code, expected=excepted_code)
        self.source_map_tester(code=code, expected_source_map=expected_source_map)
