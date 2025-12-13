from database.db import initialize_database
from auth.auth import register_user, login_user
from transactions.transactions import add_transaction


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

            print("\n1. Add Income")
            print("2. Add Expense")

            sub_choice = input("Choose an option: ")

            category = input("Category: ")
            amount = float(input("Amount: "))

            if sub_choice == "1":
                add_transaction(user_id, "income", category, amount)
                print("Income added successfully!")

            elif sub_choice == "2":
                add_transaction(user_id, "expense", category, amount)
                print("Expense added successfully!")

            else:
                print("Invalid option.")

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

