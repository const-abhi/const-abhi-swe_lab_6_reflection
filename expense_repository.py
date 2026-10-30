"""Repository pattern: isolates SQL persistence from business logic."""
class ExpenseRepository:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    @property
    def connection(self):
        return self.database_manager.get_connection()

    def save(self, amount, category, date, description=""):
        cursor = self.connection.execute(
            "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
            (float(amount), category, date, description))
        self.connection.commit()
        return cursor.lastrowid

    def fetch_all(self):
        return self.connection.execute(
            "SELECT id, amount, category, date, description FROM expenses ORDER BY date, id"
        ).fetchall()

    def fetch_by_category(self, category):
        return self.connection.execute(
            "SELECT id, amount, category, date, description FROM expenses WHERE category=? ORDER BY date, id",
            (category,)).fetchall()

    def fetch_by_month(self, month):
        return self.connection.execute(
            "SELECT id, amount, category, date, description FROM expenses WHERE substr(date,1,7)=? ORDER BY date, id",
            (month,)).fetchall()

    def update(self, expense_id, amount, category, date, description):
        cursor = self.connection.execute(
            "UPDATE expenses SET amount=?, category=?, date=?, description=? WHERE id=?",
            (float(amount), category, date, description, expense_id))
        self.connection.commit()
        return cursor.rowcount > 0

    def delete(self, expense_id):
        cursor = self.connection.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        self.connection.commit()
        return cursor.rowcount > 0
