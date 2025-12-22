from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton
)
from PySide6.QtCore import Qt


class ConfirmDeleteBudgetDialog(QDialog):
    """
    Confirmation dialog for deleting a budget.
    """

    def __init__(self, category: str, month: int, year: int, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Delete Budget")
        self.setModal(True)
        self.setFixedWidth(380)

        self._init_ui(category, month, year)

    def _init_ui(self, category: str, month: int, year: int):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        message = (
            f"Are you sure you want to delete the budget for "
            f"<b>{category}</b> "
            f"({self._month_name(month)} {year})?"
        )

        label = QLabel(message)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        cancel_btn = QPushButton("Cancel")
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("DangerButton")

        btn_row.addStretch()
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(delete_btn)

        layout.addLayout(btn_row)

        cancel_btn.clicked.connect(self.reject)
        delete_btn.clicked.connect(self.accept)

    @staticmethod
    def _month_name(month: int) -> str:
        months = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]
        return months[month - 1]
