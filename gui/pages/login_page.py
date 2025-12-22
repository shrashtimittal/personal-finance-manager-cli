from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt

from auth.auth import login_user


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

        # callback (set by AppWindow)
        self.on_login_success = None

    def _init_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedWidth(420)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(20)

        title = QLabel("Welcome Back")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Login to manage your finances")
        subtitle.setObjectName("SecondaryText")
        subtitle.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)

        self.error_label = QLabel("")
        self.error_label.setObjectName("DangerText")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()
        card_layout.addWidget(self.error_label)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.toggle_password = QPushButton("Show")
        self.toggle_password.setObjectName("SecondaryButton")
        self.toggle_password.setFixedWidth(80)
        self.toggle_password.clicked.connect(self._toggle_password)

        password_row = QHBoxLayout()
        password_row.addWidget(self.password)
        password_row.addWidget(self.toggle_password)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self._login)

        self.register_link = QPushButton("Create an account")
        self.register_link.setObjectName("SecondaryButton")

        card_layout.addWidget(self.username)
        card_layout.addLayout(password_row)
        card_layout.addWidget(self.login_btn)
        card_layout.addWidget(self.register_link, alignment=Qt.AlignCenter)

        root_layout.addWidget(card)

    def _toggle_password(self):
        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.toggle_password.setText("Hide")
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.toggle_password.setText("Show")

    def _login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()

        if not username or not password:
            self._show_error("Username and password are required.")
            return

        user_id = login_user(username, password)

        if not user_id:
            self._show_error("Invalid username or password.")
            return

        self.error_label.hide()

        # Notify AppWindow
        if self.on_login_success:
            self.on_login_success(user_id)

    def _show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.show()
