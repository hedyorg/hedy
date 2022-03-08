import unittest
import hedy

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

  def test_command_en(self):
    listTest = [
      {'level':1 ,'correct':'turn'   ,'mistake':'purn'   },
      {'level':3 ,'correct':'at'     ,'mistake':'mt'     },
      {'level':4 ,'correct':'add'    ,'mistake':'addg'   },
      {'level':4 ,'correct':'print'  ,'mistake':'pridnt' },
      {'level':5 ,'correct':'else'   ,'mistake':'elyse'  },
      {'level':5 ,'correct':'else'   ,'mistake':'esle'   },
      {'level':5 ,'correct':'forward','mistake':'fowrard'},
      {'level':5 ,'correct':'forward','mistake':'fwroard'},
      {'level':5 ,'correct':'random' ,'mistake':'arndom' },
      {'level':6 ,'correct':'add'    ,'mistake':'dda'    },
      {'level':6 ,'correct':'else'   ,'mistake':'eles'   },
      {'level':6 ,'correct':'remove' ,'mistake':'zremove'},
      {'level':6 ,'correct':'turn'   ,'mistake':'tunr'   },
      {'level':7 ,'correct':'print'  ,'mistake':'pxrint' },
      {'level':7 ,'correct':'print'  ,'mistake':'pyrint' },
      {'level':7 ,'correct':'random' ,'mistake':'radnom' },
      {'level':7 ,'correct':'times'  ,'mistake':'tiems'  },
      {'level':8 ,'correct':'ask'    ,'mistake':'abk'    },
      {'level':8 ,'correct':'remove' ,'mistake':'reomve' },
      {'level':8 ,'correct':'remove' ,'mistake':'rmeove' },
      {'level':8 ,'correct':'repeat' ,'mistake':'repceat'},
      {'level':9 ,'correct':'remove' ,'mistake':'reove'  },
      {'level':9 ,'correct':'times'  ,'mistake':'timers' },
      {'level':11,'correct':'for'    ,'mistake':'or'     },
      {'level':11,'correct':'random' ,'mistake':'raodnm' },
      {'level':12,'correct':'is'     ,'mistake':'isw'    },
      {'level':12,'correct':'sleep'  ,'mistake':'suleep' },
      {'level':13,'correct':'else'   ,'mistake':'lese'   },
      {'level':14,'correct':'add'    ,'mistake':'dadd'   },
      {'level':14,'correct':'range'  ,'mistake':'raige'  },
      {'level':15,'correct':'else'   ,'mistake':'ese'    },
      {'level':15,'correct':'print'  ,'mistake':'irpnt'  },
      {'level':15,'correct':'print'  ,'mistake':'pribnt' },
      {'level':15,'correct':'random' ,'mistake':'randoo' },
      {'level':15,'correct':'while'  ,'mistake':'whcle'  },
      {'level':16,'correct':'print'  ,'mistake':'prnit'  },
      {'level':16,'correct':'remove' ,'mistake':'emove'  },
      {'level':16,'correct':'while'  ,'mistake':'whilee' },
      {'level':17,'correct':'sleep'  ,'mistake':'slkep'  },
      {'level':18,'correct':'print'  ,'mistake':'prinbt' },
    ]
    for test in listTest :
      keywords = hedy.get_suggestions_for_language('en', test['level'] )
      closest = hedy.closest_command(test['mistake'], keywords)
      self.assertEqual(test['correct'], closest)