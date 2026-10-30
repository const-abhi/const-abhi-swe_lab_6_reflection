import sqlite3
from datetime import datetime
from database_manager import DatabaseManager
from expense_repository import ExpenseRepository
from expense_service import ExpenseService
from report_strategy import MonthlyReportStrategy, CategoryReportStrategy


def init_db(db_name="expenses.db"):
    """Initialize a SQLite database and return its connection.

    Existing databases are migrated by adding the optional description column.
    The original API is preserved for compatibility with the initial tests.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT ''
        )
    """)
    columns = {row[1] for row in cursor.execute("PRAGMA table_info(expenses)")}
    if "description" not in columns:
        cursor.execute("ALTER TABLE expenses ADD COLUMN description TEXT NOT NULL DEFAULT ''")
    conn.commit()
    return conn


def add_expense(conn, amount, category, date=None, description=""):
    if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("Amount must be positive")
    if not isinstance(category, str) or not category.strip():
        raise ValueError("Category cannot be empty")
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError("Date must use YYYY-MM-DD format")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
        (float(amount), category.strip(), date, (description or "").strip())
    )
    conn.commit()
    return cursor.lastrowid


def fetch_expenses(conn, category=None, date=None, month=None):
    """Return rows as (id, amount, category, date, description)."""
    query = "SELECT id, amount, category, date, description FROM expenses WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if date:
        query += " AND date = ?"
        params.append(date)
    if month:
        if len(month) != 7 or month[4] != "-":
            raise ValueError("Month must use YYYY-MM format")
        query += " AND substr(date, 1, 7) = ?"
        params.append(month)
    query += " ORDER BY date, id"
    return conn.execute(query, params).fetchall()


def update_expense(conn, expense_id, amount=None, category=None, date=None, description=None):
    current = conn.execute(
        "SELECT amount, category, date, description FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()
    if current is None:
        return False
    values = [
        current[0] if amount is None else amount,
        current[1] if category is None else category,
        current[2] if date is None else date,
        current[3] if description is None else description
    ]
    if isinstance(values[0], bool) or not isinstance(values[0], (int, float)) or values[0] <= 0:
        raise ValueError("Amount must be positive")
    if not isinstance(values[1], str) or not values[1].strip():
        raise ValueError("Category cannot be empty")
    try:
        datetime.strptime(values[2], "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError("Date must use YYYY-MM-DD format")
    conn.execute(
        "UPDATE expenses SET amount=?, category=?, date=?, description=? WHERE id=?",
        (float(values[0]), values[1].strip(), values[2], (values[3] or "").strip(), expense_id)
    )
    conn.commit()
    return True


def delete_expense(conn, expense_id):
    cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    return cursor.rowcount > 0


def monthly_summary(expenses):
    return MonthlyReportStrategy().generate(expenses)


def category_summary(expenses):
    return CategoryReportStrategy().generate(expenses)


def build_service(db_name="expenses.db"):
    """Construct the pattern-based service layer for application use."""
    manager = DatabaseManager.get_instance(db_name)
    return ExpenseService(ExpenseRepository(manager))


if __name__ == "__main__":
    connection = init_db()
    print("ExpenseTracker database initialized.")
    print("Use the functions in app.py or ExpenseService to manage expenses.")
    connection.close()
