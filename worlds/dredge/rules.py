from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule
from .locations import location_table

if TYPE_CHECKING:
    from . import DredgeWorld, item_table


def set_region_rules(world: "DredgeWorld") -> None:
    player = world.player
    world.get_entrance("Open Ocean -> Gale Cliffs").access_rule = \
        lambda state: has_engines(1, state, player)
    world.get_entrance("Open Ocean -> Stellar Basin").access_rule = \
        lambda state: has_engines(1, state, player)
    world.get_entrance("Open Ocean -> Twisted Strand").access_rule = \
        lambda state: has_engines(1, state, player)
    world.get_entrance("Open Ocean -> Devil's Spine").access_rule = \
        lambda state: has_engines(1, state, player)
    world.get_entrance("Open Ocean -> The Iron Rig").access_rule = \
        lambda state: has_engines(2, state, player)
    world.get_entrance("Open Ocean -> The Pale Reach").access_rule = \
        lambda state: has_engines(2, state, player)
    world.get_entrance("Open Ocean -> Insanity").access_rule = \
        lambda state: has_relics(state, player)


def set_location_rule(location_name: str, world: "DredgeWorld") -> None:
    player = world.player
    print(f"Location name: {location_name}, keys: {list(location_table.keys())}")
    location = location_table[location_name]
    if location.requirement == "":
        return
    set_rule(world.get_location(location_name),
             lambda state: can_catch(location.requirement, location.expansion == "IronRig", state, player))


def has_engines(number: int, state: CollectionState, player: int) -> bool:
    return state.has("Progressive Engine", player, number)


def has_relics(state: CollectionState, player: int) -> bool:
    return state.has("Ornate Key", player) \
        and state.has("Rusted Music Box", player) \
        and state.has("Jewel Encrusted Band", player) \
        and state.has("Shimmering Necklace", player) \
        and state.has("Antique Pocket Watch", player)


def can_catch(requirement: str, is_iron_rig: bool, state: CollectionState, player: int) -> bool:
    return state.has_any(get_rods_by_requirement(requirement), player) or (
            is_iron_rig and state.has_any(get_rods_by_requirement(requirement, is_iron_rig), player)
    )


def get_rods_by_requirement(requirement: str, is_iron_rig: bool = False) -> list:
    return [name for name, item in item_table.items()
            if requirement in item.can_catch and (not is_iron_rig or item.expansion == "IronRig")
            ]
