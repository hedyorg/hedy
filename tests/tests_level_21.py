import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel21(HedyTester):
    level = 21

    def test_sum_in_if(self):
        code = textwrap.dedent("""\
    if 5+3 == 8:
        print('5+3 is inderdaad 8')
    else:
        print('Dit wordt niet geprint want 5+3 is 8!')""")
        expected = textwrap.dedent("""\
    if int(5) + int(3) == int(8):
      print(f'5+3 is inderdaad 8')
    else:
      print(f'Dit wordt niet geprint want 5+3 is 8!')""")

        self.multi_level_tester(
          
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_sum_in_right_side_if(self):
        code = textwrap.dedent("""\
    if 8 == 5+3:
        print('5+3 is inderdaad 8')
    else:
        print('Dit wordt niet geprint want 5+3 is 8!')""")
        expected = textwrap.dedent("""\
    if int(8) == int(5) + int(3):
      print(f'5+3 is inderdaad 8')
    else:
      print(f'Dit wordt niet geprint want 5+3 is 8!')""")

        self.multi_level_tester(
          
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_min_in_if(self):
        code = textwrap.dedent("""\
    if 5-3 == 2:
        print('5-3 is inderdaad 2')
    else:
        print('Dit wordt niet geprint want 5+3 is 8!')""")
        expected = textwrap.dedent("""\
    if int(5) - int(3) == int(2):
      print(f'5-3 is inderdaad 2')
    else:
      print(f'Dit wordt niet geprint want 5+3 is 8!')""")

        self.multi_level_tester(
          
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_multiply_in_if(self):
        code = textwrap.dedent("""\
    if 5*3 == 15:
        print('5*3 is inderdaad 15')
    else:
        print('Dit wordt niet geprint want 5+3 is 8!')""")
        expected = textwrap.dedent("""\
    if int(5) * int(3) == int(15):
      print(f'5*3 is inderdaad 15')
    else:
      print(f'Dit wordt niet geprint want 5+3 is 8!')""")

        self.multi_level_tester(
          
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_print_brackets(self):
        code = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        print('Dus jij hebt zo veel verjaardagen gehad:')
        for i in range(0,leeftijd):
            print(i)""")
        expected = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        print(f'Dus jij hebt zo veel verjaardagen gehad:')
        step = 1 if int(0) < int(leeftijd) else -1
        for i in range(int(0), int(leeftijd) + step, step):
          print(f'{i}')""")

        self.multi_level_tester(
          
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_print_var_brackets(self):
        code = "naam = Hedy\nprint('ik heet' naam)"
        expected = "naam = 'Hedy'\nprint(f'ik heet{naam}')"

        self.multi_level_tester(
          max_level=18,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_if_nesting(self):
        code = textwrap.dedent("""\
        kleur = blauw
        kleurtwee = geel
        if kleur == blauw:
          if kleurtwee == geel:
            print('Samen is dit groen!')""")
        expected = textwrap.dedent("""\
        kleur = 'blauw'
        kleurtwee = 'geel'
        if str(kleur) == str('blauw'):
          if str(kleurtwee) == str('geel'):
            print(f'Samen is dit groen!')""")

        self.multi_level_tester(
          
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )

    # negative tests
    def test_var_undefined_error_message(self):
      code = textwrap.dedent("""\
        naam = Hedy
        print('ik heet ' name)""")

      self.multi_level_tester(
        code=code,
        exception=hedy.UndefinedVarException,
        max_level=self.max_Hedy_level,
        test_name=self.name()
      )

      # deze extra check functie kan nu niet mee omdat die altijd op result werkt
      # evt toch splitsen in 2 (pos en neg?)
      # self.assertEqual('name', context.exception.arguments['name'])