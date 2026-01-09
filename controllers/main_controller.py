from PyQt5.QtWidgets import QMessageBox


class MainController:
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
        aspect_xp = 0
        chain_levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        chain_xp = 0

        self.set_combo_items(self.window.aspect_combo, items = aspect_choices, placeholder="Select an aspect")
        self.set_combo_items(self.window.aspect_level_combo, items = aspect_levels, placeholder="Current")
        self.set_combo_items(self.window.chain_combo, items = chain_levels, placeholder="Select mastery chain level")

    def connect_signals(self):
        return

    def refresh_history(self):
        return

    def refresh_graphs(self):
        return

    def set_combo_items(self, combo, items, placeholder=None):
        combo.blockSignals(True)
        combo.clear()
        if placeholder is not None:
            combo.addItem(placeholder)
        for item in items:
            combo.addItem(str(item))
        combo.blockSignals(False)
