
class SourceCode:
    def __init__(self, hedy, python):
        self.hedy = hedy
        self.python = python

    def __str__(self):
        return (
            f'{self.hedy} <-> {self.python}'
        )

    def __repr__(self):
        return self.__str__()


class SourceRange:
    def __init__(self, from_line, from_character, to_line, to_character):
        self.from_line = from_line
        self.from_character = from_character
        self.to_line = to_line
        self.to_character = to_character

    def __hash__(self):
        return hash((self.from_line, self.from_character, self.to_line, self.to_character))

    def __eq__(self, other):
        return (
            self.from_line, self.from_character, self.to_line, self.to_character
        ) == (
            other.from_line, other.from_character, other.to_line, other.to_character
        )

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return f'{self.from_line}/{self.from_character}-{self.to_line}/{self.to_character}'

    def __repr__(self):
        return self.__str__()


class SourceMap:
    SOURCE_MAP = {}
    hedy = ''

    def set_hedy_input(self, hedy):
        self.hedy = hedy

    def add_source(self, source_range: SourceRange, source_code: SourceCode):
        self.SOURCE_MAP[source_range] = source_code

    def clear(self):
        self.SOURCE_MAP.clear()

    def get_response_object(self):
        # We can use this to return an optimized object for the front-end
        pass

    def __str__(self):
        return str(self.SOURCE_MAP)


def source_map_rule(source_map: SourceMap):
    def decorator(function):
        def wrapper(*args, **kwargs):
            meta = args[1]
            generated_python = function(*args, **kwargs)

            source_range = SourceRange(meta.container_line, meta.start_pos, meta.container_end_line, meta.end_pos)
            source = SourceCode(
                source_map.hedy[source_range.from_character:source_range.to_character],
                generated_python
            )

            source_map.add_source(source_range, source)

            return generated_python
        return wrapper
    return decorator
