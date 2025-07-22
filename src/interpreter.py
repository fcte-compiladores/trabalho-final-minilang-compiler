from .ast_nodes import Visitor
from .errors import RuntimeError

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise RuntimeError(f"Variável '{name}' não definida", 0, 0)

    def set(self, name, value):
        if name in self.values:
            self.values[name] = value
            return
        if self.parent:
            self.parent.set(name, value)
            return
        raise RuntimeError(f"Variável '{name}' não definida", 0, 0)

class Function:
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        
        for i, param in enumerate(self.declaration.parameters):
            if i < len(arguments):
                environment.define(param.name, arguments[i])
            else:
                environment.define(param.name, None)        
        try:
            interpreter.execute_block(self.declaration.body.statements, environment)
        except ReturnException as ret:
            return ret.value
        
        return None

class Interpreter(Visitor):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals

    def interpret(self, ast):
        try:
            ast.accept(self)
        except RuntimeError as e:
            print(f"Erro em tempo de execução: {e}")
            raise

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                statement.accept(self)
        finally:
            self.environment = previous

    def visit_program(self, node):
        for statement in node.statements:
            statement.accept(self)

    def visit_var_declaration(self, node):
        value = None
        if node.initializer:
            value = node.initializer.accept(self)
        
        if node.type == 'int' and isinstance(value, float):
            value = int(value)
        elif node.type == 'float' and isinstance(value, int):
            value = float(value)
        elif node.type == 'string' and value is not None:
            value = str(value)
        elif node.type == 'bool' and value is not None:
            value = bool(value)
        
        self.environment.define(node.name, value)

    def visit_array_declaration(self, node):
        value = []
        if node.size:
            size = node.size.accept(self)
            if not isinstance(size, int) or size < 0:
                raise RuntimeError("Tamanho do array deve ser um inteiro não negativo", node.line, node.column)
            
            default_value = None
            if node.element_type == 'int':
                default_value = 0
            elif node.element_type == 'float':
                default_value = 0.0
            elif node.element_type == 'bool':
                default_value = False
            elif node.element_type == 'string':
                default_value = ""
            
            value = [default_value] * size
        elif node.initializer:
            value = node.initializer.accept(self)
        
        self.environment.define(node.name, value)
    def visit_function_declaration(self, node):
        function = Function(node, self.environment)
        self.environment.define(node.name, function)

    def visit_assignment(self, node):
        value = node.value.accept(self)
        
        if hasattr(node.target, 'name'):
            self.environment.set(node.target.name, value)
        elif hasattr(node.target, 'array'):
            array = node.target.array.accept(self)
            index = node.target.index.accept(self)
            
            if not isinstance(array, list):
                raise RuntimeError("Tentativa de indexar não-array", node.line, node.column)
            
            if not isinstance(index, int):
                raise RuntimeError("Índice deve ser inteiro", node.line, node.column)
            
            if index < 0 or index >= len(array):
                raise RuntimeError("Índice fora dos limites", node.line, node.column)
            
            array[index] = value

    def visit_if_statement(self, node):
        condition = node.condition.accept(self)
        
        if self.is_truthy(condition):
            node.then_stmt.accept(self)
        elif node.else_stmt:
            node.else_stmt.accept(self)

    def visit_while_statement(self, node):
        while self.is_truthy(node.condition.accept(self)):
            node.body.accept(self)

    def visit_for_statement(self, node):
        environment = Environment(self.environment)
        
        previous = self.environment
        try:
            self.environment = environment
            
            if node.init:
                node.init.accept(self)
            
            while True:
                if node.condition:
                    if not self.is_truthy(node.condition.accept(self)):
                        break
                
                node.body.accept(self)
                
                if node.update:
                    node.update.accept(self)
        finally:
            self.environment = previous

    def visit_return_statement(self, node):
        value = None
        if node.value:
            value = node.value.accept(self)
        
        raise ReturnException(value)

    def visit_print_statement(self, node):
        value = node.expression.accept(self)
        print(self.stringify(value))

    def visit_expression_statement(self, node):
        node.expression.accept(self)

    def visit_block(self, node):
        self.execute_block(node.statements, Environment(self.environment))

    def visit_binary_op(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        
        if node.operator == '+':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            if right == 0:
                raise RuntimeError("Divisão por zero", node.line, node.column)
            return left / right
        elif node.operator == '%':
            return left % right
        elif node.operator == '<':
            return left < right
        elif node.operator == '>':
            return left > right
        elif node.operator == '<=':
            return left <= right
        elif node.operator == '>=':
            return left >= right
        elif node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right
        elif node.operator == 'and':
            return self.is_truthy(left) and self.is_truthy(right)
        elif node.operator == 'or':
            return self.is_truthy(left) or self.is_truthy(right)
        
        raise RuntimeError(f"Operador binário desconhecido: {node.operator}", node.line, node.column)

    def visit_unary_op(self, node):
        operand = node.operand.accept(self)
        
        if node.operator == '-':
            return -operand
        elif node.operator == 'not':
            return not self.is_truthy(operand)
        
        raise RuntimeError(f"Operador unário desconhecido: {node.operator}", node.line, node.column)

    def visit_literal(self, node):
        return node.value

    def visit_identifier(self, node):
        return self.environment.get(node.name)

    def visit_function_call(self, node):
        callee = self.environment.get(node.name)
        
        if not isinstance(callee, Function):
            raise RuntimeError(f"'{node.name}' não é uma função", node.line, node.column)
        
        arguments = []
        for arg in node.arguments:
            arguments.append(arg.accept(self))
        
        return callee.call(self, arguments)

    def visit_array_access(self, node):
        array = node.array.accept(self)
        index = node.index.accept(self)
        
        if not isinstance(array, list):
            raise RuntimeError("Tentativa de indexar não-array", node.line, node.column)
        
        if not isinstance(index, int):
            raise RuntimeError("Índice deve ser inteiro", node.line, node.column)
        
        if index < 0 or index >= len(array):
            raise RuntimeError("Índice fora dos limites", node.line, node.column)
        
        return array[index]

    def visit_array_literal(self, node):
        elements = []
        for element in node.elements:
            elements.append(element.accept(self))
        return elements

    def is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True

    def stringify(self, value):
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                return text[:-2]
            return text
        return str(value)

