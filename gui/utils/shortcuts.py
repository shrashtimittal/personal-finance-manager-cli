from PySide6.QtGui import QKeySequence, QAction


class ShortcutManager:
    """
    Centralized keyboard shortcut manager.
    Keeps shortcuts declarative and reusable.
    """

    def __init__(self, window):
        self.window = window
        self._register_global_shortcuts()
        self._register_context_shortcuts()

    # ===============================
    # GLOBAL NAVIGATION SHORTCUTS
    # ===============================
    def _register_global_shortcuts(self):
        self._add_shortcut(
            "Ctrl+D", lambda: self.window._navigate("dashboard")
        )
        self._add_shortcut(
            "Ctrl+T", lambda: self.window._navigate("transactions")
        )
        self._add_shortcut(
            "Ctrl+B", lambda: self.window._navigate("budgets")
        )
        self._add_shortcut(
            "Ctrl+R", lambda: self.window._navigate("reports")
        )
        self._add_shortcut(
            "Ctrl+I", lambda: self.window._navigate("insights")
        )

    # ===============================
    # CONTEXT-SPECIFIC SHORTCUTS
    # ===============================
    def _register_context_shortcuts(self):
        # Transactions
        self._add_shortcut(
            "Ctrl+N", self._add_transaction
        )
        self._add_shortcut(
            "Ctrl+F", self._focus_transaction_search
        )

        # Budgets
        self._add_shortcut(
            "Ctrl+E", self._edit_budget
        )

    # ===============================
    # ACTION HELPERS
    # ===============================
    def _add_transaction(self):
        page = self.window.transactions_page
        if page and page.isVisible():
            page._add_transaction()

    def _focus_transaction_search(self):
        page = self.window.transactions_page
        if page and page.isVisible():
            page.search_input.setFocus()

    def _edit_budget(self):
        page = self.window.budgets_page
        if page and page.isVisible():
            page._open_set_dialog()

    # ===============================
    # UTILITY
    # ===============================
    def _add_shortcut(self, sequence: str, handler):
        action = QAction(self.window)
        action.setShortcut(QKeySequence(sequence))
        action.triggered.connect(handler)
        self.window.addAction(action)
