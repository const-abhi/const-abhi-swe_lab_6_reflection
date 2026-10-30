"""Business rules separated from database operations."""
from datetime import datetime


class ExpenseService:
    def __init__(self, repository):
        self.repository = repository

    @staticmethod
    def _validate(amount, category, date, description=""):
        if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be positive")
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Category cannot be empty")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except (TypeError, ValueError):
            raise ValueError("Date must use YYYY-MM-DD format")
        if description is not None and not isinstance(description, str):
            raise ValueError("Description must be text")

    def add_expense(self, amount, category, date, description=""):
        self._validate(amount, category, date, description)
        return self.repository.save(amount, category.strip(), date, (description or "").strip())

    def list_expenses(self):
        return self.repository.fetch_all()

    def filter_by_category(self, category):
        if not category or not category.strip():
            raise ValueError("Category cannot be empty")
        return self.repository.fetch_by_category(category.strip())

    def filter_by_month(self, month):
        try:
            datetime.strptime(month + "-01", "%Y-%m-%d")
        except (TypeError, ValueError):
            raise ValueError("Month must use YYYY-MM format")
        return self.repository.fetch_by_month(month)

    def update_expense(self, expense_id, amount, category, date, description=""):
        self._validate(amount, category, date, description)
        return self.repository.update(
            expense_id, amount, category.strip(), date, (description or "").strip())

    def delete_expense(self, expense_id):
        return self.repository.delete(expense_id)

    def generate_report(self, strategy, expenses=None):
        if expenses is None:
            expenses = self.repository.fetch_all()
        return strategy.generate(expenses)
