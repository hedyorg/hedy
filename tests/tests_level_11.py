import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel11(HedyTester):
  level = 11

  def test_for_nesting(self):
    code = textwrap.dedent("""\
    for i in range 1 to 3:
      for j in range 1 to 4:
        print 'rondje: ' i ' tel: ' j""")
    expected = textwrap.dedent("""\
    step = 1 if int(1) < int(3) else -1
    for i in range(int(1), int(3) + step, step):
      step = 1 if int(1) < int(4) else -1
      for j in range(int(1), int(4) + step, step):
        print(f'rondje: {i} tel: {j}')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_if_nesting(self):
    code = textwrap.dedent("""\
    kleur is blauw
    kleurtwee is geel
    if kleur is blauw:
      if kleurtwee is geel:
        print 'Samen is dit groen!'""")
    expected = textwrap.dedent("""\
    kleur = 'blauw'
    kleurtwee = 'geel'
    if str(kleur) == str('blauw'):
      if str(kleurtwee) == str('geel'):
        print(f'Samen is dit groen!')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

#programs with issues to see if we catch them properly
# (so this should fail, for now)
# at one point we want a real "Indent" error and a better error message
# for this!

  # def test_level_7_no_indentation(self):
  #   #test that we get a parse error here
  #   code = textwrap.dedent("""\
  #   antwoord is ask Hoeveel is 10 keer tien?
  #   if antwoord is 100
  #   print 'goed zo'
  #   else
  #   print 'bah slecht'""")
  #
  #   with self.assertRaises(Exception) as context:
  #     result = hedy.transpile(code, self.level)
  #   self.assertEqual(str(context.exception), 'Parse')


