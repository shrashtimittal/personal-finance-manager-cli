import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from gui.app_window import AppWindow
from gui.splash_screen import AppSplashScreen
from gui.utils.paths import resource_path


def main():
    app = QApplication(sys.argv)

    # ===============================
    # LOAD GLOBAL STYLESHEET (SAFE)
    # ===============================
    try:
        with open(resource_path("gui/styles/theme.qss"), "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print("Failed to load theme:", e)

    # ===============================
    # SPLASH SCREEN
    # ===============================
    splash = AppSplashScreen()
    splash.show()

    def start_app():
        window = AppWindow()
        window.show()
        splash.finish(window)

    QTimer.singleShot(1200, start_app)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
