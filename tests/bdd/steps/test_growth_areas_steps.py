"""BDD step definitions for economic growth areas feature."""

from pytest_bdd import given, parsers, scenario, then, when

from vrm_crawl.growth_areas import get_all_supported_states, get_growth_areas


@scenario("../features/growth_areas.feature", "Request growth areas for Virginia")
def test_growth_areas_virginia():
    pass


@scenario("../features/growth_areas.feature", "Request growth areas for Texas")
def test_growth_areas_texas():
    pass


@scenario("../features/growth_areas.feature", "Request growth areas for unsupported state")
def test_growth_areas_unsupported():
    pass


@scenario("../features/growth_areas.feature", "Get all supported states")
def test_get_all_supported_states():
    pass


@given(parsers.parse('a state "{state}"'), target_fixture="given_state")
def given_state(state: str) -> str:
    """Store the state code."""
    return state


@when("the user requests growth areas")
def request_growth_areas(given_state: str, context: dict):
    """Request growth areas for the given state."""
    context["growth_areas"] = get_growth_areas(given_state)


@when("the user requests all supported states")
def request_supported_states(context: dict):
    """Request all supported states."""
    context["supported_states"] = get_all_supported_states()


@then("the system provides a list of economically growing areas")
def assert_growth_areas_exist(context: dict):
    """Assert that growth areas are returned."""
    areas = context.get("growth_areas", [])
    assert len(areas) > 0, "Expected at least one growth area"


@then(parsers.parse('the list includes "{area_name}"'))
def assert_area_in_list(context: dict, area_name: str):
    """Assert that a specific area is in the list."""
    if "growth_areas" in context:
        areas = context["growth_areas"]
        area_names = [area["area"] for area in areas]
        assert area_name in area_names, f"Expected {area_name} in {area_names}"
    elif "supported_states" in context:
        states = context["supported_states"]
        assert area_name in states, f"Expected {area_name} in {states}"


@then("the list includes growth indicators")
def assert_has_growth_indicators(context: dict):
    """Assert that growth areas have indicators."""
    areas = context.get("growth_areas", [])
    assert len(areas) > 0, "No growth areas found"
    first_area = areas[0]
    assert "growth_indicators" in first_area, "No growth_indicators found"
    assert len(first_area["growth_indicators"]) > 0, "Growth indicators are empty"


@then("the system returns an empty list")
def assert_empty_list(context: dict):
    """Assert that an empty list is returned."""
    areas = context.get("growth_areas", [])
    assert len(areas) == 0, f"Expected empty list but got {len(areas)} areas"
