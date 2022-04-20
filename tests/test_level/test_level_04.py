import hedy
import textwrap
from tests.Tester import HedyTester
from parameterized import parameterized


class TestsLevel4(HedyTester):
    level = 4
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
    def test_print_single_quoted_text(self):
        code = "print 'hallo wereld!'"
        expected = "print(f'hallo wereld!')"

        self.multi_level_tester(
            code=code,
            max_level=11,
            expected=expected)

    def test_print_double_quoted_text(self):
        code = 'print "hallo wereld!"'
        expected = "print(f'hallo wereld!')"

        self.multi_level_tester(
            code=code,
            max_level=11,
            expected=expected)

    def test_print_single_quoted_text_with_inner_double_quote(self):
        code = """print 'quote is "'"""
        expected = """print(f'quote is "')"""

        self.multi_level_tester(
            code=code,
            max_level=11,
            expected=expected)

    def test_print_double_quoted_text_with_inner_single_quote(self):
        code = '''print "It's me"'''
        expected = """print(f'It\\'s me')"""

        self.multi_level_tester(
            code=code,
            max_level=11,
            expected=expected)

    def test_print_no_space(self):
        code = "print'hallo wereld!'"
        expected = "print(f'hallo wereld!')"

        self.multi_level_tester(
            code=code,
            max_level=11,
            expected=expected)

    def test_print_comma(self):
        code = "print 'Hi, I am Hedy'"
        expected = "print(f'Hi, I am Hedy')"
        self.multi_level_tester(
            code=code,
            max_level=11,
            expected=expected
        )

    def test_print_slash(self):
        code = "print 'Yes/No'"
        expected = "print(f'Yes/No')"

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_print_backslash(self):
        code = "print 'Yes\\No'"
        expected = "print(f'Yes\\\\No')"
        output = "Yes\\No"

        self.multi_level_tester(
            code=code,
            expected=expected,
            output=output,
            max_level=11,
            translate=True
        )

    def test_print_with_backslash_at_end(self):
        code = "print 'Welcome to \\'"
        expected = "print(f'Welcome to \\\\')"
        self.multi_level_tester(
            code=code,
            max_level=11,
            expected=expected,
            translate=True
        )

    def test_print_with_spaces(self):
        code = "print        'hallo!'"
        expected = "print(f'hallo!')"

        self.multi_level_tester(
            code=code,
            max_level=11,
            expected=expected
        )

    def test_print_asterisk(self):
        code = "print '*Jouw* favoriet is dus kleur'"
        expected = "print(f'*Jouw* favoriet is dus kleur')"

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_print_without_quotes_gives_error(self):
        code = "print hedy 123"
        self.single_level_tester(code, exception=hedy.exceptions.UnquotedTextException)

    def test_print_text_without_quotes_gives_error(self):
        code = "print hallo wereld"

        self.multi_level_tester(
            code=code,
            max_level=17,
            exception=hedy.exceptions.UndefinedVarException,
        )

    @parameterized.expand(HedyTester.quotes)
    def test_print_without_opening_quote_gives_error(self, q):
        code = f"print hedy 123{q}"
        self.single_level_tester(code, exception=hedy.exceptions.UnquotedTextException)

    @parameterized.expand(HedyTester.quotes)
    def test_print_without_closing_quote_gives_error(self, q):
        code = f"print {q}hedy 123"
        self.single_level_tester(code, exception=hedy.exceptions.UnquotedTextException)

    #
    # ask tests
    #
    def test_ask_single_quoted_text(self):
        code = "details is ask 'tell me more'"
        expected = "details = input(f'tell me more')"

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_ask_double_quoted_text(self):
        code = 'details is ask "tell me more"'
        expected = "details = input(f'tell me more')"

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_ask_single_quoted_text_with_inner_double_quote(self):
        code = """details is ask 'say "no"'"""
        expected = """details = input(f'say "no"')"""

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_ask_double_quoted_text_with_inner_single_quote(self):
        code = f'''details is ask "say 'no'"'''
        expected = '''details = input(f'say \\'no\\'')'''

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_ask_without_quotes_gives_error(self):
        code = "kleur is ask Hedy 123"
        self.single_level_tester(code, exception=hedy.exceptions.HedyException)

    def test_ask_text_without_quotes_gives_error(self):
        code = "var is ask hallo wereld"

        self.multi_level_tester(
            code=code,
            max_level=17,
            exception=hedy.exceptions.UndefinedVarException,
        )

    @parameterized.expand(HedyTester.quotes)
    def test_ask_without_opening_quote_gives_error(self, q):
        code = f"kleur is ask Hedy 123{q}"
        self.single_level_tester(code, exception=hedy.exceptions.UnquotedTextException)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_without_closing_quote_gives_error(self, q):
        code = f"kleur is ask {q}Hedy 123"
        self.single_level_tester(code, exception=hedy.exceptions.UnquotedTextException)

    def test_ask_with_comma(self):
        code = textwrap.dedent("""\
        dieren is ask 'hond, kat, kangoeroe'
        print dieren""")

        expected = textwrap.dedent("""\
        dieren = input(f'hond, kat, kangoeroe')
        print(f'{dieren}')""")

        # TODO: set max_level to 11 after #2497 is merged
        self.multi_level_tester(code=code, expected=expected, max_level=5)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_es(self, q):
        code = f"""color is ask {q}Cuál es tu color favorito?{q}"""
        expected = f"""color = input(f'Cuál es tu color favorito?')"""

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_ask_bengali_var(self):
        code = textwrap.dedent("""\
        রং is ask 'আপনার প্রিয় রং কি?'
        print রং ' is আপনার প্রিয'""")

        expected = textwrap.dedent("""\
        ve1760b6272d4c9f816e62af4882d874f = input(f'আপনার প্রিয় রং কি?')
        print(f'{ve1760b6272d4c9f816e62af4882d874f} is আপনার প্রিয')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_ask_list_random(self):
        code = textwrap.dedent("""\
        colors is orange, blue, green
        favorite is ask 'Is your fav color ' colors at random""")

        expected = textwrap.dedent("""\
        colors = ['orange', 'blue', 'green']
        favorite = input(f'Is your fav color {random.choice(colors)}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_ask_list_access_index(self):
        code = textwrap.dedent("""\
        colors is orange, blue, green
        favorite is ask 'Is your fav color ' colors at 1""")

        expected = textwrap.dedent("""\
        colors = ['orange', 'blue', 'green']
        favorite = input(f'Is your fav color {colors[1-1]}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_ask_string_var(self):
        code = textwrap.dedent("""\
        color is orange
        favorite is ask 'Is your fav color ' color""")

        expected = textwrap.dedent("""\
        color = 'orange'
        favorite = input(f'Is your fav color {color}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_ask_integer_var(self):
        code = textwrap.dedent("""\
        number is 10
        favorite is ask 'Is your fav number' number""")

        expected = textwrap.dedent("""\
        number = '10'
        favorite = input(f'Is your fav number{number}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_list_values_with_inner_single_quotes(self):
        code = textwrap.dedent(f"""\
          taart is 'appeltaart, choladetaart, kwarktaart'
          print 'we bakken een ' taart at random""")

        expected = textwrap.dedent("""\
          taart = ['\\'appeltaart', 'choladetaart', 'kwarktaart\\'']
          print(f'we bakken een {random.choice(taart)}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_list_values_with_inner_double_quotes(self):
        code = textwrap.dedent(f"""\
          taart is "appeltaart, choladetaart, kwarktaart"
          print 'we bakken een ' taart at random""")

        expected = textwrap.dedent("""\
          taart = ['"appeltaart', 'choladetaart', 'kwarktaart"']
          print(f'we bakken een {random.choice(taart)}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_list_with_single_quoted_values(self):
        code = textwrap.dedent(f"""\
        taart is 'appeltaart', 'choladetaart', 'kwarktaart'
        print 'we bakken een' taart at random""")

        expected = textwrap.dedent("""\
        taart = ['\\'appeltaart\\'', '\\'choladetaart\\'', '\\'kwarktaart\\'']
        print(f'we bakken een{random.choice(taart)}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_list_with_double_quoted_values(self):
        code = textwrap.dedent(f"""\
        taart is "appeltaart, choladetaart, kwarktaart"
        print 'we bakken een' taart at random""")

        expected = textwrap.dedent("""\
        taart = ['"appeltaart', 'choladetaart', 'kwarktaart"']
        print(f'we bakken een{random.choice(taart)}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # is tests
    #
    def test_assign_print(self):
        code = textwrap.dedent("""\
        naam is Hedy
        print 'ik heet' naam""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        print(f'ik heet{naam}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_assign_underscore(self):
        code = textwrap.dedent("""\
        voor_naam is Hedy
        print 'ik heet ' voor_naam""")

        expected = textwrap.dedent("""\
        voor_naam = 'Hedy'
        print(f'ik heet {voor_naam}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # add/remove tests
    #
    def test_add_ask_to_list(self):
        code = textwrap.dedent("""\
        color is ask 'what is your favorite color?'
        colors is green, red, blue
        add color to colors
        print colors at random""")

        expected = textwrap.dedent("""\
        color = input(f'what is your favorite color?')
        colors = ['green', 'red', 'blue']
        colors.append(color)
        print(f'{random.choice(colors)}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_remove_ask_from_list(self):
        code = textwrap.dedent("""\
        colors is green, red, blue
        color is ask 'what color to remove?'
        remove color from colors
        print colors at random""")

        expected = textwrap.dedent("""\
        colors = ['green', 'red', 'blue']
        color = input(f'what color to remove?')
        try:
          colors.remove(color)
        except:
          pass
        print(f'{random.choice(colors)}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # combined tests
    #
    def test_assign_print_chinese(self):
        hashed_var = hedy.hash_var("你世界")
        self.assertEqual('v406b71a2caed270b782fe8a1f2d5741a', hashed_var)

        code = textwrap.dedent("""\
        你世界 is 你好世界
        print 你世界""")

        expected = textwrap.dedent("""\
        v406b71a2caed270b782fe8a1f2d5741a = '你好世界'
        print(f'{v406b71a2caed270b782fe8a1f2d5741a}')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_ask_forward(self):
        code = textwrap.dedent("""\
        afstand is ask 'hoe ver dan?'
        forward afstand""")

        expected = HedyTester.dedent(
            "afstand = input(f'hoe ver dan?')",
            HedyTester.forward_transpiled('afstand'))

        self.multi_level_tester(
            max_level=self.max_turtle_level,
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle()
        )

    #
    # negative tests
    #
    def test_var_undefined_error_message(self):
        code = textwrap.dedent("""\
        naam is Hedy
        print 'ik heet ' name""")

        self.multi_level_tester(
            code=code,
            max_level=11,
            exception=hedy.exceptions.UndefinedVarException
        )

    # issue 375
    def test_program_gives_hedy_parse_exception(self):
        code = textwrap.dedent("""\
        is Foobar
        print welcome""")

        self.multi_level_tester(
            code=code,
            max_level=11,
            exception=hedy.exceptions.ParseException,
            extra_check_function=lambda c: c.exception.error_location[0] == 1 and c.exception.error_location[1] == 1
        )

    def test_quoted_text_gives_error(self):
        code = 'competitie die gaan we winnen'

        self.multi_level_tester(code=code, exception=hedy.exceptions.MissingCommandException)

    def test_repair_incorrect_print_argument(self):
        code = "print ,'Hello'"

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.ParseException,
            extra_check_function=lambda c: c.exception.fixed_code == "print 'Hello'"
        )

    #
    # assorti tests
    #
    def test_detect_accented_chars(self):
        self.assertEqual(True, hedy.hash_needed('éyyy'))
        self.assertEqual(True, hedy.hash_needed('héyyy'))
        self.assertEqual(False, hedy.hash_needed('heyyy'))

    @parameterized.expand(HedyTester.quotes)
    def test_meta_column_missing_closing_quote(self, q):
        code = textwrap.dedent(f"""\
        print {q}Hello{q}
        print {q}World""")

        line, column = self._codeToInvalidInfo(code)

        self.assertEqual(2, line)
        self.assertEqual(7, column)

    @parameterized.expand(HedyTester.quotes)
    def test_meta_column_missing_opening_quote(self, q):
        code = textwrap.dedent(f"""\
        print {q}Hello{q}
        print World{q}""")

        line, column = self._codeToInvalidInfo(code)

        self.assertEqual(2, line)
        self.assertEqual(7, column)

    def _codeToInvalidInfo(self, code):
        instance = hedy.IsValid()
        instance.level = self.level
        program_root = hedy.parse_input(code, self.level, 'en')
        is_valid = instance.transform(program_root)
        _, invalid_info = is_valid

        return invalid_info[0].line, invalid_info[0].column
