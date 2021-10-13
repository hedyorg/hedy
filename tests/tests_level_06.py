import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel6(HedyTester):
  level = 6
  
  # print should still work
  def test_print_with_var(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet'+str(naam))""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_print_with_comma(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet,' naam""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet,'+str(naam))""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_turtle_basic(self):
    result = hedy.transpile("forward 50\nturn\nforward 100", self.level)
    expected = textwrap.dedent("""\
    t.forward(50)
    time.sleep(0.1)
    t.right(90)
    t.forward(100)
    time.sleep(0.1)""")
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

  def test_allow_space_after_else_line(self):
    # can gemerged met 5?
    #this code has a space at the end of line 2
    code = textwrap.dedent("""\
    a is 2
    if a is 1 print a 
    else print 'nee'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    a = '2'
    if str(a) == str('1'):
      print(str(a))
    else:
      print('nee')""")

    self.assertEqual(expected, result.code)

  def test_turtle_with_ask(self):
    code = textwrap.dedent("""\
    afstand is ask 'hoe ver dan?'
    forward afstand""")
    result = hedy.transpile(code, self.level)
    expected = textwrap.dedent("""\
    afstand = input('hoe ver dan?')
    t.forward(afstand)
    time.sleep(0.1)""")
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

  def test_print_Spanish(self):
    code = textwrap.dedent("""\
    print 'Cuál es tu color favorito?'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('Cuál es tu color favorito?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_ask_Spanish(self):
    code = textwrap.dedent("""\
    color is ask 'Cuál es tu color favorito?'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    color = input('Cuál es tu color favorito?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


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
      print('me wants a cookie!')""")

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
      print('me wants a cookie!')""")

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
      print('me wants a cookie!')""")

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


  def test_random(self):
    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print dieren at random""")

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(str(random.choice(dieren)))""")

    # check if result is in the expected list
    check_in_list = (lambda x: self.run_code(x) in ['Hond', 'Kat', 'Kangoeroe'])

    self.multi_level_tester(
      max_level=10,
      code=code,
      expected=expected,
      test_name=self.test_name(),
      extra_check_function=check_in_list
    )



  def test_repeat_with_collision(self):
      code = textwrap.dedent("""\
      i is hallo!
      repeat 5 times print 'me wants a cookie!'
      print i""")

      result = hedy.transpile(code, self.level)

      expected = textwrap.dedent("""\
      i = 'hallo!'
      for _i in range(int('5')):
        print('me wants a cookie!')
      print(str(i))""")

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