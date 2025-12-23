from dataclasses import dataclass

from Options import Toggle, PerGameCommonOptions


# class Goal(Choice):
#     """
#     Set what base game conditions need to be met to complete the game
#
#     Standard Ending: Return artifacts to collector and trigger the ending
#     All Pursuits: Complete all pursuits
#     All Fish Found: Fill out all applicable encyclopedia entries (Including DLCs will add those fish to this goal)
#     """
#     internal_name = "goal"
#     display_name = "Goal"
#     option_standard_ending = 0
#     option_all_pursuits = 1
#     option_all_fish_found = 2
#     default = 0

class IncludeIronRigDLC(Toggle):
    """
    Include the Iron Rig DLC (Iron Rig DLC required for this)
    """
    display_name = "Include Iron Rig DLC"

# class RequireIronRigEnding(Toggle):
#     """
#     Require Iron Rig ending to have been achieved before game can be completed
#     """
#     internal_name = "require_iron_rig_ending"
#     display_name = "Require Iron Rig Ending"

class IncludePaleReachDLC(Toggle):
    """
    Include the Pale Reach DLC (Pale Reach DLC required for this)
    """
    display_name = "Include Pale Reach DLC"

# class RequirePaleReachEnding(Toggle):
#     """
#     Require Pale Reach ending to have been achieved before game can be completed
#     """
#     internal_name = "require_pale_reach_ending"
#     display_name = "Require Pale Reach Ending"

class RequireEngines(Toggle):
    """
    Set logic to require engine upgrade to reach further archipelagos
    """
    display_name = "Require Engines"

class LogicalNets(Toggle):
    """
    If enabled, logic may expect players to use nets as the only method of catching fish that are also catchable with a
    rod. This includes passive net catches in specific regions.

    If disabled, logic will only consider rod-based access for such fish, ensuring checks are reachable through active
    fishing.

    Recommended: disabled for players who prefer reliable, targeted fishing.
    """
    display_name = "Logical Nets"

class IncludeAberrations(Toggle):
    """
    If enabled, checks for fish aberrations may contain progression items.
    """
    display_name = "Include Aberrations"

# class EnableTraps(Toggle):
#     """
#     Allow traps to be added to the pool to replace filler items
#     """
#     internal_name = "enable_traps"
#     display_name = "Enable Traps"


@dataclass
class DREDGEOptions(PerGameCommonOptions):
    # goal: Goal
    include_iron_rig_dlc: IncludeIronRigDLC
    # require_iron_rig_ending: RequireIronRigEnding
    include_pale_reach_dlc: IncludePaleReachDLC
    # require_pale_reach_ending: RequirePaleReachEnding
    require_engines: RequireEngines
    logical_nets: LogicalNets
    include_aberrations: IncludeAberrations
    # enable_traps: EnableTraps
