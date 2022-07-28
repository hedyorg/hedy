import unittest

from parameterized import parameterized

from parsing.lexer import HedyBaseLexer, HedyLexerTokenType, HedyLexerToken, HedyMarker


def create_lexer(program: str):
    return HedyBaseLexer.create_for_program(program)


class TestBaseLexer(unittest.TestCase):
    @parameterized.expand([
        ('1',),
        ('1.2',),
        ('١',),
        ('١.١',),
    ])
    def test_base_lexer_parse_number(self, number_string: str):
        lexer = create_lexer(number_string)
        self.assertEqual(HedyLexerToken(
            type=HedyLexerTokenType.NUMBER,
            marker=HedyMarker(index=0, line_number=0, column_index=0),
            data=number_string
        ), lexer.token())
        self.assertEqual(HedyLexerTokenType.EOF, lexer.token().type)

    def test_base_lexer_parse_keyword(self):
        lexer = create_lexer("print")
        lexer.register_keyword("print", HedyLexerTokenType.PRINT)
        self.assertEqual(HedyLexerToken(
            type=HedyLexerTokenType.PRINT,
            marker=HedyMarker(index=0, line_number=0, column_index=0),
            data="print"
        ), lexer.token())
        self.assertEqual(HedyLexerTokenType.EOF, lexer.token().type)

    def test_base_lexer_identifier(self):
        lexer = create_lexer("hedy")
        self.assertEqual(HedyLexerToken(
            type=HedyLexerTokenType.IDENTIFIER,
            marker=HedyMarker(index=0, line_number=0, column_index=0),
            data="hedy"
        ), lexer.token())
        self.assertEqual(HedyLexerTokenType.EOF, lexer.token().type)

    def test_base_lexer_advances_new_line(self):
        lexer = create_lexer("print\nprint")
        lexer.register_keyword("print", HedyLexerTokenType.PRINT)
        self.assertEqual(HedyLexerToken(
            type=HedyLexerTokenType.PRINT,
            marker=HedyMarker(index=0, line_number=0, column_index=0),
            data="print"
        ), lexer.token())
        self.assertEqual(HedyLexerTokenType.EOL, lexer.token().type)
        self.assertEqual(HedyLexerToken(
            type=HedyLexerTokenType.PRINT,
            marker=HedyMarker(index=len("print") + 1, line_number=1, column_index=0),
            data="print"
        ), lexer.token())
        self.assertEqual(HedyLexerTokenType.EOF, lexer.token().type)


if __name__ == '__main__':
    unittest.main()
