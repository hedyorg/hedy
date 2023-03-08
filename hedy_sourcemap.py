
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
    map = {}
    hedy_code = ''
    python_line = 0

    def set_hedy_input(self, hedy_code):
        self.hedy_code = hedy_code

    def add_source(self, hedy_code: SourceCode, python_code: SourceCode):
        self.map[hedy_code] = python_code

    def clear(self):
        self.python_line = 0
        self.map.clear()

    def get_response_object(self):
        # We can use this to return an optimized object for the front-end
        pass

    def __str__(self):
        return str(self.map)


def source_map_rule(source_map: SourceMap):
    def decorator(function):
        def wrapper(*args, **kwargs):
            meta = args[1]
            generated_python = function(*args, **kwargs)

            hedy_code = SourceCode(
                SourceRange(meta.container_line, meta.start_pos, meta.container_end_line, meta.end_pos),
                source_map.hedy_code[meta.start_pos:meta.end_pos]
            )
            source_map.python_line += 1
            current_line = source_map.python_line
            source_map.python_line += generated_python.count('\n')
            python_code = SourceCode(
                SourceRange(current_line, 0, 0, source_map.python_line),  # this is tricky
                generated_python
            )
            source_map.add_source(hedy_code, python_code)

            return generated_python
        return wrapper
    return decorator
