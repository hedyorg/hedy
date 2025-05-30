import random
import textwrap
from dataclasses import dataclass
import pickle
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
import typing
from hedy_content import ALL_KEYWORD_LANGUAGES, KEYWORDS

from hedy_sourcemap import SourceRange
from functools import cache

from app import create_app
from hedy_error import get_error_text
from flask_babel import force_locale

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Snippet:
    def __init__(self, filename, level, code, username=None, field_name=None, adventure_name=None, experiment_language=None, error=None, language=None, key=None, counter=0):
        self.filename = filename
        self.level = level
        self.field_name = field_name if field_name is not None else ''
        self.code = code
        self.username = username
        self.error = error
        self.key = key if key is not None else ''
        filename_shorter = os.path.basename(filename)
        if language is None:
            self.language = filename_shorter.split(".")[0]
        else:
            self.language = language
        self.adventure_name = adventure_name
        self.experiment_language = experiment_language
        self.name = f'{self.language}-{self.level}-{self.key}-{self.field_name}'
        self.hash = sha1digest(self.code)
        self.counter = counter
        if counter > 0:
            self.name += f'-{self.counter + 1}'

    def __repr__(self):
        return f'Snippet({self.name})'


@dataclass
class YamlSnippet:
    """A snippet found in one of the YAML files.

    This is a replacement of 'Snippet' with fewer fields, only the fields that
    are used in the snippet tests.

    `yaml_path` is the path in the YAML where this snippet was found, as an
    array of either strings or ints.

    For example, in a YAML file that looks like:

    ```
    adventures:
        1:
            code: |
               print hello
    ```

    The `yaml_path` would be `['adventures', 1, 'code']`.
    """
    filename: str
    yaml_path: typing.List
    code: str
    language: str
    level: int

    def __post_init__(self):
        # 'code' may be replaced later on when translating keywords
        self.original_code = self.code
        self.name = f'{self.relative_filename}-{self.yaml_path_str}'

    @property
    def relative_filename(self):
        return os.path.relpath(self.filename, ROOT_DIR)

    @property
    def yaml_path_str(self):
        return '.'.join(str(x) for x in self.yaml_path)

    @property
    def location(self):
        """Returns a description of the location."""
        return f'{self.relative_filename} at {self.yaml_path_str}'


class SkippedMapping:
    """ Class used to test if a certain source mapping contains an exception type """

    def __init__(self, source_range: SourceRange, exception_type: type(Exception)):
        self.source_range = source_range
        self.exception_type = exception_type


@cache
def get_hedy_source_hash():
    grammars_dir = os.path.join(ROOT_DIR, 'grammars')

    files_affecting_parsing = (
        [os.path.join(grammars_dir, filename) for filename in os.listdir(grammars_dir)] +
        [os.path.join(ROOT_DIR, 'hedy.py')] +
        [os.path.join(ROOT_DIR, file) for file in os.listdir(ROOT_DIR) if re.fullmatch('hedy_.*\\.py', file)]
    )

    files_affecting_parsing.sort()

    files_contents = []
    for filename in files_affecting_parsing:
        with open(filename, 'r', encoding='utf-8', newline='\n') as f:
            contents = f.read()
            files_contents.append(contents)

    all_language_texts = '\n|\n'.join(files_contents)
    return hashlib.sha1(all_language_texts.encode('utf-8')).hexdigest()


