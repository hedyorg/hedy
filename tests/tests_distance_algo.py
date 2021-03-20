import unittest
import hedy

class TestsHelperFunctions(unittest.TestCase):

  def test_closest_command(self):
    invalid_command = ""
    closest = hedy.closest_command(invalid_command, ['ask', 'print', 'echo'])
    self.assertEqual(closest, 'ask')

    invalid_command = "print"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual(closest, "print")

    invalid_command = "ask"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual(closest, "ask")

    invalid_command = "echo"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual(closest, "echo")

    invalid_command = "printechoask"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual(closest, "print")

    invalid_command = "printaskecho"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual(closest, "print")

    invalid_command = "echoprintask"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual(closest, "echo")

    invalid_command = "echoprint ask"
    closest = hedy.closest_command(invalid_command, ['print', 'ask', 'echo'])
    self.assertEqual(closest, "echo")

    invalid_command = "echo print ask"
    closest = hedy.closest_command(invalid_command, ['ask', 'print', 'echo'])
    self.assertEqual(closest, "echo")

    invalid_command = "hello ask echoprint"
    closest = hedy.closest_command(invalid_command, ['ask', 'print', 'echo'])
    self.assertEqual(closest, "ask")

    invalid_command = "hello Ask echo0 print"
    closest = hedy.closest_command(invalid_command, ['ask', 'print', 'echo'])
    self.assertEqual(closest, "echo")
