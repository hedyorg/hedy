import hedy
import textwrap
from parameterized import parameterized
from test_level_01 import HedyTester

class TestsLevel8(HedyTester):
  level = 8

  def test_if_with_indent(self):
    code = textwrap.dedent("""\
    naam is Hedy
    if naam is Hedy
        print 'koekoek'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=11)

  def test_if_with_equals_sign(self):
    code = textwrap.dedent("""\
    naam is Hedy
    if naam = Hedy
        print 'koekoek'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=11)

  def test_one_space_in_rhs_if(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is James Bond
        print 'shaken'""")

    expected = textwrap.dedent("""\
    naam = 'James'
    if str(naam) == str('James Bond'):
      print(f'shaken')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=11)

  def test_one_space_in_rhs_if_else(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is James Bond
        print 'shaken'
    else
        print 'biertje!'""")

    expected = textwrap.dedent("""\
    naam = 'James'
    if str(naam) == str('James Bond'):
      print(f'shaken')
    else:
      print(f'biertje!')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=11)

  def test_multiple_spaces_in_rhs_if(self):
    code = textwrap.dedent("""\
    naam is James
    if naam is Bond James Bond
        print 'shaken'""")

    expected = textwrap.dedent("""\
    naam = 'James'
    if str(naam) == str('Bond James Bond'):
      print(f'shaken')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=11)

  def test_equality_promotes_int_to_string(self):
    code = textwrap.dedent("""\
    a is test
    b is 15
    if a is b
        c is 1""")
    expected = textwrap.dedent("""\
    a = 'test'
    b = '15'
    if str(a) == str(b):
      c = '1'""")
    self.multi_level_tester(
      max_level=11,
      code=code,
      expected=expected
    )

  def test_equality_with_lists_gives_error(self):
    code = textwrap.dedent("""\
      m is 1, 2
      n is 1, 2
      if m is n
        print 'success!'""")

    self.multi_level_tester(
      max_level=11,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_if_in_list_with_string_var_gives_type_error(self):
    code = textwrap.dedent("""\
    items is red
    if red in items
        print 'found!'""")
    self.multi_level_tester(
      max_level=11,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_equality_with_list_gives_error(self):
    code = textwrap.dedent("""\
    color is 5, 6, 7
    if red is color
        print 'success!'""")
    self.multi_level_tester(
      max_level=11,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_repeat_with_indent(self):
    code = textwrap.dedent("""\
    repeat 5 times
        print 'koekoek'""")
 
    expected = textwrap.dedent("""\
    for i in range(int(5)):
      print(f'koekoek')
      time.sleep(0.1)""")

    self.single_level_tester(code=code, expected=expected)
  def test_repeat_with_variable_print(self):
    code = textwrap.dedent("""\
    n is 5
    repeat n times
        print 'me wants a cookie!'""")

 
    expected = textwrap.dedent("""\
    n = '5'
    for i in range(int(n)):
      print(f'me wants a cookie!')
      time.sleep(0.1)""")

    output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.single_level_tester(code=code, expected=expected, output=output)

  def test_repeat_with_undefined_variable(self):
    code = textwrap.dedent("""\
    repeat n times
        print 'me wants a cookie!'""")

    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.UndefinedVarException,
      max_level=10)

  def test_repeat_with_non_latin_variable_print(self):
    code = textwrap.dedent("""\
    állatok is 5
    repeat állatok times
        print 'me wants a cookie!'""")

    expected = textwrap.dedent("""\
    v79de0191e90551f058d466c5e8c267ff = '5'
    for i in range(int(v79de0191e90551f058d466c5e8c267ff)):
      print(f'me wants a cookie!')
      time.sleep(0.1)""")

    output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.single_level_tester(code=code, expected=expected, output=output)

  def test_if_else(self):
    code = textwrap.dedent("""\
    antwoord is ask 'Hoeveel is 10 plus 10?'
    if antwoord is 20
        print 'Goedzo!'
        print 'Het antwoord was inderdaad ' antwoord
    else
        print 'Foutje'
        print 'Het antwoord moest zijn ' antwoord""")

    expected = textwrap.dedent("""\
    antwoord = input(f'Hoeveel is 10 plus 10?')
    if str(antwoord) == str('20'):
      print(f'Goedzo!')
      print(f'Het antwoord was inderdaad {antwoord}')
    else:
      print(f'Foutje')
      print(f'Het antwoord moest zijn {antwoord}')""")

    self.single_level_tester(code=code, expected=expected)
  def test_repeat_basic_print(self):
    code = textwrap.dedent("""\
    repeat 5 times
        print 'me wants a cookie!'""")

    expected = textwrap.dedent("""\
    for i in range(int(5)):
      print(f'me wants a cookie!')
      time.sleep(0.1)""")

    output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.single_level_tester(code=code, expected=expected, output=output)

  def test_allow_space_after_else_line(self):
    #todo should work up to 12??
    code = textwrap.dedent("""\
    a is 1
    if a is 1
        print a
    else
        print 'nee'""")

    expected = textwrap.dedent("""\
    a = '1'
    if str(a) == str('1'):
      print(f'{a}')
    else:
      print(f'nee')""")

    self.multi_level_tester(
      max_level=9,
      code=code,
      expected=expected
    )

  def test_issue_297(self):
    code = textwrap.dedent("""\
    count is 1
    repeat 12 times
        print count ' times 12 is ' count * 12
        count is count + 1""")

    expected = textwrap.dedent("""\
    count = '1'
    for i in range(int(12)):
      print(f'{count} times 12 is {int(count) * int(12)}')
      count = int(count) + int(1)
      time.sleep(0.1)""")

    self.single_level_tester(code=code, expected=expected)

  # negative tests

  def test_issue_902(self):
    code = textwrap.dedent("""\
    print 'kassabon'
    prijs is 0
    repeat 7 times
        ingredient is ask 'wat wil je kopen?'
        if ingredient is appel
            prijs is prijs + 1
    print 'Dat is in totaal ' prijs ' euro.'""")

    self.single_level_tester(code=code, exception=hedy.exceptions.LockedLanguageFeatureException)

  def test_repeat_nested_in_if(self):
    code = textwrap.dedent("""\
    kleur is groen
    if kleur is groen
        repeat 3 times
            print 'mooi'""")

    self.single_level_tester(code=code, exception=hedy.exceptions.LockedLanguageFeatureException)

  @parameterized.expand(HedyTester.quotes)
  def test_quote_in_if(self, q):
    code = textwrap.dedent(f"""\
    if eten is {q}pizza{q}
        print 'lekker'""")

    expected = textwrap.dedent(f"""\
    if str('eten') == str('pizza'):
      print(f'lekker')""")

    self.multi_level_tester(
      code=code,
      max_level=11,
      expected=expected
    )

  def test_level_8_no_indentation(self):
    # gives the right exception for all levels even though it misses brackets
    # because the indent check happens before parsing
    code = textwrap.dedent("""\
    antwoord is ask Hoeveel is 10 keer tien?
    if antwoord is 100
    print 'goed zo'
    else
    print 'bah slecht'""")

    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.NoIndentationException)

  def test_repair_too_few_indents(self):
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


  def test_repair_too_many_indents(self):
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

  @parameterized.expand(["", "'"])
  def test_equality_single_or_not_quoted_rhs_with_inner_double_quote(self, q):
    code = textwrap.dedent(f"""\
      answer is no
      if answer is {q}He said "no"{q}
        print 'no'""")

    expected = textwrap.dedent(f"""\
      answer = 'no'
      if str(answer) == str('He said "no"'):
        print(f'no')""")

    self.multi_level_tester(code=code, expected=expected, max_level=11)

  @parameterized.expand(['', '"'])
  def test_equality_double_or_not_quoted_rhs_with_inner_single_quote(self, q):
    code = textwrap.dedent(f"""\
      answer is no
      if answer is {q}He said 'no'{q}
        print 'no'""")

    expected = textwrap.dedent(f"""\
      answer = 'no'
      if str(answer) == str('He said \\'no\\''):
        print(f'no')""")

    self.multi_level_tester(code=code, expected=expected, max_level=11)
