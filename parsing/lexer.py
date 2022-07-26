from contextlib import contextmanager
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Callable, Optional


class HedyLexerTokenType(str, Enum):
    IDENTIFIER = 'IDENTIFIER'
    SPACE = 'SPACE'
    PRINT = 'PRINT'
    EOL = 'EOL'
    EOF = 'EOF'


@dataclass
class HedyLexerConfig:
    pass


@dataclass
class HedyLexerToken:
    type: HedyLexerTokenType
    index: int
    line_number: int
    column_index: int
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
        self.next()
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
        return len(self.input) >= self.state.index

    def current(self) -> Optional[str]:
        if self._eol():
            return None
        return self.input[self.state.index]

    def next(self) -> str:
        self.state.next()
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
            while predicate(self.current()):
                self.state.next()
            self._store()
            return True

    def accept(self, expected: str) -> bool:
        if expected[0] != self.current():
            return False
        with self.peeking():
            for char in expected:
                if char != self.current():
                    return False
                self.state.next()
            self._store()
            return True


    def maybe_identifier(self) -> Optional[HedyLexerToken]:


    def _create_token(self, data: Optional[str], token_type: HedyLexerTokenType):
        return HedyLexerToken(token_type, self.state.index, self.state.line_number, self.state.column_index, data)

    def token(self) -> HedyLexerToken:
        if self._eol():
            return self._create_token(None, HedyLexerTokenType.EOF)
        for (keyword, token_type) in self.keywords.items():
            if self.accept(keyword):
                return self._create_token(keyword, token_type)

        maybe_identifier = self.maybe_identifier()
        if maybe_identifier is not None:
            return maybe_identifier

        raise

    @contextmanager
    def peeking(self):
        self._store()
        try:
            yield self
        finally:
            self._recover()

    def register_keyword(self, keyword: str, token_type: HedyLexerTokenType):
        self.keywords[keyword] = token_type


class HedyLevelOneLexer(HedyBaseLexer):
    def __init__(self, program: str, config: HedyLexerConfig):
        super().__init__(program, config)
        self.register_keyword(' ', token_type=HedyLexerTokenType.SPACE)
        self.register_keyword('print', token_type=HedyLexerTokenType.PRINT)
