from database.db import get_connection
from datetime import datetime


# ===============================
# TRANSACTION CREATION
# ===============================

def add_transaction(user_id: int, txn_type: str, category: str, amount: float):
    """
    Add a new income or expense transaction for a user.
    """
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


# ===============================
# TRANSACTION FETCHING
# ===============================

def get_transactions(user_id: int):
    """
    Fetch all transactions for a user.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, type, category, amount, date
        FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_transactions_by_category(user_id: int, category: str):
    """
    Fetch transactions filtered by category.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, type, category, amount, date
        FROM transactions
        WHERE user_id = ? AND category = ?
        ORDER BY date DESC
        """,
        (user_id, category)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_transactions_by_date_range(user_id: int, start_date: str, end_date: str):
    """
    Fetch transactions within a specific date range.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, type, category, amount, date
        FROM transactions
        WHERE user_id = ?
          AND date BETWEEN ? AND ?
        ORDER BY date DESC
        """,
        (user_id, start_date, end_date)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


# ===============================
# UPDATE & DELETE
# ===============================

def update_transaction(txn_id: int, user_id: int, category: str, amount: float):
    """
    Update category and amount of a transaction.
    Returns True if updated, False if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE transactions
        SET category = ?, amount = ?
        WHERE id = ? AND user_id = ?
        """,
        (category, amount, txn_id, user_id)
    )

    affected = cursor.rowcount
    conn.commit()
    conn.close()

    return affected > 0


def delete_transaction(txn_id: int, user_id: int):
    """
    Delete a transaction safely.
    Returns True if deleted, False if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM transactions
        WHERE id = ? AND user_id = ?
        """,
        (txn_id, user_id)
    )

    affected = cursor.rowcount
    conn.commit()
    conn.close()

    return affected > 0


# ===============================
# REPORTING FUNCTIONS
# ===============================

def get_monthly_report(user_id: int, year: int, month: int):
    """
    Returns total income, expense, and savings for a given month.
    """
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

    return income, expense, income - expense


def get_yearly_report(user_id: int, year: int):
    """
    Returns total income, expense, and savings for a year.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT type, SUM(amount)
        FROM transactions
        WHERE user_id = ?
          AND date LIKE ?
        GROUP BY type
        """,
        (user_id, f"{year}%")
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

    return income, expense, income - expense


def get_yearly_monthly_breakdown(user_id: int, year: int):
    """
    Returns month-wise income, expense, and savings for a year.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT substr(date, 1, 7) AS month, type, SUM(amount)
        FROM transactions
        WHERE user_id = ?
          AND date LIKE ?
        GROUP BY month, type
        ORDER BY month
        """,
        (user_id, f"{year}%")
    )

    rows = cursor.fetchall()
    conn.close()

    breakdown = {}

    for month, txn_type, total in rows:
        if month not in breakdown:
            breakdown[month] = {"income": 0, "expense": 0}

        if txn_type == "income":
            breakdown[month]["income"] = total or 0
        elif txn_type == "expense":
            breakdown[month]["expense"] = total or 0

    for month in breakdown:
        breakdown[month]["savings"] = (
            breakdown[month]["income"] - breakdown[month]["expense"]
        )

    return breakdown


def get_category_summary(user_id: int):
    """
    Returns category-wise income and expense totals.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT category, type, SUM(amount)
        FROM transactions
        WHERE user_id = ?
        GROUP BY category, type
        ORDER BY category
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    summary = {}

    for category, txn_type, total in rows:
        if category not in summary:
            summary[category] = {"income": 0, "expense": 0}

        if txn_type == "income":
            summary[category]["income"] = total or 0
        elif txn_type == "expense":
            summary[category]["expense"] = total or 0

    return summary


def get_income_expense_summary(user_id: int):
    """
    Returns total income, total expense, and savings (all-time).
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT type, SUM(amount)
        FROM transactions
        WHERE user_id = ?
        GROUP BY type
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    income = 0
    expense = 0

    for txn_type, total in rows:
        if txn_type == "income":
            income = total or 0
        elif txn_type == "expense":
            expense = total or 0

    return income, expense, income - expense
