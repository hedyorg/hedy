import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel13(HedyTester):
  level = 13


  def test_list(self):
    code = textwrap.dedent("""\
    fruit is ['appel', 'banaan', 'kers']
    print(fruit)""")
    expected = textwrap.dedent("""\
    fruit = ['appel', 'banaan', 'kers']
    print(f'{fruit}')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_random(self):
    code = textwrap.dedent("""\
    dieren is ['Hond', 'Kat', 'Kangoeroe']
    print(dieren[random])""")

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(f'{random.choice(dieren)}')""")

    # check if result is in the expected list
    check_in_list = (lambda x: self.run_code(x) in ['Hond', 'Kat', 'Kangoeroe'])

    self.multi_level_tester(
      max_level=19,
      code=code,
      expected=expected,
      test_name=self.name(),
      extra_check_function=check_in_list
    )
  def test_list_multiple_spaces(self):
    code = textwrap.dedent("""\
    fruit is ['appel',  'banaan',    'kers']
    print(fruit)""")
    expected = textwrap.dedent("""\
    fruit = ['appel', 'banaan', 'kers']
    print(f'{fruit}')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_specific_access(self):
    code = textwrap.dedent("""\
    fruit is ['banaan', 'appel', 'kers']
    eerstefruit is fruit[1]
    print(eerstefruit)""")
    expected = textwrap.dedent("""\
    fruit = ['banaan', 'appel', 'kers']
    eerstefruit=fruit[1-1]
    print(f'{eerstefruit}')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

#note that print(str(highscore)) will not print as it will compare 'score[i]' as str to a variable
  def test_everything_combined(self):
    code = textwrap.dedent("""\
    score is ['100', '300', '500']
    highscore is score[random]
    print('De highscore is: ' highscore)
    for i in range(1,3):
        scorenu is score[i]
        print('Score is nu ' scorenu)
        if highscore is score[i]:
            print(highscore)""")
    expected = textwrap.dedent("""\
    score = ['100', '300', '500']
    highscore=random.choice(score)
    print(f'De highscore is: {highscore}')
    step = 1 if int(1) < int(3) else -1
    for i in range(int(1), int(3) + step, step):
      scorenu=score[i-1]
      print(f'Score is nu {scorenu}')
      if str(highscore) == str('score[i]'):
        print(f'{highscore}')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

