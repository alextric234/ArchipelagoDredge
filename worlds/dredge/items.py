from itertools import groupby
from typing import NamedTuple, Dict, Set

from BaseClasses import ItemClassification


class DredgeItemData(NamedTuple):
    classification: ItemClassification
    item_id_offset: int
    item_group: str = ""

item_base_id = 3459028911689314

item_table: Dict[str, DredgeItemData] = {
    "Basic Fishing Pole": DredgeItemData(ItemClassification.progression, 0, "Rods"),
}

def get_item_group(item_name: str) -> str:
    return item_table[item_name].item_group


item_name_to_id: Dict[str, int] = {name: item_base_id + data.item_id_offset for name, data in item_table.items()}

item_name_groups: Dict[str, Set[str]] = {
    group: set(item_names) for group, item_names in groupby(sorted(item_table, key=get_item_group), get_item_group) if group != ""
}