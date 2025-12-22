from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QComboBox
)
from PySide6.QtCore import Qt, QDate


class SetBudgetDialog(QDialog):
    """
    Dialog to set a monthly budget for a category.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Set Monthly Budget")
        self.setModal(True)
        self.setFixedWidth(420)

        self._init_ui()

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
        title = QLabel("Set Monthly Budget")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        # -------------------------------
        # CATEGORY
        # -------------------------------
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("e.g. Food, Rent, Travel")

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

        current_month = QDate.currentDate().month()
        self.month_input.setCurrentIndex(current_month - 1)

        layout.addWidget(QLabel("Month"))
        layout.addWidget(self.month_input)

        # -------------------------------
        # YEAR
        # -------------------------------
        self.year_input = QComboBox()

        current_year = QDate.currentDate().year()
        for y in range(current_year - 2, current_year + 3):
            self.year_input.addItem(str(y))

        self.year_input.setCurrentText(str(current_year))

        layout.addWidget(QLabel("Year"))
        layout.addWidget(self.year_input)

        # -------------------------------
        # AMOUNT
        # -------------------------------
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Budget amount")

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
        self.save_btn = QPushButton("Save Budget")

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
    # VALIDATION
    # ===============================
    def _validate(self):
        category = self.category_input.text().strip()
        amount_text = self.amount_input.text().strip()

        if not category:
            self._show_error("Category is required.")
            return

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
        Returns validated budget data.
        """
        return {
            "category": self.category_input.text().strip(),
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
