from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Location
from worlds.generic.Rules import set_rule
from .items import item_table
from .locations import location_table, DredgeLocationData
from .options import DredgeOptions

if TYPE_CHECKING:
    from . import DredgeWorld


def set_region_rules(world: "DredgeWorld") -> None:
    player = world.player

    world.get_entrance("Open Ocean -> Gale Cliffs").access_rule = \
        lambda state: not world.options.require_engines or has_engines(1, state, player)
    world.get_entrance("Open Ocean -> Stellar Basin").access_rule = \
        lambda state: not world.options.require_engines or has_engines(1, state, player)
    world.get_entrance("Open Ocean -> Twisted Strand").access_rule = \
        lambda state: not world.options.require_engines or has_engines(1, state, player)
    world.get_entrance("Open Ocean -> Devil's Spine").access_rule = \
        lambda state: not world.options.require_engines or has_engines(1, state, player)
    world.get_entrance("Open Ocean -> The Iron Rig").access_rule = \
        lambda state: not world.options.require_engines or has_engines(2, state, player)
    world.get_entrance("Open Ocean -> The Pale Reach").access_rule = \
        lambda state: not world.options.require_engines or has_engines(2, state, player)
    world.get_entrance("Open Ocean -> Insanity").access_rule = \
        lambda state: has_relics(state, player)


def set_location_rules(world: "DredgeWorld") -> None:
    player = world.player
    for location_name, location_id in world.player_location_table.items():
        location = location_table[location_name]
        world_location = world.get_location(location_name)
        match location.location_group:
            case "Encyclopedia":
                set_fish_rule(world_location, location, player, world.options)
            case "Research":
                set_research_rule(world_location, location, player)
            case "Relic" | "Shop" | "World" | "Quest":
                world_location.item_rule = lambda item: not item.advancement
            case _:
                set_rule(world.get_location(location_name), lambda state: True)


def has_engines(distance: int, state: CollectionState, player: int) -> bool:
    valid_engines = [name for name, item in item_table.items() if item.item_value >= distance]
    return state.has_any(valid_engines, player)


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

def set_fish_rule(world_location: Location, location: DredgeLocationData, player: int, options: DredgeOptions) -> None:
    set_rule(
        world_location,
        lambda state, is_iron_rig=(location.expansion == "IronRig"): can_catch(location, is_iron_rig, state, player, options),
    )

def can_catch(location: DredgeLocationData, is_iron_rig: bool, state: CollectionState, player: int, options: DredgeOptions) -> bool:
    if location.requirement == "Crab":
        return state.has_any(get_harvest_tool_by_requirement(location.requirement, "Crab Pot"), player)
    else:
        if is_iron_rig and location.iron_rig_phase > 2:
            return can_catch_fish(is_iron_rig, location, player, state, options) \
                and state.has("Siphon Trawler", player)

        return can_catch_fish(is_iron_rig, location, player, state, options)


def can_catch_fish(is_iron_rig: bool, location: DredgeLocationData, player: int, state: CollectionState, options: DredgeOptions) -> bool:
    has_rod = False
    has_net = False
    if location.can_catch_rod:
        has_rod = state.has_any(get_harvest_tool_by_requirement(location.requirement, "Rod"), player) or (
                is_iron_rig and state.has_any(get_harvest_tool_by_requirement(location.requirement, "Rod", is_iron_rig),
                                              player))
    if location.can_catch_net:
        if location.can_catch_rod and not options.logical_nets:
            has_net = False
        else:
            has_net = state.has_any(get_harvest_tool_by_requirement(location.requirement, "Net"), player) or (
                    is_iron_rig and state.has_any(
                get_harvest_tool_by_requirement(location.requirement, "Net", is_iron_rig), player))
    return has_rod or has_net


def get_harvest_tool_by_requirement(requirement: str, tool_type: str, is_iron_rig: bool = False) -> list:
    excluded_names = {"Tendon Rod", "Viscera Crane", "Bottomless Lines"}

    return [
        name
        for name, item in item_table.items()
        if requirement in item.can_catch
        and item.item_group == tool_type
        and (not is_iron_rig or item.expansion == "IronRig")
        and item.size <= 4
        and name not in excluded_names
    ]