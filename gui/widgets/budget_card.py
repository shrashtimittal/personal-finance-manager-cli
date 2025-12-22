from typing import Optional

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar
)
from PySide6.QtCore import Qt


class BudgetCard(QFrame):
    """
    Displays a single category budget with:
    - Category name
    - Budget amount
    - Spent amount
    - Progress bar
    - Status label
    """

    def __init__(
        self,
        category: str,
        budget_amount: Optional[float],
        spent_amount: float,
        parent=None
    ):
        super().__init__(parent)

        self.category = category
        self.budget_amount = budget_amount
        self.spent_amount = spent_amount

        self._init_ui()
        self._update_ui()

    # ===============================
    # UI SETUP
    # ===============================
    def _init_ui(self):
        self.setObjectName("BudgetCard")
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # Top row
        top_row = QHBoxLayout()

        self.category_label = QLabel(self.category)
        self.category_label.setObjectName("CardTitle")

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.status_label.setObjectName("BudgetStatus")

        top_row.addWidget(self.category_label)
        top_row.addStretch()
        top_row.addWidget(self.status_label)

        layout.addLayout(top_row)

        # Amounts row
        amounts_row = QHBoxLayout()

        self.budget_label = QLabel()
        self.spent_label = QLabel()

        amounts_row.addWidget(self.budget_label)
        amounts_row.addStretch()
        amounts_row.addWidget(self.spent_label)

        layout.addLayout(amounts_row)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(10)

        layout.addWidget(self.progress)

        # Actions
        actions = QHBoxLayout()

        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setObjectName("DangerButton")

        actions.addStretch()
        actions.addWidget(self.edit_btn)
        actions.addWidget(self.delete_btn)

        layout.addLayout(actions)

    # ===============================
    # UI UPDATE LOGIC
    # ===============================
    def _update_ui(self):
        if self.budget_amount is None:
            self.budget_label.setText("Budget: Not set")
            self.spent_label.setText(f"Spent: ₹{self.spent_amount:,.2f}")
            self.progress.setValue(0)
            self._set_status("No Budget", "neutral")
            return

        usage_ratio = (
            self.spent_amount / self.budget_amount
            if self.budget_amount > 0
            else 0
        )

        percent = min(int(usage_ratio * 100), 100)

        self.budget_label.setText(f"Budget: ₹{self.budget_amount:,.2f}")
        self.spent_label.setText(f"Spent: ₹{self.spent_amount:,.2f}")
        self.progress.setValue(percent)

        if usage_ratio >= 1:
            self._set_status("Over Budget", "danger")
        elif usage_ratio >= 0.8:
            self._set_status("Near Limit", "warning")
        else:
            self._set_status("Safe", "success")

    # ===============================
    # STATUS STYLING
    # ===============================
    def _set_status(self, text: str, level: str):
        self.status_label.setText(text)

        self.progress.setProperty("level", level)
        self.status_label.setProperty("level", level)

        # Force style refresh
        self.progress.style().unpolish(self.progress)
        self.progress.style().polish(self.progress)

        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
