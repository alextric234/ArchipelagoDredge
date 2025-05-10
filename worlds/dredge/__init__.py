from typing import List, Dict, Any

from BaseClasses import Tutorial, Location, Item, ItemClassification, Region
from worlds.AutoWorld import World, WebWorld
from .items import item_name_to_id, item_name_groups, item_table
from .locations import location_name_groups, location_table, location_name_to_id
from .options import DredgeOptions
# from .rules import set_location_rule
from .regions import dredge_regions

class DredgeWeb(WebWorld):
    tutorials = [Tutorial(
        tutorial_name="Multiworld Setup Guide",
        description="A guide to setting up the Dredge for Archipelago multiworld games.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["Alextric"]
    )]
    theme = "ocean"
    game = "Dredge"

class DredgeItem(Item):
    game: str = "Dredge"

class DredgeLocation(Location):
    game: str = "Dredge"

class DredgeWorld(World):
    """
    Sell your catch, upgrade your boat, and dredge the depths for long-buried secrets. Explore a mysterious archipelago
    and discover why some things are best left forgotten.
    """

    game = "Dredge"
    web = DredgeWeb()
    options: DredgeOptions
    options_dataclass = DredgeOptions
    item_name_groups = item_name_groups
    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    location_name_groups = location_name_groups

    def generate_early(self) -> None:
        self.player_location_table = location_name_to_id.copy()

    def create_item(self, name: str, classification: ItemClassification = None) -> DredgeItem:
        item_data = item_table[name]
        return DredgeItem(name, item_data.classification, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        dredge_items: List[DredgeItem] = []

        for item, data in item_table.items():
            if data.expansion == "Base":
                dredge_items.append(self.create_item(item, data.classification))
            if self.options.include_pale_reach_dlc and data.expansion == "PaleReach":
                dredge_items.append(self.create_item(item, data.classification))
            if self.options.include_iron_rig_dlc and data.expansion == "IronRig":
                dredge_items.append(self.create_item(item, data.classification))

        self.multiworld.itempool += dredge_items

    def create_regions(self) -> None:
        for region_name in dredge_regions:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        for region_name, exits in dredge_regions.items():
            region = self.get_region(region_name)
            region.add_exits(exits)

        for location_name, location_id in self.player_location_table.items():
            if location_table[location_name].expansion == "PaleReach" and not self.options.include_pale_reach_dlc:
                continue
            if location_table[location_name].expansion == "IronRig" and not self.options.include_iron_rig_dlc:
                continue
            region = self.get_region(location_table[location_name].region)
            location = DredgeLocation(self.player, location_name, location_id, region)
            # set_location_rules(location)
            region.locations.append(location)

            victory_region = self.get_region("Insanity")
            victory_location = DredgeLocation(self.player, "The Collector", None, victory_region)
            victory_location.place_locked_item(DredgeItem("Victory",
                                                          ItemClassification.progression,
                                                          None, self.player))
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
            victory_region.locations.append(victory_location)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            # "goal": self.options.goal.value,
            "include_iron_rig_dlc": self.options.include_iron_rig_dlc.value,
            # "require_iron_rig_ending": self.options.require_iron_rig_ending.value,
            "include_pale_reach_dlc": self.options.include_pale_reach_dlc.value,
            # "require_pale_reach_ending": self.options.require_pale_reach_ending.value,
            # "enable_traps": self.options.enable_traps.value,
        }
        return slot_data
