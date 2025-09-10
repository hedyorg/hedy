import textwrap

import hedy
from hedy_sourcemap import SourceRange
from tests.Tester import HedyTester, SkippedMapping


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

    def test_print_list_converts_to_literal_string(self):
        code = textwrap.dedent("""\
            plaatsen is een stad, een  dorp, een strand
            print plaatsen""")

        expected = textwrap.dedent("""\
            plaatsen = ['een stad', 'een  dorp', 'een strand']
            print(f'plaatsen')""")

        check_in_list = (lambda x: HedyTester.run_code(x) in ['een stad', 'een  dorp', 'een strand'])

        self.single_level_tester(
            code=code,
            expected=expected,
            extra_check_function=check_in_list,
            unused_allowed=True
        )

    def test_list_access_misspelled_at_converts_to_literal_string(self):
        code = textwrap.dedent("""\
            dieren is Hond, Kat, Kangoeroe
            print dieren ad random""")

        expected = textwrap.dedent("""\
            dieren = ['Hond', 'Kat', 'Kangoeroe']
            print(f'dieren ad random')""")

        check_in_list = (lambda x: HedyTester.run_code(x) in ['Hond', 'Kat', 'Kangoeroe'])

        self.single_level_tester(
            code=code,
            expected=expected,
            extra_check_function=check_in_list,
            unused_allowed=True
        )

    def test_color_basic(self):
        code = textwrap.dedent("""\
            color red
            forward 10""")

        expected = self.dedent(
            self.color_transpiled("red", 'en'),
            self.forward_transpiled('10'))

        self.single_level_tester(
            code=code,
            expected=expected
        )

    def test_random_turtle_dutch(self):
        lang = 'nl'
        code = textwrap.dedent("""\
            lijstkleuren is blauw, groen, wit
            kleur lijstkleuren at random
            vooruit 10""")

        expected = self.dedent(
            "lijstkleuren = ['blauw', 'groen', 'wit']",
            self.color_transpiled("{random.choice(lijstkleuren)}", lang),
            self.forward_transpiled('10'))

        self.multi_level_tester(
            max_level=5,
            code=code,
            lang=lang,
            translate=False,
            expected=expected
        )

    def test_print_list_random_punctuation(self):
        code = textwrap.dedent("""\
            gerechten is spaghetti, spruitjes, hamburgers
            print Jij eet vanavond gerechten at random!""")

        expected = self.dedent(
            "gerechten = ['spaghetti', 'spruitjes', 'hamburgers']",
            self.list_access_transpiled("random.choice(gerechten)"),
            "print(f'Jij eet vanavond {random.choice(gerechten)} !')")

        self.multi_level_tester(
            max_level=3,
            code=code,
            expected=expected
        )

    def test_print_list_random_punctuation_2(self):
        code = textwrap.dedent("""\
            prijzen is 1 euro, 10 euro, 100 euro
            print Dat wordt dan prijzen at random, alstublieft.""")

        expected = self.dedent(
            "prijzen = ['1 euro', '10 euro', '100 euro']",
            self.list_access_transpiled("random.choice(prijzen)"),
            "print(f'Dat wordt dan {random.choice(prijzen)} , alstublieft.')")

        self.multi_level_tester(
            max_level=3,
            code=code,
            expected=expected
        )

    def test_print_list_random_fr(self):
        code = textwrap.dedent("""\
            animaux est chien, chat, kangourou
            affiche animaux au hasard""")

        expected = self.dedent(
            "animaux = ['chien', 'chat', 'kangourou']",
            self.list_access_transpiled('random.choice(animaux)'),
            "print(f'{random.choice(animaux)}')")

        # check if result is in the expected list
        check_in_list = (lambda x: HedyTester.run_code(x) in ['chien', 'chat', 'kangourou'])

        self.multi_level_tester(
            max_level=5,
            code=code,
            expected=expected,
            extra_check_function=check_in_list,
            lang='fr'
        )

    #
    # ask tests
    #
    def test_ask_list_converts_to_literal_string(self):
        code = textwrap.dedent("""\
            dieren is Hond, Kat, Kangoeroe
            a is ask dieren""")

        expected = textwrap.dedent("""\
            dieren = ['Hond', 'Kat', 'Kangoeroe']
            a = input(f'dieren')""")

        check_in_list = (lambda x: HedyTester.run_code(x) in ['Hond', 'Kat', 'Kangoeroe'])

        self.single_level_tester(
            code=code,
            expected=expected,
            extra_check_function=check_in_list,
            unused_allowed=True
        )

    def test_ask_list_random(self):
        code = textwrap.dedent("""\
            dieren is Hond, Kat, Kangoeroe
            a is ask dieren at random""")

        expected = self.dedent(
            "dieren = ['Hond', 'Kat', 'Kangoeroe']",
            self.list_access_transpiled("random.choice(dieren)"),
            "a = input(f'{random.choice(dieren)}')")

        self.multi_level_tester(
            max_level=5,
            code=code,
            expected=expected,
            unused_allowed=True
        )

    def test_ask_list_random_punctuation(self):
        code = textwrap.dedent("""\
            gerechten is spaghetti, spruitjes, hamburgers
            answer is ask Jij eet vanavond gerechten at random!""")

        expected = self.dedent(
            "gerechten = ['spaghetti', 'spruitjes', 'hamburgers']",
            self.list_access_transpiled("random.choice(gerechten)"),
            "answer = input(f'Jij eet vanavond {random.choice(gerechten)} !')"
        )

        self.multi_level_tester(
            max_level=3,
            code=code,
            expected=expected,
            unused_allowed=True
        )

    def test_ask_list_random_punctuation_2(self):
        code = textwrap.dedent("""\
            prijzen is 1 euro, 10 euro, 100 euro
            answer is ask Dat wordt dan prijzen at random, alstublieft.""")

        expected = self.dedent(
            "prijzen = ['1 euro', '10 euro', '100 euro']",
            self.list_access_transpiled("random.choice(prijzen)"),
            "answer = input(f'Dat wordt dan {random.choice(prijzen)} , alstublieft.')"
        )

        self.multi_level_tester(
            max_level=3,
            code=code,
            expected=expected,
            unused_allowed=True
        )

    def test_ask_list_access_index(self):
        code = textwrap.dedent("""\
            dieren is Hond, Kat, Kangoeroe
            answer is ask dieren at 1""")

        expected = self.dedent(
            "dieren = ['Hond', 'Kat', 'Kangoeroe']",
            self.list_access_transpiled('dieren[int(1)-1]'),
            "answer = input(f'{dieren[int(1)-1]}')")

        self.multi_level_tester(
            max_level=5,
            code=code,
            expected=expected,
            unused_allowed=True
        )

    def test_ask_list_random_fr(self):
        code = textwrap.dedent("""\
            animaux est chien, chat, kangourou
            a est demande animaux au hasard""")

        expected = self.dedent(
            "animaux = ['chien', 'chat', 'kangourou']",
            self.list_access_transpiled('random.choice(animaux)'),
            "a = input(f'{random.choice(animaux)}')")

        self.multi_level_tester(
            max_level=5,
            code=code,
            expected=expected,
            lang='fr',
            unused_allowed=True
        )

    #
    # sleep tests
    #
    def test_sleep_with_time_variable(self):
        code = textwrap.dedent("""\
            time is 10
            sleep time""")

        expected = self.dedent(
            "_time = '10'",
            self.sleep_transpiled('_time'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=5)

    def test_sleep_with_list_access(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n at 1""")

        expected = self.dedent(
            "n = ['1', '2', '3']",
            self.list_access_transpiled('n[int(1)-1]'),
            self.sleep_transpiled('n[int(1)-1]'))

        self.multi_level_tester(max_level=5, code=code, expected=expected)

    def test_sleep_with_list_random(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n at random""")

        expected = self.dedent(
            "n = ['1', '2', '3']",
            self.list_access_transpiled('random.choice(n)'),
            self.sleep_transpiled('random.choice(n)'))

        self.multi_level_tester(max_level=5, code=code, expected=expected)

    def test_sleep_with_list_gives_error(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException)

    #
    # assign tests
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

        self.multi_level_tester(max_level=5, code=code, expected=expected)

    def test_assign_var_trims_spaces(self):
        code = "answer is  This is long    "
        expected = "answer = 'This is long'"

        self.multi_level_tester(max_level=5, code=code, expected=expected, unused_allowed=True)

    def test_assign_var_trims_spaces_with_comment(self):
        code = "answer is  This is long    # comment"
        expected = "answer = 'This is long'"

        self.multi_level_tester(max_level=5, code=code, expected=expected, unused_allowed=True)

    def test_assign_list(self):
        code = "dieren is Hond, Kat, Kangoeroe"
        expected = "dieren = ['Hond', 'Kat', 'Kangoeroe']"

        self.multi_level_tester(max_level=5, code=code, expected=expected, unused_allowed=True)

    def test_assign_list_with_var_starting_with_ask(self):
        code = "asks is one, two, three"
        expected = "asks = ['one', 'two', 'three']"

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True)

    def test_assign_list_with_var_starting_with_ask_nl(self):
        code = "vraaga is vind je honden aardig, doe jij teveel gamen, je ging op pad"
        expected = "vraaga = ['vind je honden aardig', 'doe jij teveel gamen', 'je ging op pad']"

        self.multi_level_tester(code=code, expected=expected, max_level=5, unused_allowed=True)

    def test_assign_list_to_hungarian_var(self):
        code = textwrap.dedent("""\
            állatok is kutya, macska, kenguru
            print állatok at random""")

        expected = self.dedent(
            "állatok = ['kutya', 'macska', 'kenguru']",
            self.list_access_transpiled("random.choice(állatok)"),
            "print(f'{random.choice(állatok)}')")

        self.multi_level_tester(max_level=5, code=code, expected=expected)

    def test_assign_list_trims_elements_trailing_spaces(self):
        code = "dieren is Hond , Kat , Kangoeroe "
        expected = "dieren = ['Hond', 'Kat', 'Kangoeroe']"

        self.multi_level_tester(max_level=5, code=code, expected=expected, unused_allowed=True)

    def test_assign_list_trims_elements_leading_spaces(self):
        code = "dieren is   Hond,   Kat,   Kangoeroe"
        expected = "dieren = ['Hond', 'Kat', 'Kangoeroe']"

        self.multi_level_tester(max_level=5, code=code, expected=expected, unused_allowed=True)

    def test_assign_list_trims_elements_spaces(self):
        code = "dieren is   I am  ,  waiting for  ,  the summer  "
        expected = "dieren = ['I am', 'waiting for', 'the summer']"

        self.multi_level_tester(max_level=5, code=code, expected=expected, unused_allowed=True)

    def test_assign_random_value(self):
        code = textwrap.dedent("""\
            dieren is hond, kat, kangoeroe
            dier is dieren at random
            print dier""")

        expected = self.dedent(
            "dieren = ['hond', 'kat', 'kangoeroe']",
            self.list_access_transpiled("random.choice(dieren)"),
            "dier = random.choice(dieren)",
            "print(f'{dier}')")

        self.multi_level_tester(
            max_level=5,
            code=code,
            expected=expected,
            extra_check_function=self.result_in(['Hond', 'Kat', 'Kangoeroe'])
        )

    def test_assign_list_with_dutch_comma_arabic_lang(self):
        code = "صديقي هو احمد, خالد, حسن"
        expected = "صديقي = ['احمد', 'خالد', 'حسن']"

        self.multi_level_tester(
            max_level=5,
            code=code,
            expected=expected,
            lang='ar',
            unused_allowed=True,
            # translation must be off because the Latin commas will be converted to arabic commas and this is correct
            translate=False
        )

    def test_assign_list_with_arabic_comma_and_is(self):
        code = "animals هو cat، dog، platypus"
        expected = "animals = ['cat', 'dog', 'platypus']"

        self.multi_level_tester(
            max_level=5,
            code=code,
            unused_allowed=True,
            expected=expected,
            lang='ar'
        )

    def test_assign_list_with_arabic_comma(self):
        code = "صديقي هو احمد، خالد، حسن"
        expected = "صديقي = ['احمد', 'خالد', 'حسن']"

        self.multi_level_tester(
            max_level=5,
            code=code,
            unused_allowed=True,
            expected=expected,
            lang='ar'
        )

    def test_assign_list_exclamation_mark(self):
        code = textwrap.dedent("""\
            antwoorden is ja, NEE!, misschien
            print antwoorden at random""")

        expected = self.dedent(
            "antwoorden = ['ja', 'NEE!', 'misschien']",
            self.list_access_transpiled("random.choice(antwoorden)"),
            "print(f'{random.choice(antwoorden)}')")

        self.multi_level_tester(max_level=5, code=code, expected=expected)

    def test_assign_list_values_with_inner_single_quotes(self):
        code = textwrap.dedent(f"""\
            taart is 'appeltaart, choladetaart, kwarktaart'
            print 'we bakken een' taart at random""")

        expected = self.dedent(
            "taart = ['\\'appeltaart', 'choladetaart', 'kwarktaart\\'']",
            self.list_access_transpiled("random.choice(taart)"),
            "print(f'\\'we bakken een\\' {random.choice(taart)}')")

        self.single_level_tester(code=code, expected=expected)

    def test_assign_list_values_with_inner_double_quotes(self):
        code = textwrap.dedent(f"""\
            taart is "appeltaart, choladetaart, kwarktaart"
            print 'we bakken een' taart at random""")

        expected = self.dedent(
            "taart = ['\"appeltaart', 'choladetaart', 'kwarktaart\"']",
            self.list_access_transpiled("random.choice(taart)"),
            "print(f'\\'we bakken een\\' {random.choice(taart)}')")

        self.single_level_tester(code=code, expected=expected)

    def test_assign_list_with_single_quoted_values(self):
        code = textwrap.dedent(f"""\
            taart is 'appeltaart', 'choladetaart', 'kwarktaart'
            print 'we bakken een' taart at random""")

        expected = self.dedent(
            "taart = ['\\'appeltaart\\'', '\\'choladetaart\\'', '\\'kwarktaart\\'']",
            self.list_access_transpiled('random.choice(taart)'),
            "print(f'\\'we bakken een\\' {random.choice(taart)}')")

        self.single_level_tester(code=code, expected=expected)

    def test_assign_list_with_double_quoted_values(self):
        code = textwrap.dedent(f"""\
            taart is "appeltaart", "choladetaart", "kwarktaart"
            print "we bakken een" taart at random""")

        expected = self.dedent(
            "taart = ['\"appeltaart\"', '\"choladetaart\"', '\"kwarktaart\"']",
            self.list_access_transpiled('random.choice(taart)'),
            "print(f'\"we bakken een\" {random.choice(taart)}')")

        self.single_level_tester(code=code, expected=expected)

    def test_assign_list_values_with_inner_quotes(self):
        code = """dieren is Hond's, Kat"s, 'Kangoeroe', "Muis\""""
        expected = """dieren = ['Hond\\\'s', 'Kat"s', '\\\'Kangoeroe\\\'', '"Muis"']"""

        self.multi_level_tester(max_level=5, code=code, expected=expected, unused_allowed=True)

    #
    # forward tests
    #
    def test_forward_with_list_variable_gives_error(self):
        code = textwrap.dedent("""\
        a is 1, 2, 3
        forward a""")

        self.multi_level_tester(
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_forward_with_list_access(self):
        code = textwrap.dedent("""\
            directions is 10, 100, 360
            forward directions at 3""")

        expected = self.dedent(
            "directions = ['10', '100', '360']",
            self.list_access_transpiled('directions[int(3)-1]'),
            self.forward_transpiled('directions[int(3)-1]'))

        self.multi_level_tester(
            max_level=5,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_forward_with_list_access_random(self):
        code = textwrap.dedent("""\
            directions is 10, 100, 360
            forward directions at random""")

        expected = self.dedent(
            "directions = ['10', '100', '360']",
            self.list_access_transpiled('random.choice(directions)'),
            self.forward_transpiled('random.choice(directions)'))

        self.multi_level_tester(
            max_level=5,
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
            max_level=15,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_turn_with_list_access_random(self):
        code = textwrap.dedent("""\
            directions is 10, 100, 360
            turn directions at random""")

        expected = self.dedent(
            "directions = ['10', '100', '360']",
            self.list_access_transpiled('random.choice(directions)'),
            self.turn_transpiled('random.choice(directions)'))

        self.multi_level_tester(
            max_level=5,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_turn_with_list_access(self):
        code = textwrap.dedent("""\
            directions is 10, 100
            turn directions at 1""")

        expected = self.dedent(
            "directions = ['10', '100']",
            self.list_access_transpiled('directions[int(1)-1]'),
            self.turn_transpiled('directions[int(1)-1]'))

        self.multi_level_tester(
            max_level=5,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    #
    # color tests
    #
    def test_color_with_list_variable_gives_runtime_error(self):
        code = textwrap.dedent("""\
            c is red, green, blue
            color c""")

        expected = self.dedent(
            "c = ['red', 'green', 'blue']",
            self.color_transpiled('c'))

        self.single_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True
        )

    def test_color_with_list_color_variable(self):
        code = textwrap.dedent("""\
            red is light, dark
            color red""")

        expected = self.dedent(
            "red = ['light', 'dark']",
            self.color_transpiled('red'))

        self.single_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True
        )

    def test_color_with_list_access(self):
        code = textwrap.dedent("""\
            colors is red, green, blue
            color colors at 2""")

        expected = self.dedent(
            "colors = ['red', 'green', 'blue']",
            self.color_transpiled('{colors[int(2)-1]}'))

        self.multi_level_tester(
            max_level=5,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_color_with_list_access_random(self):
        code = textwrap.dedent("""\
            colors is red, green, blue
            color colors at random""")

        expected = self.dedent(
            "colors = ['red', 'green', 'blue']",
            self.color_transpiled('{random.choice(colors)}'))

        self.multi_level_tester(
            max_level=5,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    #
    # add/remove tests
    #
    def test_add_text_to_list(self):
        code = textwrap.dedent("""\
            dieren is koe, kiep
            add muis to dieren
            print dieren at random""")

        expected = self.dedent(
            "dieren = ['koe', 'kiep']",
            "dieren.append('muis')",
            self.list_access_transpiled("random.choice(dieren)"),
            "print(f'{random.choice(dieren)}')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=5,
            extra_check_function=self.result_in(['koe', 'kiep', 'muis']),
        )

    def test_add_text_to_list_numerical(self):
        code = textwrap.dedent("""\
            numbers is 1, 2
            remove 1 from numbers
            remove 2 from numbers
            add 4 to numbers
            print numbers at random""")

        expected = self.dedent(
            "numbers = ['1', '2']",
            self.remove_transpiled('numbers', "'1'"),
            self.remove_transpiled('numbers', "'2'"),
            "numbers.append('4')",
            self.list_access_transpiled("random.choice(numbers)"),
            "print(f'{random.choice(numbers)}')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=5,
            extra_check_function=self.result_in([4]),
        )

    def test_add_text_with_inner_single_quote_to_list(self):
        code = textwrap.dedent("""\
            dieren is koe, kiep
            add mui's to dieren
            print dieren at random""")

        expected = self.dedent(
            "dieren = ['koe', 'kiep']",
            "dieren.append('mui\\\'s')",
            self.list_access_transpiled("random.choice(dieren)"),
            "print(f'{random.choice(dieren)}')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=5,
            extra_check_function=self.result_in(['koe', 'kiep', 'mui\'s']),
        )

    def test_add_text_with_inner_double_quote_to_list(self):
        code = textwrap.dedent("""\
            dieren is koe, kiep
            add mui"s to dieren
            print dieren at random""")

        expected = self.dedent(
            "dieren = ['koe', 'kiep']",
            "dieren.append('mui\"s')",
            self.list_access_transpiled("random.choice(dieren)"),
            "print(f'{random.choice(dieren)}')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=5,
            extra_check_function=self.result_in(['koe', 'kiep', 'mui\"s']),
        )

    def test_add_integer_to_list(self):
        code = textwrap.dedent("""\
            dieren is koe, kiep
            add 5 to dieren
            print dieren at random""")

        expected = self.dedent(
            "dieren = ['koe', 'kiep']",
            "dieren.append('5')",
            self.list_access_transpiled("random.choice(dieren)"),
            "print(f'{random.choice(dieren)}')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=5,
            extra_check_function=self.result_in(['koe', 'kiep', 5]),
        )

    def test_remove_text_from_list(self):
        code = textwrap.dedent("""\
            dieren is koe, kiep
            remove kiep from dieren
            print dieren at random""")

        expected = self.dedent(
            "dieren = ['koe', 'kiep']",
            self.remove_transpiled('dieren', "'kiep'"),
            self.list_access_transpiled('random.choice(dieren)'),
            "print(f'{random.choice(dieren)}')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=5,
            extra_check_function=self.result_in(['koe']),
        )

    def test_remove_text_with_single_quote_from_list(self):
        code = textwrap.dedent("""\
            dieren is koe, kiep's
            remove kiep's from dieren
            print dieren at random""")

        expected = self.dedent(
            "dieren = ['koe', 'kiep\\\'s']",
            self.remove_transpiled('dieren', "'kiep\\\'s'"),
            self.list_access_transpiled('random.choice(dieren)'),
            "print(f'{random.choice(dieren)}')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=5,
            extra_check_function=self.result_in(['koe', 'kiep', 'mui\'s']),
        )

    def test_remove_text_with_double_quote_from_list(self):
        code = textwrap.dedent("""\
            dieren is koe, kiep"s
            remove kiep"s from dieren
            print dieren at random""")

        expected = self.dedent(
            "dieren = ['koe', 'kiep\"s']",
            self.remove_transpiled('dieren', "'kiep\"s'"),
            self.list_access_transpiled("random.choice(dieren)"),
            "print(f'{random.choice(dieren)}')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=5,
            extra_check_function=self.result_in(['koe', 'kiep', 'mui\'s']),
        )

    def test_add_text_with_spaces_to_list(self):
        code = textwrap.dedent("""\
            opties is zeker weten, misschien wel
            add absoluut niet to opties
            print opties at random""")

        expected = self.dedent(
            "opties = ['zeker weten', 'misschien wel']",
            "opties.append('absoluut niet')",
            self.list_access_transpiled("random.choice(opties)"),
            "print(f'{random.choice(opties)}')")

        self.multi_level_tester(
            max_level=5,
            code=code,
            expected=expected
        )

    def test_access_before_assign_with_random(self):
        code = textwrap.dedent("""\
            print colors at random
            colors is green, red, blue""")

        expected = textwrap.dedent("""\
            print(f'pass')
            colors = ['green', 'red', 'blue']""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 7, 1, 13), hedy.exceptions.AccessBeforeAssignException),
            SkippedMapping(SourceRange(1, 7, 1, 23), hedy.exceptions.UndefinedVarException),
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            skipped_mappings=skipped_mappings,
        )

    def test_add_ask_to_list(self):
        code = textwrap.dedent("""\
            color is ask what is your favorite color?
            colors is green, red, blue
            add color to colors
            print colors at random""")

        expected = self.dedent(
            "color = input(f'what is your favorite color?')",
            "colors = ['green', 'red', 'blue']",
            "colors.append(color)",
            self.list_access_transpiled("random.choice(colors)"),
            "print(f'{random.choice(colors)}')")

        self.single_level_tester(code=code, expected=expected)

    def test_remove_ask_from_list(self):
        code = textwrap.dedent("""\
            colors is green, red, blue
            color is ask what color to remove?
            remove color from colors
            print colors at random""")

        expected = self.dedent(
            "colors = ['green', 'red', 'blue']",
            "color = input(f'what color to remove?')",
            self.remove_transpiled('colors', 'color'),
            self.list_access_transpiled('random.choice(colors)'),
            "print(f'{random.choice(colors)}')")

        self.single_level_tester(code=code, expected=expected)

    def test_add_to_list_with_string_var_gives_error(self):
        code = textwrap.dedent("""\
        color is yellow
        colors is green, red, blue
        add colors to color""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
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
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_add_to_list_without_to_gives_error(self):
        code = textwrap.dedent("""\
        animals is dog, cat, kangaroo
        add favorite
        print animals at random""")

        self.multi_level_tester(
            max_level=11,
            skip_faulty=False,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.MissingAdditionalCommand
        )

    def test_remove_from_list_with_string_var_gives_error(self):
        code = textwrap.dedent("""\
        color is yellow
        colors is green, red, blue
        remove colors from color""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_add_to_list_without_list_gives_error(self):
        code = textwrap.dedent("""\
        animals is dog, cat, kangaroo
        add favorite to
        print animals at random""")

        self.multi_level_tester(
            max_level=11,
            skip_faulty=False,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.IncompleteCommandException
        )

    def test_remove_from_list_with_input_var_gives_error(self):
        code = textwrap.dedent("""\
        colors is ask 'What are the colors?'
        favorite is red
        remove favorite from colors""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_remove_from_list_without_to_gives_error(self):
        code = textwrap.dedent("""\
        animals is dog, cat, kangaroo
        remove dog
        print animals at random""")

        self.multi_level_tester(
            max_level=11,
            skip_faulty=False,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.MissingAdditionalCommand
        )

    def test_remove_from_list_without_list_gives_error(self):
        code = textwrap.dedent("""\
        animals is dog, cat, kangaroo
        remove dog from
        print animals at random""")

        self.multi_level_tester(
            max_level=11,
            skip_faulty=False,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.IncompleteCommandException
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
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_random_undefined_var_gives_error(self):
        code = textwrap.dedent("""\
        dieren is hond, kat, kangoeroe
        print dier at random""")

        self.multi_level_tester(
            code=code,
            max_level=11,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.UndefinedVarException
        )

    def test_list_access_with_type_input_gives_error(self):
        code = textwrap.dedent("""\
        animals is ask 'What are the animals?'
        print animals at random""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_print_list_access_at_index(self):  # 3778
        code = textwrap.dedent("""\
            l is 1, 2, 3
            print l at 3""")

        expected = self.dedent(
            "l = ['1', '2', '3']",
            self.list_access_transpiled("l[int(3)-1]"),
            "print(f'{l[int(3)-1]}')")

        self.multi_level_tester(code=code, expected=expected, max_level=5)

    def test_print_list_access_at_random(self):  # 3778
        code = textwrap.dedent("""\
            l is 1, 2, 3
            print l at random""")
        expected = self.dedent(
            "l = ['1', '2', '3']",
            self.list_access_transpiled("random.choice(l)"),
            "print(f'{random.choice(l)}')")

        self.multi_level_tester(code=code, expected=expected, max_level=5)

    #
    # play tests
    #
    def test_play_list_access(self):
        code = textwrap.dedent("""\
            notes is C4, E4, D4, F4, G4
            play notes at 4""")

        expected = self.dedent(
            "notes = ['C4', 'E4', 'D4', 'F4', 'G4']",
            self.play_transpiled('notes[int(4)-1]'))

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=5
        )

    def test_play_list_access_random(self):
        code = textwrap.dedent("""\
            notes is C4, E4, D4, F4, G4
            play notes at random""")

        expected = self.dedent(
            "notes = ['C4', 'E4', 'D4', 'F4', 'G4']",
            self.play_transpiled('random.choice(notes)'))

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=5
        )


def test_play_chord(self):
    code = textwrap.dedent("""\
    play C4 E4 D4""")

    expected = textwrap.dedent("""\
    play(notes_mapping.get(str(C4), notes_mapping.get(str(C4), notes_mapping.get(str(C4))))
    time.sleep(0.5)""")

    self.multi_level_tester(
        code=code,
        translate=False,
        skip_faulty=False,
        unused_allowed=True,
        expected=expected,
        max_level=11
    )
