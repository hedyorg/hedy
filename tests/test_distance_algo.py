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
      {'level':3 ,'correct':'ask'    ,'mistake':'aks'    },
      {'level':4 ,'correct':'add'    ,'mistake':'addg'   },
      {'level':4 ,'correct':'print'  ,'mistake':'pridnt' },
      {'level':5 ,'correct':'else'   ,'mistake':'elyse'  },
      {'level':5 ,'correct':'forward','mistake':'fowrard'},
      {'level':5 ,'correct':'if'     ,'mistake':'fi'     },
      {'level':5 ,'correct':'in'     ,'mistake':'iv'     },
      {'level':6 ,'correct':'add'    ,'mistake':'dda'    },
      {'level':6 ,'correct':'remove' ,'mistake':'zremove'},
      {'level':7 ,'correct':'print'  ,'mistake':'pxrint' },
      {'level':7 ,'correct':'print'  ,'mistake':'pyrint' },
      {'level':8 ,'correct':'at'     ,'mistake':'ut'     },
      {'level':8 ,'correct':'from'   ,'mistake':'fro'    },
      {'level':8 ,'correct':'remove' ,'mistake':'reomve' },
      {'level':8 ,'correct':'repeat' ,'mistake':'repceat'},
      {'level':10,'correct':'is'     ,'mistake':'si'     },
      {'level':11,'correct':'from'   ,'mistake':'fmor'   },
      {'level':11,'correct':'random' ,'mistake':'raodnm' },
      {'level':12,'correct':'if'     ,'mistake':'fi'     },
      {'level':12,'correct':'sleep'  ,'mistake':'suleep' },
      {'level':13,'correct':'else'   ,'mistake':'lese'   },
      {'level':13,'correct':'for'    ,'mistake':'ofr'    },
      {'level':14,'correct':'add'    ,'mistake':'dadd'   },
      {'level':14,'correct':'to'     ,'mistake':'tio'    },
      {'level':15,'correct':'and'    ,'mistake':'adn'    },
      {'level':16,'correct':'remove' ,'mistake':'emove'  },
      {'level':17,'correct':'to'     ,'mistake':'tov'    },
    ]
    for test in listTest :
      keywords = hedy.get_suggestions_for_language('en', test['level'] )
      closest = hedy.closest_command(test['mistake'], keywords)
      self.assertEqual(test['correct'], closest)