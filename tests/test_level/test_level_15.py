import textwrap

from parameterized import parameterized

import exceptions
import hedy
from tests.Tester import HedyTester


class TestsLevel15(HedyTester):
    level = 15

    #
    # print tests
    #
    def test_print_arabic_var(self):
        code = textwrap.dedent("""\
            a = ١١
            print a""")
        expected = textwrap.dedent("""\
            a = Value(11, num_sys='Arabic')
            print(f'''{a}''')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            translate=False,
            skip_faulty=False,
        )

    def test_print_arabic_calc_var(self):
        code = textwrap.dedent("""\
            a = ٢٢ + ١١
            print a""")
        expected = textwrap.dedent("""\
            a = Value(22 + 11, num_sys='Arabic')
            print(f'''{a}''')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            translate=False,
            skip_faulty=False,
        )

    #
    # ask tests
    #
    def test_ask_number(self):
        code = "n is ask 42"
        expected = self.input_transpiled('n', '42')

        self.multi_level_tester(code=code, expected=expected, max_level=17, unused_allowed=True)

    def test_ask_arabic_number(self):
        code = "n is ask ٢٣٤"
        expected = self.input_transpiled('n', "{localize(234, num_sys='Arabic')}")

        self.multi_level_tester(code=code, expected=expected, max_level=17, unused_allowed=True)

    def test_ask_multi_args(self):
        code = "n is ask 'hello' 'Hedy' 4 ١١"
        expected = self.input_transpiled('n', "helloHedy4{localize(11, num_sys='Arabic')}")

        self.multi_level_tester(code=code, expected=expected, max_level=17, unused_allowed=True)

    def test_ask_number_answer(self):
        code = textwrap.dedent("""\
            prijs is ask 'hoeveel?'
            gespaard is 7
            sparen is prijs - gespaard""")
        minus_op = f"{self.number_transpiled('prijs')} - {self.number_transpiled('gespaard')}"
        expected = self.dedent(
            self.input_transpiled('prijs', 'hoeveel?'),
            "gespaard = Value(7, num_sys='Latin')",
            f"sparen = Value({minus_op}, num_sys=get_num_sys(prijs))")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_with_list_var(self):
        code = textwrap.dedent("""\
        colors is 'orange', 'blue', 'green'
        favorite is ask 'Is your fav color' colors at 1""")

        expected = self.dedent(
            "colors = Value([Value('orange'), Value('blue'), Value('green')])",
            self.list_access_transpiled('colors.data[int(1)-1]'),
            self.input_transpiled('favorite', 'Is your fav color{colors.data[int(1)-1]}'))

        self.single_level_tester(code=code, unused_allowed=True, expected=expected)

    def test_ask_literal_strings(self):
        code = """var is ask "It's " '"Hedy"!'"""
        expected = self.input_transpiled('var', """It\\'s "Hedy"!""")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_literal_strings_bulgarian(self):
        code = """отг е попитай 'Is it Hedy?'"""
        bool_sys = [{'Вярно': True, 'Невярно': False}, {'True': True, 'False': False},
                    {'вярно': True, 'невярно': False}, {'true': True, 'false': False}]
        expected = self.input_transpiled('отг', """Is it Hedy?""", bool_sys=bool_sys)

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17, lang='bg')

    @parameterized.expand(HedyTester.quotes)
    def test_ask_with_string_var(self, q):
        code = textwrap.dedent(f"""\
        color is {q}orange{q}
        favorite is ask {q}Is your fav color{q} color""")

        expected = self.dedent(
            "color = Value('orange')",
            self.input_transpiled('favorite', 'Is your fav color{color}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    @parameterized.expand(['10', '10.0'])
    def test_ask_with_number_var(self, number):
        code = textwrap.dedent(f"""\
        number is {number}
        favorite is ask 'Is your fav number' number""")

        expected = self.dedent(
            f"number = Value({number}, num_sys='Latin')",
            self.input_transpiled('favorite', 'Is your fav number{number}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_with_keyword_var(self):
        code = textwrap.dedent("""\
            sum is 'Hedy'
            v is ask sum""")

        expected = self.dedent(
            "_sum = Value('Hedy')",
            self.input_transpiled('v', '{_sum}'))

        self.multi_level_tester(code=code, expected=expected, max_level=17, unused_allowed=True)

    def test_ask_single_quoted_text(self):
        code = "details is ask 'tell me more'"
        expected = self.input_transpiled('details', 'tell me more')

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_double_quoted_text(self):
        code = 'details is ask "tell me more"'
        expected = self.input_transpiled('details', 'tell me more')

        self.multi_level_tester(code=code, expected=expected, unused_allowed=True, max_level=17)

    def test_ask_single_quoted_text_with_inner_double_quote(self):
        code = """details is ask 'say "no"'"""
        expected = self.input_transpiled('details', 'say "no"')

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_double_quoted_text_with_inner_single_quote(self):
        code = f'''details is ask "say 'no'"'''
        expected = self.input_transpiled('details', "say \\'no\\'")

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_with_comma(self):
        code = "dieren is ask 'hond, kat, kangoeroe'"
        expected = self.input_transpiled('dieren', 'hond, kat, kangoeroe')

        self.multi_level_tester(code=code, expected=expected, max_level=17, unused_allowed=True)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_es(self, q):
        code = f"""color is ask {q}Cuál es tu color favorito?{q}"""
        expected = self.input_transpiled('color', 'Cuál es tu color favorito?')

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    @parameterized.expand(HedyTester.quotes)
    def test_ask_bengali_var(self, q):
        code = f"""রং is ask {q}আপনার প্রিয় রং কি?{q}"""
        expected = self.input_transpiled('রং', 'আপনার প্রিয় রং কি?')

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_list_random(self):
        code = textwrap.dedent("""\
            numbers is 1, 2, 3
            favorite is ask 'Is your fav number ' numbers at random""")
        expected = self.dedent(
            "numbers = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(3, num_sys='Latin')])",
            self.list_access_transpiled('random.choice(numbers.data)'),
            self.input_transpiled('favorite', 'Is your fav number {random.choice(numbers.data)}'))

        self.single_level_tester(code=code, unused_allowed=True, expected=expected)

    def test_ask_list_access_index(self):
        code = textwrap.dedent("""\
            numbers is 1, 2, 3
            favorite is ask 'Is your fav number ' numbers at 2""")

        expected = self.dedent(
            "numbers = Value([Value(1, num_sys='Latin'), Value(2, num_sys='Latin'), Value(3, num_sys='Latin')])",
            self.list_access_transpiled('numbers.data[int(2)-1]'),
            self.input_transpiled('favorite', 'Is your fav number {numbers.data[int(2)-1]}'))

        self.single_level_tester(code=code, unused_allowed=True, expected=expected)

    def test_ask_string_var(self):
        code = textwrap.dedent("""\
            color is "orange"
            favorite is ask 'Is your fav color ' color""")
        expected = self.dedent(
            "color = Value('orange')",
            self.input_transpiled('favorite', 'Is your fav color {color}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_ask_integer_var(self):
        code = textwrap.dedent("""\
            number is 10
            favorite is ask 'Is your fav number ' number""")
        expected = self.dedent(
            "number = Value(10, num_sys='Latin')",
            self.input_transpiled('favorite', 'Is your fav number {number}'))

        self.multi_level_tester(code=code, unused_allowed=True, expected=expected, max_level=17)

    def test_add_ask_to_list(self):
        code = textwrap.dedent("""\
            color is ask 'what is your favorite color?'
            colors is 'green', 'red', 'blue'
            add color to colors""")

        expected = self.dedent(
            self.input_transpiled('color', 'what is your favorite color?'),
            "colors = Value([Value('green'), Value('red'), Value('blue')])",
            "colors.data.append(color)")

        self.single_level_tester(code=code, expected=expected)

    def test_remove_ask_from_list(self):
        code = textwrap.dedent("""\
            colors is 'green', 'red', 'blue'
            color is ask 'what color to remove?'
            remove color from colors""")

        expected = self.dedent(
            "colors = Value([Value('green'), Value('red'), Value('blue')])",
            self.input_transpiled('color', 'what color to remove?'),
            self.remove_transpiled('colors', 'color'))

        self.single_level_tester(code=code, expected=expected)

    def test_sleep_with_input_variable(self):
        code = textwrap.dedent("""\
            n is ask "how long"
            sleep n""")

        expected = self.dedent(
            self.input_transpiled('n', 'how long'),
            self.sleep_transpiled("n.data"))

        self.multi_level_tester(max_level=17, code=code, expected=expected)

    def test_play_input(self):
        code = textwrap.dedent("""\
            note = ask 'Give me a note'
            play note""")

        expected = self.dedent(
            self.input_transpiled('note', 'Give me a note'),
            self.play_transpiled('note.data'))

        self.multi_level_tester(code=code, expected=expected, max_level=17)

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

        self.multi_level_tester(code=code, expected=expected, max_level=16)

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

    #
    # boolean values
    #
    @parameterized.expand(HedyTester.booleans)
    def test_assign_var_boolean(self, value, exp):
        code = f"cond = {value}"
        true_, false_ = HedyTester.bool_options(value)
        expected = f"cond = Value({exp}, bool_sys={{True: '{true_}', False: '{false_}'}})"

        self.multi_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True,
            translate=False
        )

    def test_assign_list_var_boolean(self):
        code = "cond = true"
        expected = "cond = Value(True, bool_sys={True: 'true', False: 'false'})"

        self.single_level_tester(
            code=code,
            expected=expected,
            unused_allowed=True
        )

    def test_assign_print_var_boolean(self):
        code = textwrap.dedent("""\
            cond = true
            print cond""")
        expected = textwrap.dedent("""\
            cond = Value(True, bool_sys={True: 'true', False: 'false'})
            print(f'''{cond}''')""")

        self.single_level_tester(
            code=code,
            expected=expected,
            output="true"
        )

    @parameterized.expand(HedyTester.booleans)
    def test_print_boolean(self, value, exp):
        code = f"print 'variable is ' {value}"
        true_, false_ = HedyTester.bool_options(value)
        expected = f"print(f'''variable is {{localize({exp}, bool_sys={{True: '{true_}', False: '{false_}'}})}}''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            translate=False
        )

    @parameterized.expand([
        ('вярно', True, 'вярно', 'невярно'),
        ('Вярно', True, 'Вярно', 'Невярно'),
        ('невярно', False, 'вярно', 'невярно'),
        ('Невярно', False, 'Вярно', 'Невярно')
    ])
    def test_print_boolean_bulgarian(self, input_, value, true_, false_):
        code = f"принтирай 'Това е ' {input_}"
        expected = f"print(f'''Това е {{localize({value}, bool_sys={{True: '{true_}', False: '{false_}'}})}}''')"

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            lang='bg'
        )

    @parameterized.expand(HedyTester.booleans)
    def test_print_boolean_var(self, value, expected):
        code = textwrap.dedent(f"""\
            cond = {value}
            print 'variable is ' cond""")
        true_, false_ = HedyTester.bool_options(value)
        expected = textwrap.dedent(f"""\
            cond = Value({expected}, bool_sys={{True: '{true_}', False: '{false_}'}})
            print(f'''variable is {{cond}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected,
            translate=False
        )

    @parameterized.expand(HedyTester.booleans)
    def test_cond_boolean(self, value, expected):
        code = textwrap.dedent(f"""\
            cond = {value}
            if cond is {value}
                sleep""")
        true_, false_ = HedyTester.bool_options(value)
        expected = textwrap.dedent(f"""\
            cond = Value({expected}, bool_sys={{True: '{true_}', False: '{false_}'}})
            if cond.data == {expected}:
              time.sleep(1)""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
            translate=False,
            skip_faulty=False
        )

    #
    # calc tests
    #
    def test_concat_promotes_ask_input_to_string(self):
        code = textwrap.dedent("""\
            answer is ask 'Yes or No?'
            print 'The answer is ' + answer""")

        expected = self.dedent(
            self.input_transpiled('answer', 'Yes or No?'),
            f"""print(f'''{{localize({self.sum_transpiled("'The answer is '", 'answer')})}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    def test_concat_promotes_ask_input_to_int(self):
        code = textwrap.dedent("""\
            answer is ask '1 or 2?'
            print 5 + answer""")

        expected = self.dedent(
            self.input_transpiled('answer', '1 or 2?'),
            f"""print(f'''{{localize({self.sum_transpiled('5', 'answer')}, num_sys='Latin')}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    def test_concat_promotes_ask_input_to_float(self):
        code = textwrap.dedent("""\
            answer is ask '1 or 2?'
            print 0.5 + answer""")

        expected = self.dedent(
            self.input_transpiled('answer', '1 or 2?'),
            f"""print(f'''{{localize({self.sum_transpiled('0.5', 'answer')}, num_sys='Latin')}}''')""")

        self.multi_level_tester(
            code=code,
            max_level=17,
            expected=expected
        )

    #
    # while tests
    #
    def test_while_equals(self):
        code = textwrap.dedent("""\
        a is true
        while a != false
            print a
            a = false
        print 'Bye!'""")
        expected = textwrap.dedent("""\
        a = Value(True, bool_sys={True: 'true', False: 'false'})
        while a.data!=False:
          print(f'''{a}''')
          a = Value(False, bool_sys={True: 'true', False: 'false'})
          time.sleep(0.1)
        print(f'''Bye!''')""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            expected=expected,
            skip_faulty=False
        )

    @parameterized.expand(HedyTester.booleans)
    def test_while_equals_boolean(self, value, exp):
        code = textwrap.dedent(f"""\
            cond is {value}
            while cond != {value}
              cond is {value}""")
        true_, false_ = HedyTester.bool_options(value)
        expected = textwrap.dedent(f"""\
            cond = Value({exp}, bool_sys={{True: '{true_}', False: '{false_}'}})
            while cond.data!={exp}:
              cond = Value({exp}, bool_sys={{True: '{true_}', False: '{false_}'}})
              time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
            skip_faulty=False,
            translate=False
        )

    @parameterized.expand(['and', 'or'])
    def test_while_and_or(self, op):
        code = textwrap.dedent(f"""\
            answer = 7
            while answer > 5 {op} answer < 10
              answer = ask 'What is 5 times 5?'
            print 'A correct answer has been given'""")

        # Splitting like this to wrap the line around 120 characters max
        expected = self.dedent(
            "answer = Value(7, num_sys='Latin')",
            f"while answer.data>5 {op} answer.data<10:",
            (self.input_transpiled('answer', 'What is 5 times 5?'), '  '),
            ('time.sleep(0.1)', '  '),
            "print(f'''A correct answer has been given''')")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
            expected_commands=['is', 'while', op, 'ask', 'print']
        )

    def test_while_fr_equals(self):
        code = textwrap.dedent("""\
            antwoord est 0
            tant que antwoord != 25
                antwoord est antwoord + 1
            affiche 'Goed gedaan!'""")
        expected = self.dedent(f"""\
            antwoord = Value(0, num_sys='Latin')
            while antwoord.data!=25:
              antwoord = Value({self.sum_transpiled('antwoord', 1)}, num_sys=get_num_sys(antwoord))
              time.sleep(0.1)
            print(f'''Goed gedaan!''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
            expected_commands=['is', 'while', 'is', 'addition', 'print'],
            lang='fr'
        )

    @parameterized.expand([
        ('0', 'Latin', '1\n2\n3\n4\n5'),
        ('𑁦', 'Brahmi', '𑁧\n𑁨\n𑁩\n𑁪\n𑁫'),
        ('०', 'Devanagari', '१\n२\n३\n४\n५'),
        ('൦', 'Malayalam', '൧\n൨\n൩\n൪\n൫')
    ])
    def test_while_calc_var(self, num, num_sys, output):
        code = textwrap.dedent(f"""\
            a = {num}
            while a != 5
                a = a + 1
                print a""")
        expected = self.dedent(f"""\
            a = Value(0, num_sys='{num_sys}')
            while a.data!=5:
              a = Value({self.sum_transpiled('a', 1)}, num_sys=get_num_sys(a))
              print(f'''{{a}}''')
              time.sleep(0.1)""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            max_level=16,
            output=output,
        )

    def test_while_undefined_var(self):
        code = textwrap.dedent("""\
            while antwoord != 25
                print 'hoera'""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.UndefinedVarException,
            max_level=16,
        )

    def test_while_smaller(self):
        code = textwrap.dedent("""\
            getal is 0
            while getal < 100000
                getal is ask 'HOGER!!!!!'
            print 'Hoog he?'""")
        expected = self.dedent(
            "getal = Value(0, num_sys='Latin')",
            "while getal.data<100000:",
            (self.input_transpiled('getal', 'HOGER!!!!!'), '  '),
            ("time.sleep(0.1)", '  '),
            "print(f'''Hoog he?''')")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected
        )

    def test_missing_indent_while(self):
        code = textwrap.dedent(f"""\
            answer = 0
            while answer != 25
            answer = ask 'What is 5 times 5?'
            print 'A correct answer has been given'""")

        self.multi_level_tester(
            code=code,
            max_level=15,
            exception=exceptions.NoIndentationException
        )

    def test_if_pressed_without_else_works(self):
        code = textwrap.dedent("""\
            if p is pressed
                print 'press'""")

        expected = textwrap.dedent("""\
            if_pressed_mapping = {"else": "if_pressed_default_else"}
            if_pressed_mapping['p'] = 'if_pressed_p_'
            def if_pressed_p_():
                print(f'''press''')
            extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(code, expected=expected, max_level=16)

    def test_if_pressed_works_in_while_loop(self):
        code = textwrap.dedent("""\
        stop is 0
        while stop != 1
            if p is pressed
                print 'press'
            if s is pressed
                stop = 1
        print 'Uit de loop!'""")

        expected = textwrap.dedent("""\
        stop = Value(0, num_sys='Latin')
        while stop.data!=1:
          if_pressed_mapping = {"else": "if_pressed_default_else"}
          if_pressed_mapping['p'] = 'if_pressed_p_'
          def if_pressed_p_():
              print(f'''press''')
          extensions.if_pressed(if_pressed_mapping)
          if_pressed_mapping = {"else": "if_pressed_default_else"}
          if_pressed_mapping['s'] = 'if_pressed_s_'
          def if_pressed_s_():
              stop = Value(1, num_sys='Latin')
          extensions.if_pressed(if_pressed_mapping)
          time.sleep(0.1)
        print(f'''Uit de loop!''')""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
        )

    def test_if_pressed_multiple_lines_body(self):
        code = textwrap.dedent("""\
        if x is pressed
            print 'x'
            print 'lalalalala'
        else
            print 'not x'
            print 'lalalalala'""")

        expected = textwrap.dedent("""\
         if_pressed_mapping = {"else": "if_pressed_default_else"}
         if_pressed_mapping['x'] = 'if_pressed_x_'
         def if_pressed_x_():
             print(f'''x''')
             print(f'''lalalalala''')
         if_pressed_mapping['else'] = 'if_pressed_else_'
         def if_pressed_else_():
             print(f'''not x''')
             print(f'''lalalalala''')
         extensions.if_pressed(if_pressed_mapping)""")

        self.multi_level_tester(
            code=code,
            max_level=16,
            expected=expected,
        )

    def test_source_map(self):
        code = textwrap.dedent("""\
            answer = 0
            while answer != 25
                answer = ask 'What is 5 times 5?'
            print 'A correct answer has been given'""")

        excepted_code = self.dedent(
            "answer = Value(0, num_sys='Latin')",
            "while answer.data!=25:",
            (self.input_transpiled('answer', 'What is 5 times 5?'), '  '),
            ("time.sleep(0.1)", '  '),
            "print(f'''A correct answer has been given''')")

        expected_source_map = {
            '1/1-1/7': '1/1-1/7',
            '1/1-1/11': '1/1-1/35',
            '2/7-2/13': '2/7-2/13',
            '2/7-2/19': '2/7-2/22',
            '3/5-3/11': '10/5-10/11',
            '3/5-3/38': '3/1-15/28',
            '2/1-3/47': '2/1-16/18',
            '4/1-4/40': '17/1-17/46',
            '1/1-4/41': '1/1-17/46'
        }

        self.single_level_tester(code, expected=excepted_code)
        self.source_map_tester(code=code, expected_source_map=expected_source_map)
