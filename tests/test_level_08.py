import hedy
import textwrap
from test_level_01 import HedyTester

class TestsLevel8(HedyTester):
  level = 8

  def test_if_with_indent(self):
    # todo should be tested for all levels!
    code = textwrap.dedent("""\
    naam is Hedy
    if naam is Hedy
        print 'koekoek'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")

    self.assertEqual(expected, result.code)

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
      expected=expected,
      test_name=self.name()
    )

  def test_if_in_list_with_string_var_gives_type_error(self):
    code = textwrap.dedent("""\
    items is red
    if red in items
        print 'found!'""")
    self.multi_level_tester(
      max_level=11,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException,
      test_name=self.name()
    )

  def test_equality_with_list_gives_error(self):
    code = textwrap.dedent("""\
    color is 5, 6, 7
    if red is color
        print 'success!'""")
    self.multi_level_tester(
      max_level=11,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException,
      test_name=self.name()
    )

  def test_repeat_with_indent(self):
    code = textwrap.dedent("""\
    repeat 5 times
      print 'koekoek'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    for i in range(int(5)):
      print(f'koekoek')""")

    self.assertEqual(expected, result.code)
  def test_repeat_with_variable_print(self):
    code = textwrap.dedent("""\
    n is 5
    repeat n times
        print 'me wants a cookie!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    n = '5'
    for i in range(int(n)):
      print(f'me wants a cookie!')""")

    self.assertEqual(expected, result.code)

    expected_output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.assertEqual(expected_output, HedyTester.run_code(result))
  def test_repeat_with_non_latin_variable_print(self):
    code = textwrap.dedent("""\
    állatok is 5
    repeat állatok times
        print 'me wants a cookie!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    v79de0191e90551f058d466c5e8c267ff = '5'
    for i in range(int(v79de0191e90551f058d466c5e8c267ff)):
      print(f'me wants a cookie!')""")

    self.assertEqual(expected, result.code)

    expected_output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.assertEqual(expected_output, HedyTester.run_code(result))
  def test_if_else(self):
    code = textwrap.dedent("""\
    antwoord is ask 'Hoeveel is 10 plus 10?'
    if antwoord is 20
        print 'Goedzo!'
        print 'Het antwoord was inderdaad ' antwoord
    else
        print 'Foutje'
        print 'Het antwoord moest zijn ' antwoord""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    antwoord = input('Hoeveel is 10 plus 10?')
    if str(antwoord) == str('20'):
      print(f'Goedzo!')
      print(f'Het antwoord was inderdaad {antwoord}')
    else:
      print(f'Foutje')
      print(f'Het antwoord moest zijn {antwoord}')""")

    self.assertEqual(expected, result.code)
  def test_repeat_basic_print(self):
    code = textwrap.dedent("""\
    repeat 5 times
      print 'me wants a cookie!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    for i in range(int(5)):
      print(f'me wants a cookie!')""")

    self.assertEqual(expected, result.code)

    expected_output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.assertEqual(expected_output, HedyTester.run_code(result))
  def test_allow_space_after_else_line(self):
    #todo should work up to 11??
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
      expected=expected,
      test_name=self.name()
    )

  def test_issue_297(self):
    code = textwrap.dedent("""\
    count is 1
    repeat 12 times
      print count ' times 12 is ' count*12
      count is count + 1""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    count = '1'
    for i in range(int(12)):
      print(f'{count} times 12 is {int(count) * int(12)}')
      count = int(count) + int(1)""")

    self.assertEqual(expected, result.code)

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

    with self.assertRaises(hedy.exceptions.LockedLanguageFeatureException) as context:
      result = hedy.transpile(code, self.level)
  def test_repeat_nested_in_if(self):
    code = textwrap.dedent("""\
    kleur is groen
    if kleur is groen
        repeat 3 times
            print 'mooi'""")

    with self.assertRaises(hedy.exceptions.LockedLanguageFeatureException) as context:
      result = hedy.transpile(code, self.level)


  def test_quote_in_if(self):
    code = textwrap.dedent("""\
    if eten is 'pizza'
      print 'lekker'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    if str('eten') == str('pizza'):
      print(f'lekker')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected,
      test_name=self.name()
    )


# (so this should fail, for now)
# at one point we want a real "Indent" error and a better error message
# for this!

# def test_level_7_no_indentation(self):
#   #test that we get a parse error here
#   code = textwrap.dedent("""\
#   antwoord is ask Hoeveel is 10 keer tien?
#   if antwoord is 100
#   print 'goed zo'
#   else
#   print 'bah slecht'""")
#
#   with self.assertRaises(Exception) as context:
#     result = hedy.transpile(code, self.level)
#   self.assertEqual(str(context.exception), 'Parse')

