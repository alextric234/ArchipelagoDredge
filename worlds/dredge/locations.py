from __future__ import annotations

import json
import pkgutil

from typing import Dict, Set, TYPE_CHECKING

from BaseClasses import Location
from BaseClasses import LocationProgressType as LPT

from dataclasses import dataclass

from .options import DREDGEOptions

from . import items

if TYPE_CHECKING:
    from .world import DREDGEWorld

class DREDGELocation(Location):
    game: str = "DREDGE"

@dataclass
class DREDGELocationData:
    base_id_offset: int
    region: str
    location_group: str
    expansion: str
    requirement: str = ""
    can_catch_rod: bool = True
    can_catch_net: bool = False
    progress_type: LPT = LPT.DEFAULT
    is_aberration: bool = False
    is_exotic: bool = False
    iron_rig_phase: int = 0
    is_behind_debris: bool = False


location_base_id = 3459028911689314

def load_data_file(*args) -> dict:
    fname = "/".join(["data", *args])
    return json.loads(pkgutil.get_data(__name__, fname).decode())

location_table = {
    name: DREDGELocationData(
        base_id_offset=entry["base_id_offset"],
        region=entry["region"],
        location_group=entry["location_group"],
        expansion=entry["expansion"],
        requirement=entry.get("requirement", ""),
        can_catch_rod=entry.get("can_catch_rod", True),
        can_catch_net=entry.get("can_catch_net", False),
        progress_type=entry.get("progress_type", LPT.DEFAULT),
        is_aberration=entry.get("is_aberration", False),
        iron_rig_phase=entry.get("iron_rig_phase", 0),
    )
    for name, entry in load_data_file("locations.json").items()
}

LOCATION_NAME_TO_ID: Dict[str, int] = {name: location_base_id + data.base_id_offset for name, data in location_table.items()}

def get_player_location_table(options: DREDGEOptions) -> Dict[str, bool]:
    all_locations: Dict[str, bool] = {}
    base_locations = {name: location.is_aberration for (name, location)
                      in location_table.items() if location.expansion == "Base"}
    iron_rig_locations = {name: location.is_aberration for (name, location)
                      in location_table.items() if location.expansion == "IronRig"}
    pale_reach_locations = {name: location.is_aberration for (name, location)
                      in location_table.items() if location.expansion == "PaleReach"}
    both_dlc_locations = {name: location.is_aberration for (name, location)
                      in location_table.items() if location.expansion == "Both"}

    all_locations.update(base_locations)

    if options.include_iron_rig_dlc:
        all_locations.update(iron_rig_locations)
    if options.include_pale_reach_dlc:
        all_locations.update(pale_reach_locations)
    if options.include_pale_reach_dlc and options.include_iron_rig_dlc:
        all_locations.update(both_dlc_locations)

    # removing these checks while waiting for fix from mod
    excluded_groups = {"Shop", "Pursuit", "World", "Relic"}
    all_locations = {
        name: id
        for name, id in all_locations.items()
        if location_table[name].location_group not in excluded_groups
    }

    return all_locations

LOCATION_NAME_GROUPS: Dict[str, Set[str]] = {}
for loc_name, loc_data in location_table.items():
    loc_group_name = loc_name.split(" - ", 1)[0]
    LOCATION_NAME_GROUPS.setdefault(loc_group_name, set()).add(loc_name)
    if loc_data.location_group:
        LOCATION_NAME_GROUPS.setdefault(loc_data.location_group, set()).add(loc_name)

def create_all_locations(world: DREDGEWorld) -> None:
    create_locations(world)
    create_victory_event_location(world)

def create_locations(world: DREDGEWorld) -> None:
    for location_name, is_aberration in get_player_location_table(world.options).items():
        region = world.get_region(location_table[location_name].region)
        location_id = LOCATION_NAME_TO_ID[location_name]
        location = DREDGELocation(world.player, location_name, location_id, region)
        if is_aberration and not world.options.include_aberrations:
            location.progress_type = LPT.EXCLUDED
        region.locations.append(location)

def create_victory_event_location(world: DREDGEWorld) -> None:
    victory_region = world.get_region("Insanity")
    victory_region.add_event("The Collector", "Victory", location_type=DREDGELocation, item_type=items.DREDGEItem)