from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QPushButton,
    QLineEdit, QComboBox, QDateEdit,
    QTableWidgetItem
)
from PySide6.QtCore import Qt, QDate

from gui.dialogs.add_transaction_dialog import AddTransactionDialog
from gui.dialogs.edit_transaction_dialog import EditTransactionDialog
from gui.dialogs.confirm_delete_dialog import ConfirmDeleteDialog


class TransactionsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.controller = None

        self.current_page = 1
        self.page_size_value = 10
        self.total_rows = 0
        self.transactions = []

        self._init_ui()

    # ===============================
    # CONTROLLER BINDING
    # ===============================
    def set_controller(self, controller):
        self.controller = controller
        self.current_page = 1
        self._load_transactions()

    # ===============================
    # UI
    # ===============================
    def _init_ui(self):
        layout = QVBoxLayout(self)

        # -------------------------------
        # HEADER
        # -------------------------------
        header = QHBoxLayout()
        title = QLabel("Transactions")
        title.setObjectName("PageTitle")

        self.add_btn = QPushButton("Add Transaction")
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.add_btn)
        layout.addLayout(header)

        # -------------------------------
        # FILTERS
        # -------------------------------
        filters = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search…")

        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories")

        self.from_date = QDateEdit(QDate.currentDate().addMonths(-1))
        self.from_date.setCalendarPopup(True)
        self.from_date.setDisplayFormat("yyyy-MM-dd")

        self.to_date = QDateEdit(QDate.currentDate())
        self.to_date.setCalendarPopup(True)
        self.to_date.setDisplayFormat("yyyy-MM-dd")

        filters.addWidget(self.search_input)
        filters.addWidget(self.category_filter)
        filters.addWidget(self.from_date)
        filters.addWidget(self.to_date)

        layout.addLayout(filters)

        # -------------------------------
        # TABLE
        # -------------------------------
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Date", "Category", "Type", "Amount", "Actions"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # -------------------------------
        # PAGINATION
        # -------------------------------
        pager = QHBoxLayout()

        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        self.page_label = QLabel("Page 1 of 1")

        self.page_size = QComboBox()
        self.page_size.addItems(["10", "25", "50"])
        self.page_size.setCurrentText("10")

        pager.addWidget(self.prev_btn)
        pager.addWidget(self.next_btn)
        pager.addStretch()
        pager.addWidget(self.page_label)
        pager.addWidget(self.page_size)

        layout.addLayout(pager)

        # -------------------------------
        # SIGNALS
        # -------------------------------
        self.add_btn.clicked.connect(self._add_transaction)
        self.search_input.textChanged.connect(self._load_transactions)
        self.category_filter.currentTextChanged.connect(self._load_transactions)
        self.from_date.dateChanged.connect(self._load_transactions)
        self.to_date.dateChanged.connect(self._load_transactions)
        self.page_size.currentTextChanged.connect(self._change_page_size)
        self.prev_btn.clicked.connect(self._prev_page)
        self.next_btn.clicked.connect(self._next_page)
        self.table.cellDoubleClicked.connect(self._edit_transaction)

    # ===============================
    # DATA LOADING (CONTROLLER)
    # ===============================
    def _load_transactions(self):
        if not self.controller or not self.controller.state.is_authenticated:
            return

        offset = (self.current_page - 1) * self.page_size_value

        self.transactions, self.total_rows = self.controller.fetch_transactions(
            search=self.search_input.text(),
            category=self.category_filter.currentText(),
            from_date=self.from_date.date().toString("yyyy-MM-dd"),
            to_date=self.to_date.date().toString("yyyy-MM-dd"),
            limit=self.page_size_value,
            offset=offset
        )

        self._populate_table()

    def _populate_table(self):
        self.table.setRowCount(0)

        for row, txn in enumerate(self.transactions):
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(txn["date"]))
            self.table.setItem(row, 1, QTableWidgetItem(txn["category"]))
            self.table.setItem(row, 2, QTableWidgetItem(txn["type"]))
            self.table.setItem(row, 3, QTableWidgetItem(f"{txn['amount']:.2f}"))

            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda _, r=row: self._delete_transaction(r))
            self.table.setCellWidget(row, 4, delete_btn)

        pages = max(
            1,
            (self.total_rows + self.page_size_value - 1) // self.page_size_value
        )
        self.page_label.setText(f"Page {self.current_page} of {pages}")

    # ===============================
    # ACTIONS
    # ===============================
    def _add_transaction(self):
        dialog = AddTransactionDialog(self)
        if dialog.exec():
            self.controller.create_transaction(dialog.get_data())
            self._load_transactions()

    def _edit_transaction(self, row, _):
        dialog = EditTransactionDialog(self.transactions[row], self)
        if dialog.exec():
            self.controller.edit_transaction(
                self.transactions[row]["id"],
                dialog.get_updated_data()
            )
            self._load_transactions()

    def _delete_transaction(self, row):
        dialog = ConfirmDeleteDialog("Delete this transaction?", self)
        if dialog.exec():
            self.controller.remove_transaction(self.transactions[row]["id"])
            self._load_transactions()

    def _change_page_size(self, value):
        self.page_size_value = int(value)
        self.current_page = 1
        self._load_transactions()

    def _next_page(self):
        if self.current_page * self.page_size_value < self.total_rows:
            self.current_page += 1
            self._load_transactions()

    def _prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self._load_transactions()
