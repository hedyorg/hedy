from dataclasses import dataclass
from typing import Optional, Callable, Tuple

from parsing import HedyBaseLexer, HedyLexerToken, HedyLexerTokenType
from parsing.tree import HedyStringLiteral, HedyPrintStatement, HedyProgram, HedyExpression, HedyStringComposition, \
    HedyAskStatement, HedyEchoStatement, HedyStatement, HedyIsStatement, HedyNumericalLiteral, HedySleepStatement


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
        if self.current_token.type != token_type:
            raise
        token = self.current_token
        self.next_token()
        return token

    def accept_any(self) -> HedyLexerToken:
        token = self.current_token
        self.next_token()
        return token

    def accept(self, token_type: HedyLexerTokenType) -> Optional[HedyLexerToken]:
        if self.current_token.type != token_type:
            return None
        token = self.current_token
        self.next_token()
        return token

    def program(self) -> HedyProgram:
        raise NotImplementedError

    def parse_statement(self) -> Optional[HedyPrintStatement]:
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
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
                continue
            raise Exception(f"Unexpected token: {self.current_token}")
        return HedyProgram(tuple(statements))

    def _statements(self) -> Tuple[Callable[[], Optional[HedyStatement]], ...]:
        return (
            self.parse_ask_statement,
            self.parse_echo_statement,
            self.parse_print_statement,
        )

    def parse_statement(self) -> Optional[HedyStatement]:
        for statement_parser in self._statements():
            statement = statement_parser()
            if statement:
                return statement
        raise

    def parse_echo_statement(self) -> Optional[HedyEchoStatement]:
        echo_token = self.accept(HedyLexerTokenType.ECHO)
        if not echo_token:
            return None
        self.expect_one_or_more_whitespace()
        echo_question = self.parse_expression()
        return HedyEchoStatement(echo_token.marker, echo_question)

    def parse_ask_statement(self) -> Optional[HedyAskStatement]:
        ask_token = self.accept(HedyLexerTokenType.ASK)
        if not ask_token:
            return None
        self.expect_one_or_more_whitespace()
        ask_question = self.parse_expression()
        return HedyAskStatement(ask_token.marker, ask_question, None)

    def expect_one_or_more_whitespace(self):
        self.expect(HedyLexerTokenType.SPACE)
        while self.accept(HedyLexerTokenType.SPACE):
            pass

    def parse_print_statement(self) -> Optional[HedyPrintStatement]:
        print_token = self.accept(HedyLexerTokenType.PRINT)
        if not print_token:
            return None
        self.expect_one_or_more_whitespace()
        print_argument = self.parse_expression()
        return HedyPrintStatement(print_token.marker, print_argument)

    def parse_expression(self):
        return self.parse_string_composition()

    def parse_literal(self) -> Optional[HedyExpression]:
        identifier = self.accept(HedyLexerTokenType.IDENTIFIER)
        if identifier:
            return HedyStringLiteral(identifier.marker, identifier.data)
        number = self.accept(HedyLexerTokenType.NUMBER)
        if number:
            return HedyNumericalLiteral(number.marker, float(number.data))
        token = self.accept_any()
        if token:
            return HedyStringLiteral(token.marker, token.data)

    def parse_string_composition(self) -> Optional[HedyExpression]:
        left = self.parse_literal()
        if left:
            while self.accept(HedyLexerTokenType.SPACE):
                pass
            if self.accept(HedyLexerTokenType.EOL) or self.accept(HedyLexerTokenType.EOF):
                return left
            right = self.parse_expression()
            if right:
                return HedyStringComposition(left.marker, left, right)
            return left


class LevelTwoHedyParser(LevelOneHedyParser):

    def _statements(self) -> Tuple[Callable[[], Optional[HedyStatement]], ...]:
        return super()._statements() + (
            self.parse_is_statement(),
            self.parse_sleep_statement(),
        )

    def parse_is_statement(self):
        identifier_token = self.accept(HedyLexerTokenType.IDENTIFIER)
        if not identifier_token:
            return None
        self.expect_one_or_more_whitespace()
        self.expect(HedyLexerTokenType.IS)
        self.expect_one_or_more_whitespace()
        value = self.parse_expression()
        return HedyIsStatement(identifier_token.marker, value, identifier_token.data)

    def parse_sleep_statement(self):
        sleep_token = self.accept(HedyLexerTokenType.SLEEP)
        if not sleep_token:
            return None
        self.expect_one_or_more_whitespace()
        amount = self.parse_expression()
        return HedySleepStatement(sleep_token.marker, amount)
