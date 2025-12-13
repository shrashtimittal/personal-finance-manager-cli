from database.db import initialize_database
from auth.auth import register_user, login_user


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
        if login_user(username, password):
            print("Login successful!")
        else:
            print("Invalid credentials.")

    elif choice == "3":
        print("Goodbye!")
        exit()

    else:
        print("Invalid option.")


if __name__ == "__main__":
    initialize_database()   # ensure DB exists
    main()
