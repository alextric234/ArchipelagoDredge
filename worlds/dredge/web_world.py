from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

class DREDGEWebWorld(WebWorld):
    tutorials = [Tutorial(
        tutorial_name="Multiworld Setup Guide",
        description="A guide to setting up DREDGE for Archipelago multiworld games.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["Alextric"]
    )]
    theme = "ocean"
    game = "DREDGE"