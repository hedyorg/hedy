from dataclasses import dataclass
from typing import Tuple

from parsing import HedyLexerToken, HedyMarker


class Visitor:
    def visit_print_statement(self, print_statement: 'HedyPrintStatement'):
        pass

    def visit_string_literal(self, string_literal: 'HedyStringLiteral'):
        pass

    def visit_string_composition(self, string_composition: 'HedyStringComposition'):
        pass


@dataclass
class HedyProgram:
    statements: Tuple['HedyNode', ...]


@dataclass
class HedyNode:
    marker: HedyMarker

    def visit(self, visitor: Visitor):
        raise NotImplementedError


@dataclass
class HedyExpression(HedyNode):
    def visit(self, visitor: Visitor):
        raise NotImplementedError


@dataclass
class HedyStringComposition(HedyExpression):
    expressions: Tuple[HedyExpression, ...]

    def visit(self, visitor: Visitor):
        return visitor.visit_string_composition(expressions)


@dataclass
class HedyStringLiteral(HedyExpression):
    string_literal: str

    def visit(self, visitor: Visitor):
        return visitor.visit_string_literal(self)


@dataclass
class HedyPrintStatement(HedyNode):
    print_argument: HedyExpression

    def visit(self, visitor: Visitor):
        return visitor.visit_print_statement(self)
