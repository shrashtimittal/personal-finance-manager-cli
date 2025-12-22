from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox,
    QFrame, QFileDialog
)
from PySide6.QtCore import Qt

from gui.utils.db_utils import backup_database, restore_database
from gui.widgets.toast import Toast


class SettingsPage(QWidget):
    """
    Application settings and utilities.
    """

    def __init__(self):
        super().__init__()
        self._init_ui()
        self._wire_actions()

    # ===============================
    # UI SETUP
    # ===============================
    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Settings")
        title.setObjectName("PageTitle")

        subtitle = QLabel("Customize preferences and manage your data")
        subtitle.setObjectName("SecondaryText")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Appearance
        theme_card = self._create_card("Appearance")
        theme_row = QHBoxLayout()

        theme_row.addWidget(QLabel("Theme"))
        theme_row.addStretch()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        theme_row.addWidget(self.theme_combo)

        theme_card.layout().addLayout(theme_row)

        # Currency
        currency_card = self._create_card("Currency")
        currency_row = QHBoxLayout()

        currency_row.addWidget(QLabel("Preferred Currency"))
        currency_row.addStretch()

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["INR (₹)", "USD ($)", "EUR (€)"])
        currency_row.addWidget(self.currency_combo)

        currency_card.layout().addLayout(currency_row)

        # Data Management
        data_card = self._create_card("Data Management")
        buttons_row = QHBoxLayout()

        self.backup_btn = QPushButton("Backup Database")
        self.restore_btn = QPushButton("Restore Database")

        buttons_row.addWidget(self.backup_btn)
        buttons_row.addWidget(self.restore_btn)

        data_card.layout().addLayout(buttons_row)

        main_layout.addWidget(theme_card)
        main_layout.addWidget(currency_card)
        main_layout.addWidget(data_card)
        main_layout.addStretch()

    # ===============================
    # ACTIONS
    # ===============================
    def _wire_actions(self):
        self.backup_btn.clicked.connect(self._backup_db)
        self.restore_btn.clicked.connect(self._restore_db)

    def _backup_db(self):
        success, result = backup_database()

        Toast(
            parent=self,
            message=result if success else f"Backup failed: {result}",
            level="success" if success else "error"
        )

    def _restore_db(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Backup File",
            "",
            "Database Files (*.db)"
        )

        if not file_path:
            return

        success, result = restore_database(file_path)

        Toast(
            parent=self,
            message=result,
            level="success" if success else "error"
        )

    # ===============================
    # CARD HELPER
    # ===============================
    def _create_card(self, title: str) -> QFrame:
        card = QFrame()
        card.setObjectName("SettingsCard")

        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        label = QLabel(title)
        label.setObjectName("CardTitle")

        layout.addWidget(label)
        return card
