import textwrap

from parameterized import parameterized

import exceptions
import hedy
from tests.Tester import HedyTester


class TestsLevel14(HedyTester):
    level = 14

    @parameterized.expand(str(i) for i in range(10, 700, 10))
    def test_greater_than_with_int_and_float(self, a):
        b = 7.0
        code = textwrap.dedent(f"""\
        var = {a}
        if var > {b}
          print 'Above {b}'
        else
          print 'Below'""")
        expected = textwrap.dedent(f"""\
        var = {a}
        if convert_numerals('Latin', var)>convert_numerals('Latin', {b}):
          print(f'''Above {b}''')
        else:
          print(f'''Below''')""")
        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
            output=f'Above {b}',
        )

    @parameterized.expand(str(float(i)) for i in range(2, 16))
    def test_not_greater_than_with_int_and_float(self, a):
        b = 15
        code = textwrap.dedent(f"""\
        var = {a}
        if var > {b}
          print 'Above {b}'
        else
          print 'Below'""")
        expected = textwrap.dedent(f"""\
        var = {a}
        if convert_numerals('Latin', var)>convert_numerals('Latin', {b}):
          print(f'''Above {b}''')
        else:
          print(f'''Below''')""")
        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=16,
            output='Below',
        )

    @parameterized.expand(HedyTester.comparison_commands)
    def test_comparisons_with_int(self, comparison):
        code = textwrap.dedent(f"""\
      leeftijd is ask 'Hoe oud ben jij?'
      if leeftijd {comparison} 12
          print 'Dan ben je jonger dan ik!'""")
        expected = textwrap.dedent(f"""\
      leeftijd = input(f'''Hoe oud ben jij?''')
      try:
        leeftijd = int(leeftijd)
      except ValueError:
        try:
          leeftijd = float(leeftijd)
        except ValueError:
          pass
      if convert_numerals('Latin', leeftijd){comparison}convert_numerals('Latin', 12):
        print(f'''Dan ben je jonger dan ik!''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
        )

    def test_equality_arabic(self):
        code = textwrap.dedent("""\
      nummer1 is ٢
      nummer2 is 2
      if nummer1 != nummer2
          print 'jahoor!'
      else
          print 'neejoh!'""")

        expected = textwrap.dedent("""\
      nummer1 = 2
      nummer2 = 2
      if convert_numerals('Latin', nummer1)!=convert_numerals('Latin', nummer2):
        print(f'''jahoor!''')
      else:
        print(f'''neejoh!''')""")

        self.multi_level_tester(
            max_level=16,
            code=code,
            expected=expected,
            output='neejoh!')

    def test_inequality_with_string(self):
        code = textwrap.dedent(f"""\
      name is ask 'What is your name?'
      if name != 'Hedy'
          print 'meh'""")
        expected = textwrap.dedent(f"""\
      name = input(f'''What is your name?''')
      try:
        name = int(name)
      except ValueError:
        try:
          name = float(name)
        except ValueError:
          pass
      if convert_numerals('Latin', name)!='Hedy':
        print(f'''meh''')""")

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
      उम्र = input(f'''आप कितने साल के हैं?''')
      try:
        उम्र = int(उम्र)
      except ValueError:
        try:
          उम्र = float(उम्र)
        except ValueError:
          pass
      if convert_numerals('Latin', उम्र)>convert_numerals('Latin', 12):
        print(f'''आप मुझसे छोटे हैं!''')
      else:
        print(f'''आप मुझसे बड़े हैं!''')""")

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
      name = input(f'''What is your name?''')
      try:
        name = int(name)
      except ValueError:
        try:
          name = float(name)
        except ValueError:
          pass
      if convert_numerals('Latin', name) == convert_numerals('Latin', 'Hedy'):
        print(f'''meh''')""")

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
      leeftijd = input(f'''Hoe oud ben jij?''')
      try:
        leeftijd = int(leeftijd)
      except ValueError:
        try:
          leeftijd = float(leeftijd)
        except ValueError:
          pass
      if convert_numerals('Latin', leeftijd){comparison}convert_numerals('Latin', 12):
        print(f'''Dan ben je jonger dan ik!''')
      else:
        print(f'''Dan ben je ouder dan ik!''')""")

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
    leeftijd = input(f'''Hoe oud ben jij?''')
    try:
      leeftijd = int(leeftijd)
    except ValueError:
      try:
        leeftijd = float(leeftijd)
      except ValueError:
        pass
    if convert_numerals('Latin', leeftijd){comparison}convert_numerals('Latin', 12):
      print(f'''Dan ben je jonger dan ik!''')""")

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
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
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
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
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
      if convert_numerals('Latin', a)!=convert_numerals('Latin', b):
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
      if convert_numerals('Latin', a)!=convert_numerals('Latin', b):
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
    if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Hedy'):
      print(f'''koekoek''')""")

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
    if convert_numerals('Latin', a) == convert_numerals('Latin', b):
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
    if convert_numerals('Latin', a)!=convert_numerals('Latin', b):
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
      leeftijd = input(f'''Hoe oud ben jij?''')
      try:
        leeftijd = int(leeftijd)
      except ValueError:
        try:
          leeftijd = float(leeftijd)
        except ValueError:
          pass
      if convert_numerals('Latin', leeftijd){comparison}convert_numerals('Latin', 12)\
 or convert_numerals('Latin', leeftijd){comparison}convert_numerals('Latin', 15):
        print(f'''Dan ben je jonger dan ik!''')
      if convert_numerals('Latin', leeftijd){comparison}convert_numerals('Latin', 12)\
 and convert_numerals('Latin', leeftijd){comparison}convert_numerals('Latin', 15):
        print(f'''Some other string!''')""")

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
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=exceptions.InvalidTypeCombinationException
        )

    def test_missing_indent_else(self):
        code = textwrap.dedent(f"""\
      age = ask 'How old are you?'
      if age < 13
          print 'You are younger than me!'
      else
      print 'You are older than me!'""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            exception=exceptions.NoIndentationException
        )

    def test_simple_function(self):
        code = textwrap.dedent(f"""\
        define test_function_1
            int = 1
            return "Test function " int
        define test_function_2 with int
            return "Test function " int
        define test_function_3 with input
            if input != 5
                print "NE5"
            if input < 5
                print "LT5"
            if input <= 5
                print "LTE5"
            if input > 5
                print "GT5"
            if input >= 5
                print "GTE5"
            if input = 5
                print "E5"
        print call test_function_1
        print call test_function_2 with 2
        m = 3
        print call test_function_2 with m
        print call test_function_2 with 4.0
        print call test_function_2 with "5"
        print call test_function_2 with 1.5 * 4
        print ""
        call test_function_3 with 4
        print ""
        call test_function_3 with 5
        print ""
        call test_function_3 with 6""")

        expected = self.dedent(
            """\
            def test_function_1():
              _int = 1""",
            (self.return_transpiled(f"Test function {{_int}}"), '  '),
            "def test_function_2(_int):",
            (self.return_transpiled(f"Test function {{_int}}"), '  '),
            f"""\
            def test_function_3(_input):
              if convert_numerals('Latin', _input)!=convert_numerals('Latin', 5):
                print(f'''NE5''')
              if convert_numerals('Latin', _input)<convert_numerals('Latin', 5):
                print(f'''LT5''')
              if convert_numerals('Latin', _input)<=convert_numerals('Latin', 5):
                print(f'''LTE5''')
              if convert_numerals('Latin', _input)>convert_numerals('Latin', 5):
                print(f'''GT5''')
              if convert_numerals('Latin', _input)>=convert_numerals('Latin', 5):
                print(f'''GTE5''')
              if convert_numerals('Latin', _input) == convert_numerals('Latin', '5'):
                print(f'''E5''')
            print(f'''{{test_function_1()}}''')
            print(f'''{{test_function_2(2)}}''')
            m = 3
            print(f'''{{test_function_2(m)}}''')
            print(f'''{{test_function_2(4.0)}}''')
            print(f'''{{test_function_2('5')}}''')
            print(f'''{{test_function_2({self.number_cast_transpiled('1.5')} * {self.number_cast_transpiled('4')})}}''')
            print(f'''''')
            test_function_3(4)
            print(f'''''')
            test_function_3(5)
            print(f'''''')
            test_function_3(6)""")

        output = textwrap.dedent("""\
        Test function 1
        Test function 2
        Test function 3
        Test function 4.0
        Test function 5
        Test function 6.0

        NE5
        LT5
        LTE5

        LTE5
        GTE5
        E5

        NE5
        GT5
        GTE5""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output=output,
            max_level=16
        )

    def test_source_map(self):
        code = textwrap.dedent("""\
        age = ask 'How old are you?'
        if age < 13
            print 'You are younger than me!'
        else
            print 'You are older than me!'""")

        excepted_code = textwrap.dedent("""\
        age = input(f'''How old are you?''')
        try:
          age = int(age)
        except ValueError:
          try:
            age = float(age)
          except ValueError:
            pass
        if convert_numerals('Latin', age)<convert_numerals('Latin', 13):
          print(f'''You are younger than me!''')
        else:
          print(f'''You are older than me!''')""")

        expected_source_map = {
            '1/1-1/4': '1/1-1/4',
            '1/1-1/29': '1/1-8/9',
            '2/4-2/7': '3/3-3/6',
            '2/4-2/12': '9/4-9/64',
            '3/5-3/37': '10/1-10/39',
            '2/1-3/46': '9/1-10/41',
            '5/5-5/35': '12/1-12/37',
            '3/46-5/44': '12/-248-3/3',
            '2/1-5/44': '9/1-12/39',
            '1/1-5/45': '1/1-12/39'
        }

        self.single_level_tester(code, expected=excepted_code)
        self.source_map_tester(code=code, expected_source_map=expected_source_map)
