# ExpenseTracker

A lightweight Python and SQLite expense tracker for the CSE 3206 Software Engineering Sessional.

## Functional modules
- SQLite database initialization and connection management.
- Add expenses with amount, category, date, and description.
- List expenses and filter by category, exact date, or month.
- Update and delete expenses.
- Generate monthly and category-wise spending summaries.

## Design patterns
- **Singleton (creational):** `DatabaseManager` provides one manager per database path.
- **Repository (persistence abstraction):** `ExpenseRepository` encapsulates SQL operations.
- **Strategy (behavioral):** `ReportStrategy` supports monthly and category-wise reports.

## Files
- `app.py`: backward-compatible functions and service factory.
- `database_manager.py`: Singleton database manager.
- `expense_repository.py`: data access.
- `expense_service.py`: validation and business logic.
- `report_strategy.py`: interchangeable report calculations.
- `test_app.py`: SQLite-backed tests.
- `test_service.py`: `MagicMock`-based service tests.

## Run
```bash
python3 -m pip install -r requirements.txt
python3 -m pytest -v
python3 -m pytest --cov=. --cov-report=term-missing
python3 app.py
```

The current project is a Python service/application prototype. It does not include a browser interface or Selenium test. Do not claim Selenium was implemented unless you add and execute a browser-based test.

The default persistent database is `expenses.db`. Existing expense tables are migrated to add the `description` column. The original `init_db()` function remains available for tests and compatibility.
