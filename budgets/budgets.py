from database.db import get_connection


def set_budget(user_id: int, category: str, month: int, year: int, amount: float):
    """
    Create or update a monthly budget for a category.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO budgets (user_id, category, month, year, amount)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id, category, month, year)
        DO UPDATE SET amount = excluded.amount
        """,
        (user_id, category, month, year, amount)
    )

    conn.commit()
    conn.close()


def get_budgets(user_id: int, month: int, year: int):
    """
    Fetch all budgets for a given month and year.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT category, amount
        FROM budgets
        WHERE user_id = ? AND month = ? AND year = ?
        ORDER BY category
        """,
        (user_id, month, year)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows
