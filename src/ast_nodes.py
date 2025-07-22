from abc import ABC, abstractmethod

class ASTNode(ABC):
    """Classe base para todos os nós da AST"""
    def __init__(self, line=None, column=None):
        self.line = line
        self.column = column
    
    @abstractmethod
    def accept(self, visitor):
        pass

# Nós de Expressão
class Expression(ASTNode):
    """Classe base para expressões"""
    pass

class BinaryOp(Expression):
    def __init__(self, left, operator, right, line=None, column=None):
        super().__init__(line, column)
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)

class UnaryOp(Expression):
    def __init__(self, operator, operand, line=None, column=None):
        super().__init__(line, column)
        self.operator = operator
        self.operand = operand
    
    def accept(self, visitor):
        return visitor.visit_unary_op(self)

class Literal(Expression):
    def __init__(self, value, type_, line=None, column=None):
        super().__init__(line, column)
        self.value = value
        self.type = type_
    
    def accept(self, visitor):
        return visitor.visit_literal(self)

class Identifier(Expression):
    def __init__(self, name, line=None, column=None):
        super().__init__(line, column)
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)

class FunctionCall(Expression):
    def __init__(self, name, arguments, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.arguments = arguments
    
    def accept(self, visitor):
        return visitor.visit_function_call(self)

class ArrayAccess(Expression):
    def __init__(self, array, index, line=None, column=None):
        super().__init__(line, column)
        self.array = array
        self.index = index
    
    def accept(self, visitor):
        return visitor.visit_array_access(self)

class ArrayLiteral(Expression):
    def __init__(self, elements, line=None, column=None):
        super().__init__(line, column)
        self.elements = elements
    
    def accept(self, visitor):
        return visitor.visit_array_literal(self)

# Nós de Declaração
class Declaration(ASTNode):
    """Classe base para declarações"""
    pass

class VarDeclaration(Declaration):
    def __init__(self, type_, name, initializer=None, line=None, column=None):
        super().__init__(line, column)
        self.type = type_
        self.name = name
        self.initializer = initializer
    
    def accept(self, visitor):
        return visitor.visit_var_declaration(self)

class ArrayDeclaration(Declaration):
    def __init__(self, element_type, name, size=None, initializer=None, line=None, column=None):
        super().__init__(line, column)
        self.element_type = element_type
        self.name = name
        self.size = size
        self.initializer = initializer
    
    def accept(self, visitor):
        return visitor.visit_array_declaration(self)

class FunctionDeclaration(Declaration):
    def __init__(self, name, parameters, body, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.parameters = parameters
        self.body = body
    
    def accept(self, visitor):
        return visitor.visit_function_declaration(self)

class Parameter:
    def __init__(self, type_, name, line=None, column=None):
        self.type = type_
        self.name = name
        self.line = line
        self.column = column

# Nós de Comando
class Statement(ASTNode):
    """Classe base para comandos"""
    pass

class Assignment(Statement):
    def __init__(self, target, value, line=None, column=None):
        super().__init__(line, column)
        self.target = target
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)

class IfStatement(Statement):
    def __init__(self, condition, then_stmt, else_stmt=None, line=None, column=None):
        super().__init__(line, column)
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)

class WhileStatement(Statement):
    def __init__(self, condition, body, line=None, column=None):
        super().__init__(line, column)
        self.condition = condition
        self.body = body
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)

class ForStatement(Statement):
    def __init__(self, init, condition, update, body, line=None, column=None):
        super().__init__(line, column)
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body
    
    def accept(self, visitor):
        return visitor.visit_for_statement(self)

class ReturnStatement(Statement):
    def __init__(self, value=None, line=None, column=None):
        super().__init__(line, column)
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_return_statement(self)

class PrintStatement(Statement):
    def __init__(self, expression, line=None, column=None):
        super().__init__(line, column)
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_print_statement(self)

class ExpressionStatement(Statement):
    def __init__(self, expression, line=None, column=None):
        super().__init__(line, column)
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)

class Block(Statement):
    def __init__(self, statements, line=None, column=None):
        super().__init__(line, column)
        self.statements = statements
    
    def accept(self, visitor):
        return visitor.visit_block(self)

# Nó raiz do programa
class Program(ASTNode):
    def __init__(self, statements, line=None, column=None):
        super().__init__(line, column)
        self.statements = statements
    
    def accept(self, visitor):
        return visitor.visit_program(self)

# Interface Visitor
class Visitor(ABC):
    """Interface para implementar o padrão Visitor"""
    
    @abstractmethod
    def visit_binary_op(self, node): pass
    
    @abstractmethod
    def visit_unary_op(self, node): pass
    
    @abstractmethod
    def visit_literal(self, node): pass
    
    @abstractmethod
    def visit_identifier(self, node): pass
    
    @abstractmethod
    def visit_function_call(self, node): pass
    
    @abstractmethod
    def visit_array_access(self, node): pass
    
    @abstractmethod
    def visit_array_literal(self, node): pass
    
    @abstractmethod
    def visit_var_declaration(self, node): pass
    
    @abstractmethod
    def visit_array_declaration(self, node): pass
    
    @abstractmethod
    def visit_function_declaration(self, node): pass
    
    @abstractmethod
    def visit_assignment(self, node): pass
    
    @abstractmethod
    def visit_if_statement(self, node): pass
    
    @abstractmethod
    def visit_while_statement(self, node): pass
    
    @abstractmethod
    def visit_for_statement(self, node): pass
    
    @abstractmethod
    def visit_return_statement(self, node): pass
    
    @abstractmethod
    def visit_print_statement(self, node): pass
    
    @abstractmethod
    def visit_expression_statement(self, node): pass
    
    @abstractmethod
    def visit_block(self, node): pass
    
    @abstractmethod
    def visit_program(self, node): pass

