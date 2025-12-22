from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt


class EmptyState(QWidget):
    """
    Reusable empty-state widget with optional illustration and action.
    """

    def __init__(
        self,
        title: str,
        message: str,
        icon: str = "📭",
        action_text: str | None = None,
        action_callback=None
    ):
        super().__init__()

        self._init_ui(title, message, icon, action_text, action_callback)

    def _init_ui(
        self,
        title: str,
        message: str,
        icon: str,
        action_text: str | None,
        action_callback
    ):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)
        layout.setContentsMargins(40, 40, 40, 40)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px;")

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("PageTitle")

        message_label = QLabel(message)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        message_label.setObjectName("SecondaryText")

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(message_label)

        if action_text and action_callback:
            action_btn = QPushButton(action_text)
            action_btn.clicked.connect(action_callback)
            layout.addSpacing(12)
            layout.addWidget(action_btn, alignment=Qt.AlignCenter)
