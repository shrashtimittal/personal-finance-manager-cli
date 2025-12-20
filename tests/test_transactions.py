from transactions.transactions import add_transaction, get_transactions
from database.db import initialize_database
from auth.auth import register_user, login_user

def test_add_and_fetch_transaction():
    initialize_database()

    register_user("txn_user", "1234")
    user_id = login_user("txn_user", "1234")

    add_transaction(user_id, "income", "Salary", 5000)
    transactions = get_transactions(user_id)

    assert len(transactions) > 0
    assert transactions[0][2] == "Salary"
