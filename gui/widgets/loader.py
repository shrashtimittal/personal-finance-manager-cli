from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QProgressBar
)
from PySide6.QtCore import Qt


class Loader(QWidget):
    """
    Lightweight non-blocking loading indicator.
    Can be overlaid on any widget.
    """

    def __init__(self, message: str = "Loading..."):
        super().__init__()

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            """
            background-color: rgba(255, 255, 255, 0.85);
            """
        )

        self._init_ui(message)

    def _init_ui(self, message: str):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        spinner = QProgressBar()
        spinner.setRange(0, 0)  # infinite / busy indicator
        spinner.setFixedWidth(200)

        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("SecondaryText")

        layout.addWidget(spinner)
        layout.addWidget(label)

    # ===============================
    # VISIBILITY HELPERS
    # ===============================
    def show_loader(self):
        self.show()
        self.raise_()

    def hide_loader(self):
        self.hide()
