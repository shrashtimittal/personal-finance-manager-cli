from PySide6.QtGui import QIcon
from gui.utils.paths import resource_path


def icon(name: str) -> QIcon:
    return QIcon(resource_path(f"assets/icons/{name}.svg"))


ICONS = {
    # Navigation
    "dashboard": icon("dashboard"),
    "transactions": icon("transactions"),
    "budgets": icon("budgets"),
    "reports": icon("reports"),
    "insights": icon("insights"),
    "settings": icon("settings"),

    # Actions
    "add": icon("add"),
    "edit": icon("edit"),
    "delete": icon("delete"),

    # Status
    "warning": icon("warning"),
    "success": icon("success"),
    "info": icon("info"),
}
