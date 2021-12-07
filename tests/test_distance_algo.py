import unittest
import hedy
from test_translating import check_local_lang_bool

class TestsKeywordSuggestions(unittest.TestCase):

  def test_self_command_print(self):
    invalid_command = "print"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en', 1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual(None, closest)

  def test_self_command_ask(self):
    invalid_command = "ask"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en', 1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual(None, closest)

  def test_self_command_echo(self):
    invalid_command = "echo"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en', 1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual(None, closest)

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

  @check_local_lang_bool
  def test_ask_command_nl(self):
    invalid_command = "vrag wat is er?"
    keywords_nl_level_1 = hedy.get_suggestions_for_language('nl', 1)
    closest = hedy.closest_command(invalid_command, keywords_nl_level_1)
    self.assertEqual('vraag', closest)
