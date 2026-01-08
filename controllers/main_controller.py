from PyQt5.QtWidgets import QMessageBox


class MainController:
    def __init__(self, window):
        self.window = window
        self.PopulateDropdowns()
        self.ConnectSignals()
        self.RefreshHistory()
        self.RefreshGraphs()

    def PopulateDropdowns(self):
        """
        Variables
        """
        aspect_choices = ["Air", "Arcane", "Artisan", "Blood", "Command", "Death", "Discipline", "Earth", "Eldritch",
                          "Fire", "Fortune", "Frost", "Gadget", "Harvest", "Holy", "Lightning", "Lyric", "Death",
                          "Madness", "Poison", "Shadow", "Void", "War", "Water"]
        aspect_levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        aspect_xp = 0
        chain_levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        chain_xp = 0



    def ConnectSignals(self):
        return

    def RefreshHistory(self):
        return

    def RefreshGraphs(self):
        return
