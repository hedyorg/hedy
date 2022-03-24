import hedy
import textwrap
from Tester import HedyTester



class TestsLevel1(HedyTester):
  level = 1

  # tests should be ordered as follows:
  # * commands in the order of hedy.py e..g for level 1: ['print', 'ask', 'echo', 'turn', 'forward']
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
    code = "print Hallo welkom bij Hedy!"
    expected = "print('Hallo welkom bij Hedy!')"
    expected_commands = ['print']

    self.single_level_tester(
      code=code,
      expected=expected,
      output='Hallo welkom bij Hedy!',
      expected_commands=expected_commands
    )

    self.assertEqual(['Hallo welkom bij Hedy!'], hedy.all_print_arguments(code, self.level))

  def test_print_has_no_turtle(self):
    code = "print koekoek"
    result = hedy.transpile_inner(code, self.level)
    expected = False
    self.assertEqual(expected, result.has_turtle)
    self.assertEqual(['koekoek'], hedy.all_print_arguments(code, self.level))


  def test_print_with_comma(self):
    code = "print iedereen zegt tegen hem: NERD, omdat hij de slimste van de klas is."
    expected = "print('iedereen zegt tegen hem: NERD, omdat hij de slimste van de klas is.')"
    expected_commands = ['print']

    self.single_level_tester(
      code=code,
      expected=expected,
      expected_commands=expected_commands
    )

  def test_print_multiple_lines(self):
    code = "print Hallo welkom bij Hedy\nprint Mooi hoor"
    expected = "print('Hallo welkom bij Hedy')\nprint('Mooi hoor')"

    self.single_level_tester(code=code, expected=expected)
    self.assertEqual(['Hallo welkom bij Hedy', 'Mooi hoor'], hedy.all_print_arguments(code, self.level))


  def test_print_with_quotes(self):
    code = "print 'Welcome to OceanView!'"

    expected = textwrap.dedent("""\
    print('\\'Welcome to OceanView!\\'')""")

    self.single_level_tester(
      code=code,
      expected=expected,
      output="'Welcome to OceanView!'")

  def test_print_with_slashes(self):
    code = "print 'Welcome to \\O/ceanView!'"


    expected = textwrap.dedent("""\
    print('\\'Welcome to \\\\O/ceanView!\\'')""")

    self.single_level_tester(code=code, expected=expected)

  def test_print_with_slashed_at_end(self):
    code = "print Welcome to \\"

    expected = textwrap.dedent("""\
    print('Welcome to \\\\')""")

    self.single_level_tester(
      code=code,
      expected=expected,
      output="Welcome to \\"
    )

  def test_print_with_spaces(self):
    code = "print        hallo!"
    expected = textwrap.dedent("""\
    print('hallo!')""")

    self.single_level_tester(code=code, expected=expected)

  def test_print_nl(self):
    code = "print Hallo welkom bij Hedy!"
    expected = "print('Hallo welkom bij Hedy!')"
    output = 'Hallo welkom bij Hedy!'
    self.single_level_tester(code=code,
                             expected=expected,
                             output=output,
                             lang='nl')

  def test_print_ar(self):
    code = "قول أهلا ومرحبا بكم في هيدي!"
    expected = "print('أهلا ومرحبا بكم في هيدي!')"
    output ='أهلا ومرحبا بكم في هيدي!'
    self.single_level_tester(code=code,
                             expected=expected,
                             output=output,
                             lang='ar')

  def test_print_ar_2(self):
    code = "قول مرحبا أيها العالم!"
    expected = "print('مرحبا أيها العالم!')"
    output ='مرحبا أيها العالم!'
    self.single_level_tester(code=code,
                             expected=expected,
                             output=output,
                             lang='ar')

  # ask tests
  def test_ask(self):
    code = "ask wat is je lievelingskleur?"
    expected = "answer = input('wat is je lievelingskleur?')"
    self.single_level_tester(code=code, expected=expected)

  def test_ask_Spanish(self):
    code = "ask ask Cuál es tu color favorito?"
    expected = "answer = input('ask Cuál es tu color favorito?')"
    self.single_level_tester(code=code, expected=expected)
  def test_ask_with_quotes(self):
    code = "ask 'Welcome to OceanView?'"

    expected = textwrap.dedent("""\
    answer = input('\\'Welcome to OceanView?\\'')""")

    self.single_level_tester(code=code, expected=expected)

  def test_ask_nl_code_transpiled_in_nl(self):
    code = "vraag Heb je er zin in?"
    expected = "answer = input('Heb je er zin in?')"

    self.single_level_tester(code=code,
                             expected=expected,
                             lang='nl')

  def test_ask_en_code_transpiled_in_nl(self):
    code = "ask Heb je er zin in?"
    expected = "answer = input('Heb je er zin in?')"

    self.single_level_tester(code=code,
                             expected=expected,
                             lang='nl',
                             translate=False) #we are trying a Dutch keyword in en, can't be translated

  def test_mixes_languages_nl_en(self):
    code = textwrap.dedent("""\
    vraag Heb je er zin in?
    echo
    ask are you sure?
    print mooizo!""")

    expected = textwrap.dedent("""\
    answer = input('Heb je er zin in?')
    print(answer)
    answer = input('are you sure?')
    print('mooizo!')""")

    self.single_level_tester(code=code,
                             expected=expected,
                             expected_commands=['ask', 'echo', 'ask', 'print'],
                             lang='nl',
                             translate=False) #mixed codes will not translate back to their original form, sadly

  # echo tests
  def test_echo_without_argument(self):
    code = "ask wat?\necho"
    expected = "answer = input('wat?')\nprint(answer)"
    self.single_level_tester(code=code, expected=expected)
  def test_echo_with_quotes(self):
    code = textwrap.dedent("""\
    ask waar?
    echo oma's aan de""")

    expected = textwrap.dedent("""\
    answer = input('waar?')
    print('oma\\'s aan de '+answer)""")

    self.single_level_tester(code=code, expected=expected)

  # forward tests
  def test_forward(self):
    code = "forward 50"
    expected = HedyTester.dedent(HedyTester.forward_transpiled(50))
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_forward_arabic_numeral(self):
    code = "forward ١١١١١١١"
    expected = HedyTester.forward_transpiled(1111111)
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_forward_hindi_numeral(self):
    code = "forward ५५५"
    expected = HedyTester.forward_transpiled(555)
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_forward_without_argument(self):
    code = 'forward'
    expected = textwrap.dedent("""\
      t.forward(50)
      time.sleep(0.1)""")

    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_forward_with_text_gives_type_error(self):
    code = "forward lalalala"
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_multiple_forward_without_arguments(self):
    code = "forward\nforward"
    expected = textwrap.dedent("""\
    t.forward(50)
    time.sleep(0.1)
    t.forward(50)
    time.sleep(0.1)""")

    self.single_level_tester(code=code, expected=expected, extra_check_function=self.is_turtle())

  # turn tests
  def test_turn_no_args(self):
    code = "turn"
    expected = "t.right(90)"
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_one_turn_right(self):
    code = "turn right"
    expected = "t.right(90)"

    self.single_level_tester(code=code, expected=expected,
                             extra_check_function=self.is_turtle())

  def test_one_turn_left(self):
    code = "turn left"
    expected = "t.left(90)"

    self.single_level_tester(code=code, expected=expected,
                             extra_check_function=self.is_turtle())


  def test_one_turn_left_nl(self):
    code = "draai links"
    expected = "t.left(90)"

    #TODO next step is add left/right to translation code!

    self.single_level_tester(code=code, expected=expected,
                             extra_check_function=self.is_turtle(), lang='nl')


  def test_one_turn_with_text_gives_error(self):
    code = "turn koekoek"
    self.single_level_tester(
      code=code,
      exception=hedy.exceptions.InvalidArgumentException
    )

  # comment test
  def test_comment(self):
    code = "# geen commentaar, helemaal geen!"
    expected = ""
    self.multi_level_tester(
      code=code,
      expected=expected
    )

  # combined keywords tests
  def test_print_ask_echo(self):
    code = textwrap.dedent("""\
      print Hallo
      ask Wat is je lievelingskleur
      echo je lievelingskleur is""")

    expected = textwrap.dedent("""\
      print('Hallo')
      answer = input('Wat is je lievelingskleur')
      print('je lievelingskleur is '+answer)""")

    self.single_level_tester(
      code=code,
      expected=expected,
      expected_commands=['print', 'ask', 'echo'])
  def test_forward_turn_combined(self):
    code = textwrap.dedent("""\
      forward 50
      turn
      forward 100""")
    expected = HedyTester.dedent(
      HedyTester.forward_transpiled(50),
      't.right(90)',
      HedyTester.forward_transpiled(100))
    self.multi_level_tester(
      max_level=7,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle(),
      expected_commands=['forward', 'turn', 'forward']
    )


  # markup tests
  def test_lines_may_end_in_spaces(self):
    code = "print Hallo welkom bij Hedy! "
    expected = "print('Hallo welkom bij Hedy! ')"
    self.single_level_tester(code=code, expected=expected,
                             output='Hallo welkom bij Hedy!')

  # negative tests
  def test_lines_with_space_gives_invalid(self):
    code = " print Hallo welkom bij Hedy! "
    self.single_level_tester(code=code, exception=hedy.exceptions.InvalidSpaceException)

  def test_lines_with_spaces_gives_invalid(self):
    code = " print Hallo welkom bij Hedy!\n print Hallo welkom bij Hedy!"
    self.single_level_tester(code=code, exception=hedy.exceptions.InvalidSpaceException)

  def test_word_plus_period_gives_invalid(self):
    code = "word."
    self.single_level_tester(code, exception=hedy.exceptions.MissingCommandException)

  # def test_empty_gives_exception(self):
  #   self.single_level_tester("", exception=hedy.exceptions.EmptyProgramException)

  def test_non_keyword_gives_Invalid(self):
    code = "groen"
    self.single_level_tester(code, exception=hedy.exceptions.MissingCommandException)

  def test_lonely_echo_gives_LonelyEcho(self):
    code = "echo wat dan?"
    self.single_level_tester(code, exception=hedy.exceptions.LonelyEchoException)

  def test_echo_before_ask_gives_LonelyEcho(self):
    code = textwrap.dedent("""\
    echo what can't we do?
    ask time travel """)
    self.single_level_tester(code, exception=hedy.exceptions.LonelyEchoException)

  # def test_newlines_only_gives_EmptyProgram(self):
  #   code = textwrap.dedent("""\
  #   """)
  #   self.single_level_tester(code, exception=hedy.exceptions.EmptyProgramException)

  def test_incomplete_gives_Incomplete(self):
    with self.assertRaises(hedy.exceptions.IncompleteCommandException) as context:
      result = hedy.transpile("print", self.level)
    self.assertEqual('Incomplete', context.exception.error_code)

  def test_incomplete_on_line_2_gives_Incomplete(self):
    with self.assertRaises(hedy.exceptions.IncompleteCommandException) as context:
      result = hedy.transpile("print lalalala\nprint", self.level)
    self.assertEqual('Incomplete', context.exception.error_code)
    self.assertEqual('print', str(context.exception.arguments['incomplete_command']))

  def test_print_without_argument_gives_incomplete(self):
    self.multi_level_tester(
      max_level=22,
      code="print",
      exception=hedy.exceptions.IncompleteCommandException
    )

  def test_non_keyword_with_argument_gives_invalid(self):
    self.multi_level_tester(
      max_level=10,
      code="abc felienne 123",
      exception=hedy.exceptions.InvalidCommandException
    )

  # def test_other_2(self):
  #   with self.assertRaises(Exception) as context:
  #     result = hedy.transpile("abc felienne 123", self.level)
  #   self.assertEqual(str(context.exception), 'Invalid')
  #   self.assertEqual(str(context.exception.arguments),
  #                    "{'invalid_command': 'abc', 'level': 1, 'guessed_command': 'ask'}")

