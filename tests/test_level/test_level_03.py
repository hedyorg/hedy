import hedy
import textwrap
from tests.Tester import HedyTester


class TestsLevel3(HedyTester):
    level = 3
    '''
    Tests should be ordered as follows:
     * commands in the order of hedy.py e.g. for level 1: ['print', 'ask', 'echo', 'turn', 'forward']
     * combined tests
     * markup tests
     * negative tests

    Naming conventions are like this:
     * single keyword positive tests are just keyword or keyword_special_case
     * multi keyword positive tests are keyword1_keywords_2
     * negative tests should be situation_gives_exception
    '''

    #
    # print tests
    #

    # issue #745
    def test_print_list_gives_type_error(self):
        code = textwrap.dedent("""\
        plaatsen is een stad, een  dorp, een strand
        print plaatsen""")

        self.multi_level_tester(
            code=code,
            max_level=11,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_print_list_random(self):
        code = textwrap.dedent("""\
        dieren is Hond, Kat, Kangoeroe
        print dieren at random""")

        expected = textwrap.dedent("""\
        dieren = ['Hond', 'Kat', 'Kangoeroe']
        print(f'{random.choice(dieren)}')""")

        # check if result is in the expected list
        check_in_list = (lambda x: HedyTester.run_code(x) in ['Hond', 'Kat', 'Kangoeroe'])

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=check_in_list
        )

    def test_print_list_access_index(self):
        code = textwrap.dedent("""\
        dieren is Hond, Kat, Kangoeroe
        print dieren at 1""")

        expected = textwrap.dedent("""\
        dieren = ['Hond', 'Kat', 'Kangoeroe']
        print(f'{dieren[1-1]}')""")

        check_in_list = (lambda x: HedyTester.run_code(x) == 'Hond')

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=check_in_list
        )

    def test_print_list_random_fr(self):
        code = textwrap.dedent("""\
        animaux est chien, chat, kangourou
        affiche animaux au hasard""")

        expected = textwrap.dedent("""\
        animaux = ['chien', 'chat', 'kangourou']
        print(f'{random.choice(animaux)}')""")

        # check if result is in the expected list
        check_in_list = (lambda x: HedyTester.run_code(x) in ['chien', 'chat', 'kangourou'])

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=check_in_list,
            lang='fr'
        )

    #
    # ask tests
    #
    def test_ask_list_gives_type_error(self):
        code = textwrap.dedent("""\
        plaatsen is een stad, een  dorp, een strand
        var is ask plaatsen""")

        self.multi_level_tester(
            code=code,
            max_level=11,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    #
    # sleep tests
    #
    def test_sleep_with_list_access(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n at 1""")
        expected = HedyTester.dedent(
            "n = ['1', '2', '3']",
            HedyTester.sleep_command_transpiled("n[1-1]"))

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_sleep_with_list_random(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n at random""")
        expected = HedyTester.dedent(
            "n = ['1', '2', '3']",
            HedyTester.sleep_command_transpiled("random.choice(n)"))

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_sleep_with_list_gives_error(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n""")

        self.multi_level_tester(max_level=11, code=code, exception=hedy.exceptions.InvalidArgumentTypeException)

    #
    # is tests
    #
    def test_assign_var_to_var(self):
        code = textwrap.dedent("""\
        dier1 is hond
        dier2 is dier1
        print dier2""")

        expected = textwrap.dedent("""\
        dier1 = 'hond'
        dier2 = dier1
        print(f'{dier2}')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_assign_list(self):
        code = "dieren is Hond, Kat, Kangoeroe"
        expected = "dieren = ['Hond', 'Kat', 'Kangoeroe']"

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_assign_list_to_hungarian_var(self):
        code = textwrap.dedent("""\
        állatok is kutya, macska, kenguru
        print állatok at random""")

        expected = textwrap.dedent("""\
        v79de0191e90551f058d466c5e8c267ff = ['kutya', 'macska', 'kenguru']
        print(f'{random.choice(v79de0191e90551f058d466c5e8c267ff)}')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_assign_list_with_spaces(self):
        # spaces are parsed in the text here, that is fine (could be avoided if we say text
        # can't *end* (or start) in a space but I find this ok for now
        code = "dieren is Hond , Kat , Kangoeroe"
        expected = "dieren = ['Hond ', 'Kat ', 'Kangoeroe']"

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_assign_random_value(self):
        code = textwrap.dedent("""\
        dieren is hond, kat, kangoeroe
        dier is dieren at random
        print dier""")

        expected = textwrap.dedent("""\
        dieren = ['hond', 'kat', 'kangoeroe']
        dier = random.choice(dieren)
        print(f'{dier}')""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=self.result_in(['Hond', 'Kat', 'Kangoeroe'])
        )

    def test_assign_list_with_dutch_comma_arabic_lang(self):
        code = "صديقي هو احمد, خالد, حسن"
        expected = "vbd60ecd50ef1238a3f6a563bcfb1d331 = ['احمد', 'خالد', 'حسن']"

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            lang='ar',
            # translation must be off because the Latin commas will be converted to arabic commas and this is correct
            translate=False
        )

    def test_assign_list_with_arabic_comma_and_is(self):
        code = "animals هو cat، dog، platypus"
        expected = "animals = ['cat', 'dog', 'platypus']"

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            lang='ar'
        )

    def test_assign_list_with_arabic_comma(self):
        code = "صديقي هو احمد، خالد، حسن"
        expected = "vbd60ecd50ef1238a3f6a563bcfb1d331 = ['احمد', 'خالد', 'حسن']"

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            lang='ar'
        )

    def test_assign_list_exclamation_mark(self):
        code = textwrap.dedent("""\
        antwoorden is ja, NEE!, misschien
        print antwoorden at random""")

        expected = textwrap.dedent("""\
        antwoorden = ['ja', 'NEE!', 'misschien']
        print(f'{random.choice(antwoorden)}')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_assign_list_values_with_inner_single_quotes(self):
        code = textwrap.dedent(f"""\
        taart is 'appeltaart, choladetaart, kwarktaart'
        print 'we bakken een' taart at random""")

        expected = textwrap.dedent("""\
        taart = ['\\'appeltaart', 'choladetaart', 'kwarktaart\\'']
        print(f'\\'we bakken een\\' {random.choice(taart)}')""")

        self.single_level_tester(code=code, expected=expected)

    def test_assign_list_values_with_inner_double_quotes(self):
        code = textwrap.dedent(f"""\
        taart is "appeltaart, choladetaart, kwarktaart"
        print 'we bakken een' taart at random""")

        expected = textwrap.dedent("""\
        taart = ['"appeltaart', 'choladetaart', 'kwarktaart"']
        print(f'\\'we bakken een\\' {random.choice(taart)}')""")

        self.single_level_tester(code=code, expected=expected)

    def test_assign_list_with_single_quoted_values(self):
        code = textwrap.dedent(f"""\
        taart is 'appeltaart', 'choladetaart', 'kwarktaart'
        print 'we bakken een' taart at random""")

        expected = textwrap.dedent("""\
        taart = ['\\'appeltaart\\'', '\\'choladetaart\\'', '\\'kwarktaart\\'']
        print(f'\\'we bakken een\\' {random.choice(taart)}')""")

        self.single_level_tester(code=code, expected=expected)

    def test_assign_list_with_double_quoted_values(self):
        code = textwrap.dedent(f"""\
        taart is "appeltaart", "choladetaart", "kwarktaart"
        print "we bakken een" taart at random""")

        expected = textwrap.dedent("""\
        taart = ['"appeltaart"', '"choladetaart"', '"kwarktaart"']
        print(f'"we bakken een" {random.choice(taart)}')""")

        self.single_level_tester(code=code, expected=expected)

    def test_assign_list_values_with_inner_quotes(self):
        code = """dieren is Hond's, Kat"s, 'Kangoeroe', "Muis\""""
        expected = """dieren = ['Hond\\\'s', 'Kat"s', '\\\'Kangoeroe\\\'', '"Muis"']"""

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    #
    # forward tests
    #
    def test_forward_with_list_variable_gives_error(self):
        code = textwrap.dedent("""\
        a is 1, 2, 3
        forward a""")

        self.multi_level_tester(
            max_level=self.max_turtle_level,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_forward_with_list_access_random(self):
        code = textwrap.dedent("""\
        directions is 10, 100, 360
        forward directions at random""")

        expected = HedyTester.dedent("""\
        directions = ['10', '100', '360']""",
        HedyTester.forward_transpiled('random.choice(directions)'))

        self.multi_level_tester(
            max_level=self.max_turtle_level,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    #
    # turn tests
    #
    def test_turn_with_list_variable_gives_error(self):
        code = textwrap.dedent("""\
        a is 45, 90, 180
        turn a""")

        self.multi_level_tester(
            max_level=self.max_turtle_level,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_turn_with_list_access_random(self):
        code = textwrap.dedent("""\
        directions is 10, 100, 360
        turn directions at random""")

        expected = HedyTester.dedent("""\
        directions = ['10', '100', '360']""",
        HedyTester.turn_transpiled('random.choice(directions)'))

        self.multi_level_tester(
            max_level=self.max_turtle_level,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    #
    # combined tests
    #
    def test_list_access_misspelled_at_gives_error(self):
        code = textwrap.dedent("""\
        dieren is Hond, Kat, Kangoeroe
        print dieren ad random""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    #
    # add/remove tests
    #
    def test_add_text_to_list(self):
        code = textwrap.dedent("""\
        dieren is koe, kiep
        add muis to dieren
        print dieren at random""")

        expected = textwrap.dedent("""\
        dieren = ['koe', 'kiep']
        dieren.append('muis')
        print(f'{random.choice(dieren)}')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11,
            extra_check_function=self.result_in(['koe', 'kiep', 'muis']),
        )

    def test_add_text_with_inner_single_quote_to_list(self):
        code = textwrap.dedent("""\
        dieren is koe, kiep
        add mui's to dieren
        print dieren at random""")

        expected = textwrap.dedent("""\
        dieren = ['koe', 'kiep']
        dieren.append('mui\\\'s')
        print(f'{random.choice(dieren)}')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11,
            extra_check_function=self.result_in(['koe', 'kiep', 'mui\'s']),
        )

    def test_add_text_with_inner_double_quote_to_list(self):
        code = textwrap.dedent("""\
        dieren is koe, kiep
        add mui"s to dieren
        print dieren at random""")

        expected = textwrap.dedent("""\
        dieren = ['koe', 'kiep']
        dieren.append('mui"s')
        print(f'{random.choice(dieren)}')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11,
            extra_check_function=self.result_in(['koe', 'kiep', 'mui\"s']),
        )

    def test_remove_text_from_list(self):
        code = textwrap.dedent("""\
        dieren is koe, kiep
        remove kiep from dieren
        print dieren at random""")

        expected = textwrap.dedent("""\
        dieren = ['koe', 'kiep']
        try:
          dieren.remove('kiep')
        except:
          pass
        print(f'{random.choice(dieren)}')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11,
            extra_check_function=self.result_in(['koe']),
        )

    def test_remove_text_with_single_quote_from_list(self):
        code = textwrap.dedent("""\
        dieren is koe, kiep's
        remove kiep's from dieren
        print dieren at random""")

        expected = textwrap.dedent("""\
        dieren = ['koe', 'kiep\\\'s']
        try:
          dieren.remove('kiep\\\'s')
        except:
          pass
        print(f'{random.choice(dieren)}')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11,
            extra_check_function=self.result_in(['koe', 'kiep', 'mui\'s']),
        )

    def test_remove_text_with_double_quote_from_list(self):
        code = textwrap.dedent("""\
        dieren is koe, kiep"s
        remove kiep"s from dieren
        print dieren at random""")

        expected = textwrap.dedent("""\
        dieren = ['koe', 'kiep"s']
        try:
          dieren.remove('kiep"s')
        except:
          pass
        print(f'{random.choice(dieren)}')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11,
            extra_check_function=self.result_in(['koe', 'kiep', 'mui\'s']),
        )

    def test_add_text_with_spaces_to_list(self):
        code = textwrap.dedent("""\
        opties is zeker weten, misschien wel
        add absoluut niet to opties
        print opties at random""")

        expected = textwrap.dedent("""\
        opties = ['zeker weten', 'misschien wel']
        opties.append('absoluut niet')
        print(f'{random.choice(opties)}')""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected
        )

    def test_add_ask_to_list(self):
        code = textwrap.dedent("""\
        color is ask what is your favorite color?
        colors is green, red, blue
        add color to colors
        print colors at random""")

        expected = textwrap.dedent("""\
        color = input('what is your favorite color'+'?')
        colors = ['green', 'red', 'blue']
        colors.append(color)
        print(f'{random.choice(colors)}')""")

        self.single_level_tester(code=code, expected=expected)

    def test_remove_ask_from_list(self):
        code = textwrap.dedent("""\
        colors is green, red, blue
        color is ask what color to remove?
        remove color from colors
        print colors at random""")

        expected = textwrap.dedent("""\
        colors = ['green', 'red', 'blue']
        color = input('what color to remove'+'?')
        try:
          colors.remove(color)
        except:
          pass
        print(f'{random.choice(colors)}')""")

        self.single_level_tester(code=code, expected=expected)

    def test_add_to_list_with_string_var_gives_error(self):
        code = textwrap.dedent("""\
        color is yellow
        colors is green, red, blue
        add colors to color""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_add_to_list_with_input_var_gives_error(self):
        code = textwrap.dedent("""\
        colors is ask 'What are the colors?'
        favorite is red
        add favorite to colors""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_remove_from_list_with_string_var_gives_error(self):
        code = textwrap.dedent("""\
        color is yellow
        colors is green, red, blue
        remove colors from color""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_remove_from_list_with_input_var_gives_error(self):
        code = textwrap.dedent("""\
        colors is ask 'What are the colors?'
        favorite is red
        remove favorite from colors""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    #
    # negative tests
    #
    def test_random_from_string_gives_type_error(self):
        code = textwrap.dedent("""\
        items is aap noot mies
        print items at random""")

        self.multi_level_tester(
            code=code,
            max_level=11,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_random_undefined_var_gives_error(self):
        code = textwrap.dedent("""\
        dieren is hond, kat, kangoeroe
        print dier at random""")

        self.multi_level_tester(
            code=code,
            max_level=11,
            exception=hedy.exceptions.UndefinedVarException
        )

    def test_list_access_with_type_input_gives_error(self):
        code = textwrap.dedent("""\
        animals is ask 'What are the animals?'
        print animals at random""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )
