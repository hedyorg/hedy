import unittest
import hedy
import sys
import io
from contextlib import contextmanager
import inspect
import unittest

class HedyTester(unittest.TestCase):
  level = None
  max_Hedy_level = 23

  @contextmanager
  def captured_output(self):
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
      sys.stdout, sys.stderr = new_out, new_err
      yield sys.stdout, sys.stderr
    finally:
      sys.stdout, sys.stderr = old_out, old_err

  def run_code(self, parse_result):
    code = "import random\n" + parse_result.code
    with self.captured_output() as (out, err):
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

    if len(snippet.code) == 0:
      return True  # We ignore empty code snippets or those of length 0
    try:
      hedy.transpile(snippet.code, int(snippet.level))
      filename_shorter = snippet.filename.split("/")[3]
      language = filename_shorter.split(".")[0]
    except Exception as E:
      if len(E.args) == 0:
        error = f'{language}: adventure {snippet.adventure_name} - level #{snippet.level} - {snippet.field_name}. Error: {E.args}'
        # We print the error for readability, since otherwise they get accumulated on a long list
        print(error)
        return error
      else:
        if E.args[0] != 'Has Blanks':  # code with blanks is ok!
          error = f'{language}: level #{snippet.level} - {snippet.field_name}. Error: {E.args[0]}'
          # We print the error for readability, since otherwise they get accumulated on a long list
          print(error)
          return error
    return  True
