from dataclasses import dataclass

from lexer import HedyLexer


@dataclass
class HedyParserConfig:
    pass


class HedyParser:
    def __init__(self, lexer: HedyLexer, config: HedyParserConfig):
        self.config = config
        self.lexer = lexer

    def program(self):
        raise NotImplementedError



