import hedy
import textwrap
from parameterized import parameterized
from test_level_01 import HedyTester

class TestsLevel6(HedyTester):
  level = 6

  # test/command order: 6: ['print', 'ask', 'is', 'if', 'repeat', 'turn', 'forward', calculations]

  # print tests
  def test_print_quoted_var(self):
    code = textwrap.dedent("""\
    naam is 'Hedy'
    print 'ik heet ' naam""")
    expected = textwrap.dedent("""\
    naam = '\\'Hedy\\''
    print(f'ik heet {naam}')""")

    self.multi_level_tester(
      max_level=10,
      code=code,
      expected=expected,
      test_name=self.name()
    )

  @parameterized.expand(['1.5', '1,5'])
  def test_calculation_with_unsupported_float_gives_error(self, number):
    self.multi_level_tester(
      max_level=11,
      code=f"print {number} + 1",
      exception=hedy.exceptions.UnsupportedFloatException,
      test_name=self.name()
    )

  #ask tests
  def test_ask(self):
    code = textwrap.dedent("""\
    antwoord is ask 'wat is je lievelingskleur?'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    antwoord = input(f'wat is je lievelingskleur?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  #if tests
  def test_print_if_else_with_line_break(self):
    # line breaks should be allowed in if-elses until level 7 when we start with indentation
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam
    if naam is Hedy print 'leuk'
    else print 'minder leuk'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet{naam}')
    if str(naam) == str('Hedy'):
      print(f'leuk')
    else:
      print(f'minder leuk')""")

    self.multi_level_tester(
      max_level=6,
      code=code,
      expected=expected,
      test_name=self.name(),
      extra_check_function=self.is_not_turtle()
    )
  def test_print_if_else_with_line_break_and_space(self):
    # line breaks should be allowed in if-elses until level 7 when we start with indentation

    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam
    if naam is Hedy print 'leuk'
    else print 'minder leuk'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet{naam}')
    if str(naam) == str('Hedy'):
      print(f'leuk')
    else:
      print(f'minder leuk')""")

    self.multi_level_tester(
      max_level=6,
      code=code,
      expected=expected,
      test_name=self.name(),
      extra_check_function=self.is_not_turtle()
    )
  def test_if_else_with_space(self):
    #this code has a space at the end of line 2
    code = textwrap.dedent("""\
    a is 2
    if a is 1 print a
    else print 'nee'""")

    expected = textwrap.dedent("""\
    a = '2'
    if str(a) == str('1'):
      print(f'{a}')
    else:
      print(f'nee')""")

    self.multi_level_tester(
      max_level=6,
      code=code,
      expected=expected,
      test_name=self.name(),
      extra_check_function=self.is_not_turtle()
    )

  # calculation tests
  # todo should all be tested for higher levels too!
  def test_print_calc(self):
    code = textwrap.dedent("""\
    print '5 keer 5 is ' 5 * 5""")

    expected = textwrap.dedent("""\
    print(f'5 keer 5 is {int(5) * int(5)}')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_print_multiple_calcs(self):
    code = textwrap.dedent("""\
    print '5 keer 5 keer 5 is ' 5 * 5 * 5""")

    expected = textwrap.dedent("""\
    print(f'5 keer 5 keer 5 is {int(5) * int(5) * int(5)}')""")

    result = hedy.transpile(code, self.level)
    self.assertEqual(expected, result.code)

    output = HedyTester.run_code(result)
    self.assertEqual(output, '5 keer 5 keer 5 is 125')
    self.assertEqual(False, result.has_turtle)
  def test_calc_print(self):
    code = textwrap.dedent("""\
    nummer is 4 + 5
    print nummer""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    nummer = int(4) + int(5)
    print(f'{nummer}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertEqual("9", HedyTester.run_code(result))
  def test_calc_assign(self):
    code = "nummer is 4 + 5"
    result = hedy.transpile(code, self.level)

    expected = "nummer = int(4) + int(5)"
    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_calc_without_space(self):
    code = "nummer is 4+5"
    result = hedy.transpile(code, self.level)

    expected = "nummer = int(4) + int(5)"
    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_assign_calc(self):
    code = textwrap.dedent("""\
    var is 5
    print var + 5""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    var = '5'
    print(f'{int(var) + int(5)}')""")

    self.assertEqual(expected, result.code)

  def test_assign_parses_periods(self):
    code = "period is ."
    expected = "period = '.'"

    self.multi_level_tester(
      max_level=10,
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  def test_calc_vars(self):
    code = textwrap.dedent("""\
    nummer is 5
    nummertwee is 6
    getal is nummer * nummertwee
    print getal""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    getal = int(nummer) * int(nummertwee)
    print(f'{getal}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertEqual("30", HedyTester.run_code(result))
  def test_calc_vars_print(self):
    code = textwrap.dedent("""\
    nummer is 5
    nummertwee is 6
    print nummer * nummertwee""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    print(f'{int(nummer) * int(nummertwee)}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertEqual("30", HedyTester.run_code(result))
  def test_calc_vars_print_divide(self):
    code = textwrap.dedent("""\
    nummer is 5
    nummertwee is 6
    print nummer / nummertwee""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    print(f'{int(nummer) // int(nummertwee)}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertEqual("0", HedyTester.run_code(result))

  def test_calc_with_string_var_gives_type_error(self):
    code = textwrap.dedent("""\
      a is test
      print a + 2""")

    self.multi_level_tester(
      max_level=11,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException,
      test_name=self.name()
    )

  def test_calc_with_list_var_gives_type_error(self):
    code = textwrap.dedent("""\
      a is one, two
      print a + 2""")

    self.multi_level_tester(
      max_level=11,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException,
      test_name=self.name()
    )

  # combined tests
  def test_print_else(self):
      code = textwrap.dedent("""\
      keuzes is 1, 2, 3, 4, 5, regenworm
      punten is 0
      worp is keuzes at random
      if worp is regenworm punten is punten + 5
      else punten is punten + worp
      print 'dat zijn dan ' punten""")

      result = hedy.transpile(code, self.level)

      expected = textwrap.dedent("""\
      keuzes = ['1', '2', '3', '4', '5', 'regenworm']
      punten = '0'
      worp=random.choice(keuzes)
      if str(worp) == str('regenworm'):
        punten = int(punten) + int(5)
      else:
        punten = int(punten) + int(worp)
      print(f'dat zijn dan {punten}')""")

      self.assertEqual(expected, result.code)
      self.assertEqual(False, result.has_turtle)
  def test_ifelse_should_go_before_assign(self):
    code = textwrap.dedent("""\
    kleur is geel
    if kleur is groen antwoord is ok else antwoord is stom
    print antwoord""")
    expected = textwrap.dedent("""\
    kleur = 'geel'
    if str(kleur) == str('groen'):
      antwoord = 'ok'
    else:
      antwoord = 'stom'
    print(f'{antwoord}')""")

    self.multi_level_tester(
      max_level=6,
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )
  def test_ifelse_calc_vars(self):
    code =  textwrap.dedent("""\
    cmp is 1
    test is 2
    acu is 0
    if test is cmp
    acu is acu + 1
    else
    acu is acu + 5""")
    expected = textwrap.dedent("""\
    cmp = '1'
    test = '2'
    acu = '0'
    if str(test) == str(cmp):
      acu = int(acu) + int(1)
    else:
      acu = int(acu) + int(5)""")
    self.multi_level_tester(
      max_level=6,
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  def test_if_calc_vars(self):
    code =  textwrap.dedent("""\
    cmp is 1
    test is 2
    acu is 0
    if test is cmp
    acu is acu + 1""")
    expected = textwrap.dedent("""\
    cmp = '1'
    test = '2'
    acu = '0'
    if str(test) == str(cmp):
      acu = int(acu) + int(1)""")
    self.multi_level_tester(
      max_level=6,
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  def test_equality_promotes_int_to_string(self):
    code = textwrap.dedent("""\
    a is test
    b is 15
    if a is b c is 1""")
    expected = textwrap.dedent("""\
    a = 'test'
    b = '15'
    if str(a) == str(b):
      c = '1'""")
    self.multi_level_tester(
      max_level=7,
      code=code,
      expected=expected,
      test_name=self.name()
    )

  def test_calc_chained_vars(self):
    code = textwrap.dedent("""\
      a is 5
      b is a + 1
      print a + b""")

    expected = textwrap.dedent("""\
      a = '5'
      b = int(a) + int(1)
      print(f'{int(a) + int(b)}')""")

    self.multi_level_tester(
      code=code,
      max_level=11,
      expected=expected,
      extra_check_function=lambda x: self.run_code(x) == "11",
      test_name=self.name()
    )

  def test_cyclic_var_definition_gives_error(self):
    code = "b is b + 1"

    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.CyclicVariableDefinitionException,
      test_name=self.name()
    )
