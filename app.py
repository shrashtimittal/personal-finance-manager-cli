from database.db import initialize_database, backup_database, restore_database
from auth.auth import register_user, login_user
from transactions.transactions import (
    add_transaction,
    get_transactions,
    get_transactions_by_category,
    get_transactions_by_date_range,
    update_transaction,
    delete_transaction,
    get_deleted_transactions,
    restore_transaction,
    get_monthly_report,
    get_yearly_report,
    get_yearly_monthly_breakdown,
    get_category_summary,
    get_income_expense_summary,
    export_monthly_report_csv,
    export_yearly_report_csv,
    export_category_summary_csv,
    export_all_transactions_csv

)
from budgets.budgets import (
    set_budget,
    get_budgets,
    get_budget_status,
    delete_budget,
    get_budget_insights
)
from utils.logger import get_logger
from datetime import datetime
from colorama import Fore, Style, init
import os

init(autoreset=True)

logger = get_logger("app")

# ===============================
# UI / HELPER FUNCTIONS
# ===============================

def print_header(title: str):
    print(Fore.CYAN + f"\n{title}")
    print(Fore.CYAN + "-" * len(title))


def success(msg: str):
    print(Fore.GREEN + f"✔ {msg}")


def error(msg: str):
    print(Fore.RED + f"✖ {msg}")


def warning(msg: str):
    print(Fore.YELLOW + f"⚠ {msg}")


def print_no_data():
    warning("No financial data available for this period.")


