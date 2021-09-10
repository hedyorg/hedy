import unittest
import hedy
import sys
import io
from contextlib import contextmanager
import textwrap

@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def run_code(parse_result):
  code = "import random\n" + parse_result.code
  with captured_output() as (out, err):
    exec(code)
  return out.getvalue().strip()


class TestsLevel6(unittest.TestCase):
  level = 6
  
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


  def test_transpile_ask(self):
    code = textwrap.dedent("""\
    antwoord is ask 'wat is je lievelingskleur?'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    antwoord = input('wat is je lievelingskleur?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_repeat_nested_in_if(self):

    code = textwrap.dedent("""\
    kleur is ask 'Wat is je lievelingskleur?'
    if kleur is groen repeat 3 times print 'mooi!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    kleur = input('Wat is je lievelingskleur?')
    if str(kleur) == str('groen'):
      for i in range(int('3')):
        print('mooi!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

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

    self.assertEqual(expected_output, run_code(result))

  # new tests for calculations
  def test_simple_calculation(self):
    code = "nummer is 4 + 5"
    result = hedy.transpile(code, self.level)

    expected = "nummer = int(4) + int(5)"
    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_addition_var(self):
    code = textwrap.dedent("""\
    var is 5
    print var + 5""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    var = '5'
    print(str(int(var) + int(5)))""")

    self.assertEqual(expected, result.code)

  def test_simple_calculation_without_space(self):
    code = "nummer is 4+5"
    result = hedy.transpile(code, self.level)

    expected = "nummer = int(4) + int(5)"
    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_transpile_turtle_basic(self):
    result = hedy.transpile("forward 50\nturn\nforward 100", self.level)
    expected = textwrap.dedent("""\
    t.forward(50)
    t.right(90)
    t.forward(100)""")
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

  def test_transpile_turtle_with_ask(self):
    code = textwrap.dedent("""\
    afstand is ask 'hoe ver dan?'
    forward afstand""")
    result = hedy.transpile(code, self.level)
    expected = textwrap.dedent("""\
    afstand = input('hoe ver dan?')
    t.forward(afstand)""")
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

  def test_calculation_and_printing(self):

    code = textwrap.dedent("""\
    nummer is 4 + 5
    print nummer""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    nummer = int(4) + int(5)
    print(str(nummer))""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertEqual("9", run_code(result))

  def test_calculation_with_vars(self):
    code = textwrap.dedent("""\
    nummer is 5
    nummertwee is 6
    getal is nummer * nummertwee
    print getal""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    getal = int(nummer) * int(nummertwee)
    print(str(getal))""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertEqual("30", run_code(result))

  def test_print_calculation_times_directly(self):
    code = textwrap.dedent("""\
    nummer is 5
    nummertwee is 6
    print nummer * nummertwee""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    print(str(int(nummer) * int(nummertwee)))""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertEqual("30", run_code(result))

  def test_print_calculation_divide_directly(self):
    code = textwrap.dedent("""\
    nummer is 5
    nummertwee is 6
    print nummer / nummertwee""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    nummer = '5'
    nummertwee = '6'
    print(str(int(nummer) // int(nummertwee)))""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertEqual("0", run_code(result))

  def test_issue_andras(self):
      code = textwrap.dedent("""\
      prijs is 0
      optiestoetje is ask 'zou u nog een toetje willen'
      if optiestoetje is ja toet is ask 'zou u een brownie of een ijsje willen' else print 'ok dan wordt het ' prijs ' euro'
      print toet
      if toet is ijsje prijs is prijs + 2
      print 'ok bedankt dan wordt het ' prijs ' euro'""")

      result = hedy.transpile(code, self.level)

      expected = textwrap.dedent("""\
        prijs = '0'
        optiestoetje = input('zou u nog een toetje willen')
        if str(optiestoetje) == str('ja'):
          toet = input('zou u een brownie of een ijsje willen')
        else:
          print('ok dan wordt het '+str(prijs)+' euro')
        print(str(toet))
        if str(toet) == str('ijsje'):
          prijs = int(prijs) + int(2)
        print('ok bedankt dan wordt het '+str(prijs)+' euro')""")

      self.assertEqual(expected, result.code)
      self.assertEqual(False, result.has_turtle)

  def test_print_and_else(self):
      code = textwrap.dedent("""\
      keuzes is 1, 2, 3, 4, 5, regenworm
      punten is 0
      worp is keuzes at random
      if worp is regenworm punten is punten + 5
      else punten is punten + worp
      print 'dat zijn dan ' punten""")

      result = hedy.transpile(code, self.level)

      expected = textwrap.dedent("""\
      keuzes = ['1', '2', '3', '4', '5', 'regenworm']
      punten = '0'
      worp=random.choice(keuzes)
      if str(worp) == str('regenworm'):
        punten = int(punten) + int(5)
      else:
        punten = int(punten) + int(worp)
      print('dat zijn dan '+str(punten))""")

      self.assertEqual(expected, result.code)
      self.assertEqual(False, result.has_turtle)


  def test_ifelse_should_go_before_assign(self):

    code = textwrap.dedent("""\
    kleur is geel
    if kleur is groen antwoord is ok else antwoord is stom
    print ans""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    kleur = 'geel'
    if str(kleur) == str('groen'):
      antwoord = 'ok'
    else:
      antwoord = 'stom'
    print(str(ans))""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
