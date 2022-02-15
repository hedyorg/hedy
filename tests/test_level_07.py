import hedy
import textwrap
from test_level_01 import HedyTester

class TestsLevel7(HedyTester):
  level = 7

  #repeat tests
  def test_repeat_turtle(self):
    code = textwrap.dedent("""\
    repeat 3 times forward 100""")

    expected = textwrap.dedent("""\
    for i in range(int('3')):
      t.forward(100)
      time.sleep(0.1)""")

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

  def test_repeat_basic_print(self):
    code = textwrap.dedent("""\
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

