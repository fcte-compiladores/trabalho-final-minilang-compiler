#!/usr/bin/env python3
"""
MiniLang - Interpretador de Linguagem Simples
Trabalho Final de Compiladores

Autores: João Victor Felix Moreira, Pedro Everton
"""

import sys
import os
from .lexer import Lexer
from .parser import Parser
from .semantic import SemanticAnalyzer
from .interpreter import Interpreter
from .errors import LexerError, ParserError, SemanticError, RuntimeError

def read_file(filename):
    """Lê o conteúdo de um arquivo"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler arquivo '{filename}': {e}")
        sys.exit(1)

def run_code(source_code, filename="<stdin>"):
    """Executa código MiniLang"""
    try:
        # Análise Léxica
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        # Análise Sintática
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Análise Semântica
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(ast)
        
        # Interpretação
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
    except LexerError as e:
        print(f"Erro Léxico em {filename}: {e}")
        sys.exit(1)
    except ParserError as e:
        print(f"Erro Sintático em {filename}: {e}")
        sys.exit(1)
    except SemanticError as e:
        print(f"Erro Semântico em {filename}: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"Erro em Tempo de Execução em {filename}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado em {filename}: {e}")
        sys.exit(1)

def run_interactive():
    """Executa o interpretador em modo interativo"""
    print("MiniLang Interpretador v1.0")
    print("Digite 'exit' para sair")
    print()
    
    while True:
        try:
            line = input(">>> ")
            if line.strip().lower() == 'exit':
                break
            if line.strip():
                run_code(line, "<interactive>")
        except KeyboardInterrupt:
            print("\nSaindo...")
            break
        except EOFError:
            break

def main():
    """Função principal"""
    if len(sys.argv) == 1:
        # Modo interativo
        run_interactive()
    elif len(sys.argv) == 2:
        # Executa arquivo
        filename = sys.argv[1]
        if not os.path.exists(filename):
            print(f"Erro: Arquivo '{filename}' não encontrado.")
            sys.exit(1)
        
        source_code = read_file(filename)
        run_code(source_code, filename)
    else:
        print("Uso: python3 minilang.py [arquivo.ml]")
        print("  arquivo.ml - arquivo de código MiniLang para executar")
        print("  (sem argumentos) - modo interativo")
        sys.exit(1)

if __name__ == "__main__":
    main()

