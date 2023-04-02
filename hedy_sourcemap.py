import re
from os import path


class SourceRange:
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
    def __init__(self, source_range: SourceRange, code: str):
        self.source_range = source_range
        self.code = code

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
        return f'{self.source_range} --- {self.code}'

    def __repr__(self):
        return self.__str__()


class SourceMap:
    map = dict()
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

    def set_hedy_input(self, hedy_code):
        self.hedy_code = hedy_code

    def set_python_output(self, python_code):
        self.python_code = python_code

        for hedy_source_code, python_source_code in self.map.items():
            start_index = python_code.find(python_source_code.code)
            start_line = python_code[0:start_index].count('\n') + 1

            code_char_length = len(python_source_code.code)
            end_index = start_index + code_char_length
            code_line_length = python_code[start_index:end_index].count('\n')
            end_line = start_line + code_line_length

            python_source_code.source_range = SourceRange(
                start_line, start_index, end_line, end_index
            )

    def add_source(self, hedy_code: SourceCode, python_code: SourceCode):
        self.map[hedy_code] = python_code

    def clear(self):
        self.map.clear()

    def get_response_object(self):
        # We can use this to return an optimized object for the front-end
        pass

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
    def decorator(function):
        def wrapper(*args, **kwargs):
            meta = args[1]
            generated_python = function(*args, **kwargs)

            hedy_code = SourceCode(
                SourceRange(meta.container_line, meta.start_pos, meta.container_end_line, meta.end_pos),
                source_map.hedy_code[meta.start_pos:meta.end_pos]
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
    def decorate(cls):
        for rule in cls.__dict__:
            if rule in source_map.grammar_rules:
                setattr(cls, rule, source_map_rule(source_map)(getattr(cls, rule)))
        return cls

    return decorate
