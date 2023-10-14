import re
import textwrap
import exceptions
from os import path
from lark import Tree


class SourceRange:
    """
    A class used to represent source code ranges

    The source code range is made out of:
    from_line (int), from_column (int), to_line (int), to_column (int)

    An example:
    print Hello!
    ask What is your name?

    For the above snippet we could have the following mappings:
    print Hello! - from_line (1), from_column (1), to_line (1), to_column (13)
    ask What is your name? - from_line (2), from_column (1), to_line (2), to_column (23)
    Hello! - from_line (1), from_column (7), to_line (1), to_column (13)

    Tip: You can use a more advanced text editor like Notepad++ to get these values for a certain cursor position
    """

    def __init__(self, from_line, from_column, to_line, to_column):
        self.from_line = from_line
        self.from_column = from_column
        self.to_line = to_line
        self.to_column = to_column

    def __str__(self):
        return f'{self.from_line}/{self.from_column}-{self.to_line}/{self.to_column}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.from_line, self.from_column,
            self.to_line, self.to_column
        ) == (
            other.from_line, other.from_column,
            other.to_line, other.to_column
        )


class SourceCode:
    """
    A class used to represent Hedy/Python source code

    The source code range is made out of:
    a source_range (SourceRange) and the code (str)
    """

    def __init__(self, source_range: SourceRange, code: str, error: Exception = None, command_name: str = None):
        self.source_range = source_range
        self.code = code
        self.error = error
        self.command_name = command_name

    def __hash__(self):
        return hash((
            self.source_range.from_line, self.source_range.from_column,
            self.source_range.to_line, self.source_range.to_column
        ))

    def __eq__(self, other):
        return (
            self.source_range.from_line, self.source_range.from_column,
            self.source_range.to_line, self.source_range.to_column
        ) == (
            other.source_range.from_line, other.source_range.from_column,
            other.source_range.to_line, other.source_range.to_column
        )

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        if self.error is None:
            return f'{self.source_range} --- {self.code} --- {self.command_name}'
        else:
            return f'{self.source_range} -- ERROR[{self.error}] CODE[{self.code}]'

    def __repr__(self):
        return self.__str__()


class SourceMap:
    """
    A class used to represent the Hedy - Python source map.

    The map contains entries in the form of:
    SourceCode object (Hedy) - SourceCode object (Python)

    the string representation of the sourcemap is defined as:
    [Start line]-[Start Character]/[End line]-[End Character] :
        [Code]
    """

    map = dict()
    level = 0

    skip_faulty = False
    exception_found_during_parsing = None

    exceptions_not_to_skip = (
        exceptions.UnsupportedStringValue,
    )

    language = 'en'
    hedy_code = ''
    python_code = ''
    grammar_rules = []

    def __init__(self):
        self.get_grammar_rules()

    def set_level(self, level):
        self.level = level

    def set_language(self, language):
        self.language = language

    def set_skip_faulty(self, skip_faulty):
        # if the mapping encounters an error and skip_faulty is True we will 'skip' the exception
        self.skip_faulty = skip_faulty

    def set_hedy_input(self, hedy_code):
        self.hedy_code = hedy_code

    def set_python_output(self, python_code):
        self.python_code = python_code
        python_code_mapped = list()
        hedy_lines = self.hedy_code.split('\n')
        indent_size = find_program_indent_length(hedy_lines)

        def line_col(context, idx):
            return context.count('\n', 0, idx) + 1, idx - context.rfind('\n', 0, idx)

        for hedy_source_code, python_source_code in self.map.items():
            if hedy_source_code.error is not None or python_source_code.code == '':
                continue

            number_of_indents = find_indent_length(
                hedy_lines[hedy_source_code.source_range.from_line - 1]) // indent_size

            python_statement_code = textwrap.indent(python_source_code.code, '  '*number_of_indents)
            start_index = python_code.find(python_statement_code)
            code_char_length = len(python_source_code.code)

            for i in range(python_code_mapped.count(python_source_code.code)):
                start_index = python_code.find(python_statement_code, start_index+code_char_length)
                start_index = max(0, start_index)  # not found (-1) means that start_index = 0

            end_index = start_index + code_char_length
            start_line, start_column = line_col(python_code, start_index)
            end_line, end_column = line_col(python_code, end_index)

            python_source_code.source_range = SourceRange(
                start_line,
                start_column,
                end_line,
                end_column
            )

            python_code_mapped.append(python_source_code.code)

    def get_grammar_rules(self):
        script_dir = path.abspath(path.dirname(__file__))

        with open(path.join(script_dir, "grammars", "level1.lark"), "r", encoding="utf-8") as file:
            grammar_text = file.read()

        for i in range(2, 19):
            with open(path.join(script_dir, "grammars", f'level{i}-Additions.lark'), "r", encoding="utf-8") as file:
                grammar_text += '\n' + file.read()

        self.grammar_rules = re.findall(r"(\w+):", grammar_text)
        self.grammar_rules = [rule for rule in self.grammar_rules if 'text' not in rule]  # exclude text from mapping
        self.grammar_rules = list(set(self.grammar_rules))  # remove duplicates

    def add_source(self, hedy_code: SourceCode, python_code: SourceCode):
        self.map[hedy_code] = python_code

    def clear(self):
        self.map.clear()
        self.level = 0
        self.language = 'en'
        self.hedy_code = ''
        self.python_code = ''

    def get_result(self):
        response_map = dict()
        index = 0

        for hedy_source_code, python_source_code in self.map.items():
            response_map[index] = {
                'hedy_range': {
                    'from_line': hedy_source_code.source_range.from_line,
                    'from_column': hedy_source_code.source_range.from_column,
                    'to_line': hedy_source_code.source_range.to_line,
                    'to_column': hedy_source_code.source_range.to_column,
                },
                'python_range': {
                    'from_line': python_source_code.source_range.from_line,
                    'from_column': python_source_code.source_range.from_column,
                    'to_line': python_source_code.source_range.to_line,
                    'to_column': python_source_code.source_range.to_column,
                },
                'error': hedy_source_code.error,
                'command': hedy_source_code.command_name
            }

            index += 1
        return response_map

    def get_compressed_mapping(self):
        response_map = dict()

        for hedy_source_code, python_source_code in self.map.items():
            response_map[str(hedy_source_code.source_range)] = str(python_source_code.source_range)

        return response_map

    def get_error_from_hedy_source_range(self, hedy_range: SourceRange) -> Exception:
        for hedy_source_code, python_source_code in self.map.items():
            if hedy_source_code.source_range == hedy_range:
                return hedy_source_code.error

    def print_source_map(self, d, indent=0):
        for key, value in d.items():
            print('\t' * indent + str(key) + ':')
            if isinstance(value, dict):
                self.print_source_map(value, indent + 1)
            else:
                code_lines = str(value).splitlines()
                code_lines = ['\t' * (indent + 1) + str(x) for x in code_lines]
                code = "\n".join(code_lines)
                print(code)
            print('')

    def __str__(self):
        self.print_source_map(self.map)
        return str()


def source_map_rule(source_map: SourceMap):
    """ A decorator function that should decorator the transformer method (grammar rule)
        the decorator adds the hedy code & python code to the map when the transformer method (grammar rule) is used
    """

    def decorator(function):
        def wrapper(*args, **kwargs):
            meta = args[1]

            hedy_code_input = source_map.hedy_code[meta.start_pos:meta.end_pos]
            hedy_code_input = hedy_code_input.replace('#ENDBLOCK', '')  # ENDBLOCK is not part of the Hedy code, remove
            error = None

            if not source_map.skip_faulty:
                generated_python = function(*args, **kwargs)
            else:
                try:
                    generated_python = function(*args, **kwargs)

                    # When parsing with skip_faulty enabled it could happen that because sanitization is not done
                    # a tree is returned instead of a string containing valid Python code by a transformer method.
                    # If this happens we have to raise an exception, we cannot map a Lark tree

                    if (
                        # if a Lark tree is returned
                        isinstance(generated_python, Tree) or
                        # if a Lark tree is returned as a string, we check with regex
                        bool(re.match(r".*Tree\(.*Token\(.*\).*\).*", generated_python))
                    ):
                        raise Exception('Can not map a Lark tree, only strings')

                except Exception as e:
                    # If an exception is found, we set the Python code to pass (null operator)
                    # we also map the error
                    generated_python = 'pass'
                    error = e

            hedy_code = SourceCode(
                SourceRange(
                    meta.container_line, meta.container_column,
                    meta.container_end_line, meta.container_end_column
                ),
                hedy_code_input,
                error=error,
                command_name=function.__name__
            )

            python_code = SourceCode(
                # We don't know now, set_python_output will set the ranges later
                SourceRange(None, None, None, None),
                generated_python
            )

            source_map.add_source(hedy_code, python_code)
            return generated_python

        return wrapper

    return decorator


def source_map_transformer(source_map: SourceMap):
    """ A decorator function that should decorate a transformer class

        This is used for convenience, instead of adding source_map_rule to all methods,
        source_map_transformer needs only to be added to the transformer class.
        This decorator add source_map_rule to all appropriate methods.
    """

    def decorate(cls):
        for rule in cls.__dict__:
            if rule in source_map.grammar_rules:
                setattr(cls, rule, source_map_rule(source_map)(getattr(cls, rule)))
        return cls

    return decorate


def find_indent_length(line):
    number_of_spaces = 0
    for x in line:
        if x == ' ':
            number_of_spaces += 1
        else:
            break
    return number_of_spaces


def find_program_indent_length(program_lines):
    indent_size = 4
    found_indent_size = False
    for line in program_lines:
        leading_spaces = find_indent_length(line)
        # continue if line is just spaces
        if leading_spaces == len(line):
            continue

        if not found_indent_size and leading_spaces > 0:
            indent_size = leading_spaces
            found_indent_size = True

    return indent_size
