import ply.lex as lex

tokens = (
	# assignment
	'IDENTIFIER',
	'ASSIGNMENT',
	'SEMICOLON',
	'COLON',
	'COMMA',

	'COMMENT',

	# main
	'PROGRAM',
	'DOT',
	
	# blocks
	'VAR',
	'BEGIN',
	'END',
	
	# control flow
	'IF',
	'THEN',
	'ELSE',
	'FOR',
	'WHILE',
	'REPEAT',
	'UNTIL',
	'DO',
	'TO',
	'DOWNTO',
	
	# logic
	'AND',
	'OR',
	'NOT',
	
	# operations
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVISION',
	'DIV',
	'MOD',
    'RANGE',
	
	# comparations
	'EQ',
	'NEQ',
	'LT',
	'GT',
	'LTE',
	'GTE',
	
	# functions
	'LPAREN',
	'RPAREN',
 	'LBRACKET',
 	'RBRACKET',
	'PROCEDURE',
	'FUNCTION',
    'ARRAY',
    'OF',
    'WRITELN',
    'READLN',

	# types names
	'NREAL',
	'NINTEGER',
	'NSTRING',
	'NCHAR',
    'NBOOLEAN',
	
	# types
	'REAL',
	'INTEGER',
	'STRING', 
	'CHAR',   
    'BOOLEAN'
)

reserved_keywords = {
	'program':	'PROGRAM',
	'var':		'VAR',
	'begin':	'BEGIN',
	'end':		'END',
	
	'if':		'IF',
	'then':		'THEN',
	'else':		'ELSE',
	'for':		'FOR',
	'while':	'WHILE',
	'repeat':	'REPEAT',
	'do':		'DO',
	'to':		'TO',
	'downto':	'DOWNTO',
	'until':	'UNTIL',
	
	'and':		'AND',
	'or':		'OR',
	'not':		'NOT',
	
	'div':		'DIV',
	'mod':		'MOD',
	
	'procedure':'PROCEDURE',
	'function':	'FUNCTION',
    'array':    'ARRAY',
    'of':       'OF',
    'writeln':  'WRITELN',
    'readln':   'READLN',
	
	'real':		'NREAL',
	'integer':	'NINTEGER',
	'string':	'NSTRING',
	'char':	    'NCHAR',
    'boolean':	'NBOOLEAN'
}

t_DOT			= r"\."

t_ASSIGNMENT	= r":="
t_SEMICOLON		= r";"
t_COLON			= r":"
t_COMMA			= r","

t_PLUS			= r"\+"
t_MINUS			= r"\-"
t_TIMES			= r"\*"
t_DIVISION		= r"\/"
t_RANGE         = r"\.\."

t_EQ			= r"\="
t_NEQ			= r"\<\>"
t_LT			= r"\<"
t_GT			= r"\>"
t_LTE			= r"\<\="
t_GTE			= r"\>\="

t_LPAREN		= r"\("
t_RPAREN		= r"\)"
t_LBRACKET		= r"\["
t_RBRACKET		= r"\]"

t_REAL			= r"(\-)?[0-9]+\.[0-9]+"
t_INTEGER		= r"(\-)?[0-9]+"
t_BOOLEAN		= r"true|false"

def t_IDENTIFIER(t):
	r"[a-zA-Z]([a-zA-Z0-9])*"
	if t.value.lower() in reserved_keywords:
		t.type = reserved_keywords[t.value.lower()]
	return t

def t_CHAR(t):
    r"'\w'"
    t.value = t.value[1]  
    return t

def t_STRING(t):
    r"'([^']*)'"
    t.value = t.value[1:-1]
    return t

def t_COMMENT(t):
    r'\{.*?\}|\(\*.*?\*\)|\/\/.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Carácter desconhecido '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()