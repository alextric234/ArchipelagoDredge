import json
import pkgutil
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List

from BaseClasses import ItemClassification


@dataclass
class DredgeItemData:
    classification: ItemClassification
    item_group: str
    expansion: str
    can_catch: List[str] = field(default_factory=list)
    size: int = 0

item_base_id = 3459028911689314

def load_data_file(*args) -> dict:
    fname = "/".join(["data", *args])
    return json.loads(pkgutil.get_data(__name__, fname).decode())

item_table = {
    name: DredgeItemData(
        classification=ItemClassification[entry["classification"]],
        item_group=entry["item_group"],
        expansion=entry["expansion"],
        can_catch=entry.get("can_catch", []),
        size=entry.get("size", 0),
    )
    for name, entry in load_data_file("items.json").items()
}

def get_item_group(item_name: str) -> str:
    return item_table[item_name].item_group

item_name_to_id = {
    name: item_base_id + i
    for i, name in enumerate(item_table)
}

item_name_groups = defaultdict(set)
for name, data in item_table.items():
    if data.item_group:
        item_name_groups[data.item_group].add(name)
