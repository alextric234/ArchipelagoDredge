from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Location
from worlds.generic.Rules import set_rule, add_rule
from .items import item_table
from .locations import location_table, DREDGELocationData
from .options import DREDGEOptions

if TYPE_CHECKING:
    from . import DREDGEWorld

def set_all_rules(world: DREDGEWorld) -> None:
    set_region_rules(world)
    set_location_rules(world)
    set_completion_condition(world)

def set_region_rules(world: "DREDGEWorld") -> None:
    player = world.player

    world.get_entrance("Open Ocean to Gale Cliffs").access_rule = \
        lambda state: not world.options.require_engines or has_engines(1, state, player)
    world.get_entrance("Open Ocean to Stellar Basin").access_rule = \
        lambda state: not world.options.require_engines or has_engines(1, state, player)
    world.get_entrance("Open Ocean to Twisted Strand").access_rule = \
        lambda state: not world.options.require_engines or has_engines(1, state, player)
    world.get_entrance("Open Ocean to Devil's Spine").access_rule = \
        lambda state: not world.options.require_engines or has_engines(1, state, player)
    world.get_entrance("Open Ocean to The Iron Rig").access_rule = \
        lambda state: not world.options.require_engines or has_engines(2, state, player)
    world.get_entrance("Open Ocean to The Pale Reach").access_rule = \
        lambda state: not world.options.require_engines or has_engines(2, state, player)
    world.get_entrance("Open Ocean to Insanity").access_rule = \
        lambda state: has_relics(state, player)


def set_location_rules(world: "DREDGEWorld") -> None:
    player = world.player
    for world_location in world.get_locations():
        if world_location.name == "The Collector":
            continue
        location = location_table[world_location.name]
        match location.location_group:
            case "Encyclopedia":
                set_fish_rule(world_location, location, player, world.options)
            case "Research":
                set_research_rule(world_location, location, player)
            case "Dredge":
                set_dredge_rule(world_location, location, player)
            case "Relic" | "Shop" | "World" | "Pursuit":
                world_location.item_rule = lambda item: not item.advancement
            case _:
                set_rule(world_location, lambda state: True)

def set_dredge_rule(world_location: Location, location: DREDGELocationData, player: int) -> None:
    add_rule(world_location, lambda state: state.has("Dredge Crane", player))
    match location.requirement:
        case "explosives":
            add_rule(world_location, lambda state: state.has("Packed Explosives", player))
        case "icebreaker":
            add_rule(world_location, lambda state: state.has("Icebreaker", player))
        case "":
            return
        case _:
            #maybe log here
            return
    return


def has_engines(distance: int, state: CollectionState, player: int) -> bool:
    valid_engines = [name for name, item in item_table.items() if item.item_value >= distance]
    return state.has_any(valid_engines, player)

def has_relics(state: CollectionState, player: int) -> bool:
    return state.has("Ornate Key", player) \
        and state.has("Rusted Music Box", player) \
        and state.has("Jewel Encrusted Band", player) \
        and state.has("Shimmering Necklace", player) \
        and state.has("Antique Pocket Watch", player)

def set_research_rule(world_location: Location, location: DREDGELocationData, player: int) -> None:
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

def set_fish_rule(world_location: Location, location: DREDGELocationData, player: int, options: DREDGEOptions) -> None:
    set_rule(
        world_location,
        lambda state, is_iron_rig=(location.expansion == "IronRig"): can_catch(location, is_iron_rig, state, player, options),
    )

def can_catch(location: DREDGELocationData, is_iron_rig: bool, state: CollectionState, player: int, options: DREDGEOptions) -> bool:
    if location.is_behind_debris and not state.has("Packed Explosives", player):
        return False

    if location.requirement == "Crab":
        return state.has_any(get_harvest_tool_by_requirement(location.requirement, "Crab Pot"), player)
    else:
        if is_iron_rig and location.iron_rig_phase > 2:
            return can_catch_fish(is_iron_rig, location, player, state, options) \
                and state.has("Siphon Trawler", player)

        return can_catch_fish(is_iron_rig, location, player, state, options)


def can_catch_fish(is_iron_rig: bool, location: DREDGELocationData, player: int, state: CollectionState, options: DREDGEOptions) -> bool:
    has_rod = False
    has_net = False
    if location.can_catch_rod:
        if location.is_exotic and not state.has("Exotic Bait", player):
                return False

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

def set_completion_condition(world: DREDGEWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)