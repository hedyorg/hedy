import hedy
import textwrap
from parameterized import parameterized
from test_level_01 import HedyTester

class TestsLevel17(HedyTester):
  level = 17

  def test_if_with_indent(self):
    code = textwrap.dedent("""\
    naam is 'Hedy'
    if naam is Hedy:
        print 'koekoek'""")
    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

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
    antwoord = input(f'Hoeveel is 10 plus 10?')
    try:
      antwoord = int(antwoord)
    except ValueError:
      try:
        antwoord = float(antwoord)
      except ValueError:
        pass
    if str(antwoord) == str('20'):
      print(f'Goedzo!')
      print(f'Het antwoord was inderdaad {antwoord}')
    else:
      print(f'Foutje')
      print(f'Het antwoord moest zijn {antwoord}')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

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
    step = 1 if int(2) < int(4) else -1
    for a in range(int(2), int(4) + step, step):
      a = a + 2
      b = b + 2""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_if__else(self):
    code = textwrap.dedent("""\
    a is 5
    if a is 1:
      x is 2
    else:
      x is 222""")
    expected = textwrap.dedent("""\
    a = 5
    if str(a) == str('1'):
      x = 2
    else:
      x = 222""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_forloop(self):
    code = textwrap.dedent("""\
    for i in range 1 to 10:
      print i
    print 'wie niet weg is is gezien'""")
    expected = textwrap.dedent("""\
    step = 1 if int(1) < int(10) else -1
    for i in range(int(1), int(10) + step, step):
      print(f'{i}')
    print(f'wie niet weg is is gezien')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_allow_space_after_else_line(self):
    code = textwrap.dedent("""\
    a is 1
    if a is 1:
      print a
    else:   
      print 'nee'""")

    expected = textwrap.dedent("""\
    a = 1
    if str(a) == str('1'):
      print(f'{a}')
    else:
      print(f'nee')""")

    self.multi_level_tester(
      max_level=17,
      code=code,
      expected=expected,
      test_name=self.name()
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
    if str(a) == str('1'):
      print(f'{a}')
    else:
      print(f'nee')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected,
      test_name=self.name()
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
    step = 1 if int(0) < int(10) else -1
    for i in range(int(0), int(10) + step, step):
      antwoord = input(f'Wat is 5*5')
      try:
        antwoord = int(antwoord)
      except ValueError:
        try:
          antwoord = float(antwoord)
        except ValueError:
          pass
      if str(antwoord) == str('24'):
        print(f'Dat is fout!')
      else:
        print(f'Dat is goed!')
      if str(antwoord) == str('25'):
        i = 10""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_if_elif(self):
    code = textwrap.dedent("""\
      a is 5
      if a is 1:
        x is 2
      elif a is 2:
        x is 222""")
    expected = textwrap.dedent("""\
      a = 5
      if str(a) == str('1'):
        x = 2
      elif str(a) == str('2'):
        x = 222""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

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
      if str(a) == str('1'):
        x = 2
      elif str(a) == str('4'):
        x = 3
      elif str(a) == str('2'):
        x = 222""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_if_in_list_with_string_var_gives_type_error(self):
    code = textwrap.dedent("""\
    items is 'red'
    if 'red' in items:
        a is 1""")
    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException,
      test_name=self.name()
    )

  def test_equality_with_list_gives_error(self):
    code = textwrap.dedent("""\
      color is [5, 6, 7]
      if 1 is color:
          a is 1""")
    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException,
      test_name=self.name()
    )

  def test_equality_with_incompatible_types_gives_error(self):
    code = textwrap.dedent("""\
    a is 'test'
    b is 15
    if a is b:
      c is 1""")
    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.InvalidTypeCombinationException,
      test_name=self.name()
    )

  @parameterized.expand(HedyTester.comparison_commands)
  def test_comparisons(self, comparison):
    code = textwrap.dedent(f"""\
      leeftijd is ask 'Hoe oud ben jij?'
      if leeftijd {comparison} 12:
          print 'Dan ben je jonger dan ik!'""")
    expected = textwrap.dedent(f"""\
      leeftijd = input(f'Hoe oud ben jij?')
      try:
        leeftijd = int(leeftijd)
      except ValueError:
        try:
          leeftijd = float(leeftijd)
        except ValueError:
          pass
      if str(leeftijd).zfill(100){comparison}str(12).zfill(100):
        print(f'Dan ben je jonger dan ik!')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  @parameterized.expand(HedyTester.number_comparisons_commands)
  def test_smaller_with_string_gives_type_error(self, comparison):
    code = textwrap.dedent(f"""\
      a is 'text'
      if a {comparison} 12:
          b is 1""")

    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException,
      test_name=self.name()
    )
