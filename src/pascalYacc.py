import ply.yacc as yacc
from pascalLexer import tokens

vm_code = ""
functions = {}
variables = {}
variables_assigned = {}

def p_program(p):
    'program : header block DOT'
    p[0] = ('program', p[1], p[2])

def p_header(p):
    'header : PROGRAM IDENTIFIER SEMICOLON'
    p[0] = ('header', p[2])
    
def p_block(p):
    """block : VAR variable_declaration body
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
    """variable_declaration : identifier_list COLON type_name SEMICOLON variable_declaration
                            | identifier_list COLON type_name SEMICOLON"""
    # Permite declarações de múltiplas variáveis do mesmo tipo.
    # Exemplo: 'n, i, fat: integer;' será interpretado como [('n', 'NINTEGER'), ('i', 'NINTEGER'), ('fat', 'NINTEGER')]
    # O símbolo '+' é utilizado para concatenar listas.
    global variables
    variables_aux = {}
    for var in p[1]:  # Para cada variável declarada
        variables_aux[var] = p[3]  # Associa à tabela de símbolos com seu tipo
    variables = {**variables_aux, **variables}
    if len(p) == 6:
        p[0] = [(var, p[3]) for var in p[1]] + p[5]
    else:
        p[0] = [(var, p[3]) for var in p[1]]

def p_identifier_list(p):
    '''identifier_list : IDENTIFIER COMMA identifier_list
                       | IDENTIFIER'''
    # Permite listar múltiplos identificadores separados por vírgula.
    # Exemplo: 'n, i, fat' será transformado em ['n', 'i', 'fat']
    if len(p) == 4:
        p[0] = [p[1]] + p[3]  # Lista de identificadores
    else:
        p[0] = [p[1]]  # Apenas um identificador
        
def p_array_type(p):
    'array_type : ARRAY LBRACKET type RANGE type RBRACKET OF type_name'
    # Representa arrays, incluindo limites inferiores e superiores
    p[0] = ("array", p[3], p[5], p[8])  # Exemplo: ('array', 1, 5, 'NINTEGER')

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
    """statement : writeln
                 | assignment"""
#                 | readln
    p[0] = p[1]

def p_assignment(p):
    """assignment : IDENTIFIER ASSIGNMENT expression"""
    global variables_assigned, variables
    if p[1] in variables.keys():
        var = (p[1], p[3])
        var_type = variables[p[1]]
        variables_assigned[var] = var_type

        if var_type == 'integer':
            p[0] = [f'PUSHI {p[3]}']  # Empilha inteiro
        elif var_type == 'real':
            p[0] = [f'PUSHF {p[3]}']  # Empilha real
        elif var_type == 'string':
            p[0] = [f'PUSHS "{p[3]}"']  # Empilha string
        elif var_type == 'char':
            p[0] = [f'PUSHS "{p[3]}"']  # Empilha caractere
        elif var_type == 'boolean':
            p[0] = [f'PUSHS {str(p[3]).lower()}']  # Empilha booleano (true/false)
        else:
            raise Exception(f"Erro: Tipo inválido para variável '{p[1]}'.")
        
    else:
        #TODO: Lidar com assigmnents a variaveis que nao foram declaradas
        pass

def p_expression(p):
    """expression : type"""
    if len(p) == 4:
        # TODO: Tratar do caso "type operation type"
        pass
    else:
        p[0] = p[1]

def p_operation(p):
    """operation : PLUS
                 | MINUS
                 | TIMES
                 | DIVISION
                 | DIV
                 | MOD
                 | RANGE"""
    p[0] = p[1]

def p_type_name(p):
    """type_name : NINTEGER
            | NREAL
            | NSTRING
            | NCHAR
            | NBOOLEAN
            | array_type""" 
    p[0] = p[1]
    
def p_type(p):
    """type : INTEGER
            | REAL
            | STRING
            | CHAR
            | BOOLEAN
            | IDENTIFIER""" 
    p[0] = p[1]

def p_writeln(p):
    """writeln : WRITELN LPAREN writeln_args RPAREN"""        
    """if isinstance(p[3], str): 
        p[0] = [f'PUSHS "{p[3]}"', "WRITES", "WRITELN"]
    elif isinstance(p[3], int):
        p[0] = [f'PUSHI {p[3]}', "WRITEI", "WRITELN"]
    elif isinstance(p[3], float):
        p[0] = [f'PUSHF {p[3]}', "WRITEF", "WRITELN"]
    elif isinstance(p[3], chr):
        p[0] = [f'PUSHI {ord(p[3])}', "WRITECHR", "WRITELN"]
    if len(p) > 5:"""
    p[0] = p[3] + ["WRITELN"] 
    
def p_writeln_args(p):
    """writeln_args : type COMMA writeln_args 
                    | type"""
    # TODO: Handle IDENTIFIERS. Ainda crasha porque os IDENTIFIERS não fazem parte do type
    global variables
    
    if isinstance(p[1], str) and p[1] not in variables:
        p[0] = [f'PUSHS "{p[1]}"', "WRITES"] + (p[3] if len(p) == 4 else [])
    elif isinstance(p[1], int):
        p[0] = [f'PUSHI {p[1]}', "WRITEI"] + (p[3] if len(p) == 4 else [])
    elif isinstance(p[1], float):
        p[0] = [f'PUSHF {p[1]}', "WRITEF"] + (p[3] if len(p) == 4 else [])
    elif p[1] in variables:
        var_type = variables[p[1]]
        index = list(variables.keys()).index(p[1])
        
        if var_type == 'integer':
            p[0] = [f'PUSHG {index}', "WRITEI"] + (p[3] if len(p) == 4 else [])
        elif var_type == 'real':
            p[0] = [f'PUSHG {index}', "WRITEF"] + (p[3] if len(p) == 4 else [])
        elif var_type == 'string':
            p[0] = [f'PUSHG {index}', "WRITES"] + (p[3] if len(p) == 4 else [])
        elif var_type == 'char':
            p[0] = [f'PUSHG {index}', "WRITECHR"] + (p[3] if len(p) == 4 else [])
        elif var_type == 'boolean':
            p[0] = [f'PUSHG {index}', "WRITES"] + (p[3] if len(p) == 4 else [])
        else:
            raise Exception(f"Erro: Tipo inválido para a variável '{p[1]}'.")
    else:
        raise Exception(f"Erro: Variável '{p[1]}' não declarada.")

def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo a '{p.value}' na linha {p.lineno}")
        parser.errok()
    else:
        print("Erro de sintaxe: token inesperado")
    
parser = yacc.yacc()

def parse_input(input_string):
    parser.parse(input_string)
    print(variables)
    print(variables_assigned)
    return vm_code