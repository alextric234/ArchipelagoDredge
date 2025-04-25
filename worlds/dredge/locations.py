from typing import Dict, Set, NamedTuple


class DredgeLocationData(NamedTuple):
    region: str
    location_group: str = ""

location_base_id = 3459028911689314

location_table: Dict[str, DredgeLocationData] ={
    "Fish Monger 1": DredgeLocationData("Shop", "Open Ocean"),
}

standard_location_name_to_id: Dict[str, int] = {name: location_base_id + index for index, name in enumerate(location_table)}

location_name_groups: Dict[str, Set[str]] = {}
for loc_name, loc_data in location_table.items():
    loc_group_name = loc_name.split(" - ", 1)[0]
    location_name_groups.setdefault(loc_group_name, set()).add(loc_name)
    if loc_data.location_group:
        location_name_groups.setdefault(loc_data.location_group, set()).add(loc_name)