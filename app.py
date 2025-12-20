from database.db import initialize_database
from auth.auth import register_user, login_user
from transactions.transactions import (
    add_transaction,
    get_transactions,
    get_transactions_by_category,
    get_transactions_by_date_range,
    update_transaction,
    delete_transaction,
    get_monthly_report,
    get_yearly_report,
    get_yearly_monthly_breakdown,
    get_category_summary,
    get_income_expense_summary
)
from datetime import datetime
from budgets.budgets import (
    set_budget,
    get_budgets,
    get_budget_status,
    delete_budget,
    get_budget_insights
)

# ===============================
# HELPER FUNCTIONS
# ===============================

def print_no_data():
    print("No financial data available for this period.")


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_valid_amount():
    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return None
        return amount
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return None


def get_valid_category():
    category = input("Category: ").strip()
    if not category:
        print("Category cannot be empty.")
        return None
    return category


def show_transactions(transactions):
    print("\nID   Type     Category        Amount     Date")
    print("-" * 55)
    for txn_id, txn_type, category, amount, date in transactions:
        print(f"{txn_id:<4} {txn_type:<8} {category:<15} {amount:<10} {date}")


# ===============================
# USER DASHBOARD
# ===============================

def user_session(user_id):
    while True:
        print("\n--- Dashboard ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. View Transactions by Category")
        print("5. View Transactions by Date Range")
        print("6. Update Transaction")
        print("7. Delete Transaction")
        print("8. Monthly Report")
        print("9. Yearly Report")
        print("10. Yearly Monthly Breakdown")
        print("11. Category-wise Summary")
        print("12. Income vs Expense Summary")
        print("13. Set Monthly Budget")
        print("14. View Monthly Budgets")
        print("15. Check Budget Status")
        print("16. Delete Monthly Budget")
        print("17. Budget Insights & Recommendations")   
        print("18. Logout")

        choice = input("Choose an option: ")

        # Add Income
        if choice == "1":
            category = get_valid_category()
            amount = get_valid_amount()
            if category and amount is not None:
                add_transaction(user_id, "income", category, amount)
                print("Income added successfully!")

        # Add Expense
        elif choice == "2":
            category = get_valid_category()
            amount = get_valid_amount()
            if category and amount is not None:
                add_transaction(user_id, "expense", category, amount)
                print("Expense added successfully!")

        # View All Transactions
        elif choice == "3":
            transactions = get_transactions(user_id)
            if transactions:
                show_transactions(transactions)
            else:
                print_no_data()

        # View by Category
        elif choice == "4":
            category = get_valid_category()
            if not category:
                continue

            transactions = get_transactions_by_category(user_id, category)
            if transactions:
                show_transactions(transactions)
            else:
                print_no_data()

        # View by Date Range
        elif choice == "5":
            start_date = input("Start date (YYYY-MM-DD): ").strip()
            end_date = input("End date (YYYY-MM-DD): ").strip()

            if not is_valid_date(start_date) or not is_valid_date(end_date):
                print("Invalid date format.")
                continue

            transactions = get_transactions_by_date_range(user_id, start_date, end_date)
            if transactions:
                show_transactions(transactions)
            else:
                print_no_data()

        # Update Transaction
        elif choice == "6":
            transactions = get_transactions(user_id)
            if not transactions:
                print_no_data()
                continue

            show_transactions(transactions)
            try:
                txn_id = int(input("Transaction ID to update: "))
            except ValueError:
                print("Invalid transaction ID.")
                continue

            category = get_valid_category()
            amount = get_valid_amount()
            if category and amount is not None:
                if update_transaction(txn_id, user_id, category, amount):
                    print("Transaction updated successfully!")
                else:
                    print("Transaction not found.")

        # Delete Transaction
        elif choice == "7":
            transactions = get_transactions(user_id)
            if not transactions:
                print_no_data()
                continue

            show_transactions(transactions)
            try:
                txn_id = int(input("Transaction ID to delete: "))
            except ValueError:
                print("Invalid transaction ID.")
                continue

            if delete_transaction(txn_id, user_id):
                print("Transaction deleted successfully!")
            else:
                print("Transaction not found.")

        # Monthly Report
        elif choice == "8":
            try:
                year = int(input("Year (YYYY): "))
                month = int(input("Month (1-12): "))
                if month not in range(1, 13):
                    raise ValueError
            except ValueError:
                print("Invalid year or month.")
                continue

            income, expense, savings = get_monthly_report(user_id, year, month)

            print("\n--- Monthly Report ---")
            print(f"Period       : {year}-{month:02d}")
            if income == 0 and expense == 0:
                print_no_data()
            else:
                print(f"Total Income : {income}")
                print(f"Total Expense: {expense}")
                print(f"Savings      : {savings}")

        # Yearly Report
        elif choice == "9":
            try:
                year = int(input("Year (YYYY): "))
            except ValueError:
                print("Invalid year.")
                continue

            income, expense, savings = get_yearly_report(user_id, year)

            print("\n--- Yearly Report ---")
            print(f"Year         : {year}")
            if income == 0 and expense == 0:
                print_no_data()
            else:
                print(f"Total Income : {income}")
                print(f"Total Expense: {expense}")
                print(f"Savings      : {savings}")

        # Yearly Monthly Breakdown
        elif choice == "10":
            try:
                year = int(input("Year (YYYY): "))
            except ValueError:
                print("Invalid year.")
                continue

            breakdown = get_yearly_monthly_breakdown(user_id, year)
            if not breakdown:
                print_no_data()
                continue

            print(f"\n--- Monthly Breakdown for {year} ---")
            for month in sorted(breakdown.keys()):
                data = breakdown[month]
                print(
                    f"{month} | "
                    f"Income: {data['income']:>8} | "
                    f"Expense: {data['expense']:>8} | "
                    f"Savings: {data['savings']:>8}"
                )

        # Category-wise Summary
        elif choice == "11":
            summary = get_category_summary(user_id)
            if not summary:
                print_no_data()
                continue

            print("\n--- Category-wise Summary ---")
            for category in sorted(summary.keys()):
                data = summary[category]
                if data["income"] > 0:
                    print(f"{category:<15} Income : {data['income']}")
                if data["expense"] > 0:
                    print(f"{category:<15} Expense: {data['expense']}")

        # Income vs Expense Summary
        elif choice == "12":
            income, expense, savings = get_income_expense_summary(user_id)

            print("\n--- Income vs Expense Summary ---")
            if income == 0 and expense == 0:
                print_no_data()
            else:
                print(f"Total Income : {income}")
                print(f"Total Expense: {expense}")
                print(f"Net Savings  : {savings}")

                if savings > 0:
                    print("Status       : Positive (Income > Expense)")
                elif savings < 0:
                    print("Status       : Negative (Expense > Income)")
                else:
                    print("Status       : Neutral (Balanced)")

        elif choice == "13":
            category = get_valid_category()
            if not category:
                continue

            try:
                month = int(input("Month (1-12): "))
                year = int(input("Year (YYYY): "))
                if month not in range(1, 13):
                    raise ValueError
            except ValueError:
                print("Invalid month or year.")
                continue

            amount = get_valid_amount()
            if amount is None:
                continue

            set_budget(user_id, category, month, year, amount)
            print("Budget set successfully!")

        elif choice == "14":
            try:
                month = int(input("Month (1-12): "))
                year = int(input("Year (YYYY): "))
                if month not in range(1, 13):
                    raise ValueError
            except ValueError:
                print("Invalid month or year.")
                continue

            budgets = get_budgets(user_id, month, year)

            if not budgets:
                print("No budgets found for this period.")
                continue

            print(f"\n--- Budgets for {year}-{month:02d} ---")
            for category, amount in budgets:
                print(f"{category:<15} Budget: {amount}")

        elif choice == "15":
            try:
                month = int(input("Month (1-12): "))
                year = int(input("Year (YYYY): "))
                if month not in range(1, 13):
                    raise ValueError
            except ValueError:
                print("Invalid month or year.")
                continue

            status = get_budget_status(user_id, month, year)

            if not status:
                print("No budgets found for this period.")
                continue

            print(f"\n--- Budget Status for {year}-{month:02d} ---")
            print("Category        Budget     Spent      Status")
            print("-" * 50)

            for category, budget, spent in status:
                if spent > budget:
                    result = "OVER BUDGET"
                else:
                    result = "OK"

                print(f"{category:<15} {budget:<10} {spent:<10} {result}")

        elif choice == "16":
            try:
                month = int(input("Month (1-12): "))
                year = int(input("Year (YYYY): "))
                if month not in range(1, 13):
                    raise ValueError
            except ValueError:
                print("Invalid month or year.")
                continue

            budgets = get_budgets(user_id, month, year)

            if not budgets:
                print("No budgets found for this period.")
                continue

            print(f"\n--- Budgets for {year}-{month:02d} ---")
            for category, amount in budgets:
                print(f"{category:<15} Budget: {amount}")

            category = input("Enter category to delete: ").strip()
            if not category:
                print("Category cannot be empty.")
                continue

            if delete_budget(user_id, category, month, year):
                print("Budget deleted successfully!")
            else:
                print("Budget not found.")

        elif choice == "17":
            try:
                month = int(input("Enter month (1-12): "))
                year = int(input("Enter year (YYYY): "))
                if month not in range(1, 13):
                    raise ValueError
            except ValueError:
                print("Invalid month or year.")
                continue

            insights = get_budget_insights(user_id, month, year)

            if not insights:
                print("No expense data found for this period.")
                continue

            print(f"\n--- Budget Insights for {year}-{month:02d} ---")
            print("Category        Spent     Budget     Status        Recommendation")
            print("-" * 75)

            for item in insights:
                budget_display = item["budget"] if item["budget"] else "N/A"
                print(
                    f"{item['category']:<15} "
                    f"{item['spent']:<9} "
                    f"{budget_display:<10} "
                    f"{item['status']:<13} "
                    f"{item['suggestion']}"
                )

        # Logout
        elif choice == "18":
            print("Logged out.")
            break

        else:
            print("Invalid option. Please try again.")


# ===============================
# APPLICATION ENTRY POINT
# ===============================

def main():
    print("\nPersonal Finance Manager")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if not username or not password:
            print("Username and password cannot be empty.")
            return

        if register_user(username, password):
            print("User registered successfully!")
        else:
            print("Username already exists.")

    elif choice == "2":
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if not username or not password:
            print("Username and password cannot be empty.")
            return

        user_id = login_user(username, password)
        if user_id:
            print("Login successful!")
            user_session(user_id)
        else:
            print("Invalid credentials.")

    elif choice == "3":
        print("Goodbye!")
        exit()

    else:
        print("Invalid option.")


if __name__ == "__main__":
    initialize_database()
    main()
