from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QTimer


class Toast(QWidget):
    """
    Lightweight, non-blocking toast notification.
    """

    def __init__(
        self,
        parent,
        message: str,
        level: str = "info",
        duration: int = 3000
    ):
        super().__init__(parent)

        self.message = message
        self.level = level
        self.duration = duration

        self._init_ui()
        self._position()
        self._auto_close()

    # ===============================
    # UI SETUP
    # ===============================
    def _init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)

        label = QLabel(self.message)
        label.setWordWrap(True)
        label.setObjectName("ToastLabel")

        layout.addWidget(label)

        self._apply_style()

    # ===============================
    # POSITION (BOTTOM-RIGHT)
    # ===============================
    def _position(self):
        parent_rect = self.parent().geometry()
        self.adjustSize()

        x = parent_rect.right() - self.width() - 20
        y = parent_rect.bottom() - self.height() - 20

        self.move(x, y)
        self.show()

    # ===============================
    # AUTO CLOSE
    # ===============================
    def _auto_close(self):
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self.close)
        timer.start(self.duration)

    # ===============================
    # STYLE
    # ===============================
    def _apply_style(self):
        color_map = {
            "success": "#2ecc71",
            "error": "#e74c3c",
            "warning": "#f39c12",
            "info": "#3498db",
        }

        bg = color_map.get(self.level, "#3498db")

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg};
                border-radius: 8px;
            }}
            QLabel#ToastLabel {{
                color: white;
                font-size: 13px;
            }}
        """)
