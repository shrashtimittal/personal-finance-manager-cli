from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt

from auth.auth import register_user


class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

        # callback (set by AppWindow)
        self.on_register_success = None

    def _init_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedWidth(420)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(20)

        title = QLabel("Create Account")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Start managing your finances smarter")
        subtitle.setObjectName("SecondaryText")
        subtitle.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.hide()
        card_layout.addWidget(self.message_label)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.confirm_password.setEchoMode(QLineEdit.Password)

        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self._register)

        self.login_link = QPushButton("Back to Login")
        self.login_link.setObjectName("SecondaryButton")

        card_layout.addWidget(self.username)
        card_layout.addWidget(self.password)
        card_layout.addWidget(self.confirm_password)
        card_layout.addWidget(self.register_btn)
        card_layout.addWidget(self.login_link, alignment=Qt.AlignCenter)

        root_layout.addWidget(card)

    def _register(self):
        username = self.username.text().strip()
        password = self.password.text()
        confirm = self.confirm_password.text()

        if not username or not password or not confirm:
            self._show_error("All fields are required.")
            return

        if password != confirm:
            self._show_error("Passwords do not match.")
            return

        if len(password) < 6:
            self._show_error("Password must be at least 6 characters.")
            return

        success = register_user(username, password)

        if not success:
            self._show_error("Username already exists.")
            return

        self._show_success("Account created successfully!")

        if self.on_register_success:
            self.on_register_success()

    def _show_error(self, msg):
        self.message_label.setObjectName("DangerText")
        self.message_label.setText(msg)
        self.message_label.show()

    def _show_success(self, msg):
        self.message_label.setObjectName("SuccessText")
        self.message_label.setText(msg)
        self.message_label.show()
