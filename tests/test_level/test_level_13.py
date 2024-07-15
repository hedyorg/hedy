
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
        expected = self.dedent(
            self.input_transpiled('naam', 'hoe heet jij?'),
            self.input_transpiled('leeftijd', 'hoe oud ben jij?'),
            """\
            if naam.data == 'Felienne' and leeftijd.data == 37:
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

        expected = self.dedent(
            self.input_transpiled('name', 'what is your name?'),
            self.input_transpiled('age', 'what is your age?'),
            """\
            if name.data == 'Hedy' and age.data == 2:
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
            if 5 == 5 or 4 == 4:
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
          m = V('simple_function_1 - 2')
          print(f'''{m.text()}''')
        def simple_function_2(param):
          print(f'''simple_function_2 - 1''')
          print(f'''{param.text()}''')
        def simple_function_3(param_a, param_b, param_c):
          if param_a.data == 'A' or param_a.data == 'B':
            print(f'''simple_function_3 - 1''')
            print(f'''{param_b.text()}''')
          else:
            print(f'''simple_function_3 - 2''')
            if param_a.data == 'B' and param_b.data == 'test1':
              print(f'''simple_function_3 - 2A''')
              print(f'''{param_b.text()}''')
            else:
              print(f'''simple_function_3 - 2B''')
              print(f'''{param_c.text()}''')
        a = V('test1')
        simple_function_3(V('A'), a, V(1.0, num_sys='Latin'))
        simple_function_3(V('B'), a, V(1.0, num_sys='Latin'))
        simple_function_3(V('C'), a, V(1.0, num_sys='Latin'))
        simple_function_3(V('C'), V(3 + 3, num_sys='Latin'), V(1.0, num_sys='Latin'))""")

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
            unused_allowed=True,
            max_level=16,
            skip_faulty=False
        )
