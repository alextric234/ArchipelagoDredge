if TYPE_CHECKING:
    from . import DredgeWorld

def set_region_rules(world: "DredgeWorld")
    player = world.player
    world.get_entrance("Open Ocean -> Gale Cliffs").access_rule \
        lambda state: has_engines(1, state, player)

def has_engines(number: int, state: CollectionState, player: int)
    return state.has("Engine Tier 1", player)
