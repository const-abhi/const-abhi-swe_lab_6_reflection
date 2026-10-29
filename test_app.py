import pytest
import sqlite3
from app import init_db, add_expense, fetch_expenses

@pytest.fixture
def db_conn():
    # Use in-memory database for testing
    conn = init_db(":memory:")
    yield conn
    conn.close()

def test_add_and_fetch_expense(db_conn):
    add_expense(db_conn, 50.0, "Food", "2026-10-30")
    expenses = fetch_expenses(db_conn)
    assert len(expenses) == 1
    assert expenses[0][1] == 50.0
    assert expenses[0][2] == "Food"

def test_add_expense_invalid_amount(db_conn):
    with pytest.raises(ValueError, match="Amount must be positive"):
        add_expense(db_conn, -10.0, "Food")

def test_fetch_expenses_by_category(db_conn):
    add_expense(db_conn, 20.0, "Transport")
    add_expense(db_conn, 30.0, "Food")
    expenses = fetch_expenses(db_conn, category="Food")
    assert len(expenses) == 1
    assert expenses[0][2] == "Food"

def test_fetch_expenses_by_date(db_conn):
    add_expense(db_conn, 100.0, "Rent", "2026-10-01")
    add_expense(db_conn, 50.0, "Utilities", "2026-10-15")
    expenses = fetch_expenses(db_conn, date="2026-10-01")
    assert len(expenses) == 1
    assert expenses[0][2] == "Rent"
