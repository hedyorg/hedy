import textwrap
import hashlib
import hedy
import hedy_translation
import re
import sys
import io
import os
from contextlib import contextmanager
import inspect
import unittest
import utils
from hedy_content import ALL_KEYWORD_LANGUAGES, KEYWORDS
import pickle


class Snippet:
    def __init__(self, filename, level, code, field_name=None, adventure_name=None, error=None, language=None):
        self.filename = filename
        self.level = level
        self.field_name = field_name
        self.code = code
        self.error = error
        filename_shorter = os.path.basename(filename)
        if language is None:
            self.language = filename_shorter.split(".")[0]
        else:
            self.language = language
        self.adventure_name = adventure_name
        self.name = f'{self.language}-{self.level}-{self.field_name}'
        self.hash = md5digest(self.code)


class HedyTester(unittest.TestCase):

    level = None
    equality_comparison_with_is = ['is', '=']
    equality_comparison_commands = ['==', '=']
    number_comparison_commands = ['>', '>=', '<', '<=']
    comparison_commands = number_comparison_commands + ['!=']
    arithmetic_operations = ['+', '-', '*', '/']
    quotes = ["'", '"']

    @classmethod
    def setUpClass(cls):
        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        directory = os.path.join(ROOT_DIR, 'grammars')

        files_affecting_parsing = (
            [os.path.join(directory, filename) for filename in os.listdir(directory)] +
            [os.path.join(ROOT_DIR, 'hedy.py')]
        )

        # Sort these files so that the order is consistent between all platforms (this affects the hash!)
        files_affecting_parsing.sort()

        files_contents = []
        for filename in files_affecting_parsing:
            with open(filename, 'r', encoding='utf-8', newline='\n') as f:
                contents = f.read()
                files_contents.append(contents)

        all_language_texts = '\n|\n'.join(files_contents)

        cls.all_language_texts = all_language_texts
        cls.snippet_hashes = get_list_from_pickle(ROOT_DIR + '/all_snippet_hashes.pkl')
        cls.snippet_hashes_original_len = len(cls.snippet_hashes)

    @classmethod
    def tearDownClass(cls):
        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Only write file if we added any hashes to it and the env var is set
        if os.getenv('save_snippet_hashes') and cls.snippet_hashes_original_len != len(cls.snippet_hashes):
            with open(ROOT_DIR + '/all_snippet_hashes.pkl', 'wb') as f:
                pickle.dump(cls.snippet_hashes, f)

    def snippet_already_tested_with_current_hedy_version(self, snippet, level):
        hash_language_plus_snippet_and_level = self.create_hash(self.all_language_texts, snippet, level)
        return hash_language_plus_snippet_and_level in self.snippet_hashes

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
        code = utils.NORMAL_PREFIX_CODE

        if parse_result.has_turtle:
            code += utils.TURTLE_PREFIX_CODE
        if parse_result.has_pygame:
            code += utils.PYGAME_PREFIX_CODE

        code += parse_result.code
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

    def multi_level_tester(
            self,
            code,
            max_level=hedy.HEDY_MAX_LEVEL,
            expected=None,
            exception=None,
            extra_check_function=None,
            expected_commands=None,
            lang='en',
            translate=True,
            output=None):
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
            self.single_level_tester(
                code,
                level,
                expected=expected,
                exception=exception,
                extra_check_function=extra_check_function,
                expected_commands=expected_commands,
                lang=lang,
                translate=translate,
                output=output)
            print(f'Passed for level {level}')

    def single_level_tester(
            self,
            code,
            level=None,
            exception=None,
            expected=None,
            extra_check_function=None,
            output=None,
            expected_commands=None,
            lang='en',
            translate=True):
        if level is None:  # no level set (from the multi-tester)? grap current level from class
            level = self.level
        if not self.snippet_already_tested_with_current_hedy_version(code, level):
            if exception is not None:
                with self.assertRaises(exception) as context:
                    result = hedy.transpile(code, level, lang)
                if extra_check_function is not None:
                    self.assertTrue(extra_check_function(context))
            else:
                result = hedy.transpile(code, level, lang)
                if expected is not None:
                    self.assertEqual(expected, result.code)

                if translate:
                    if lang == 'en':  # if it is English
                        # and if the code transpiles (evidenced by the fact that we reach this
                        # line) we should be able to translate too

                        # TODO FH Feb 2022: we pick Dutch here not really fair or good practice :D
                        # Maybe we should do a random language?
                        in_dutch = hedy_translation.translate_keywords(
                            code, from_lang=lang, to_lang="nl", level=self.level)
                        back_in_english = hedy_translation.translate_keywords(
                            in_dutch, from_lang="nl", to_lang=lang, level=self.level).strip()
                        self.assert_translated_code_equal(code, back_in_english)
                    else:  # not English? translate to it and back!
                        in_english = hedy_translation.translate_keywords(
                            code, from_lang=lang, to_lang="en", level=self.level)
                        back_in_org = hedy_translation.translate_keywords(
                            in_english, from_lang="en", to_lang=lang, level=self.level)
                        self.assert_translated_code_equal(code, back_in_org)

                all_commands = hedy.all_commands(code, level, lang)
                if expected_commands is not None:
                    self.assertEqual(expected_commands, all_commands)
                if ('ask' not in all_commands) and ('input' not in all_commands):  # <- use this to run tests locally with unittest
                    self.assertTrue(self.validate_Python_code(result))
                if output is not None:
                    if extra_check_function is None:  # most programs have no turtle so make that the default
                        extra_check_function = self.is_not_turtle()
                    self.assertEqual(output, HedyTester.run_code(result))
                    self.assertTrue(extra_check_function(result))

            # all ok? -> save hash!
            self.snippet_hashes.add(self.create_hash(self.all_language_texts, code, level))

    def assert_translated_code_equal(self, orignal, translation):
        # When we translate a program we lose information about the whitespaces of the original program.
        # So when comparing the original and the translated code, we compress multiple whitespaces into one.
        self.assertEqual(re.sub('\\s+', ' ', orignal), re.sub('\\s+', ' ', translation))

    @staticmethod
    def validate_Python_code(parseresult):
        # Code used in the Adventure and Level Defaults tester to validate Hedy code

        try:
            if not parseresult.has_turtle and not parseresult.has_pygame:  # ouput from turtle or pygame cannot be captured
                HedyTester.run_code(parseresult)
        except hedy.exceptions.CodePlaceholdersPresentException:  # Code with blanks is allowed
            pass
        except OSError:
            return True  # programs with ask cannot be tested with output :(
        except Exception:
            return False
        return True

    # The turtle commands get transpiled into big pieces of code that probably will change
    # The followings methods abstract the specifics of the tranpilation and keep tests succinct
    @staticmethod
    def forward_transpiled(val, level):
        return HedyTester.turtle_command_transpiled('forward', val, level)

    @staticmethod
    def turn_transpiled(val, level):
        return HedyTester.turtle_command_transpiled('right', val, level)

    @staticmethod
    def turtle_command_transpiled(command, val, level):
        command_text = 'turn'
        suffix = ''
        if command == 'forward':
            command_text = 'forward'
            suffix = '\n      time.sleep(0.1)'

        type = 'int' if level < 12 else 'float'

        return textwrap.dedent(f"""\
      __trtl = {val}
      try:
        __trtl = {type}(__trtl)
      except ValueError:
        raise Exception(f'While running your program the command <span class="command-highlighted">{command_text}</span> received the value <span class="command-highlighted">{{__trtl}}</span> which is not allowed. Try changing the value to a number.')
      t.{command}(min(600, __trtl) if __trtl > 0 else max(-600, __trtl)){suffix}""")

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
      __trtl = f'{val}'
      if __trtl not in ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'pink', 'purple', 'red', 'white', 'yellow']:
        raise Exception(f'While running your program the command <span class="command-highlighted">color</span> received the value <span class="command-highlighted">{{__trtl}}</span> which is not allowed. Try using another color.')
      t.pencolor(__trtl)""")

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
        return '\n'.join([textwrap.indent(textwrap.dedent(a[0]), a[1]) if isinstance(a, tuple) else textwrap.dedent(a)
                          for a in args])

    @staticmethod
    def indent(code, spaces_amount=2, skip_first_line=False):
        lines = code.split('\n')

        if not skip_first_line:
            return '\n'.join([' ' * spaces_amount + line for line in lines])
        else:
            return lines[0] + '\n' + '\n'.join([' ' * spaces_amount + line for line in lines[1::]])

    @staticmethod
    def translate_keywords_in_snippets(snippets):
        # fill keyword dict for all keyword languages
        keyword_dict = {}
        for lang in ALL_KEYWORD_LANGUAGES:
            keyword_dict[lang] = KEYWORDS.get(lang)
            for k, v in keyword_dict[lang].items():
                if isinstance(v, str) and "|" in v:
                    # when we have several options, pick the first one as default
                    keyword_dict[lang][k] = v.split('|')[0]
        english_keywords = KEYWORDS.get("en")

        # We replace the code snippet placeholders with actual keywords to the code is valid: {print} -> print
        # NOTE: .format() instead of safe_format() on purpose!
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

    def create_hash(self, hedy_language, snippet, level):
        t = snippet + "|\n" + str(level) + "|\n" + hedy_language
        return hashlib.md5(t.encode('utf-8')).hexdigest()


def get_list_from_pickle(filename):
    try:
        with open(filename, 'rb') as f:
            snippet_hashes = pickle.load(f)
    except FileNotFoundError:  # non existent file
        snippet_hashes = set()
        with open(filename, 'wb') as f:
            pickle.dump(snippet_hashes, f)
    return snippet_hashes


def md5digest(x):
    return hashlib.md5(x.encode('utf-8')).hexdigest()
