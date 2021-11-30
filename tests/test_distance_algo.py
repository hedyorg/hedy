import unittest
import hedy

class TestsHelperFunctions(unittest.TestCase):

  def test_empty_command(self):
    invalid_command = ""
    keywords_en_level_1 = hedy.get_suggestions_for_language('en',1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('ask', closest)

  def test_self_command_print(self):
    invalid_command = "print"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en',1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual(None, closest)

  def test_self_command_ask(self):
    invalid_command = "ask"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en',1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual(None, closest)

  def test_self_command_echo(self):
    invalid_command = "echo"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en',1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual(None, closest)

  def test_print_command_1(self):
    invalid_command = "printechoask"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en',1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('print', closest)

  def test_print_command_2(self):
    invalid_command = "printaskecho"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en',1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('print', closest)

  def test_echo_command_1(self):
    invalid_command = "echoprintask"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en',1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('echo', closest)

  def test_echo_command_2(self):
    invalid_command = "echoprint ask"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en',1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('echo', closest)

  def test_echo_command_3(self):
    invalid_command = "echo print ask"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en',1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('echo', closest)

  def test_ask_command_1(self):
    invalid_command = "hello ask echoprint"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en',1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('ask', closest)

  def test_echo_command_4(self):
    invalid_command = "hello Ask echo0 print"
    keywords_en_level_1 = hedy.get_suggestions_for_language('en',1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('echo', closest)

  def test_ask_command_nl(self):
    invalid_command = "vrag wat is er?"
    keywords_en_level_1 = hedy.get_suggestions_for_language('nl',1)
    closest = hedy.closest_command(invalid_command, keywords_en_level_1)
    self.assertEqual('vraag', closest)
