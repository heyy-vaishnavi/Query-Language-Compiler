import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compiler')))
from lexer import lexer

query = 'SELECT name, age FROM data.csv WHERE age = 25 ORDERBY name LIMIT 10'
lexer.input(query)

print("Tokens:")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
