from BaseClasses import CollectionState, LocationProgressType
from .bases import DredgeTestBase
from ..locations import location_table, ItemsReq

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


class TestIcebreakerAccess(DredgeTestBase):
    options = {
        "include_pale_reach_dlc": True,
    }
    run_default_tests = False

    def test_icebreaker_or_all_parts(self) -> None:
        locations = [
            location.name
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
            and any(isinstance(req, ItemsReq) and "Icebreaker" in req.all_of
                    for req in location_table[location.name].requirements)
        ]
        self.assertTrue(locations, "No locations require the Icebreaker")
        self.assertAccessDependency(
            locations,
            [["Icebreaker"], ["Icebreaker Plow Half 1", "Icebreaker Plow Half 2", "Icebreaker Bracing"]],
            only_check_listed=True)


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


class TestBoatPerformanceAccess(DredgeTestBase):
    options = {
        "include_pale_reach_dlc": True,
        "require_boat_performance": True,
    }
    run_default_tests = False

    def state_with(self, *item_names: str) -> CollectionState:
        state = CollectionState(self.multiworld)
        for name in item_names:
            state.collect(self.world.create_item(name), True)
        return state

    def test_lights_are_progression(self) -> None:
        self.assertTrue(self.world.create_item("Cracked Bulb").advancement)

    def test_mid_regions(self) -> None:
        ready = ("Progressive Hull", "Twin Prop Engine", "Halogen Spotlight")
        for region in ("Gale Cliffs", "Stellar Basin", "Twisted Strand", "Devil's Spine"):
            with self.subTest(region=region):
                self.assertTrue(self.state_with(*ready).can_reach_region(region, self.player))
                for missing in ready:
                    items = [name for name in ready if name != missing]
                    self.assertFalse(self.state_with(*items).can_reach_region(region, self.player), missing)

    def test_open_ocean_locations_need_more_light(self) -> None:
        dim = self.state_with("Progressive Hull", "Twin Prop Engine", "Halogen Spotlight")
        bright = self.state_with("Progressive Hull", "Twin Prop Engine", "Tungsten Floodlight")
        for state in (dim, bright):
            state.collect(self.world.create_item("Dredge Crane"), True)
        locations = [location for location in self.multiworld.get_region("Open Ocean", self.player).locations
                     if location.address is not None
                     and location_table[location.name].location_group in ("Dredge", "Encyclopedia", "World")
                     and location.can_reach(bright)]
        self.assertTrue(locations, "No Open Ocean location reachable with a Tungsten Floodlight")
        for location in locations:
            with self.subTest(location=location.name):
                self.assertFalse(location.can_reach(dim))

    def test_pale_reach_needs_more_speed(self) -> None:
        state = self.state_with("Progressive Hull", "Twin Prop Engine", "Tungsten Floodlight")
        self.assertFalse(state.can_reach_region("The Pale Reach", self.player))
        state.collect(self.world.create_item("Engine Stack"), True)
        self.assertTrue(state.can_reach_region("The Pale Reach", self.player))


class TestLightsUsefulWithoutBoatPerformance(DredgeTestBase):
    run_default_tests = False

    def test_lights_are_useful(self) -> None:
        self.assertFalse(self.world.create_item("Cracked Bulb").advancement)


class TestResearchUnlockEvents(DredgeTestBase):
    run_default_tests = False

    def test_unlocks_are_events(self) -> None:
        self.assertNotIn("Flexible Fishing Pole Researched", self.world.item_name_to_id)
        self.assertNotIn("Flexible Fishing Pole Researched", self.world.location_name_to_id)
        location = self.multiworld.get_location("Flexible Fishing Pole Researched", self.player)
        self.assertIsNone(location.address)
        self.assertIsNone(location.item.code)
        self.assertTrue(location.item.advancement)

    def test_unlock_events_gate_later_research(self) -> None:
        location = self.multiworld.get_location("Heat-Resistant Line Researched", self.player)
        state = CollectionState(self.multiworld)
        for _ in range(30):
            state.collect(self.world.create_item("Research Part"), True)
        self.assertFalse(location.can_reach(state))
        state.collect(self.multiworld.get_location("Flexible Fishing Pole Researched", self.player).item, True)
        self.assertTrue(location.can_reach(state))


BASE_PURSUITS = {
    "Fishmonger's Gift", "Shipwright's Gift", "Little Marrow Trader's Gift", "Travelling Merchant's Gift",
    "Package Delivery", "Craven Courier", "Figure in Blue", "Figure in Gold", "Figure in Purple", "Figure in Red",
    "Research Assistant", "A Place to Rest",
}


def pursuit_locations(test: DredgeTestBase) -> dict[str, object]:
    return {location.name: location for location in test.multiworld.get_locations(test.player)
            if location.name in location_table and location_table[location.name].location_group == "Pursuit"}


class TestPursuitAccess(DredgeTestBase):
    options = {
        "add_passage_items": True,
    }
    run_default_tests = False

    def test_base_pursuits_present(self) -> None:
        self.assertEqual(set(pursuit_locations(self)), BASE_PURSUITS)

    def test_a_place_to_rest_only_needs_dredge_crane(self) -> None:
        location = pursuit_locations(self)["A Place to Rest"]
        self.assertEqual(location.progress_type, LocationProgressType.DEFAULT)
        self.assertEqual(location_table["A Place to Rest"].requirements, [ItemsReq(all_of=["Dredge Crane"])])

    def test_hooded_figure_needs_its_fish_regions(self) -> None:
        # Tiger Mackerel is a Gale Cliffs fish and Snake Mackerel a Devil's Spine one.
        self.assertAccessDependency(["Figure in Blue"], [["The Windward Litany"]], only_check_listed=True)
        self.assertAccessDependency(["Figure in Blue"], [["The Cinder Gospel"]], only_check_listed=True)

    def test_travelling_merchant_needs_open_ocean(self) -> None:
        self.assertAccessDependency(["Travelling Merchant's Gift"], [["The Pelagic Psalm"]], only_check_listed=True)

    def test_trader_and_builder_need_dredge_crane(self) -> None:
        self.assertAccessDependency(["Little Marrow Trader's Gift", "A Place to Rest"], [["Dredge Crane"]],
                                    only_check_listed=True)


class TestPaleReachPursuit(DredgeTestBase):
    options = {
        "include_pale_reach_dlc": True,
        "include_aberrations": True,
    }
    run_default_tests = False

    def test_figure_in_white_present_and_not_excluded(self) -> None:
        pursuits = pursuit_locations(self)
        self.assertEqual(set(pursuits), BASE_PURSUITS | {"Figure in White"})
        self.assertEqual(pursuits["Figure in White"].progress_type, LocationProgressType.DEFAULT)


class TestPursuitLicenseAccess(DredgeTestBase):
    options = {
        "add_fishing_licenses": True,
    }
    run_default_tests = False

    def test_hooded_figure_needs_its_fish_licenses(self) -> None:
        for license_name in ("Gale Cliffs Fishing License", "Devil's Spine Fishing License"):
            with self.subTest(license=license_name):
                self.assertAccessDependency(["Figure in Blue"], [[license_name]], only_check_listed=True)
