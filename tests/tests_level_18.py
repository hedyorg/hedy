import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel18(HedyTester):
    level = 18

    def test_whileloop(self):
        code = textwrap.dedent("""\
        goedantwoord is False
        while goedantwoord is False:
            antwoord is input('Wat is 5 keer 5?')
            if antwoord is 25:
                goedantwoord is True""")
        expected = textwrap.dedent("""\
        goedantwoord = False
        while goedantwoord == False:
          antwoord = input('Wat is 5 keer 5?')
          if str(antwoord) == str('25'):
            goedantwoord = True""")

        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_whileloop2(self):
        code = textwrap.dedent("""\
        tel is 1
        # we gaan door totdat tel 3 is!
        while tel < 3:
            print('Dit is de ' tel 'e keer')
            tel is tel + 1
        print('We zijn klaar')""")
        expected = textwrap.dedent("""\
        tel = '1'
        # [' we gaan door totdat tel 3 is!']
        while int(tel) < int('3'):
          print(f'Dit is de {tel}e keer')
          tel = int(tel) + int(1)
        print(f'We zijn klaar')""")

        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_whileloop3(self):
        code = textwrap.dedent("""\
        goedantwoord is False
        # we gaan door totdat een goed antwoord is gegeven!
        while goedantwoord is False:
            antwoord is input('Wat is 5 keer 5?')
            if antwoord is 25:
                goedantwoord is True
                print('Er is een goed antwoord gegeven')""")
        expected = textwrap.dedent("""\
        goedantwoord = False
        # [' we gaan door totdat een goed antwoord is gegeven!']
        while goedantwoord == False:
          antwoord = input('Wat is 5 keer 5?')
          if str(antwoord) == str('25'):
            goedantwoord = True
            print(f'Er is een goed antwoord gegeven')""")

        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )

