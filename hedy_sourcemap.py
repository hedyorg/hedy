import re
from os import path

from lark import Tree, ParseError


class SourceRange:
    """
    A class used to represent source code ranges

    The source code range is made out of:
    from_line (int), from_character (int), to_line (int), to_character (int)
    """

    def __init__(self, from_line, from_character, to_line, to_character):
        self.from_line = from_line
        self.from_character = from_character
        self.to_line = to_line
        self.to_character = to_character

    def __str__(self):
        return f'{self.from_line}/{self.from_character}-{self.to_line}/{self.to_character}'

    def __repr__(self):
        return self.__str__()


class SourceCode:
    """
    A class used to represent Hedy/Python source code

    The source code range is made out of:
    a source_range (SourceRange) and the code (str)
    """

    def __init__(self, source_range: SourceRange, code: str, error: Exception = None):
        self.source_range = source_range
        self.code = code
        self.error = error

    def __hash__(self):
        return hash((
            self.source_range.from_line, self.source_range.from_character,
            self.source_range.to_line, self.source_range.to_character
        ))

    def __eq__(self, other):
        return (
            self.source_range.from_line, self.source_range.from_character,
            self.source_range.to_line, self.source_range.to_character
        ) == (
            other.source_range.from_line, other.source_range.from_character,
            other.source_range.to_line, other.source_range.to_character
        )

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        if self.error is None:
            return f'{self.source_range} --- {self.code}'
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
    language = 'en'
    hedy_code = ''
    python_code = ''

    def __init__(self):
        script_dir = path.abspath(path.dirname(__file__))

        with open(path.join(script_dir, "grammars", "level1.lark"), "r", encoding="utf-8") as file:
            grammar_text = file.read()

        for i in range(2, 19):
            with open(path.join(script_dir, "grammars", f'level{i}-Additions.lark'), "r", encoding="utf-8") as file:
                grammar_text += '\n' + file.read()

        self.grammar_rules = re.findall(r"(\w+):", grammar_text)
        self.grammar_rules = [rule for rule in self.grammar_rules if 'text' not in rule]  # exclude text from mapping

    def set_level(self, level):
        self.level = level
        self.get_grammar_rules(level)

    def set_language(self, language):
        self.language = language

    def set_hedy_input(self, hedy_code):
        self.hedy_code = hedy_code

    def set_python_output(self, python_code):
        self.python_code = python_code
        python_code_mapped = list()

        for hedy_source_code, python_source_code in self.map.items():
            if hedy_source_code.error is not None or python_source_code.code == '':
                continue

            start_index = python_code.find(python_source_code.code)
            start_line = python_code[0:start_index].count('\n') + 1
            code_char_length = len(python_source_code.code)

            for i in range(python_code_mapped.count(python_source_code.code)):
                start_index = python_code.find(python_source_code.code, start_index+code_char_length)
                start_index = max(0, start_index)  # not found (-1) means that start_index = 0
                start_line = python_code[0:start_index].count('\n') + 1

            end_index = start_index + code_char_length
            code_line_length = python_code[start_index:end_index].count('\n')
            end_line = start_line + code_line_length

            python_source_code.source_range = SourceRange(
                start_line, start_index, end_line, end_index
            )

            python_code_mapped.append(python_source_code.code)

    def get_grammar_rules(self, level):
        script_dir = path.abspath(path.dirname(__file__))

        with open(path.join(script_dir, "grammars-Total", f'level{level}.en-Total.lark'), "r", encoding="utf-8") as file:
            grammar_text = file.read()

        self.grammar_rules = re.findall(r"(\w+):", grammar_text)
        self.grammar_rules = [rule for rule in self.grammar_rules if 'text' not in rule]  # exclude text from mapping

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
                    'from_character': hedy_source_code.source_range.from_character,
                    'to_line': hedy_source_code.source_range.to_line,
                    'to_character': hedy_source_code.source_range.to_character,
                },
                'python_range': {
                    'from_line': python_source_code.source_range.from_line,
                    'from_character': python_source_code.source_range.from_character,
                    'to_line': python_source_code.source_range.to_line,
                    'to_character': python_source_code.source_range.to_character,
                },
                'error': hedy_source_code.error,
            }

            index += 1

        response_map.popitem()  # remove mapping for program rule
        return response_map

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

            try:
                generated_python = function(*args, **kwargs)

                if isinstance(generated_python, Tree):
                    raise ParseError()  # code could not be parsed, raise ParseError

                error = None
            except Exception as e:
                generated_python = 'pass'
                error = e

            hedy_code = SourceCode(
                SourceRange(
                    meta.container_line, meta.container_column,
                    meta.container_end_line, meta.container_end_column
                ),
                hedy_code_input,
                error=error
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
