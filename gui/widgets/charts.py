from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class BaseChart(QWidget):
    """
    Base chart widget embedding matplotlib into Qt.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)
        self._apply_style()

    def _apply_style(self):
        self.figure.patch.set_facecolor("#ffffff")
        self.ax.set_facecolor("#ffffff")

        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)

        self.ax.tick_params(axis="both", labelsize=9)
        self.figure.tight_layout()

    def clear(self):
        self.ax.clear()
        self._apply_style()


# ===============================
# BAR CHART
# ===============================
class BarChart(BaseChart):
    def plot(self, labels, values, title="", color="#4F46E5"):
        self.clear()

        self.ax.bar(labels, values, color=color)
        self.ax.set_title(title, fontsize=11)

        self.canvas.draw()


# ===============================
# LINE CHART
# ===============================
class LineChart(BaseChart):
    def plot(self, x_values, y_values, title="", color="#16A34A"):
        self.clear()

        self.ax.plot(x_values, y_values, marker="o", color=color)
        self.ax.set_title(title, fontsize=11)

        self.canvas.draw()


# ===============================
# PIE CHART
# ===============================
class PieChart(BaseChart):
    def plot(self, labels, values, title=""):
        self.clear()

        self.ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )
        self.ax.axis("equal")
        self.ax.set_title(title, fontsize=11)

        self.canvas.draw()
