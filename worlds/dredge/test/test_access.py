from .bases import DredgeTestBase
from ..locations import location_table

PASSAGE_ITEM_BY_REGION = {
    "Gale Cliffs": "The Windward Litany",
    "Stellar Basin": "The Astral Testament",
    "Twisted Strand": "The Mangrove Canticle",
    "Devil's Spine": "The Cinder Gospel",
    "The Pale Reach": "The Rimebound Chronicle",
}

LICENSE_BY_REGION = {
    "Gale Cliffs": "Gale Cliffs Fishing License",
    "Stellar Basin": "Stellar Basin Fishing License",
    "Twisted Strand": "Twisted Strand Fishing License",
    "Devil's Spine": "Devil's Spine Fishing License",
    "Open Ocean": "Open Ocean Fishing License",
    "The Pale Reach": "Pale Reach Fishing License",
}


class TestPassageAccess(DredgeTestBase):
    options = {
        "include_pale_reach_dlc": True,
        "add_passage_items": True,
    }
    run_default_tests = False

    def test_regions_need_their_passage(self) -> None:
        for region_name, passage_item in PASSAGE_ITEM_BY_REGION.items():
            with self.subTest(region=region_name):
                region = self.multiworld.get_region(region_name, self.player)
                locations = [location.name for location in region.locations if location.address is not None]
                self.assertTrue(locations, f"No locations in {region_name}")
                self.assertAccessDependency(locations, [[passage_item]], only_check_listed=True)


class TestIronRigPhaseAccess(DredgeTestBase):
    options = {
        "include_iron_rig_dlc": True,
        "add_passage_items": True,
    }
    run_default_tests = False

    def test_phase_locations_need_rig_access(self) -> None:
        locations = [
            location.name
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
            and any(req.type == "iron_rig_phase" for req in location_table[location.name].requirements)
        ]
        self.assertTrue(locations, "No Iron Rig phase locations")
        self.assertAccessDependency(locations, [["The Pelagic Psalm"]], only_check_listed=True)


class TestLicenseAccess(DredgeTestBase):
    options = {
        "include_pale_reach_dlc": True,
        "add_fishing_licenses": True,
    }
    run_default_tests = False

    def test_encyclopedia_locations_need_their_license(self) -> None:
        for region_name, license_item in LICENSE_BY_REGION.items():
            with self.subTest(region=region_name):
                locations = [
                    location.name
                    for location in self.multiworld.get_locations(self.player)
                    if location.address is not None
                    and location_table[location.name].location_group == "Encyclopedia"
                    and location_table[location.name].region == region_name
                ]
                self.assertTrue(locations, f"No encyclopedia locations in {region_name}")
                self.assertAccessDependency(locations, [[license_item]], only_check_listed=True)
