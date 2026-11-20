"""Interactive terminal interface for ExpenseTracker."""
from datetime import datetime

from app import build_service
from database_manager import DatabaseManager
from report_strategy import MonthlyReportStrategy, CategoryReportStrategy


def read_amount(prompt="Amount: "):
    while True:
        raw = input(prompt).strip()
        try:
            amount = float(raw)
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return amount
        except ValueError:
            print("Please enter a valid number, e.g. 125 or 125.50.")


def read_date(prompt="Date (YYYY-MM-DD): "):
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, for example 2026-11-20.")


def read_id(prompt="Expense ID: "):
    while True:
        try:
            value = int(input(prompt).strip())
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a positive whole-number ID.")


def display_expenses(expenses):
    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n{:<5} {:>10}  {:<15} {:<12} {}".format(
        "ID", "AMOUNT", "CATEGORY", "DATE", "DESCRIPTION"))
    print("-" * 75)
    for expense_id, amount, category, date, description in expenses:
        print("{:<5} {:>10.2f}  {:<15} {:<12} {}".format(
            expense_id, amount, category, date, description or "-"))


def display_summary(title, summary):
    print(f"\n{title}")
    print("-" * len(title))
    if not summary:
        print("No data available.")
        return
    for label, total in summary.items():
        print(f"{label:<20} {total:>10.2f}")
    print("-" * 32)
    print(f"{'Total':<20} {sum(summary.values()):>10.2f}")


def run_menu(service):
    while True:
        print("\n========== EXPENSE TRACKER ==========")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Filter expenses")
        print("4. Update expense")
        print("5. Delete expense")
        print("6. Monthly report")
        print("7. Category-wise report")
        print("0. Exit")
        print("====================================")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                amount = read_amount()
                category = input("Category: ").strip()
                date = read_date()
                description = input("Description (optional): ").strip()
                expense_id = service.add_expense(
                    amount, category, date, description)
                print(f"Expense added successfully. ID: {expense_id}")

            elif choice == "2":
                display_expenses(service.list_expenses())

            elif choice == "3":
                print("\nFilter by: 1. Category  2. Exact date  3. Month")
                filter_choice = input("Choose filter: ").strip()
                if filter_choice == "1":
                    category = input("Category: ").strip()
                    display_expenses(service.filter_by_category(category))
                elif filter_choice == "2":
                    date = read_date()
                    matches = [row for row in service.list_expenses()
                               if row[3] == date]
                    display_expenses(matches)
                elif filter_choice == "3":
                    month = input("Month (YYYY-MM): ").strip()
                    display_expenses(service.filter_by_month(month))
                else:
                    print("Invalid filter option.")

            elif choice == "4":
                expense_id = read_id()
                print("Enter the complete updated expense details:")
                amount = read_amount()
                category = input("Category: ").strip()
                date = read_date()
                description = input("Description (optional): ").strip()
                updated = service.update_expense(
                    expense_id, amount, category, date, description)
                print("Expense updated successfully." if updated
                      else "No expense found with that ID.")

            elif choice == "5":
                expense_id = read_id()
                deleted = service.delete_expense(expense_id)
                print("Expense deleted successfully." if deleted
                      else "No expense found with that ID.")

            elif choice == "6":
                summary = service.generate_report(MonthlyReportStrategy())
                display_summary("MONTHLY SPENDING SUMMARY", summary)

            elif choice == "7":
                summary = service.generate_report(CategoryReportStrategy())
                display_summary("CATEGORY-WISE SPENDING SUMMARY", summary)

            elif choice == "0":
                print("Thank you for using ExpenseTracker.")
                break

            else:
                print("Invalid option. Please choose a listed option.")

        except (ValueError, TypeError) as error:
            print(f"Unable to complete operation: {error}")
        except Exception as error:
            # Keep the menu alive for an unexpected operation-level failure.
            print(f"An unexpected error occurred: {error}")


def main():
    service = build_service()
    try:
        run_menu(service)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting ExpenseTracker.")
    finally:
        DatabaseManager.get_instance().close()


if __name__ == "__main__":
    main()
