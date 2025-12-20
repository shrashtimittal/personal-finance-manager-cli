from database.db import get_connection


# ===============================
# CREATE / UPDATE BUDGET
# ===============================

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


# ===============================
# READ BUDGETS
# ===============================

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


# ===============================
# DELETE BUDGET (DAY 18)
# ===============================

def delete_budget(user_id: int, category: str, month: int, year: int):
    """
    Delete a specific monthly budget.
    Returns True if deleted, False if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM budgets
        WHERE user_id = ?
          AND category = ?
          AND month = ?
          AND year = ?
        """,
        (user_id, category, month, year)
    )

    affected = cursor.rowcount
    conn.commit()
    conn.close()

    return affected > 0


# ===============================
# BUDGET STATUS / ALERTS (DAY 17)
# ===============================

def get_budget_status(user_id: int, month: int, year: int):
    """
    Compare budgets with actual expenses and return status.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT b.category,
               b.amount AS budget,
               COALESCE(SUM(t.amount), 0) AS spent
        FROM budgets b
        LEFT JOIN transactions t
          ON b.user_id = t.user_id
         AND b.category = t.category
         AND t.type = 'expense'
         AND t.date LIKE ?
        WHERE b.user_id = ?
          AND b.month = ?
          AND b.year = ?
        GROUP BY b.category, b.amount
        ORDER BY b.category
        """,
        (f"{year}-{month:02d}%", user_id, month, year)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows

def get_budget_insights(user_id: int, month: int, year: int):
    """
    Generate budget insights and recommendations.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Total expenses per category
    cursor.execute(
        """
        SELECT category, SUM(amount) as spent
        FROM transactions
        WHERE user_id = ?
          AND type = 'expense'
          AND date LIKE ?
        GROUP BY category
        ORDER BY spent DESC
        """,
        (user_id, f"{year}-{month:02d}%")
    )

    expenses = cursor.fetchall()

    # Budgets for the month
    cursor.execute(
        """
        SELECT category, amount
        FROM budgets
        WHERE user_id = ?
          AND month = ?
          AND year = ?
        """,
        (user_id, month, year)
    )

    budgets = dict(cursor.fetchall())
    conn.close()

    insights = []

    for category, spent in expenses:
        budget = budgets.get(category)

        if budget:
            usage = spent / budget
            if usage >= 1:
                status = "Over Budget"
                suggestion = "Reduce spending or increase budget"
            elif usage >= 0.8:
                status = "Near Limit"
                suggestion = "Monitor spending closely"
            else:
                status = "Safe"
                suggestion = "Spending under control"
        else:
            status = "No Budget"
            suggestion = "Consider setting a budget"

        insights.append({
            "category": category,
            "spent": spent,
            "budget": budget,
            "status": status,
            "suggestion": suggestion
        })

    return insights

