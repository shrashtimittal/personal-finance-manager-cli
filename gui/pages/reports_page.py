from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTabWidget, QMessageBox
)
from PySide6.QtCore import Qt

from gui.widgets.charts import BarChart, LineChart, PieChart
from gui.utils.exporter import export_to_csv


class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.controller = None

        self._init_ui()

    # ===============================
    # CONTROLLER BINDING
    # ===============================
    def set_controller(self, controller):
        self.controller = controller
        self._load_reports()

    # ===============================
    # UI SETUP
    # ===============================
    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # -------------------------------
        # HEADER
        # -------------------------------
        header = QHBoxLayout()
        title = QLabel("Reports")
        title.setObjectName("PageTitle")

        self.export_btn = QPushButton("Export CSV")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.export_btn)
        main_layout.addLayout(header)

        # -------------------------------
        # TABS
        # -------------------------------
        self.tabs = QTabWidget()

        self.monthly_tab = QWidget()
        self.yearly_tab = QWidget()
        self.category_tab = QWidget()
        self.comparison_tab = QWidget()

        self.tabs.addTab(self.monthly_tab, "Monthly")
        self.tabs.addTab(self.yearly_tab, "Yearly")
        self.tabs.addTab(self.category_tab, "Category-wise")
        self.tabs.addTab(self.comparison_tab, "Income vs Expense")

        main_layout.addWidget(self.tabs)

        # -------------------------------
        # CHARTS
        # -------------------------------
        self.monthly_chart = BarChart()
        self.yearly_chart = LineChart()
        self.category_chart = PieChart()
        self.comparison_chart = BarChart()

        self._setup_tab(self.monthly_tab, self.monthly_chart)
        self._setup_tab(self.yearly_tab, self.yearly_chart)
        self._setup_tab(self.category_tab, self.category_chart)
        self._setup_tab(self.comparison_tab, self.comparison_chart)

        self.export_btn.clicked.connect(self._export_current_tab)

    def _setup_tab(self, tab: QWidget, chart):
        layout = QVBoxLayout(tab)
        layout.addWidget(chart)

    # ===============================
    # LOAD REPORTS (CONTROLLER)
    # ===============================
    def _load_reports(self):
        if not self.controller or not self.controller.state.is_authenticated:
            return

        data = self.controller.get_reports_data()
        state = self.controller.state

        # -------- Monthly
        income, expense, _ = data["monthly"]
        self.monthly_chart.plot(
            labels=["Income", "Expense"],
            values=[income, expense],
            title=f"Monthly Report ({state.year}-{state.month:02d})"
        )

        # -------- Yearly Trend
        breakdown = data["breakdown"]
        months = sorted(breakdown.keys())
        expenses = [breakdown[m]["expense"] for m in months]

        self.yearly_chart.plot(
            x_values=months,
            y_values=expenses,
            title=f"Yearly Expense Trend ({state.year})"
        )

        # -------- Category-wise
        category_summary = data["categories"]

        categories = list(category_summary.keys())
        expenses = [
            item["expense"] for item in category_summary.values()
        ]

        self.category_chart.plot(
            labels=categories,
            values=expenses,
            title="Category-wise Expense Distribution"
        )

        # -------- Income vs Expense (All-time)
        income, expense, _ = data["income_vs_expense"]
        self.comparison_chart.plot(
            labels=["Income", "Expense"],
            values=[income, expense],
            title="Income vs Expense (All Time)"
        )

    # ===============================
    # EXPORT CSV (CONTROLLER)
    # ===============================
    def _export_current_tab(self):
        if not self.controller:
            return

        data = self.controller.get_reports_data()
        state = self.controller.state

        tab = self.tabs.currentIndex()

        if tab == 0:
            income, expense, savings = data["monthly"]
            rows = [
                {"metric": "Income", "amount": income},
                {"metric": "Expense", "amount": expense},
                {"metric": "Savings", "amount": savings},
            ]
            columns = ["metric", "amount"]
            prefix = "monthly_report"

        elif tab == 1:
            income, expense, savings = data["yearly"]
            rows = [
                {"metric": "Income", "amount": income},
                {"metric": "Expense", "amount": expense},
                {"metric": "Savings", "amount": savings},
            ]
            columns = ["metric", "amount"]
            prefix = "yearly_report"

        elif tab == 2:
            summary = data["categories"]
            rows = [
                {
                    "category": cat,
                    "income": item["income"],
                    "expense": item["expense"]
                }
                for cat, item in summary.items()
            ]
            columns = ["category", "income", "expense"]
            prefix = "category_summary"

        else:
            income, expense, savings = data["income_vs_expense"]
            rows = [
                {"metric": "Income", "amount": income},
                {"metric": "Expense", "amount": expense},
                {"metric": "Savings", "amount": savings},
            ]
            columns = ["metric", "amount"]
            prefix = "income_vs_expense"

        success, result = export_to_csv(rows, columns, prefix)

        if success:
            QMessageBox.information(
                self, "Export Successful",
                f"Report exported to:\n{result}"
            )
        else:
            QMessageBox.warning(
                self, "Export Failed",
                result
            )
