from unittest.mock import MagicMock
import pytest
from expense_service import ExpenseService
from report_strategy import CategoryReportStrategy

def make_service():
    repository = MagicMock()
    return ExpenseService(repository), repository

def test_service_saves_valid_expense():
    service, repo = make_service()
    repo.save.return_value = 7
    assert service.add_expense(150, "Food", "2026-10-30", "Lunch") == 7
    repo.save.assert_called_once_with(150, "Food", "2026-10-30", "Lunch")

def test_invalid_expense_is_rejected_before_repository_call():
    service, repo = make_service()
    with pytest.raises(ValueError, match="Amount must be positive"):
        service.add_expense(-10, "Food", "2026-10-30", "Lunch")
    repo.save.assert_not_called()

def test_service_uses_selected_report_strategy():
    service, repo = make_service()
    repo.fetch_all.return_value = [
        (1, 100, "Food", "2026-10-30", "Lunch"),
        (2, 50, "Transport", "2026-10-30", "Bus")
    ]
    assert service.generate_report(CategoryReportStrategy()) == {
        "Food": 100.0, "Transport": 50.0
    }
    repo.fetch_all.assert_called_once()

def test_singleton_returns_same_manager_for_same_database(tmp_path):
    from database_manager import DatabaseManager
    path = str(tmp_path / "singleton.db")
    first = DatabaseManager.get_instance(path)
    second = DatabaseManager.get_instance(path)
    assert first is second
    first.close()
    DatabaseManager._instances.pop(path, None)


def test_repository_persists_and_updates_expense(tmp_path):
    from database_manager import DatabaseManager
    from expense_repository import ExpenseRepository
    path = str(tmp_path / "repository.db")
    manager = DatabaseManager.get_instance(path)
    repo = ExpenseRepository(manager)
    expense_id = repo.save(90, "Food", "2026-10-30", "Dinner")
    assert repo.fetch_all()[0][4] == "Dinner"
    assert repo.update(expense_id, 110, "Food", "2026-10-30", "Late dinner")
    assert repo.fetch_all()[0][1] == 110
    assert repo.delete(expense_id)
    assert repo.fetch_all() == []
    manager.close()
    DatabaseManager._instances.pop(path, None)


def test_service_rejects_empty_category():
    service, repository = make_service()
    with pytest.raises(ValueError, match="Category cannot be empty"):
        service.add_expense(10, " ", "2026-10-30")
    repository.save.assert_not_called()


def test_service_filters_by_month():
    service, repository = make_service()
    service.filter_by_month("2026-10")
    repository.fetch_by_month.assert_called_once_with("2026-10")
