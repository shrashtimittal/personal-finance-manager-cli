from budgets.budgets import set_budget, get_budgets
from database.db import initialize_database
from auth.auth import register_user, login_user

def test_set_and_get_budget():
    initialize_database()

    register_user("budget_user", "pass")
    user_id = login_user("budget_user", "pass")

    set_budget(user_id, "Food", 5, 2025, 3000)
    budgets = get_budgets(user_id, 5, 2025)

    assert len(budgets) == 1
    assert budgets[0][0] == "Food"
