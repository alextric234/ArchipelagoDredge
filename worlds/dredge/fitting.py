from __future__ import annotations

from functools import cache

from .items import item_table, load_data_file

# Hull cells each equipment group can use: N cells take rods or nets, R cells take rods only.
CELL_KINDS_BY_ITEM_GROUP = {"Rod": "RN", "Net": "N"}

HULL_LAYOUTS = load_data_file("hulls.json")

Cell = tuple[int, int]


def parse_cells(rows: list[str], kinds: str) -> set[Cell]:
    return {(x, y) for y, row in enumerate(rows) for x, kind in enumerate(row) if kind in kinds}


def rotations(shape: set[Cell]) -> list[set[Cell]]:
    result = []
    for _ in range(4):
        min_x = min(x for x, _ in shape)
        min_y = min(y for _, y in shape)
        result.append({(x - min_x, y - min_y) for x, y in shape})
        shape = {(y, -x) for x, y in shape}
    return result


def fits(shape: set[Cell], cells: set[Cell]) -> bool:
    for rotation in rotations(shape):
        anchor_x, anchor_y = next(iter(rotation))
        for cell_x, cell_y in cells:
            dx, dy = cell_x - anchor_x, cell_y - anchor_y
            if all((x + dx, y + dy) in cells for x, y in rotation):
                return True
    return False


@cache
def hulls_needed(item_name: str, include_iron_rig: bool) -> int:
    item = item_table.get(item_name)
    kinds = CELL_KINDS_BY_ITEM_GROUP.get(item.item_group) if item else None
    if kinds is None or not item.shape:
        return 0

    shape = parse_cells(item.shape, "X")
    layouts = HULL_LAYOUTS["with_iron_rig" if include_iron_rig else "without_iron_rig"]
    for hull_count, rows in enumerate(layouts):
        if fits(shape, parse_cells(rows, kinds)):
            return hull_count
    raise ValueError(f"{item_name} doesn't fit on any hull")
