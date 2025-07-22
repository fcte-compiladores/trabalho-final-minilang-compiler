import pytest
from src.lexer import Lexer, TokenType, Token
from src.errors import LexerError

def test_empty_input():
    lexer = Lexer("")
    tokens = lexer.tokenize()
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF

def test_whitespace_and_comments():
    lexer = Lexer("   // comentario\n  \t  ")
    tokens = lexer.tokenize()
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF

def test_numbers():
    lexer = Lexer("123 45.67 0.0 0")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.NUMBER and tokens[0].value == "123"
    assert tokens[1].type == TokenType.NUMBER and tokens[1].value == "45.67"
    assert tokens[2].type == TokenType.NUMBER and tokens[2].value == "0.0"
    assert tokens[3].type == TokenType.NUMBER and tokens[3].value == "0"
    assert tokens[4].type == TokenType.EOF

def test_strings():
    lexer = Lexer("\"hello world\" \'single quotes\' \"escaped\\nstring\"")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING and tokens[0].value == "hello world"
    assert tokens[1].type == TokenType.STRING and tokens[1].value == "single quotes"
    assert tokens[2].type == TokenType.STRING and tokens[2].value == "escaped\nstring"
    assert tokens[3].type == TokenType.EOF

def test_identifiers_and_keywords():
    lexer = Lexer("if else while function myVar _anotherVar int float string bool true false and or not")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.IF
    assert tokens[1].type == TokenType.ELSE
    assert tokens[2].type == TokenType.WHILE
    assert tokens[3].type == TokenType.FUNCTION
    assert tokens[4].type == TokenType.IDENTIFIER and tokens[4].value == "myVar"
    assert tokens[5].type == TokenType.IDENTIFIER and tokens[5].value == "_anotherVar"
    assert tokens[6].type == TokenType.INT
    assert tokens[7].type == TokenType.FLOAT
    assert tokens[8].type == TokenType.STRING_TYPE
    assert tokens[9].type == TokenType.BOOL
    assert tokens[10].type == TokenType.TRUE
    assert tokens[11].type == TokenType.FALSE
    assert tokens[12].type == TokenType.AND
    assert tokens[13].type == TokenType.OR
    assert tokens[14].type == TokenType.NOT
    assert tokens[15].type == TokenType.EOF

def test_operators():
    lexer = Lexer("+ - * / % = == != < > <= >= ( ) { } [ ] ; ,")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.PLUS
    assert tokens[1].type == TokenType.MINUS
    assert tokens[2].type == TokenType.MULTIPLY
    assert tokens[3].type == TokenType.DIVIDE
    assert tokens[4].type == TokenType.MODULO
    assert tokens[5].type == TokenType.ASSIGN
    assert tokens[6].type == TokenType.EQUAL
    assert tokens[7].type == TokenType.NOT_EQUAL
    assert tokens[8].type == TokenType.LESS
    assert tokens[9].type == TokenType.GREATER
    assert tokens[10].type == TokenType.LESS_EQUAL
    assert tokens[11].type == TokenType.GREATER_EQUAL
    assert tokens[12].type == TokenType.LPAREN
    assert tokens[13].type == TokenType.RPAREN
    assert tokens[14].type == TokenType.LBRACE
    assert tokens[15].type == TokenType.RBRACE
    assert tokens[16].type == TokenType.LBRACKET
    assert tokens[17].type == TokenType.RBRACKET
    assert tokens[18].type == TokenType.SEMICOLON
    assert tokens[19].type == TokenType.COMMA
    assert tokens[20].type == TokenType.EOF

def test_complex_expression():
    code = "int x = 10 + (5 * 2); // calcula\nprint(\"Resultado: \" + x);"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    expected_types = [
        TokenType.INT, TokenType.IDENTIFIER, TokenType.ASSIGN, TokenType.NUMBER, 
        TokenType.PLUS, TokenType.LPAREN, TokenType.NUMBER, TokenType.MULTIPLY,
        TokenType.NUMBER, TokenType.RPAREN, TokenType.SEMICOLON, 
        TokenType.PRINT, TokenType.LPAREN, TokenType.STRING, TokenType.PLUS,
        TokenType.IDENTIFIER, TokenType.RPAREN, TokenType.SEMICOLON, TokenType.EOF
    ]
    
    assert len(tokens) == len(expected_types)
    for i, token in enumerate(tokens):
        assert token.type == expected_types[i]

def test_lexer_error():
    lexer = Lexer("$")
    with pytest.raises(LexerError):
        lexer.tokenize()

def test_unterminated_string_error():
    lexer = Lexer("\"abc")
    with pytest.raises(LexerError):
        lexer.tokenize()


