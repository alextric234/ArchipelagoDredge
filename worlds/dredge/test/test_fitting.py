from unittest import TestCase

from BaseClasses import CollectionState
from .bases import DredgeTestBase
from ..fitting import hulls_needed
from ..items import item_table
from ..rules import can_equip


class TestHullsNeeded(TestCase):
    def test_every_rod_and_net_fits_some_hull(self) -> None:
        for name, item in item_table.items():
            if item.item_group not in ("Rod", "Net"):
                continue
            for include_iron_rig in (False, True):
                with self.subTest(item=name, include_iron_rig=include_iron_rig):
                    self.assertTrue(item.shape, f"{name} has no shape")
                    hulls_needed(name, include_iron_rig)

    def test_known_fits(self) -> None:
        expected = {
            "Starting Gear - Basic Fishing Pole": 0,
            "Flexible Fishing Pole": 0,
            "Hydraulic Rod": 0,
            "Bottomless Lines": 1,
            "Viscera Crane": 1,
            "Versatile Rod": 2,
            "Tendon Rod": 2,
            "Harvesting Platform": 2,
            "Basic Trawl Net": 1,
            "Siphon Trawler": 1,
            "Large Trawl Net": 3,
            "Heavy-Duty Trawl Net": 3,
        }
        for name, hulls in expected.items():
            for include_iron_rig in (False, True):
                with self.subTest(item=name, include_iron_rig=include_iron_rig):
                    self.assertEqual(hulls_needed(name, include_iron_rig), hulls)

    def test_items_without_a_shape_need_no_hull(self) -> None:
        self.assertEqual(hulls_needed("Dredge Crane", False), 0)
        self.assertEqual(hulls_needed("Not An Item", False), 0)


class TestCanEquip(DredgeTestBase):
    run_default_tests = False

    def test_versatile_rod_needs_two_hulls(self) -> None:
        world = self.multiworld.worlds[self.player]
        state = CollectionState(self.multiworld)
        state.collect(world.create_item("Versatile Rod"), True)
        state.collect(world.create_item("Progressive Hull"), True)
        self.assertFalse(can_equip("Versatile Rod", state, self.player, False))
        state.collect(world.create_item("Progressive Hull"), True)
        self.assertTrue(can_equip("Versatile Rod", state, self.player, False))
