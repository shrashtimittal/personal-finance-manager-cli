from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal


class Sidebar(QFrame):
    navigate = Signal(str)  # emits page key

    def __init__(self):
        super().__init__()

        self.setObjectName("Sidebar")
        self.setFixedWidth(240)

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 24)
        layout.setSpacing(12)

        # App Logo / Name
        logo = QLabel("💰 Finance Manager")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        layout.addWidget(logo)

        user = QLabel("Welcome")
        user.setAlignment(Qt.AlignCenter)
        user.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 13px;")
        layout.addWidget(user)

        layout.addSpacing(20)

        # Buttons
        self.buttons = {}

        for key, text in [
            ("dashboard", "Dashboard"),
            ("transactions", "Transactions"),
            ("budgets", "Budgets"),
            ("reports", "Reports"),
            ("insights", "Insights"),
        ]:
            btn = self._btn(text)
            btn.clicked.connect(lambda _, k=key: self.navigate.emit(k))
            self.buttons[key] = btn
            layout.addWidget(btn)

        layout.addStretch()

        self.settings_btn = self._btn("Settings")
        self.logout_btn = self._btn("Logout")

        layout.addWidget(self.settings_btn)
        layout.addWidget(self.logout_btn)

    def _btn(self, text):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setObjectName("SidebarButton")
        return btn

    def set_active(self, key: str):
        for k, btn in self.buttons.items():
            btn.setChecked(k == key)
