import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compiler')))

from lexer import lexer
from parser import parser

def parse_query(query):
    lexer.input(query)
    result = parser.parse(query)
    return result

# Test the parser
query = 'SELECT name, age FROM data.csv WHERE age >= 25 AND city != "New York" ORDERBY name LIMIT 5'
result = parse_query(query)

print("Parsed Query:")
print(result)
