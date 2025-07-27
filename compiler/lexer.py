import ply.lex as lex

tokens = (
    'SELECT', 'FROM', 'WHERE', 'ORDERBY', 'LIMIT',
    'AND', 'OR', 'DESC',
    'COUNT', 'SUM', 'AVG', 'MIN', 'MAX',
    'IDENTIFIER', 'COMMA', 'ASTERISK',
    'EQUALS', 'NOTEQUALS', 'LESSTHAN', 'LESSEQUAL', 'GREATERTHAN', 'GREATEREQUAL',
    'NUMBER', 'STRING',
    'LPAREN', 'RPAREN' 
)

# Add regex for new tokens
t_EQUALS = r'='
t_NOTEQUALS = r'!='
t_LESSTHAN = r'<'
t_LESSEQUAL = r'<='
t_GREATERTHAN = r'>'
t_GREATEREQUAL = r'>='
t_COMMA         = r','
t_ASTERISK = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'

keywords = {
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'orderby': 'ORDERBY',
    'limit': 'LIMIT',
    'and': 'AND',
    'or': 'OR',
    'desc': 'DESC',
    'count': 'COUNT',
    'sum': 'SUM',
    'avg': 'AVG',
    'min': 'MIN',
    'max': 'MAX'
}

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_ORDERBY(t):
    r'ORDER\s*BY|ORDERBY'
    t.type = 'ORDERBY'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*'
    t.type = keywords.get(t.value.lower(), 'IDENTIFIER')
    return t


def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]  # Remove quotation marks
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
