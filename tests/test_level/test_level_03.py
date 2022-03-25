import hedy
import textwrap
from Tester import HedyTester
from parameterized import parameterized

class TestsLevel3(HedyTester):
  level = 3

  # tests should be ordered as follows:
  # * commands in the order of hedy.py e..g for level 2: ['print', 'ask', 'echo', 'is', 'turn', 'forward']
  # * combined tests
  # * markup tests
  # * negative tests (inc. negative & multilevel)

  # test name conventions are like this:
  # * single keyword positive tests are just keyword or keyword_special_case
  # * multi keyword positive tests are keyword1_keywords_2
  # * negative tests should be
  # * situation_gives_exception


  #print tests
  def test_print(self):
    code = "print Hallo welkom bij Hedy!"
    expected = textwrap.dedent("""\
    print(f'Hallo welkom bij Hedy!')""")

    self.single_level_tester(code=code, expected=expected)

  def test_print_comma(self):
    code = "print welkom bij steen, schaar, papier"
    expected = textwrap.dedent("""\
    print(f'welkom bij steen, schaar, papier')""")

    self.single_level_tester(code=code, expected=expected)

  def test_assign_dutch_comma_arabic(self):
      code = "صديقي هو احمد, خالد, حسن"
      expected = textwrap.dedent("""\
      vbd60ecd50ef1238a3f6a563bcfb1d331 = ['احمد', 'خالد', 'حسن']""")

      self.multi_level_tester(
        code=code,
        max_level=6,
        expected=expected,
        lang='ar',
        translate=False
        )

  def test_assign_arabic_comma_and_is(self):
    code = "animals هو cat، dog، platypus"
    expected = "animals = ['cat', 'dog', 'platypus']"

    self.multi_level_tester(
      code=code,
      max_level=6, #TODO: should be 11 but Arabic translation is not ready over level 6 (misses _REPEAT) can be extended when translation is ready
      expected=expected,
      lang='ar')

  def test_assign_comma_arabic(self):
    code = "صديقي هو احمد، خالد، حسن"
    expected = textwrap.dedent("""\
    vbd60ecd50ef1238a3f6a563bcfb1d331 = ['احمد', 'خالد', 'حسن']""")

    self.single_level_tester(code=code, expected=expected, lang='ar')

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

  def test_print_multiple_lines(self):
    code = textwrap.dedent("""\
    print Hallo welkom bij Hedy!
    print Mooi hoor""")

    expected = textwrap.dedent("""\
    print(f'Hallo welkom bij Hedy!')
    print(f'Mooi hoor')""")

    output = textwrap.dedent("""\
    Hallo welkom bij Hedy!
    Mooi hoor""")

    self.single_level_tester(code=code, expected=expected, output=output)

  def test_print_spaces(self):
    code = "print        hallo!"
    
    expected = textwrap.dedent("""\
    print(f'hallo!')""")

    self.single_level_tester(code=code, expected=expected)

  def test_print_asterisk(self):
    code = "print *Jouw* favoriet is dus kleur"
    
    expected = textwrap.dedent("""\
    print(f'*Jouw* favoriet is dus kleur')""")

    self.single_level_tester(code=code, expected=expected)

  def test_print_quotes(self):
    code = "print 'Welcome to OceanView!'"
    
    expected = textwrap.dedent("""\
    print(f'\\'Welcome to OceanView! \\'')""")

    output = "'Welcome to OceanView! '"

    self.single_level_tester(code=code, expected=expected, output=output)

  def test_print_slashes(self):
    code = "print Welcome to O/ceanView"
    expected = textwrap.dedent("""\
    print(f'Welcome to O/ceanView')""")

    output = "Welcome to O/ceanView"

    self.single_level_tester(code=code, expected=expected, output=output)

  def test_print_list_access(self):
    code = textwrap.dedent("""\
    animals is cat, dog, platypus
    print animals at random""")

    expected = textwrap.dedent("""\
    animals = ['cat', 'dog', 'platypus']
    print(f'{random.choice(animals)}')""")

    self.multi_level_tester(
      code=code,
      max_level=11,
      expected=expected
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
      max_level=10,
      code=code,
      expected=expected,
      extra_check_function=check_in_list,
      lang='fr'
    )

  #is tests
  def test_assign(self):
    code = "naam is Felienne"
    expected = textwrap.dedent("""\
    naam = 'Felienne'""")

    self.single_level_tester(code=code, expected=expected)
  def test_assign_integer(self):
    code = "naam is 14"
    expected = textwrap.dedent("""\
    naam = '14'""")

    self.single_level_tester(code=code, expected=expected)
  def test_assign_list(self):

    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe""")

    
    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']""")

    self.single_level_tester(code=code, expected=expected)

  def test_assign_list_spaces(self):
    code = textwrap.dedent("""\
    dieren is Hond , Kat , Kangoeroe""")

    #spaces are parsed in the text here, that is fine (could be avoided if we say text
    # can't *end* (or start) in a space but I find this ok for now

    expected = textwrap.dedent("""\
    dieren = ['Hond ', 'Kat ', 'Kangoeroe']""")

    self.single_level_tester(code=code, expected=expected)

  def test_assign_random_value(self):
    code = textwrap.dedent("""\
    dieren is hond, kat, kangoeroe
    dier is dieren at random
    print dier""")

    expected = textwrap.dedent("""\
    dieren = ['hond', 'kat', 'kangoeroe']
    dier = random.choice(dieren)
    print(f'{dier}')""")

    list = ['Hond', 'Kat', 'Kangoeroe']

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.result_in(list),
      max_level=11)


  def test_assign_var_to_var(self):
    code = textwrap.dedent("""\
    dier1 is hond
    dier2 is dier1
    print dier1""")

    expected = textwrap.dedent("""\
    dier1 = 'hond'
    dier2 = dier1
    print(f'{dier1}')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=5)

  def test_assign_list_exclamation_mark(self):
    code = textwrap.dedent("""\
    antwoorden is ja, NEE!, misschien
    print antwoorden at random""")

    expected = textwrap.dedent("""\
    antwoorden = ['ja', 'NEE!', 'misschien']
    print(f'{random.choice(antwoorden)}')""")

    self.single_level_tester(code=code, expected=expected)

  #ask tests
  def test_ask(self):
    code = "kleur is ask wat is je lievelingskleur?"

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur'+'?')""")

    self.single_level_tester(code=code, expected=expected)
  def test_ask_quotes(self):
    code = "name is ask 'What restaurant'"
    

    expected = textwrap.dedent("""\
    name = input('\\'What restaurant\\'')""")

    self.single_level_tester(code=code, expected=expected)
  def test_ask_Spanish_text(self):
    code = "color is ask ask Cuál es tu color favorito?"

    expected = textwrap.dedent("""\
    color = input('ask Cuál es tu color favorito'+'?')""")

    self.single_level_tester(code=code, expected=expected)
  def test_ask_bengali_var(self):
    code = textwrap.dedent("""\
      রং is ask আপনার প্রিয় রং কি?
      print রং is আপনার প্রিয""")

    expected = textwrap.dedent("""\
    ve1760b6272d4c9f816e62af4882d874f = input('আপনার প্রিয় রং কি'+'?')
    print(f'{ve1760b6272d4c9f816e62af4882d874f} is আপনার প্রিয')""")

    self.single_level_tester(code=code, expected=expected)
  def test_ask_Hungarian_var(self):
    code = textwrap.dedent("""\
      állatok is kutya, macska, kenguru
      print állatok at random""")

    expected = textwrap.dedent("""\
      v79de0191e90551f058d466c5e8c267ff = ['kutya', 'macska', 'kenguru']
      print(f'{random.choice(v79de0191e90551f058d466c5e8c267ff)}')""")

    self.single_level_tester(code=code, expected=expected)

    
  def test_ask_with_comma(self):
    code = textwrap.dedent("""\
    dieren is ask hond, kat, kangoeroe
    print dieren""")

    expected = textwrap.dedent("""\
    dieren = input('hond, kat, kangoeroe')
    print(f'{dieren}')""")

    self.single_level_tester(code=code, expected=expected)

  def test_list_access_with_type_input_gives_error(self):
    code = textwrap.dedent("""\
    animals is ask 'What are the animals?'
    print animals at random""")

    self.multi_level_tester(
      max_level=11,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_turn_number(self):
    code = textwrap.dedent("""\
      print Turtle race
      turn 90""")

    expected = HedyTester.dedent(
      "print(f'Turtle race')",
      HedyTester.turn_transpiled(90))

    self.single_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle(),
      expected_commands=['print', 'turn']
    )
  def test_turn_number_var(self):
    code = textwrap.dedent("""\
    print Turtle race
    direction is 70
    turn direction""")

    expected = HedyTester.dedent("""\
      print(f'Turtle race')
      direction = '70'""",
      HedyTester.turn_transpiled('direction'))

    self.single_level_tester(code=code, expected=expected, extra_check_function=self.is_turtle())

  #forward tests
  def test_forward_without_argument(self):
    code = textwrap.dedent("""\
    forward""")

    expected = textwrap.dedent("""\
    t.forward(50)
    time.sleep(0.1)""")

    self.single_level_tester(code=code, expected=expected, extra_check_function=self.is_turtle())

  def test_forward_with_list_variable(self):
    code = textwrap.dedent("""\
        a is 1, 2, 3
        forward a""")
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  #markup tests
  def test_spaces_in_arguments(self):
    code = "print hallo      wereld"
    expected = textwrap.dedent("""\
    print(f'hallo wereld')""")

    self.single_level_tester(code=code, expected=expected)

  #combined tests
  def test_ask_print(self):
    code = "kleur is ask wat is je lievelingskleur?\nprint kleur!"

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur'+'?')
    print(f'{kleur}!')""")

    self.single_level_tester(code=code, expected=expected)
  def test_assign_print(self):
    code = textwrap.dedent("""\
    naam is Felienne
    print naam""")

    expected = textwrap.dedent("""\
    naam = 'Felienne'
    print(f'{naam}')""")

    self.single_level_tester(code=code, expected=expected)

  def test_forward_ask(self):
    code = textwrap.dedent("""\
      afstand is ask hoe ver dan?
      forward afstand""")

    expected = HedyTester.dedent(
      "afstand = input('hoe ver dan'+'?')",
      HedyTester.forward_transpiled('afstand'))
    self.single_level_tester(code=code, expected=expected, extra_check_function=self.is_turtle())

  def test_turn_ask(self):
    code = textwrap.dedent("""\
      print Turtle race
      direction is ask Where to turn?
      turn direction""")

    expected = HedyTester.dedent("""\
      print(f'Turtle race')
      direction = input('Where to turn'+'?')""",
      HedyTester.turn_transpiled('direction'))

    self.single_level_tester(code=code, expected=expected, extra_check_function=self.is_turtle())
  def test_random_turn(self):
    code = textwrap.dedent("""\
      print Turtle race
      directions is 10, 100, 360
      turn directions at random""")

    expected = HedyTester.dedent("""\
      print(f'Turtle race')
      directions = ['10', '100', '360']""",
      HedyTester.turn_transpiled('random.choice(directions)'))

    self.single_level_tester(code=code, expected=expected, extra_check_function=self.is_turtle())

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
      max_level=10,
      code=code,
      expected=expected,
      extra_check_function=check_in_list
    )

  def test_misspell_at(self):
    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print dieren ad random""")

    self.multi_level_tester(
      max_level=10,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_assign_print_punctuation(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print Hallo naam!""")

    
    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'Hallo {naam}!')""")

    self.single_level_tester(code=code, expected=expected)
  def test_assign_print_sentence(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print naam is jouw voornaam""")

    
    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'{naam} is jouw voornaam')""")

    self.single_level_tester(code=code, expected=expected)
  def test_assign_print_something_else(self):
    code = textwrap.dedent("""\
    naam is Felienne
    print Hallo""")

    expected = textwrap.dedent("""\
    naam = 'Felienne'
    print(f'Hallo')""")

    self.single_level_tester(code=code, expected=expected)

  def test_print_list_var(self):
    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print dieren at 1""")

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(f'{dieren[1-1]}')""")

    check_in_list = (lambda x: HedyTester.run_code(x) == 'Hond')

    self.multi_level_tester(
      max_level=10,
      code=code,
      expected=expected,
      extra_check_function=check_in_list
    )

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

    self.single_level_tester(
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

    self.single_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.result_in(['koe']),
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

    self.single_level_tester(
      # max_level=3,
      code=code,
      expected=expected,
      translate=False
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

    self.multi_level_tester(
      max_level=3,
      code=code,
      expected=expected
    )

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

    self.multi_level_tester(
      max_level=3,
      code=code,
      expected=expected
    )

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

  #negative tests
  def test_echo_no_longer_in_use(self):
    code = textwrap.dedent("""\
    ask what is jouw lievelingskleur?
    echo Jouw lievelingskleur is dus...""")
    with self.assertRaises(hedy.exceptions.WrongLevelException) as context:
          hedy.transpile(code, self.level)
          self.assertEqual('Wrong Level', context.exception.error_code)
  def test_ask_without_argument_upto_22(self):
    self.multi_level_tester(
      code="name is ask",
      max_level=10,
      exception=hedy.exceptions.IncompleteCommandException
    )

  def test_random_from_string_gives_type_error(self):
    code = textwrap.dedent("""\
      items is aap noot mies
      print items at random""")
    self.multi_level_tester(
      code=code,
      max_level=5,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )
  def test_random_undefined_var(self):
    # todo could be added for higher levels but that is a lot of variations so I am not doing it now :) (FH, oct 2021)
    code = textwrap.dedent("""\
    dieren is hond, kat, kangoeroe
    print dier at random""")
    self.multi_level_tester(
      code=code,
      max_level=10,
      exception=hedy.exceptions.UndefinedVarException
    )

  def test_ask_level_2(self):
    code = textwrap.dedent("""\
    keuzes is steen, schaar, papier
    print keuzes at random
    ask is de papier goed?""")
    self.multi_level_tester(
      max_level=3,
      code=code,
      exception=hedy.exceptions.WrongLevelException
    )

  def test_list_values_in_single_quotes(self):
    code = textwrap.dedent(f"""\
      taart is 'appeltaart, choladetaart, kwarktaart'
      print 'we bakken een' taart at random""")

    expected = textwrap.dedent("""\
      taart = ['\\'appeltaart', 'choladetaart', 'kwarktaart\\'']
      print(f'\\'we bakken een\\' {random.choice(taart)}')""")

    self.single_level_tester(code=code, expected=expected)

  def test_list_values_with_single_quotes(self):
    code = textwrap.dedent(f"""\
      taart is 'appeltaart', 'choladetaart', 'kwarktaart'
      print 'we bakken een' taart at random""")

    expected = textwrap.dedent("""\
      taart = ['\\'appeltaart\\'', '\\'choladetaart\\'', '\\'kwarktaart\\'']
      print(f'\\'we bakken een\\' {random.choice(taart)}')""")

    self.single_level_tester(code=code, expected=expected)

  def test_list_values_in_double_quotes(self):
    code = textwrap.dedent(f"""\
      taart is "appeltaart, choladetaart, kwarktaart"
      print 'we bakken een' taart at random""")

    expected = textwrap.dedent("""\
      taart = ['"appeltaart', 'choladetaart', 'kwarktaart"']
      print(f'\\'we bakken een\\' {random.choice(taart)}')""")

    self.single_level_tester(code=code, expected=expected)

  def test_list_values_with_double_quotes(self):
    code = textwrap.dedent(f"""\
      taart is "appeltaart", "choladetaart", "kwarktaart"
      print "we bakken een" taart at random""")

    expected = textwrap.dedent("""\
      taart = ['"appeltaart"', '"choladetaart"', '"kwarktaart"']
      print(f'"we bakken een" {random.choice(taart)}')""")

    self.single_level_tester(code=code, expected=expected)
