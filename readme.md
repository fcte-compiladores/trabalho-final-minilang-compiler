# MiniLang - Interpretador de Linguagem Simples

## Integrantes

- **João Victor Felix Moreira** - Matrícula: 231037709

- **Pedro Everton** - Matrícula: 221008768

## Introdução

O projeto MiniLang implementa um interpretador completo para uma linguagem de programação simples, mas funcional, que demonstra todos os conceitos fundamentais da teoria de compiladores. A linguagem foi projetada para ser didática e ao mesmo tempo suficientemente expressiva para permitir a implementação de algoritmos básicos e estruturas de dados simples.

### Características da Linguagem MiniLang

A linguagem MiniLang possui as seguintes características principais:

**Tipos de Dados Suportados:**

- Números inteiros (int)

- Números de ponto flutuante (float)

- Strings (string)

- Booleanos (bool)

- Arrays unidimensionais

**Estruturas de Controle:**

- Condicionais (if/else)

- Loops (while, for)

- Funções definidas pelo usuário

**Operadores:**

- Aritméticos: +, -, *, /, %

- Relacionais: ==, !=, <, >, <=, >=

- Lógicos: and, or, not

- Atribuição: =

### Estratégias e Algoritmos Implementados

O interpretador MiniLang foi desenvolvido seguindo a arquitetura clássica de compiladores, implementando as seguintes fases:

