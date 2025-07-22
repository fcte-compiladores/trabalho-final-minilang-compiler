import pytest
import io
import sys
from src.lexer import Lexer
from src.parser import Parser
from src.semantic import SemanticAnalyzer
from src.interpreter import Interpreter
from src.errors import RuntimeError

def run_code(code):
    """Helper para executar código MiniLang"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.analyze(ast)
    interpreter = Interpreter()
    interpreter.interpret(ast)
    return interpreter

def capture_output(code):
    """Helper para capturar saída do print"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    try:
        run_code(code)
        return captured_output.getvalue().strip()
    finally:
        sys.stdout = old_stdout

def test_variable_declaration_and_assignment():
    interpreter = run_code("""
        int x = 10;
        float y = 3.14;
        string name = "MiniLang";
        bool active = true;
    """)
    
    assert interpreter.globals.get("x") == 10
    assert interpreter.globals.get("y") == 3.14
    assert interpreter.globals.get("name") == "MiniLang"
    assert interpreter.globals.get("active") == True

def test_arithmetic_operations():
    output = capture_output("""
        int a = 10;
        int b = 5;
        print(a + b);
        print(a - b);
        print(a * b);
        print(a / b);
        print(a % b);
    """)
    
    lines = output.split('\n')
    assert lines[0] == "15"
    assert lines[1] == "5"
    assert lines[2] == "50"
    assert lines[3] == "2"
    assert lines[4] == "0"

def test_comparison_operations():
    output = capture_output("""
        int x = 10;
        int y = 5;
        print(x > y);
        print(x < y);
        print(x >= y);
        print(x <= y);
        print(x == y);
        print(x != y);
    """)
    
    lines = output.split('\n')
    assert lines[0] == "true"
    assert lines[1] == "false"
    assert lines[2] == "true"
    assert lines[3] == "false"
    assert lines[4] == "false"
    assert lines[5] == "true"

def test_logical_operations():
    output = capture_output("""
        bool a = true;
        bool b = false;
        print(a and b);
        print(a or b);
        print(not a);
        print(not b);
    """)
    
    lines = output.split('\n')
    assert lines[0] == "false"
    assert lines[1] == "true"
    assert lines[2] == "false"
    assert lines[3] == "true"

def test_string_concatenation():
    output = capture_output("""
        string first = "Hello";
        string second = "World";
        print(first + " " + second);
    """)
    
    assert output == "Hello World"

def test_if_statement():
    output = capture_output("""
        int x = 10;
        if (x > 5) {
            print("x é maior que 5");
        } else {
            print("x é menor ou igual a 5");
        }
    """)
    
    assert output == "x é maior que 5"

def test_while_loop():
    output = capture_output("""
        int i = 0;
        while (i < 3) {
            print(i);
            i = i + 1;
        }
    """)
    
    lines = output.split('\n')
    assert lines[0] == "0"
    assert lines[1] == "1"
    assert lines[2] == "2"

def test_function_declaration_and_call():
    output = capture_output("""
        function add(x, y) {
            return x + y;
        }
        
        int result = add(10, 20);
        print(result);
    """)
    
    assert output == "30"

def test_recursive_function():
    output = capture_output("""
        function factorial(n) {
            if (n <= 1) {
                return 1;
            }
            return n * factorial(n - 1);
        }
        
        print(factorial(5));
    """)
    
    assert output == "120"

def test_array_operations():
    output = capture_output("""
        int[] numbers = [1, 2, 3, 4, 5];
        print(numbers[0]);
        print(numbers[2]);
        numbers[1] = 10;
        print(numbers[1]);
    """)
    
    lines = output.split('\n')
    assert lines[0] == "1"
    assert lines[1] == "3"
    assert lines[2] == "10"

def test_array_assignment():
    interpreter = run_code("""
        int[] arr = [1, 2, 3];
        arr[0] = 10;
        arr[2] = 30;
    """)
    
    arr = interpreter.globals.get("arr")
    assert arr[0] == 10
    assert arr[1] == 2
    assert arr[2] == 30

def test_scope_in_function():
    output = capture_output("""
        int global_var = 100;
        
        function test() {
            int local_var = 50;
            print(global_var);
            print(local_var);
        }
        
        test();
    """)
    
    lines = output.split('\n')
    assert lines[0] == "100"
    assert lines[1] == "50"

def test_for_loop():
    output = capture_output("""
        for (int i = 0; i < 3; i = i + 1) {
            print(i);
        }
    """)
    
    lines = output.split('\n')
    assert lines[0] == "0"
    assert lines[1] == "1"
    assert lines[2] == "2"

def test_division_by_zero():
    with pytest.raises(RuntimeError):
        run_code("int x = 10 / 0;")

def test_array_index_out_of_bounds():
    with pytest.raises(RuntimeError):
        run_code("""
            int[] arr = [1, 2, 3];
            print(arr[5]);
        """)

def test_undefined_variable():
    with pytest.raises(Exception):  # Pode ser SemanticError ou RuntimeError
        run_code("print(undefined_var);")

def test_type_conversions():
    output = capture_output("""
        int x = 10;
        float y = 3.14;
        print(x + y);
    """)
    
    assert output == "13.14"

def test_complex_program():
    output = capture_output("""
        function fibonacci(n) {
            if (n <= 1) {
                return n;
            }
            return fibonacci(n-1) + fibonacci(n-2);
        }
        
        int[5] results;
        for (int i = 0; i < 5; i = i + 1) {
            results[i] = fibonacci(i);
        }
        
        for (int i = 0; i < 5; i = i + 1) {
            print("Fibonacci(" + i + ") = " + results[i]);
        }
    """)
    
    lines = output.split('\n')
    assert "Fibonacci(0) = 0" in lines[0]
    assert "Fibonacci(1) = 1" in lines[1]
    assert "Fibonacci(2) = 1" in lines[2]
    assert "Fibonacci(3) = 2" in lines[3]
    assert "Fibonacci(4) = 3" in lines[4]

