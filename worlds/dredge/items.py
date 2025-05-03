import json
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Dict, Set, List

from BaseClasses import ItemClassification


@dataclass
class DredgeItemData:
    classification: ItemClassification
    item_group: str
    expansion: str
    can_catch: List[str] = field(default_factory=list)
    size: int = 0

item_base_id = 3459028911689314

def load_item_table(json_path: str) -> Dict[str, DredgeItemData]:
    raw = json.loads(Path(json_path).read_text())
    return {
        name: DredgeItemData(
            classification=ItemClassification[entry["classification"]],
            item_group=entry["item_group"],
            expansion=entry["expansion"],
            can_catch=entry.get("can_catch", []),
            size=entry.get("size", 0),
        )
        for name, entry in raw.items()
    }

item_table: load_item_table("data/item_table_data.json")

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
