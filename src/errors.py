class LexerError(Exception):
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Erro Léxico na linha {line}, coluna {column}: {message}")

class ParserError(Exception):
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Erro Sintático na linha {line}, coluna {column}: {message}")

class SemanticError(Exception):
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Erro Semântico na linha {line}, coluna {column}: {message}")

class RuntimeError(Exception):
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Erro em Tempo de Execução na linha {line}, coluna {column}: {message}")


