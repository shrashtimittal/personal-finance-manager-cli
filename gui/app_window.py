from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget
)

from gui.widgets.sidebar import Sidebar
from gui.widgets.topbar import TopBar

from gui.pages.login_page import LoginPage
from gui.pages.register_page import RegisterPage
from gui.pages.dashboard_page import DashboardPage
from gui.pages.transactions_page import TransactionsPage
from gui.pages.budgets_page import BudgetsPage
from gui.pages.reports_page import ReportsPage
from gui.pages.insights_page import InsightsPage
from gui.pages.settings_page import SettingsPage

# Phase 10
from gui.state.app_state import AppState
from gui.controllers.app_controller import AppController

# Phase 11
from gui.utils.shortcuts import ShortcutManager
from gui.utils.animations import PageTransition
from gui.widgets.loader import Loader
from gui.dialogs.error_dialog import ErrorDialog


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Personal Finance Manager")
        self.resize(1200, 800)
        self.setMinimumSize(1000, 700)

        # ===============================
        # STATE & CONTROLLER
        # ===============================
        self.state = AppState()
        self.controller = AppController(self.state)

        self._init_ui()
        self._wire_auth_flow()
        self._wire_sidebar_nav()

        # ===============================
        # PHASE 11 UTILITIES
        # ===============================
        self.shortcuts = ShortcutManager(self)
        self.transitions = PageTransition(self.pages)

        self.loader = Loader("Loading…")
        self.loader.setParent(self)
        self.loader.hide()

        self._enter_auth_mode()

    # ===============================
    # UI SETUP
    # ===============================
    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(24)

        self.topbar = TopBar()
        content_layout.addWidget(self.topbar)

        self.pages = QStackedWidget()

        # ===============================
        # PAGES
        # ===============================
        self.login_page = LoginPage()
        self.register_page = RegisterPage()

        self.dashboard_page = DashboardPage()
        self.transactions_page = TransactionsPage()
        self.budgets_page = BudgetsPage()
        self.reports_page = ReportsPage()
        self.insights_page = InsightsPage()
        self.settings_page = SettingsPage()

        for page in [
            self.dashboard_page,
            self.transactions_page,
            self.budgets_page,
            self.reports_page,
            self.insights_page,
            self.settings_page
        ]:
            if hasattr(page, "set_controller"):
                page.set_controller(self.controller)

        for page in [
            self.login_page,
            self.register_page,
            self.dashboard_page,
            self.transactions_page,
            self.budgets_page,
            self.reports_page,
            self.insights_page,
            self.settings_page
        ]:
            self.pages.addWidget(page)

        content_layout.addWidget(self.pages)
        main_layout.addWidget(content_widget)

        self.page_map = {
            "dashboard": self.dashboard_page,
            "transactions": self.transactions_page,
            "budgets": self.budgets_page,
            "reports": self.reports_page,
            "insights": self.insights_page,
            "settings": self.settings_page,
        }

        self.page_titles = {
            "dashboard": "Dashboard",
            "transactions": "Transactions",
            "budgets": "Budgets",
            "reports": "Reports",
            "insights": "Insights",
            "settings": "Settings",
        }

    # ===============================
    # AUTH FLOW
    # ===============================
    def _wire_auth_flow(self):
        self.login_page.register_link.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.register_page)
        )

        self.register_page.login_link.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.login_page)
        )

        self.login_page.on_login_attempt = self._handle_login
        self.register_page.on_register_attempt = self._handle_register

    def _handle_login(self, username: str, password: str):
        self.loader.show_loader()
        try:
            success, message = self.controller.login(username, password)
            if success:
                self._enter_app_mode()
                self._navigate("dashboard")
            else:
                self.login_page.show_error(message)
        except Exception as e:
            ErrorDialog(
                title="Login Failed",
                message="Unable to sign in.",
                details=str(e),
                parent=self
            ).exec()
        finally:
            self.loader.hide_loader()

    def _handle_register(self, username: str, password: str):
        success, message = self.controller.register(username, password)
        if success:
            self.pages.setCurrentWidget(self.login_page)
        else:
            self.register_page.show_error(message)

    def _enter_auth_mode(self):
        self.sidebar.hide()
        self.topbar.hide()
        self.pages.setCurrentWidget(self.login_page)

    def _enter_app_mode(self):
        self.sidebar.show()
        self.topbar.show()

    # ===============================
    # NAVIGATION (WITH ANIMATION)
    # ===============================
    def _wire_sidebar_nav(self):
        self.sidebar.navigate.connect(self._navigate)

    def _navigate(self, key: str):
        if key not in self.page_map:
            return

        index = self.pages.indexOf(self.page_map[key])
        self.transitions.fade_to(index)

        self.topbar.title.setText(self.page_titles[key])
        self.sidebar.set_active(key)
