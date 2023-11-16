
import textwrap

from tests.Tester import HedyTester


class TestsLevel13(HedyTester):
    level = 13

    def test_and(self):
        code = textwrap.dedent("""\
      naam is ask 'hoe heet jij?'
      leeftijd is ask 'hoe oud ben jij?'
      if naam is 'Felienne' and leeftijd is 37
          print 'hallo jij!'""")
        expected = textwrap.dedent("""\
      naam = input(f'''hoe heet jij?''')
      try:
        naam = int(naam)
      except ValueError:
        try:
          naam = float(naam)
        except ValueError:
          pass
      leeftijd = input(f'''hoe oud ben jij?''')
      try:
        leeftijd = int(leeftijd)
      except ValueError:
        try:
          leeftijd = float(leeftijd)
        except ValueError:
          pass
      if convert_numerals('Latin', naam) == convert_numerals('Latin', 'Felienne') and convert_numerals('Latin', leeftijd) == convert_numerals('Latin', '37'):
        print(f'''hallo jij!''')""")

        self.multi_level_tester(
            max_level=16,
            code=code,
            expected=expected
        )

    def test_equals(self):
        code = textwrap.dedent("""\
    name = ask 'what is your name?'
    age = ask 'what is your age?'
    if name is 'Hedy' and age is 2
        print 'You are the real Hedy!'""")

        expected = textwrap.dedent("""\
      name = input(f'''what is your name?''')
      try:
        name = int(name)
      except ValueError:
        try:
          name = float(name)
        except ValueError:
          pass
      age = input(f'''what is your age?''')
      try:
        age = int(age)
      except ValueError:
        try:
          age = float(age)
        except ValueError:
          pass
      if convert_numerals('Latin', name) == convert_numerals('Latin', 'Hedy') and convert_numerals('Latin', age) == convert_numerals('Latin', '2'):
        print(f'''You are the real Hedy!''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
            expected_commands=['ask', 'ask', 'if', 'and', 'print']
        )

    def test_or(self):
        code = textwrap.dedent("""\
      if 5 is 5 or 4 is 4
          print 'hallo'""")
        expected = textwrap.dedent("""\
      if convert_numerals('Latin', '5') == convert_numerals('Latin', '5') or convert_numerals('Latin', '4') == convert_numerals('Latin', '4'):
        print(f'''hallo''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
            expected_commands=['if', 'or', 'print']
        )

    def test_simple_function(self):
        code = textwrap.dedent("""\
        define simple_function_1 with parameter
            print "simple_function_1 - 1"
            m = "simple_function_1 - 2"
            print m
        define simple_function_2 with param
            print "simple_function_2 - 1"
            print param
        define simple_function_3 with param_a, param_b, param_c
            if param_a = "A" or param_a = "B"
                print "simple_function_3 - 1"
                print param_b
            else
                print "simple_function_3 - 2"
                if param_a = "B" and param_b = "test1"
                    print "simple_function_3 - 2A"
                    print param_b
                else
                    print "simple_function_3 - 2B"
                    print param_c
        a = "test1"
        call simple_function_3 with "A", a, 1.0
        call simple_function_3 with "B", a, 1.0
        call simple_function_3 with "C", a, 1.0
        call simple_function_3 with "C", 3 + 3, 1.0""")

        expected = textwrap.dedent("""\
        def simple_function_1(parameter):
          print(f'''simple_function_1 - 1''')
          m = 'simple_function_1 - 2'
          print(f'''{m}''')
        def simple_function_2(param):
          print(f'''simple_function_2 - 1''')
          print(f'''{param}''')
        def simple_function_3(param_a, param_b, param_c):
          if convert_numerals('Latin', param_a) == convert_numerals('Latin', 'A') or convert_numerals('Latin', param_a) == convert_numerals('Latin', 'B'):
            print(f'''simple_function_3 - 1''')
            print(f'''{param_b}''')
          else:
            print(f'''simple_function_3 - 2''')
            if convert_numerals('Latin', param_a) == convert_numerals('Latin', 'B') and convert_numerals('Latin', param_b) == convert_numerals('Latin', 'test1'):
              print(f'''simple_function_3 - 2A''')
              print(f'''{param_b}''')
            else:
              print(f'''simple_function_3 - 2B''')
              print(f'''{param_c}''')
        a = 'test1'
        simple_function_3('A', a, 1.0)
        simple_function_3('B', a, 1.0)
        simple_function_3('C', a, 1.0)
        simple_function_3('C', 3 + 3, 1.0)""")

        output = textwrap.dedent("""\
        simple_function_3 - 1
        test1
        simple_function_3 - 1
        test1
        simple_function_3 - 2
        simple_function_3 - 2B
        1.0
        simple_function_3 - 2
        simple_function_3 - 2B
        1.0""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output=output,
            max_level=16
        )
