import re
from enum import Enum
from .errors import LexerError

class TokenType(Enum):
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    
    IDENTIFIER = "IDENTIFIER"
    
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    FUNCTION = "FUNCTION"
    RETURN = "RETURN"
    PRINT = "PRINT"
    INT = "INT"
    FLOAT = "FLOAT"
    STRING_TYPE = "STRING_TYPE"
    BOOL = "BOOL"
    TRUE = "TRUE"
    FALSE = "FALSE"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    ASSIGN = "ASSIGN"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    GREATER = "GREATER"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    
    EOF = "EOF"
    NEWLINE = "NEWLINE"

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}:{self.column})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        self.keywords = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'function': TokenType.FUNCTION,
            'return': TokenType.RETURN,
            'print': TokenType.PRINT,
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'string': TokenType.STRING_TYPE,
            'bool': TokenType.BOOL,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'and': TokenType.AND,
            'or': TokenType.OR,
            'not': TokenType.NOT,
        }
    
    def current_char(self):
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]
    
    def peek_char(self, offset=1):
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def advance(self):
        if self.pos < len(self.text) and self.text[self.pos] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_number(self):
        start_pos = self.pos
        start_column = self.column
        
        while self.current_char() and self.current_char().isdigit():
            self.advance()
        
        if self.current_char() == '.' and self.peek_char() and self.peek_char().isdigit():
            self.advance()  
            while self.current_char() and self.current_char().isdigit():
                self.advance()
        
        value = self.text[start_pos:self.pos]
        return Token(TokenType.NUMBER, value, self.line, start_column)
    
    def read_string(self):
        start_column = self.column
        quote_char = self.current_char()
        self.advance()  
        
        value = ""
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() == 'n':
                    value += '\n'
                elif self.current_char() == 't':
                    value += '\t'
                elif self.current_char() == 'r':
                    value += '\r'
                elif self.current_char() == '\\':
                    value += '\\'
                elif self.current_char() == quote_char:
                    value += quote_char
                else:
                    value += self.current_char()
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if not self.current_char():
            raise LexerError("String não terminada", self.line, start_column)
        
        self.advance()  
        return Token(TokenType.STRING, value, self.line, start_column)
    
    def read_identifier(self):
        start_pos = self.pos
        start_column = self.column
        
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() == '_')):
            self.advance()
        
        value = self.text[start_pos:self.pos]
        token_type = self.keywords.get(value, TokenType.IDENTIFIER)
        return Token(token_type, value, self.line, start_column)
    
    def tokenize(self):
        while self.pos < len(self.text):
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            if self.current_char() == '/' and self.peek_char() == '/':
                self.skip_comment()
                continue
            
            if self.current_char() == '\n':
                self.advance()
                continue
            
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            if self.current_char() in '"\'':
                self.tokens.append(self.read_string())
                continue
            
            if self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            if self.current_char() == '=' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.EQUAL, '==', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            if self.current_char() == '!' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            if self.current_char() == '<' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            if self.current_char() == '>' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '=': TokenType.ASSIGN,
                '<': TokenType.LESS,
                '>': TokenType.GREATER,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
            }
            
            if self.current_char() in single_char_tokens:
                token_type = single_char_tokens[self.current_char()]
                self.tokens.append(Token(token_type, self.current_char(), self.line, self.column))
                self.advance()
                continue
            
            raise LexerError(f"Caractere inválido: '{self.current_char()}'", self.line, self.column)
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

