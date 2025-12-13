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

def get_transactions(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT type, category, amount, date
        FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows

def get_monthly_report(user_id: int, year: int, month: int):
    conn = get_connection()
    cursor = conn.cursor()

    month_str = f"{year}-{month:02d}"

    cursor.execute(
        """
        SELECT type, SUM(amount)
        FROM transactions
        WHERE user_id = ?
          AND date LIKE ?
        GROUP BY type
        """,
        (user_id, f"{month_str}%")
    )

    results = cursor.fetchall()
    conn.close()

    income = 0
    expense = 0

    for txn_type, total in results:
        if txn_type == "income":
            income = total or 0
        elif txn_type == "expense":
            expense = total or 0

    savings = income - expense
    return income, expense, savings

