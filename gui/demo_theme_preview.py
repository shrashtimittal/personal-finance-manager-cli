import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QHBoxLayout
)

app = QApplication(sys.argv)

# Load global theme
with open("gui/styles/theme.qss", "r") as f:
    app.setStyleSheet(f.read())

# Root window
window = QWidget()
window.setWindowTitle("Theme Preview")
window.resize(500, 400)

main_layout = QVBoxLayout(window)
main_layout.setSpacing(16)
main_layout.setContentsMargins(24, 24, 24, 24)

# Page title
title = QLabel("Dashboard")
title.setObjectName("PageTitle")
main_layout.addWidget(title)

# Card
card = QFrame()
card_layout = QVBoxLayout(card)
card_layout.setSpacing(12)
card_layout.setContentsMargins(16, 16, 16, 16)

section = QLabel("Quick Action")
section.setObjectName("SectionTitle")
card_layout.addWidget(section)

input_field = QLineEdit()
input_field.setPlaceholderText("Enter amount")
card_layout.addWidget(input_field)

# Buttons row
btn_row = QHBoxLayout()

primary_btn = QPushButton("Add Income")
secondary_btn = QPushButton("Cancel")
secondary_btn.setObjectName("SecondaryButton")
danger_btn = QPushButton("Delete")
danger_btn.setObjectName("DangerButton")

btn_row.addWidget(primary_btn)
btn_row.addWidget(secondary_btn)
btn_row.addWidget(danger_btn)

card_layout.addLayout(btn_row)

# Status text
success = QLabel("Transaction added successfully")
success.setObjectName("SuccessText")

error = QLabel("Over budget warning")
error.setObjectName("DangerText")

card_layout.addWidget(success)
card_layout.addWidget(error)

main_layout.addWidget(card)

window.show()
sys.exit(app.exec())
