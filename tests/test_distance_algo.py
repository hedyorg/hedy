import unittest
import hedy
from parameterized import parameterized

class TestsKeywordSuggestions(unittest.TestCase):

  def test_self_command_print(self):
    invalid_command = "print"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en', 1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('keyword', closest)

  def test_self_command_ask(self):
    invalid_command = "ask"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en', 1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('keyword', closest)

  def test_self_command_echo(self):
    invalid_command = "echo"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en', 1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('keyword', closest)

  def test_print_difference_1(self):
    invalid_command = "pront"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en', 1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('print', closest)

  def test_print_difference_2(self):
    invalid_command = "prond"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en', 1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('print', closest)

  def test_echo_command_1(self):
    invalid_command = "echoo"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en', 1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('echo', closest)

  def test_echo_command_2(self):
    invalid_command = "ego"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en', 1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('echo', closest)

  def test_echo_command_3(self):
    invalid_command = "eechooooooo"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en', 1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual(None, closest)

  def test_ask_command_nl(self):
    invalid_command = "ask"
    keywords_nl_level_1 = hedy.get_suggestions_for_language('nl', 1)
    closest = hedy.closest_command(invalid_command, keywords_nl_level_1)
    self.assertEqual('keyword', closest)

  @parameterized.expand([
      (1  ,'print'  ,'pnirt'  ),
      (1  ,'turn'   ,'tnru'   ),
      (1 , 'turn'   ,'purn'   ),
      (3  ,'sleep'  ,'sleepb' ),
      (3 , 'at'     ,'mt'     ),
      (4  ,'ask'    ,'sk'     ),
      (4  ,'print'  ,'prtni'  ),
      (4  ,'random' ,'nandom' ),
      (4 , 'add'    ,'addg'   ),
      (4 , 'print'  ,'pridnt' ),
      (5  ,'add'    ,'wdd'    ),
      (5 , 'else'   ,'elyse'  ),
      (5 , 'else'   ,'esle'   ),
      (5 , 'forward','fowrard'),
      (5 , 'forward','fwroard'),
      (5 , 'random' ,'arndom' ),
      (6  ,'print'  ,'pritn'  ),
      (6 , 'add'    ,'dda'    ),
      (6 , 'else'   ,'eles'   ),
      (6 , 'remove' ,'zremove'),
      (6 , 'turn'   ,'tunr'   ),
      (7 , 'print'  ,'pxrint' ),
      (7 , 'print'  ,'pyrint' ),
      (7 , 'random' ,'radnom' ),
      (7 , 'times'  ,'tiems'  ),
      (8 , 'ask'    ,'abk'    ),
      (8 , 'remove' ,'reomve' ),
      (8 , 'remove' ,'rmeove' ),
      (8 , 'repeat' ,'repceat'),
      (9  ,'from'   ,'rfom'   ),
      (9 , 'remove' ,'reove'  ),
      (9 , 'times'  ,'timers' ),
      (10 ,'add'    ,'ajdd'   ),
      (11 ,'at'     ,'rt'     ),
      (11, 'for'    ,'or'     ),
      (11, 'random' ,'raodnm' ),
      (12 ,'in'     ,'inm'    ),
      (12 ,'print'  ,'rint'   ),
      (12, 'sleep'  ,'suleep' ),
      (13, 'else'   ,'lese'   ),
      (14 ,'remove' ,'remoe'  ),
      (14, 'add'    ,'dadd'   ),
      (14, 'range'  ,'raige'  ),
      (15 ,'and'    ,'asnd'   ),
      (15 ,'random' ,'rakdom' ),
      (15, 'else'   ,'ese'    ),
      (15, 'print'  ,'irpnt'  ),
      (15, 'print'  ,'pribnt' ),
      (15, 'random' ,'randoo' ),
      (15, 'while'  ,'whcle'  ),
      (16, 'print'  ,'prnit'  ),
      (16, 'remove' ,'emove'  ),
      (16, 'while'  ,'whilee' ),
      (17, 'sleep'  ,'slkep'  ),
      (18 ,'or'     ,'oru'    ),
      (18 ,'sleep'  ,'slvep'  ),
      (18, 'print'  ,'prinbt' ),
    ])
  def test_command_en(self,level,correct,mistake):
    keywords = hedy.get_suggestions_for_language('en', level )
    closest = hedy.closest_command(mistake, keywords)
    self.assertEqual(correct, closest)
