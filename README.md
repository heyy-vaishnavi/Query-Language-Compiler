📌 Overview
This project is a custom SQL-like query language compiler built using Python, PLY (Python Lex-Yacc), and Pandas. It allows users to execute structured queries over .csv or .json files using a simple GUI.

⚙️ Features
🔎 SELECT with specific columns or *
📄 FROM CSV or JSON files
🧠 WHERE clause with conditions and logical operators (AND, OR)
📊 Aggregate functions: COUNT, SUM, AVG, MIN, MAX
📑 ORDER BY clause (with optional DESC support)
⏳ LIMIT clause
🧵 Query history tracking in GUI
📋 Copy and Save query results
✨ Syntax highlighting in the query box
✅ Subquery support in WHERE clause

🖥️ GUI Features
Simple and responsive interface using tkinter
Query input with syntax coloring
Buttons to:
  Run Query
  Show History
  Copy Result
  Save Result
Scrollable results display

🧰 Technologies Used
Python 3.x
PLY (Python Lex-Yacc)
Pandas
Tkinter (for GUI)

🛠️ How to Run
Clone the repo or download the source.

Install dependencies:
pip install pandas ply

Run the GUI:
python query_gui.py

🔄 Sample Queries
sql

SELECT * FROM data.csv

SELECT name, age FROM data.csv WHERE age > 30

SELECT AVG(salary) FROM employees.csv

SELECT name FROM employees.csv WHERE salary > (SELECT AVG(salary) FROM employees.csv)

SELECT name FROM students.json WHERE marks >= 90 ORDERBY name DESC LIMIT 5

✅ Coming Soon / Future Ideas
Support for GROUP BY and HAVING
Subqueries in SELECT and FROM clauses
JOIN support
Export results in JSON
Dark mode GUI theme