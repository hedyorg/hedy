import unittest
import hedy
import sys
import io
from contextlib import contextmanager
import inspect
import unittest


class Snippet:
  def __init__(self, filename, level, field_name, code, adventure_name=None):
    self.filename = filename
    self.level = level
    self.field_name = field_name
    self.code = code
    filename_shorter = filename.split("/")[3]
    self.language = filename_shorter.split(".")[0]
    self.adventure_name = adventure_name
    self.name = f'{self.language}-{self.level}-{self.field_name}'



class HedyTester(unittest.TestCase):
  level = None
  max_Hedy_level = 23

  @staticmethod
  @contextmanager
  def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
      sys.stdout, sys.stderr = new_out, new_err
      yield sys.stdout, sys.stderr
    finally:
      sys.stdout, sys.stderr = old_out, old_err

  @staticmethod
  def run_code(parse_result):
    code = "import random\n" + parse_result.code
    with HedyTester.captured_output() as (out, err):
      exec(code)
    return out.getvalue().strip()

  def name(self):
    return inspect.stack()[1][3]

  def is_not_turtle(self):
    return (lambda x: not x.has_turtle)

  def is_turtle(self):
    return (lambda x: x.has_turtle)

  def multi_level_tester(self, test_name, code, max_level=max_Hedy_level, expected=None, exception=None, extra_check_function=None):
    # TODO: test_name could be stored in __init__ of test method
    #  if we created our own method (not sure it that is worth it?)

    # used to test the same code snippet over multiple levels
    # Use exception to check for an exception

    #ensure we never test levels above the max (sueful for debugging)
    max_level = min(max_level, hedy.HEDY_MAX_LEVEL)

    # Or use expect to check for an expected Python program
    # In the second case, you can also pass an extra function to check
    for level in range(self.level, max_level + 1):
      if exception is not None:
        with self.assertRaises(exception) as context:
          result = hedy.transpile(code, level)
      if expected is not None:
        result = hedy.transpile(code, level)
        self.assertEqual(expected, result.code)

      if extra_check_function is not None:
        self.assertTrue(extra_check_function(result))

      print(f'{test_name} passed for level {level}')

  @staticmethod
  def validate_Hedy_code(snippet):
    # Code used in the Adventure and Level Defaults tester to validate Hedy code

    try:
      if len(snippet.code) != 0:   # We ignore empty code snippets or those of length 0
        result = hedy.transpile(snippet.code, int(snippet.level))
        if not result.has_turtle: #ouput from turtle cannot be captured
          output = HedyTester.run_code(result)
    except hedy.exceptions.CodePlaceholdersPresentException as E: # Code with blanks is allowed
      pass
    except OSError as E:
      return True # programs with ask cannot be tested with output :(
    except Exception as E:
      return False
    return True

