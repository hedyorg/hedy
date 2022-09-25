import textwrap
import hedy, hedy_translation
import re
import sys
import io, os
from contextlib import contextmanager
import inspect
import unittest
import utils
import random
from hedy_content import ALL_KEYWORD_LANGUAGES, KEYWORDS


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


class HedyTester(unittest.TestCase):
  level = None
  max_turtle_level = 10
  equality_comparison_with_is = ['is', '=']
  equality_comparison_commands = ['==', '=']
  number_comparison_commands = ['>', '>=', '<', '<=']
  comparison_commands = number_comparison_commands + ['!=']
  arithmetic_operations = ['+', '-', '*', '/']
  arithmetic_transpiled_operators = [('*', '*'), ('/', '//'), ('+', '+'), ('-', '-')]
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
      code = utils.TURTLE_PREFIX_CODE + parse_result.code
    else:
      code = utils.NORMAL_PREFIX_CODE + parse_result.code
# remove sleep comments to make program execution less slow
    code = re.sub(r'time\.sleep\([^\n]*\)', 'pass', code)

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

  def codeToInvalidInfo(self, code):
    instance = hedy.IsValid()
    instance.level = self.level
    program_root = hedy.parse_input(code, self.level, 'en')
    is_valid = instance.transform(program_root)
    _, invalid_info = is_valid

    return invalid_info[0].line, invalid_info[0].column

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

  def random_tester(self,level, programs, max_lines=30, block_size=5, max_indent=3):
    has_ask = False
    program_result_hedy = []
    program_length = 0
    program_result_python = [] 
    ident_stack = [block_size]
    last_line_hedy = ''
    # Keep looping while we have blocks to process and the program haven't reached the maximum lenght
    # If the last line needs identation we loop until we add a line inside of it
    while (ident_stack and program_length < max_lines) or hedy.needs_indentation(last_line_hedy):                
      # the identation level is how many blocks are inside the stack
      ident_level = len(ident_stack) - 1
      program = random.choice(list(programs.values()))
      program_hedy = program[0]
      program_python = program[1]
  
      if not has_ask and program_hedy.startswith('echo'):
        continue        
      if program_hedy.startswith('ask'):
        has_ask = True
      
      needs_indentation = hedy.needs_indentation(program_hedy)        
      
      if not needs_indentation or ident_level < max_indent:
        program_result_hedy.append(' '*(ident_level)*2 + program_hedy)
        last_line_hedy = program_hedy
        program_length += last_line_hedy.count('\n') + 1
        program_result_python.append(' '*(ident_level)*2 + program_python)
        # The number of sub_blocks left to add in this block
        ident_stack[-1] = ident_stack[-1] - 1
        # if this is the last sub_block, but we have indentation, we dont pop yet to be able to compute the number of spaces
        # correctly
        if ident_stack[-1] <= 0 and not needs_indentation:
          ident_stack.pop()
          
        if needs_indentation and ident_level < max_indent:
          ident_stack.append(random.randint(1, block_size))
          
      result_python = '\n'.join(program_result_python)
      result_hedy  = '\n'.join(program_result_hedy)
      self.single_level_tester(code=result_hedy, expected=result_python, level=level)

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

  @staticmethod
  def sleep_command_transpiled(val):
    return textwrap.dedent(f"""\
        try:
          time.sleep(int({val}))
        except ValueError:
          raise Exception(f'While running your program the command <span class="command-highlighted">sleep</span> received the value <span class="command-highlighted">{{{val}}}</span> which is not allowed. Try changing the value to a number.')""")

  @staticmethod
  def turtle_color_command_transpiled(val):
    return textwrap.dedent(f"""\
      trtl = f'{val}'
      if trtl not in ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'pink', 'purple', 'red', 'white', 'yellow']:
        raise Exception(f'While running your program the command <span class="command-highlighted">color</span> received the value <span class="command-highlighted">{{trtl}}</span> which is not allowed. Try using another color.')
      t.pencolor(trtl)""")

  @staticmethod
  def input_transpiled(var_name, text):
    return textwrap.dedent(f"""\
    {var_name} = input(f'''{text}''')
    try:
      {var_name} = int({var_name})
    except ValueError:
      try:
        {var_name} = float({var_name})
      except ValueError:
        pass""")

  @staticmethod
  def remove_transpiled(list_name, value):
    return textwrap.dedent(f"""\
      try:
        {list_name}.remove({value})
      except:
        pass""")

  # Used to overcome indentation issues when the above code is inserted
  # in test cases which use different indentation style (e.g. 2 or 4 spaces)
  @staticmethod
  def dedent(*args):
    return '\n'.join([textwrap.indent(textwrap.dedent(a[0]), a[1]) if type(a) is tuple else textwrap.dedent(a)
                      for a in args])

  @staticmethod
  def translate_keywords_in_snippets(snippets):
    # fill keyword dict for all keyword languages
    keyword_dict = {}
    for lang in ALL_KEYWORD_LANGUAGES:
      keyword_dict[lang] = KEYWORDS.get(lang)
      for k, v in keyword_dict[lang].items():
        if type(v) == str and "|" in v:
          # when we have several options, pick the first one as default
          keyword_dict[lang][k] = v.split('|')[0]
    english_keywords = KEYWORDS.get("en")

    # We replace the code snippet placeholders with actual keywords to the code is valid: {print} -> print
    for snippet in snippets:
      try:
        if snippet[1].language in ALL_KEYWORD_LANGUAGES.keys():
          snippet[1].code = snippet[1].code.format(**keyword_dict[snippet[1].language])
        else:
          snippet[1].code = snippet[1].code.format(**english_keywords)
      except KeyError:
        print("This following snippet contains an invalid placeholder...")
        print(snippet)
      except ValueError:
        print("This following snippet contains an unclosed invalid placeholder...")
        print(snippet)


    return snippets