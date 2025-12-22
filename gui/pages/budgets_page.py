from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame
)
from PySide6.QtCore import Qt

from gui.widgets.budget_card import BudgetCard
from gui.dialogs.set_budget_dialog import SetBudgetDialog
from gui.dialogs.edit_budget_dialog import EditBudgetDialog
from gui.dialogs.confirm_delete_budget_dialog import ConfirmDeleteBudgetDialog


class BudgetsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.controller = None

        self._init_ui()

    # ===============================
    # CONTROLLER BINDING
    # ===============================
    def set_controller(self, controller):
        self.controller = controller
        self._load_budgets()

    # ===============================
    # UI SETUP
    # ===============================
    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # -------------------------------
        # HEADER
        # -------------------------------
        header = QHBoxLayout()
        title = QLabel("Budgets")
        title.setObjectName("PageTitle")

        self.add_budget_btn = QPushButton("Set Budget")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.add_budget_btn)

        main_layout.addLayout(header)

        # -------------------------------
        # SCROLL AREA
        # -------------------------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setSpacing(16)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(self.cards_container)
        main_layout.addWidget(scroll)

        # -------------------------------
        # EMPTY STATE
        # -------------------------------
        self.empty_label = QLabel("No budgets set for this month.")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setObjectName("SecondaryText")
        self.empty_label.hide()

        main_layout.addWidget(self.empty_label)

        # -------------------------------
        # SIGNALS
        # -------------------------------
        self.add_budget_btn.clicked.connect(self._open_set_dialog)

    # ===============================
    # DATA LOADING (CONTROLLER)
    # ===============================
    def _load_budgets(self):
        if not self.controller or not self.controller.state.is_authenticated:
            return

        # Clear old cards
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        budgets = self.controller.fetch_budgets()
        insights = self.controller.get_insights()

        spent_map = {
            item["category"]: item["spent"]
            for item in insights
            if item.get("spent") is not None
        }

        if not budgets:
            self.empty_label.show()
            return
        else:
            self.empty_label.hide()

        for category, amount in budgets:
            spent = spent_map.get(category, 0)

            card = BudgetCard(
                category=category,
                budget_amount=amount,
                spent_amount=spent
            )

            card.edit_btn.clicked.connect(
                lambda _, c=category, a=amount: self._open_edit_dialog(c, a)
            )
            card.delete_btn.clicked.connect(
                lambda _, c=category: self._open_delete_dialog(c)
            )

            self.cards_layout.addWidget(card)

        self.cards_layout.addStretch()

    # ===============================
    # DIALOGS
    # ===============================
    def _open_set_dialog(self):
        dialog = SetBudgetDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            self.controller.save_budget(
                data["category"],
                data["amount"]
            )
            self._load_budgets()

    def _open_edit_dialog(self, category: str, amount: float):
        budget = {
            "category": category,
            "amount": amount
        }

        dialog = EditBudgetDialog(budget, self)
        if dialog.exec():
            data = dialog.get_data()
            self.controller.save_budget(
                data["category"],
                data["amount"]
            )
            self._load_budgets()

    def _open_delete_dialog(self, category: str):
        dialog = ConfirmDeleteBudgetDialog(category, self)
        if dialog.exec():
            self.controller.remove_budget(category)
            self._load_budgets()
