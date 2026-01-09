from PyQt5.QtWidgets import QMessageBox


class MainController:
    """
    Globals
    """
    aspect_xp = 0
    chain_xp = 0

    def __init__(self, window):
        self.window = window
        self.populate_dropdowns()
        self.connect_signals()
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
        # self.window.save_button.clicked.connect(self.on_save_clicked)

    #region Event Handlers
    # ---------------------------
    # Event handlers (stubs)
    # ---------------------------

    def on_aspect_changed(self):
        """
        Called when the Aspect Select dropdown changes.
        """
        # Example idea: enable/disable inputs or update graphs
        # selected = self.window.aspect_combo.currentText()
        pass

    def on_aspect_level_changed(self):
        """
        Called when the Aspect Level dropdown changes.
        """
        pass

    def on_chain_level_changed(self):
        """
        Called when the Chain Level dropdown changes.
        """
        pass

    def on_aspect_xp_edited(self):
        """
        Called when the Aspect XP line edit loses focus / user presses Enter.
        Great place for lightweight validation feedback.
        """
        #text = self.window.aspect_xp_input.text().strip()
        #if text and not self.is_number(text):
            #self.show_error("Aspect XP must be a number.")
            # Keep UI feedback minimal—don’t do heavy logic here yet.
        #else:
            #aspect_xp = text
        #pass

    def on_chain_xp_edited(self):
        """
        Called when the Chain XP line edit loses focus / user presses Enter.
        """
        #text = self.window.chain_xp_input.text().strip()
        #if text and not self._is_number(text):
            #self.show_error("Chain XP must be a number.")
        pass

    def on_save_clicked(self):
        """
        Stub for later:
        - Read values
        - Validate (controller/model)
        - Save (service)
        - Reload history + graphs
        """
        # entry = self.build_entry_from_ui()
        # if not entry_valid: show error and return
        # self.storage.append(entry)
        # self.refresh_history()
        # self.refresh_graphs()
        pass
    #endregion

    # ---------------------------
    # UI refresh hooks (stubs)
    # ---------------------------

    def refresh_history(self):
        """
        Later: load JSON and render into history_table.
        For now: do nothing.
        """
        pass

    def refresh_graphs(self):
        """
        Later: read data and render graphs into graph panels.
        For now: do nothing.
        """
        pass

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

    def is_number(self, text):
        # TODO - Implement input validation
        return True #if text.isdigit() else False

    def show_error(self, message, title = "Invalid Input"):
        # TODO - Upgrade this to inline field highlighting.
        QMessageBox.warning(self.window, title, message)