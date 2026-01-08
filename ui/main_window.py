# ui/main_window.py

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QSizePolicy,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tracker")
        self.setMinimumSize(900, 650)

        # ---- Central container ----
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        # ---- Create widgets (exposed for controller) ----
        # Left (Aspect)
        self.aspect_combo = QComboBox()
        self.aspect_combo.addItem("Select aspect...")

        self.aspect_level_combo = QComboBox()
        self.aspect_level_combo.addItem("Lvl")
        self.aspect_level_combo.setFixedWidth(80)

        self.aspect_xp_input = QLineEdit()
        self.aspect_xp_input.setPlaceholderText("Enter XP")

        # Right (Chain)
        self.chain_combo = QComboBox()
        self.chain_combo.addItem("Select level...")

        self.chain_xp_input = QLineEdit()
        self.chain_xp_input.setPlaceholderText("Enter XP")

        # ---- Top controls row (2 columns) ----
        controls_row = QHBoxLayout()
        controls_row.setSpacing(18)

        left_controls = self._build_aspect_panel()
        right_controls = self._build_chain_panel()

        controls_row.addLayout(left_controls, 1)
        controls_row.addLayout(right_controls, 1)
        root.addLayout(controls_row)

        # ---- Graphs row (2 panels) ----
        graphs_row = QHBoxLayout()
        graphs_row.setSpacing(18)

        self.graph1_panel = self._placeholder_panel("Graph 1")
        self.graph2_panel = self._placeholder_panel("Graph 2")

        graphs_row.addWidget(self.graph1_panel, 1)
        graphs_row.addWidget(self.graph2_panel, 1)
        root.addLayout(graphs_row, 1)

        # ---- History panel (bottom, full width) ----
        history_group = QGroupBox("JSON Data History")
        history_layout = QVBoxLayout(history_group)
        history_layout.setContentsMargins(14, 14, 14, 14)

        self.history_table = QTableWidget(0, 4)
        self.history_table.setHorizontalHeaderLabels(
            ["Timestamp", "Aspect", "Aspect XP", "Chain Level"]
        )
        self.history_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(self.history_table.SelectRows)
        self.history_table.setEditTriggers(self.history_table.NoEditTriggers)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.horizontalHeader().setStretchLastSection(True)

        history_layout.addWidget(self.history_table, 1)
        root.addWidget(history_group, 1)

        # ---- Styling ----
        self._apply_styles()

    def _build_aspect_panel(self):
        """
        Aspect row 1:
          Aspect: [aspect_combo]  Level: [aspect_level_combo]
        Aspect row 2:
          Aspect XP: [aspect_xp_input]
        """
        layout = QGridLayout()
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # Row 1
        lbl_aspect = QLabel("Aspect:")
        lbl_aspect.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lbl_aspect.setMinimumWidth(110)

        row1 = QHBoxLayout()
        row1.setSpacing(8)

        level_label = QLabel("Level:")
        level_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.aspect_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        row1.addWidget(self.aspect_combo, 1)
        row1.addWidget(level_label, 0)
        row1.addWidget(self.aspect_level_combo, 0)

        layout.addWidget(lbl_aspect, 0, 0)
        layout.addLayout(row1, 0, 1)

        # Row 2
        lbl_xp = QLabel("Aspect XP:")
        lbl_xp.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lbl_xp.setMinimumWidth(110)

        self.aspect_xp_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout.addWidget(lbl_xp, 1, 0)
        layout.addWidget(self.aspect_xp_input, 1, 1)

        return layout

    def _build_chain_panel(self):
        """
        Chain row 1:
          Chain Level: [chain_combo]
        Chain row 2:
          Chain XP: [chain_xp_input]
        """
        layout = QGridLayout()
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl1 = QLabel("Chain Level:")
        lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lbl1.setMinimumWidth(110)

        self.chain_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        lbl2 = QLabel("Chain XP:")
        lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lbl2.setMinimumWidth(110)

        self.chain_xp_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout.addWidget(lbl1, 0, 0)
        layout.addWidget(self.chain_combo, 0, 1)
        layout.addWidget(lbl2, 1, 0)
        layout.addWidget(self.chain_xp_input, 1, 1)

        return layout

    def _placeholder_panel(self, title_text):
        frame = QFrame()
        frame.setObjectName("panelFrame")
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        frame.setMinimumHeight(320)

        lay = QVBoxLayout(frame)
        lay.setContentsMargins(12, 12, 12, 12)

        title = QLabel(title_text)
        title.setObjectName("panelTitle")
        title.setAlignment(Qt.AlignCenter)

        lay.addStretch(1)
        lay.addWidget(title)
        lay.addStretch(1)

        return frame

    def _apply_styles(self):
        base_font = QFont()
        base_font.setPointSize(10)
        self.setFont(base_font)

        self.setStyleSheet(
            """
            QMainWindow {
                background: #0f1115; /* main app background */
            }

            QWidget {
                color: #e6e9ef;      /* default text */
                font-size: 10pt;
            }

            QLabel {
                color: #e6e9ef;
            }

            /* --- Cards / Sections --- */
            QGroupBox {
                font-weight: 600;
                color: #e6e9ef;
                border: 1px solid #2a2f3a;
                border-radius: 12px;
                margin-top: 12px;
                background: #151922; /* card surface */
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
                color: #cfd6e4;
            }

            /* Graph placeholder panels */
            QFrame#panelFrame {
                background: #151922;
                border: 1px solid #2a2f3a;
                border-radius: 14px;
            }

            QLabel#panelTitle {
                font-size: 14px;
                font-weight: 600;
                color: #9aa6b2;
            }

            /* --- Inputs --- */
            QComboBox, QLineEdit {
                background: #0f131a;
                border: 1px solid #2a2f3a;
                border-radius: 10px;
                padding: 8px 10px;
                min-height: 18px;
                color: #e6e9ef;
                selection-background-color: #2b6de8; /* accent */
                selection-color: #ffffff;
            }

            QComboBox::drop-down {
                border: none;
                width: 28px;
            }

            QComboBox:focus, QLineEdit:focus {
                border: 1px solid #2b6de8; /* accent focus */
            }

            QLineEdit::placeholder {
                color: #7f8a98;
            }

            /* --- ComboBox dropdown list --- */
            QComboBox QAbstractItemView {
                background: #151922;              /* same as cards */
                color: #e6e9ef;
                border: 1px solid #2a2f3a;
                selection-background-color: #2b6de8;
                selection-color: #ffffff;
                outline: 0;
            }

            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
            }

            QComboBox QAbstractItemView::item:selected {
                background: #2b6de8;
                color: #ffffff;
            }

            /* --- Table / History --- */
            QTableWidget {
                border: 1px solid #2a2f3a;
                border-radius: 12px;
                background: #151922;
                gridline-color: #232834;
                color: #e6e9ef;
                selection-background-color: #203a72; /* subtle selection */
                selection-color: #ffffff;
            }

            QHeaderView::section {
                background: #111520;
                color: #cfd6e4;
                font-weight: 600;
                border: none;
                border-bottom: 1px solid #2a2f3a;
                padding: 8px;
            }

            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #1f2430;
            }

            QTableWidget::item:selected {
                background: #203a72;
                color: #ffffff;
            }

            /* --- Scrollbars (subtle, pro) --- */
            QScrollBar:vertical {
                background: transparent;
                width: 10px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: #2a2f3a;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3a4150;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """
        )


# Optional: run this file directly to preview just the UI.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
