import unittest

from parsing import LevelOneHedyParser, HedyParserConfig, HedyBaseLexer, HedyProgram, HedyPrintStatement, HedyMarker, \
    HedyStringComposition, HedyStringLiteral, HedyLexerTokenType, HedyAskStatement


def create_parser(program: str):
    lexer = HedyBaseLexer.create_for_program(program)
    lexer.register_keyword(" ", HedyLexerTokenType.SPACE)
    lexer.register_keyword("print", HedyLexerTokenType.PRINT)
    lexer.register_keyword("ask", HedyLexerTokenType.PRINT)
    lexer.register_keyword("?", HedyLexerTokenType.QUESTION_MARK)
    return LevelOneHedyParser(lexer, HedyParserConfig())


class TestLevelOneParser(unittest.TestCase):
    def test_ask_statement(self):
        parser = create_parser("ask hoe heet je?")
        self.assertEqual(HedyProgram(statements=(
            HedyAskStatement(
                marker=HedyMarker(0, 0, 0),
                variable_name=None,
                question_expression=HedyStringComposition(
                    marker=HedyMarker(index=len("ask") + 1, column_index=len("ask") + 1, line_number=0),
                    left=HedyStringLiteral(
                        marker=HedyMarker(index=len("print") + 1, column_index=len("print") + 1, line_number=0),
                        string_literal="hallo"
                    ),
                    right=HedyStringLiteral(
                        marker=HedyMarker(index=len("print hallo") + 1, column_index=len("print hallo") + 1,
                                          line_number=0),
                        string_literal="hedy"
                    )
                )
            ),
        )), parser.program())

    def test_print_statement(self):
        parser = create_parser("print hallo hedy")
        self.assertEqual(HedyProgram(statements=(
            HedyPrintStatement(
                marker=HedyMarker(0, 0, 0),
                print_argument=HedyStringComposition(
                    marker=HedyMarker(index=len("print") + 1, column_index=len("print") + 1, line_number=0),
                    left=HedyStringLiteral(
                        marker=HedyMarker(index=len("print") + 1, column_index=len("print") + 1, line_number=0),
                        string_literal="hallo"
                    ),
                    right=HedyStringLiteral(
                        marker=HedyMarker(index=len("print hallo") + 1, column_index=len("print hallo") + 1, line_number=0),
                        string_literal="hedy"
                    )
                )
            ),
        )), parser.program())
