import unittest
import hedy

class TestsHelperFunctions(unittest.TestCase):

  def test_empty_command(self):
    invalid_command = ""
    closest = hedy.closest_command(invalid_command, ['ask', 'print', 'echo'])
    self.assertEqual('ask', closest)

  def test_self_command_print(self):
    invalid_command = "print"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual(None, closest)

  def test_self_command_ask(self):
    invalid_command = "ask"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual(None, closest)

  def test_self_command_echo(self):
    invalid_command = "echo"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual(None, closest)

  def test_print_command_1(self):
    invalid_command = "printechoask"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual("print", closest)

  def test_print_command_2(self):
    invalid_command = "printaskecho"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual("print", closest)

  def test_echo_command_1(self):
    invalid_command = "echoprintask"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual("echo", closest)

  def test_echo_command_2(self):
    invalid_command = "echoprint ask"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual("echo", closest)

  def test_echo_command_3(self):
    invalid_command = "echo print ask"
    closest = hedy.closest_command(invalid_command, ['ask', 'print', 'echo'])
    self.assertEqual("echo", closest)

  def test_ask_command_1(self):
    invalid_command = "hello ask echoprint"
    closest = hedy.closest_command(invalid_command, ['ask', 'print', 'echo'])
    self.assertEqual("ask", closest)

  def test_echo_command_4(self):
    invalid_command = "hello Ask echo0 print"
    closest = hedy.closest_command(invalid_command, ['ask', 'print', 'echo'])
    self.assertEqual("echo", closest)
