import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel10(HedyTester):
  level = 10
  
  def test_if_with_indent(self):
    code = textwrap.dedent("""\
    naam is Hedy
    if naam is Hedy:
        print 'koekoek'""")
    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
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
    antwoord = input('Hoeveel is 10 plus 10?')
    if str(antwoord) == str('20'):
      print(f'Goedzo!')
      print(f'Het antwoord was inderdaad {antwoord}')
    else:
      print(f'Foutje')
      print(f'Het antwoord moest zijn {antwoord}')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_for_loop(self):
    code = textwrap.dedent("""\
    a is 2
    a is 3
    for a in range 2 to 4:
      a is a + 2
      b is b + 2""")
    expected = textwrap.dedent("""\
    a = '2'
    a = '3'
    step = 1 if int(2) < int(4) else -1
    for a in range(int(2), int(4) + step, step):
      a = int(a) + int(2)
      b = int(b) + int(2)""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_if__else(self):
    code = textwrap.dedent("""\
    a is 5
    if a is 1:
      x is 2
    else:
      x is 222""")
    expected = textwrap.dedent("""\
    a = '5'
    if str(a) == str('1'):
      x = '2'
    else:
      x = '222'""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_forloop(self):
    code = textwrap.dedent("""\
    for i in range 1 to 10:
      print i
    print 'wie niet weg is is gezien'""")
    expected = textwrap.dedent("""\
    step = 1 if int(1) < int(10) else -1
    for i in range(int(1), int(10) + step, step):
      print(f'{i}')
    print(f'wie niet weg is is gezien')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_allow_space_after_else_line(self):

    code = textwrap.dedent("""\
    a is 1
    if a is 1:
      print a
    else:   
      print 'nee'""")

    expected = textwrap.dedent("""\
    a = '1'
    if str(a) == str('1'):
      print(f'{a}')
    else:
      print(f'nee')""")

    self.multi_level_tester(
      max_level=10,
      code=code,
      expected=expected,
      test_name=self.name()
    )


  def test_allow_space_before_colon(self):
    max_level=10

    code = textwrap.dedent("""\
    a is 1
    if a is 1  :
      print a
    else:   
      print 'nee'""")

    expected = textwrap.dedent("""\
    a = '1'
    if str(a) == str('1'):
      print(f'{a}')
    else:
      print(f'nee')""")

    self.multi_level_tester(
      max_level=10,
      code=code,
      expected=expected,
      test_name=self.name()
    )


  def test_if_under_else_in_for(self):
    #todo can me multitester with higher levels!
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
      antwoord = input('Wat is 5*5')
      if str(antwoord) == str('24'):
        print(f'Dat is fout!')
      else:
        print(f'Dat is goed!')
      if str(antwoord) == str('25'):
        i = '10'""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_if_elif(self):
      code = textwrap.dedent("""\
      a is 5
      if a is 1:
        x is 2
      elif a is 2:
        x is 222""")
      expected = textwrap.dedent("""\
      a = '5'
      if str(a) == str('1'):
        x = '2'
      elif str(a) == str('2'):
        x = '222'""")

      result = hedy.transpile(code, self.level)

      self.assertEqual(expected, result.code)
      self.assertEqual(False, result.has_turtle)

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
      a = '5'
      if str(a) == str('1'):
        x = '2'
      elif str(a) == str('4'):
        x = '3'
      elif str(a) == str('2'):
        x = '222'""")

      result = hedy.transpile(code, self.level)

      self.assertEqual(expected, result.code)
      self.assertEqual(False, result.has_turtle)


