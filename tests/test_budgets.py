from auth.auth import register_user, login_user
from budgets.budgets import set_budget, get_budgets


def test_budget_creation():
    register_user("budgetuser", "pass")
    user_id = login_user("budgetuser", "pass")

    set_budget(user_id, "Food", 2, 2025, 3000)

    budgets = get_budgets(user_id, 2, 2025)
    assert len(budgets) == 1
    assert budgets[0][0] == "Food"
    assert budgets[0][1] == 3000
