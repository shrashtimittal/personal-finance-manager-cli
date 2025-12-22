from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QScrollArea, QFrame
)
from PySide6.QtCore import Qt

from gui.widgets.insight_card import InsightCard


class InsightsPage(QWidget):
    """
    Displays real financial insights and recommendations
    derived from budgets and transactions (controller-driven).
    """

    def __init__(self):
        super().__init__()

        self.controller = None

        self._init_ui()

    # ===============================
    # CONTROLLER BINDING
    # ===============================
    def set_controller(self, controller):
        self.controller = controller
        self._load_real_insights()

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

        title = QLabel("Insights")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Smart recommendations based on your spending and budgets"
        )
        subtitle.setObjectName("SecondaryText")

        header_col = QVBoxLayout()
        header_col.addWidget(title)
        header_col.addWidget(subtitle)

        header.addLayout(header_col)
        header.addStretch()

        main_layout.addLayout(header)

        # -------------------------------
        # SCROLL AREA
        # -------------------------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        self.container = QWidget()
        self.cards_layout = QVBoxLayout(self.container)
        self.cards_layout.setSpacing(16)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(self.container)
        main_layout.addWidget(scroll)

        # -------------------------------
        # EMPTY STATE
        # -------------------------------
        self.empty_label = QLabel(
            "No insights available yet. Try setting budgets first."
        )
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setObjectName("SecondaryText")
        self.empty_label.hide()

        main_layout.addWidget(self.empty_label)

    # ===============================
    # INSIGHTS (CONTROLLER-DRIVEN)
    # ===============================
    def _load_real_insights(self):
        self._clear_cards()

        if not self.controller or not self.controller.state.is_authenticated:
            return

        insights = self.controller.get_insights()

        if not insights:
            self.empty_label.show()
            return

        self.empty_label.hide()

        # 🔴 Critical first → 🟢 Safe last
        priority = {
            "Over Budget": 0,
            "Near Limit": 1,
            "No Budget": 2,
            "Safe": 3
        }

        insights.sort(
            key=lambda i: priority.get(i["status"], 4)
        )

        for item in insights:
            recommendation = self._friendly_message(item)

            card = InsightCard(
                category=item["category"],
                status=item["status"],
                recommendation=recommendation
            )

            self.cards_layout.addWidget(card)

        self.cards_layout.addStretch()

    # ===============================
    # FRIENDLY LANGUAGE ENGINE
    # ===============================
    def _friendly_message(self, item: dict) -> str:
        category = item["category"]
        spent = item["spent"]
        budget = item["budget"]
        status = item["status"]

        if status == "Over Budget":
            return (
                f"You’ve exceeded your {category} budget 🚨. "
                f"You spent ₹{spent:.0f} against a budget of ₹{budget:.0f}. "
                "Consider reducing expenses or adjusting the budget."
            )

        if status == "Near Limit":
            return (
                f"You’re close to your {category} budget ⚠️. "
                f"₹{spent:.0f} spent out of ₹{budget:.0f}. "
                "Keeping an eye on this category could help avoid overspending."
            )

        if status == "Safe":
            return (
                f"Your {category} spending is under control ✅. "
                "Nice job maintaining healthy financial habits!"
            )

        if status == "No Budget":
            return (
                f"No budget is set for {category} 🧩. "
                "Setting one could help you track and optimize spending."
            )

        return "Review this category for better financial planning."

    # ===============================
    # HELPERS
    # ===============================
    def _clear_cards(self):
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
