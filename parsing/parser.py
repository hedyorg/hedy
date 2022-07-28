from dataclasses import dataclass
from typing import Optional

from parsing import HedyBaseLexer, HedyLexerToken, HedyLexerTokenType
from parsing.tree import HedyStringLiteral, HedyPrintStatement, HedyProgram, HedyExpression, HedyStringComposition


@dataclass
class HedyParserConfig:
    pass


class HedyBaseParser:
    def __init__(self, lexer: HedyBaseLexer, config: HedyParserConfig):
        self.config = config
        self.lexer = lexer
        self.current_token: Optional[HedyLexerToken] = None

    def next_token(self):
        self.current_token = self.lexer.token()
        return self.current_token

    def expect(self, token_type: HedyLexerTokenType) -> HedyLexerToken:
        if self.current_token != token_type:
            raise
        token = self.current_token
        self.next_token()
        return token

    def accept(self, token_type: HedyLexerTokenType) -> Optional[HedyLexerToken]:
        if self.current_token != token_type:
            return None
        token = self.current_token
        self.next_token()
        return token

    def program(self) -> HedyProgram:
        raise NotImplementedError

    def parse_expression(self) -> Optional[HedyExpression]:
        pass

    def parse_string_literal(self) -> Optional[HedyExpression]:
        pass

    def parse_print_statement(self) -> Optional[HedyExpression]:
        pass

    def parse_string_composition(self) -> Optional[HedyExpression]:
        pass


class LevelOneHedyParser(HedyBaseParser):
    def program(self) -> HedyProgram:
        statements = []
        self.next_token()
        while self.current_token.type is not HedyLexerTokenType.EOF:
            print_statement = self.parse_print_statement()
            if print_statement:
                statements.append(print_statement)
                continue
        return HedyProgram(tuple(statements))

    def parse_print_statement(self) -> Optional[HedyPrintStatement]:
        print_token = self.accept(HedyLexerTokenType.PRINT)
        if not print_token:
            return None
        self.expect(HedyLexerTokenType.SPACE)
        while self.accept(HedyLexerTokenType.SPACE):
            pass
        print_argument = self.parse_expression()
        return HedyPrintStatement(print_token.marker, print_argument)

    def parse_expression(self):
        pass

    def parse_string_literal(self) -> Optional[HedyExpression]:
        identifier = self.accept(HedyLexerTokenType.IDENTIFIER)
        if identifier:
            return HedyStringLiteral(identifier.marker, identifier.data)

    def parse_string_composition(self) -> Optional[HedyExpression]:
        composition = []

