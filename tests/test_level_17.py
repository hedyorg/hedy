import exceptions
import hedy
import textwrap
from parameterized import parameterized
from test_level_01 import HedyTester

class TestsLevel17(HedyTester):
  level = 17

  def test_if_with_indent(self):
    code = textwrap.dedent("""\
    naam is 'Hedy'
    if naam is 'Hedy':
        print 'koekoek'""")
    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")

    self.single_level_tester(code=code, expected=expected)

  def test_if_with_equals_sign(self):
    code = textwrap.dedent("""\
    naam is 'Hedy'
    if naam == Hedy:
        print 'koekoek'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")

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
    print(f'Pilihan komputer: {computerc}')
    if str(userc) == str(computerc) and str(userc) == str('Hedy'):
      print(f'SERI')
    else:
      print(f'Komputer')""")

    self.single_level_tester(code=code, expected=expected)

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
    print(f'Pilihan komputer: {computerc}')
    if str(userc) == str(computerc) and str(userc) == str('Hedy'):
      print(f'SERI')
    elif str(userc) == str('PC') and str(userc) == str('Hedy'):
      print(f'HARI')
    else:
      print(f'Komputer')""")

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
    step = 1 if int(2) < int(4) else -1
    for a in range(int(2), int(4) + step, step):
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
    if str(a) == str('1'):
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
    step = 1 if int(1) < int(10) else -1
    for i in range(int(1), int(10) + step, step):
      print(f'{i}')
      time.sleep(0.1)
    print(f'wie niet weg is is gezien')""")



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
    if str(a) == str('1'):
      print(f'{a}')
    else:
      print(f'nee')""")

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
    if str(a) == str('1'):
      print(f'{a}')
    else:
      print(f'nee')""")

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
      if str(a) == str('1'):
        x = 2
      elif str(a) == str('2'):
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
      if str(a) == str('1'):
        x = 2
      elif str(a) == str('2'):
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
      if str(a) == str('1'):
        x = 2
      elif str(a) == str('4'):
        x = 3
      elif str(a) == str('2'):
        x = 222""")

    self.single_level_tester(code=code, expected=expected, expected_commands=['is', 'if', 'is', 'elif', 'is', 'elif', 'is'])

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
      if str(m) == str(n):
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
      if str(a).zfill(100)!=str(b).zfill(100):
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
