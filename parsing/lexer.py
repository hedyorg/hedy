from contextlib import contextmanager
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Callable


class HedyLexerTokenType(str, Enum):
    IDENTIFIER = 'IDENTIFIER'


@dataclass
class HedyLexerConfig:
    pass


@dataclass
class HedyLexerToken:
    type: HedyLexerTokenType
    index: int
    line_number: int
    column_index: int
    data: str


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
        self.state = HedyLexerState()

    def current(self) -> str:
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
            accepted_state = self.state
        self.state = accepted_state
        return True

    def accept(self, expected: str) -> bool:
        with self.peeking():
            for char in expected:
                if char is not self.current():
                    return False
                self.state.next()
            accepted_state = self.state
        self.state = accepted_state
        return True

    def next(self) -> HedyLexerToken:
        pass

    @contextmanager
    def peeking(self):
        marked_state = self.state.copy()
        try:
            yield self
        finally:
            self.state = marked_state
