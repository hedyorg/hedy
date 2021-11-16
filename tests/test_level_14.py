import textwrap
from test_level_01 import HedyTester


class TestsLevel14(HedyTester):
    level = 14

    def tests_smaller(self):
        code = textwrap.dedent("""\
        leeftijd is ask 'Hoe oud ben jij?'
        if leeftijd < 12
          print 'Dan ben je jonger dan ik!'""")
        expected = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        try:
          leeftijd = int(leeftijd)
        except ValueError:
          try:
            leeftijd = float(leeftijd)
          except ValueError:
            pass
        if str(leeftijd).zfill(100)<str(12).zfill(100):
          print(f'Dan ben je jonger dan ik!')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            test_name=self.name()
        )

    def tests_bigger(self):
        code = textwrap.dedent("""\
        leeftijd is ask 'Hoe oud ben jij?'
        if leeftijd > 12
          print 'Dan ben je ouder dan ik!'""")
        expected = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        try:
          leeftijd = int(leeftijd)
        except ValueError:
          try:
            leeftijd = float(leeftijd)
          except ValueError:
            pass
        if str(leeftijd).zfill(100)>str(12).zfill(100):
          print(f'Dan ben je ouder dan ik!')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            test_name=self.name()
        )

    def tests_smaller_else(self):
        code = textwrap.dedent("""\
        leeftijd is ask 'Hoe oud ben jij?'
        if leeftijd < 12
            print 'Dan ben je jonger dan ik!'
        else
            print 'Dan ben je ouder dan ik!'""")
        expected = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        try:
          leeftijd = int(leeftijd)
        except ValueError:
          try:
            leeftijd = float(leeftijd)
          except ValueError:
            pass
        if str(leeftijd).zfill(100)<str(12).zfill(100):
          print(f'Dan ben je jonger dan ik!')
        else:
          print(f'Dan ben je ouder dan ik!')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            test_name=self.name()
        )

    def test_not_equal(self):
        code = textwrap.dedent("""\
        land is ask 'In welk land woon jij?'
        if land != Nederland
            print 'Cool!'
        else
            print 'Ik kom ook uit Nederland!'""")
        expected = textwrap.dedent("""\
        land = input('In welk land woon jij?')
        try:
          land = int(land)
        except ValueError:
          try:
            land = float(land)
          except ValueError:
            pass
        if str(land).zfill(100)!='Nederland'.zfill(100):
          print(f'Cool!')
        else:
          print(f'Ik kom ook uit Nederland!')""")
        self.multi_level_tester(

            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            test_name=self.name()
        )

    def tests_smaller_equal(self):
        code = textwrap.dedent("""\
        leeftijd is ask 'Hoe oud ben jij?'
        if leeftijd <= 12
            print 'Dan ben je jonger dan ik!'""")
        expected = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        try:
          leeftijd = int(leeftijd)
        except ValueError:
          try:
            leeftijd = float(leeftijd)
          except ValueError:
            pass
        if str(leeftijd).zfill(100)<=str(12).zfill(100):
          print(f'Dan ben je jonger dan ik!')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            test_name=self.name()
        )

    def tests_bigger_equal(self):
        code = textwrap.dedent("""\
        leeftijd is ask 'Hoe oud ben jij?'
        if leeftijd >= 12
            print 'Dan ben je ouder dan ik!'""")
        expected = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        try:
          leeftijd = int(leeftijd)
        except ValueError:
          try:
            leeftijd = float(leeftijd)
          except ValueError:
            pass
        if str(leeftijd).zfill(100)>=str(12).zfill(100):
          print(f'Dan ben je ouder dan ik!')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            test_name=self.name()
        )

    def tests_smaller_equal_else(self):
        code = textwrap.dedent("""\
        leeftijd is ask 'Hoe oud ben jij?'
        if leeftijd <= 12
            print 'Dan ben je jonger dan ik!'
        else
            print 'Dan ben je ouder dan ik!'""")
        expected = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        try:
          leeftijd = int(leeftijd)
        except ValueError:
          try:
            leeftijd = float(leeftijd)
          except ValueError:
            pass
        if str(leeftijd).zfill(100)<=str(12).zfill(100):
          print(f'Dan ben je jonger dan ik!')
        else:
          print(f'Dan ben je ouder dan ik!')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_not_turtle(),
            test_name=self.name()
        )
