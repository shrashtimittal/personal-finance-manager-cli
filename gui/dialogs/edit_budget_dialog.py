from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QComboBox
)
from PySide6.QtCore import Qt


class EditBudgetDialog(QDialog):
    """
    Dialog to edit an existing monthly budget.
    Expects a budget dict with keys:
    category, month, year, amount
    """

    def __init__(self, budget: dict, parent=None):
        super().__init__(parent)

        self.budget = budget

        self.setWindowTitle("Edit Budget")
        self.setModal(True)
        self.setFixedWidth(420)

        self._init_ui()
        self._prefill()

    # ===============================
    # UI SETUP
    # ===============================
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # -------------------------------
        # TITLE
        # -------------------------------
        title = QLabel("Edit Budget")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        # -------------------------------
        # CATEGORY (LOCKED)
        # -------------------------------
        self.category_input = QLineEdit()
        self.category_input.setReadOnly(True)

        layout.addWidget(QLabel("Category"))
        layout.addWidget(self.category_input)

        # -------------------------------
        # MONTH
        # -------------------------------
        self.month_input = QComboBox()
        self.month_input.addItems([
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ])

        layout.addWidget(QLabel("Month"))
        layout.addWidget(self.month_input)

        # -------------------------------
        # YEAR
        # -------------------------------
        self.year_input = QComboBox()
        for y in range(self.budget["year"] - 2, self.budget["year"] + 3):
            self.year_input.addItem(str(y))

        layout.addWidget(QLabel("Year"))
        layout.addWidget(self.year_input)

        # -------------------------------
        # AMOUNT
        # -------------------------------
        self.amount_input = QLineEdit()

        layout.addWidget(QLabel("Amount"))
        layout.addWidget(self.amount_input)

        # -------------------------------
        # ERROR LABEL
        # -------------------------------
        self.error_label = QLabel("")
        self.error_label.setObjectName("DangerText")
        self.error_label.hide()
        layout.addWidget(self.error_label)

        # -------------------------------
        # BUTTONS
        # -------------------------------
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.cancel_btn = QPushButton("Cancel")
        self.save_btn = QPushButton("Save Changes")

        btn_row.addStretch()
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)

        layout.addLayout(btn_row)

        # -------------------------------
        # ACTIONS
        # -------------------------------
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self._validate)

    # ===============================
    # PREFILL DATA
    # ===============================
    def _prefill(self):
        self.category_input.setText(self.budget["category"])
        self.month_input.setCurrentIndex(self.budget["month"] - 1)
        self.year_input.setCurrentText(str(self.budget["year"]))
        self.amount_input.setText(str(self.budget["amount"]))

    # ===============================
    # VALIDATION
    # ===============================
    def _validate(self):
        amount_text = self.amount_input.text().strip()

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            self._show_error("Amount must be a positive number.")
            return

        self.error_label.hide()
        self.accept()

    # ===============================
    # DATA ACCESS
    # ===============================
    def get_data(self) -> dict:
        """
        Returns updated budget data.
        """
        return {
            "category": self.category_input.text(),
            "month": self.month_input.currentIndex() + 1,
            "year": int(self.year_input.currentText()),
            "amount": float(self.amount_input.text())
        }

    # ===============================
    # ERROR HANDLER
    # ===============================
    def _show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.show()
