from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel
)
from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

from gui.widgets.stat_card import StatCard


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.controller = None

        self._init_ui()

    # ===============================
    # CONTROLLER BINDING
    # ===============================
    def set_controller(self, controller):
        self.controller = controller
        self.refresh()

    # ===============================
    # UI SETUP
    # ===============================
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(28)
        layout.setContentsMargins(0, 0, 0, 0)

        # ===============================
        # KPI CARDS
        # ===============================
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(18)

        self.income_card = StatCard("Total Income", "₹0", "#2ECC71", "⬆")
        self.expense_card = StatCard("Total Expense", "₹0", "#E74C3C", "⬇")
        self.savings_card = StatCard("Savings", "₹0", "#2D3FE8", "💰")
        self.budget_card = StatCard("Budget Status", "—", "#9CA3AF", "📊")

        kpi_row.addWidget(self.income_card)
        kpi_row.addWidget(self.expense_card)
        kpi_row.addWidget(self.savings_card)
        kpi_row.addWidget(self.budget_card)

        layout.addLayout(kpi_row)

        # ===============================
        # SNAPSHOT TITLE
        # ===============================
        title = QLabel("Monthly Snapshot")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)

        # ===============================
        # CHART
        # ===============================
        self.chart_view = self._create_chart()
        layout.addWidget(self.chart_view)

    # ===============================
    # DATA REFRESH
    # ===============================
    def refresh(self):
        if not self.controller or not self.controller.state.is_authenticated:
            return

        # -------------------------------
        # DASHBOARD SUMMARY
        # -------------------------------
        summary = self.controller.get_dashboard_summary()

        self.income_card.set_value(f"₹{summary['income']:.2f}")
        self.expense_card.set_value(f"₹{summary['expense']:.2f}")
        self.savings_card.set_value(f"₹{summary['savings']:.2f}")

        # -------------------------------
        # BUDGET STATUS
        # -------------------------------
        self._update_budget_status()

        # -------------------------------
        # MONTHLY CHART
        # -------------------------------
        income = summary["income"]
        expense = summary["expense"]
        self._update_chart(income, expense)

    # ===============================
    # BUDGET STATUS (CONTROLLER-DRIVEN)
    # ===============================
    def _update_budget_status(self):
        insights = self.controller.get_insights()

        label = self.budget_card.value_label

        if not insights:
            label.setText("No Budget")
            label.setStyleSheet("font-size: 26px; font-weight: 600; color: #9CA3AF;")
            return

        status = "Safe"
        color = "#2ECC71"

        for item in insights:
            if item["status"] == "Over Budget":
                status = "Over Budget"
                color = "#E74C3C"
                break
            elif item["status"] == "Near Limit":
                status = "Near Limit"
                color = "#F59E0B"

        label.setText(status)
        label.setStyleSheet(
            f"font-size: 26px; font-weight: 600; color: {color};"
        )

    # ===============================
    # CHART CREATION
    # ===============================
    def _create_chart(self):
        self.income_set = QBarSet("Income")
        self.expense_set = QBarSet("Expense")

        self.income_set.setColor(Qt.green)
        self.expense_set.setColor(Qt.red)

        series = QBarSeries()
        series.append(self.income_set)
        series.append(self.expense_set)
        series.setBarWidth(0.5)

        chart = QChart()
        chart.addSeries(series)
        chart.setBackgroundVisible(False)
        chart.setTitle("Income vs Expense (Selected Month)")
        chart.legend().setAlignment(Qt.AlignBottom)

        axis_x = QBarCategoryAxis()
        axis_x.append(["Month"])
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumHeight(320)

        return chart_view

    # ===============================
    # CHART UPDATE
    # ===============================
    def _update_chart(self, income: float, expense: float):
        self.income_set.remove(0, self.income_set.count())
        self.expense_set.remove(0, self.expense_set.count())

        self.income_set.append(income)
        self.expense_set.append(expense)
