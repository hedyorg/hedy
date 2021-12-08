import unittest
import app
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
  max_turtle_level = 10
  number_comparisons_commands = ['>', '>=', '<', '<=']
  comparison_commands = number_comparisons_commands + ['!=']

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
    if parse_result.has_turtle:
      code = app.TURTLE_PREFIX_CODE + parse_result.code
    else:
      code = app.NORMAL_PREFIX_CODE + parse_result.code
    with HedyTester.captured_output() as (out, err):
      exec(code)
    return out.getvalue().strip()

  def name(self):
    return inspect.stack()[1][3]

  def is_not_turtle(self):
    return (lambda result: not result.has_turtle)

  def is_turtle(self):
    return (lambda result: result.has_turtle)

  def result_in(self, list):
    return (lambda result: HedyTester.run_code(result) in list)

  def multi_level_tester(self, code, max_level=hedy.HEDY_MAX_LEVEL, expected=None, exception=None, extra_check_function=None):
    # used to test the same code snippet over multiple levels
    # Use exception to check for an exception

    # ensure we never test levels above the max (useful for debugging)
    max_level = min(max_level, hedy.HEDY_MAX_LEVEL)

    # make it clear in the output this is a multilevel tester
    print('\n\n\n')
    print('-----------------')
    print('Multi-level test!')
    print('\n')

    # Or use expect to check for an expected Python program
    # In the second case, you can also pass an extra function to check
    for level in range(self.level, max_level + 1):
      self.single_level_tester(code, level, expected=expected, exception=exception, extra_check_function=extra_check_function)
      print(f'Passed for level {level}')

  def single_level_tester(self, code, level=None, exception=None, expected=None, extra_check_function=None, output=None):
    if level is None: # no level set (from the multi-tester)? grap current level from class
      level = self.level
    if extra_check_function is None: # most programs have no turtle so make that the default
      extra_check_function = self.is_not_turtle()
    if exception is not None:
      with self.assertRaises(exception) as context:
        result = hedy.transpile(code, level)
    if expected is not None:
      result = hedy.transpile(code, level)
      self.assertEqual(expected, result.code)
      self.assertTrue(self.validate_Python_code(result))
      if output is not None:
        self.assertEqual(output, HedyTester.run_code(result))
      if extra_check_function is not None:
        self.assertTrue(extra_check_function(result))

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

  @staticmethod
  def validate_Python_code(parseresult):
    # Code used in the Adventure and Level Defaults tester to validate Hedy code

    try:
        if not parseresult.has_turtle: #ouput from turtle cannot be captured
          output = HedyTester.run_code(parseresult)
    except hedy.exceptions.CodePlaceholdersPresentException as E: # Code with blanks is allowed
      pass
    except OSError as E:
      return True # programs with ask cannot be tested with output :(
    except Exception as E:
      return False
    return True