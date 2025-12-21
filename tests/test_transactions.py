from auth.auth import register_user, login_user
from transactions.transactions import (
    add_transaction,
    get_transactions,
    delete_transaction
)


def test_add_and_delete_transaction():
    register_user("txnuser", "1234")
    user_id = login_user("txnuser", "1234")

    add_transaction(user_id, "income", "Salary", 5000)

    transactions = get_transactions(user_id)
    assert len(transactions) == 1

    txn_id = transactions[0][0]

    assert delete_transaction(txn_id, user_id) is True

    transactions = get_transactions(user_id)
    assert len(transactions) == 0
