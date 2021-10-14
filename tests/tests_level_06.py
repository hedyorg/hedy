import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel6(HedyTester):
  level = 6




  def test_repeat_turtle(self):
    code = textwrap.dedent("""\
    repeat 3 times forward 100""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    for i in range(int('3')):
      t.forward(100)
      time.sleep(0.1)""")

    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)



  def test_repeat_with_variable_print(self):
    code = textwrap.dedent("""\
    n is 5
    repeat n times print 'me wants a cookie!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    n = '5'
    for i in range(int(n)):
      print(f'me wants a cookie!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.assertEqual(expected_output, self.run_code(result))

  # todo: a few more things repeated from 4 here?


  # now add repeat
  def test_repeat_basic_print(self):
    code = textwrap.dedent("""\
    repeat 5 times print 'me wants a cookie!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    for i in range(int('5')):
      print(f'me wants a cookie!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = textwrap.dedent("""\
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!
    me wants a cookie!""")

    self.assertEqual(expected_output, self.run_code(result))


  def test_repeat_over_9_times(self):

    code = textwrap.dedent("""\
    repeat 10 times print 'me wants a cookie!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    for i in range(int('10')):
      print(f'me wants a cookie!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = textwrap.dedent("""\
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
    self.assertEqual(expected_output, self.run_code(result))


  def test_repeat_with_collision(self):
      code = textwrap.dedent("""\
      i is hallo!
      repeat 5 times print 'me wants a cookie!'
      print i""")

      result = hedy.transpile(code, self.level)

      expected = textwrap.dedent("""\
      i = 'hallo!'
      for _i in range(int('5')):
        print(f'me wants a cookie!')
      print(f'{i}')""")

      self.assertEqual(expected, result.code)
      self.assertEqual(False, result.has_turtle)

      expected_output = textwrap.dedent("""\
      me wants a cookie!
      me wants a cookie!
      me wants a cookie!
      me wants a cookie!
      me wants a cookie!
      hallo!""")

      self.assertEqual(expected_output, self.run_code(result))