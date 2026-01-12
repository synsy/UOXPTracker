from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QToolButton
from datetime import datetime
from services.storage_service import StorageService, StorageConfig
from pathlib import Path
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt


class MainController:
    """
    Globals
    """
    ASPECT_XP_BY_LEVEL = {
        0: 500, 1: 1000, 2: 1500, 3: 2000, 4: 2500, 5: 3000, 6: 3500, 7: 4000,
        8: 4500, 9: 5000, 10: 15000, 11: 25000, 12: 40000, 13: 120000, 14: 250000
    }

    CHAIN_XP_BY_LEVEL = {
        0: 250000, 1: 500000, 2: 750000, 3: 1000000, 4: 1250000, 5: 1500000,
        6: 1750000, 7: 2000000, 8: 2250000, 9: 2500000, 10: 2750000, 11: 3000000,
        12: 3250000, 13: 3500000, 14: 3750000, 15: 4000000, 16: 4250000,
        17: 4500000, 18: 4750000, 19: 5000000, 20: 5250000, 21: 5500000,
        22: 5750000, 23: 6000000, 24: 6250000, 25: 6500000, 26: 6750000,
        27: 7000000, 28: 7250000, 29: 7500000
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
                          "Fire", "Fortune", "Frost", "Gadget", "Harvest", "Holy", "Lightning", "Lyric",
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
        records = list(reversed(self.storage.load_history()))
        table = self.window.history_table

        table.setRowCount(0)
        table.setColumnCount(7)  # keep consistent even if empty

        if not records:
            return

        table.setRowCount(len(records))

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
                f"{record['aspect_xp']:,}",
                str(record.get("chain_level", "")),
                f"{record['chain_xp']:,}",
            ]

            # Fill columns 0..5
            for col, value in enumerate(values):
                table.setItem(row, col, QTableWidgetItem(value))

            # Delete button in column 6 (once per row)
            delete_btn = QToolButton()
            delete_btn.setText("x")
            delete_btn.setObjectName("deleteButton")
            delete_btn.setToolTip("Delete entry")
            delete_btn.setFixedSize(18, 18)
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.setProperty("timestamp", record.get("timestamp", ""))
            delete_btn.clicked.connect(lambda _, ts=record["timestamp"]: self.on_delete_row_clicked(ts))

            table.setCellWidget(row, 6, delete_btn)

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

        # ---- Progress Bars validity ----
        self.refresh_progress_bars()

    def refresh_progress_bars(self):
        records = self.storage.load_history()

        # ---------------- Aspect progress (by selected aspect + selected level) ----------------
        level_idx = self.window.aspect_level_combo.currentIndex()
        aspect_idx = self.window.aspect_combo.currentIndex()

        if aspect_idx == 0 or level_idx == 0:
            self.window.aspect_progress_bar.setValue(0)
            self.window.aspect_progress_bar.setFormat("0%")
        else:
            selected_aspect = self.window.aspect_combo.currentText()
            selected_level = int(self.window.aspect_level_combo.currentText())

            max_xp = self.ASPECT_XP_BY_LEVEL.get(selected_level, 0)

            # Find latest matching record (scan from end)
            latest_xp = None
            for r in reversed(records):
                if r.get("aspect") == selected_aspect and r.get("aspect_level") == selected_level:
                    latest_xp = int(r.get("aspect_xp", 0))
                    break

            if latest_xp is None or max_xp <= 0:
                self.window.aspect_progress_bar.setValue(0)
                self.window.aspect_progress_bar.setFormat(f"0 / {max_xp} (0%)" if max_xp else "0%")
            else:
                pct = max(0, min(100, int((latest_xp / max_xp) * 100)))
                self.window.aspect_progress_bar.setValue(pct)
                self.window.aspect_progress_bar.setFormat(f"{latest_xp:,} / {max_xp:,} ({pct}%)")

        # ---------------- Chain progress (by selected chain level) ----------------
        chain_idx = self.window.chain_combo.currentIndex()
        if chain_idx == 0:
            self.window.chain_progress_bar.setValue(0)
            self.window.chain_progress_bar.setFormat("—")
        else:
            selected_chain_level = int(self.window.chain_combo.currentText())
            max_xp = self.CHAIN_XP_BY_LEVEL.get(selected_chain_level, 0)

            latest_xp = None
            for r in reversed(records):
                if r.get("chain_level") == selected_chain_level:
                    latest_xp = int(r.get("chain_xp", 0))
                    break

            if latest_xp is None or max_xp <= 0:
                self.window.chain_progress_bar.setValue(0)
                self.window.chain_progress_bar.setFormat(f"0 / {max_xp} (0%)" if max_xp else "—")
            else:
                pct = max(0, min(100, int((latest_xp / max_xp) * 100)))
                self.window.chain_progress_bar.setValue(pct)
                self.window.chain_progress_bar.setFormat(f"{latest_xp} / {max_xp} ({pct}%)")

    def _set_valid(self, widget, is_valid: bool):
        widget.setProperty("valid", "true" if is_valid else "false")
        widget.style().unpolish(widget)  # force stylesheet refresh
        widget.style().polish(widget)

    def on_delete_row_clicked(self, ts_iso):
        if not ts_iso:
            return

        records = self.storage.load_history()
        new_records = [r for r in records if r.get("timestamp") != ts_iso]
        self.storage.save_history(new_records)

        self.refresh_history()
        self.refresh_graphs()


