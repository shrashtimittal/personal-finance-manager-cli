from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
)
from PySide6.QtCore import Qt


class ErrorDialog(QDialog):
    """
    Friendly error dialog for user-facing failures.
    """

    def __init__(
        self,
        title: str = "Something went wrong",
        message: str = "An unexpected error occurred.",
        details: str | None = None,
        parent=None
    ):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(420)

        self._init_ui(message, details)

    def _init_ui(self, message: str, details: str | None):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        icon = QLabel("⚠️")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size: 36px;")

        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setObjectName("PageTitle")

        layout.addWidget(icon)
        layout.addWidget(message_label)

        if details:
            details_box = QTextEdit()
            details_box.setReadOnly(True)
            details_box.setPlainText(details)
            details_box.setMaximumHeight(140)

            layout.addWidget(details_box)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)

        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
