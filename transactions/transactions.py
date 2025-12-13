from database.db import get_connection
from datetime import datetime


def add_transaction(user_id: int, txn_type: str, category: str, amount: float):
    conn = get_connection()
    cursor = conn.cursor()

    date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        """
        INSERT INTO transactions (user_id, type, category, amount, date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, txn_type, category, amount, date)
    )

    conn.commit()
    conn.close()
