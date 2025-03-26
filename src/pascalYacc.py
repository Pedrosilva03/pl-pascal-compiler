import ply.yacc as yacc
from pascalLexer import tokens

vm_code = ""
functions = {}
variables = {}

def p_program(p):
    'program : header block DOT'
    p[0] = ('program', p[1], p[2])

def p_header(p):
    'header : PROGRAM IDENTIFIER SEMICOLON'
    p[0] = ('header', p[2])
    
def p_block(p):
    """block : variable_declaration body
             | body"""
            #| variable_declaration procedure_function body"""
    # Um bloco contém declarações de variáveis, definições de funções/procedimentos e comandos dentro do 'begin ... end'.
    if len(p) == 4:
        p[0] = ("block", p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = ("block", p[1], p[2])
    else:
        p[0] = ("block", p[1])        
    
### VARIABLE DECLARATION ###

def p_variable_declaration(p):
    """variable_declaration : VAR identifier_list COLON type SEMICOLON variable_declaration
                            | VAR identifier_list COLON type SEMICOLON"""
    # Permite declarações de múltiplas variáveis do mesmo tipo.
    # Exemplo: 'n, i, fat: integer;' será interpretado como [('n', 'NINTEGER'), ('i', 'NINTEGER'), ('fat', 'NINTEGER')]
    # O símbolo '+' é utilizado para concatenar listas.
    global variables
    for var in p[2]:  # Para cada variável declarada
        variables[var] = p[4]  # Associa à tabela de símbolos com seu tipo
    if len(p) == 7:
        p[0] = [(var, p[4]) for var in p[2]] + p[6]
    else:
        p[0] = [(var, p[4]) for var in p[2]]

def p_identifier_list(p):
    '''identifier_list : IDENTIFIER COMMA identifier_list
                       | IDENTIFIER'''
    # Permite listar múltiplos identificadores separados por vírgula.
    # Exemplo: 'n, i, fat' será transformado em ['n', 'i', 'fat']
    if len(p) == 4:
        p[0] = [p[1]] + p[3]  # Lista de identificadores
    else:
        p[0] = [p[1]]  # Apenas um identificador
        
def p_type(p):
    """type : NINTEGER
            | NREAL
            | NSTRING
            | NCHAR
            | NBOOLEAN
            | array_type""" 
    p[0] = p[1]

def p_array_type(p):
    'array_type : ARRAY LBRACKET INTEGER RANGE INTEGER RBRACKET OF type'
    # Representa arrays, incluindo limites inferiores e superiores
    p[0] = ("array", p[3], p[5], p[8])  # Exemplo: ('array', 1, 5, 'NINTEGER')
    
### PROCEDURES E FUNCTIONS ###


### BODY ###
    
def p_body(p):
    'body : BEGIN statements END'
    global vm_code
    vm_code += "START\n"
    vm_code += "\n".join(p[2]) + "\n" 
    vm_code += "STOP\n"
    p[0] = ["START"] + p[2] + ["STOP"]
    
def p_statements(p):
    """statements : statement SEMICOLON statements
                  | statement SEMICOLON"""
    # Concatena os comandos da VM
    if len(p) == 4:
        p[0] = p[1] + p[3]  # Junta as instruções das statements
    else:
        p[0] = p[1]  # Apenas um statement

def p_statement(p):
    """statement : WRITELN LPAREN STRING RPAREN"""
    p[0] = [f'PUSHS "{p[3]}"', "WRITES", "WRITELN"]

# VER SE O QUE FOI FEITO ANTERIORMENTE NÃO PRECISA JÁ DE CÓDIGO MÁQUINA LÁ INSERIDO # 
    
"""
PARA SE VER MAIS TARDE
def p_statement_assignment(p):
    'statement : IDENTIFIER ASSIGNMENT expression'
    global variables
    var_name = p[1]
    if var_name not in variables:
        print(f"Erro: variável '{var_name}' não foi declarada!")
    else:
        expected_type = variables[var_name]
        print(f"Atribuição válida: {var_name} ({expected_type}) := {p[3]}")
    p[0] = ("assign", var_name, p[3])""" 
    
""" 
GRAMÁTICA:
-> program : header block DOT
-> header : PROGRAM IDENTIFIER SEMICOLON
-> block : variable_declaration procedure_function statements
-> variable_declaration : VAR identifier_list COLON type SEMICOLON variable_declaration
                        | VAR identifier_list COLON type SEMICOLON
-> identifier_list : IDENTIFIER COMMA identifier_list
                   | IDENTIFIER'''                        
-> type : NINTEGER | NREAL | NSTRING | NCHAR | NBOOLEAN

### A FAZER ###

-> procedure_function : procedure_function procedure_function
                      | procedure_function
-> compound_statement : BEGIN statement_list END
-> statement_list : statement (SEMICOLON statement)*
-> statement : compound_statement | assignment_statement | empty
-> assignment_statement : variable ASSIGNMENT expr
-> variable : IDENTIFIER
-> expr : term ((PLUS | MINUS) term)*
-> term : factor ((TIMES | DIV) factor)*
-> factor : PLUS factor | MINUS factor | INTEGER | LPAREN expr RPAREN | variable

"""

def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo a '{p.value}' na linha {p.lineno}")
        parser.errok()
    else:
        print("Erro de sintaxe: token inesperado")
    
parser = yacc.yacc()

def parse_input(input_string):
    parser.parse(input_string)
    return vm_code