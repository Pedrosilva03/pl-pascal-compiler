import ply.yacc as yacc
from pascalLexer import tokens


def p_error(p):
    print("Erro sintático no input!")
    
parser = yacc.yacc()

def parse_input(data):
    return parser.parse(data)