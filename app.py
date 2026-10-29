import sqlite3
from datetime import datetime

def init_db(db_name="expenses.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

def add_expense(conn, amount, category, date=None):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)", (amount, category, date))
    conn.commit()
    return cursor.lastrowid

def fetch_expenses(conn, category=None, date=None):
    cursor = conn.cursor()
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if date:
        query += " AND date = ?"
        params.append(date)
    cursor.execute(query, params)
    return cursor.fetchall()

def get_total():
    pass
