from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplGraph(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

        # Dark theme defaults
        self.fig.set_facecolor("#151922")
        self.ax.set_facecolor("#151922")

        self.ax.tick_params(colors="#cfd6e4")
        for spine in self.ax.spines.values():
            spine.set_color("#2a2f3a")

        self.ax.title.set_color("#e6e9ef")
        self.ax.xaxis.label.set_color("#cfd6e4")
        self.ax.yaxis.label.set_color("#cfd6e4")

        self.ax.grid(True, alpha=0.25)

    def plot_timeseries(self, x, y, title: str, ylabel: str):
        self.ax.clear()

        # Re-apply dark styling after clear()
        self.ax.set_facecolor("#151922")
        self.ax.tick_params(colors="#cfd6e4")
        for spine in self.ax.spines.values():
            spine.set_color("#2a2f3a")
        self.ax.grid(True, alpha=0.25)

        if not x or not y:
            self.ax.text(
                0.5, 0.5, "No data yet",
                ha="center", va="center",
                transform=self.ax.transAxes,
                color="#9aa6b2",
                fontsize=12,
                fontweight="600"
            )
            self.ax.set_title(title, color="#e6e9ef", fontsize=13, fontweight="600")
            self.ax.set_ylabel(ylabel)
            self.draw()
            return

        # Plot
        self.ax.plot(x, y, marker="o", linewidth=2)

        self.ax.set_title(title)
        self.ax.set_ylabel(ylabel)

        # Make dates readable
        self.fig.autofmt_xdate(rotation=30, ha="right")

        self.draw()
