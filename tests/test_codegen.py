import sys
import os

# Include the compiler folder in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compiler')))

from parser import parser
from lexer import lexer
from codegen import execute_query

def run_query(query):
    lexer.input(query)
    parsed = parser.parse(query)
    print("Parsed Query:", parsed)
    result = execute_query(parsed)
    print("\nQuery Result:")
    print(result)

# Prompt user for query input
if __name__ == "__main__":
    print("🔎 Enter your custom query (type 'exit' to quit):")
    while True:
        user_query = input(">> ")
        if user_query.lower() in ['exit', 'quit']:
            print("👋 Exiting...")
            break
        try:
            run_query(user_query)
        except Exception as e:
            print(f"❌ Error: {e}")
