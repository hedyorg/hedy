import hedy
import textwrap
from test_level_01 import HedyTester

class TestsLevel3(HedyTester):
  level = 3

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
  def test_print(self):
    code = textwrap.dedent("""\
    print 'hallo wereld!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'hallo wereld!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_print_comma(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet ,'""")
    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet ,')""")
    self.multi_level_tester(
      code=code,
      max_level=10,
      expected=expected,
      test_name=self.name(),
      extra_check_function=self.is_not_turtle()
    )
  def test_print_two_spaces(self):
    code = "print        'hallo!'"

    expected = textwrap.dedent("""\
    print(f'hallo!')""")

    self.multi_level_tester(
      code=code,
      max_level=4,
      expected=expected,
      test_name=self.name(),
      extra_check_function=self.is_not_turtle()
    )
  def test_print_with_slashes(self):
    code = "print 'Welcome to \\'"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Welcome to \\\\')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = HedyTester.run_code(result)
    self.assertEqual("Welcome to \\", expected_output)

  # ask
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
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )

  # issue #745
  def test_print_list(self):
    code = textwrap.dedent("""\
        plaatsen is een stad, een  dorp, een strand
        print 'test' plaatsen""")

    self.multi_level_tester(
      code=code,
      max_level=10,
      exception=hedy.exceptions.InvalidArgumentTypeException,
      test_name=self.name()
    )

  def test_ask_Spanish(self):
    code = textwrap.dedent("""\
    color is ask 'Cuál es tu color favorito?'""")
    expected = textwrap.dedent("""\
    color = input('Cuál es tu color favorito?')""")
    self.multi_level_tester(
      max_level=10,
      code=code,
      expected=expected,
      extra_check_function=self.is_not_turtle(),
      test_name=self.name()
    )
  def test_ask_without_quotes(self):
    code = textwrap.dedent("""
    ding is kleur
    kleur is ask Wat is je lievelingskleur'
    print 'Jouw favoriet is dus ' kleur""")

    with self.assertRaises(hedy.exceptions.UnquotedTextException) as context:
      result = hedy.transpile(code, self.level)

    self.assertEqual('Unquoted Text', context.exception.error_code)  # hier moet nog we een andere foutmelding komen!

  # is - assign tests
  def test_assign_underscore(self):
    code = textwrap.dedent("""\
    voor_naam is Hedy
    print 'ik heet '""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    voor_naam = 'Hedy'
    print(f'ik heet ')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_assign_bengali(self):
    hashed_var = hedy.hash_var("নাম")

    code = textwrap.dedent("""\
    নাম is হেডি""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent(f"""\
    {hashed_var} = 'হেডি'""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_assign_Python_keyword(self):
    hashed_var = hedy.hash_var("for")

    code = textwrap.dedent("""\
    for is Hedy
    print 'ik heet ' for """)

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    vd55669822f1a8cf72ec1911e462a54eb = 'Hedy'
    print(f'ik heet {vd55669822f1a8cf72ec1911e462a54eb}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

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
    print 'আমার নাম is ' নাম """)

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    veb9b5c786e8cde0910df4197f630ee75 = 'হেডি'
    print(f'আমার নাম is {veb9b5c786e8cde0910df4197f630ee75}')""")

    self.assertEqual(expected, result.code)
  def test_assign_print_chinese(self):
    hashed_var = hedy.hash_var("你好世界")
    self.assertEqual('v65396ee4aad0b4f17aacd1c6112ee364', hashed_var)

    code = textwrap.dedent("""\
    你好世界 is 你好世界
    print 你好世界""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    v65396ee4aad0b4f17aacd1c6112ee364 = '你好世界'
    print(f'{v65396ee4aad0b4f17aacd1c6112ee364}')""")

    self.assertEqual(expected, result.code)

  def test_print_list_var_random(self):

    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print 'hallo ' dieren at random""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(f'hallo {random.choice(dieren)}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertIn(HedyTester.run_code(result), ['hallo Hond', 'hallo Kat', 'hallo Kangoeroe'])
  def test_ask_print(self):

    code = textwrap.dedent("""
    kleur is ask 'wat is je lievelingskleur?'
    print 'jouw lievelingskleur is dus' kleur '!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur?')
    print(f'jouw lievelingskleur is dus{kleur}!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_ask_assign(self):

    code = textwrap.dedent("""
    ding is kleur
    kleur is ask 'Wat is je lievelings' ding
    print 'Jouw favoriet is dus ' kleur""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    ding = 'kleur'
    kleur = input('Wat is je lievelings'+ding)
    print(f'Jouw favoriet is dus {kleur}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_ask_assign_list(self):
    code = textwrap.dedent("""\
    color is gree, blue
    choice is ask 'Is your favorite color one of: ' color""")

    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException,
      max_level=10,
      test_name=self.name()
    )

  def test_forward_ask(self):
    code = textwrap.dedent("""\
    afstand is ask 'hoe ver dan?'
    forward afstand""")
    expected = textwrap.dedent("""\
    afstand = input('hoe ver dan?')
    t.forward(afstand)
    time.sleep(0.1)""")
    self.multi_level_tester(
      max_level=7,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle(),
      test_name=self.name()
    )


  #negative tests
  def test_var_undefined_error_message(self):
    code = textwrap.dedent("""\
      naam is Hedy
      print 'ik heet ' name""")

    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.UndefinedVarException,
      max_level=10,
      test_name=self.name()
    )

    # deze extra check functie kan nu niet mee omdat die altijd op result werkt
    # evt toch splitsen in 2 (pos en neg?)
    # self.assertEqual('name', context.exception.arguments['name'])

  def test_issue_375(self):
    code = textwrap.dedent("""
      is Foobar
      print welcome""")

    with self.assertRaises(hedy.exceptions.ParseException) as context:
      result = hedy.transpile(code, self.level)

    self.assertEqual('Parse', context.exception.error_code)
  def test_missing_opening_quote(self):
    code = textwrap.dedent("""\
      print hallo wereld'""")

    with self.assertRaises(hedy.exceptions.UnquotedTextException) as context:
      result = hedy.transpile(code, self.level)

    self.assertEqual('Unquoted Text', context.exception.error_code)
  def test_missing_all_quotes(self):
    code = textwrap.dedent("""\
      print hallo wereld""")

    self.multi_level_tester(
      code=code,
      max_level=4,
      test_name=self.name(),
      exception=hedy.exceptions.UndefinedVarException,
    )
  def test_print_Spanish(self):
    code = textwrap.dedent("""\
    print 'Cuál es tu color favorito?'""")
    expected = textwrap.dedent("""\
    print(f'Cuál es tu color favorito?')""")

    self.multi_level_tester(
      code=code,
      max_level=11,
      test_name=self.name(),
      expected=expected,
      extra_check_function=self.is_not_turtle()
    )

  #assorti
  def test_detect_accented_chars(self):
    self.assertEqual(True, hedy.hash_needed('éyyy'))
    self.assertEqual(True, hedy.hash_needed('héyyy'))
    self.assertEqual(False, hedy.hash_needed('heyyy'))










