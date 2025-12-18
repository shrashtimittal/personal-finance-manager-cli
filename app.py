from database.db import initialize_database
from auth.auth import register_user, login_user
from transactions.transactions import (
    add_transaction,
    get_transactions,
    get_transactions_by_category,
    update_transaction,
    delete_transaction,
    get_monthly_report
)


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
    for txn in transactions:
        txn_id, txn_type, category, amount, date = txn
        print(f"{txn_id:<4} {txn_type:<8} {category:<15} {amount:<10} {date}")


def user_session(user_id):
    while True:
        print("\n--- Dashboard ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. View Transactions by Category")
        print("5. Update Transaction")
        print("6. Delete Transaction")
        print("7. Monthly Report")
        print("8. Logout")

        choice = input("Choose an option: ")

        # 1️⃣ Add Income
        if choice == "1":
            category = get_valid_category()
            if not category:
                continue

            amount = get_valid_amount()
            if amount is None:
                continue

            add_transaction(user_id, "income", category, amount)
            print("Income added successfully!")

        # 2️⃣ Add Expense
        elif choice == "2":
            category = get_valid_category()
            if not category:
                continue

            amount = get_valid_amount()
            if amount is None:
                continue

            add_transaction(user_id, "expense", category, amount)
            print("Expense added successfully!")

        # 3️⃣ View All Transactions
        elif choice == "3":
            transactions = get_transactions(user_id)
            if not transactions:
                print("No transactions found.")
            else:
                show_transactions(transactions)

        # 4️⃣ View Transactions by Category  ✅ DAY 8 FEATURE
        elif choice == "4":
            category = get_valid_category()
            if not category:
                continue

            transactions = get_transactions_by_category(user_id, category)
            if not transactions:
                print(f"No transactions found for category '{category}'.")
            else:
                show_transactions(transactions)

        # 5️⃣ Update Transaction
        elif choice == "5":
            transactions = get_transactions(user_id)
            if not transactions:
                print("No transactions available to update.")
                continue

            show_transactions(transactions)

            try:
                txn_id = int(input("Enter Transaction ID to update: "))
            except ValueError:
                print("Invalid transaction ID.")
                continue

            category = get_valid_category()
            if not category:
                continue

            amount = get_valid_amount()
            if amount is None:
                continue

            update_transaction(txn_id, user_id, category, amount)
            print("Transaction updated successfully!")

        # 6️⃣ Delete Transaction
        elif choice == "6":
            transactions = get_transactions(user_id)
            if not transactions:
                print("No transactions available to delete.")
                continue

            show_transactions(transactions)

            try:
                txn_id = int(input("Enter Transaction ID to delete: "))
            except ValueError:
                print("Invalid transaction ID.")
                continue

            delete_transaction(txn_id, user_id)
            print("Transaction deleted successfully!")

        # 7️⃣ Monthly Report (already implemented earlier)
        elif choice == "7":
            try:
                year = int(input("Enter year (YYYY): "))
                month = int(input("Enter month (1-12): "))
                if month < 1 or month > 12:
                    print("Month must be between 1 and 12.")
                    continue
            except ValueError:
                print("Invalid year or month.")
                continue

            income, expense, savings = get_monthly_report(user_id, year, month)

            print("\n--- Monthly Report ---")
            print(f"Total Income : {income}")
            print(f"Total Expense: {expense}")
            print(f"Savings      : {savings}")

        # 8️⃣ Logout
        elif choice == "8":
            print("Logged out.")
            break

        else:
            print("Invalid option. Please try again.")


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
