import textwrap

from parameterized import parameterized

import exceptions
import hedy
from tests.Tester import HedyTester


class TestsLevel17(HedyTester):
    level = 17

    def test_if_with_indent(self):
        code = textwrap.dedent("""\
    naam is 'Hedy'
    if naam is 'Hedy':
        print 'koekoek'""")
        expected = textwrap.dedent("""\
    naam = 'Hedy'
    if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
      print(f'''koekoek''')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_with_equals_sign(self):
        code = textwrap.dedent("""\
    naam is 'Hedy'
    if naam == Hedy:
        print 'koekoek'""")

        expected = textwrap.dedent("""\
    naam = 'Hedy'
    if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
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

        expected = textwrap.dedent("""\
    antwoord = input(f'''Hoeveel is 10 plus 10?''')
    try:
      antwoord = int(antwoord)
    except ValueError:
      try:
        antwoord = float(antwoord)
      except ValueError:
        pass
    if convert_numerals('Latin', antwoord) == convert_numerals('Latin', '20'):
      print(f'''Goedzo!''')
      print(f'''Het antwoord was inderdaad {antwoord}''')
    else:
      print(f'''Foutje''')
      print(f'''Het antwoord moest zijn {antwoord}''')""")

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
    computerc = 'PC'
    userc = 'Hedy'
    print(f'''Pilihan komputer: {computerc}''')
    if convert_numerals('Latin', userc) == convert_numerals('Latin', computerc) and convert_numerals('Latin', userc) == convert_numerals('Latin', 'Hedy'):
      print(f'''SERI''')
    else:
      print(f'''Komputer''')""")

        self.single_level_tester(code=code, expected=expected)

    def test_for_loop_arabic(self):
        code = textwrap.dedent("""\
    for دورة in range ١ to ٥:
        print دورة""")

        expected = textwrap.dedent("""\
    step = 1 if 1 < 5 else -1
    for دورة in range(1, 5 + step, step):
      print(f'''{دورة}''')
      time.sleep(0.1)""")

        self.single_level_tester(
            code=code,
            expected=expected,
            expected_commands=['for', 'print'])

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
    computerc = 'PC'
    userc = 'Hedy'
    print(f'''Pilihan komputer: {computerc}''')
    if convert_numerals('Latin', userc) == convert_numerals('Latin', computerc) and convert_numerals('Latin', userc) == convert_numerals('Latin', 'Hedy'):
      print(f'''SERI''')
    elif convert_numerals('Latin', userc) == convert_numerals('Latin', 'PC') and convert_numerals('Latin', userc) == convert_numerals('Latin', 'Hedy'):
      print(f'''HARI''')
    else:
      print(f'''Komputer''')""")

        self.single_level_tester(code=code, expected=expected)

    def test_for_loop(self):
        code = textwrap.dedent("""\
    a is 2
    b is 3
    for a in range 2 to 4:
        a is a + 2
        b is b + 2""")
        expected = textwrap.dedent("""\
    a = 2
    b = 3
    step = 1 if 2 < 4 else -1
    for a in range(2, 4 + step, step):
      a = a + 2
      b = b + 2
      time.sleep(0.1)""")

        self.single_level_tester(code=code, expected=expected)

    def test_if__else(self):
        code = textwrap.dedent("""\
    a is 5
    if a is 1:
        x is 2
    else:
        x is 222""")
        expected = textwrap.dedent("""\
    a = 5
    if convert_numerals('Latin', a) == convert_numerals('Latin', '1'):
      x = 2
    else:
      x = 222""")
        self.single_level_tester(code=code, expected=expected)

    def test_forloop(self):
        code = textwrap.dedent("""\
    for i in range 1 to 10:
        print i
    print 'wie niet weg is is gezien'""")
        expected = textwrap.dedent("""\
    step = 1 if 1 < 10 else -1
    for i in range(1, 10 + step, step):
      print(f'''{i}''')
      time.sleep(0.1)
    print(f'''wie niet weg is is gezien''')""")

        self.single_level_tester(code=code, expected=expected)

    def test_allow_space_after_else_line(self):
        code = textwrap.dedent("""\
    a is 1
    if a is 1:
        print a
    else:
        print 'nee'""")

        expected = textwrap.dedent("""\
    a = 1
    if convert_numerals('Latin', a) == convert_numerals('Latin', '1'):
      print(f'''{a}''')
    else:
      print(f'''nee''')""")

        self.multi_level_tester(
            max_level=17,
            code=code,
            expected=expected,
            expected_commands=['is', 'if', 'print', 'print']
        )

    def test_while_undefined_var(self):
        code = textwrap.dedent("""\
      while antwoord != 25:
          print 'hoera'""")

        self.single_level_tester(
            code=code,
            exception=hedy.exceptions.UndefinedVarException
        )

    def test_allow_space_before_colon(self):

        code = textwrap.dedent("""\
    a is 1
    if a is 1  :
        print a
    else:
        print 'nee'""")

        expected = textwrap.dedent("""\
    a = 1
    if convert_numerals('Latin', a) == convert_numerals('Latin', '1'):
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

        expected = textwrap.dedent("""\
    step = 1 if 0 < 10 else -1
    for i in range(0, 10 + step, step):
      antwoord = input(f'''Wat is 5*5''')
      try:
        antwoord = int(antwoord)
      except ValueError:
        try:
          antwoord = float(antwoord)
        except ValueError:
          pass
      if convert_numerals('Latin', antwoord) == convert_numerals('Latin', '24'):
        print(f'''Dat is fout!''')
      else:
        print(f'''Dat is goed!''')
      if convert_numerals('Latin', antwoord) == convert_numerals('Latin', '25'):
        i = 10
      time.sleep(0.1)""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_elif(self):
        code = textwrap.dedent("""\
      a is 5
      if a is 1:
          x is 2
      elif a is 2:
          x is 222""")
        expected = textwrap.dedent("""\
      a = 5
      if convert_numerals('Latin', a) == convert_numerals('Latin', '1'):
        x = 2
      elif convert_numerals('Latin', a) == convert_numerals('Latin', '2'):
        x = 222""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_elif_french(self):
        code = textwrap.dedent("""\
      a est 5
      si a est 1:
          x est 2
      sinon si a est 2:
          x est 222""")
        expected = textwrap.dedent("""\
      a = 5
      if convert_numerals('Latin', a) == convert_numerals('Latin', '1'):
        x = 2
      elif convert_numerals('Latin', a) == convert_numerals('Latin', '2'):
        x = 222""")

        self.single_level_tester(code=code, expected=expected, lang='fr')

    def test_if_with_multiple_elifs(self):
        code = textwrap.dedent("""\
      a is 5
      if a is 1:
          x is 2
      elif a is 4:
          x is 3
      elif a is 2:
          x is 222""")
        expected = textwrap.dedent("""\
      a = 5
      if convert_numerals('Latin', a) == convert_numerals('Latin', '1'):
        x = 2
      elif convert_numerals('Latin', a) == convert_numerals('Latin', '4'):
        x = 3
      elif convert_numerals('Latin', a) == convert_numerals('Latin', '2'):
        x = 222""")

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
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_equality_with_lists(self):
        code = textwrap.dedent("""\
      m is [1, 2]
      n is [1, 2]
      if m is n:
          a is 1""")

        expected = textwrap.dedent("""\
      m = [1, 2]
      n = [1, 2]
      if convert_numerals('Latin', m) == convert_numerals('Latin', n):
        a = 1""")

        self.multi_level_tester(
            code=code,
            expected=expected
        )

    def test_equality_with_incompatible_types_gives_error(self):
        code = textwrap.dedent("""\
    a is 'test'
    b is 15
    if a is b:
      c is 1""")
        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.InvalidTypeCombinationException
        )

    @parameterized.expand(HedyTester.comparison_commands)
    def test_comparisons(self, comparison):
        code = textwrap.dedent(f"""\
      leeftijd is ask 'Hoe oud ben jij?'
      if leeftijd {comparison} 12:
          print 'Dan ben je jonger dan ik!'""")
        expected = textwrap.dedent(f"""\
      leeftijd = input(f'''Hoe oud ben jij?''')
      try:
        leeftijd = int(leeftijd)
      except ValueError:
        try:
          leeftijd = float(leeftijd)
        except ValueError:
          pass
      if convert_numerals('Latin', leeftijd).zfill(100){comparison}convert_numerals('Latin', 12).zfill(100):
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
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_not_equal_string_literal(self):
        code = textwrap.dedent(f"""\
    if 'quoted' != 'string':
      sleep""")
        expected = textwrap.dedent(f"""\
    if 'quoted'.zfill(100)!='string'.zfill(100):
      time.sleep(1)""")

        self.multi_level_tester(
            code=code,
            expected=expected
        )

    @parameterized.expand(["'text'", '1', '1.3', '[1, 2]'])
    def test_not_equal(self, arg):
        code = textwrap.dedent(f"""\
      a = {arg}
      b = {arg}
      if a != b:
          b = 1""")

        expected = textwrap.dedent(f"""\
      a = {arg}
      b = {arg}
      if convert_numerals('Latin', a).zfill(100)!=convert_numerals('Latin', b).zfill(100):
        b = 1""")

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
            exception=exceptions.InvalidTypeCombinationException
        )

    #
    # if pressed turtle tests
    #
    def test_if_pressed_repeat_multiple_x_turtle_move(self):
        code = textwrap.dedent("""\
      repeat 10 times
          if w is pressed:
              forward 25
          if a is pressed:
              turn -90
          if d is pressed:
              turn 90
          if s is pressed:
              turn 180""")

        expected = HedyTester.dedent(f"""\
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
              {HedyTester.indent(
                HedyTester.forward_transpiled(25.0, self.level),
                14, True)
              }
              break
            if event.unicode == 'a':
              {HedyTester.indent(
                HedyTester.turn_transpiled(-90.0, self.level),
                14, True)
              }
              break
            if event.unicode == 'd':
              {HedyTester.indent(
                HedyTester.turn_transpiled(90.0, self.level),
                14, True)
              }
              break
            if event.unicode == 's':
              {HedyTester.indent(
                HedyTester.turn_transpiled(180.0, self.level),
                14, True)
              }
              break
        time.sleep(0.1)""")

        print(expected)

        self.multi_level_tester(code=code, expected=expected, extra_check_function=self.is_turtle())

    def test_if_pressed_with_turtlecolor(self):
        code = textwrap.dedent("""\
      if x is pressed:
          color red""")

        expected = HedyTester.dedent(f"""\
      while not pygame_end:
        pygame.display.update()
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
          pygame_end = True
          pygame.quit()
          break
        if event.type == pygame.KEYDOWN:
          if event.unicode == 'x':
            {HedyTester.indent(
              HedyTester.turtle_color_command_transpiled('red'),
              12, True)
            }
            break""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_if_pressed_else_with_turtle(self):
        self.maxDiff = None
        code = textwrap.dedent("""\
      if x is pressed:
          forward 25
      else:
          turn 90""")

        expected = HedyTester.dedent(f"""\
      while not pygame_end:
        pygame.display.update()
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
          pygame_end = True
          pygame.quit()
          break
        if event.type == pygame.KEYDOWN:
          if event.unicode == 'x':
            {HedyTester.indent(
              HedyTester.forward_transpiled(25.0, self.level),
              12, True)
            }
            break    
          else:
            {HedyTester.indent(
              HedyTester.turn_transpiled(90.0, self.level),
              12, True)
            }
            break\n""") + "    "

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    #
    # pressed negative tests
    #

    def test_if_no_colon_after_pressed_gives_parse_error(self):
        code = textwrap.dedent("""\
        if x is pressed
            print 'no colon!'""")

        self.single_level_tester(
            code=code,
            exception=hedy.exceptions.ParseException,
            extra_check_function=lambda c: c.exception.error_location[0] == 2 and c.exception.error_location[1] == 5
        )
