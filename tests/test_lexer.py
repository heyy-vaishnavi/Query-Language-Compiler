import sys
import os

# Add the compiler directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compiler')))

from lexer import lexer  # Now you can import the lexer properly

# Test query
query = 'SELECT name, age FROM data.csv WHERE age = 25 ORDERBY name LIMIT 10'

lexer.input(query)

print("Tokens:")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