**1. Análise Léxica (Lexer)**
Implementamos um analisador léxico baseado em autômatos finitos que reconhece todos os tokens da linguagem. O lexer utiliza uma abordagem de máquina de estados para identificar palavras-chave, identificadores, literais numéricos, strings e operadores. A implementação inclui tratamento de comentários de linha única (iniciados com //) e espaços em branco.

**2. Análise Sintática (Parser)**
O analisador sintático utiliza a técnica de descida recursiva (Recursive Descent Parser) para construir uma Árvore Sintática Abstrata (AST). Esta abordagem foi escolhida por sua simplicidade de implementação e facilidade de depuração. A gramática da linguagem foi cuidadosamente projetada para evitar ambiguidades e conflitos de precedência.

**3. Análise Semântica**
A fase de análise semântica implementa verificação de tipos, resolução de escopo e validação de declarações. Utilizamos uma tabela de símbolos hierárquica para gerenciar escopos aninhados e garantir que variáveis sejam declaradas antes do uso.

**4. Interpretação**
A execução do código é realizada através de um interpretador tree-walking que percorre a AST e executa as operações diretamente. Esta abordagem, embora menos eficiente que a compilação para código de máquina, é mais simples de implementar e adequada para fins educacionais.

### Sintaxe e Semântica da Linguagem

A sintaxe da MiniLang foi inspirada em linguagens como C e Python, buscando um equilíbrio entre familiaridade e simplicidade. Abaixo estão alguns exemplos da sintaxe:

**Declaração de Variáveis:**

```
int x = 10;
float pi = 3.14159;
string nome = "MiniLang";
bool ativo = true;
```

**Estruturas de Controle:**

```
if (x > 5) {
    print("x é maior que 5");
} else {
    print("x é menor ou igual a 5");
}

while (x > 0) {
    print(x);
    x = x - 1;
}
```

**Definição de Funções:**

```
function fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n-1) + fibonacci(n-2);
}
```

**Arrays:**

```
int[] numeros = [1, 2, 3, 4, 5];
print(numeros[0]); // Imprime 1
```

A semântica da linguagem segue convenções padrão: variáveis devem ser declaradas antes do uso, funções podem ser recursivas, arrays são indexados a partir de zero, e a linguagem suporta escopo léxico para variáveis locais.

## Instalação

### Pré-requisitos

O projeto foi desenvolvido em Python 3.8+ e utiliza apenas bibliotecas padrão da linguagem, não requerendo dependências externas. Certifique-se de ter Python instalado em seu sistema.

### Passos de Instalação

1. **Clone o repositório:**

```bash
git clone [URL_DO_REPOSITORIO]
cd compilador_final
```

1. **Verificar a instalação do Python:**

```bash
python3 --version
```

1. **Executar o interpretador:**

```bash
python3 src/minilang.py exemplos/hello.ml
```

### Uso Básico

Para executar um programa MiniLang, use o comando:

```bash
python3 src/minilang.py <arquivo.ml>
```

Para executar o interpretador em modo interativo:

```bash
python3 src/minilang.py
```

Para executar os testes:

```bash
python3 -m pytest tests/
```

## Exemplos

O diretório `exemplos/` contém uma série de programas demonstrando as capacidades da linguagem MiniLang, organizados por ordem crescente de complexidade:

### 1. Hello World (hello.ml)

Programa básico que demonstra saída de texto:

```
print("Olá, mundo!");
```

### 2. Fibonacci (fibonacci.ml)

Implementação recursiva da sequência de Fibonacci:

```
function fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n-1) + fibonacci(n-2);
}

int resultado = fibonacci(10);
print("Fibonacci de 10: " + resultado);
```

### 3. Função Recursiva - Fatorial (fatorial.ml)

Demonstra recursão com cálculo de fatorial:

```
function fatorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * fatorial(n-1);
}

print("Fatorial de 5: " + fatorial(5));
```

Estes exemplos demonstram progressivamente as capacidades da linguagem, desde operações básicas até algoritmos mais complexos, mostrando que a MiniLang é capaz de expressar uma variedade significativa de programas.

## Referências

O desenvolvimento do interpretador MiniLang foi baseado em várias fontes acadêmicas e recursos técnicos fundamentais na área de compiladores. Cada referência desempenhou um papel específico na implementação e design da linguagem:

### Livros e Materiais Acadêmicos

**[1] Aho, Alfred V., et al. "Compilers: Principles, Techniques, and Tools" (Dragon Book), 2nd Edition, Addison-Wesley, 2006.**
Esta obra clássica serviu como base teórica fundamental para o projeto, especialmente nos capítulos sobre análise léxica e sintática. As técnicas de construção de analisadores léxicos baseados em autômatos finitos e os algoritmos de parsing descendente recursivo foram diretamente inspirados nos conceitos apresentados neste livro. A estrutura geral do compilador e a organização das fases de compilação seguem as diretrizes estabelecidas pelos autores.

**[2] Crafting Interpreters por Robert Nystrom, disponível em **[**https://craftinginterpreters.com/**](https://craftinginterpreters.com/)
Este recurso online foi fundamental para a implementação prática do interpretador tree-walking. O livro forneceu insights valiosos sobre como estruturar um interpretador de forma clara e eficiente, especialmente na implementação da AST (Abstract Syntax Tree) e no sistema de avaliação de expressões. A abordagem de implementação em duas partes (tree-walking interpreter e bytecode virtual machine) influenciou nossa decisão de focar na primeira abordagem para fins educacionais.

**[3] Engineering a Compiler, 2nd Edition, por Keith Cooper e Linda Torczon, Morgan Kaufmann, 2011.**
Este livro contribuiu significativamente para o design da análise semântica e do sistema de tipos da MiniLang. Os capítulos sobre análise de escopo e verificação de tipos forneceram a base teórica para a implementação da tabela de símbolos hierárquica e dos algoritmos de verificação de tipos em tempo de compilação.

### Recursos Online e Documentação Técnica

**[4] Python AST Documentation - **[**https://docs.python.org/3/library/ast.html**](https://docs.python.org/3/library/ast.html)
A documentação oficial do módulo AST do Python serviu como referência para o design da estrutura de nós da árvore sintática abstrata da MiniLang. Embora não tenhamos usado diretamente o módulo AST do Python, a estrutura e organização dos diferentes tipos de nós influenciaram nosso design.

**[5] ANTLR Documentation - **[**https://www.antlr.org/**](https://www.antlr.org/)
Embora não tenhamos usado ANTLR diretamente, a documentação e exemplos de gramáticas forneceram insights valiosos sobre como estruturar gramáticas livres de contexto de forma clara e sem ambiguidades. Os exemplos de gramáticas para linguagens similares ajudaram na definição da sintaxe da MiniLang.

### Contribuições Originais

Todas as implementações de código neste projeto são originais, desenvolvidas especificamente para este trabalho acadêmico. As principais contribuições originais incluem:

- **Design da Linguagem MiniLang**: A sintaxe e semântica da linguagem foram projetadas especificamente para este projeto, combinando elementos familiares de linguagens populares com simplificações adequadas para fins educacionais.

- **Implementação do Lexer**: O analisador léxico foi implementado do zero usando uma abordagem de máquina de estados finitos, sem uso de geradores de lexers externos.

- **Parser Recursivo Descendente**: O analisador sintático foi implementado manualmente usando a técnica de descida recursiva, com tratamento cuidadoso de precedência de operadores e associatividade.

- **Sistema de Tipos Simplificado**: Desenvolvemos um sistema de tipos básico mas funcional que suporta verificação estática de tipos e conversões implícitas quando apropriado.

- **Interpretador Tree-Walking**: A implementação do interpretador que percorre a AST foi desenvolvida especificamente para este projeto, com otimizações para melhor performance e clareza de código.

- **Conjunto de Exemplos**: Todos os programas de exemplo foram escritos especificamente para demonstrar as capacidades da linguagem MiniLang, progredindo de conceitos básicos para algoritmos mais complexos.

## Estrutura do Código

O projeto está organizado em uma estrutura modular que separa claramente as diferentes fases do processo de compilação/interpretação. Esta organização facilita a manutenção, teste e compreensão do código:

### Organização de Diretórios

```
compilador_final/
├── src/                    # Código fonte principal
│   ├── minilang.py        # Ponto de entrada principal
│   ├── lexer.py           # Analisador léxico
│   ├── parser.py          # Analisador sintático
│   ├── ast_nodes.py       # Definições dos nós da AST
│   ├── semantic.py        # Análise semântica
│   ├── interpreter.py     # Interpretador tree-walking
│   ├── symbol_table.py    # Tabela de símbolos
│   └── errors.py          # Classes de erro personalizadas
├── exemplos/              # Programas de exemplo
├── tests/                 # Testes unitários
├── docs/                  # Documentação adicional
└── README.md             # Este arquivo
```

### Módulos Principais

#### 1. minilang.py - Ponto de Entrada

Este módulo serve como interface principal do interpretador, coordenando todas as fases do processo de compilação/interpretação. Suas responsabilidades incluem:

- Processamento de argumentos de linha de comando

- Leitura de arquivos de código fonte

- Coordenação das fases de análise léxica, sintática e semântica

- Invocação do interpretador

- Tratamento de erros globais e relatórios de diagnóstico

#### 2. lexer.py - Análise Léxica

O módulo lexer implementa a primeira fase do processo de compilação, responsável por converter o texto de entrada em uma sequência de tokens. A implementação inclui:

**Classe Token**: Representa um token individual com tipo, valor e informações de posição no código fonte.

**Classe Lexer**: Implementa o analisador léxico principal usando uma abordagem de máquina de estados. Principais características:

- Reconhecimento de palavras-chave da linguagem

- Identificação de identificadores e literais

- Processamento de operadores e delimitadores

- Tratamento de comentários e espaços em branco

- Relatório de erros léxicos com informações de posição

**Tipos de Token Suportados**:

- IDENTIFIER: nomes de variáveis e funções

- NUMBER: literais numéricos (inteiros e ponto flutuante)

- STRING: literais de string

- KEYWORD: palavras-chave da linguagem (if, while, function, etc.)

- OPERATOR: operadores aritméticos, relacionais e lógicos

- DELIMITER: parênteses, chaves, colchetes, ponto e vírgula

- EOF: fim do arquivo

#### 3. ast_nodes.py - Nós da Árvore Sintática Abstrata

Este módulo define a hierarquia de classes que representam os diferentes tipos de nós na AST. A estrutura segue o padrão Visitor para facilitar operações sobre a árvore:

**Classe Base ASTNode**: Classe abstrata que define a interface comum para todos os nós da AST.

**Nós de Expressão**:

- BinaryOp: operações binárias (aritméticas, relacionais, lógicas)

- UnaryOp: operações unárias (negação, not lógico)

- Literal: valores literais (números, strings, booleanos)

- Identifier: referências a variáveis

- FunctionCall: chamadas de função

- ArrayAccess: acesso a elementos de array

**Nós de Declaração**:

- VarDeclaration: declarações de variáveis

- FunctionDeclaration: declarações de funções

- ArrayDeclaration: declarações de arrays

**Nós de Comando**:

- Assignment: atribuições

- IfStatement: comandos condicionais

- WhileStatement: loops while

- ForStatement: loops for

- ReturnStatement: comandos return

- PrintStatement: comandos print

- Block: blocos de comandos

#### 4. parser.py - Análise Sintática

O analisador sintático implementa um parser recursivo descendente que constrói a AST a partir da sequência de tokens. A implementação segue a gramática da linguagem MiniLang:

**Classe Parser**: Implementa o analisador sintático principal com métodos para cada construção sintática da linguagem.

**Métodos Principais**:

- parse(): método principal que inicia a análise

- parse_statement(): analisa comandos

- parse_expression(): analisa expressões com precedência de operadores

- parse_declaration(): analisa declarações

- parse_function(): analisa definições de funções

- parse_block(): analisa blocos de comandos

**Tratamento de Precedência**: O parser implementa precedência de operadores usando a técnica de climbing precedence, garantindo que expressões sejam avaliadas na ordem correta.

**Recuperação de Erros**: O parser inclui mecanismos básicos de recuperação de erros sintáticos, permitindo continuar a análise após encontrar erros e reportar múltiplos problemas em uma única execução.

#### 5. semantic.py - Análise Semântica

Este módulo implementa a análise semântica, responsável por verificar a correção semântica do programa:

**Classe SemanticAnalyzer**: Implementa o analisador semântico usando o padrão Visitor para percorrer a AST.

**Verificações Implementadas**:

- Verificação de tipos: garante compatibilidade de tipos em operações e atribuições

- Resolução de escopo: verifica se variáveis são declaradas antes do uso

- Verificação de funções: valida chamadas de função e tipos de retorno

- Verificação de arrays: valida acessos a arrays e tipos de índices

**Sistema de Tipos**: Implementa um sistema de tipos simples mas robusto que suporta:

- Tipos primitivos: int, float, string, bool

- Arrays unidimensionais

- Conversões implícitas quando apropriado

- Verificação de compatibilidade em operações

#### 6. symbol_table.py - Tabela de Símbolos

Implementa uma tabela de símbolos hierárquica para gerenciar escopos aninhados:

**Classe Symbol**: Representa um símbolo na tabela com informações de tipo e escopo.

**Classe SymbolTable**: Implementa a tabela de símbolos com suporte a escopos aninhados:

- Inserção e busca de símbolos

- Gerenciamento de escopos (enter_scope/exit_scope)

- Resolução de nomes considerando hierarquia de escopos

- Verificação de redeclarações

#### 7. interpreter.py - Interpretador Tree-Walking

O interpretador implementa a execução do programa percorrendo a AST:

**Classe Interpreter**: Implementa o interpretador principal usando o padrão Visitor.

**Ambiente de Execução**: Mantém o estado do programa durante a execução:

- Valores de variáveis

- Pilha de chamadas de função

- Gerenciamento de escopo em tempo de execução

**Execução de Comandos**: Implementa a semântica de execução para todos os tipos de comandos da linguagem:

- Avaliação de expressões

- Execução de comandos de controle de fluxo

- Chamadas de função com passagem de parâmetros

- Operações com arrays

#### 8. errors.py - Tratamento de Erros

Define classes de erro personalizadas para diferentes tipos de problemas:

**LexicalError**: Erros na análise léxica (caracteres inválidos, strings não terminadas)
**SyntaxError**: Erros na análise sintática (sintaxe inválida, tokens inesperados)
**SemanticError**: Erros na análise semântica (tipos incompatíveis, variáveis não declaradas)
**RuntimeError**: Erros em tempo de execução (divisão por zero, acesso inválido a array)

### Fluxo de Execução

O processo de compilação/interpretação segue o fluxo tradicional:

1. **Análise Léxica**: O código fonte é tokenizado pelo lexer

1. **Análise Sintática**: Os tokens são analisados pelo parser para construir a AST

1. **Análise Semântica**: A AST é verificada semanticamente

1. **Interpretação**: A AST é executada pelo interpretador tree-walking

Cada fase pode detectar e reportar erros específicos, permitindo diagnósticos precisos para o programador.

## Bugs/Limitações/Problemas Conhecidos

Embora o interpretador MiniLang implemente com sucesso os conceitos fundamentais de compiladores, existem várias limitações e áreas que poderiam ser melhoradas em versões futuras:

### Limitações de Design da Linguagem

**1. Sistema de Tipos Simplificado**
O sistema de tipos atual é bastante básico e não suporta algumas características importantes:

- Não há suporte para tipos definidos pelo usuário (structs ou classes)

- Arrays são limitados a uma dimensão

- Não há suporte para ponteiros ou referências

- O sistema de tipos não suporta generics ou templates

**2. Gerenciamento de Memória**
A linguagem não implementa gerenciamento explícito de memória:

- Não há controle sobre alocação/desalocação de memória

- Arrays têm tamanho fixo definido na declaração

- Não há garbage collection implementado (depende do garbage collector do Python)

**3. Limitações de Escopo**
Algumas limitações no sistema de escopo:

- Não há suporte para closures

- Variáveis globais têm comportamento limitado

- Não há suporte para namespaces ou módulos

### Problemas de Implementação

**1. Performance do Interpretador**
O interpretador tree-walking, embora simples de implementar, tem limitações de performance:

- Cada nó da AST é visitado repetidamente durante loops

- Não há otimizações de código implementadas

- Chamadas de função têm overhead significativo devido à criação de novos escopos

**2. Tratamento de Erros**
O sistema de tratamento de erros poderia ser mais robusto:

- Mensagens de erro poderiam ser mais descritivas

- Não há suporte para warnings (apenas erros fatais)

- A recuperação de erros sintáticos é básica

- Não há stack trace detalhado para erros em tempo de execução

**3. Limitações do Parser**
O parser recursivo descendente tem algumas limitações:

- Não suporta recursão à esquerda direta

- Algumas construções sintáticas são mais verbosas que o necessário

- Não há suporte para operadores definidos pelo usuário

### Bugs Conhecidos

**1. Overflow de Inteiros**
A linguagem não trata adequadamente overflow de inteiros:

- Operações que resultam em valores muito grandes podem causar comportamento indefinido

- Não há verificação de limites para operações aritméticas

**2. Divisão por Zero**
Embora seja detectada em tempo de execução, a divisão por zero poderia ser tratada de forma mais elegante:

- Não há diferenciação entre divisão inteira e de ponto flutuante

- A mensagem de erro poderia ser mais específica

**3. Comparação de Tipos Diferentes**
A comparação entre tipos diferentes pode produzir resultados inesperados:

- Comparações entre strings e números não são adequadamente tratadas

- Não há conversão automática consistente entre tipos

### Melhorias Incrementais Propostas

**1. Melhorias no Sistema de Tipos**

- Implementar verificação mais rigorosa de tipos

- Adicionar suporte para arrays multidimensionais

- Implementar conversões de tipo mais inteligentes

- Adicionar tipos opcionais (nullable types)

**2. Otimizações de Performance**

- Implementar constant folding durante a análise sintática

- Adicionar cache para resultados de expressões constantes

- Otimizar chamadas de função recursivas (tail call optimization)

- Implementar um sistema de bytecode para melhor performance

**3. Melhorias na Usabilidade**

- Implementar um debugger básico

- Adicionar suporte para importação de módulos

- Melhorar mensagens de erro com sugestões de correção

- Implementar um sistema de warnings para código potencialmente problemático

**4. Extensões da Linguagem**

- Adicionar suporte para strings multi-linha

- Implementar operadores de incremento/decremento (++, --)

- Adicionar suporte para switch/case statements

- Implementar try/catch para tratamento de exceções

**5. Ferramentas de Desenvolvimento**

- Implementar um formatter de código

- Adicionar um linter básico

- Criar um sistema de documentação automática

- Implementar testes de integração mais abrangentes

### Considerações para Uso Educacional

É importante notar que muitas dessas limitações são intencionais, dado o propósito educacional do projeto. A simplicidade da implementação permite focar nos conceitos fundamentais de compiladores sem se perder em detalhes de otimização ou características avançadas de linguagens modernas.

Para uso em produção, seria necessário abordar muitas dessas limitações, mas para fins de aprendizado e demonstração dos conceitos de compiladores, a implementação atual atende adequadamente aos objetivos propostos.

A experiência de implementar este interpretador fornece uma base sólida para compreender como linguagens de programação mais complexas são implementadas, e as limitações identificadas servem como pontos de partida para estudos mais avançados na área de compiladores e design de linguagens.

## Documentação Técnica

Para uma análise aprofundada da arquitetura, design e implementação do compilador, consulte a [Documentação Técnica](documentation.md).

