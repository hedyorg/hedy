
import hedy
import textwrap
from test_level_01 import HedyTester

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

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  # new calculations
  def test_int_addition_directly(self):
    code = textwrap.dedent("""\
            print 2 + 2""")
    expected = textwrap.dedent("""\
            print(f'{2 + 2}')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  def test_float_addition_directly(self):
    code = textwrap.dedent("""\
            print 2.5 + 2.5""")
    expected = textwrap.dedent("""\
            print(f'{2.5 + 2.5}')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  def test_float_addition_with_string(self):
    code = textwrap.dedent("""\
            print 'het antwoord is ' 2.5 + 2.5""")
    expected = textwrap.dedent("""\
            print(f'het antwoord is {2.5 + 2.5}')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  def test_float_addition_in_var(self):
    code = textwrap.dedent("""\
            antwoord is 2.5 + 2.5
            print antwoord
            """)
    expected = textwrap.dedent("""\
            antwoord = 2.5 + 2.5
            print(f'{antwoord}')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

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

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

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

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  def test_add_string_vars(self):
    code = textwrap.dedent("""\
            getal1 is '5'
            getal2 is '6'
            print 'dat is dan: ' getal1 + getal2""")
    expected = textwrap.dedent("""\
            getal1 = '5'
            getal2 = '6'
            print(f'dat is dan: {getal1 + getal2}')""")

    check_output = (lambda x: HedyTester.run_code(x) == 'dat is dan: 56')

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=check_output,
      test_name=self.name()
    )

  def test_add_int_vars(self):
    code = textwrap.dedent("""\
            getal1 is 5
            getal2 is 6
            print 'dat is dan: ' getal1 + getal2""")
    expected = textwrap.dedent("""\
            getal1 = 5
            getal2 = 6
            print(f'dat is dan: {getal1 + getal2}')""")

    check_output = (lambda x: HedyTester.run_code(x) == 'dat is dan: 11')

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=check_output,
      test_name=self.name()
    )

  def test_assign_string_with_quotes(self):
    code = textwrap.dedent("""\
            name is 'felienne'
            print name""")
    expected = textwrap.dedent("""\
            name = 'felienne'
            print(f'{name}')""")
    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  def test_assign_string_with_quotes_and_string_value(self):
    code = textwrap.dedent("""\
            name is 'felienne'
            print 'hallo ' name""")
    expected = textwrap.dedent("""\
            name = 'felienne'
            print(f'hallo {name}')""")
    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  def test_print_multiple_calcs(self):
    code = textwrap.dedent("""\
            name is 1 + 2 + 3
            print name""")

    expected = textwrap.dedent("""\
            name = 1 + 2 + 3
            print(f'{name}')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  def test_calc_string_and_int(self):
    code = textwrap.dedent("""\
            x is 'test1'
            y is x + 1""")

    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException,
      test_name=self.name()
    )

  def test_print_chained_assignments(self):
    code = textwrap.dedent("""\
            x is 1 + 2
            y is x + 3
            print y + 4""")

    expected = textwrap.dedent("""\
            x = 1 + 2
            y = x + 3
            print(f'{y + 4}')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  def test_assign_calc(self):
    code = textwrap.dedent("""\
            var is 5
            print var + 5""")

    expected = textwrap.dedent("""\
            var = 5
            print(f'{var + 5}')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  def test_access_variable_before_definition(self):
    code = textwrap.dedent("""\
            a is b
            b is 3
            print a""")

    expected = textwrap.dedent("""\
            a = b
            b = 3
            print(f'{a}')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  # negative tests
  def test_assign_string_without_quotes(self):
    code = textwrap.dedent("""\
            name is felienne
            print name""")

    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.UnquotedAssignTextException,
      test_name=self.name()
    )
  
  def test_list_creation(self):
    code = textwrap.dedent("""\
    animals is 'duck', 'dog', 'penguin'""")
    expected = textwrap.dedent("""\
    animals = ['duck', 'dog', 'penguin']""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_list_creation_with_spaces(self):
    code = textwrap.dedent("""\
    actions is 'clap your hands', 'stomp your feet', 'shout Hurray'
    for action in actions
        for i in range 1 to 2
            print 'if youre happy and you know it'
            print action
        print 'if youre happy and you know it and you really want to show it'
        print 'if youre happy and you know it'
        print action""")
    expected = textwrap.dedent("""\
    actions = ['clap your hands', 'stomp your feet', 'shout Hurray']
    for action in actions:
      step = 1 if int(1) < int(2) else -1
      for i in range(int(1), int(2) + step, step):
        print(f'if youre happy and you know it')
        print(f'{action}')
      print(f'if youre happy and you know it and you really want to show it')
      print(f'if youre happy and you know it')
      print(f'{action}')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_list_creation_with_numbers(self):
    code = textwrap.dedent("""\
    getallen is 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    getal is getallen at random""")
    expected = textwrap.dedent("""\
    getallen = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    getal=random.choice(getallen)""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

