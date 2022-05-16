import hedy
import textwrap
from tests.Tester import HedyTester

class TestsLevel11(HedyTester):
  level = 11


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

  def test_for_loop(self):
    code = textwrap.dedent("""\
    a is 2
    b is 3
    for a in range 2 to 4
        a is a + 2
        b is b + 2""")
    expected = textwrap.dedent("""\
    a = '2'
    b = '3'
    step = 1 if int(2) < int(4) else -1
    for a in range(int(2), int(4) + step, step):
      a = int(a) + int(2)
      b = int(b) + int(2)
      time.sleep(0.1)""")

    self.single_level_tester(code=code, expected=expected)

  def test_if__else(self):
    code = textwrap.dedent("""\
    a is 5
    if a is 1
        x is 2
    else
        x is 222""")
    expected = textwrap.dedent("""\
    a = '5'
    if str(a) == str('1'):
      x = '2'
    else:
      x = '222'""")



    self.single_level_tester(code=code, expected=expected)

  def test_repeat_with_indent(self):
    code = textwrap.dedent("""\
    repeat 5 times
        print 'koekoek'""")


    expected = textwrap.dedent("""\
    for i in range(int('5')):
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

  def test_for_loop_with_print(self):
    code = textwrap.dedent("""\
    for i in range 1 to 10
        print i
    print 'wie niet weg is is gezien'""")
    expected = textwrap.dedent("""\
    step = 1 if int(1) < int(10) else -1
    for i in range(int(1), int(10) + step, step):
      print(f'{i}')
      time.sleep(0.1)
    print(f'wie niet weg is is gezien')""")

    self.single_level_tester(
      code=code,
      expected=expected,
      expected_commands=['for', 'print', 'print'])

  def test_for_loop_hindi(self):
    code = textwrap.dedent("""\
    for काउंटर in range 1 to 5
        print काउंटर""")

    expected = textwrap.dedent("""\
    step = 1 if int(1) < int(5) else -1
    for v7693a3e5c7a942bd47bf4b5af10576ac in range(int(1), int(5) + step, step):
      print(f'{v7693a3e5c7a942bd47bf4b5af10576ac}')
      time.sleep(0.1)""")

    self.single_level_tester(
      code=code,
      expected=expected,
      expected_commands=['for', 'print'])


  def test_for_loop_arabic(self):
    code = textwrap.dedent("""\
    for دورة in range ١ to ٥
        print دورة""")

    expected = textwrap.dedent("""\
    step = 1 if int(1) < int(5) else -1
    for v637d5dd1f16a4cc1d923588cb55ede49 in range(int(1), int(5) + step, step):
      print(f'{v637d5dd1f16a4cc1d923588cb55ede49}')
      time.sleep(0.1)""")

    self.multi_level_tester(
      max_level=12,
      code=code,
      expected=expected,
      expected_commands=['for', 'print'])

  def test_for_loop_with_assignment(self):
    code = textwrap.dedent("""\
      for i in range 1 to 10
          a is i + 1""")
    expected = textwrap.dedent("""\
      step = 1 if int(1) < int(10) else -1
      for i in range(int(1), int(10) + step, step):
        a = int(i) + int(1)
        time.sleep(0.1)""")

    self.single_level_tester(
      code=code,
      expected=expected,
      expected_commands=['for', 'is', 'addition'])

  def test_reverse_range(self):
    code = textwrap.dedent("""\
    for i in range 10 to 1
        print i
    print 'wie niet weg is is gezien'""")
    expected = textwrap.dedent("""\
    step = 1 if int(10) < int(1) else -1
    for i in range(int(10), int(1) + step, step):
      print(f'{i}')
      time.sleep(0.1)
    print(f'wie niet weg is is gezien')""")

    self.single_level_tester(
      code=code,
      expected=expected,
      expected_commands=['for', 'print', 'print'])


  def test_if_under_else_in_for(self):
    code = textwrap.dedent("""\
    for i in range 0 to 10
        antwoord is ask 'Wat is 5*5'
        if antwoord is 24
            print 'Dat is fout!'
        else
            print 'Dat is goed!'
        if antwoord is 25
            i is 10""")

    expected = textwrap.dedent("""\
    step = 1 if int(0) < int(10) else -1
    for i in range(int(0), int(10) + step, step):
      antwoord = input(f'Wat is 5*5')
      if str(antwoord) == str('24'):
        print(f'Dat is fout!')
      else:
        print(f'Dat is goed!')
      if str(antwoord) == str('25'):
        i = '10'
      time.sleep(0.1)""")

    self.single_level_tester(code=code, expected=expected)

    #fails, issue 363

  def test_for_ifbug(self):
    code = textwrap.dedent("""\
    for i in range 0 to 10
        antwoord is ask 'Wat is 5*5'
        if antwoord is 24
            print 'fout'
    print 'klaar met for loop'""")

    expected = textwrap.dedent("""\
      step = 1 if int(0) < int(10) else -1
      for i in range(int(0), int(10) + step, step):
        antwoord = input(f'Wat is 5*5')
        if str(antwoord) == str('24'):
          print(f'fout')
        time.sleep(0.1)
      print(f'klaar met for loop')""")



    self.single_level_tester(code=code, expected=expected)

  def test_for_loopbug599(self):
    code = textwrap.dedent("""\
    for i in range 0 to 10
        if i is 2
            print '2'""")

    expected = textwrap.dedent("""\
      step = 1 if int(0) < int(10) else -1
      for i in range(int(0), int(10) + step, step):
        if str(i) == str('2'):
          print(f'2')
        time.sleep(0.1)""")



    self.single_level_tester(code=code, expected=expected)

  def test_unindented_second_loop_1209(self):
    code = textwrap.dedent("""\
    for x in range 1 to 10
     for y in range 1 to 10
     print 'x*y'""")

    self.single_level_tester(code, exception=hedy.exceptions.NoIndentationException)
  

  def test_dedented_second_loop_1209(self):
    code = textwrap.dedent("""\
    for x in range 1 to 10
     for y in range 1 to 10
    print 'x*y'""")

    self.single_level_tester(code, exception=hedy.exceptions.NoIndentationException)
  

  def test_zigzag_indented_loop_1209(self):
    code = textwrap.dedent("""\
    for x in range 1 to 10
      for y in range 1 to 10
         print 'this number is'
        print x*y""")

    self.single_level_tester(code, exception=hedy.exceptions.IndentationException)
  



