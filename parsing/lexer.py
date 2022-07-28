from contextlib import contextmanager
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Callable, Optional


class HedyLexerTokenType(str, Enum):
    ECHO = 'ECHO'
    ASK = 'ASK'
    IS = 'IS'
    SLEEP = 'SLEEP'
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    SPACE = 'SPACE'
    PRINT = 'PRINT'
    EOL = 'EOL'
    EOF = 'EOF'
    RANDOM = 'RANDOM'
    COMMA = 'COMMA'
    ADD = 'ADD'
    REMOVE = 'REMOVE'
    TO = 'TO'


@dataclass
class HedyLexerAlphabet:
    def is_alpha(self, character: str):
        return character.isalpha()

    def is_alphanumeric(self, character: str):
        return character.isalnum()

    def is_numeric(self, character: str):
        return character.isnumeric()


@dataclass
class HedyLexerConfig:
    alphabet: HedyLexerAlphabet


@dataclass
class HedyMarker:
    index: int
    line_number: int
    column_index: int


@dataclass
class HedyLexerToken:
    type: HedyLexerTokenType
    marker: HedyMarker
    data: Optional[str]


@dataclass
class HedyLexerState:
    index: int = 0
    line_number: int = 0
    column_index: int = 0

    def next(self):
        self.index = self.index + 1

    def advance(self):
        self.next()
        self.column_index = self.column_index + 1

    def newline(self):
        self.column_index = 0
        self.line_number = self.line_number + 1

    def copy(self):
        return HedyLexerState(**asdict(self))


class HedyBaseLexer:
    def __init__(self, program: str, config: HedyLexerConfig):
        self.config = config
        self.input = program
        self.keywords = {}
        self.state = HedyLexerState()
        self._state = self.state

    def _store(self):
        self._state = self.state

    def _recover(self):
        self.state = self._state

    def _eol(self) -> bool:
        return self.accept('\n') or self.accept('\r\n')

    def _eof(self) -> bool:
        return len(self.input) <= self.state.index

    def current(self) -> Optional[str]:
        if self._eof():
            return None
        return self.input[self.state.index]

    def next(self) -> str:
        self.state.advance()
        return self.current()

    def peek(self) -> str:
        return self.input[self.state.index + 1]

    def expect(self, expected: str) -> bool:
        if not self.accept(expected):
            raise
        return True

    def accept_predicate(self, predicate: Callable[[str], bool]):
        with self.peeking():
            if not predicate(self.current()):
                return False
            while not self._eof() and predicate(self.current()):
                self.state.advance()
            self._store()
            return True

    def accept(self, expected: str) -> bool:
        if expected[0] != self.current():
            return False
        with self.peeking():
            for char in expected:
                if char != self.current():
                    return False
                self.state.advance()
            self._store()
            return True

    def maybe_number(self) -> Optional[HedyLexerToken]:
        if not self.config.alphabet.is_numeric(self.current()):
            return None
        with self.peeking():
            number = ""
            while not self._eof() and self.config.alphabet.is_numeric(self.current()):
                number = number + self.current()
                self.state.advance()
            if self.current() == '.':
                number = number + self.current()
                self.state.advance()
            while not self._eof() and self.config.alphabet.is_numeric(self.current()):
                number = number + self.current()
                self.state.advance()
            return self._create_token(number, HedyLexerTokenType.NUMBER)

    def maybe_identifier(self) -> Optional[HedyLexerToken]:
        if not self.config.alphabet.is_alpha(self.current()):
            return None
        with self.peeking():
            identifier = ""
            while not self._eof() and self.config.alphabet.is_alphanumeric(self.current()):
                identifier = identifier + self.current()
                self.state.advance()
            self._store()
            return self._create_token(identifier, HedyLexerTokenType.IDENTIFIER)

    def _create_token(self, data: Optional[str], token_type: HedyLexerTokenType):
        offset = len(data) if data is not None else 0
        marker = HedyMarker(self.state.index - offset, self.state.line_number, self.state.column_index - offset)
        return HedyLexerToken(
            token_type,
            marker,
            data
        )

    def token(self) -> HedyLexerToken:
        if self._eol():
            token = self._create_token(None, HedyLexerTokenType.EOL)
            self.state.newline()
            return token
        if self._eof():
            return self._create_token(None, HedyLexerTokenType.EOF)
        for (keyword, token_type) in self.keywords.items():
            if self.accept(keyword):
                return self._create_token(keyword, token_type)

        for lexeme in (self.maybe_identifier, self.maybe_number):
            token = lexeme()
            if token is not None:
                return token
        raise

    @contextmanager
    def peeking(self):
        self._store()
        try:
            yield self.state
        finally:
            self._recover()

    def register_keyword(self, keyword: str, token_type: HedyLexerTokenType):
        self.keywords[keyword] = token_type

    @classmethod
    def create_for_program(cls, program: str, alphabet: Optional[HedyLexerAlphabet] = None):
        if alphabet is None:
            alphabet = HedyLexerAlphabet()
        return cls(program, HedyLexerConfig(alphabet))


class HedyLevelOneLexer(HedyBaseLexer):
    def __init__(self, program: str, config: HedyLexerConfig):
        super().__init__(program, config)
        self.register_keyword(' ', token_type=HedyLexerTokenType.SPACE)
        self.register_keyword('print', token_type=HedyLexerTokenType.PRINT)
