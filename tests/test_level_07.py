import hedy
import textwrap
from parameterized import parameterized
from test_level_01 import HedyTester

class TestsLevel7(HedyTester):
  level = 7

  #repeat tests
  def test_repeat_turtle(self):
    code = "repeat 3 times forward 100"

    expected = HedyTester.dedent(
      "for i in range(int('3')):",
      (HedyTester.forward_transpiled(100), '  '))

    self.single_level_tester(code=code, expected=expected, extra_check_function=self.is_turtle())

  def test_repeat_with_variable_print(self):
    code = textwrap.dedent("""\
    n is 5
    repeat n times print 'me wants a cookie!'""")

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
    repeat n times print 'me wants a cookie!'""")

    self.single_level_tester(code=code, exception=hedy.exceptions.UndefinedVarException)

  def test_repeat_with_string_variable_gives_type_error(self):
    code = textwrap.dedent("""\
      n is 'test'
      repeat n times print 'n'""")

    self.single_level_tester(code=code, exception=hedy.exceptions.InvalidArgumentTypeException)

  def test_repeat_with_list_variable_gives_type_error(self):
    code = textwrap.dedent("""\
      n is 1, 2, 3
      repeat n times print 'n'""")

    self.single_level_tester(code=code, exception=hedy.exceptions.InvalidArgumentTypeException)

  def test_repeat_with_ask(self):
    code = textwrap.dedent("""\
      n is ask 'How many times?'
      repeat n times print 'n'""")

    expected = textwrap.dedent("""\
      n = input(f'How many times?')
      for i in range(int(n)):
        print(f'{n}')
        time.sleep(0.1)""")

    self.single_level_tester(code=code, expected=expected)

  def test_repeat_basic_print(self):
    code = textwrap.dedent(f"""\
    repeat 5 times print 'me wants a cookie!'""")

    expected = textwrap.dedent("""\
    for i in range(int('5')):
      print(f'me wants a cookie!')
      time.sleep(0.1)""")

    output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.single_level_tester(code=code, expected=expected, output=output)

  @parameterized.expand(['5', '𑁫', '५', '૫', '੫', '৫', '೫', '୫', '൫', '௫', '౫', '၅', '༥', '᠕', '៥', '๕', '໕', '꧕', '٥', '۵'])
  def test_repeat_all_numerals(self, number):
    code = textwrap.dedent(f"repeat {number} times print 'me wants a cookie!'")

    expected = textwrap.dedent(f"""\
    for i in range(int('{number}')):
      print(f'me wants a cookie!')
      time.sleep(0.1)""")

    output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    print("number:", number)

    self.single_level_tester(code=code, expected=expected, output=output)


  def test_repeat_over_9_times(self):

    code = textwrap.dedent("""\
    repeat 10 times print 'me wants a cookie!'""")

    expected = textwrap.dedent("""\
    for i in range(int('10')):
      print(f'me wants a cookie!')
      time.sleep(0.1)""")

    output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")
    self.single_level_tester(
      code=code,
      expected=expected,
      expected_commands=['repeat','print'],
      output=output)

  def test_repeat_with_collision(self):
      code = textwrap.dedent("""\
      i is hallo!
      repeat 5 times print 'me wants a cookie!'
      print i""")

      expected = textwrap.dedent("""\
      i = 'hallo!'
      for _i in range(int('5')):
        print(f'me wants a cookie!')
        time.sleep(0.1)
      print(f'{i}')""")

      output = textwrap.dedent("""\
      me wants a cookie!
      me wants a cookie!
      me wants a cookie!
      me wants a cookie!
      me wants a cookie!
      hallo!""")

      self.single_level_tester(
        code=code,
        expected=expected,
        expected_commands=['is', 'repeat', 'print', 'print'],
        output=output)

  def test_if_and_repeat(self):
    code = textwrap.dedent("""\
    naam is Hedy
    if naam is Hedy repeat 3 times print 'Hallo Hedy!'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      for i in range(int('3')):
        print(f'Hallo Hedy!')
        time.sleep(0.1)""")

    self.single_level_tester(
      code=code,
      expected=expected)

