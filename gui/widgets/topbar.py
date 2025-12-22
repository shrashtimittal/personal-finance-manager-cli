from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QComboBox, QPushButton
from datetime import datetime


class TopBar(QFrame):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Page title
        self.title = QLabel("Dashboard")
        self.title.setObjectName("PageTitle")

        layout.addWidget(self.title)
        layout.addStretch()

        # Month selector
        self.month = QComboBox()
        self.month.addItems([
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ])
        self.month.setCurrentIndex(datetime.now().month - 1)

        # Year selector
        self.year = QComboBox()
        current_year = datetime.now().year
        for y in range(current_year - 5, current_year + 1):
            self.year.addItem(str(y))
        self.year.setCurrentText(str(current_year))

        # Export button
        self.export_btn = QPushButton("Export")
        self.export_btn.setObjectName("SecondaryButton")

        layout.addWidget(self.month)
        layout.addWidget(self.year)
        layout.addWidget(self.export_btn)
