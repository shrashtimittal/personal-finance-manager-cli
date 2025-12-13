from database.db import initialize_database
from auth.auth import register_user, login_user
from transactions.transactions import add_transaction, get_transactions


def user_session(user_id):
    while True:
        print("\n--- Dashboard ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            category = input("Category: ")
            amount = float(input("Amount: "))
            add_transaction(user_id, "income", category, amount)
            print("Income added successfully!")

        elif choice == "2":
            category = input("Category: ")
            amount = float(input("Amount: "))
            add_transaction(user_id, "expense", category, amount)
            print("Expense added successfully!")

        elif choice == "3":
            transactions = get_transactions(user_id)

            if not transactions:
                print("No transactions found.")
            else:
                print("\nType | Category | Amount | Date")
                print("-" * 35)
                for t in transactions:
                    print(f"{t[0]:<6} | {t[1]:<8} | {t[2]:<6} | {t[3]}")

        elif choice == "4":
            print("Logged out.")
            break

        else:
            print("Invalid option.")


def main():
    print("\nPersonal Finance Manager")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        username = input("Username: ")
        password = input("Password: ")
        if register_user(username, password):
            print("User registered successfully!")
        else:
            print("Username already exists.")

    elif choice == "2":
        username = input("Username: ")
        password = input("Password: ")

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
