import ply.yacc as yacc
from pascalLexer import tokens

import utils

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
             | body
             | function block"""
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
    for var in p[1]:  # Para cada variável declarada
        variables[var] = p[3]  # Associa à tabela de símbolos com seu tipo
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
    """assignment : IDENTIFIER ASSIGNMENT type
                  | IDENTIFIER ASSIGNMENT expression"""
    global variables_assigned, variables, functions
    # Caso para lidar com tentativas de assignment a variáveis que não fora declaradas
    if p[1] in variables.keys() or p[1] in functions.keys():
        var_type = variables[p[1]]
        variables_assigned[p[1]] = var_type
        index_destiny = list(variables.keys()).index(p[1])
        if isinstance(p[3], list): # Caso em que são valores elementares ou previamente processados e podem ser imediatamente atribuidos
            p[0] = p[3]
        else: # Caso em que é um identifier
            index_source = list(variables.keys()).index(p[3])
            if p[3] not in variables.keys():
                raise Exception(f"Erro: Variável '{p[3]}' não declarada.")
            if p[3] not in variables_assigned.keys():
                print(f"Erro: Variável '{p[3]}' não atribuida.")
            p[0] = [f'PUSHG {index_source}']
        
        p[0] += [f'STOREG {index_destiny}']
    else:
        raise Exception(f"Erro: Variável '{p[1]}' não declarada.")

def p_expression(p):
    """expression : type operation type
                  | expression_paren
                  | expression operation expression
                  | func_call"""
    global variables_assigned, variables
    if len(p) == 4:
        if not isinstance(p[1], str) and not isinstance(p[3], str):
            p[0] = p[1] + p[3] + p[2]
        else:
            if p[1] not in variables.keys():
                raise Exception(f"Erro: Variável '{p[1]}' não declarada.")
            if p[1] not in variables_assigned.keys():
                print(f"Warning: Variável '{p[1]}' não atribuida.")
            if p[3] not in variables.keys():
                raise Exception(f"Erro: Variável '{p[3]}' não declarada.")
            if p[3] not in variables_assigned.keys():
                print(f"Warning: Variável '{p[3]}' não atribuida.")
            
            p[0] = []
            if not isinstance(p[1], str):
                p[0] += p[1]
            else:
                index_source1 = list(variables.keys()).index(p[1])
                p[0] += [f'PUSHG {index_source1}']
            if not isinstance(p[3], str):
                p[0] += p[3]
            else:
                index_source2 = list(variables.keys()).index(p[3])
                p[0] += [f'PUSHG {index_source2}']
            p[0] += p[2]
    else:
        if "CALL" in p[1]: # Caso em que é uma function call visto que tem o mesmo numero de tokens que a expressao entre parentises
            func_index = utils.get_name_from_pusha(p[1])
            p[0] = p[1] + [f'PUSHG {list(variables.keys()).index(func_index)}']
        else:
            p[0] = p[1]

def p_expression_paren(p):
    """expression_paren : LPAREN expression RPAREN"""
    p[0] = p[2]

def p_operation(p):
    """operation : plus
                 | minus
                 | times
                 | division
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
    """type : integer
            | real
            | string
            | char
            | boolean
            | identifier
            | func_call""" 
    p[0] = p[1]

# TIPOS ELEMENTARES

def p_integer(p):
    """integer : INTEGER"""
    p[0] = [f'PUSHI {p[1]}']

def p_real(p):
    """real : REAL"""
    p[0] = [f'PUSHF {p[1]}']

def p_string(p):
    """string : STRING"""
    p[0] = [f'PUSHS "{p[1]}"']

def p_char(p):
    """char : CHAR"""
    p[0] = [f'PUSHS "{p[1]}"']

def p_boolean(p):
    """boolean : BOOLEAN"""
    p[0] = [f'PUSHS {str(p[3]).lower()}']

def p_identifier(p):
    """identifier : IDENTIFIER"""
    p[0] = p[1]

# OPERAÇÕES ELEMENTARES

def p_plus(p):
    """plus : PLUS"""
    p[0] = ['ADD']

def p_minus(p):
    """minus : MINUS"""
    p[0] = ['SUB']

def p_times(p):
    """times : TIMES"""
    p[0] = ['MUL']

def p_division(p):
    """division : DIVISION"""
    p[0] = ['DIV']

def p_writeln(p):
    """writeln : WRITELN LPAREN writeln_args RPAREN"""        
    p[0] = p[3] + ["WRITELN"] 
    
# FUNCOES

def p_function(p):
    """function : func_header SEMICOLON func_body SEMICOLON"""
    global vm_code, functions
    p[0] = [f'{p[1]}:'] + p[3]
    functions[p[1]] = (functions[p[1]][0], p[0])