class HedyTester(unittest.TestCase):

    level = None
    equality_comparison_with_is = ['is', '=']
    equality_comparison_commands = ['==', '=']
    number_comparison_commands = ['>', '>=', '<', '<=']
    comparison_commands = number_comparison_commands + ['!=']
    arithmetic_operations = ['+', '-', '*', '/']
    in_not_in_list_commands = ['in', 'not in']
    quotes = ["'", '"']
    booleans = [('true', True), ('True', True), ('false', False), ('False', False)]
    commands_level_4 = [("print 'hello'", "print(f'hello')"),
                        ("name is ask 'who?'", "name = input(f'who?')"),
                        ('name is Harry', "name = 'Harry'")]

    @classmethod
    def setUpClass(cls):
        os.environ["ENABLE_SKIP_FAULTY"] = 'True'  # Always test with skipping faulty enabled

    def snippet_already_tested_with_current_hedy_version(self, test_hash):
        try:
            total_hash_incl_the_hedy_language = create_hash(get_hedy_source_hash(), test_hash)
            if total_hash_incl_the_hedy_language is None:
                return False
            filename = get_hash_filename(total_hash_incl_the_hedy_language)
            already_successful = os.path.isfile(filename)
            return already_successful
        except UnicodeEncodeError:  # some tests (generated by Hypothesis) can't be hashed
            return False

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

        code += parse_result.code
        # remove sleep comments to make program execution less slow
        code = re.sub(r'time\.sleep\([^\n]*\)', 'pass', code)

        with HedyTester.captured_output() as (out, err):
            exec(code, locals())
        return out.getvalue().strip()

    def name(self):
        return inspect.stack()[1][3]

    def is_not_turtle(self):
        return lambda result: not result.has_turtle

    def is_turtle(self):
        return lambda result: result.has_turtle

    def result_in(self, list_):
        return lambda result: HedyTester.run_code(result) in list_

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

    def multi_level_tester(
            self,
            code,
            max_level=hedy.HEDY_MAX_LEVEL,
            expected=None,
            exception=None,
            skipped_mappings: 'list[SkippedMapping]' = None,
            extra_check_function=None,
            expected_commands=None,
            unused_allowed=False,
            lang='en',
            translate=True,
            output=None,
            skip_faulty=True,
            microbit=False
    ):
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
                skipped_mappings=skipped_mappings,
                extra_check_function=extra_check_function,
                expected_commands=expected_commands,
                unused_allowed=unused_allowed,
                lang=lang,
                translate=translate,
                output=output,
                skip_faulty=skip_faulty,
                microbit=microbit)
            print(f'Passed for level {level}')

    def single_level_tester(
            self,
            code,
            level=None,
            exception=None,
            skipped_mappings: 'list[SkippedMapping]' = None,
            expected=None,
            extra_check_function=None,
            output=None,
            expected_commands=None,
            unused_allowed=False,
            lang='en',
            translate=True,
            skip_faulty=True,
            microbit=False
    ):
        if level is None:  # no level set (from the multi-tester)? grap current level from class
            level = self.level

        # To speed up the test executing we calculate a hash of the test.
        # It is important to capture all the parameters that are passed to the function
        # as sometimes we expect a snippet to fail and sometimes we expect it to succeed.
        # We do this with `locals`, which captures a kwargs of this function and then we hash that.
        # This means we have to collect the locals at the beginning because else there will be
        # other things than arguments in the `locals()` output.

        all_args = locals()
        del all_args["self"]
        try:
            # we use pickle instead of hash for consistency across test-runs
            # see PYTHONHASHSEED
            test_hash = pickle.dumps(all_args)
        except AttributeError:
            test_hash = None
        except TypeError:
            test_hash = None

        if not self.snippet_already_tested_with_current_hedy_version(test_hash):
            if skipped_mappings is not None:
                result = hedy.transpile(code, level, lang, skip_faulty=skip_faulty, unused_allowed=unused_allowed)
                for skipped in skipped_mappings:
                    result_error = result.source_map.get_error_from_hedy_source_range(skipped.source_range)
                    self.assertEqual(expected, result.code)
                    self.assertEqual(type(result_error), skipped.exception_type)
                    if extra_check_function is not None:
                        self.assertTrue(extra_check_function(result_error))
            else:
                if exception is not None:
                    with self.assertRaises(exception) as context:
                        result = hedy.transpile(code, level, lang, skip_faulty=skip_faulty,
                                                unused_allowed=unused_allowed)
                    if extra_check_function is not None:
                        self.assertTrue(extra_check_function(context))
                else:
                    result = hedy.transpile(code, level, lang, skip_faulty=skip_faulty,
                                            unused_allowed=unused_allowed, microbit=microbit)
                    if expected is not None:
                        self.assertEqual(expected, result.code)

                    all_commands = result.commands
                    if expected_commands is not None:
                        self.assertEqual(expected_commands, all_commands)
                    # <- use this to run tests locally with unittest
                    skipped_commands = ['ask', 'input', 'clear', 'play']
                    if not any(x for x in skipped_commands if x in all_commands):
                        if microbit:
                            return
                        else:
                            self.assertTrue(self.validate_Python_code(result))

                    if output is not None:
                        if extra_check_function is None:  # most programs have no turtle so make that the default
                            extra_check_function = self.is_not_turtle()
                        self.assertEqual(output, HedyTester.run_code(result))
                        self.assertTrue(extra_check_function(result))

            # whether or not the code should give an exception,
            # if it parses, it should always be possible
            # to translate it, unless there is an NoIndentationException
            # because in that case our preprocessor throws the error so there is no parsetree
            # (todo maybe parse first?)

            skipped_exceptions = [
                hedy.exceptions.ParseException, hedy.exceptions.CodePlaceholdersPresentException,
                hedy.exceptions.TooFewIndentsStartLevelException, hedy.exceptions.TooManyIndentsStartLevelException,
                hedy.exceptions.NoIndentationException, hedy.exceptions.IndentationException,
                hedy.exceptions.ElseWithoutIfException
            ]

            if translate and exception not in skipped_exceptions and skipped_mappings is None:
                self.verify_translation(code, lang, level)

            # all ok? -> save hash!
            hash_of_run = create_hash(get_hedy_source_hash(), test_hash)
            if hash_of_run:
                filename = get_hash_filename(hash_of_run)
                os.makedirs(os.path.dirname(filename), mode=0o777, exist_ok=True)
                with open(filename, "w") as fp:
                    fp.write("")

    def verify_translation(self, code, lang, level):
        if lang == 'en':  # if it is English

            # pick a random language to translate to
            # all = list(ALL_KEYWORD_LANGUAGES.keys()) <- this no longer really holds
            # all keyword languages! TODO fix or remove

            # a nice mix of latin/non-latin and l2r and r2l!
            all = ['ar', 'ca', 'sq', 'bg', 'es', 'fi', 'fr', 'he', 'nl', 'hi', 'ur', 'te', 'th', 'vi', 'uk', 'tr']

            to_lang = random.choice(all)

            translated = hedy_translation.translate_keywords(
                code, from_lang=lang, to_lang=to_lang, level=level)
            back_in_english = hedy_translation.translate_keywords(
                translated, from_lang=to_lang, to_lang=lang, level=level).strip()
            self.assert_translated_code_equal(code, back_in_english)
        else:  # not English? translate to it and back!
            in_english = hedy_translation.translate_keywords(
                code, from_lang=lang, to_lang="en", level=level)
            back_in_org = hedy_translation.translate_keywords(
                in_english, from_lang="en", to_lang=lang, level=level)
            self.assert_translated_code_equal(code, back_in_org)

    def source_map_tester(self, code, expected_source_map: dict):
        result = hedy.transpile(code, self.level, 'en')
        self.assertDictEqual(result.source_map.get_compressed_mapping(), expected_source_map)

    def assert_translated_code_equal(self, original, translation):
        # When we translate a program we lose information about the whitespaces of the original program.
        # So when comparing the original and the translated code, we compress multiple whitespaces into one.
        # Also, we lose the trailing spaces, so we strip before comparing.
        self.assertEqual(re.sub('\\s+', ' ', original).strip(),
                         re.sub('\\s+', ' ', translation).strip())

    @staticmethod
    def validate_Python_code(parseresult):
        # Code used in the Adventure and Level Defaults tester to validate Hedy code

        try:
            if not parseresult.has_turtle and not parseresult.has_pressed:  # ouput from turtle or pygame cannot be captured
                HedyTester.run_code(parseresult)
        except hedy.exceptions.CodePlaceholdersPresentException:  # Code with blanks is allowed
            pass
        except OSError:
            return True  # programs with ask cannot be tested with output :(
        except Exception:
            return False
        return True

    def forward_transpiled(self, val):
        return self.turtle_command_transpiled('forward', val)

    def turn_transpiled(self, val):
        return self.turtle_command_transpiled('right', val)

    def turtle_command_transpiled(self, command, val):
        suffix = '\ntime.sleep(0.1)' if command == 'forward' else ''
        func = 'int_with_error' if self.level < 12 else 'number_with_error'

        return textwrap.dedent(f"""\
            __trtl = {func}({val}, {HedyTester.value_exception_transpiled()})
            t.{command}(min(600, __trtl) if __trtl > 0 else max(-600, __trtl))""") + suffix

    @staticmethod
    def sleep_transpiled(val):
        return f"time.sleep(int_with_error({val}, {HedyTester.value_exception_transpiled()}))"

    @staticmethod
    def color_transpiled(val, lang="en"):
        color_dict = {hedy_translation.translate_keyword_from_en(x, lang): x for x in hedy.english_colors}
        both_colors = hedy.command_make_color_local(lang)

        return textwrap.dedent(f'''\
        __trtl = f'{val}'
        color_dict = {color_dict}
        if __trtl not in {both_colors}:
          raise Exception(f{HedyTester.value_exception_transpiled()})
        else:
          if not __trtl in {hedy.english_colors}:
            __trtl = color_dict[__trtl]
        t.pencolor(__trtl)''')

    def input_transpiled(self, var_name, text, bool_sys=None):
        if self.level < 6:
            return f"{var_name} = input(f'{text}')"
        elif self.level < 12:
            return textwrap.dedent(f"""\
                {var_name} = input(f'{text}')
                __ns = get_num_sys({var_name})
                {var_name} = Value({var_name}, num_sys=__ns)""")
        elif self.level < 15:
            return textwrap.dedent(f"""\
                {var_name} = input(f'''{text}''')
                __ns = get_num_sys({var_name})
                try:
                  {var_name} = int({var_name})
                except ValueError:
                  try:
                    {var_name} = float({var_name})
                  except ValueError:
                    pass
                {var_name} = Value({var_name}, num_sys=__ns)""")
        else:
            bool_sys = bool_sys if bool_sys else "[{'True': True, 'False': False}, {'true': True, 'false': False}]"
            return textwrap.dedent(f"""\
                {var_name} = input(f'''{text}''')
                __ns = get_num_sys({var_name})
                __bs = None
                try:
                  {var_name} = int({var_name})
                except ValueError:
                  try:
                    {var_name} = float({var_name})
                  except ValueError:
                    __b, __bs = get_value_and_bool_sys({var_name}, {bool_sys})
                    if __b is not None:
                      {var_name} = __b
                {var_name} = Value({var_name}, num_sys=__ns, bool_sys=__bs)""")

    def remove_transpiled(self, list_name, value):
        data_part = '' if self.level < 6 else '.data'
        return textwrap.dedent(f"""\
            try:
              {list_name}{data_part}.remove({value})
            except:
              pass""")

    @staticmethod
    def play_transpiled(arg):
        return textwrap.dedent(f"""\
            play(note_with_error(localize({arg}), {HedyTester.value_exception_transpiled()}))
            time.sleep(0.5)""")

    @staticmethod
    def list_access_transpiled(list_access):
        return textwrap.dedent(f'''\
        try:
          {list_access}
        except IndexError:
          raise Exception({HedyTester.index_exception_transpiled()})''')

    def value(self, value, num_sys=None, bool_sys=None):
        value_part = f"'{value}'" if self.level < 12 else str(value)
        if num_sys:
            num_sys = num_sys if num_sys[0] == num_sys[-1] == "'" else f"'{num_sys}'"
        else:
            str_value = str(value)
            str_value = str_value[1:] if str_value and str_value[0] == '-' else str_value
            if str_value.isnumeric():
                num_sys = "'Latin'"
        num_sys_part = f', num_sys={num_sys}' if num_sys else ''
        bool_sys_part = f', bool_sys={bool_sys}' if bool_sys else ''
        return f'Value({value_part}{num_sys_part}{bool_sys_part})'

    def list_transpiled(self, *args, num_sys=None):
        args_string = ', '.join([self.value(a, num_sys) for a in args])
        return f'Value([{args_string}])'

    def int_transpiled(self, value):
        if self.level < 12 and str(value).isnumeric():
            val = f"'{value}'"
        else:
            val = f'{value}'
        return f'''int_with_error({val}, {HedyTester.value_exception_transpiled()})'''

    @staticmethod
    def number_transpiled(value):
        return f'''number_with_error({value}, {HedyTester.value_exception_transpiled()})'''

    def for_loop(self, i, begin, end, num_sys="'Latin'"):
        def for_loop_arg(arg):
            if self.level >= 12:
                return arg
            elif str(arg).isnumeric():
                return f'int({arg})'
            else:
                return self.int_transpiled(f'{arg}')

        range_begin = f'{begin}' if str(begin).isnumeric() else f'{begin}.data'
        range_end = f'{end}' if str(end).isnumeric() else f'{end}.data'
        step_begin = for_loop_arg(range_begin)
        step_end = for_loop_arg(range_end)
        return textwrap.dedent(f"""\
            __step = 1 if {step_begin} < {step_end} else -1
            for {i} in {self.range_transpiled(range_begin, range_end, num_sys)}:""")

    def range_transpiled(self, start, stop, num_sys):
        if self.level < 12:
            start_part = f'int({start})'
            stop_part = f'int({stop})'
        else:
            start_part = start
            stop_part = stop
        return f"[Value(__rv, num_sys={num_sys}) for __rv in range({start_part}, {stop_part} + __step, __step)]"

    @staticmethod
    def sum_transpiled(left, right):
        return f'''sum_with_error({left}, {right}, """Runtime Values Error""")'''

    @staticmethod
    def value_exception_transpiled():
        return '"""Runtime Value Error"""'

    @staticmethod
    def index_exception_transpiled():
        return '"""Runtime Index Error"""'

    @staticmethod
    def return_transpiled(arg):
        return textwrap.dedent(f"""\
        try:
          return Value(int(f'''{arg}'''), num_sys=get_num_sys(f'''{arg}'''))
        except ValueError:
          try:
            return Value(float(f'''{arg}'''), num_sys=get_num_sys(f'''{arg}'''))
          except ValueError:
            return Value(f'''{arg}''')""")

    def in_list_transpiled(self, val, list_name):
        if self.level < 12:
            data_part = '.data' if self.level > 5 else ''
            return f"localize({val}) in [localize(__la{data_part}) for __la in {list_name}{data_part}]"
        else:
            return f"{val} in {list_name}.data"

    def not_in_list_transpiled(self, val, list_name):
        if self.level < 12:
            data_part = '.data' if self.level > 5 else ''
            return f"localize({val}) not in [localize(__la{data_part}) for __la in {list_name}{data_part}]"
        else:
            return f"{val} not in {list_name}.data"

    @staticmethod
    def bool_options(value):
        return ('true', 'false') if value.islower() else ('True', 'False')

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
        """Mutates the snippets in-place."""

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
            # store original code
            snippet.original_code = snippet.code
            try:
                if snippet.language in ALL_KEYWORD_LANGUAGES.keys():
                    snippet.code = snippet.code.format(**keyword_dict[snippet.language])
                else:
                    snippet.code = snippet.code.format(**english_keywords)
            except KeyError:
                print("This following snippet contains an invalid placeholder...")
                print(snippet.code)
            except ValueError:
                print("This following snippet contains an unclosed invalid placeholder...")
                print(snippet.code)

    def format_test_error_md(self, E, snippet: Snippet):
        """Given a snippet and an exception, return a Markdown string describing the problem."""
        message = []

        arrow = True  # set to False if you want to remove the <---- in the output f.e. for easy copy-pasting
        try:
            location = E.error_location
        except BaseException:
            location = 'No Location Found'

        # Must run this in the context of the Flask app, because FlaskBabel requires that.
        with create_app().app_context():
            with force_locale('en'):
                error_message = get_error_text(E, 'en')
                error_message = error_message.replace('<span class="command-highlighted">', '`')
                error_message = error_message.replace('</span>', '`')

        def add_arrow(code):
            """Adds an arrow to the given code snippet on the line that caused the error."""
            if not arrow:
                return code
            lines = code.split('\n')
            lines = [line + (" <---- ERROR HERE" if i+1 == location[0] else "")
                     for i, line in enumerate(lines)]
            return '\n'.join(lines).strip()

        rel_file = os.path.relpath(snippet.filename, ROOT_DIR)
        message.append(f'## {rel_file}')
        message.append(f'There was a problem in a level {snippet.level} snippet, at {snippet.yaml_path_str}:')

        # Use a 'caution' admonition because it renders in red
        message.append('> [!CAUTION]')
        message.append(f'> {error_message} at line {location}')

        message.append('\nTranslation source')
        message.append('```')
        message.append(add_arrow(snippet.original_code))
        message.append('```')
        message.append('\nTranslated version')
        message.append('```')
        message.append(add_arrow(snippet.code))
        message.append('```')

        return '\n'.join(message)


def create_hash(hedy_language, test_hash):
    if test_hash is None:
        return None
    t = str(test_hash) + "|\n" + hedy_language
    return hashlib.sha1(t.encode('utf-8')).hexdigest()


def get_hash_filename(input_hash):
    # We make one level of subdirectories
    # as some OS'es (Windows) does not like having too many files
    # in one directory.
    # This might be based on very outdated preconceptions, but let's
    # just copy what git does with their hash storage and not think about
    # it too long
    return os.path.join(
        ROOT_DIR,
        ".test-cache",
        input_hash[0:2],
        input_hash,
    )


def sha1digest(x):
    return hashlib.sha1(x.encode('utf-8')).hexdigest()
