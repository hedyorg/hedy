import hedy
import textwrap
from parameterized import parameterized
from Tester import HedyTester

class TestsLevel6(HedyTester):
  level = 6

  # test/command order: 6: ['print', 'ask', 'is', 'if', 'turn', 'forward', calculations]

  # print tests
  @parameterized.expand(HedyTester.quotes)
  def test_print_quoted_var(self, q):
    code = textwrap.dedent(f"""\
    naam is {q}Hedy{q}
    print {q}ik heet {q} naam""")
    eq = "\\'" if q == "'" else '"'
    expected = textwrap.dedent(f"""\
    naam = '{eq}Hedy{eq}'
    print(f'ik heet {{naam}}')""")

    self.multi_level_tester(
      max_level=11,
      code=code,
      expected=expected
    )

  def test_print_equals(self):
    code = textwrap.dedent("""\
    naam = 'Hedy'
    print 'ik heet ' naam""")
    expected = textwrap.dedent("""\
    naam = '\\'Hedy\\''
    print(f'ik heet {naam}')""")

    self.multi_level_tester(
      max_level=11,
      code=code,
      expected=expected
    )

  def test_print_equals_no_space(self):
    code = textwrap.dedent("""\
    naam='Hedy'
    print 'ik heet ' naam""")
    expected = textwrap.dedent("""\
    naam = '\\'Hedy\\''
    print(f'ik heet {naam}')""")

    self.multi_level_tester(
      max_level=11,
      code=code,
      expected=expected
    )

  @parameterized.expand(['1.5', '1,5'])
  def test_calculation_with_unsupported_float_gives_error(self, number):
    self.multi_level_tester(
      max_level=11,
      code=f"print {number} + 1",
      exception=hedy.exceptions.UnsupportedFloatException
    )

  #ask tests
  def test_ask(self):
    code = textwrap.dedent("""\
    antwoord is ask 'wat is je lievelingskleur?'""")

    expected = textwrap.dedent("""\
    antwoord = input(f'wat is je lievelingskleur?')""")

    self.single_level_tester(code=code, expected=expected)

  def test_ask_equals(self):
    code = textwrap.dedent("""\
    antwoord = ask 'wat is je lievelingskleur?'""")

    expected = textwrap.dedent("""\
    antwoord = input(f'wat is je lievelingskleur?')""")

    self.single_level_tester(code=code, expected=expected)


  def test_chained_ask(self):
    code = textwrap.dedent("""\
    a is ask 'What is a?'
    b is ask 'Are you sure a is ' a '?'
    print a b""")

    expected = textwrap.dedent("""\
      a = input(f'What is a?')
      b = input(f'Are you sure a is {a}?')
      print(f'{a}{b}')""")

    self.single_level_tester(code=code, expected=expected)

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
      max_level=7,
      code=code,
      expected=expected,
      expected_commands=['is', 'print', 'else', 'print', 'print']
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
      expected=expected
    )
  def test_if_else_with_space(self):
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
      expected=expected
    )
  def test_print_if_else_with_is(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam
    if naam is Hedy print 'leuk' else print 'minder leuk'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet{naam}')
    if str(naam) == str('Hedy'):
      print(f'leuk')
    else:
      print(f'minder leuk')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=7)

  def test_print_if_else_with_equals_sign(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam
    if naam = Hedy print 'leuk' else print 'minder leuk'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet{naam}')
    if str(naam) == str('Hedy'):
      print(f'leuk')
    else:
      print(f'minder leuk')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=7
    )

  # calculation tests
  # todo should all be tested for higher levels too!
  def test_print_calc(self):
    code = textwrap.dedent("""\
    print '5 keer 5 is ' 5 * 5""")

    expected = textwrap.dedent("""\
    print(f'5 keer 5 is {int(5) * int(5)}')""")

    self.single_level_tester(code=code, expected=expected)
  def test_print_multiple_calcs(self):
    code = textwrap.dedent("""\
    print '5 keer 5 keer 5 is ' 5 * 5 * 5""")

    expected = textwrap.dedent("""\
    print(f'5 keer 5 keer 5 is {int(5) * int(5) * int(5)}')""")

    output = '5 keer 5 keer 5 is 125'
    self.single_level_tester(code=code, expected=expected, output=output)

  def test_calc_print(self):
    code = textwrap.dedent("""\
    nummer is 4 + 5
    print nummer""")

    expected = textwrap.dedent("""\
    nummer = int(4) + int(5)
    print(f'{nummer}')""")

    self.single_level_tester(code=code, expected=expected, output='9')

  def test_calc_assign(self):
    code = "nummer is 4 + 5"
    expected = "nummer = int(4) + int(5)"
    self.single_level_tester(code=code, expected=expected)

  def test_calc_without_space(self):
    code = "nummer is 4+5"
    expected = "nummer = int(4) + int(5)"
    self.single_level_tester(code=code, expected=expected)

  def test_assign_calc(self):
    code = textwrap.dedent("""\
    var is 5
    print var + 5""")
    expected = textwrap.dedent("""\
    var = '5'
    print(f'{int(var) + int(5)}')""")

    self.single_level_tester(code=code, expected=expected)

  @parameterized.expand(HedyTester.arithmetic_operations)
  def test_calc_precedes_quoted_string_in_assign(self, operation):  # issue #2067
    code = f"a is '3{operation}10'"  # gets parsed to arithmetic operation of '3 and 10'

    self.multi_level_tester(
      max_level=11,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_assign_parses_periods(self):
    code = "period is ."
    expected = "period = '.'"

    self.multi_level_tester(
      max_level=10,
      code=code,
      expected=expected
    )
  def test_assign_var_to_var(self):
    code = textwrap.dedent("""\
    dier1 is hond
    dier2 is dier1
    print dier1""")

    expected = textwrap.dedent("""\
    dier1 = 'hond'
    dier2 = dier1
    print(f'{dier1}')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=11)


  def test_calc_vars(self):
    code = textwrap.dedent("""\
    nummer is 5
    nummertwee is 6
    getal is nummer * nummertwee
    print getal""")

    expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    getal = int(nummer) * int(nummertwee)
    print(f'{getal}')""")

    self.single_level_tester(code=code, expected=expected, output='30')

  def test_calc_vars_print(self):
    code = textwrap.dedent("""\
    nummer is 5
    nummertwee is 6
    print nummer * nummertwee""")

    expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    print(f'{int(nummer) * int(nummertwee)}')""")

    self.single_level_tester(code=code, expected=expected, output='30')

  def test_calc_vars_print_divide(self):
    code = textwrap.dedent("""\
    nummer is 5
    nummertwee is 6
    print nummer / nummertwee""")

    expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    print(f'{int(nummer) // int(nummertwee)}')""")

    self.single_level_tester(code=code, expected=expected, output='0')

  def test_calc_vars_print_subtract(self):
    code = textwrap.dedent("""\
    print '5 min 5 is ' 5 - 5""")

    expected = textwrap.dedent("""\
    print(f'5 min 5 is {int(5) - int(5)}')""")

    self.single_level_tester(code=code, expected=expected, output='5 min 5 is 0')

  def test_calc_vars_print_add_arabic(self):
    code = textwrap.dedent("""\
    nummer is ١
    nummertwee is ١
    print nummer + nummertwee""")

    expected = textwrap.dedent("""\
    nummer = '١'
    nummertwee = '١'
    print(f'{int(nummer) + int(nummertwee)}')""")

    self.single_level_tester(code=code, expected=expected, output='2')

  @parameterized.expand(HedyTester.arithmetic_operations)
  def test_calc_with_string_var_gives_type_error(self, operation):
    code = textwrap.dedent(f"""\
      a is test
      print a {operation} 2""")

    self.multi_level_tester(
      max_level=11,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  @parameterized.expand(HedyTester.arithmetic_operations)
  def test_calc_with_quoted_string_gives_type_error(self, operation):
    code = textwrap.dedent(f"""\
      a is 1
      print a {operation} 'Test'""")

    self.multi_level_tester(
      max_level=11,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  @parameterized.expand(HedyTester.arithmetic_operations)
  def test_calc_with_list_var_gives_type_error(self, operation):
    code = textwrap.dedent(f"""\
      a is one, two
      print a {operation} 2""")

    self.multi_level_tester(
      max_level=11,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  #assign with =
  def test_calc_assign_equals(self):
    code = "nummer = 4 + 5"
    expected = "nummer = int(4) + int(5)"
    self.multi_level_tester(
      code=code,
      max_level=11,
      expected=expected)

  # combined tests
  def test_print_else(self):
      code = textwrap.dedent("""\
      keuzes is 1, 2, 3, 4, 5, regenworm
      punten is 0
      worp is keuzes at random
      if worp is regenworm punten is punten + 5
      else punten is punten + worp
      print 'dat zijn dan ' punten""")

      expected = textwrap.dedent("""\
      keuzes = ['1', '2', '3', '4', '5', 'regenworm']
      punten = '0'
      worp = random.choice(keuzes)
      if str(worp) == str('regenworm'):
        punten = int(punten) + int(5)
      else:
        punten = int(punten) + int(worp)
      print(f'dat zijn dan {punten}')""")

      self.single_level_tester(code=code, expected=expected)

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
      expected=expected
    )
  def test_ifelse_calc_vars(self):
    code = textwrap.dedent("""\
    cmp is 1
    test is 2
    acu is 0
    if test is cmp
    acu is acu + 1
    else acu is acu + 5""")
    # @TODO: Felienne, if the above line starts with "else\nacu", then the test fails intermittently due to ambiguity
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
      expected=expected
    )

  def test_if_calc_vars(self):
    code =  textwrap.dedent("""\
    cmp is 1
    test is 2
    acu is 0
    if test is cmp acu is acu + 1""")
    expected = textwrap.dedent("""\
    cmp = '1'
    test = '2'
    acu = '0'
    if str(test) == str(cmp):
      acu = int(acu) + int(1)""")
    self.single_level_tester(
      code=code,
      expected=expected
    )

  # So legal are:
  #
  # if name is Hedy print 'hello'
  # if name is 'Hedy' print 'hello'
  # if name is 'Hedy is het beste' print 'hello'
  # if name is Hedy c is 5

  # Illegal is:
  #
  # if name is Hedy is het beste print 'hello'
  # if name is Hedy is het beste x is 5

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
      expected=expected
    )

  def test_one_space_in_rhs_if(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is 'James Bond' print 'shaken'""")

    expected = textwrap.dedent("""\
    naam = 'James'
    if str(naam) == str('James Bond'):
      print(f'shaken')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=7)

  def test_no_space_nor_quotes_in_rhs(self):
    code = textwrap.dedent("""\
    warna = ask 'Apa warna favorit kamu?'
    if warna is hijau print 'cantik!' else print 'meh!'""")

    expected = textwrap.dedent("""\
    warna = input(f'Apa warna favorit kamu?')
    if str(warna) == str('hijau'):
      print(f'cantik!')
    else:
      print(f'meh!')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=7)

  def test_one_space_in_rhs_if_else(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is 'James Bond' print 'shaken' else print 'biertje!'""")

    expected = textwrap.dedent("""\
    naam = 'James'
    if str(naam) == str('James Bond'):
      print(f'shaken')
    else:
      print(f'biertje!')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=7)

  @parameterized.expand(HedyTester.quotes)
  def test_quoted_space_rhs(self, q):
    code = textwrap.dedent(f"""\
    naam is James
    if naam is {q}James Bond{q} print {q}shaken{q} else print {q}biertje!{q}""")

    expected = textwrap.dedent(f"""\
    naam = 'James'
    if str(naam) == str({q}James Bond{q}):
      print(f'shaken')
    else:
      print(f'biertje!')""")
    self.single_level_tester(
      code=code,
      expected=expected)


  def test_space_enter_rhs_ifelse(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is James Bond
    print 'shaken' else print 'biertje!'""")

    expected = textwrap.dedent("""\
    naam = 'James'
    if naam == 'James Bond':
      print(f'shaken')
    else:
      print(f'biertje!')""")

    self.single_level_tester(
      code=code,
      expected=expected)

  def test_space_enter_rhs_if(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is James Bond print 'shaken'""")

    self.single_level_tester(
      code=code,
      exception=hedy.exceptions.UnquotedEqualityCheck)


  def test_multiple_spaces_in_rhs_if(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is 'Bond James Bond' print 'shaken'""")

    expected = textwrap.dedent("""\
    naam = 'James'
    if str(naam) == str('Bond James Bond'):
      print(f'shaken')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=7)

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
      expected_commands=['is', 'is', 'addition', 'print', 'addition'],
      extra_check_function=lambda x: self.run_code(x) == "11"
    )

  def test_cyclic_var_definition_gives_error(self):
    code = "b is b + 1"

    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.CyclicVariableDefinitionException
    )

  def test_type_reassignment_to_proper_type_valid(self):
    code = textwrap.dedent("""\
      a is Hello
      a is 5
      b is a + 1
      print a + b""")

    expected = textwrap.dedent("""\
        a = 'Hello'
        a = '5'
        b = int(a) + int(1)
        print(f'{int(a) + int(b)}')""")

    self.multi_level_tester(
      code=code,
      max_level=11,
      expected=expected,
      expected_commands=['is', 'is', 'is', 'addition', 'print', 'addition'],
      extra_check_function=lambda x: self.run_code(x) == "11"
    )
  
  def test_type_reassigment_to_wrong_type_raises_error(self):
    code = textwrap.dedent("""\
      a is 5
      a is test
      print a + 2""")

    self.multi_level_tester(
      max_level=11,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_space_in_string_assignment(self):
    code = textwrap.dedent("""\
      a is 'Hello World'
      print a
      
      a = 'Hello World'
      print a

      a is Hello World
      print a

      a = Hello World
      print a""")
  
    expected = textwrap.dedent("""\
      a = '\\'Hello World\\''
      print(f'{a}')
      a = '\\'Hello World\\''
      print(f'{a}')
      a = 'Hello World'
      print(f'{a}')
      a = 'Hello World'
      print(f'{a}')""")
    
    self.multi_level_tester(
      max_level=11,
      code=code,
      expected=expected
    )