def is_valid_date(date_str: str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_valid_amount():
    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            error("Amount must be greater than zero.")
            return None
        return amount
    except ValueError:
        error("Invalid amount. Please enter a number.")
        return None


def get_valid_category():
    category = input("Category: ").strip()
    if not category:
        error("Category cannot be empty.")
        return None
    return category


def show_transactions(transactions):
    print_header("Transactions")
    print("Transaction ID  Type     Category        Amount     Date")
    print("-" * 70)

    for txn_id, txn_type, category, amount, date in transactions:
        color = Fore.GREEN if txn_type == "income" else Fore.RED
        print(color + f"{txn_id:<14} {txn_type:<8} {category:<15} {amount:<10} {date}")

# ===============================
# USER DASHBOARD
# ===============================

def user_session(user_id):
    logger.info(f"User session started (user_id={user_id})")
    
    while True:
        print_header("Dashboard")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. View Transactions by Category")
        print("5. View Transactions by Date Range")
        print("6. Update Transaction")
        print("7. Delete Transaction")
        print("8. View Deleted Transactions")
        print("9. Restore Deleted Transaction")
        print("10. Monthly Report")
        print("11. Yearly Report")
        print("12. Yearly Monthly Breakdown")
        print("13. Category-wise Summary")
        print("14. Income vs Expense Summary")
        print("15. Set Monthly Budget")
        print("16. View Monthly Budgets")
        print("17. Check Budget Status")
        print("18. Delete Monthly Budget")
        print("19. Budget Insights & Recommendations")
        print("20. Backup Database")
        print("21. Restore Database")
        print("22. Logout")

        choice = input("Choose an option: ").strip()

        # 1 Add Income
        if choice == "1":
            category = get_valid_category()
            amount = get_valid_amount()
            if category and amount is not None:
                add_transaction(user_id, "income", category, amount)
                logger.info(f"Income added | user_id={user_id}, {category}, {amount}")
                success("Income added successfully.")

        # 2 Add Expense
        elif choice == "2":
            category = get_valid_category()
            amount = get_valid_amount()
            if category and amount is not None:
                add_transaction(user_id, "expense", category, amount)
                logger.info(f"Expense added | user_id={user_id}, {category}, {amount}")
                success("Expense added successfully.")

        # 3 View All Transactions
        elif choice == "3":
            transactions = get_transactions(user_id)
            if not transactions:
                print_no_data()
                continue

            show_transactions(transactions)

            export = input("Export all transactions to CSV? (y/n): ").lower()
            if export == "y":
                filename = export_all_transactions_csv(user_id, transactions)
                logger.info(f"Transactions exported | user_id={user_id} | {filename}")
                success(f"All transactions exported to {filename}")

        # 4 View by Category
        elif choice == "4":
            category = get_valid_category()
            if category:
                txns = get_transactions_by_category(user_id, category)
                show_transactions(txns) if txns else print_no_data()

        # 5 View by Date Range
        elif choice == "5":
            start = input("Start date (YYYY-MM-DD): ").strip()
            end = input("End date (YYYY-MM-DD): ").strip()
            if not is_valid_date(start) or not is_valid_date(end):
                error("Invalid date format.")
                continue
            txns = get_transactions_by_date_range(user_id, start, end)
            show_transactions(txns) if txns else print_no_data()

        # 6 Update Transaction
        elif choice == "6":
            txns = get_transactions(user_id)
            if not txns:
                print_no_data()
                continue
            show_transactions(txns)
            try:
                txn_id = int(input("Transaction ID to update: "))
            except ValueError:
                error("Invalid Transaction ID.")
                continue
            category = get_valid_category()
            amount = get_valid_amount()
            if category and amount is not None:
                if update_transaction(txn_id, user_id, category, amount):
                    logger.warning(f"Transaction updated | user_id={user_id}, txn_id={txn_id}")
                    success("Transaction updated.")
                else:
                    error("Transaction not found.")

        # 7 Delete Transaction
        elif choice == "7":
            txns = get_transactions(user_id)
            if not txns:
                print_no_data()
                continue
            show_transactions(txns)
            try:
                txn_id = int(input("Transaction ID to delete: "))
            except ValueError:
                error("Invalid Transaction ID.")
                continue
            if input("Are you sure? (y/n): ").lower() == "y":
                if delete_transaction(txn_id, user_id):
                    logger.warning(f"Transaction deleted | user_id={user_id}, txn_id={txn_id}")
                    success("Transaction deleted.")
                else:
                    error("Transaction not found.")

        # 8️ View Deleted Transactions
        elif choice == "8":
            deleted_txns = get_deleted_transactions(user_id)

            if not deleted_txns:
                warning("No deleted transactions found.")
                continue

            print_header("Deleted Transactions")
            show_transactions(deleted_txns)

        # 9️ Restore Deleted Transaction
        elif choice == "9":
            deleted_txns = get_deleted_transactions(user_id)

            if not deleted_txns:
                warning("No deleted transactions to restore.")
                continue

            print_header("Deleted Transactions")
            show_transactions(deleted_txns)

            try:
                txn_id = int(input("Enter Transaction ID to restore: "))
            except ValueError:
                error("Invalid Transaction ID.")
                continue

            if restore_transaction(txn_id, user_id):
                success("Transaction restored successfully.")
                logger.info(f"User {user_id} restored transaction {txn_id}")
            else:
                error("Transaction not found or already active.")
                logger.warning(f"User {user_id} failed to restore transaction {txn_id}")

        # 10 Monthly Report
        elif choice == "10":
            try:
                year = int(input("Year (YYYY): "))
                month = int(input("Month (1-12): "))
            except ValueError:
                error("Invalid year or month.")
                continue

            income, expense, savings = get_monthly_report(user_id, year, month)

            print_header("Monthly Report")
            if income == 0 and expense == 0:
                print_no_data()
            else:
                print(f"Income : {Fore.GREEN}{income}")
                print(f"Expense: {Fore.RED}{expense}")
                print(f"Savings: {Fore.CYAN}{savings}")

                export = input("Export this report to CSV? (y/n): ").lower()
                if export == "y":
                    filename = export_monthly_report_csv(
                        user_id, year, month, income, expense, savings
                    )
                    logger.info(f"Monthly report exported | {file}")
                    success(f"Monthly report exported to {filename}")

        # 11 Yearly Report
        elif choice == "11":
            try:
                year = int(input("Year (YYYY): "))
            except ValueError:
                error("Invalid year.")
                continue

            income, expense, savings = get_yearly_report(user_id, year)

            print_header("Yearly Report")
            if income == 0 and expense == 0:
                print_no_data()
            else:
                print(f"Income : {Fore.GREEN}{income}")
                print(f"Expense: {Fore.RED}{expense}")
                print(f"Savings: {Fore.CYAN}{savings}")

                export = input("Export this report to CSV? (y/n): ").lower()
                if export == "y":
                    filename = export_yearly_report_csv(
                        user_id, year, income, expense, savings
                    )
                    logger.info(f"Yearly report exported | {file}")
                    success(f"Yearly report exported to {filename}")

        # 12 Yearly Monthly Breakdown
        elif choice == "12":
            year = int(input("Year (YYYY): "))
            breakdown = get_yearly_monthly_breakdown(user_id, year)
            if not breakdown:
                print_no_data()
                continue
            print_header(f"Monthly Breakdown {year}")
            for m, d in breakdown.items():
                print(f"{m} → Income: {d['income']} | Expense: {d['expense']} | Savings: {d['savings']}")

        # 13 Category Summary
        elif choice == "13":
            summary = get_category_summary(user_id)
            if not summary:
                print_no_data()
                continue

            print_header("Category-wise Summary")
            for category, data in summary.items():
                print(f"{category:<15} Income: {data['income']}  Expense: {data['expense']}")

            export = input("Export this summary to CSV? (y/n): ").lower()
            if export == "y":
                filename = export_category_summary_csv(user_id, summary)
                success(f"Category summary exported to {filename}")
          
        # 14 Income vs Expense
        elif choice == "14":
            income, expense, savings = get_income_expense_summary(user_id)
            print_header("Income vs Expense")
            print(f"Income : {Fore.GREEN}{income}")
            print(f"Expense: {Fore.RED}{expense}")
            print(f"Savings: {Fore.CYAN}{savings}")

        # 15 Set Monthly Budget
        elif choice == "15":
            category = get_valid_category()
            if not category:
                continue
            try:
                month = int(input("Month (1-12): "))
                year = int(input("Year (YYYY): "))
            except ValueError:
                error("Invalid month or year.")
                continue
            amount = get_valid_amount()
            if amount is not None:
                set_budget(user_id, category, month, year, amount)
                success("Budget set successfully.")

        # 16 View Monthly Budgets
        elif choice == "16":
            try:
                month = int(input("Month (1-12): "))
                year = int(input("Year (YYYY): "))
            except ValueError:
                error("Invalid month or year.")
                continue
            budgets = get_budgets(user_id, month, year)
            if not budgets:
                print_no_data()
                continue
            print_header(f"Budgets for {year}-{month:02d}")
            for category, amount in budgets:
                print(f"{category:<15} Budget: {amount}")

        # 17 Check Budget Status
        elif choice == "17":
            try:
                month = int(input("Month (1-12): "))
                year = int(input("Year (YYYY): "))
            except ValueError:
                error("Invalid month or year.")
                continue
            status = get_budget_status(user_id, month, year)
            if not status:
                print_no_data()
                continue
            print_header("Budget Status")
            for category, budget, spent in status:
                state = "OVER BUDGET" if spent > budget else "OK"
                color = Fore.RED if spent > budget else Fore.GREEN
                print(color + f"{category:<15} Budget: {budget} Spent: {spent} Status: {state}")

        # 18 Delete Monthly Budget
        elif choice == "18":
            try:
                month = int(input("Month (1-12): "))
                year = int(input("Year (YYYY): "))
            except ValueError:
                error("Invalid month or year.")
                continue
            category = input("Category to delete: ").strip()
            if delete_budget(user_id, category, month, year):
                success("Budget deleted successfully.")
            else:
                error("Budget not found.")

        # 19 Budget Insights & Recommendations
        elif choice == "19":
            try:
                month = int(input("Month (1-12): "))
                year = int(input("Year (YYYY): "))
            except ValueError:
                error("Invalid month or year.")
                continue
            insights = get_budget_insights(user_id, month, year)
            if not insights:
                print_no_data()
                continue
            print_header("Budget Insights & Recommendations")
            for item in insights:
                print(
                    f"{item['category']:<15} "
                    f"{item['status']:<12} "
                    f"{item['suggestion']}"
                )

        # 20 Backup Database
        elif choice == "20":
            backup_database()
            logger.warning("Database backup created")
            success("Database backup completed.")

        # 21 Restore Database
        elif choice == "21":
            backup_dir = os.path.join("data", "backups")
            backups = os.listdir(backup_dir) if os.path.exists(backup_dir) else []
            if not backups:
                error("No backups available.")
                continue
            print_header("Available Backups")
            for i, file in enumerate(backups, 1):
                print(f"{i}. {file}")
            index = int(input("Select backup number: ")) - 1
            restore_database(backups[index])
            logger.warning(f"Database restored from {backups[index]}")
            success("Database restored successfully.")


        elif choice == "22":
            logger.info(f"User logged out (user_id={user_id})")
            success("Logged out.")
            break

        else:
            error("Invalid option. Please try again.")

# ===============================
# APPLICATION ENTRY POINT
# ===============================

def main():
    logger.info("Application started")
    while True:
        print_header("Personal Finance Manager")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            if register_user(username, password):
                logger.info(f"User registered | {username}")
                success("User registered.")
            else:
                error("Username already exists.")

        elif choice == "2":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user_id = login_user(username, password)
            if user_id:
                logger.info(f"User logged in | user_id={user_id}")
                success("Login successful.")
                user_session(user_id)
            else:
                error("Invalid credentials.")

        elif choice == "3":
            logger.info("Application exited")
            print("Goodbye!")
            break

        else:
            error("Invalid option.")

if __name__ == "__main__":
    initialize_database()
    main()
