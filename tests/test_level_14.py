import exceptions
import hedy
import textwrap
from parameterized import parameterized
from test_level_01 import HedyTester

class TestsLevel14(HedyTester):
  level = 14


  @parameterized.expand(HedyTester.comparison_commands)
  def test_comparisons_with_int(self, comparison):
    code = textwrap.dedent(f"""\
      leeftijd is ask 'Hoe oud ben jij?'
      if leeftijd {comparison} 12
          print 'Dan ben je jonger dan ik!'""")
    expected = textwrap.dedent(f"""\
      leeftijd = input(f'Hoe oud ben jij?')
      try:
        leeftijd = int(leeftijd)
      except ValueError:
        try:
          leeftijd = float(leeftijd)
        except ValueError:
          pass
      if str(leeftijd).zfill(100){comparison}str(12).zfill(100):
        print(f'Dan ben je jonger dan ik!')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected,
    )

  def test_inequality_with_string(self):
    code = textwrap.dedent(f"""\
      name is ask 'What is your name?'
      if name != 'Hedy'
          print 'meh'""")
    expected = textwrap.dedent(f"""\
      name = input(f'What is your name?')
      try:
        name = int(name)
      except ValueError:
        try:
          name = float(name)
        except ValueError:
          pass
      if str(name).zfill(100)!='Hedy'.zfill(100):
        print(f'meh')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected,
    )

  def test_inequality_Hindi(self):
    code = textwrap.dedent(f"""\
    उम्र is ask 'आप कितने साल के हैं?'
    if उम्र > 12
        print 'आप मुझसे छोटे हैं!'
    else
        print 'आप मुझसे बड़े हैं!'""")
    expected = textwrap.dedent(f"""\
      v6cdeb9dc4e33aa47ac927755899137f2 = input(f'आप कितने साल के हैं?')
      try:
        v6cdeb9dc4e33aa47ac927755899137f2 = int(v6cdeb9dc4e33aa47ac927755899137f2)
      except ValueError:
        try:
          v6cdeb9dc4e33aa47ac927755899137f2 = float(v6cdeb9dc4e33aa47ac927755899137f2)
        except ValueError:
          pass
      if str(v6cdeb9dc4e33aa47ac927755899137f2).zfill(100)>str(12).zfill(100):
        print(f'आप मुझसे छोटे हैं!')
      else:
        print(f'आप मुझसे बड़े हैं!')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected,
    )



  @parameterized.expand(HedyTester.equality_comparison_commands)
  def test_equality_with_string(self, comparison):
    code = textwrap.dedent(f"""\
      name is ask 'What is your name?'
      if name {comparison} 'Hedy'
          print 'meh'""")
    expected = textwrap.dedent(f"""\
      name = input(f'What is your name?')
      try:
        name = int(name)
      except ValueError:
        try:
          name = float(name)
        except ValueError:
          pass
      if str(name) == str('Hedy'):
        print(f'meh')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected,
    )

  @parameterized.expand(HedyTester.comparison_commands)
  def test_comparisons_else(self, comparison):
    code = textwrap.dedent(f"""\
      leeftijd is ask 'Hoe oud ben jij?'
      if leeftijd {comparison} 12
          print 'Dan ben je jonger dan ik!'
      else
          print 'Dan ben je ouder dan ik!'""")
    expected = textwrap.dedent(f"""\
      leeftijd = input(f'Hoe oud ben jij?')
      try:
        leeftijd = int(leeftijd)
      except ValueError:
        try:
          leeftijd = float(leeftijd)
        except ValueError:
          pass
      if str(leeftijd).zfill(100){comparison}str(12).zfill(100):
        print(f'Dan ben je jonger dan ik!')
      else:
        print(f'Dan ben je ouder dan ik!')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected
    )

  @parameterized.expand(HedyTester.comparison_commands)
  def tests_smaller_no_spaces(self, comparison):
    code = textwrap.dedent(f"""\
    leeftijd is ask 'Hoe oud ben jij?'
    if leeftijd {comparison} 12
        print 'Dan ben je jonger dan ik!'""")
    expected = textwrap.dedent(f"""\
    leeftijd = input(f'Hoe oud ben jij?')
    try:
      leeftijd = int(leeftijd)
    except ValueError:
      try:
        leeftijd = float(leeftijd)
      except ValueError:
        pass
    if str(leeftijd).zfill(100){comparison}str(12).zfill(100):
      print(f'Dan ben je jonger dan ik!')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected
    )

  @parameterized.expand(HedyTester.number_comparison_commands)
  def test_comparison_with_string_gives_type_error(self, comparison):
    code = textwrap.dedent(f"""\
      a is 'text'
      if a {comparison} 12
          b is 1""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )


  @parameterized.expand(HedyTester.number_comparison_commands)
  def test_comparison_with_list_gives_type_error(self, comparison):
    code = textwrap.dedent(f"""\
      a is 1, 2, 3
      if a {comparison} 12
          b is 1""")

    self.multi_level_tester(
      code=code,
      max_level=15,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_not_equal_promotes_int_to_float(self):
    code = textwrap.dedent(f"""\
      a is 1
      b is 1.2
      if a != b
          b is 1""")

    expected = textwrap.dedent(f"""\
      a = 1
      b = 1.2
      if str(a).zfill(100)!=str(b).zfill(100):
        b = 1""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected
    )

  @parameterized.expand([
    ('"text"', "'text'"),
    ("'text'", "'text'"),
    ('1', '1'),
    ('1.3', '1.3'),
    ('1, 2', '[1, 2]')])
  def test_not_equal(self, arg, exp):
    code = textwrap.dedent(f"""\
      a is {arg}
      b is {arg}
      if a != b
          b is 1""")

    expected = textwrap.dedent(f"""\
      a = {exp}
      b = {exp}
      if str(a).zfill(100)!=str(b).zfill(100):
        b = 1""")

    self.multi_level_tester(
      code=code,
      max_level=15,
      expected=expected
    )

  def test_if_with_double_equals(self):
    code = textwrap.dedent("""\
    naam = 'Hedy'
    if naam == Hedy
        print 'koekoek'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=16)

  @parameterized.expand(HedyTester.equality_comparison_commands)
  def test_equality_with_lists(self, comparison):
    code = textwrap.dedent(f"""\
    a = 1, 2
    b = 1, 2
    if a {comparison} b
        sleep""")

    expected = textwrap.dedent(f"""\
    a = [1, 2]
    b = [1, 2]
    if str(a) == str(b):
      time.sleep(1)""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=15)

  def test_inequality_with_lists(self):
    code = textwrap.dedent("""\
    a = 1, 2
    b = 1, 2
    if a != b
        sleep""")

    expected = textwrap.dedent("""\
    a = [1, 2]
    b = [1, 2]
    if str(a).zfill(100)!=str(b).zfill(100):
      time.sleep(1)""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=15)

  @parameterized.expand(HedyTester.comparison_commands)
  def test_comparisons_with_boolean(self, comparison):
    code = textwrap.dedent(f"""\
      leeftijd is ask 'Hoe oud ben jij?'
      if leeftijd {comparison} 12 or leeftijd {comparison} 15
          print 'Dan ben je jonger dan ik!'
      if leeftijd {comparison} 12 and leeftijd {comparison} 15
          print 'Some other string!'""")
      
    expected = textwrap.dedent(f"""\
      leeftijd = input(f'Hoe oud ben jij?')
      try:
        leeftijd = int(leeftijd)
      except ValueError:
        try:
          leeftijd = float(leeftijd)
        except ValueError:
          pass
      if str(leeftijd).zfill(100){comparison}str(12).zfill(100) or str(leeftijd).zfill(100){comparison}str(15).zfill(100):
        print(f'Dan ben je jonger dan ik!')
      if str(leeftijd).zfill(100){comparison}str(12).zfill(100) and str(leeftijd).zfill(100){comparison}str(15).zfill(100):
        print(f'Some other string!')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected,
    )

  @parameterized.expand([
    ('"text"', '1'),      # double-quoted text and number
    ("'text'", '1'),      # single-quoted text and number
    ('1, 2', '1'),        # list and number
    ('1, 2', "'text'"),   # list and single-quoted text
    ('1, 2', '"text"')])  # list and double-quoted text
  def test_not_equal_with_diff_types_gives_error(self, left, right):
    code = textwrap.dedent(f"""\
      a is {left}
      b is {right}
      if a != b
          b is 1""")

    self.multi_level_tester(
      code=code,
      max_level=15,
      exception=exceptions.InvalidTypeCombinationException
    )


