import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel11(HedyTester):
  level = 11

  # ask tests
  def test_ask_number_answer(self):
    code = textwrap.dedent("""\
    prijs is ask 'hoeveel?'
    gespaard is 7
    sparen is prijs - gespaard
    print 'hallo' sparen""")
    expected = textwrap.dedent("""\
    prijs = input('hoeveel?')
    try:
      prijs = int(prijs)
    except ValueError:
      try:
        prijs = float(prijs)
      except ValueError:
        pass
    gespaard = 7
    sparen = prijs - gespaard
    print(f'hallo{sparen}')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  #new calculations
  def test_int_addition_directly(self):
    code = textwrap.dedent("""\
    print 2 + 2""")
    expected = textwrap.dedent("""\
    print(f'{2 + 2}')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_float_addition_directly(self):
    code = textwrap.dedent("""\
    print 2.5 + 2.5""")
    expected = textwrap.dedent("""\
    print(f'{2.5 + 2.5}')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_float_addition_with_string(self):
    code = textwrap.dedent("""\
    print 'het antwoord is ' 2.5 + 2.5""")
    expected = textwrap.dedent("""\
    print(f'het antwoord is {2.5 + 2.5}')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_float_addition_in_var(self):
    code = textwrap.dedent("""\
    antwoord is 2.5 + 2.5
    print antwoord
    """)
    expected = textwrap.dedent("""\
    antwoord = 2.5 + 2.5
    print(f'{antwoord}')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_float_addition_with_var(self):
    code = textwrap.dedent("""\
    getal1 is 5
    getal2 is 4.3
    print 'dat is dan: ' getal1 + getal2
    """)
    expected = textwrap.dedent("""\
    getal1 = 5
    getal2 = 4.3
    print(f'dat is dan: {getal1 + getal2}')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_store_calc_in_var(self):
    code = textwrap.dedent("""\
    a is 1
    b is 2
    c is a + b
    print c ' is 3'""")
    expected = textwrap.dedent("""\
    a = 1
    b = 2
    c = a + b
    print(f'{c} is 3')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_add_string_vars(self):
    code = textwrap.dedent("""\
    getal1 is '5'
    getal2 is '6'
    print 'dat is dan: ' getal1 + getal2""")
    expected = textwrap.dedent("""\
    getal1 = '5'
    getal2 = '6'
    print(f'dat is dan: {getal1 + getal2}')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    output = self.run_code(result)
    expected_output = 'dat is dan: 56'

    self.assertEqual(expected_output, output)
  def test_add_int_vars(self):
    code = textwrap.dedent("""\
    getal1 is 5
    getal2 is 6
    print 'dat is dan: ' getal1 + getal2""")
    expected = textwrap.dedent("""\
    getal1 = 5
    getal2 = 6
    print(f'dat is dan: {getal1 + getal2}')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)

    output = self.run_code(result)
    expected_output = 'dat is dan: 11'

    self.assertEqual(expected_output, output)

  def test_assign_string_with_quotes(self):
    code = textwrap.dedent("""\
    name is 'felienne'
    print name""")
    expected = textwrap.dedent("""\
    name = 'felienne'
    print(f'{name}')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_assign_string_with_quotes_and_string_value(self):
    code = textwrap.dedent("""\
    name is 'felienne'
    print 'hallo ' name""")
    expected = textwrap.dedent("""\
    name = 'felienne'
    print(f'hallo {name}')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  # negative tests
  def test_assign_string_without_quotes(self):
    code = textwrap.dedent("""\
    name is felienne
    print name""")

    with self.assertRaises(hedy.exceptions.UnquotedAssignTextException) as context:
      result = hedy.transpile(code, self.level)
