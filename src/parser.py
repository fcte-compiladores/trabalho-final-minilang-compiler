from .lexer import TokenType
from .ast_nodes import *
from .errors import ParserError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
    def current_token(self):
        if self.current >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[self.current]
    
    def peek_token(self, offset=1):
        pos = self.current + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[pos]
    
    def advance(self):
        if self.current < len(self.tokens) - 1:
            self.current += 1
        return self.tokens[self.current - 1]
    
    def match(self, *types):
        for token_type in types:
            if self.current_token().type == token_type:
                return self.advance()
        return None
    
    def consume(self, token_type, message):
        if self.current_token().type == token_type:
            return self.advance()
        
        current = self.current_token()
        raise ParserError(message, current.line, current.column)
    
    def parse(self):
        statements = []
        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self):
        # Declarações de variáveis
        if self.current_token().type in [TokenType.INT, TokenType.FLOAT, 
                                       TokenType.STRING_TYPE, TokenType.BOOL]:
            return self.parse_declaration()
        
        # Declaração de função
        if self.current_token().type == TokenType.FUNCTION:
            return self.parse_function_declaration()
        
        # Comandos de controle
        if self.current_token().type == TokenType.IF:
            return self.parse_if_statement()
        
        if self.current_token().type == TokenType.WHILE:
            return self.parse_while_statement()
        
        if self.current_token().type == TokenType.FOR:
            return self.parse_for_statement()
        
        if self.current_token().type == TokenType.RETURN:
            return self.parse_return_statement()
        
        if self.current_token().type == TokenType.PRINT:
            return self.parse_print_statement()
        
        # Bloco
        if self.current_token().type == TokenType.LBRACE:
            return self.parse_block()
        
        # Atribuição ou expressão
        return self.parse_expression_statement()
    
    def parse_declaration(self):
        type_token = self.advance()
        
        # Verifica se é array
        if self.current_token().type == TokenType.LBRACKET:
            self.advance()  # consome '['
            size = None
            if self.current_token().type == TokenType.NUMBER:
                size = self.parse_expression() # O tamanho deve ser uma expressão
            self.consume(TokenType.RBRACKET, "Esperado ']' após tipo do array ou tamanho")
            
            name_token = self.consume(TokenType.IDENTIFIER, "Esperado nome da variável")
            
            initializer = None
            if self.current_token().type == TokenType.ASSIGN:
                self.advance()  # consome '='
                initializer = self.parse_expression()
            
            self.consume(TokenType.SEMICOLON, "Esperado ';' após declaração")
            
            return ArrayDeclaration(
                type_token.value,
                name_token.value,
                size,
                initializer,
                type_token.line,
                type_token.column
            )        
        # Declaração de variável normal
        name_token = self.consume(TokenType.IDENTIFIER, "Esperado nome da variável")
        
        initializer = None
        if self.current_token().type == TokenType.ASSIGN:
            self.advance()  # consome '='
            initializer = self.parse_expression()
        
        self.consume(TokenType.SEMICOLON, "Esperado ';' após declaração")
        
        return VarDeclaration(
            type_token.value,
            name_token.value,
            initializer,
            type_token.line,
            type_token.column
        )
    
    def parse_declaration_no_semicolon(self):
        type_token = self.advance()
        
        # Verifica se é array
        if self.current_token().type == TokenType.LBRACKET:
            self.advance()  # consome '['
            size = None
            if self.current_token().type == TokenType.NUMBER:
                size = self.parse_expression() # O tamanho deve ser uma expressão
            self.consume(TokenType.RBRACKET, "Esperado ']' após tipo do array ou tamanho")
            
            name_token = self.consume(TokenType.IDENTIFIER, "Esperado nome da variável")
            
            initializer = None
            if self.current_token().type == TokenType.ASSIGN:
                self.advance()  # consome '='
                initializer = self.parse_expression()
            
            return ArrayDeclaration(
                type_token.value,
                name_token.value,
                size,
                initializer,
                type_token.line,
                type_token.column
            )        
        # Declaração de variável normal
        name_token = self.consume(TokenType.IDENTIFIER, "Esperado nome da variável")
        
        initializer = None
        if self.current_token().type == TokenType.ASSIGN:
            self.advance()  # consome '='
            initializer = self.parse_expression()
        
        return VarDeclaration(
            type_token.value,
            name_token.value,
            initializer,
            type_token.line,
            type_token.column
        )
    
    def parse_function_declaration(self):
        func_token = self.advance()  # consome 'function'
        name_token = self.consume(TokenType.IDENTIFIER, "Esperado nome da função")

        self.consume(TokenType.LPAREN, "Esperado '(' após nome da função")

        parameters = []
        if self.current_token().type != TokenType.RPAREN:
            # Primeiro parâmetro
            param_type = None
            if self.current_token().type in [TokenType.INT, TokenType.FLOAT, 
                                           TokenType.STRING_TYPE, TokenType.BOOL]:
                param_type = self.advance().value
            
            param_name = self.consume(TokenType.IDENTIFIER, "Esperado nome do parâmetro")
            parameters.append(Parameter(param_type, param_name.value, param_name.line, param_name.column))
            
            # Parâmetros adicionais
            while self.current_token().type == TokenType.COMMA:
                self.advance()  # consome ','
                
                param_type = None
                if self.current_token().type in [TokenType.INT, TokenType.FLOAT, 
                                               TokenType.STRING_TYPE, TokenType.BOOL]:
                    param_type = self.advance().value
                
                param_name = self.consume(TokenType.IDENTIFIER, "Esperado nome do parâmetro")
                parameters.append(Parameter(param_type, param_name.value, param_name.line, param_name.column))
        
        self.consume(TokenType.RPAREN, "Esperado ')' após parâmetros")
        
        body = self.parse_block()
        
        return FunctionDeclaration(
            name_token.value,
            parameters,
            body,
            func_token.line,
            func_token.column
        )

    def parse_if_statement(self):
        if_token = self.advance()  # consome 'if'
        
        self.consume(TokenType.LPAREN, "Esperado '(' após 'if'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Esperado ')' após condição")
        
        then_stmt = self.parse_statement()
        
        else_stmt = None
        if self.current_token().type == TokenType.ELSE:
            self.advance()  # consome 'else'
            else_stmt = self.parse_statement()
        
        return IfStatement(condition, then_stmt, else_stmt, if_token.line, if_token.column)
    
    def parse_while_statement(self):
        while_token = self.advance()  # consome 'while'
        
        self.consume(TokenType.LPAREN, "Esperado '(' após 'while'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Esperado ')' após condição")
        
        body = self.parse_statement()
        
        return WhileStatement(condition, body, while_token.line, while_token.column)
    
    def parse_for_statement(self):
        for_token = self.advance()  # consome 'for'
        
        self.consume(TokenType.LPAREN, "Esperado '(' após 'for'")
        
        # Inicialização
        init = None
        if self.current_token().type != TokenType.SEMICOLON:
            if self.current_token().type in [TokenType.INT, TokenType.FLOAT, 
                                           TokenType.STRING_TYPE, TokenType.BOOL]:
                init = self.parse_declaration_no_semicolon()
            else:
                init = self.parse_expression_statement_no_semicolon()
        self.consume(TokenType.SEMICOLON, "Esperado ';' após inicialização do for")
        
        # Condição
        condition = None
        if self.current_token().type != TokenType.SEMICOLON:
            condition = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Esperado ';' após condição do for")
        
        # Atualização
        update = None
        if self.current_token().type != TokenType.RPAREN:
            update = self.parse_expression_statement_no_semicolon()
        
        self.consume(TokenType.RPAREN, "Esperado ')' após for")
        
        body = self.parse_statement()
        
        return ForStatement(init, condition, update, body, for_token.line, for_token.column)

    def parse_expression_statement_no_semicolon(self):
        expr = self.parse_expression()
        
        # Verifica se é atribuição
        if self.current_token().type == TokenType.ASSIGN:
            self.advance()  # consome '='
            value = self.parse_expression()
            return Assignment(expr, value, expr.line, expr.column)
        
        return ExpressionStatement(expr, expr.line, expr.column)

    def parse_return_statement(self):
        return_token = self.advance()  # consome 'return'
        
        value = None
        if self.current_token().type != TokenType.SEMICOLON:
            value = self.parse_expression()
        
        self.consume(TokenType.SEMICOLON, "Esperado ';' após return")
        
        return ReturnStatement(value, return_token.line, return_token.column)
    
    def parse_print_statement(self):
        print_token = self.advance()  # consome 'print'
        
        self.consume(TokenType.LPAREN, "Esperado '(' após 'print'")
        expression = self.parse_expression()
        self.consume(TokenType.RPAREN, "Esperado ')' após expressão")
        self.consume(TokenType.SEMICOLON, "Esperado ';' após print")
        
        return PrintStatement(expression, print_token.line, print_token.column)
    
    def parse_block(self):
        brace_token = self.consume(TokenType.LBRACE, "Esperado '{'")
        
        statements = []
        while (self.current_token().type != TokenType.RBRACE and 
               self.current_token().type != TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        self.consume(TokenType.RBRACE, "Esperado '}' para fechar bloco")
        
        return Block(statements, brace_token.line, brace_token.column)
    
    def parse_expression_statement(self):
        expr = self.parse_expression()
        
        # Verifica se é atribuição
        if self.current_token().type == TokenType.ASSIGN:
            self.advance()  # consome '='
            value = self.parse_expression()
            self.consume(TokenType.SEMICOLON, "Esperado ';' após atribuição")
            return Assignment(expr, value, expr.line, expr.column)
        
        self.consume(TokenType.SEMICOLON, "Esperado ';' após expressão")
        return ExpressionStatement(expr, expr.line, expr.column)
    
    def parse_expression(self):
        return self.parse_logical_or()
    
    def parse_logical_or(self):
        expr = self.parse_logical_and()
        
        while self.current_token().type == TokenType.OR:
            operator = self.advance()
            right = self.parse_logical_and()
            expr = BinaryOp(expr, operator.value, right, expr.line, expr.column)
        
        return expr
    
    def parse_logical_and(self):
        expr = self.parse_equality()
        
        while self.current_token().type == TokenType.AND:
            operator = self.advance()
            right = self.parse_equality()
            expr = BinaryOp(expr, operator.value, right, expr.line, expr.column)
        
        return expr
    
    def parse_equality(self):
        expr = self.parse_comparison()
        
        while self.current_token().type in [TokenType.EQUAL, TokenType.NOT_EQUAL]:
            operator = self.advance()
            right = self.parse_comparison()
            expr = BinaryOp(expr, operator.value, right, expr.line, expr.column)
        
        return expr
    
    def parse_comparison(self):
        expr = self.parse_term()
        
        while self.current_token().type in [TokenType.GREATER, TokenType.GREATER_EQUAL,
                                          TokenType.LESS, TokenType.LESS_EQUAL]:
            operator = self.advance()
            right = self.parse_term()
            expr = BinaryOp(expr, operator.value, right, expr.line, expr.column)
        
        return expr
    
    def parse_term(self):
        expr = self.parse_factor()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            operator = self.advance()
            right = self.parse_factor()
            expr = BinaryOp(expr, operator.value, right, expr.line, expr.column)
        
        return expr
    
    def parse_factor(self):
        expr = self.parse_unary()
        
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            operator = self.advance()
            right = self.parse_unary()
            expr = BinaryOp(expr, operator.value, right, expr.line, expr.column)
        
        return expr
    
    def parse_unary(self):
        if self.current_token().type in [TokenType.NOT, TokenType.MINUS]:
            operator = self.advance()
            operand = self.parse_unary()
            return UnaryOp(operator.value, operand, operator.line, operator.column)
        
        return self.parse_postfix()
    
    def parse_postfix(self):
        expr = self.parse_primary()
        
        while True:
            if self.current_token().type == TokenType.LBRACKET:
                # Acesso a array
                self.advance()  # consome '['
                index = self.parse_expression()
                self.consume(TokenType.RBRACKET, "Esperado ']' após índice")
                expr = ArrayAccess(expr, index, expr.line, expr.column)
            
            elif self.current_token().type == TokenType.LPAREN:
                # Chamada de função
                self.advance()  # consome '('
                arguments = []
                
                if self.current_token().type != TokenType.RPAREN:
                    arguments.append(self.parse_expression())
                    
                    while self.current_token().type == TokenType.COMMA:
                        self.advance()  # consome ','
                        arguments.append(self.parse_expression())
                
                self.consume(TokenType.RPAREN, "Esperado ')' após argumentos")
                
                if isinstance(expr, Identifier):
                    expr = FunctionCall(expr.name, arguments, expr.line, expr.column)
                else:
                    raise ParserError("Chamada de função inválida", expr.line, expr.column)
            else:
                break
        
        return expr
    
    def parse_primary(self):
        # Números
        if self.current_token().type == TokenType.NUMBER:
            token = self.advance()
            if '.' in token.value:
                return Literal(float(token.value), 'float', token.line, token.column)
            else:
                return Literal(int(token.value), 'int', token.line, token.column)
        
        # Strings
        if self.current_token().type == TokenType.STRING:
            token = self.advance()
            return Literal(token.value, 'string', token.line, token.column)
        
        # Booleanos
        if self.current_token().type in [TokenType.TRUE, TokenType.FALSE]:
            token = self.advance()
            value = token.value == 'true'
            return Literal(value, 'bool', token.line, token.column)
        
        # Identificadores
        if self.current_token().type == TokenType.IDENTIFIER:
            token = self.advance()
            return Identifier(token.value, token.line, token.column)
        
        # Expressões entre parênteses
        if self.current_token().type == TokenType.LPAREN:
            self.advance()  # consome '('
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Esperado ')' após expressão")
            return expr
        
        # Arrays literais
        if self.current_token().type == TokenType.LBRACKET:
            bracket_token = self.advance()  # consome '['
            elements = []
            
            if self.current_token().type != TokenType.RBRACKET:
                elements.append(self.parse_expression())
                
                while self.current_token().type == TokenType.COMMA:
                    self.advance()  # consome ','
                    elements.append(self.parse_expression())
            
            self.consume(TokenType.RBRACKET, "Esperado ']' após elementos do array")
            return ArrayLiteral(elements, bracket_token.line, bracket_token.column)
        
        # Erro
        current = self.current_token()
        raise ParserError(f"Token inesperado: {current.value}", current.line, current.column)

