import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import pandas as pd

# Include the compiler directory in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'compiler')))

from parser import parser
from lexer import lexer
from codegen import execute_query

query_history = []

def run_query():
    query = query_entry.get("1.0", tk.END).strip()
    if not query:
        messagebox.showwarning("Empty Query", "Please enter a query to run.")
        return

    try:
        lexer.input(query)
        parsed = parser.parse(query)
        if not parsed:
            messagebox.showerror("Syntax Error", "Query parsing failed.")
            return
        result = execute_query(parsed)
        query_history.append(query)
        display_result(result)
    except Exception as e:
        messagebox.showerror("Execution Error", f"Error: {str(e)}")

def show_history():
    if not query_history:
        messagebox.showinfo("Query History", "No queries executed yet.")
        return

    history_window = tk.Toplevel(root)
    history_window.title("Query History")
    history_window.geometry("600x400")
    history_window.configure(bg="#ffffff")

    tk.Label(history_window, text="Executed Queries", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

    history_listbox = tk.Listbox(history_window, font=("Courier", 10), width=80, height=20)
    history_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    for idx, q in enumerate(query_history, 1):
        history_listbox.insert(tk.END, f"{idx}. {q}")

def display_result(df):
    for widget in result_frame.winfo_children():
        widget.destroy()

    result_frame.df = df

    if df.empty:
        tk.Label(result_frame, text="No results found.", font=("Arial", 12)).pack()
        return

    count_label = tk.Label(result_frame, text=f"{len(df)} row(s) returned.", font=("Arial", 10, "italic"))
    count_label.pack(anchor="w", padx=5)

    tree_scroll = tk.Scrollbar(result_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(result_frame, yscrollcommand=tree_scroll.set)
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(fill=tk.BOTH, expand=True)
    tree_scroll.config(command=tree.yview)

def copy_results():
    try:
        df = result_frame.df
        root.clipboard_clear()
        root.clipboard_append(df.to_string(index=False))
        root.update()
        messagebox.showinfo("Copied", "Results copied to clipboard.")
    except:
        messagebox.showwarning("No Data", "Nothing to copy.")

def save_results():
    try:
        df = result_frame.df
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Saved", f"Results saved to {file_path}")
    except:
        messagebox.showwarning("No Data", "Nothing to save.")

def highlight_query(event=None):
    keywords = ['SELECT', 'FROM', 'WHERE', 'AND', 'OR']
    query_entry.tag_remove("keyword", "1.0", tk.END)
    for keyword in keywords:
        start = "1.0"
        while True:
            pos = query_entry.search(keyword, start, tk.END, nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(keyword)}c"
            query_entry.tag_add("keyword", pos, end)
            start = end
    query_entry.tag_config("keyword", foreground="#1a73e8", font=("Courier", 10, "bold"))

# GUI Setup
root = tk.Tk()
root.title("Query Language Compiler")
root.geometry("880x680")
root.configure(bg="#fafafa")

title = tk.Label(root, text="Query Language Compiler", font=("Helvetica", 18, "bold"), bg="#fafafa", fg="#333")
title.pack(pady=15)

query_label = tk.Label(root, text="Enter your query:", font=("Arial", 12), bg="#fafafa")
query_label.pack()

query_entry = tk.Text(root, height=4, width=100, font=("Courier", 10))
query_entry.pack(pady=6)
query_entry.bind("<KeyRelease>", highlight_query)

# Button Row
button_frame = tk.Frame(root, bg="#fafafa")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Run Query", command=run_query, font=("Arial", 11), bg="#4CAF50", fg="white", padx=10).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Show History", command=show_history, font=("Arial", 11), bg="#2196F3", fg="white", padx=10).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Copy Result", command=copy_results, font=("Arial", 11), bg="#FFC107", padx=10).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Save Result", command=save_results, font=("Arial", 11), bg="#FF5722", fg="white", padx=10).pack(side=tk.LEFT, padx=5)

result_label = tk.Label(root, text="Query Results:", font=("Arial", 12, "bold"), bg="#fafafa", anchor="w")
result_label.pack(anchor="w", padx=15, pady=(10, 0))

result_frame = tk.Frame(root)
result_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

# Treeview style
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
style.configure("Treeview", font=("Courier", 10), rowheight=25)

# Shortcuts
root.bind("<Control-Return>", lambda event: run_query())
root.bind("<Control-h>", lambda event: show_history())

root.mainloop()
