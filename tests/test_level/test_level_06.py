import textwrap
from parameterized import parameterized
import hedy
from tests.Tester import HedyTester


class TestsLevel6(HedyTester):
    level = 6
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
    def test_print_single_quoted_text_var(self):
        code = textwrap.dedent("""\
        naam is 'Hedy'
        print 'ik heet ' naam""")

        expected = textwrap.dedent("""\
        naam = Value('\\'Hedy\\'')
        print(f'ik heet {naam}')""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected
        )

    def test_print_double_quoted_text_var(self):
        code = textwrap.dedent("""\
        naam is "Hedy"
        print 'ik heet ' naam""")

        expected = textwrap.dedent("""\
        naam = Value('"Hedy"')
        print(f'ik heet {naam}')""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected
        )

    # issue 1795
    def test_print_quoted_var_reference(self):
        code = textwrap.dedent("""\
        naam is 'Daan'
        woord1 is zomerkamp
        print 'naam' ' is naar het' 'woord1'""")

        expected = textwrap.dedent("""\
        naam = Value('\\'Daan\\'')
        woord1 = Value('zomerkamp')
        print(f'naam is naar hetwoord1')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_print_list_access_at_index(self):
        code = textwrap.dedent("""\
            l is 1, 2, 3
            print l at 3""")

        expected = self.dedent(
            "l = Value([Value('1', num_sys='Latin'), Value('2', num_sys='Latin'), Value('3', num_sys='Latin')])",
            self.list_access_transpiled("l.data[int(3)-1]"),
            "print(f'{l.data[int(3)-1]}')")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_print_list_access_at_index_arabic(self):
        code = textwrap.dedent("""\
               l is ١,٢,٣ 
               print l at ٣""")

        expected = self.dedent(
            f"l = {self.list_transpiled(1, 2, 3, num_sys='Arabic')}",
            self.list_access_transpiled("l.data[int(3)-1]"),
            "print(f'{l.data[int(3)-1]}')")

        self.multi_level_tester(code=code, expected=expected, max_level=11, output='٣')

    def test_print_list_access_at_random(self):
        code = textwrap.dedent("""\
            l is 1, 2, 3
            print l at random""")
        expected = self.dedent(
            "l = Value([Value('1', num_sys='Latin'), Value('2', num_sys='Latin'), Value('3', num_sys='Latin')])",
            self.list_access_transpiled("random.choice(l.data)"),
            "print(f'{random.choice(l.data)}')")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_print_list_random_fr(self):
        code = textwrap.dedent("""\
            animaux est chien, chat, kangourou
            affiche animaux au hasard""")

        expected = self.dedent(
            "animaux = Value([Value('chien'), Value('chat'), Value('kangourou')])",
            self.list_access_transpiled('random.choice(animaux.data)'),
            "print(f'{random.choice(animaux.data)}')")

        # check if result is in the expected list
        check_in_list = (lambda x: HedyTester.run_code(x) in ['chien', 'chat', 'kangourou'])

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=check_in_list,
            lang='fr'
        )

    def test_print_list_access_index_var(self):
        code = textwrap.dedent("""\
            index is 1
            dieren is Hond, Kat, Kangoeroe
            print dieren at index""")

        expected = self.dedent(
            "index = Value('1', num_sys='Latin')",
            "dieren = Value([Value('Hond'), Value('Kat'), Value('Kangoeroe')])",
            self.list_access_transpiled('dieren.data[int(index.data)-1]'),
            "print(f'{dieren.data[int(index.data)-1]}')")

        check_in_list = (lambda x: HedyTester.run_code(x) == 'Hond')

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=check_in_list
        )

    def test_print_var_number(self):
        code = textwrap.dedent("""\
            n is 10
            print n""")
        expected = textwrap.dedent("""\
            n = Value('10', num_sys='Latin')
            print(f'{n}')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='10',
            max_level=11)

    def test_print_var_number_arabic(self):
        code = textwrap.dedent("""\
            n is ١١
            print n""")
        expected = textwrap.dedent("""\
            n = Value('11', num_sys='Arabic')
            print(f'{n}')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='١١',
            max_level=11)

    def test_print_keyword_var(self):
        code = textwrap.dedent("""\
            sum is 10
            print sum""")
        expected = textwrap.dedent("""\
            _sum = Value('10', num_sys='Latin')
            print(f'{_sum}')""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='10',
            max_level=11)

    def test_print_multi_args(self):
        code = "print 'hello' 'Hedy' 4 ١١"
        expected = """print(f'helloHedy4{localize(11, num_sys="Arabic")}')"""

        self.multi_level_tester(
            code=code,
            expected=expected,
            output='helloHedy4١١',
            max_level=11)

    #
    # ask tests
    #
    def test_ask_single_quoted_text(self):
        code = "details is ask 'tell me more'"
        expected = self.input_transpiled('details', 'tell me more')

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_ask_single_quoted_text_with_inner_double_quote(self):
        code = """details is ask 'say "no"'"""
        expected = self.input_transpiled('details', 'say "no"')

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_ask_double_quoted_text(self):
        code = 'details is ask "tell me more"'
        expected = self.input_transpiled('details', 'tell me more')

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_ask_double_quoted_text_with_inner_single_quote(self):
        code = f'''details is ask "say 'no'"'''
        expected = self.input_transpiled('details', "say \\'no\\'")

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_es(self, q):
        code = f"""color is ask {q}Cuál es tu color favorito?{q}"""
        expected = self.input_transpiled("color", 'Cuál es tu color favorito?')

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_bengali_var(self, q):
        code = textwrap.dedent(f"""\
            রং is ask {q}আপনার প্রিয় রং কি?{q}
            print রং {q} is আপনার প্রিয{q}""")

        expected = self.dedent(
            self.input_transpiled('রং', 'আপনার প্রিয় রং কি?'),
            "print(f'{রং} is আপনার প্রিয')")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_ask_forward(self):
        code = textwrap.dedent("""\
            afstand is ask 'hoe ver dan?'
            forward afstand""")

        expected = self.dedent(
            self.input_transpiled('afstand', 'hoe ver dan?'),
            self.forward_transpiled('afstand.data'))

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    def test_ask_number(self):
        code = "n is ask 42"
        expected = self.input_transpiled('n', '42')

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_ask_arabic_number(self):
        code = "n is ask ٢٣٤"
        expected = self.input_transpiled('n', '{localize(234, num_sys="Arabic")}')

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_ask_multi_args(self):
        code = "n is ask 'hello' 'Hedy' 4 ١١"
        expected = self.input_transpiled('n', 'helloHedy4{localize(11, num_sys="Arabic")}')

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_ask_number_var(self):
        code = textwrap.dedent("""\
            number is 10
            favorite is ask 'Is your fav number' number""")

        expected = self.dedent(
            "number = Value('10', num_sys='Latin')",
            self.input_transpiled('favorite', 'Is your fav number{number}'))

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_ask_arabic_number_var(self):
        code = textwrap.dedent("""\
             number is ١١
             favorite is ask 'Is it ' number""")

        expected = self.dedent(
            "number = Value('11', num_sys='Arabic')",
            self.input_transpiled('favorite', 'Is it {number}'))

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_ask_with_keyword_var(self):
        code = textwrap.dedent("""\
            sum is Hedy
            v is ask sum""")

        expected = self.dedent(
            "_sum = Value('Hedy')",
            self.input_transpiled('v', '{_sum}'))

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True, skip_faulty=False)

    def test_ask_list_access_index(self):
        code = textwrap.dedent("""\
            colors is orange, blue, green
            favorite is ask 'Is your fav color ' colors at 1""")

        expected = self.dedent(
            "colors = Value([Value('orange'), Value('blue'), Value('green')])",
            self.list_access_transpiled('colors.data[int(1)-1]'),
            self.input_transpiled('favorite', 'Is your fav color {colors.data[int(1)-1]}'))

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_ask_list_random(self):
        code = textwrap.dedent("""\
            colors is orange, blue, green
            favorite is ask 'Is your fav color ' colors at random""")

        expected = self.dedent(
            "colors = Value([Value('orange'), Value('blue'), Value('green')])",
            self.list_access_transpiled('random.choice(colors.data)'),
            self.input_transpiled('favorite', 'Is your fav color {random.choice(colors.data)}'))

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_ask_list_random_fr(self):
        code = textwrap.dedent("""\
            animaux est chien, chat, kangourou
            a est demande animaux au hasard""")

        expected = self.dedent(
            "animaux = Value([Value('chien'), Value('chat'), Value('kangourou')])",
            self.list_access_transpiled('random.choice(animaux.data)'),
            self.input_transpiled('a', '{random.choice(animaux.data)}'))

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            lang='fr',
            unused_allowed=True
        )

    def test_ask_string_var(self):
        code = textwrap.dedent("""\
            color is orange
            favorite is ask 'Is your fav color ' color""")

        expected = self.dedent(
            "color = Value('orange')",
            self.input_transpiled('favorite', 'Is your fav color {color}'))

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_ask_with_comma(self):
        code = textwrap.dedent("""\
            dieren is ask 'hond, kat, kangoeroe'
            print dieren""")

        expected = self.dedent(
            self.input_transpiled('dieren', 'hond, kat, kangoeroe'),
            "print(f'{dieren}')")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_ask_equals(self):
        code = "antwoord = ask 'wat is je lievelingskleur?'"
        expected = self.input_transpiled('antwoord', 'wat is je lievelingskleur?')

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_ask_chained(self):
        code = textwrap.dedent("""\
            a is ask 'What is a?'
            b is ask 'Are you sure a is ' a '?'
            print a b""")

        expected = self.dedent(
            self.input_transpiled('a', 'What is a?'),
            self.input_transpiled('b', 'Are you sure a is {a}?'),
            "print(f'{a}{b}')")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # forward tests
    #
    def test_forward_with_number_var(self):
        code = textwrap.dedent("""\
            distance is 70
            forward distance""")
        expected = self.dedent(
            "distance = Value('70', num_sys='Latin')",
            self.forward_transpiled('distance.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    def test_forward_with_non_latin_number_var(self):
        code = textwrap.dedent("""\
            الزاوية هو ٩٠
            تقدم الزاوية""")
        expected = self.dedent(
            "الزاوية = Value('90', num_sys='Arabic')",
            self.forward_transpiled('الزاوية.data'))

        self.multi_level_tester(
            code=code,
            lang='ar',
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11,
        )

    def test_forward_with_keyword_variable(self):
        code = textwrap.dedent("""\
           sum is 50
           forward sum""")
        expected = self.dedent(
            "_sum = Value('50', num_sys='Latin')",
            self.forward_transpiled('_sum.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11)

    def test_forward_with_list_access(self):
        code = textwrap.dedent("""\
            distance is 10, 100
            forward distance at 1""")

        expected = self.dedent(
            "distance = Value([Value('10', num_sys='Latin'), Value('100', num_sys='Latin')])",
            self.list_access_transpiled('distance.data[int(1)-1]'),
            self.forward_transpiled('distance.data[int(1)-1].data'))

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_forward_with_list_access_random(self):
        code = textwrap.dedent("""\
            distance is 10, 100, 360
            forward distance at random""")

        expected = self.dedent(
            "distance = Value([Value('10', num_sys='Latin'), Value('100', num_sys='Latin'), Value('360', num_sys='Latin')])",
            self.list_access_transpiled('random.choice(distance.data)'),
            self.forward_transpiled('random.choice(distance.data).data'))

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_forward_with_list_calc(self):
        code = "forward 100 - 50"
        expected = self.forward_transpiled('100 - 50')

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_forward_with_list_arabic_calc(self):
        code = "forward ٩٠ - ١٠"
        expected = self.forward_transpiled('90 - 10')

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    #
    # turn tests
    #
    def test_turn_with_number_var(self):
        code = textwrap.dedent("""\
            direction is 70
            turn direction""")
        expected = self.dedent(
            "direction = Value('70', num_sys='Latin')",
            self.turn_transpiled('direction.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    def test_turn_with_non_latin_number_var(self):
        code = textwrap.dedent("""\
            الزاوية هو ٩٠
            استدر الزاوية""")
        expected = self.dedent(
            "الزاوية = Value('90', num_sys='Arabic')",
            self.turn_transpiled('الزاوية.data'))

        self.multi_level_tester(
            code=code,
            lang='ar',
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11,
        )

    def test_turn_with_non_ascii_var(self):
        code = textwrap.dedent("""\
            ángulo is 90
            turn ángulo""")
        expected = self.dedent(
            "ángulo = Value('90', num_sys='Latin')",
            self.turn_transpiled('ángulo.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            expected_commands=['is', 'turn'],
            max_level=11,
        )

    def test_turn_with_keyword_var(self):
        code = textwrap.dedent("""\
            sum is 70
            turn sum""")
        expected = self.dedent(
            "_sum = Value('70', num_sys='Latin')",
            self.turn_transpiled('_sum.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    def test_turn_with_list_access(self):
        code = textwrap.dedent("""\
            directions is 10, 100
            turn directions at 1""")

        expected = self.dedent(
            "directions = Value([Value('10', num_sys='Latin'), Value('100', num_sys='Latin')])",
            self.list_access_transpiled('directions.data[int(1)-1]'),
            self.turn_transpiled('directions.data[int(1)-1].data'))

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_turn_with_list_access_random(self):
        code = textwrap.dedent("""\
            directions is 10, 100, 360
            turn directions at random""")

        expected = self.dedent(
            "directions = Value([Value('10', num_sys='Latin'), Value('100', num_sys='Latin'), Value('360', num_sys='Latin')])",
            self.list_access_transpiled('random.choice(directions.data)'),
            self.turn_transpiled('random.choice(directions.data).data'))

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_random_turtle_dutch(self):
        lang = 'nl'
        code = textwrap.dedent("""\
            lijstkleuren is blauw, groen, wit
            kleur lijstkleuren at random
            vooruit 10""")

        expected = self.dedent(
            "lijstkleuren = Value([Value('blauw'), Value('groen'), Value('wit')])",
            self.color_transpiled("{random.choice(lijstkleuren.data)}", lang),
            self.forward_transpiled('10'))

        self.multi_level_tester(
            max_level=11,
            code=code,
            lang=lang,
            translate=False,
            expected=expected
        )

    def test_turn_with_calc(self):
        code = "turn 100 - 50"
        expected = self.turn_transpiled('100 - 50')

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    #
    # color tests
    #
    def test_color_with_var(self):
        code = textwrap.dedent("""\
            foo is white
            color foo""")
        expected = self.dedent(
            "foo = Value('white')",
            self.color_transpiled('{foo}')
        )

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    def test_color_with_keyword_var(self):
        code = textwrap.dedent("""\
            sum is white
            color sum""")
        expected = self.dedent(
            "_sum = Value('white')",
            self.color_transpiled('{_sum}')
        )

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=11
        )

    def test_color_with_list_access(self):
        code = textwrap.dedent("""\
            colors is red, green, blue
            color colors at 2""")

        expected = self.dedent(
            "colors = Value([Value('red'), Value('green'), Value('blue')])",
            self.color_transpiled('{colors.data[int(2)-1]}'))

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    def test_color_with_list_access_random(self):
        code = textwrap.dedent("""\
            colors is red, green, blue
            color colors at random""")

        expected = self.dedent(
            "colors = Value([Value('red'), Value('green'), Value('blue')])",
            self.color_transpiled('{random.choice(colors.data)}'))

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
        )

    #
    # sleep tests
    #
    def test_sleep_with_number_variable(self):
        code = textwrap.dedent("""\
            time is 10
            sleep time""")

        expected = self.dedent(
            "_time = Value('10', num_sys='Latin')",
            self.sleep_transpiled('_time.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11)

    def test_sleep_with_number_variable_hi(self):
        code = textwrap.dedent("""\
            n is २
            sleep n""")
        expected = self.dedent(
            "n = Value('2', num_sys='Devanagari')",
            self.sleep_transpiled("n.data"))

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_sleep_with_keyword_variable(self):
        code = textwrap.dedent("""\
            sum is 2
            sleep sum""")
        expected = self.dedent(
            "_sum = Value('2', num_sys='Latin')",
            self.sleep_transpiled("_sum.data"))

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_sleep_with_calc_variable(self):
        code = textwrap.dedent("""\
            n is 1 * 2 + 3
            sleep n""")
        expected = self.dedent(
            f"""n = Value({self.number_transpiled("1 * 2")} + {self.number_transpiled(3)}, num_sys='Latin')""",
            self.sleep_transpiled("n.data"))

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_sleep_with_calc(self):
        code = "sleep 1 * 2 + 3"
        expected = self.sleep_transpiled(f'"{self.number_transpiled("1 * 2")} + {self.number_transpiled(3)}"')

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_sleep_with_list_access(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n at 1""")

        expected = self.dedent(
            "n = Value([Value('1', num_sys='Latin'), Value('2', num_sys='Latin'), Value('3', num_sys='Latin')])",
            self.list_access_transpiled('n.data[int(1)-1]'),
            self.sleep_transpiled('n.data[int(1)-1].data'))

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_sleep_with_list_random(self):
        code = textwrap.dedent("""\
            n is 1, 2, 3
            sleep n at random""")

        expected = self.dedent(
            "n = Value([Value('1', num_sys='Latin'), Value('2', num_sys='Latin'), Value('3', num_sys='Latin')])",
            self.list_access_transpiled('random.choice(n.data)'),
            self.sleep_transpiled('random.choice(n.data).data'))

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_sleep_with_input_variable(self):
        code = textwrap.dedent("""\
            n is ask "how long"
            sleep n""")

        expected = self.dedent(
            self.input_transpiled('n', 'how long'),
            self.sleep_transpiled("n.data"))

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    #
    # play tests
    #
    def test_play_var(self):
        code = textwrap.dedent("""\
            n is C4
            play n""")

        expected = self.dedent(
            "n = Value('C4')",
            self.play_transpiled('n.data'))

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected,
            max_level=11
        )

    def test_play_arabic_number_var(self):
        code = textwrap.dedent("""\
            n is ١١
            play n""")

        expected = self.dedent(
            "n = Value('11', num_sys='Arabic')",
            self.play_transpiled('n.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11
        )

    def test_play_keyword_var(self):
        code = textwrap.dedent("""\
            return is C4
            play return""")

        expected = self.dedent(
            "_return = Value('C4')",
            self.play_transpiled('_return.data'))

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11)

    def test_play_list_access(self):
        code = textwrap.dedent("""\
            notes is C4, E4, D4, F4, G4
            play notes at 4""")

        expected = self.dedent(
            "notes = Value([Value('C4'), Value('E4'), Value('D4'), Value('F4'), Value('G4')])",
            self.play_transpiled('notes.data[int(4)-1].data'))

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=11
        )

    def test_play_list_access_random(self):
        code = textwrap.dedent("""\
            notes is C4, E4, D4, F4, G4
            play notes at random""")

        expected = self.dedent(
            "notes = Value([Value('C4'), Value('E4'), Value('D4'), Value('F4'), Value('G4')])",
            self.play_transpiled('random.choice(notes.data).data'))

        self.multi_level_tester(
            code=code,
            translate=False,
            skip_faulty=False,
            unused_allowed=True,
            expected=expected,
            max_level=11
        )

    def test_play_calc_sum(self):
        code = "play 30 + 11"
        expected = self.play_transpiled('30 + 11')

        self.multi_level_tester(code=code, expected=expected)

    def test_play_arabic_calc(self):
        code = "play ٣١ + ١"
        expected = self.play_transpiled('31 + 1')

        self.multi_level_tester(code=code, expected=expected)

    def test_play_calc_with_var(self):
        code = textwrap.dedent(f"""\
            note is 34
            play note + 1""")
        expected = self.dedent(
            "note = Value('34', num_sys='Latin')",
            self.play_transpiled(f"{self.number_transpiled('note')} + {self.number_transpiled(1)}"))

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # assign tests
    #
    def test_assign_keyword_var(self):
        code = "sum is Felienne"
        expected = "_sum = Value('Felienne')"

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_catalan_var_name(self):
        code = textwrap.dedent("""\
            pel·lícula is Sonic the Hedgehog 2
            print 'Veurem una ' pel·lícula""")

        expected = textwrap.dedent("""\
            pel·lícula = Value('Sonic the Hedgehog 2')
            print(f'Veurem una {pel·lícula}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_comment(self):
        code = 'test is "Welkom bij Hedy" # This is a comment'
        expected = 'test = Value(\'"Welkom bij Hedy" \')'
        self.multi_level_tester(
            max_level=11,
            unused_allowed=True,
            code=code,
            expected=expected
        )

    def test_assign(self):
        code = "naam is Felienne"
        expected = "naam = Value('Felienne')"

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_var_to_var(self):
        code = textwrap.dedent("""\
        dier1 is hond
        dier2 is dier1
        print dier2""")

        expected = textwrap.dedent("""\
        dier1 = Value('hond')
        dier2 = dier1
        print(f'{dier2}')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_assign_text_with_inner_single_quote(self):
        code = "var is Hedy's"
        expected = "var = Value('Hedy\\'s')"

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_text_with_inner_double_quote(self):
        code = 'var is It says "Hedy"'
        expected = """var = Value('It says "Hedy"')"""

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_single_quoted_text(self):
        code = """message is 'Hello welcome to Hedy.'"""
        expected = """message = Value('\\'Hello welcome to Hedy.\\'')"""
        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_double_quoted_text(self):
        code = '''message is "Hello welcome to Hedy."'''
        expected = """message = Value('"Hello welcome to Hedy."')"""
        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_list(self):
        code = "dieren is Hond, Kat, Kangoeroe"
        expected = "dieren = Value([Value('Hond'), Value('Kat'), Value('Kangoeroe')])"

        self.multi_level_tester(max_level=11, code=code, expected=expected, unused_allowed=True)

    def test_assign_list_index(self):
        code = textwrap.dedent("""\
            animals is dog, cat, platypus
            a = animals at 3""")
        expected = self.dedent(
            "animals = Value([Value('dog'), Value('cat'), Value('platypus')])",
            self.list_access_transpiled('animals.data[int(3)-1]'),
            "a = animals.data[int(3)-1]")

        self.multi_level_tester(max_level=11, code=code, expected=expected, unused_allowed=True)

    def test_assign_list_random(self):
        code = textwrap.dedent("""\
            animals is dog, cat, platypus
            a = animals at random""")
        expected = self.dedent(
            "animals = Value([Value('dog'), Value('cat'), Value('platypus')])",
            self.list_access_transpiled('random.choice(animals.data)'),
            "a = random.choice(animals.data)")

        self.multi_level_tester(max_level=11, code=code, expected=expected, unused_allowed=True)

    def test_assign_list_with_arabic_comma(self):
        code = "صديقي هو احمد، خالد، حسن"
        expected = "صديقي = Value([Value('احمد'), Value('خالد'), Value('حسن')])"

        self.multi_level_tester(
            max_level=11,
            code=code,
            unused_allowed=True,
            expected=expected,
            lang='ar'
        )

    def test_assign_list_with_dutch_comma_arabic_lang(self):
        code = "صديقي هو احمد, خالد, حسن"
        expected = "صديقي = Value([Value('احمد'), Value('خالد'), Value('حسن')])"

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            lang='ar',
            unused_allowed=True,
            # translation must be off because the Latin commas will be converted to arabic commas and this is correct
            translate=False
        )

    def test_assign_list_with_arabic_comma_and_is(self):
        code = "animals هو cat، dog، platypus"
        expected = "animals = Value([Value('cat'), Value('dog'), Value('platypus')])"

        self.multi_level_tester(
            max_level=11,
            code=code,
            unused_allowed=True,
            expected=expected,
            lang='ar'
        )

    def test_assign_list_with_spaces(self):
        # spaces are parsed in the text here, that is fine (could be avoided if we say text
        # can't *end* (or start) in a space but I find this ok for now
        code = "dieren is Hond , Kat , Kangoeroe"
        expected = "dieren = Value([Value('Hond '), Value('Kat '), Value('Kangoeroe')])"

        self.multi_level_tester(max_level=11, code=code, expected=expected, unused_allowed=True)

    def test_assign_list_exclamation_mark(self):
        code = textwrap.dedent("""\
            antwoorden is ja, NEE!, misschien
            print antwoorden at random""")

        expected = self.dedent(
            "antwoorden = Value([Value('ja'), Value('NEE!'), Value('misschien')])",
            self.list_access_transpiled("random.choice(antwoorden.data)"),
            "print(f'{random.choice(antwoorden.data)}')")

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_assign_list_values_with_inner_quotes(self):
        code = """dieren is Hond's, Kat"s, 'Kangoeroe', "Muis\""""
        expected = """dieren = Value([Value('Hond\\\'s'), Value('Kat"s'), Value('\\\'Kangoeroe\\\''), Value('"Muis"')])"""

        self.multi_level_tester(max_level=11, code=code, expected=expected, unused_allowed=True)

    def test_assign_list_values_with_inner_single_quotes(self):
        code = textwrap.dedent(f"""\
            taart is 'appeltaart, choladetaart, kwarktaart'
            print 'we bakken een ' taart at random""")

        expected = self.dedent(
            "taart = Value([Value('\\'appeltaart'), Value('choladetaart'), Value('kwarktaart\\'')])",
            self.list_access_transpiled('random.choice(taart.data)'),
            "print(f'we bakken een {random.choice(taart.data)}')")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_list_values_with_inner_double_quotes(self):
        code = textwrap.dedent(f"""\
            taart is "appeltaart, choladetaart, kwarktaart"
            print 'we bakken een ' taart at random""")

        expected = self.dedent(
            "taart = Value([Value('\"appeltaart'), Value('choladetaart'), Value('kwarktaart\"')])",
            self.list_access_transpiled('random.choice(taart.data)'),
            "print(f'we bakken een {random.choice(taart.data)}')")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_list_with_double_quoted_values(self):
        code = textwrap.dedent(f"""\
            taart is "appeltaart, choladetaart, kwarktaart"
            print 'we bakken een' taart at random""")

        expected = self.dedent(
            "taart = Value([Value('\"appeltaart'), Value('choladetaart'), Value('kwarktaart\"')])",
            self.list_access_transpiled('random.choice(taart.data)'),
            "print(f'we bakken een{random.choice(taart.data)}')")

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_list_with_single_quoted_values(self):
        code = textwrap.dedent(f"""\
            taart is 'appeltaart', 'choladetaart', 'kwarktaart'
            print 'we bakken een' taart at random""")

        expected = self.dedent(
            "taart = Value([Value('\\'appeltaart\\''), Value('\\'choladetaart\\''), Value('\\'kwarktaart\\'')])",
            self.list_access_transpiled('random.choice(taart.data)'),
            "print(f'we bakken een{random.choice(taart.data)}')")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_period(self):
        code = "period is ."
        expected = "period = Value('.')"

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_print(self):
        code = textwrap.dedent("""\
        naam is Hedy
        print 'ik heet' naam""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        print(f'ik heet{naam}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_random_value(self):
        code = textwrap.dedent("""\
            dieren is hond, kat, kangoeroe
            dier is dieren at random
            print dier""")

        expected = self.dedent(
            "dieren = Value([Value('hond'), Value('kat'), Value('kangoeroe')])",
            self.list_access_transpiled("random.choice(dieren.data)"),
            "dier = random.choice(dieren.data)",
            "print(f'{dier}')")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            extra_check_function=self.result_in(['Hond', 'Kat', 'Kangoeroe'])
        )

    def test_assign_print_chinese(self):
        code = textwrap.dedent("""\
        你世界 is 你好世界
        print 你世界""")

        expected = textwrap.dedent("""\
        你世界 = Value('你好世界')
        print(f'{你世界}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_text_to_hungarian_var(self):
        code = "állatok is kutya"
        expected = "állatok = Value('kutya')"

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_bengali_var(self):
        var = hedy.escape_var("নাম")
        code = "নাম is হেডি"
        expected = f"{var} = Value('হেডি')"

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_single_quoted_string(self):
        code = "naam is 'Felienne'"
        expected = "naam = Value('\\'Felienne\\'')"

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_double_quoted_string(self):
        code = 'naam is "Felienne"'
        expected = """naam = Value('"Felienne"')"""

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_integer(self):
        code = "naam is 14"
        expected = "naam = Value('14', num_sys='Latin')"

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_python_keyword(self):
        code = "for is Hedy"
        expected = "_for = Value('Hedy')"

        self.multi_level_tester(code=code, expected=expected, max_level=11, unused_allowed=True)

    def test_assign_var_with_underscore(self):
        code = textwrap.dedent("""\
        voor_naam is Hedy
        print 'ik heet ' voor_naam""")

        expected = textwrap.dedent("""\
        voor_naam = Value('Hedy')
        print(f'ik heet {voor_naam}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_with_equals(self):
        code = "name = Hedy"
        expected = "name = Value('Hedy')"

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            unused_allowed=True
        )

    def test_assign_with_equals_no_space(self):
        code = "name=Hedy"
        expected = "name = Value('Hedy')"

        self.multi_level_tester(
            max_level=11,
            code=code,
            unused_allowed=True,
            expected=expected
        )

    def test_assign_list_with_equals(self):
        code = "name = Hedy, Lamar"
        expected = "name = Value([Value('Hedy'), Value('Lamar')])"

        self.multi_level_tester(
            max_level=11,
            code=code,
            unused_allowed=True,
            expected=expected
        )

    def test_assign_text_with_space(self):
        code = textwrap.dedent("""\
        a is 'Hello World'
        print a

        a = 'Hello World'
        print a

        a is Hello World
        print a

        a = Hello World
        print a""")

        expected = textwrap.dedent("""\
        a = Value('\\'Hello World\\'')
        print(f'{a}')
        a = Value('\\'Hello World\\'')
        print(f'{a}')
        a = Value('Hello World')
        print(f'{a}')
        a = Value('Hello World')
        print(f'{a}')""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected
        )

    def test_assign_subtract_negative_number(self):
        code = textwrap.dedent("""\
            n = -3-4
            print n""")

        expected = textwrap.dedent(f"""\
            n = Value(-3 - 4, num_sys='Latin')
            print(f'{{n}}')""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected
        )

    #
    # music tests
    #
    @parameterized.expand([
        ('*', '*'),
        ('/', '//'),
        ('+', '+'),
        ('-', '-')
    ])
    def test_play_calculation(self, op, exp_op):
        op = "*"
        exp_op = '*'
        code = textwrap.dedent(f"""\
            note is 34
            play note {op} 1""")
        expected = self.dedent(
            "note = Value('34', num_sys='Latin')",
            self.play_transpiled(f'{self.number_transpiled("note")} {exp_op} {self.number_transpiled(1)}'))

        self.multi_level_tester(
            code=code,
            translate=False,
            expected=expected,
            max_level=11
        )

    #
    # if tests
    #
    def test_if_equality_linebreak_print(self):
        # line breaks after if-condition are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, output='leuk')

    def test_if_equality_linebreak_comment_print(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        # this linebreak is allowed
        print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, output='leuk')

    def test_if_equality_comment_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy  # this linebreak is allowed
        print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, output='leuk')

    def test_if_equality_linebreak_print_comment(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk'  # this linebreak is allowed""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, output='leuk')

    def test_if_equality_trailing_space_linebreak_print(self):
        value = 'trailing_space  '
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {value}
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = Value('James')
        if localize(naam.data) == localize('trailing_space'):
          print(f'shaken')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_text_with_spaces_and_double_quotes_linebreak_print_else_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James "Bond"
        print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
        naam = Value('James')
        if localize(naam.data) == localize('James "Bond"'):
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_text_with_spaces_and_single_quotes_linebreak_print_else_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James 'Bond'
        print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
        naam = Value('James')
        if localize(naam.data) == localize('James \\'Bond\\''):
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_trailing_space_linebreak_print_else(self):
        value = "trailing space  "
        code = textwrap.dedent(f"""\
           naam is James
           if naam is {value} 
           print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
           naam = Value('James')
           if localize(naam.data) == localize('trailing space'):
             print(f'shaken')
           else:
             print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_unquoted_rhs_with_space_and_trailing_space_linebreak_print(self):
        value = "trailing space "
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {value}
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = Value('James')
        if localize(naam.data) == localize('trailing space'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_equality_unquoted_rhs_with_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = Value('James')
        if localize(naam.data) == localize('James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_equality_unquoted_with_space_linebreak_print_else_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond
        print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
        naam = Value('James')
        if localize(naam.data) == localize('James Bond'):
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_single_quoted_rhs_with_inner_double_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is 'He said "no"' print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = Value('no')
        if localize(answer.data) == localize('He said "no"'):
          print(f'no')""")

        self.multi_level_tester(code=code, expected=expected, max_level=7, skip_faulty=False)

    def test_if_equality_double_quoted_rhs_with_inner_single_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is "He said 'no'" print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = Value('no')
        if localize(answer.data) == localize('He said \\'no\\''):
          print(f'no')""")

        self.multi_level_tester(code=code, expected=expected, max_level=7, skip_faulty=False)

    def test_if_2_vars_equality_print(self):
        code = textwrap.dedent("""\
        jouwkeuze is schaar
        computerkeuze is schaar
        if computerkeuze is jouwkeuze print 'gelijkspel!'""")

        expected = textwrap.dedent("""\
        jouwkeuze = Value('schaar')
        computerkeuze = Value('schaar')
        if localize(computerkeuze.data) == localize(jouwkeuze.data):
          print(f'gelijkspel!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, output='gelijkspel!')

    def test_if_french(self):
        code = textwrap.dedent("""\
            plat_principal = demande "Quel plat principal souhaitez-vous?"
            prix = 0
            si plat_principal est lasagnes prix = 12
            affiche "Ce sera " prix""")

        expected = self.dedent(
            self.input_transpiled('plat_principal', 'Quel plat principal souhaitez-vous?'),
            f"""\
            prix = {self.value(0)}
            if localize(plat_principal.data) == localize('lasagnes'):
              prix = {self.value(12)}
            else:
              x__x__x__x = {self.value(5)}
            print(f'Ce sera {{prix}}')""")

        self.multi_level_tester(max_level=7,
                                code=code,
                                expected=expected,
                                lang='fr')

    def test_if_arabic_number_equals_latin_number(self):
        code = textwrap.dedent("""\
        if ١١ is 11 print 'correct'""")

        expected = textwrap.dedent("""\
        if localize('11') == localize('11'):
          print(f'correct')""")

        self.multi_level_tester(code=code, expected=expected, max_level=7, output='correct')

    def test_if_arabic_var_equals_latin_number(self):
        code = textwrap.dedent("""\
        a is ١١
        if a is 11 print 'correct'""")

        expected = textwrap.dedent("""\
        a = Value('11', num_sys='Arabic')
        if localize(a.data) == localize('11'):
          print(f'correct')""")

        self.multi_level_tester(code=code, expected=expected, max_level=7, output='correct')

    def test_equality_arabic_and_latin_vars(self):
        code = textwrap.dedent("""\
        nummer1 is ٢
        nummer2 is 2
        if nummer1 is nummer2 print 'jahoor!'""")

        expected = textwrap.dedent(f"""\
        nummer1 = {self.value(2, "Arabic")}
        nummer2 = {self.value(2)}
        if localize(nummer1.data) == localize(nummer2.data):
          print(f'jahoor!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, output='jahoor!')

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_space(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}James Bond{q} print {q}shaken{q}""")

        expected = textwrap.dedent(f"""\
        naam = Value('James')
        if localize(naam.data) == localize('James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_spaces(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}Bond James Bond{q} print 'shaken'""")

        expected = textwrap.dedent(f"""\
        naam = Value('James')
        if localize(naam.data) == localize('Bond James Bond'):
          print(f'shaken')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_equality_promotes_int_to_string(self):
        code = textwrap.dedent("""\
        a is test
        b is 15
        if a is b c is 1""")

        expected = textwrap.dedent("""\
        a = Value('test')
        b = Value('15', num_sys='Latin')
        if localize(a.data) == localize(b.data):
          c = Value('1', num_sys='Latin')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, unused_allowed=True)

    def test_if_equality_assign_calc(self):
        code = textwrap.dedent("""\
        cmp is 1
        test is 2
        acu is 0
        if test is cmp acu is acu + 1""")

        expected = textwrap.dedent(f"""\
        cmp = Value('1', num_sys='Latin')
        test = Value('2', num_sys='Latin')
        acu = Value('0', num_sys='Latin')
        if localize(test.data) == localize(cmp.data):
          acu = Value({self.number_transpiled('acu')} + {self.number_transpiled(1)}, num_sys=get_num_sys(acu))""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_with_is(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_with_equals_sign(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam = Hedy print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    #
    # if else tests
    #
    def test_if_equality_var_and_number(self):
        code = textwrap.dedent("""\
        naam is 5
        if naam is 5 print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('5', num_sys='Latin')
        if localize(naam.data) == localize('5'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, output='leuk')

    def test_if_equality_arabic_var_and_latin_number(self):
        code = textwrap.dedent("""\
        naam is ٥
        if naam is 5 print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('5', num_sys='Arabic')
        if localize(naam.data) == localize('5'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, output='leuk')

    def test_if_equality_latin_var_and_arabic_number(self):
        code = textwrap.dedent("""\
        naam is 5
        if naam is ٥ print 'leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('5', num_sys='Latin')
        if localize(naam.data) == localize('5'):
          print(f'leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, output='leuk')

    def test_if_equality_print_else_print(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk' else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, output='leuk')

    def test_if_ask_equality_print_else_print(self):
        code = textwrap.dedent("""\
            kleur is ask 'Wat is je lievelingskleur?'
            if kleur is groen print 'mooi!' else print 'niet zo mooi'""")

        expected = self.dedent(
            self.input_transpiled('kleur', 'Wat is je lievelingskleur?'),
            """\
            if localize(kleur.data) == localize('groen'):
              print(f'mooi!')
            else:
              print(f'niet zo mooi')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_else_followed_by_print(self):
        code = textwrap.dedent("""\
        kleur is geel
        if kleur is groen antwoord is ok else antwoord is stom
        print antwoord""")

        expected = textwrap.dedent("""\
        kleur = Value('geel')
        if localize(kleur.data) == localize('groen'):
          antwoord = Value('ok')
        else:
          antwoord = Value('stom')
        print(f'{antwoord}')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_assign_else_assign(self):
        code = textwrap.dedent("""\
        cmp is 1
        test is 2
        acu is 0
        if test is cmp
        acu is acu + 1
        else
        acu is acu + 5""")

        expected = textwrap.dedent(f"""\
        cmp = {self.value(1)}
        test = {self.value(2)}
        acu = {self.value(0)}
        if localize(test.data) == localize(cmp.data):
          acu = Value({self.number_transpiled('acu')} + {self.number_transpiled(1)}, num_sys=get_num_sys(acu))
        else:
          acu = Value({self.number_transpiled('acu')} + {self.number_transpiled(5)}, num_sys=get_num_sys(acu))""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_with_negative_number(self):
        code = textwrap.dedent("""\
            antwoord is -10
            if antwoord is -10 print 'Nice' else print 'Oh no'""")

        expected = textwrap.dedent("""\
            antwoord = Value('-10', num_sys='Latin')
            if localize(antwoord.data) == localize('-10'):
              print(f'Nice')
            else:
              print(f'Oh no')""")

        self.multi_level_tester(code=code, expected=expected, output='Nice', max_level=7)

    # Legal syntax:
    #
    # if name is Hedy print 'hello'
    # if name is 'Hedy' print 'hello'
    # if name is 'Hedy is het beste' print 'hello'
    # if name is Hedy c is 5

    # Illegal syntax:
    #
    # if name is Hedy is het beste print 'hello'
    # if name is Hedy is het beste x is 5

    def test_if_equality_print_linebreak_else_print(self):
        # line break before else is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk'
        else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            expected=expected,
            expected_commands=['is', 'if', 'else', 'print', 'print']
        )

    def test_if_equality_linebreak_print_else_print(self):
        # line break after if-condition is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk' else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_print_else_linebreak_print(self):
        # line break after else is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk' else
        print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_linebreak_print_linebreak_else_print(self):
        # line breaks after if-condition and before else are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk'
        else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_linebreak_print_linebreak_else_linebreak_print(self):
        # line breaks after if-condition, before else and after else are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk'
        else
        print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_linebreak_print_else_linebreak_print(self):
        # line breaks after if-condition and after else are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk' else
        print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = Value('Hedy')
        if localize(naam.data) == localize('Hedy'):
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_space_else(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}James Bond{q} print {q}shaken{q} else print {q}biertje!{q}""")

        expected = textwrap.dedent(f"""\
        naam = Value('James')
        if localize(naam.data) == localize('James Bond'):
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    #
    # arithmetic expressions tests
    #
    def test_print_multiplication(self):
        code = "print 5 * 5"
        expected = """print(f'{localize(5 * 5, num_sys="Latin")}')"""
        output = '25'

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    def test_print_addition(self):
        code = "print 5 + 5"
        expected = """print(f'{localize(5 + 5, num_sys="Latin")}')"""
        output = '10'

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    def test_print_subtraction_without_text(self):
        code = "print 5 - 5"
        expected = """print(f'{localize(5 - 5, num_sys="Latin")}')"""
        output = '0'

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    def test_print_subtraction_with_text(self):
        code = "print 'And the winner is ' 5 - 5"
        expected = """print(f'And the winner is {localize(5 - 5, num_sys="Latin")}')"""
        output = 'And the winner is 0'

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            output=output)

    def test_print_nested_calcs(self):
        code = "print 5 * 5 * 5"
        expected = f"""print(f'{{localize({self.number_transpiled('5 * 5')} * {self.number_transpiled(5)}, num_sys="Latin")}}')"""
        output = '125'

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    def test_assign_calc_print_var(self):
        code = textwrap.dedent("""\
        nummer is 4 + 5
        print nummer""")

        expected = textwrap.dedent("""\
        nummer = Value(4 + 5, num_sys='Latin')
        print(f'{nummer}')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected, output='9')

    def test_assign_calc_no_space(self):
        code = "nummer is 4+5"
        expected = "nummer = Value(4 + 5, num_sys='Latin')"

        self.multi_level_tester(max_level=11, code=code, expected=expected, unused_allowed=True)

    def test_print_calc_with_var(self):
        code = textwrap.dedent("""\
        var is 5
        print var + 5""")
        expected = textwrap.dedent(f"""\
        var = Value('5', num_sys='Latin')
        print(f'{{localize({self.number_transpiled('var')} + {self.number_transpiled('5')}, num_sys=get_num_sys(var))}}')""")

        self.multi_level_tester(max_level=11, code=code, output='10', expected=expected)

    def test_print_calc_with_arabic_var(self):
        code = textwrap.dedent("""\
        var is ٨
        print var + ١""")
        expected = textwrap.dedent(f"""\
        var = Value('8', num_sys='Arabic')
        print(f'{{localize({self.number_transpiled('var')} + {self.number_transpiled('1')}, num_sys=get_num_sys(var))}}')""")

        self.multi_level_tester(max_level=11, code=code, output='٩', expected=expected)

    @parameterized.expand(HedyTester.arithmetic_operations)
    # issue 2067
    def test_assign_calc_precedes_quoted_string(self, operation):
        code = f"a is '3{operation}10'"  # gets parsed to arithmetic operation of '3 and 10'

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand([
        ('*', '*', '16'),
        ('/', '//', '4'),
        ('+', '+', '10'),
        ('-', '-', '6')
    ])
    def test_assign_calc_with_vars(self, op, transpiled_op, output):
        code = textwrap.dedent(f"""\
        nummer is 8
        nummer2 is 2
        getal is nummer {op} nummer2
        print getal""")

        expected = textwrap.dedent(f"""\
        nummer = Value('8', num_sys='Latin')
        nummer2 = Value('2', num_sys='Latin')
        getal = Value({self.number_transpiled('nummer')} {transpiled_op} {self.number_transpiled('nummer2')}, num_sys=get_num_sys(nummer))
        print(f'{{getal}}')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    @parameterized.expand([
        ('*', '*', '16'),
        ('/', '//', '4'),
        ('+', '+', '10'),
        ('-', '-', '6')
    ])
    def test_print_calc_with_vars(self, op, transpiled_op, output):
        code = textwrap.dedent(f"""\
        nummer is 8
        nummer2 is 2
        print nummer {op} nummer2""")

        expected = textwrap.dedent(f'''\
        nummer = Value('8', num_sys='Latin')
        nummer2 = Value('2', num_sys='Latin')
        print(f'{{localize({self.number_transpiled('nummer')} {transpiled_op} {self.number_transpiled('nummer2')}, num_sys=get_num_sys(nummer))}}')''')

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    @parameterized.expand([
        ('*', '*', '١٦'),
        ('/', '//', '٤'),
        ('+', '+', '١٠'),
        ('-', '-', '٦')
    ])
    def test_print_calc_with_vars_arabic(self, op, exp_op, output):
        code = textwrap.dedent(f"""\
            n is ٨
            n2 is ٢
            print n {op} n2""")

        expected = textwrap.dedent(f"""\
            n = Value('8', num_sys='Arabic')
            n2 = Value('2', num_sys='Arabic')
            print(f'{{localize({self.number_transpiled('n')} {exp_op} {self.number_transpiled('n2')}, num_sys=get_num_sys(n))}}')""")

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    @parameterized.expand([
        ('*', '*', '16'),
        ('/', '//', '4'),
        ('+', '+', '10'),
        ('-', '-', '6')
    ])
    def test_print_calc_directly(self, op, transpiled_op, output):
        code = f"print 8 {op} 2"
        expected = f'''print(f'{{localize(8 {transpiled_op} 2, num_sys="Latin")}}')'''

        self.multi_level_tester(max_level=11, code=code, expected=expected, output=output)

    @parameterized.expand([
        ('*', '*', '٢٥'),
        ('/', '//', '١'),
        ('+', '+', '١٠'),
        ('-', '-', '٠')])
    def test_print_calc_arabic_directly(self, op, exp_op, out):
        code = f"""قول "٥ ضرب ٥ يساوي " ٥{op}٥"""
        expected = f"""print(f'٥ ضرب ٥ يساوي {{localize(5 {exp_op} 5, num_sys="Arabic")}}')"""
        output = f'٥ ضرب ٥ يساوي {out}'

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            output=output,
            lang='ar')

    @parameterized.expand([
        ('*', '*', '٢٥'),
        ('/', '//', '١'),
        ('+', '+', '١٠'),
        ('-', '-', '٠')])
    def test_print_calc_arabic_directly_in_en(self, op, exp_op, out):
        code = f"""print "nummers" ٥{op}٥"""
        expected = f"""print(f'nummers{{localize(5 {exp_op} 5, num_sys="Arabic")}}')"""
        output = f"""nummers{out}"""
        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected,
            output=output,
            translate=False)

    @parameterized.expand(HedyTester.arithmetic_operations)
    def test_calc_with_text_var_gives_type_error(self, operation):
        code = textwrap.dedent(f"""\
        a is test
        print a {operation} 2""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand(HedyTester.arithmetic_operations)
    def test_calc_with_quoted_string_gives_type_error(self, operation):
        code = textwrap.dedent(f"""\
        a is 1
        print a {operation} 'Test'""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand(HedyTester.arithmetic_operations)
    def test_calc_with_list_var_gives_type_error(self, operation):
        code = textwrap.dedent(f"""\
        a is one, two
        print a {operation} 2""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    @parameterized.expand(['1.5', '1,5'])
    def test_calculation_with_unsupported_float_gives_error(self, number):
        self.multi_level_tester(
            max_level=11,
            code=f"print {number} + 1",
            exception=hedy.exceptions.UnsupportedFloatException
        )

    def test_print_calc_chained_vars(self):
        code = textwrap.dedent("""\
        a is 5
        b is a + 1
        print a + b""")

        expected = textwrap.dedent(f"""\
        a = Value('5', num_sys='Latin')
        b = Value({self.number_transpiled('a')} + {self.number_transpiled(1)}, num_sys=get_num_sys(a))
        print(f'{{localize({self.number_transpiled('a')} + {self.number_transpiled('b')}, num_sys=get_num_sys(a))}}')""")

        self.multi_level_tester(
            code=code,
            max_level=11,
            expected=expected,
            expected_commands=['is', 'is', 'addition', 'print', 'addition'],
            extra_check_function=lambda x: self.run_code(x) == "11"
        )

    def test_type_reassignment_to_proper_type_valid(self):
        code = textwrap.dedent("""\
        a is Hello
        a is 5
        b is a + 1
        print a + b""")

        expected = textwrap.dedent(f"""\
        a = Value('Hello')
        a = Value('5', num_sys='Latin')
        b = Value({self.number_transpiled('a')} + {self.number_transpiled(1)}, num_sys=get_num_sys(a))
        print(f'{{localize({self.number_transpiled('a')} + {self.number_transpiled('b')}, num_sys=get_num_sys(a))}}')""")

        self.multi_level_tester(
            code=code,
            max_level=11,
            expected=expected,
            expected_commands=['is', 'is', 'is', 'addition', 'print', 'addition'],
            extra_check_function=lambda x: self.run_code(x) == "11"
        )

    def test_type_reassignment_to_wrong_type_raises_error(self):
        code = textwrap.dedent("""\
        a is 5
        a is test
        print a + 2""")

        self.multi_level_tester(
            max_level=11,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_cyclic_var_definition_gives_error(self):
        code = "b is b + 1"

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.CyclicVariableDefinitionException,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 1
        )

    #
    # combined tests
    #
    def test_if_calc_else_calc_print(self):
        code = textwrap.dedent("""\
            keuzes is 1, 2, 3, 4, 5, regenworm
            punten is 0
            worp is keuzes at random
            if worp is regenworm punten is punten + 5
            else punten is punten + worp
            print 'dat zijn dan ' punten""")

        expected = self.dedent(
            f"keuzes = {self.list_transpiled(1, 2, 3, 4, 5, 'regenworm')}",
            f"punten = {self.value(0)}",
            self.list_access_transpiled('random.choice(keuzes.data)'),
            f"""\
            worp = random.choice(keuzes.data)
            if localize(worp.data) == localize('regenworm'):
              punten = Value({self.number_transpiled('punten')} + {self.number_transpiled(5)}, num_sys=get_num_sys(punten))
            else:
              punten = Value({self.number_transpiled('punten')} + {self.number_transpiled('worp')}, num_sys=get_num_sys(punten))
            print(f'dat zijn dan {{punten}}')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_consecutive_if_statements(self):
        code = textwrap.dedent("""\
            names is Hedy, Lamar
            name is ask 'What is a name you like?'
            if name is Hedy print 'nice!'
            if name in names print 'nice!'""")

        expected = self.dedent(
            "names = Value([Value('Hedy'), Value('Lamar')])",
            self.input_transpiled('name', 'What is a name you like?'),
            f"""\
            if localize(name.data) == localize('Hedy'):
              print(f'nice!')
            else:
              x__x__x__x = {self.value(5)}
            if {self.in_list_transpiled('name.data', 'names')}:
              print(f'nice!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_consecutive_if_and_if_else_statements(self):
        code = textwrap.dedent("""\
            naam is ask 'hoe heet jij?'
            if naam is Hedy print 'leuk'
            if naam is Python print 'ook leuk'
            else print 'minder leuk!'""")

        expected = self.dedent(
            self.input_transpiled('naam', 'hoe heet jij?'),
            f"""\
            if localize(naam.data) == localize('Hedy'):
              print(f'leuk')
            else:
              x__x__x__x = {self.value(5)}
            if localize(naam.data) == localize('Python'):
              print(f'ook leuk')
            else:
              print(f'minder leuk!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_two_ifs_assign(self):
        code = textwrap.dedent("""\
        order is fries
        if order is fries price is 5
        drink is water
        print drink""")

        expected = textwrap.dedent("""\
        order = Value('fries')
        if localize(order.data) == localize('fries'):
          price = Value('5', num_sys='Latin')
        else:
          x__x__x__x = Value('5', num_sys='Latin')
        drink = Value('water')
        print(f'{drink}')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected, translate=False, unused_allowed=True)

    def test_consecutive_if_else_statements(self):
        code = textwrap.dedent("""\
            names is Hedy, Lamar
            name is ask 'What is a name you like?'
            if name is Hedy print 'nice!' else print 'meh'
            if name in names print 'nice!' else print 'meh'""")

        expected = self.dedent(
            "names = Value([Value('Hedy'), Value('Lamar')])",
            self.input_transpiled('name', 'What is a name you like?'),
            f"""\
            if localize(name.data) == localize('Hedy'):
              print(f'nice!')
            else:
              print(f'meh')
            if {self.in_list_transpiled('name.data', 'names')}:
              print(f'nice!')
            else:
              print(f'meh')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_print_single_number(self):
        code = "print 5"
        expected = 'print(f\'5\')'

        self.multi_level_tester(max_level=11, code=code, expected=expected)

    def test_print_single_number_ar(self):
        code = "قول ٢"
        expected = """print(f'{localize(2, num_sys="Arabic")}')"""

        self.multi_level_tester(max_level=11, code=code, expected=expected, lang='ar')

    def test_negative_variable(self):
        code = textwrap.dedent("""\
        a = -3
        b = a + 3
        print b""")

        expected = textwrap.dedent(f"""\
        a = {self.value(-3)}
        b = Value({self.number_transpiled('a')} + {self.number_transpiled(3)}, num_sys=get_num_sys(a))
        print(f'{{b}}')""")

        self.multi_level_tester(code=code, expected=expected, output='0', max_level=11)

    def test_turtle_with_expression(self):
        code = textwrap.dedent("""\
            num = 10
            turn num + 10
            forward 10 + num""")

        expected = self.dedent(
            "num = Value('10', num_sys='Latin')",
            self.turn_transpiled(f"{self.number_transpiled('num')} + {self.number_transpiled(10)}"),
            self.forward_transpiled(f"{self.number_transpiled(10)} + {self.number_transpiled('num')}"))

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # add/remove tests
    #
    def test_add_text_to_list(self):
        code = textwrap.dedent("""\
            dieren is koe, kiep
            add muis to dieren
            print dieren at random""")

        expected = self.dedent(
            "dieren = Value([Value('koe'), Value('kiep')])",
            "dieren.data.append(Value('muis'))",
            self.list_access_transpiled("random.choice(dieren.data)"),
            "print(f'{random.choice(dieren.data)}')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11,
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
            "numbers = Value([Value('1', num_sys='Latin'), Value('2', num_sys='Latin')])",
            self.remove_transpiled('numbers', "Value('1', num_sys='Latin')"),
            self.remove_transpiled('numbers', "Value('2', num_sys='Latin')"),
            "numbers.data.append(Value('4', num_sys='Latin'))",
            self.list_access_transpiled("random.choice(numbers.data)"),
            "print(f'{random.choice(numbers.data)}')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11,
            extra_check_function=self.result_in([4]),
        )

    def test_add_text_with_inner_single_quote_to_list(self):
        code = textwrap.dedent("""\
            dieren is koe, kiep
            add mui's to dieren
            print dieren at random""")

        expected = self.dedent(
            "dieren = Value([Value('koe'), Value('kiep')])",
            "dieren.data.append(Value('mui\\\'s'))",
            self.list_access_transpiled("random.choice(dieren.data)"),
            "print(f'{random.choice(dieren.data)}')")

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

        expected = self.dedent(
            "dieren = Value([Value('koe'), Value('kiep')])",
            "dieren.data.append(Value('mui\"s'))",
            self.list_access_transpiled("random.choice(dieren.data)"),
            "print(f'{random.choice(dieren.data)}')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11,
            extra_check_function=self.result_in(['koe', 'kiep', 'mui\"s']),
        )

    def test_add_text_with_spaces_to_list(self):
        code = textwrap.dedent("""\
            opties is zeker weten, misschien wel
            add absoluut niet to opties
            print opties at random""")

        expected = self.dedent(
            "opties = Value([Value('zeker weten'), Value('misschien wel')])",
            "opties.data.append(Value('absoluut niet'))",
            self.list_access_transpiled("random.choice(opties.data)"),
            "print(f'{random.choice(opties.data)}')")

        self.multi_level_tester(
            max_level=11,
            code=code,
            expected=expected
        )

    def test_add_integer_to_list(self):
        code = textwrap.dedent("""\
            dieren is koe, kiep
            add 5 to dieren
            print dieren at random""")

        expected = self.dedent(
            "dieren = Value([Value('koe'), Value('kiep')])",
            "dieren.data.append(Value('5', num_sys='Latin'))",
            self.list_access_transpiled("random.choice(dieren.data)"),
            "print(f'{random.choice(dieren.data)}')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11,
            extra_check_function=self.result_in(['koe', 'kiep', 5]),
        )

    def test_add_ask_to_list(self):
        code = textwrap.dedent("""\
            color is ask 'what is your favorite color?'
            colors is green, red, blue
            add color to colors
            print colors at random""")

        expected = self.dedent(
            self.input_transpiled('color', 'what is your favorite color?'),
            "colors = Value([Value('green'), Value('red'), Value('blue')])",
            "colors.data.append(color)",
            self.list_access_transpiled("random.choice(colors.data)"),
            "print(f'{random.choice(colors.data)}')")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_remove_text_from_list(self):
        code = textwrap.dedent("""\
            dieren is koe, kiep
            remove kiep from dieren
            print dieren at random""")

        expected = self.dedent(
            "dieren = Value([Value('koe'), Value('kiep')])",
            self.remove_transpiled('dieren', "Value('kiep')"),
            self.list_access_transpiled('random.choice(dieren.data)'),
            "print(f'{random.choice(dieren.data)}')")

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

        expected = self.dedent(
            "dieren = Value([Value('koe'), Value('kiep\\\'s')])",
            self.remove_transpiled('dieren', "Value('kiep\\\'s')"),
            self.list_access_transpiled('random.choice(dieren.data)'),
            "print(f'{random.choice(dieren.data)}')")

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

        expected = self.dedent(
            "dieren = Value([Value('koe'), Value('kiep\"s')])",
            self.remove_transpiled('dieren', "Value('kiep\"s')"),
            self.list_access_transpiled("random.choice(dieren.data)"),
            "print(f'{random.choice(dieren.data)}')")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=11,
            extra_check_function=self.result_in(['koe', 'kiep', 'mui\'s']),
        )

    def test_remove_ask_from_list(self):
        code = textwrap.dedent("""\
            colors is green, red, blue
            color is ask 'what color to remove?'
            remove color from colors
            print colors at random""")

        expected = self.dedent(
            "colors = Value([Value('green'), Value('red'), Value('blue')])",
            self.input_transpiled('color', 'what color to remove?'),
            self.remove_transpiled('colors', 'color'),
            self.list_access_transpiled('random.choice(colors.data)'),
            "print(f'{random.choice(colors.data)}')")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # in/not in tests
    #
    def test_if_in_list_print(self):
        code = textwrap.dedent("""\
        items is red, green
        selected is red
        if selected in items print 'found!'""")

        expected = textwrap.dedent(f"""\
        items = Value([Value('red'), Value('green')])
        selected = Value('red')
        if {self.in_list_transpiled('selected.data', 'items')}:
          print(f'found!')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            output='found!',
            expected_commands=['is', 'is', 'if', 'in', 'print']
        )

    def test_if_in_list_in_print_else(self):
        code = textwrap.dedent("""\
        items is red, green
        selected is red
        if selected in items print 'found!'
        else print 'not found'""")

        expected = textwrap.dedent(f"""\
        items = Value([Value('red'), Value('green')])
        selected = Value('red')
        if {self.in_list_transpiled('selected.data', 'items')}:
          print(f'found!')
        else:
          print(f'not found')""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            expected=expected,
            output='found!'
        )

    def test_if_not_in_list_print_else(self):
        code = textwrap.dedent("""\
        items is red, green
        selected is red
        if selected not in items print 'not found!'
        else print 'found'""")

        expected = textwrap.dedent(f"""\
        items = Value([Value('red'), Value('green')])
        selected = Value('red')
        if {self.not_in_list_transpiled('selected.data', 'items')}:
          print(f'not found!')
        else:
          print(f'found')""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            expected=expected,
            output='found'
        )

    def test_list_access_index(self):
        code = textwrap.dedent("""\
            friends is Hedy, Lola, Frida
            friend is friends at 2
            print friend""")

        expected = self.dedent(
            "friends = Value([Value('Hedy'), Value('Lola'), Value('Frida')])",
            self.list_access_transpiled('friends.data[int(2)-1]'),
            "friend = friends.data[int(2)-1]",
            "print(f'{friend}')")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_ar_number_list_with_latin_numbers(self):
        code = textwrap.dedent("""\
        a is 11, 22, 33
        if ١١ in a print 'correct'""")

        expected = textwrap.dedent(f"""\
        a = {self.list_transpiled("11", "22", "33")}
        if {self.in_list_transpiled("'١١'", 'a')}:
          print(f'correct')""")

        self.multi_level_tester(code=code, expected=expected, max_level=7, output='correct')

    def test_if_ar_number_not_list_with_latin_numbers(self):
        code = textwrap.dedent("""\
        a is 22, 33, 44
        if ١١ not in a print 'correct'""")

        expected = textwrap.dedent(f"""\
        a = {self.list_transpiled("22", "33", "44")}
        if {self.not_in_list_transpiled("'١١'", 'a')}:
          print(f'correct')""")

        self.multi_level_tester(code=code, expected=expected, max_level=7, output='correct')

    #
    # if pressed tests
    #
    def test_if_pressed_x_is_variable(self):
        code = textwrap.dedent("""\
        x is a
        if x is pressed print 'it is a letter key' else print 'it is another letter key'
        print x""")

        expected = self.dedent("""\
        x = Value('a')
        if_pressed_mapping = {"else": "if_pressed_default_else"}
        if_pressed_mapping['x'] = 'if_pressed_x_'
        if_pressed_mapping['else'] = 'if_pressed_else_'
        def if_pressed_x_():
          print(f'it is a letter key')
        def if_pressed_else_():
          print(f'it is another letter key')
        extensions.if_pressed(if_pressed_mapping)
        print(f'{x}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)
