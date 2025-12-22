from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class ConfirmDeleteDialog(QDialog):
    def __init__(self, message: str, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Confirm Delete")
        self.setModal(True)
        self.setFixedWidth(360)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        label = QLabel(message)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        cancel_btn = QPushButton("Cancel")
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("DangerButton")

        btn_row.addStretch()
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(delete_btn)

        layout.addLayout(btn_row)

        cancel_btn.clicked.connect(self.reject)
        delete_btn.clicked.connect(self.accept)
