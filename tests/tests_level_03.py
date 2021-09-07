import unittest
import hedy
import sys
import io
from contextlib import contextmanager
import textwrap
import inspect

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


class TestsLevel3(unittest.TestCase):
  level = 3
  def test_name(self):
    return inspect.stack()[1][3]

  def test_transpile_other(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("abc felienne 123", self.level)
    self.assertEqual(str(context.exception), 'Invalid')

  def test_transpile_print_level_2(self):
    with self.assertRaises(Exception) as context:
      result = hedy.transpile("print felienne 123", self.level)

    self.assertEqual('Unquoted Text', context.exception.args[0])  # hier moet nog we een andere foutmelding komen!


  def test_print(self):

    code = textwrap.dedent("""\
    print 'hallo wereld!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('hallo wereld!')""")

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

  def test_print_with_comma(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet ,'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet ,')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_print_with_single_quote(self):

    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet \\''""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet \\'')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_name_with_underscore(self):
    code = textwrap.dedent("""\
    voor_naam is Hedy
    print 'ik heet '""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    voor_naam = 'Hedy'
    print('ik heet ')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_name_that_is_keyword(self):
    hashed_var = hedy.hash_var("for")

    code = textwrap.dedent("""\
    for is Hedy
    print 'ik heet ' for """)

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent(f"""\
    {hashed_var} = 'Hedy'
    print('ik heet '+{hashed_var})""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_print_Spanish(self):

    code = textwrap.dedent("""\
    print 'Cuál es tu color favorito?'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('Cuál es tu color favorito?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_print_with_list_var(self):

    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print dieren at 1""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(dieren[1])""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    self.assertEqual(run_code(result), "Kat")

  def test_print_with_list_var_random(self):

    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print dieren at random""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(random.choice(dieren))""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])

  def test_transpile_ask_Spanish(self):
    code = textwrap.dedent("""\
    color is ask 'Cuál es tu color favorito?'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    color = input('Cuál es tu color favorito?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_print_2(self):

    code = textwrap.dedent("""\
    print 'ik heet henk'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('ik heet henk')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_print_with_var(self):

    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print('ik heet'+naam)""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_transpile_ask_with_print(self):

    code = textwrap.dedent("""
    kleur is ask 'wat is je lievelingskleur?'
    print 'jouw lievelingskleur is dus' kleur '!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur?')
    print('jouw lievelingskleur is dus'+kleur+'!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_transpile_ask_with_var(self):

    code = textwrap.dedent("""
    ding is kleur
    kleur is ask 'Wat is je lievelings' ding
    print 'Jouw favoriet is dus ' kleur""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    ding = 'kleur'
    kleur = input('Wat is je lievelings'+ding)
    print('Jouw favoriet is dus '+kleur)""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_transpile_ask_no_quotes(self):
    code = textwrap.dedent("""
    ding is kleur
    kleur is ask Wat is je lievelingskleur'
    print 'Jouw favoriet is dus ' kleur""")

    with self.assertRaises(Exception) as context:
      result = hedy.transpile(code, self.level)

    self.assertEqual('Unquoted Text', context.exception.args[0])  # hier moet nog we een andere foutmelding komen!



  def test_transpile_missing_opening_quote(self):
    code = textwrap.dedent("""\
      print hallo wereld'""")

    with self.assertRaises(Exception) as context:
      result = hedy.transpile(code, self.level)

    self.assertEqual('Unquoted Text', context.exception.args[0])


  def test_transpile_missing_all_quotes(self):
    max_level = 5

    code = textwrap.dedent("""\
      print hallo wereld""")
    
    for level in range(self.level, max_level+1):

      with self.assertRaises(Exception) as context:
        result = hedy.transpile(code, level)

      self.assertEqual('Var Undefined', context.exception.args[0])

      print(f'{self.test_name()} level {level}')



  def test_transpile_issue_375(self):
    code = textwrap.dedent("""
      is Foobar
      print welcome""")

    with self.assertRaises(Exception) as context:
      result = hedy.transpile(code, self.level)

    self.assertEqual('Parse', context.exception.args[0])

  def test_two_spaces_after_print(self):

    max_level = 10
    code = "print        'hallo!'"

    for level in range(self.level, max_level+1):
      result = hedy.transpile(code, level)

      expected = textwrap.dedent("""\
      print('hallo!')""")

      print(f'{self.test_name()} level {level}')
      self.assertEqual(expected, result.code)
      self.assertEqual(False, result.has_turtle)


  def test_bengali_assign(self):
    hashed_var = hedy.hash_var("নাম")

    code = textwrap.dedent("""\
    নাম is হেডি""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent(f"""\
    {hashed_var} = 'হেডি'""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_bengali_assign_and_use(self):
    hashed_var = hedy.hash_var("নাম")

    code = textwrap.dedent("""\
    নাম is হেডি
    print 'আমার নাম is ' নাম """)

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent(f"""\
    {hashed_var} = 'হেডি'
    print('আমার নাম is '+{hashed_var})""")

    self.assertEqual(expected, result.code)

  def test_chinese_assign_and_use(self):
    hashed_var = hedy.hash_var("你好世界")

    code = textwrap.dedent("""\
    你好世界 is 你好世界
    print 你好世界""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent(f"""\
    {hashed_var} = '你好世界'
    print({hashed_var})""")

    self.assertEqual(expected, result.code)
















