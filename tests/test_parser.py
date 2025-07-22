import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.ast_nodes import *
from src.errors import ParserError

def parse_code(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()

def test_simple_variable_declaration():
    ast = parse_code("int x = 10;")
    assert isinstance(ast, Program)
    assert len(ast.statements) == 1
    
    stmt = ast.statements[0]
    assert isinstance(stmt, VarDeclaration)
    assert stmt.type == "int"
    assert stmt.name == "x"
    assert isinstance(stmt.initializer, Literal)
    assert stmt.initializer.value == 10

def test_array_declaration():
    ast = parse_code("int[] arr = [1, 2, 3];")
    assert isinstance(ast, Program)
    assert len(ast.statements) == 1
    
    stmt = ast.statements[0]
    assert isinstance(stmt, ArrayDeclaration)
    assert stmt.element_type == "int"
    assert stmt.name == "arr"
    assert stmt.size is None
    assert isinstance(stmt.initializer, ArrayLiteral)
    assert len(stmt.initializer.elements) == 3
def test_function_declaration():
    ast = parse_code("function add(x, y) { return x + y; }")
    assert isinstance(ast, Program)
    assert len(ast.statements) == 1
    
    stmt = ast.statements[0]
    assert isinstance(stmt, FunctionDeclaration)
    assert stmt.name == "add"
    assert len(stmt.parameters) == 2
    assert stmt.parameters[0].name == "x"
    assert stmt.parameters[1].name == "y"
    assert isinstance(stmt.body, Block)

def test_if_statement():
    ast = parse_code("if (x > 0) { print(x); } else { print(0); }")
    assert isinstance(ast, Program)
    assert len(ast.statements) == 1
    
    stmt = ast.statements[0]
    assert isinstance(stmt, IfStatement)
    assert isinstance(stmt.condition, BinaryOp)
    assert isinstance(stmt.then_stmt, Block)
    assert isinstance(stmt.else_stmt, Block)

def test_while_statement():
    ast = parse_code("while (x > 0) { x = x - 1; }")
    assert isinstance(ast, Program)
    assert len(ast.statements) == 1
    
    stmt = ast.statements[0]
    assert isinstance(stmt, WhileStatement)
    assert isinstance(stmt.condition, BinaryOp)
    assert isinstance(stmt.body, Block)

def test_binary_operations():
    ast = parse_code("int result = 10 + 5 * 2;")
    stmt = ast.statements[0]
    
    # Verifica precedência: 10 + (5 * 2)
    assert isinstance(stmt.initializer, BinaryOp)
    assert stmt.initializer.operator == "+"
    assert isinstance(stmt.initializer.left, Literal)
    assert stmt.initializer.left.value == 10
    assert isinstance(stmt.initializer.right, BinaryOp)
    assert stmt.initializer.right.operator == "*"

def test_function_call():
    ast = parse_code("int result = add(10, 20);")
    stmt = ast.statements[0]
    
    assert isinstance(stmt.initializer, FunctionCall)
    assert stmt.initializer.name == "add"
    assert len(stmt.initializer.arguments) == 2

def test_array_access():
    ast = parse_code("int x = arr[0];")
    stmt = ast.statements[0]
    
    assert isinstance(stmt.initializer, ArrayAccess)
    assert isinstance(stmt.initializer.array, Identifier)
    assert stmt.initializer.array.name == "arr"
    assert isinstance(stmt.initializer.index, Literal)
    assert stmt.initializer.index.value == 0

def test_assignment():
    ast = parse_code("x = 10;")
    stmt = ast.statements[0]
    
    assert isinstance(stmt, Assignment)
    assert isinstance(stmt.target, Identifier)
    assert stmt.target.name == "x"
    assert isinstance(stmt.value, Literal)
    assert stmt.value.value == 10

def test_print_statement():
    ast = parse_code("print(\"Hello World\");")
    stmt = ast.statements[0]
    
    assert isinstance(stmt, PrintStatement)
    assert isinstance(stmt.expression, Literal)
    assert stmt.expression.value == "Hello World"

def test_return_statement():
    ast = parse_code("return x + 1;")
    stmt = ast.statements[0]
    
    assert isinstance(stmt, ReturnStatement)
    assert isinstance(stmt.value, BinaryOp)

def test_complex_expression():
    ast = parse_code("bool result = (x > 0) and (y < 10) or not z;")
    stmt = ast.statements[0]
    
    # Verifica precedência: ((x > 0) and (y < 10)) or (not z)
    assert isinstance(stmt.initializer, BinaryOp)
    assert stmt.initializer.operator == "or"

def test_parser_error():
    with pytest.raises(ParserError):
        parse_code("int x = ;")  # Expressão inválida

def test_missing_semicolon():
    with pytest.raises(ParserError):
        parse_code("int x = 10")  # Falta ponto e vírgula

def test_unmatched_parentheses():
    with pytest.raises(ParserError):
        parse_code("int x = (10 + 5;")  # Parênteses não fechados

