from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QTextEdit
)
from PySide6.QtCore import Qt, QDate


class EditTransactionDialog(QDialog):
    def __init__(self, transaction: dict, parent=None):
        """
        transaction dict keys expected:
        id, type, date, category, amount, description
        """
        super().__init__(parent)

        self.transaction = transaction

        self.setWindowTitle("Edit Transaction")
        self.setModal(True)
        self.setFixedWidth(420)

        self._init_ui()
        self._prefill()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # ===============================
        # TITLE
        # ===============================
        title = QLabel("Edit Transaction")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        # ===============================
        # TYPE
        # ===============================
        self.type_input = QComboBox()
        self.type_input.addItems(["Income", "Expense"])
        layout.addWidget(QLabel("Type"))
        layout.addWidget(self.type_input)

        # ===============================
        # DATE
        # ===============================
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(QLabel("Date"))
        layout.addWidget(self.date_input)

        # ===============================
        # CATEGORY
        # ===============================
        self.category_input = QLineEdit()
        layout.addWidget(QLabel("Category"))
        layout.addWidget(self.category_input)

        # ===============================
        # AMOUNT
        # ===============================
        self.amount_input = QLineEdit()
        layout.addWidget(QLabel("Amount"))
        layout.addWidget(self.amount_input)

        # ===============================
        # DESCRIPTION
        # ===============================
        self.description_input = QTextEdit()
        self.description_input.setFixedHeight(80)
        layout.addWidget(QLabel("Description"))
        layout.addWidget(self.description_input)

        # ===============================
        # ERROR LABEL
        # ===============================
        self.error_label = QLabel("")
        self.error_label.setObjectName("DangerText")
        self.error_label.hide()
        layout.addWidget(self.error_label)

        # ===============================
        # BUTTONS
        # ===============================
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.cancel_btn = QPushButton("Cancel")
        self.save_btn = QPushButton("Save Changes")

        btn_row.addStretch()
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)

        layout.addLayout(btn_row)

        # ===============================
        # ACTIONS
        # ===============================
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self._validate)

    # ===============================
    # PREFILL
    # ===============================
    def _prefill(self):
        self.type_input.setCurrentText(self.transaction["type"])
        self.category_input.setText(self.transaction["category"])
        self.amount_input.setText(str(self.transaction["amount"]))
        self.description_input.setText(self.transaction.get("description", ""))

        year, month, day = map(int, self.transaction["date"].split("-"))
        self.date_input.setDate(QDate(year, month, day))

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
    def get_updated_data(self) -> dict:
        return {
            "id": self.transaction["id"],
            "type": self.type_input.currentText(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "category": self.category_input.text().strip(),
            "amount": float(self.amount_input.text()),
            "description": self.description_input.toPlainText().strip(),
        }

    def _show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.show()
