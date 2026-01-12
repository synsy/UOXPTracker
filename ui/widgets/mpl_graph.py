from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates


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
        self.ax.grid(True, alpha=0.25)

        # Hover/tooltip state
        self._line = None
        self._x = []
        self._y = []
        self._delta = []

        # Tooltip annotation (hidden until hover)
        self._tooltip = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(12, 12),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.35", fc="#0f131a", ec="#2a2f3a"),
            color="#e6e9ef",
            fontsize=10,
            visible=False,
        )

        # Mouse hover hook
        self.mpl_connect("motion_notify_event", self._on_hover)

    def plot_timeseries(self, x, y, title: str, ylabel: str):
        self.ax.clear()

        # Re-apply dark styling after clear()
        self.ax.set_facecolor("#151922")
        self.ax.tick_params(colors="#cfd6e4")
        for spine in self.ax.spines.values():
            spine.set_color("#2a2f3a")
        self.ax.grid(True, alpha=0.25)

        # Recreate tooltip after clear() (annotation lives on the Axes)
        self._tooltip = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(12, 12),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.35", fc="#0f131a", ec="#2a2f3a"),
            color="#e6e9ef",
            fontsize=10,
            visible=False,
        )

        self.ax.set_title(title, color="#e6e9ef", fontsize=13, fontweight="600")
        self.ax.set_ylabel(ylabel, color="#e6e9ef")

        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=6))

        if not x or not y:
            self.ax.text(
                0.5, 0.5, "No data yet",
                ha="center", va="center",
                transform=self.ax.transAxes,
                color="#9aa6b2",
                fontsize=12,
                fontweight="600"
            )
            # Clear hover state
            self._line = None
            self._x = []
            self._y = []
            self._delta = []
            self.draw()
            return

        # Store data for tooltip (ensure list-like)
        self._x = list(x)
        self._y = list(y)
        self._delta = [None] + [self._y[i] - self._y[i - 1] for i in range(1, len(self._y))]

        # Plot with a "near dot" hover radius:
        # - picker (in points) controls how close the mouse must be
        # - markersize affects dot size
        (self._line,) = self.ax.plot(
            self._x, self._y,
            marker="o",
            linewidth=2,
            markersize=5,
            picker=8,  # hover distance in points
        )

        # Make dates readable
        self.fig.autofmt_xdate(rotation=0)

        self.draw()

    def _on_hover(self, event):
        # Only respond when we're over this axes and have a plotted line
        if self._line is None or event.inaxes != self.ax:
            if self._tooltip.get_visible():
                self._tooltip.set_visible(False)
                self.draw_idle()
            return

        contains, info = self._line.contains(event)
        if not contains or "ind" not in info or not info["ind"]:
            if self._tooltip.get_visible():
                self._tooltip.set_visible(False)
                self.draw_idle()
            return

        idx = info["ind"][0]

        x_val = self._x[idx]
        y_val = self._y[idx]
        d_val = self._delta[idx]

        # Format date nicely if x is datetime-like
        try:
            date_str = x_val.strftime("%b %d, %Y")
        except Exception:
            date_str = str(x_val)

        if d_val is None:
            delta_str = "Δ XP: —"
        else:
            sign = "+" if d_val >= 0 else ""
            delta_str = f"Δ XP: {sign}{d_val:,}"

        text = f"{date_str}\nXP: {y_val:,}\n{delta_str}"

        self._tooltip.xy = (x_val, y_val)
        self._tooltip.set_text(text)
        self._tooltip.set_visible(True)
        self.draw_idle()
