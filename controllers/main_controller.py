from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from datetime import datetime
from services.storage_service import StorageService, StorageConfig
from pathlib import Path
import json

class MainController:
    """
    Globals
    """
    ASPECT_XP_BY_LEVEL = {
        0: 500, 1: 1000, 2: 1500, 3: 2000, 4: 2500, 5: 3000, 6: 3500, 7: 4000,
        8: 4500, 9: 5000, 10: 15000, 11: 25000, 12: 40000, 13: 120000, 14: 250000
    }

    CHAIN_XP_BY_LEVEL = {
        1: 250000, 2: 500000, 3: 750000, 4: 1000000, 5: 1250000, 6: 1500000,
        7: 1750000, 8: 2000000, 9: 2250000, 10: 2500000, 11: 2750000, 12: 3000000,
        13: 3250000, 14: 3500000, 15: 3750000, 16: 4000000, 17: 4250000,
        18: 4500000, 19: 4750000, 20: 5000000, 21: 5250000, 22: 5500000,
        23: 5750000, 24: 6000000, 25: 6250000, 26: 6500000, 27: 6750000,
        28: 7000000, 29: 7250000, 30: 7500000
    }

    def __init__(self, window):
        self.window = window

        # instance state (if you actually need these)
        self.aspect_xp = 0
        self.chain_xp = 0

        # storage must exist before refresh_* uses it
        config = StorageConfig(data_dir=Path("data"))
        self.storage = StorageService(config)

        self.populate_dropdowns()
        self.connect_signals()
        self.validate_all()

        self.refresh_history()
        self.refresh_graphs()

    def populate_dropdowns(self):
        """
        Variables
        """
        aspect_choices = ["Air", "Arcane", "Artisan", "Blood", "Command", "Death", "Discipline", "Earth", "Eldritch",
                          "Fire", "Fortune", "Frost", "Gadget", "Harvest", "Holy", "Lightning", "Lyric", "Death",
                          "Madness", "Poison", "Shadow", "Void", "War", "Water"]
        aspect_levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        chain_levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

        self.set_combo_items(self.window.aspect_combo, items = aspect_choices, placeholder="Select an aspect")
        self.set_combo_items(self.window.aspect_level_combo, items = aspect_levels)
        self.set_combo_items(self.window.chain_combo, items = chain_levels, placeholder="Select mastery chain level")

    def connect_signals(self):

        """
        Connect UI events (signals) to controller methods
        """
        # Respond when dropdowns change
        self.window.aspect_combo.currentIndexChanged.connect(self.on_aspect_changed)
        self.window.aspect_level_combo.currentIndexChanged.connect(self.on_aspect_level_changed)
        self.window.chain_combo.currentIndexChanged.connect(self.on_chain_level_changed)

        # Validate numeric input on edit finished
        self.window.aspect_xp_input.editingFinished.connect(self.on_aspect_xp_edited)
        self.window.chain_xp_input.editingFinished.connect(self.on_chain_xp_edited)

        # Save button:
        self.window.save_button.clicked.connect(self.on_save_clicked)

        # Refresh graphs
        self.window.aspect_combo.currentIndexChanged.connect(self.refresh_graphs)
        self.window.aspect_level_combo.currentIndexChanged.connect(self.refresh_graphs)
        self.window.chain_combo.currentIndexChanged.connect(self.refresh_graphs)

    #region Event Handlers
    # ---------------------------
    # Event handlers
    # ---------------------------

    def on_aspect_changed(self):
        """
        Called when the Aspect Select dropdown changes.
        """
        self.validate_all()
        # Example idea: enable/disable inputs or update graphs
        # selected = self.window.aspect_combo.currentText()

    def on_aspect_level_changed(self):
        """
        Called when the Aspect Level dropdown changes.
        """
        self.validate_all()

    def on_chain_level_changed(self):
        """
        Called when the Chain Level dropdown changes.
        """
        self.validate_all()

    def on_aspect_xp_edited(self):
        """
        Called when the Aspect XP line edit loses focus / user presses Enter.
        Great place for lightweight validation feedback.
        """
        self.validate_all()

    def on_chain_xp_edited(self):
        """
        Called when the Chain XP line edit loses focus / user presses Enter.
        """
        self.validate_all()

    def on_save_clicked(self):
        current_aspect = self.window.aspect_combo.currentText()
        current_aspect_level = int(self.window.aspect_level_combo.currentText())

        current_aspect_xp = int(self.window.aspect_xp_input.text())
        current_chain_level = int(self.window.chain_combo.currentText())
        current_chain_xp = int(self.window.chain_xp_input.text())

        current_time_stamp = datetime.now().isoformat(timespec="seconds")

        entry = {
            "timestamp": current_time_stamp,
            "aspect": current_aspect,
            "aspect_level": current_aspect_level,
            "aspect_xp": current_aspect_xp,
            "chain_level": current_chain_level,
            "chain_xp": current_chain_xp,
        }
        self.storage.append_record(entry)
        self.refresh_history()
        self.refresh_graphs()

    #endregion

    # ---------------------------
    # UI refresh hooks (stubs)
    # ---------------------------

    def refresh_history(self):
        """
        Load JSON and render into history_table.
        """
        records = list(reversed(self.storage.load_history()))

        table = self.window.history_table
        table.setRowCount(0)

        if not records:
            return

        table.setRowCount(len(records))
        table.setColumnCount(6)

        for row, record in enumerate(records):
            ts_raw = record.get("timestamp", "")
            try:
                ts_display = datetime.fromisoformat(ts_raw).strftime("%B %d, %Y")
            except ValueError:
                ts_display = ts_raw

            values = [
                ts_display,
                record.get("aspect", ""),
                str(record.get("aspect_level", "")),
                str(record.get("aspect_xp", "")),
                str(record.get("chain_level", "")),
                str(record.get("chain_xp", "")),
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                table.setItem(row, col, item)

    def refresh_graphs(self):
        records = self.storage.load_history()

        # ---------- Graph 1: Aspect XP over time (selected aspect + selected level) ----------
        if self.window.aspect_combo.currentIndex() == 0 or self.window.aspect_level_combo.currentIndex() == 0:
            self.window.aspect_xp_graph.plot_timeseries([], [], "Aspect XP Over Time", "XP")
        else:
            selected_aspect = self.window.aspect_combo.currentText()

            # Convert selected aspect level to int
            level_text = self.window.aspect_level_combo.currentText()
            try:
                selected_level = int(level_text)
            except ValueError:
                selected_level = None

            if selected_level is None:
                self.window.aspect_xp_graph.plot_timeseries([], [], "Aspect XP Over Time", "XP")
            else:
                aspect_points = []
                for r in records:
                    if r.get("aspect") != selected_aspect:
                        continue
                    if r.get("aspect_level") != selected_level:
                        continue

                    ts = r.get("timestamp", "")
                    try:
                        dt = datetime.fromisoformat(ts)
                    except ValueError:
                        continue

                    axp = r.get("aspect_xp", None)
                    if axp is None:
                        continue

                    aspect_points.append((dt, int(axp)))

                aspect_points.sort(key=lambda t: t[0])
                x1 = [p[0] for p in aspect_points]
                y1 = [p[1] for p in aspect_points]

                self.window.aspect_xp_graph.plot_timeseries(
                    x1, y1, f"{selected_aspect} XP (Level {selected_level}) Over Time", "XP"
                )

        # ---------- Graph 2: Mastery Chain XP over time (selected chain level) ----------
        if self.window.chain_combo.currentIndex() == 0:
            self.window.aspect_level_graph.plot_timeseries([], [], "Mastery Chain XP Over Time", "XP")
            return

        # Convert selected chain level to int if possible
        chain_text = self.window.chain_combo.currentText()
        try:
            selected_chain_level = int(chain_text)
        except ValueError:
            # If your combo items are like "Level 2", parse digits instead
            digits = "".join(ch for ch in chain_text if ch.isdigit())
            selected_chain_level = int(digits) if digits else None

        if selected_chain_level is None:
            self.window.aspect_level_graph.plot_timeseries([], [], "Mastery Chain XP Over Time", "XP")
            return

        chain_points = []
        for r in records:
            if r.get("chain_level") != selected_chain_level:
                continue

            ts = r.get("timestamp", "")
            try:
                dt = datetime.fromisoformat(ts)
            except ValueError:
                continue

            cxp = r.get("chain_xp", None)
            if cxp is None:
                continue

            chain_points.append((dt, int(cxp)))

        chain_points.sort(key=lambda t: t[0])
        x2 = [p[0] for p in chain_points]
        y2 = [p[1] for p in chain_points]

        self.window.aspect_level_graph.plot_timeseries(
            x2, y2, f"Mastery Chain XP (Level {selected_chain_level}) Over Time", "XP"
        )

    # ---------------------------
    # Helpers
    # ---------------------------

    def set_combo_items(self, combo, items, placeholder=None):
        combo.blockSignals(True)
        combo.clear()
        if placeholder is not None:
            combo.addItem(placeholder)
        for item in items:
            combo.addItem(str(item))
        combo.blockSignals(False)

    def validate_all(self):
        # ---- Drop-down validity (placeholders are index 0) ----
        aspect_ok = self.window.aspect_combo.currentIndex() > 0
        level_ok = self.window.aspect_level_combo.currentIndex() > 0
        chain_ok = self.window.chain_combo.currentIndex() > 0

        # ---- XP fields validity ----
        # Acceptable input = passes validator; also require non-empty
        axp_text = self.window.aspect_xp_input.text().strip()
        cxp_text = self.window.chain_xp_input.text().strip()

        aspect_xp_ok = bool(axp_text) and self.window.aspect_xp_input.hasAcceptableInput()
        chain_xp_ok = bool(cxp_text) and self.window.chain_xp_input.hasAcceptableInput()

        # ---- Apply inline highlight (valid property -> stylesheet) ----
        self._set_valid(self.window.aspect_combo, aspect_ok)
        self._set_valid(self.window.aspect_level_combo, level_ok)
        self._set_valid(self.window.chain_combo, chain_ok)

        self._set_valid(self.window.aspect_xp_input, aspect_xp_ok)
        self._set_valid(self.window.chain_xp_input, chain_xp_ok)

        # ---- Save enabled only if everything is valid ----
        all_ok = aspect_ok and level_ok and chain_ok and aspect_xp_ok and chain_xp_ok
        self.window.save_button.setEnabled(all_ok)
    def _set_valid(self, widget, is_valid: bool):
        widget.setProperty("valid", "true" if is_valid else "false")
        widget.style().unpolish(widget)  # force stylesheet refresh
        widget.style().polish(widget)
