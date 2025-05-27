import logging

from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Location
from worlds.generic.Rules import set_rule
from .locations import location_table, DredgeLocationData
from .items import item_table

if TYPE_CHECKING:
    from . import DredgeWorld


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


def set_location_rules(world: "DredgeWorld") -> None:
    player = world.player
    for location_name, location_id in world.player_location_table.items():
        location = location_table[location_name]
        world_location = world.get_location(location_name)
        match location.location_group:
            case "Encyclopedia":
                set_encyclopedia_rule(world_location, location, player)
            case "Research":
                set_research_rule(world_location, location, player)
            case "Relic" | "Shop" | "World" | "Quest":
                world_location.item_rule = lambda item: not item.advancement
            case _:
                set_rule(world.get_location(location_name), lambda state: True)


def has_engines(number: int, state: CollectionState, player: int) -> bool:
    ##return state.has("Progressive Engine", player, number)
    return True


def has_relics(state: CollectionState, player: int) -> bool:
    return state.has("Ornate Key", player) \
        and state.has("Rusted Music Box", player) \
        and state.has("Jewel Encrusted Band", player) \
        and state.has("Shimmering Necklace", player) \
        and state.has("Antique Pocket Watch", player)

def set_research_rule(world_location: Location, location: DredgeLocationData, player: int) -> None:
    set_rule(world_location,
             lambda state, requirement=location.requirement: can_research(state, requirement, player))

def can_research(state: CollectionState, requirement: str, player: int) -> bool:
    match requirement:
        case "Early":
            return state.count("Research Part", player) >= 3
        case "Mid":
            return state.count("Research Part", player) >= 7
        case "Late":
            return state.count("Research Part", player) >= 10
        case "All":
            return state.count("Research Part", player) >= 13
        case _:
            return True

def set_encyclopedia_rule(world_location: Location, location: DredgeLocationData, player: int) -> None:
    set_rule(
        world_location,
        lambda state, requirement=location.requirement, is_iron_rig=(location.expansion == "IronRig"): can_catch(
            requirement, is_iron_rig, state, player
        ),
    )

def can_catch(requirement: str, is_iron_rig: bool, state: CollectionState, player: int) -> bool:
    if requirement == "Crab":
        return state.has_any(get_harvest_tool_by_requirement(requirement), player)
    else:
        return state.has_any(get_harvest_tool_by_requirement(requirement), player) or (
            is_iron_rig and state.has_any(get_harvest_tool_by_requirement(requirement, is_iron_rig), player))


def get_harvest_tool_by_requirement(requirement: str, is_iron_rig: bool = False) -> list:
    return [name for name, item in item_table.items()
            if requirement in item.can_catch and (not is_iron_rig or item.expansion == "IronRig")
            ]
