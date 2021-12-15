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
    self.single_level_tester(code=code, expected=expected, output=output)

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

      self.single_level_tester(code=code, expected=expected, output=output)