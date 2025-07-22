# Documentação Técnica do MiniLang Compiler

Este documento detalha a arquitetura, o design e a implementação do compilador para a linguagem MiniLang.

## 1. Visão Geral do Projeto

O MiniLang Compiler é um projeto de compilador simples desenvolvido em Python, focado em demonstrar os conceitos fundamentais de compilação, incluindo análise léxica, análise sintática, análise semântica e interpretação. A linguagem MiniLang é uma linguagem de programação imperativa com tipagem estática, suporte a variáveis, arrays, estruturas de controle (if, while, for), funções e operações básicas.

## 2. Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```
compilador_final/
├── src/
│   ├── __init__.py
│   ├── lexer.py        
│   ├── parser.py        
│   ├── ast_nodes.py     
│   ├── symbol_table.py  
│   ├── semantic.py      
│   ├── interpreter.py   
│   ├── errors.py        
│   └── minilang.py      
├── tests/
│   ├── test_lexer.py    
│   ├── test_parser.py   
│   └── test_interpreter.py 
├── exemplos/
│   ├── hello.ml
│   ├── fibonacci.ml
│   └── fatorial.ml
├── requirements.txt     
├── README.md            
└── documentation.md     
```

## 3. Componentes do Compilador

### 3.1. Lexer (Análise Léxica)

O `lexer.py` é responsável por transformar o código fonte do MiniLang em uma sequência de tokens. Ele identifica palavras-chave, identificadores, literais (inteiros, floats, strings, booleanos), operadores e símbolos, ignorando espaços em branco e comentários.

- **Tokens Suportados:** INT, FLOAT, STRING, BOOL, IDENTIFIER, NUMBER, STRING_LITERAL, TRUE, FALSE, FUNCTION, IF, ELSE, WHILE, FOR, RETURN, PRINT, ASSIGN, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EQUAL, NOT_EQUAL, LESS, LESS_EQUAL, GREATER, GREATER_EQUAL, AND, OR, NOT, LPAREN, RPAREN, LBRACE, RBRACE, LBRACKET, RBRACKET, SEMICOLON, COMMA, EOF.

- **Tratamento de Erros:** Detecta caracteres inválidos e strings não terminadas.

### 3.2. Parser (Análise Sintática)

O `parser.py` recebe a sequência de tokens do lexer e constrói uma Árvore Sintática Abstrata (AST). Ele implementa uma gramática para MiniLang usando um parser recursivo descendente.

- **Gramática (simplificada):**
  - `Program` -> `Statement*`
  - `Statement` -> `Declaration` | `ControlStatement` | `ExpressionStatement` | `Block`
  - `Declaration` -> `VarDeclaration` | `ArrayDeclaration` | `FunctionDeclaration`
  - `VarDeclaration` -> `Type IDENTIFIER ( = Expression )? ;`
  - `ArrayDeclaration` -> `Type [ (NUMBER)? ] IDENTIFIER ( = ArrayLiteral )? ;`
  - `FunctionDeclaration` -> `function IDENTIFIER ( ParameterList ) Block`
  - `ParameterList` -> `( Type? IDENTIFIER ( , Type? IDENTIFIER )* )?`
  - `ControlStatement` -> `IfStatement` | `WhileStatement` | `ForStatement` | `ReturnStatement` | `PrintStatement`
  - `IfStatement` -> `if ( Expression ) Statement ( else Statement )?`
  - `WhileStatement` -> `while ( Expression ) Statement`
  - `ForStatement` -> `for ( (DeclarationNoSemicolon | ExpressionStatementNoSemicolon)? ; Expression? ; ExpressionStatementNoSemicolon? ) Statement`
  - `ReturnStatement` -> `return Expression? ;`
  - `PrintStatement` -> `print ( Expression ) ;`
  - `ExpressionStatement` -> `Expression ( = Expression )? ;`
  - `Block` -> `{ Statement* }`
  - `Expression` -> `LogicalOr`
  - `LogicalOr` -> `LogicalAnd ( or LogicalAnd )*`
  - `LogicalAnd` -> `Equality ( and Equality )*`
  - `Equality` -> `Comparison ( ( == | != ) Comparison )*`
  - `Comparison` -> `Term ( ( < | <= | > | >= ) Term )*`
  - `Term` -> `Factor ( ( + | - ) Factor )*`
  - `Factor` -> `Unary ( ( * | / | % ) Unary )*`
  - `Unary` -> `( - | not ) Unary | Postfix`
  - `Postfix` -> `Primary ( ArrayAccess | FunctionCall )*`
  - `ArrayAccess` -> `[ Expression ]`
  - `FunctionCall` -> `( ArgumentList )`
  - `ArgumentList` -> `( Expression ( , Expression )* )?`
  - `Primary` -> `NUMBER | STRING_LITERAL | TRUE | FALSE | IDENTIFIER | ( Expression ) | ArrayLiteral`
  - `ArrayLiteral` -> `[ ( Expression ( , Expression )* )? ]`

- **Nós da AST:** Definidos em `ast_nodes.py`, representam a estrutura hierárquica do código fonte.

- **Tratamento de Erros:** Lança `ParserError` para erros de sintaxe, como tokens inesperados ou falta de delimitadores.

### 3.3. AST Nodes (`ast_nodes.py`)

Define as classes para cada tipo de nó na Árvore Sintática Abstrata (AST). Cada nó herda de `ASTNode` e implementa o método `accept` para o padrão Visitor, facilitando a travessia da AST pelos analisadores semântico e interpretador.

### 3.4. Tabela de Símbolos (`symbol_table.py`)

Implementa uma tabela de símbolos com escopo aninhado. Usada pela análise semântica para armazenar informações sobre variáveis e funções (nome, tipo, etc.) e para verificar a visibilidade e declaração de identificadores.

### 3.5. Análise Semântica (`semantic.py`)

O `semantic.py` percorre a AST para realizar verificações de tipo, escopo e outras regras semânticas da linguagem. Ele utiliza a tabela de símbolos para rastrear declarações e resolver identificadores.

- **Verificações Principais:**
  - **Declaração de Variáveis:** Garante que variáveis não sejam redeclaradas no mesmo escopo.
  - **Resolução de Símbolos:** Verifica se todas as variáveis e funções usadas foram declaradas.
  - **Compatibilidade de Tipos:** Assegura que operações e atribuições sejam realizadas com tipos compatíveis. Suporta conversões implícitas entre `int` e `float`.
  - **Chamadas de Função:** Verifica se o identificador chamado é realmente uma função e, de forma simplificada, se o número de argumentos corresponde (poderia ser estendido para verificar tipos de argumentos).
  - **Arrays:** Verifica o tipo do elemento e o tipo do índice (deve ser `int`).

- **Tratamento de Erros:** Lança `SemanticError` para violações das regras semânticas.

### 3.6. Interpretador (`interpreter.py`)

O `interpreter.py` é o componente final que executa o código MiniLang diretamente da AST. Ele percorre a AST, avaliando expressões e executando comandos.

- **Ambiente de Execução:** Gerencia o estado das variáveis e funções usando um ambiente de escopo aninhado (similar à tabela de símbolos).

- **Execução de Comandos:** Implementa a lógica para `if`, `while`, `for`, `return`, `print`, atribuições e chamadas de função.

- **Avaliação de Expressões:** Calcula o valor de expressões aritméticas, lógicas, relacionais, literais, identificadores, chamadas de função e acessos a arrays.

- **Tratamento de Arrays:** Suporta declaração, inicialização (com literais ou tamanho fixo), acesso e atribuição de elementos de array.

- **Tratamento de Erros:** Lança `RuntimeError` para erros que ocorrem durante a execução, como divisão por zero ou índice de array fora dos limites.

### 3.7. Erros (`errors.py`)

Define classes de exceção personalizadas para diferentes tipos de erros que podem ocorrer durante as fases de compilação e execução: `LexerError`, `ParserError`, `SemanticError` e `RuntimeError`.

## 4. Como Usar

Para usar o compilador MiniLang, siga os passos abaixo:

1. **Instalação das Dependências:**

1. **Execução de um Arquivo MiniLang:**

1. **Execução dos Testes:**
Para executar os testes unitários e de integração, navegue até o diretório raiz do projeto e execute:

## 5. Exemplos de Código MiniLang

O diretório `exemplos/` contém vários programas de exemplo para demonstrar as funcionalidades da linguagem:

- `hello.ml`: Um programa simples que imprime "Hello, World!".

- `fibonacci.ml`: Implementação da sequência de Fibonacci usando recursão.

- `fatorial.ml`: Cálculo do fatorial de um número.

## 6. Considerações Finais

Este projeto serve como uma base para entender o funcionamento interno de um compilador. Embora o MiniLang seja uma linguagem simples, ele incorpora os principais conceitos de um compilador funcional. Possíveis melhorias futuras incluem a adição de mais tipos de dados, estruturas de dados complexas (objetos, structs), otimizações de código, geração de código intermediário ou código de máquina, e um sistema de módulos.

