from dataclasses import dataclass
from typing import Tuple, Optional

from parsing import HedyLexerToken, HedyMarker


class Visitor:
    def visit_print_statement(self, print_statement: 'HedyPrintStatement'):
        pass

    def visit_string_literal(self, string_literal: 'HedyStringLiteral'):
        pass

    def visit_string_composition(self, string_composition: 'HedyStringComposition'):
        pass

    def visit_ask_statement(self, ask_statement: 'HedyAskStatement'):
        pass

    def visit_echo_statement(self, echo_statement: 'HedyEchoStatement'):
        pass

    def visit_is_statement(self, is_statement: 'HedyIsStatement'):
        pass

    def visit_sleep_statement(self, sleep_statement: 'HedySleepStatement'):
        pass

    def visit_numerical_literal(self, numerical_literal: 'HedyNumericalLiteral'):
        pass

    def visit_program(self, program: 'HedyProgram'):
        pass

    def visit_variable_access(self, variable_access: 'HedyVariableAccess'):
        pass

    def visit_list_literal(self, list_literal: 'HedyListLiteral'):
        pass


@dataclass
class HedyNode:
    marker: HedyMarker

    def visit(self, visitor: Visitor):
        raise NotImplementedError


@dataclass
class HedyProgram(HedyNode):
    statements: Tuple['HedyNode', ...]

    def visit(self, visitor: Visitor):
        visitor.visit_program(self)


@dataclass
class HedyExpression(HedyNode):
    def visit(self, visitor: Visitor):
        raise NotImplementedError


@dataclass
class HedyStatement(HedyNode):
    def visit(self, visitor: Visitor):
        raise NotImplementedError


@dataclass
class HedyStringComposition(HedyExpression):
    left: HedyExpression
    right: HedyExpression

    def visit(self, visitor: Visitor):
        return visitor.visit_string_composition(self)


@dataclass
class HedyStringLiteral(HedyExpression):
    string_literal: str

    def visit(self, visitor: Visitor):
        return visitor.visit_string_literal(self)


@dataclass
class HedyVariableAccess(HedyExpression):
    variable_name: str

    def visit(self, visitor: Visitor):
        visitor.visit_variable_access(self)


@dataclass
class HedyListLiteral(HedyExpression):
    values: Tuple[HedyExpression, ...]

    def visit(self, visitor: Visitor):
        visitor.visit_list_literal(self)


@dataclass
class HedyNumericalLiteral(HedyExpression):
    numeric_value: float

    def visit(self, visitor: Visitor):
        visitor.visit_numerical_literal(self)


@dataclass
class HedyPrintStatement(HedyStatement):
    print_argument: HedyExpression

    def visit(self, visitor: Visitor):
        return visitor.visit_print_statement(self)


@dataclass
class HedyAskStatement(HedyStatement):
    variable_name: Optional[str]
    question_expression: HedyExpression

    def visit(self, visitor: Visitor):
        return visitor.visit_ask_statement(self)


@dataclass
class HedyEchoStatement(HedyStatement):
    echo_expression: HedyExpression

    def visit(self, visitor: Visitor):
        return visitor.visit_echo_statement(self)


@dataclass
class HedyIsStatement(HedyStatement):
    variable_name: str
    value: HedyExpression

    def visit(self, visitor: Visitor):
        return visitor.visit_is_statement(self)


@dataclass
class HedySleepStatement(HedyStatement):
    value: HedyExpression

    def visit(self, visitor: Visitor):
        return visitor.visit_sleep_statement(self)
