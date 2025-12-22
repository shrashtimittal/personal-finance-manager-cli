from PySide6.QtWidgets import QSplashScreen
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from PySide6.QtCore import Qt


class AppSplashScreen(QSplashScreen):
    def __init__(self):
        # Create blank pixmap
        pixmap = QPixmap(480, 300)
        pixmap.fill(QColor("#0F172A"))  # dark slate background

        super().__init__(pixmap)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self._draw_content()

    def _draw_content(self):
        painter = QPainter(self.pixmap())
        painter.setRenderHint(QPainter.Antialiasing)

        # App title
        painter.setPen(QColor("#E5E7EB"))
        painter.setFont(QFont("Segoe UI", 26, QFont.Bold))
        painter.drawText(
            self.pixmap().rect(),
            Qt.AlignCenter | Qt.AlignTop,
            "\n\nPersonal Finance Manager"
        )

        # Tagline
        painter.setFont(QFont("Segoe UI", 12))
        painter.setPen(QColor("#9CA3AF"))
        painter.drawText(
            self.pixmap().rect(),
            Qt.AlignCenter,
            "Smart tracking • Better decisions"
        )

        # Loading text
        painter.setFont(QFont("Segoe UI", 10))
        painter.setPen(QColor("#6EE7B7"))
        painter.drawText(
            self.pixmap().rect().adjusted(0, 0, 0, -24),
            Qt.AlignBottom | Qt.AlignCenter,
            "Loading application..."
        )

        painter.end()
