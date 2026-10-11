from BaseClasses import ItemClassification

from .bases import DredgeTestBase
from ..items import item_table


def pool_item_names(test: DredgeTestBase) -> list[str]:
    return [item.name for item in test.multiworld.itempool if item.player == test.player]


class TestDefaultOptions(DredgeTestBase):
    options = {}

    def test_three_progressive_hulls(self) -> None:
        self.assertEqual(pool_item_names(self).count("Progressive Hull"), 3)

    def test_no_dlc_items(self) -> None:
        dlc_items = [name for name in pool_item_names(self)
                     if item_table[name].expansion in ("PaleReach", "IronRig")]
        self.assertEqual(dlc_items, [])

    def test_no_licenses_or_passages(self) -> None:
        groups = {item_table[name].item_group for name in pool_item_names(self)}
        self.assertNotIn("Virtual License", groups)
        self.assertNotIn("Virtual Passage Item", groups)


class TestPaleReach(DredgeTestBase):
    options = {
        "include_pale_reach_dlc": True,
    }

    def test_pale_reach_useful_items_included(self) -> None:
        useful_pale_reach = {name for name, data in item_table.items()
                             if data.classification == ItemClassification.useful and data.expansion == "PaleReach"}
        self.assertTrue(useful_pale_reach.issubset(set(pool_item_names(self))))


class TestIronRig(DredgeTestBase):
    options = {
        "include_iron_rig_dlc": True,
    }

    def test_four_progressive_hulls(self) -> None:
        self.assertEqual(pool_item_names(self).count("Progressive Hull"), 4)


class TestAllOptions(DredgeTestBase):
    options = {
        "include_iron_rig_dlc": True,
        "include_pale_reach_dlc": True,
        "require_engines": True,
        "logical_nets": True,
        "include_aberrations": True,
        "add_fishing_licenses": True,
        "add_passage_items": True,
        "death_link": True,
    }

    def test_licenses_and_passages_included(self) -> None:
        groups = {item_table[name].item_group for name in pool_item_names(self)}
        self.assertIn("Virtual License", groups)
        self.assertIn("Virtual Passage Item", groups)


class TestLicensesAndPassagesWithoutDlc(DredgeTestBase):
    options = {
        "add_fishing_licenses": True,
        "add_passage_items": True,
        "require_engines": True,
    }