def p_function_header(p):
    """func_header : FUNCTION IDENTIFIER LPAREN func_args RPAREN COLON type_name
                   | FUNCTION IDENTIFIER LPAREN RPAREN COLON type_name"""
    global variables, functions
    functions[p[2]] = ((p[4] if len(p) == 8 else []), [])
    variables[p[2]] = (p[7] if len(p) == 8 else p[6])
    p[0] = p[2]

def p_function_args(p):
    """func_args : func_arg COMMA func_args
                 | func_arg"""
    global variables
    variables[p[1][0]] = p[1][1]  # Associa à tabela de símbolos com seu tipo
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = p[1]

    
def p_func_arg(p):
    """func_arg : IDENTIFIER COLON type_name"""
    p[0] = (p[1], p[3])

def p_func_body(p):
    'func_body : BEGIN statements END'
    p[0] = p[2] + ["RETURN"]

def p_func_call(p):
    """func_call : IDENTIFIER LPAREN arg_list RPAREN"""
    p[0] = p[3] + [f'PUSHA {p[1]}', 'CALL']

def p_arg_list(p):
    """arg_list : IDENTIFIER COMMA arg_list
                | IDENTIFIER
                | """
    global functions, variables
    index_arg = list(variables.keys()).index(p[1])
    index_func_arg = list(variables.keys()).index(utils.get_nth_element_dict(functions, 0, 0)[0][0]) # Brute force partindo do princípio que apenas existe uma função definida e essa função só tem um argumento

    vm = [f'PUSHG {index_arg}'] + [f'STOREG {index_func_arg}']
    if len(p) == 4:
        p[0] = vm + p[3]
    elif len(p) == 2:
        p[0] = vm

# PROCEDURES

def p_procedure(p):
    pass

# WRITELN

def writeln_for_function(caller):
    writer = []
    index_arg = list(variables.keys()).index(utils.get_nth_element_dict(functions, 0, 1))
    push_instruction = caller + [f'PUSHG {index_arg}']
    var_type = variables[utils.get_nth_element_dict(functions, 0, 1)]
    if var_type == 'integer':
        writer = push_instruction + ["WRITEI"]
    elif var_type == 'real':
        writer = push_instruction + ["WRITEF"]
    elif var_type == 'string':
        writer = push_instruction + ["WRITES"]
    elif var_type == 'char':
        writer = push_instruction + ["WRITECHR"]
    elif var_type == 'boolean':
        writer = push_instruction + ["WRITES"]
    else:
        raise Exception(f"Erro: Tipo inválido.")
    
    return writer
    
def p_writeln_args(p):
    """writeln_args : type COMMA writeln_args 
                    | type"""
    global variables
    
    # Caso em que é um valor explicito, pode ser imediatamente escrito
    if isinstance(p[1], list):
        if "PUSHS" in p[1][0]:
            p[0] = p[1] + ["WRITES"]
        elif "PUSHI" in p[1][0]:
            p[0] = p[1] + ["WRITEI"]
        elif "PUSHF" in p[1][0]:
            p[0] = p[1] + ["WRITEF"]
        else: # Caso em que é uma função, vai dar write à variável onde o return foi colocado
            p[0] = writeln_for_function(p[1])
    # Caso em que é um identifier
    elif p[1] not in variables: # Pode ser um array ou função para o futuro. Para já apenas casos em que variáveis não declaradas são chamadas
        raise Exception(f"Erro: Variável '{p[1]}' não declarada.")
    else:
        var_type = variables[p[1]]
        index = list(variables.keys()).index(p[1])
        
        push_instruction = [f'PUSHG {index}']
        if var_type == 'integer':
            p[0] = push_instruction + ["WRITEI"]
        elif var_type == 'real':
            p[0] = push_instruction + ["WRITEF"]
        elif var_type == 'string':
            p[0] = push_instruction + ["WRITES"]
        elif var_type == 'char':
            p[0] = push_instruction + ["WRITECHR"]
        elif var_type == 'boolean':
            p[0] = push_instruction + ["WRITES"]
        else:
            raise Exception(f"Erro: Tipo inválido para a variável '{p[1]}'.")
    
    if len(p) == 4:
        p[0] += p[3]

def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo a '{p.value}' na linha {p.lineno}")
        parser.errok()
    else:
        print("Erro de sintaxe: token inesperado")
    
parser = yacc.yacc()

def parse_input(input_string):
    parser.parse(input_string)

    global vm_code
    vm_code += utils.print_funcs(functions)

    print(variables)
    print(variables_assigned)
    print(functions)

    return vm_code