from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt


class InsightCard(QFrame):
    """
    Displays a single financial insight with:
    - Category
    - Status
    - Recommendation
    """

    def __init__(
        self,
        category: str,
        status: str,
        recommendation: str,
        parent=None
    ):
        super().__init__(parent)

        self.category = category
        self.status = status
        self.recommendation = recommendation

        self._init_ui()
        self._apply_status_style()

    # ===============================
    # UI SETUP
    # ===============================
    def _init_ui(self):
        self.setObjectName("InsightCard")
        self.setMinimumHeight(100)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(16, 16, 16, 16)

        # -------------------------------
        # Top Row: Category + Status
        # -------------------------------
        top_row = QHBoxLayout()

        self.category_label = QLabel(self.category)
        self.category_label.setObjectName("CardTitle")

        self.status_label = QLabel(self.status)
        self.status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.status_label.setObjectName("InsightStatus")

        top_row.addWidget(self.category_label)
        top_row.addStretch()
        top_row.addWidget(self.status_label)

        layout.addLayout(top_row)

        # -------------------------------
        # Recommendation Text
        # -------------------------------
        self.recommendation_label = QLabel(self.recommendation)
        self.recommendation_label.setWordWrap(True)
        self.recommendation_label.setObjectName("SecondaryText")

        layout.addWidget(self.recommendation_label)

    # ===============================
    # STATUS STYLING
    # ===============================
    def _apply_status_style(self):
        level_map = {
            "Safe": "success",
            "Near Limit": "warning",
            "Over Budget": "danger",
            "No Budget": "neutral"
        }

        level = level_map.get(self.status, "neutral")
        self.setProperty("level", level)
        self.status_label.setProperty("level", level)

        # Force style refresh
        self.style().unpolish(self)
        self.style().polish(self)
