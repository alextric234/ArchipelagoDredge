from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import DREDGEWorld

def create_and_connect_regions(world: DREDGEWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: DREDGEWorld) -> None:
    menu = Region("Menu", world.player, world.multiworld)
    the_marrows = Region("The Marrows", world.player, world.multiworld)
    open_ocean = Region("Open Ocean", world.player, world.multiworld)
    research = Region("Research", world.player, world.multiworld)
    gale_cliffs = Region("Gale Cliffs", world.player, world.multiworld)
    stellar_basin = Region("Stellar Basin", world.player, world.multiworld)
    twisted_strand = Region("Twisted Strand", world.player, world.multiworld)
    devils_spine = Region("Devil's Spine", world.player, world.multiworld)
    the_pale_reach = Region("The Pale Reach", world.player, world.multiworld)
    the_iron_rig = Region("The Iron Rig", world.player, world.multiworld)
    insanity = Region("Insanity", world.player, world.multiworld)

    regions = [
        menu,
        the_marrows,
        open_ocean,
        research,
        gale_cliffs,
        stellar_basin,
        twisted_strand,
        devils_spine,
        the_pale_reach,
        the_iron_rig,
        insanity
    ]

    world.multiworld.regions += regions

def connect_regions(world: DREDGEWorld) -> None:
    menu = world.get_region("Menu")
    the_marrows = world.get_region("The Marrows")
    open_ocean = world.get_region("Open Ocean")
    research = world.get_region("Research")
    gale_cliffs = world.get_region("Gale Cliffs")
    stellar_basin = world.get_region("Stellar Basin")
    twisted_strand = world.get_region("Twisted Strand")
    devils_spine = world.get_region("Devil's Spine")
    the_pale_reach = world.get_region("The Pale Reach")
    the_iron_rig = world.get_region("The Iron Rig")
    insanity = world.get_region("Insanity")

    menu.connect(the_marrows, "Menu to The Marrows")
    the_marrows.connect(open_ocean, "The Marrows to Open Ocean")
    the_marrows.connect(research, "The Marrows to Research")
    open_ocean.connect(gale_cliffs, "Open Ocean to Gale Cliffs")
    open_ocean.connect(stellar_basin, "Open Ocean to Stellar Basin")
    open_ocean.connect(twisted_strand, "Open Ocean to Twisted Strand")
    open_ocean.connect(devils_spine, "Open Ocean to Devil's Spine")
    open_ocean.connect(the_pale_reach, "Open Ocean to The Pale Reach")
    open_ocean.connect(the_iron_rig, "Open Ocean to The Iron Rig")
    open_ocean.connect(insanity, "Open Ocean to Insanity")