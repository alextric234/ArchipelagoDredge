import json
import pkgutil

from typing import Dict, Set

from BaseClasses import LocationProgressType as LPT
from dataclasses import dataclass
from .options import DredgeOptions

@dataclass
class DredgeLocationData:
    region: str
    location_group: str
    expansion: str
    requirement: str = ""
    can_catch_rod: bool = True
    can_catch_net: bool = False
    progress_type: LPT = LPT.DEFAULT
    is_aberration: bool = False
    iron_rig_phase: int = 0


location_base_id = 3459028911689314

def load_data_file(*args) -> dict:
    fname = "/".join(["data", *args])
    return json.loads(pkgutil.get_data(__name__, fname).decode())

location_table = {
    name: DredgeLocationData(
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

location_name_to_id: Dict[str, int] = {name: location_base_id + index for index, name in enumerate(location_table)}

def get_player_location_table(options: DredgeOptions) -> Dict[str, bool]:
    all_locations: Dict[str, bool] = {}
    base_locations = {name: location.is_aberration for (name, location)
                      in location_table.items() if location.expansion == "Base"}
    iron_rig_locations = {name: location.is_aberration for (name, location)
                      in location_table.items() if location.expansion == "IronRig"}
    pale_reach_locations = {name: location.is_aberration for (name, location)
                      in location_table.items() if location.expansion == "PaleReach"}

    all_locations.update(base_locations)

    if options.include_iron_rig_dlc:
        all_locations.update(iron_rig_locations)
    if options.include_pale_reach_dlc:
        all_locations.update(pale_reach_locations)

    # removing these checks while waiting for fix from mod
    excluded_groups = {"Shop", "Quest", "World", "Relic"}
    all_locations = {
        name: id
        for name, id in all_locations.items()
        if location_table[name].location_group not in excluded_groups
    }

    return all_locations

location_name_groups: Dict[str, Set[str]] = {}
for loc_name, loc_data in location_table.items():
    loc_group_name = loc_name.split(" - ", 1)[0]
    location_name_groups.setdefault(loc_group_name, set()).add(loc_name)
    if loc_data.location_group:
        location_name_groups.setdefault(loc_data.location_group, set()).add(loc_name)
