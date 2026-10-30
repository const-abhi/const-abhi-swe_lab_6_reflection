import pytest
from app import init_db, add_expense, fetch_expenses, update_expense, delete_expense, monthly_summary, category_summary

@pytest.fixture
def db_conn():
    conn = init_db(":memory:")
    yield conn
    conn.close()

def test_add_and_fetch_expense(db_conn):
    add_expense(db_conn, 50.0, "Food", "2026-10-30", "Lunch")
    rows = fetch_expenses(db_conn)
    assert len(rows) == 1
    assert rows[0][1] == 50.0 and rows[0][2] == "Food" and rows[0][4] == "Lunch"

def test_add_expense_invalid_amount(db_conn):
    with pytest.raises(ValueError, match="Amount must be positive"):
        add_expense(db_conn, -10.0, "Food")

def test_fetch_expenses_by_category(db_conn):
    add_expense(db_conn, 20.0, "Transport")
    add_expense(db_conn, 30.0, "Food")
    assert len(fetch_expenses(db_conn, category="Food")) == 1

def test_fetch_expenses_by_date(db_conn):
    add_expense(db_conn, 100.0, "Rent", "2026-10-01")
    add_expense(db_conn, 50.0, "Utilities", "2026-10-15")
    assert len(fetch_expenses(db_conn, date="2026-10-01")) == 1

def test_filter_by_month(db_conn):
    add_expense(db_conn, 100, "Food", "2026-10-01")
    add_expense(db_conn, 50, "Food", "2026-11-01")
    assert len(fetch_expenses(db_conn, month="2026-10")) == 1

def test_update_expense(db_conn):
    eid = add_expense(db_conn, 100, "Food", "2026-10-01", "Lunch")
    assert update_expense(db_conn, eid, amount=125, description="Dinner")
    assert fetch_expenses(db_conn)[0][1] == 125
    assert fetch_expenses(db_conn)[0][4] == "Dinner"

def test_delete_expense(db_conn):
    eid = add_expense(db_conn, 100, "Food")
    assert delete_expense(db_conn, eid)
    assert fetch_expenses(db_conn) == []

def test_monthly_summary(db_conn):
    add_expense(db_conn, 100, "Food", "2026-10-01")
    add_expense(db_conn, 50, "Transport", "2026-10-02")
    add_expense(db_conn, 20, "Food", "2026-11-01")
    assert monthly_summary(fetch_expenses(db_conn)) == {"2026-10": 150.0, "2026-11": 20.0}

def test_category_summary(db_conn):
    add_expense(db_conn, 100, "Food")
    add_expense(db_conn, 50, "Transport")
    add_expense(db_conn, 25, "Food")
    assert category_summary(fetch_expenses(db_conn)) == {"Food": 125.0, "Transport": 50.0}
