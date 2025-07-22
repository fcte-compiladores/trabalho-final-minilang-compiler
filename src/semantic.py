from .ast_nodes import Visitor
from .symbol_table import Symbol, SymbolTable
from .errors import SemanticError

class SemanticAnalyzer(Visitor):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_function = None
        self.errors = []

    def analyze(self, ast):
        try:
            ast.accept(self)
        except SemanticError as e:
            self.errors.append(e)
        
        if self.errors:
            raise self.errors[0]

    def enter_scope(self):
        self.symbol_table = SymbolTable(self.symbol_table)

    def exit_scope(self):
        self.symbol_table = self.symbol_table.parent

    def declare_symbol(self, name, type_, line, column):
        symbol = Symbol(name, type_)
        try:
            self.symbol_table.define(symbol)
        except Exception:
            raise SemanticError(f"Variável '{name}' já declarada neste escopo", line, column)
        return symbol

    def resolve_symbol(self, name, line, column):
        symbol = self.symbol_table.resolve(name)
        if not symbol:
            raise SemanticError(f"Variável '{name}' não declarada", line, column)
        return symbol

    def check_type_compatibility(self, left_type, right_type, operation, line, column):
        if left_type == 'any' or right_type == 'any':
            return left_type if left_type != 'any' else right_type

        if left_type == right_type:
            return left_type

        if left_type == 'float' and right_type == 'int':
            return 'float'
        if left_type == 'int' and right_type == 'float':
            return 'float'

        if operation == '+' and (left_type == 'string' or right_type == 'string'):
            return 'string'

        raise SemanticError(f"Tipos incompatíveis: {left_type} e {right_type} para operação {operation}", line, column)

    def visit_program(self, node):
        for stmt in node.statements:
            stmt.accept(self)

    def visit_var_declaration(self, node):
        symbol = self.declare_symbol(node.name, node.type, node.line, node.column)
        
        if node.initializer:
            init_type = node.initializer.accept(self)
            self.check_type_compatibility(node.type, init_type, '=', node.line, node.column)

    def visit_array_declaration(self, node):
        array_type = f"{node.element_type}[]"
        symbol = self.declare_symbol(node.name, array_type, node.line, node.column)
        
        if node.size:
            size_type = node.size.accept(self)
            if size_type != 'int':
                raise SemanticError("Tamanho do array deve ser um inteiro", node.line, node.column)

        if node.initializer:
            init_type = node.initializer.accept(self)
            if not init_type.startswith(node.element_type):
                raise SemanticError(f"Tipo do inicializador incompatível com array de {node.element_type}", 
                                      node.line, node.column)

    def visit_function_declaration(self, node):
        param_types = [param.type if param.type is not None else 'any' for param in node.parameters]
        func_type = f"function({','.join(param_types)})"
        self.declare_symbol(node.name, func_type, node.line, node.column)
        
        old_function = self.current_function
        self.current_function = node.name
        self.enter_scope()
        
        for param in node.parameters:
            self.declare_symbol(param.name, param.type if param.type is not None else 'any', param.line, param.column)
        
        node.body.accept(self)
        
        self.exit_scope()
        self.current_function = old_function

    def visit_assignment(self, node):
        if hasattr(node.target, 'name'):
            symbol = self.resolve_symbol(node.target.name, node.target.line, node.target.column)
            target_type = symbol.type
        elif hasattr(node.target, 'array'):
            array_type = node.target.accept(self)
            target_type = array_type
        else:
            raise SemanticError("Target de atribuição inválido", node.line, node.column)
        
        value_type = node.value.accept(self)
        self.check_type_compatibility(target_type, value_type, '=', node.line, node.column)

    def visit_if_statement(self, node):
        condition_type = node.condition.accept(self)
        if condition_type != 'bool' and condition_type != 'any':
            raise SemanticError("Condição do if deve ser booleana", node.condition.line, node.condition.column)
        
        node.then_stmt.accept(self)
        if node.else_stmt:
            node.else_stmt.accept(self)

    def visit_while_statement(self, node):
        condition_type = node.condition.accept(self)
        if condition_type != 'bool' and condition_type != 'any':
            raise SemanticError("Condição do while deve ser booleana", node.condition.line, node.condition.column)
        
        node.body.accept(self)

    def visit_for_statement(self, node):
        self.enter_scope()
        
        if node.init:
            node.init.accept(self)
        
        if node.condition:
            condition_type = node.condition.accept(self)
            if condition_type != 'bool' and condition_type != 'any':
                raise SemanticError("Condição do for deve ser booleana", node.condition.line, node.condition.column)
        
        if node.update:
            node.update.accept(self)
        
        node.body.accept(self)
        
        self.exit_scope()

    def visit_return_statement(self, node):
        if not self.current_function:
            raise SemanticError("Return fora de função", node.line, node.column)
        
        if node.value:
            node.value.accept(self)

    def visit_print_statement(self, node):
        node.expression.accept(self)

    def visit_expression_statement(self, node):
        node.expression.accept(self)

    def visit_block(self, node):
        self.enter_scope()
        for stmt in node.statements:
            stmt.accept(self)
        self.exit_scope()

    def visit_binary_op(self, node):
        left_type = node.left.accept(self)
        right_type = node.right.accept(self)
        
        if left_type is None: left_type = 'any'
        if right_type is None: right_type = 'any'
        
        if node.operator in ['+', '-', '*', '/', '%']:
            if node.operator == '+' and (left_type == 'string' or right_type == 'string'):
                return 'string'
            elif left_type in ['int', 'float', 'any'] and right_type in ['int', 'float', 'any']:
                if 'any' in [left_type, right_type]:
                    return 'any'
                return 'float' if 'float' in [left_type, right_type] else 'int'
            else:
                raise SemanticError(f"Operador {node.operator} não suportado para tipos {left_type} e {right_type}", node.line, node.column)
        
        elif node.operator in ['<', '>', '<=', '>=']:
            if left_type in ['int', 'float', 'any'] and right_type in ['int', 'float', 'any']:
                return 'bool'
            else:
                raise SemanticError(f"Operador {node.operator} não suportado para tipos {left_type} e {right_type}", node.line, node.column)
        
        elif node.operator in ['==', '!=']:
            return 'bool'
        
        elif node.operator in ['and', 'or']:
            if left_type in ['bool', 'any'] and right_type in ['bool', 'any']:
                return 'bool'
            else:
                raise SemanticError(f"Operador {node.operator} requer operandos booleanos", node.line, node.column)
        
        raise SemanticError(f"Operador desconhecido: {node.operator}", node.line, node.column)

    def visit_unary_op(self, node):
        operand_type = node.operand.accept(self)
        
        if node.operator == '-':
            if operand_type in ['int', 'float', 'any']:
                return operand_type
            else:
                raise SemanticError(f"Operador unário - não suportado para tipo {operand_type}", node.line, node.column)
        
        elif node.operator == 'not':
            if operand_type in ['bool', 'any']:
                return 'bool'
            else:
                raise SemanticError(f"Operador not requer operando booleano", node.line, node.column)
        
        raise SemanticError(f"Operador unário desconhecido: {node.operator}", node.line, node.column)

    def visit_literal(self, node):
        return node.type

    def visit_identifier(self, node):
        symbol = self.resolve_symbol(node.name, node.line, node.column)
        return symbol.type

    def visit_function_call(self, node):
        symbol = self.resolve_symbol(node.name, node.line, node.column)
        
        if not symbol.type.startswith('function'):
            raise SemanticError(f"'{node.name}' não é uma função", node.line, node.column)
        
        for arg in node.arguments:
            arg.accept(self)
        
        return 'any'

    def visit_array_access(self, node):
        array_type = node.array.accept(self)
        index_type = node.index.accept(self)
        
        if array_type == 'any':
            return 'any'
        
        if not array_type.endswith('[]'):
            raise SemanticError("Tentativa de indexar não-array", node.line, node.column)
        
        if index_type != 'int' and index_type != 'any':
            raise SemanticError("Índice de array deve ser inteiro", node.line, node.column)
        
        return array_type[:-2]

    def visit_array_literal(self, node):
        if not node.elements:
            return 'any[]'
        
        first_type = node.elements[0].accept(self)
        for element in node.elements[1:]:
            element_type = element.accept(self)
            self.check_type_compatibility(first_type, element_type, "elemento de array", node.line, node.column)
        
        return f"{first_type}[]"