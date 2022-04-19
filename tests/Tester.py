import textwrap
import app
import hedy, hedy_translation
import re
import sys
import io, os
from contextlib import contextmanager
import inspect
import unittest

class Snippet:
  def __init__(self, filename, level, field_name, code, adventure_name=None):
    self.filename = filename
    self.level = level
    self.field_name = field_name
    self.code = code
    filename_shorter = os.path.basename(filename)
    self.language = filename_shorter.split(".")[0]
    self.adventure_name = adventure_name
    self.name = f'{self.language}-{self.level}-{self.field_name}'


def hedy_test():
    def decorator(c):
        c.remove_inherited_test_methods()
        return c
    return decorator


class HedyTester(unittest.TestCase):
  level = None
  max_turtle_level = 10
  equality_comparison_commands = ['==', '=']
  number_comparison_commands = ['>', '>=', '<', '<=']
  comparison_commands = number_comparison_commands + ['!=']
  arithmetic_operations = ['+', '-', '*', '/']
  quotes = ["'", '"']

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
# remove sleep comments to make program execution less slow
    code = re.sub(r'time\.sleep\([^)]*\)', 'pass', code)

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

  def exception_command(self, command):
    return lambda c: c.exception.arguments['command'] == command

  @staticmethod
  def as_list_of_tuples(*args):
    # used to conver a variable number of paralel list
    # into a list of tuples to be used by the parametrized tester
    # All of the lists need to have the same size
    res = []
    for i in range(len(args[0])):
      t = tuple((item[i] for item in args))
      res.append(t)
    return res

  def multi_level_tester(self, code, max_level=hedy.HEDY_MAX_LEVEL, expected=None, exception=None, extra_check_function=None, expected_commands=None, lang='en', translate=True, output=None):
    # used to test the same code snippet over multiple levels
    # Use exception to check for an exception

    if max_level < self.level:
      raise Exception('Level too low!')

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
      self.single_level_tester(code, level, expected=expected, exception=exception, extra_check_function=extra_check_function, expected_commands=expected_commands, lang=lang, translate=translate, output=output)
      print(f'Passed for level {level}')

  def single_level_tester(self, code, level=None, exception=None, expected=None, extra_check_function=None, output=None, expected_commands=None, lang='en', translate=True):
    if level is None: # no level set (from the multi-tester)? grap current level from class
      level = self.level
    if exception is not None:
      with self.assertRaises(exception) as context:
        result = hedy.transpile(code, level, lang)

      if extra_check_function is not None:
        self.assertTrue(extra_check_function(context))

    if extra_check_function is None: # most programs have no turtle so make that the default
      extra_check_function = self.is_not_turtle()

    if expected is not None:
      result = hedy.transpile(code, level, lang)
      self.assertEqual(expected, result.code)

      if translate:
        if lang == 'en': # if it is English
          # and if the code transpiles (evidenced by the fact that we reach this line) we should be able to translate too

          #TODO FH Feb 2022: we pick Dutch here not really fair or good practice :D Maybe we should do a random language?
          in_dutch = hedy_translation.translate_keywords(code, from_lang=lang, to_lang="nl", level=self.level)
          back_in_english = hedy_translation.translate_keywords(in_dutch, from_lang="nl", to_lang=lang, level=self.level)
          self.assert_translated_code_equal(code, back_in_english)
        else: #not English? translate to it and back!
          in_english = hedy_translation.translate_keywords(code, from_lang=lang, to_lang="en", level=self.level)
          back_in_org = hedy_translation.translate_keywords(in_english, from_lang="en", to_lang=lang, level=self.level)
          self.assert_translated_code_equal(code, back_in_org)

      all_commands = hedy.all_commands(code, level, lang)
      if expected_commands is not None:
        self.assertEqual(expected_commands, all_commands)
      if (not 'ask' in all_commands) and (not 'input' in all_commands): #<- use this to run tests locally with unittest
        self.assertTrue(self.validate_Python_code(result))
      if output is not None:
        self.assertEqual(output, HedyTester.run_code(result))
        self.assertTrue(extra_check_function(result))

  def assert_translated_code_equal(self, orignal, translation):
    # When we translate a program we lose information about the whitespaces of the original program.
    # So when comparing the original and the translated code, we compress multiple whitespaces into one.
    self.assertEqual(re.sub('\\s+', ' ', orignal), re.sub('\\s+', ' ', translation))

  @staticmethod
  def validate_Hedy_code(snippet):
    # Code used in the Adventure and Level Defaults tester to validate Hedy code

    try:
      if len(snippet.code) != 0:   # We ignore empty code snippets or those of length 0
        result = hedy.transpile(snippet.code, int(snippet.level), snippet.language)
        all_commands = hedy.all_commands(snippet.code, snippet.level, snippet.language)

        if not result.has_turtle and (not 'ask' in all_commands) and (not 'input' in all_commands): #output from turtle cannot be captured
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

  # The turtle commands get transpiled into big pieces of code that probably will change
  # The followings methods abstract the specifics of the tranpilation and keep tests succinct
  @staticmethod
  def forward_transpiled(val):
    return HedyTester.turtle_command_transpiled('forward', val)

  @staticmethod
  def turn_transpiled(val):
    return HedyTester.turtle_command_transpiled('right', val)

  @staticmethod
  def turtle_command_transpiled(command, val):
    command_text = 'turn'
    suffix = ''
    if command == 'forward':
      command_text = 'forward'
      suffix = '\n      time.sleep(0.1)'
    return textwrap.dedent(f"""\
      trtl = {val}
      try:
        trtl = int(trtl)
      except ValueError:
        raise Exception(f'While running your program the command <span class="command-highlighted">{command_text}</span> received the value <span class="command-highlighted">{{trtl}}</span> which is not allowed. Try changing the value to a number.')
      t.{command}(min(600, trtl) if trtl > 0 else max(-600, trtl)){suffix}""")

  # Used to overcome indentation issues when the above code is inserted
  # in test cases which use different indentation style (e.g. 2 or 4 spaces)
  @staticmethod
  def dedent(*args):
    return '\n'.join([textwrap.indent(textwrap.dedent(a[0]), a[1]) if type(a) is tuple else textwrap.dedent(a)
                      for a in args])

  @classmethod
  def remove_inherited_test_methods(cls):
    """
    Removes test methods defined in parent classes.
    """
    get_test_methods = lambda c: set([name for name in list(vars(c))
                                      if name.startswith("test_") and callable(getattr(c, name))])

    # holds all test methods which are not defined in the current class, i.e. should not be executed. Note that even
    # tests that are overloaded in the current class have to be removed from the base class to avoid double execution.
    base_class_tests = {base: get_test_methods(base) for base in cls.__bases__}

    for base, tests in base_class_tests.items():
      for test in tests:
        delattr(base, test)
      # it is necessary to call recursively to ensure that transitive test methods from upper base classes are
      # removed too. If A(), B(A) and C(B), then this guarantees no test methods from A will be executed in C
      if hasattr(base, "remove_inherited_test_methods"):
        base.remove_inherited_test_methods()
