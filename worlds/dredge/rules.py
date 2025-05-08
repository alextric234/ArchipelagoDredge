if TYPE_CHECKING:
    from . import DredgeWorld

def set_region_rules(world: "DredgeWorld")
    player = world.player
    world.get_entrance("Open Ocean -> Gale Cliffs").access_rule \
        lambda state: has_engines(1, state, player)
    world.get_entrance("Open Ocean -> Stellar Basin").access_rule \
        lambda state: has_engines(1, state, player)
    world.get_entrance("Open Ocean -> Twisted Strand").access_rule \
        lambda state: has_engines(1, state, player)
    world.get_entrance("Open Ocean -> Devil's Spine").access_rule \
        lambda state: has_engines(1, state, player)
    world.get_entrance("Open Ocean -> The Iron Rig").access_rule \
        lambda state: has_engines(1, state, player)
    world.get_entrance("Open Ocean -> The Pale Reach").access_rule \
        lambda state: has_engines(1, state, player)

def has_engines(number: int, state: CollectionState, player: int)
    return state.has("Engine Tier 1", player)
