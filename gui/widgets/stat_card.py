from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class StatCard(QFrame):
    def __init__(self, title: str, value: str, accent_color: str, icon: str = ""):
        super().__init__()

        self.setMinimumHeight(130)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(8)

        # Title
        title_label = QLabel(f"{icon}  {title}" if icon else title)
        title_label.setObjectName("SecondaryText")

        # Value
        self.value_label = QLabel(value)
        self.value_label.setAlignment(Qt.AlignLeft)
        self.value_label.setStyleSheet(
            f"""
            font-size: 30px;
            font-weight: 600;
            color: {accent_color};
            """
        )

        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(self.value_label)

    def set_value(self, value: str):
        self.value_label.setText(value)
