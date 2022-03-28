import hedy
import textwrap
from parameterized import parameterized
from test_level_01 import HedyTester

class TestsLevel4(HedyTester):
  level = 4

  # tests should be ordered as follows:
  # * commands in the order of hedy.py for level 3: ['print', 'ask', 'is', 'turn', 'forward'],
  # * combined tests
  # * markup tests
  # * negative tests (inc. negative & multilevel)

  # test name conventions are like this:
  # * single keyword positive tests are just keyword or keyword_special_case
  # * multi keyword positive tests are keyword1_keywords_2
  # * negative tests should be
  # * situation_gives_exception


  # print tests
  def test_print_single_quoted_string(self):
    code = "print 'hallo wereld!'"
    expected = "print(f'hallo wereld!')"

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected)

  def test_print_double_quoted_string(self):
    code = 'print "hallo wereld!"'
    expected = "print(f'hallo wereld!')"

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected)

  def test_print_comma(self):
    code = "print 'ik heet ,'"
    expected = "print(f'ik heet ,')"
    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_print_two_spaces(self):
    code = "print        'hallo!'"

    expected = textwrap.dedent("""\
    print(f'hallo!')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_print_with_slashes(self):
    code = "print 'Welcome to \\'"
    expected = textwrap.dedent("""\
    print(f'Welcome to \\\\')""")
    output = "Welcome to \\"
    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected,
      translate=False  # \\ is not preserved in tests properly at the moment
    )

  # ask
  @parameterized.expand(HedyTester.quotes)
  def test_ask_quoted_string(self, q):
    code = f"details is ask {q}tell me more{q}"
    expected = "details = input(f'tell me more')"

    self.multi_level_tester(
      code=code,
      max_level=11,
      expected=expected)

  @parameterized.expand(HedyTester.quotes)
  def test_ask_Spanish(self, q):
    code = f"""color is ask {q}Cuál es tu color favorito?{q}"""
    expected = f"""color = input(f'Cuál es tu color favorito?')"""
    self.multi_level_tester(
      max_level=10,
      code=code,
      expected=expected
    )
  def test_ask_without_quotes(self):
    code = textwrap.dedent("""
    ding is kleur
    kleur is ask Wat is je lievelingskleur'
    print 'Jouw favoriet is dus ' kleur""")

    self.single_level_tester(code, exception=hedy.exceptions.UnquotedTextException)


  def test_ask_with_list_var(self):
    code = textwrap.dedent("""\
    colors is orange, blue, green
    favorite is ask 'Is your fav color ' colors at random""")

    expected = textwrap.dedent("""\
    colors = ['orange', 'blue', 'green']
    favorite = input(f'Is your fav color {random.choice(colors)}')""")

    self.multi_level_tester(
        max_level=10,
        code=code,
        expected=expected,
        extra_check_function=self.is_not_turtle()
    )

  def test_ask_with_list_gives_type_error(self):
    code = textwrap.dedent("""\
    colors is orange, blue, green
    favorite is ask 'Is your fav color' colors""")

    self.multi_level_tester(
        max_level=11,
        code=code,
        exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_ask_with_string_var(self):
    code = textwrap.dedent("""\
    color is orange
    favorite is ask 'Is your fav color ' color""")

    expected = textwrap.dedent("""\
    color = 'orange'
    favorite = input(f'Is your fav color {color}')""")

    self.multi_level_tester(
        max_level=10,
        code=code,
        expected=expected,
        extra_check_function=self.is_not_turtle()
    )
  def test_ask_with_integer_var(self):
    code = textwrap.dedent("""\
    number is 10
    favorite is ask 'Is your fav number' number""")

    expected = textwrap.dedent("""\
    number = '10'
    favorite = input(f'Is your fav number{number}')""")

    self.multi_level_tester(
        max_level=10,
        code=code,
        expected=expected,
        extra_check_function=self.is_not_turtle()
    )

  # is - assign tests
  def test_assign_print(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet{naam}')""")

    self.multi_level_tester(
      max_level=10,
      code=code,
      expected=expected
    )

  def test_assign_underscore(self):
    code = textwrap.dedent("""\
    voor_naam is Hedy
    print 'ik heet '""")

    expected = textwrap.dedent("""\
    voor_naam = 'Hedy'
    print(f'ik heet ')""")

    self.single_level_tester(code=code, expected=expected)
  def test_assign_bengali(self):
    hashed_var = hedy.hash_var("নাম")

    code = textwrap.dedent("""\
    নাম is হেডি""")

    expected = textwrap.dedent(f"""\
    {hashed_var} = 'হেডি'""")

    self.single_level_tester(code=code, expected=expected)
  def test_assign_Python_keyword(self):
    hashed_var = hedy.hash_var("for")

    code = textwrap.dedent("""\
    for is Hedy
    print 'ik heet ' for""")

    expected = textwrap.dedent("""\
    vd55669822f1a8cf72ec1911e462a54eb = 'Hedy'
    print(f'ik heet {vd55669822f1a8cf72ec1911e462a54eb}')""")

    self.single_level_tester(code=code, expected=expected)

  #add/remove tests
  #add/remove tests
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
      max_level=11,
      code=code,
      expected=expected,
      extra_check_function = self.result_in(['koe', 'kiep', 'muis']),
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
      max_level=11,
      code=code,
      expected=expected,
      extra_check_function=self.result_in(['koe']),
    )

  def test_add_to_list(self):
    code = textwrap.dedent("""\
    color is ask 'what is your favorite color? '
    colors is green, red, blue
    add color to colors
    print colors at random""")

    expected = textwrap.dedent("""\
    color = input(f'what is your favorite color? ')
    colors = ['green', 'red', 'blue']
    colors.append(color)
    print(f'{random.choice(colors)}')""")

    self.multi_level_tester(
      max_level=11,
      code=code,
      expected=expected,
      expected_commands=['ask', 'is', 'add', 'print', 'random']
    )
  def test_remove_from_list(self):
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


    self.multi_level_tester(
      max_level=11,
      code=code,
      expected=expected
    )


  # negative tests
  def test_print_without_quotes(self):
    with self.assertRaises(hedy.exceptions.UnquotedTextException) as context:
      result = hedy.transpile("print felienne 123", self.level)

    self.assertEqual('Unquoted Text', context.exception.error_code)  # hier moet nog we een andere foutmelding komen!

  #combined tests
  def test_assign_print_bengali(self):
    hashed_var = hedy.hash_var("নাম")
    self.assertEqual('veb9b5c786e8cde0910df4197f630ee75', hashed_var)

    code = textwrap.dedent("""\
    নাম is হেডি
    print 'আমার নাম is ' নাম""")
    expected = textwrap.dedent("""\
    veb9b5c786e8cde0910df4197f630ee75 = 'হেডি'
    print(f'আমার নাম is {veb9b5c786e8cde0910df4197f630ee75}')""")

    self.single_level_tester(code=code, expected=expected)
  def test_assign_print_chinese(self):
    hashed_var = hedy.hash_var("你世界")
    self.assertEqual('v406b71a2caed270b782fe8a1f2d5741a', hashed_var)

    code = textwrap.dedent("""\
    你世界 is 你好世界
    print 你世界""")
    expected = textwrap.dedent("""\
    v406b71a2caed270b782fe8a1f2d5741a = '你好世界'
    print(f'{v406b71a2caed270b782fe8a1f2d5741a}')""")

    self.single_level_tester(code=code, expected=expected)

  def test_print_list_var_random(self):

    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print 'hallo ' dieren at random""")
    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(f'hallo {random.choice(dieren)}')""")

    list = ['hallo Hond', 'hallo Kat', 'hallo Kangoeroe']

    self.single_level_tester(code=code, expected=expected, extra_check_function=self.result_in(list))
  def test_ask_print(self):

    code = textwrap.dedent("""\
    kleur is ask 'wat is je lievelingskleur?'
    print 'jouw lievelingskleur is dus' kleur '!'""")
    expected = textwrap.dedent("""\
    kleur = input(f'wat is je lievelingskleur?')
    print(f'jouw lievelingskleur is dus{kleur}!')""")

    self.single_level_tester(code=code, expected=expected)

  def test_ask_assign(self):

    code = textwrap.dedent("""\
    ding is kleur
    antwoord is ask 'Wat is je lievelings ' ding
    print 'Jouw favoriet is dus ' antwoord""")
    expected = textwrap.dedent("""\
    ding = 'kleur'
    antwoord = input(f'Wat is je lievelings {ding}')
    print(f'Jouw favoriet is dus {antwoord}')""")

    self.single_level_tester(code=code, expected=expected)

  def test_forward_ask(self):
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


  #negative tests
  def test_var_undefined_error_message(self):
    code = textwrap.dedent("""\
      naam is Hedy
      print 'ik heet ' name""")

    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.UndefinedVarException,
      max_level=10
    )

    # deze extra check functie kan nu niet mee omdat die altijd op result werkt
    # evt toch splitsen in 2 (pos en neg?)
    # self.assertEqual('name', context.exception.arguments['name'])

  def test_issue_375(self):
    code = textwrap.dedent("""\
      is Foobar
      print welcome""")

    with self.assertRaises(hedy.exceptions.ParseException) as context:
      result = hedy.transpile(code, self.level)

    #todo these could be tested in an extra_function too?
    self.assertEqual('Parse', context.exception.error_code)
    self.assertEqual(1, context.exception.error_location[0])
    self.assertEqual(1, context.exception.error_location[1])

  @parameterized.expand(HedyTester.quotes)
  def test_missing_opening_quote(self, q):
    code = f"""print hallo wereld{q}"""

    self.single_level_tester(code, exception=hedy.exceptions.UnquotedTextException)
  
  def test_missing_all_quotes(self):
    code = textwrap.dedent("""\
      print hallo wereld""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      exception=hedy.exceptions.UndefinedVarException,
    )

  def test_no_keyword_detected(self):
    code = textwrap.dedent("""\
      'competitie die gaan we winnen'""")

    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.MissingCommandException,
      max_level=11 # todo we should update the grammar of level 12 so this also works
    )

  def test_print_Spanish(self):
    code = textwrap.dedent("""\
    print 'Cuál es tu color favorito?'""")
    expected = textwrap.dedent("""\
    print(f'Cuál es tu color favorito?')""")

    self.multi_level_tester(
      code=code,
      max_level=11,
      expected=expected
    )

  def test_repair(self):
    code = "print ,'Hello'"
    with self.assertRaises(hedy.exceptions.ParseException) as context:
      result = hedy.transpile(code, self.level)

    self.assertEqual("print 'Hello'", context.exception.fixed_code)



  #assorti
  def test_detect_accented_chars(self):
    self.assertEqual(True, hedy.hash_needed('éyyy'))
    self.assertEqual(True, hedy.hash_needed('héyyy'))
    self.assertEqual(False, hedy.hash_needed('heyyy'))

  @parameterized.expand(HedyTester.quotes)
  def test_meta_column_missing_closing_quote(self, q):
    code = textwrap.dedent(f"""\
    print {q}Hello{q}
    print {q}World""")

    instance = hedy.IsValid()
    instance.level = self.level
    program_root = hedy.parse_input(code, self.level, 'en')
    is_valid = instance.transform(program_root)
    _, invalid_info = is_valid

    invalid_info = invalid_info[0]

    line = invalid_info.line
    column = invalid_info.column

    self.assertEqual(2, line)
    self.assertEqual(7, column)

  @parameterized.expand(HedyTester.quotes)
  def test_meta_column_missing_opening_quote(self, q):
    code = textwrap.dedent(f"""\
    print {q}Hello{q}
    print World{q}""")

    instance = hedy.IsValid()
    instance.level = self.level
    program_root = hedy.parse_input(code, self.level, 'en')
    is_valid = instance.transform(program_root)
    _, invalid_info = is_valid

    invalid_info = invalid_info[0]

    line = invalid_info.line
    column = invalid_info.column

    self.assertEqual(2, line)
    self.assertEqual(7, column)

  def test_list_values_in_single_quotes(self):
    code = textwrap.dedent(f"""\
      taart is 'appeltaart, choladetaart, kwarktaart'
      print 'we bakken een' taart at random""")

    expected = textwrap.dedent("""\
      taart = ['\\'appeltaart', 'choladetaart', 'kwarktaart\\'']
      print(f'we bakken een{random.choice(taart)}')""")

    self.multi_level_tester(
      code=code,
      max_level=11,
      expected=expected)

  def test_list_values_with_single_quotes(self):
    code = textwrap.dedent(f"""\
      taart is 'appeltaart', 'choladetaart', 'kwarktaart'
      print 'we bakken een' taart at random""")

    expected = textwrap.dedent("""\
      taart = ['\\'appeltaart\\'', '\\'choladetaart\\'', '\\'kwarktaart\\'']
      print(f'we bakken een{random.choice(taart)}')""")

    self.multi_level_tester(code=code, max_level=11, expected=expected)

  def test_list_values_in_double_quotes(self):
    code = textwrap.dedent(f"""\
      taart is "appeltaart, choladetaart, kwarktaart"
      print 'we bakken een' taart at random""")

    expected = textwrap.dedent("""\
      taart = ['"appeltaart', 'choladetaart', 'kwarktaart"']
      print(f'we bakken een{random.choice(taart)}')""")

    self.multi_level_tester(code=code, max_level=11, expected=expected)
