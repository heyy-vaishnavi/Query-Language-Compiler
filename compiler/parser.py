import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('left', 'EQUALS'),
)

# Grammar rules
def p_query(p):
    '''query : SELECT select_list FROM IDENTIFIER where_clause orderby_clause limit_clause'''
    print("✅ Matched full query rule")
    p[0] = {
        'type': 'QUERY',
        'columns': p[2],
        'file': p[4],
        'where': p[5],
        'orderby': p[6],
        'limit': p[7]
    }

def p_column_list_multiple(p):
    '''column_list : column_list COMMA IDENTIFIER'''
    p[0] = p[1] + [p[3]]

def p_column_list_single(p):
    '''column_list : IDENTIFIER'''
    p[0] = [p[1]]

def p_where_clause(p):
    '''where_clause : WHERE condition
                    | '''
    p[0] = p[2] if len(p) > 1 else None

def p_select_list_all(p):
    '''select_list : ASTERISK'''
    p[0] = ['*']  # Indicates select all columns

def p_select_list_columns(p):
    '''select_list : column_list'''
    p[0] = p[1]

def p_select_list_agg_func(p):
    '''select_list : aggregate_function'''
    p[0] = [p[1]]

def p_aggregate_function(p):
    '''aggregate_function : COUNT LPAREN ASTERISK RPAREN
                          | COUNT LPAREN IDENTIFIER RPAREN
                          | SUM LPAREN IDENTIFIER RPAREN
                          | AVG LPAREN IDENTIFIER RPAREN
                          | MIN LPAREN IDENTIFIER RPAREN
                          | MAX LPAREN IDENTIFIER RPAREN'''
    p[0] = ('agg', p[1].lower(), p[3])  # e.g., ('agg', 'sum', 'age')

def p_condition_logic(p):
    '''condition : condition AND condition
                 | condition OR condition'''
    p[0] = ('logic', p[2].lower(), p[1], p[3])

def p_condition_comparison(p):
    '''condition : IDENTIFIER comparison_operator value'''
    p[0] = ('comparison', p[2], p[1], p[3])

def p_comparison_operator(p):
    '''comparison_operator : EQUALS
                           | NOTEQUALS
                           | LESSTHAN
                           | LESSEQUAL
                           | GREATERTHAN
                           | GREATEREQUAL'''
    p[0] = p[1]

def p_value(p):
    '''value : NUMBER
             | STRING
             | LPAREN query RPAREN'''
    p[0] = p[1] if len(p) == 2 else ('subquery', p[2])


def p_orderby_clause(p):
    '''orderby_clause : ORDERBY IDENTIFIER
                      | ORDERBY IDENTIFIER DESC
                      | '''
    if len(p) == 3:
        p[0] = (p[2], 'asc')
    elif len(p) == 4:
        p[0] = (p[2], 'desc')
    else:
        p[0] = None

def p_limit_clause(p):
    '''limit_clause : LIMIT NUMBER
                    | '''
    p[0] = p[2] if len(p) > 1 else None

def p_error(p):
    if p:
        print(f"❌ Syntax error at '{p.value}'")
    else:
        print("❌ Syntax error at end of input")

parser = yacc.yacc()
