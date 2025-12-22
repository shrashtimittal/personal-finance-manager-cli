from typing import Dict, Any, List, Tuple

from gui.state.app_state import AppState

# ===============================
# BACKEND IMPORTS (UNCHANGED)
# ===============================
from auth.auth import login_user, register_user

from transactions.transactions import (
    get_transactions,
    add_transaction,
    update_transaction,
    delete_transaction
)

from budgets.budgets import (
    get_budgets,
    set_budget,
    delete_budget,
    get_budget_insights
)

from transactions.transactions import (
    get_monthly_report,
    get_yearly_report,
    get_yearly_monthly_breakdown,
    get_category_summary,
    get_income_expense_summary
)


class AppController:
    """
    Thin controller that:
    - Receives requests from GUI
    - Calls backend functions
    - Updates AppState
    - Returns data to GUI
    """

    def __init__(self, state: AppState):
        self.state = state

    # ===============================
    # AUTH
    # ===============================
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        success, result = login_user(username, password)
        if success:
            self.state.set_user(result)
            return True, "Login successful"
        return False, result

    def register(self, username: str, password: str) -> Tuple[bool, str]:
        success, result = register_user(username, password)
        return success, result

    def logout(self):
        self.state.clear_user()

    # ===============================
    # DATE CONTEXT
    # ===============================
    def set_period(self, month: int, year: int):
        self.state.set_period(month, year)

    # ===============================
    # DASHBOARD
    # ===============================
    def get_dashboard_summary(self) -> Dict[str, Any]:
        if self.state.dashboard_cache:
            return self.state.dashboard_cache

        income, expense, savings = get_monthly_report(
            self.state.user_id,
            self.state.year,
            self.state.month
        )

        summary = {
            "income": income,
            "expense": expense,
            "savings": savings
        }

        self.state.dashboard_cache.update(summary)
        return summary

    # ===============================
    # TRANSACTIONS
    # ===============================
    def fetch_transactions(self) -> List[Dict[str, Any]]:
        return get_transactions(self.state.user_id)

    def create_transaction(self, data: Dict[str, Any]):
        add_transaction(self.state.user_id, **data)
        self.state.clear_caches()

    def edit_transaction(self, transaction_id: int, data: Dict[str, Any]):
        update_transaction(transaction_id, **data)
        self.state.clear_caches()

    def remove_transaction(self, transaction_id: int):
        delete_transaction(transaction_id)
        self.state.clear_caches()

    # ===============================
    # BUDGETS
    # ===============================
    def fetch_budgets(self):
        return get_budgets(
            self.state.user_id,
            self.state.month,
            self.state.year
        )

    def save_budget(self, category: str, amount: float):
        set_budget(
            self.state.user_id,
            category,
            self.state.month,
            self.state.year,
            amount
        )
        self.state.clear_caches()

    def remove_budget(self, category: str):
        delete_budget(
            self.state.user_id,
            category,
            self.state.month,
            self.state.year
        )
        self.state.clear_caches()

    # ===============================
    # INSIGHTS
    # ===============================
    def get_insights(self):
        if self.state.insights_cache:
            return self.state.insights_cache

        insights = get_budget_insights(
            self.state.user_id,
            self.state.month,
            self.state.year
        )

        self.state.insights_cache["data"] = insights
        return insights

    # ===============================
    # REPORTS
    # ===============================
    def get_reports_data(self) -> Dict[str, Any]:
        if self.state.reports_cache:
            return self.state.reports_cache

        data = {
            "monthly": get_monthly_report(
                self.state.user_id,
                self.state.year,
                self.state.month
            ),
            "yearly": get_yearly_report(
                self.state.user_id,
                self.state.year
            ),
            "breakdown": get_yearly_monthly_breakdown(
                self.state.user_id,
                self.state.year
            ),
            "categories": get_category_summary(
                self.state.user_id
            ),
            "income_vs_expense": get_income_expense_summary(
                self.state.user_id
            )
        }

        self.state.reports_cache.update(data)
        return data
