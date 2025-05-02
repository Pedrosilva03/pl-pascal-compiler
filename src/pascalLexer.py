import ply.lex as lex

tokens = (
	# Assignment
	'IDENTIFIER', 'ASSIGNMENT', 'SEMICOLON', 'COLON', 'COMMA',
	# Main
    'COMMENT', 'PROGRAM', 'DOT',
	# Blocks
	'VAR', 'BEGIN', 'END',
	# Control Flow
	'IF', 'THEN', 'ELSE', 'FOR', 'WHILE', 'REPEAT', 'UNTIL', 'DO', 'TO', 'DOWNTO',
	# Logic
	'AND', 'OR', 'NOT',
	# Operations
	'PLUS', 'MINUS', 'TIMES', 'DIVISION', 'DIV', 'MOD', 'RANGE',
	# Comparations
	'EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE',
	# Functions
	'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'PROCEDURE', 'FUNCTION', 'ARRAY', 'OF', 'WRITELN', 'READLN', 'LENGTH',
	# Types Names
	'NREAL', 'NINTEGER', 'NSTRING', 'NCHAR', 'NBOOLEAN',
	# Types
	'REAL', 'INTEGER', 'STRING', 'CHAR', 'BOOLEAN'
)

t_DOT = r"\."
t_ASSIGNMENT = r":="
t_SEMICOLON = r";"
t_COLON = r":"
t_COMMA	= r","

t_PLUS = r"\+"
t_MINUS = r"\-"
t_TIMES	= r"\*"
t_DIVISION = r"\/"
t_RANGE = r"\.\."

t_EQ = r"\="
t_NEQ = r"\<\>"
t_LT = r"\<"
t_GT = r"\>"
t_LTE = r"\<\="
t_GTE = r"\>\="

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"

def t_PROGRAM(t): r"[Pp][Rr][Oo][Gg][Rr][Aa][Mm]"; return t

def t_VAR(t): r"[Vv][Aa][Rr]"; return t

def t_BEGIN(t): r"[Bb][Ee][Gg][Ii][Nn]"; return t

def t_END(t): r"[Ee][Nn][Dd]"; return t

def t_IF(t): r"[Ii][Ff]"; return t

def t_THEN(t): r"[Tt][Hh][Ee][Nn]"; return t

def t_ELSE(t): r"[Ee][Ll][Ss][Ee]"; return t

def t_FOR(t): r"[Ff][Oo][Rr]"; return t

def t_WHILE(t): r"[Ww][Hh][Ii][Ll][Ee]"; return t

def t_REPEAT(t): r"[Rr][Ee][Pp][Ee][Aa][Tt]"; return t

def t_DOWNTO(t): r"[Dd][Oo][Ww][Nn][Tt][Oo]"; return t

def t_DO(t): r"[Dd][Oo]"; return t

def t_TO(t): r"[Tt][Oo]"; return t

def t_UNTIL(t): r"[Uu][Nn][Tt][Ii][Ll]"; return t

def t_AND(t): r"[Aa][Nn][Dd]"; return t

def t_OR(t): r"[Oo][Rr]"; return t

def t_NOT(t): r"[Nn][Oo][Tt]"; return t

def t_DIV(t): r"[Dd][Ii][Vv]"; return t

def t_MOD(t): r"[Mm][Oo][Dd]"; return t

def t_PROCEDURE(t): r"[Pp][Rr][Oo][Cc][Ee][Dd][Uu][Rr][Ee]"; return t

def t_FUNCTION(t): r"[Ff][Uu][Nn][Cc][Tt][Ii][Oo][Nn]"; return t

def t_ARRAY(t): r"[Aa][Rr][Rr][Aa][Yy]"; return t

def t_OF(t): r"[Oo][Ff]"; return t

def t_WRITELN(t): r"[Ww][Rr][Ii][Tt][Ee][Ll][Nn]"; return t

def t_READLN(t): r"[Rr][Ee][Aa][Dd][Ll][Nn]"; return t

def t_LENGTH(t): r"[Ll][Ee][Nn][Gg][Tt][Hh]"; return t

def t_NREAL(t): r"[Rr][Ee][Aa][Ll]"; return t

def t_NINTEGER(t): r"[Ii][Nn][Tt][Ee][Gg][Ee][Rr]"; return t

def t_NSTRING(t): r"[Ss][Tt][Rr][Ii][Nn][Gg]"; return t

def t_NCHAR(t): r"[Cc][Hh][Aa][Rr]"; return t

def t_NBOOLEAN(t): r"[Bb][Oo][Oo][Ll][Ee][Aa][Nn]"; return t

def t_BOOLEAN(t): r"[Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee]"; return t
    
def t_REAL(t): r"(\-)?\d+\.\d+"; t.value = float(t.value) ; return t

def t_INTEGER(t): r"(\-)?\d+"; t.value = int(t.value); return t

def t_STRING(t): r"'([^']*)'"; t.value = t.value[1:-1]; return t

def t_IDENTIFIER(t): r"[a-zA-Z]([a-zA-Z0-9])*"; return t

def t_CHAR(t): r"'\w'"; t.value = t.value[1]; return t

def t_COMMENT(t): r'\{.*?\}|\(\*.*?\*\)|\/\/.*'; pass

def t_newline(t): r'\n+'; t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"CarÃ¡cter desconhecido '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()