from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import date


@dataclass
class AppState:
    """
    Central runtime state for the GUI application.

    This class holds:
    - Current user session
    - Selected month / year
    - Cached summaries to avoid redundant backend calls

    NOTE:
    - No backend logic here
    - No GUI logic here
    - Pure state container
    """

    # ===============================
    # USER SESSION
    # ===============================
    user_id: Optional[int] = None
    is_authenticated: bool = False

    # ===============================
    # DATE CONTEXT
    # ===============================
    month: int = field(default_factory=lambda: date.today().month)
    year: int = field(default_factory=lambda: date.today().year)

    # ===============================
    # CACHED DATA (RUNTIME ONLY)
    # ===============================
    dashboard_cache: Dict[str, Any] = field(default_factory=dict)
    reports_cache: Dict[str, Any] = field(default_factory=dict)
    insights_cache: Dict[str, Any] = field(default_factory=dict)

    # ===============================
    # STATE HELPERS
    # ===============================
    def set_user(self, user_id: int):
        self.user_id = user_id
        self.is_authenticated = True
        self.clear_caches()

    def clear_user(self):
        self.user_id = None
        self.is_authenticated = False
        self.clear_caches()

    def set_period(self, month: int, year: int):
        if self.month != month or self.year != year:
            self.month = month
            self.year = year
            self.clear_caches()

    def clear_caches(self):
        self.dashboard_cache.clear()
        self.reports_cache.clear()
        self.insights_cache.clear()
