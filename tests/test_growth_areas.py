"""Unit tests for growth_areas module."""


from vrm_crawl.growth_areas import (
    format_growth_areas,
    get_all_supported_states,
    get_growth_areas,
)


class TestGetGrowthAreas:
    """Test get_growth_areas function."""

    def test_get_growth_areas_va(self):
        """Test getting growth areas for Virginia."""
        areas = get_growth_areas("VA")
        assert len(areas) > 0
        assert any(area["area"] == "Northern Virginia" for area in areas)

    def test_get_growth_areas_tx(self):
        """Test getting growth areas for Texas."""
        areas = get_growth_areas("TX")
        assert len(areas) > 0
        assert any(area["area"] == "Austin Metro" for area in areas)

    def test_get_growth_areas_nc(self):
        """Test getting growth areas for North Carolina."""
        areas = get_growth_areas("NC")
        assert len(areas) > 0
        assert any(area["area"] == "Research Triangle" for area in areas)

    def test_get_growth_areas_fl(self):
        """Test getting growth areas for Florida."""
        areas = get_growth_areas("FL")
        assert len(areas) > 0
        assert any(area["area"] == "Tampa Bay" for area in areas)

    def test_get_growth_areas_ca(self):
        """Test getting growth areas for California."""
        areas = get_growth_areas("CA")
        assert len(areas) > 0
        assert any(area["area"] == "Bay Area" for area in areas)

    def test_get_growth_areas_lowercase(self):
        """Test that lowercase state codes work."""
        areas = get_growth_areas("va")
        assert len(areas) > 0

    def test_get_growth_areas_unsupported_state(self):
        """Test getting growth areas for unsupported state."""
        areas = get_growth_areas("ZZ")
        assert len(areas) == 0

    def test_growth_area_structure(self):
        """Test that growth areas have expected structure."""
        areas = get_growth_areas("VA")
        assert len(areas) > 0

        area = areas[0]
        assert "area" in area
        assert "cities" in area
        assert "growth_indicators" in area
        assert "key_sectors" in area

        assert isinstance(area["cities"], list)
        assert isinstance(area["growth_indicators"], dict)
        assert isinstance(area["key_sectors"], list)

    def test_growth_indicators_structure(self):
        """Test that growth indicators have expected keys."""
        areas = get_growth_areas("TX")
        assert len(areas) > 0

        indicators = areas[0]["growth_indicators"]
        assert "employment_growth" in indicators
        assert "gdp_growth" in indicators
        assert "population_trend" in indicators


class TestGetAllSupportedStates:
    """Test get_all_supported_states function."""

    def test_returns_list(self):
        """Test that function returns a list."""
        states = get_all_supported_states()
        assert isinstance(states, list)

    def test_includes_expected_states(self):
        """Test that all expected states are included."""
        states = get_all_supported_states()
        expected = ["VA", "TX", "NC", "FL", "CA"]
        for state in expected:
            assert state in states

    def test_returns_sorted(self):
        """Test that states are returned in sorted order."""
        states = get_all_supported_states()
        assert states == sorted(states)


class TestFormatGrowthAreas:
    """Test format_growth_areas function."""

    def test_format_va(self):
        """Test formatting Virginia growth areas."""
        output = format_growth_areas("VA")
        assert "Northern Virginia" in output
        assert "VA" in output
        assert "Cities:" in output
        assert "Growth Indicators:" in output

    def test_format_tx(self):
        """Test formatting Texas growth areas."""
        output = format_growth_areas("TX")
        assert "Austin Metro" in output
        assert "TX" in output

    def test_format_unsupported_state(self):
        """Test formatting unsupported state."""
        output = format_growth_areas("ZZ")
        assert "No growth area data available" in output
        assert "ZZ" in output

    def test_format_includes_all_sections(self):
        """Test that formatted output includes all sections."""
        output = format_growth_areas("NC")
        assert "Cities:" in output
        assert "Growth Indicators:" in output
        assert "Key Sectors:" in output
        assert "Employment Growth:" in output
        assert "Gdp Growth:" in output
        assert "Population Trend:" in output
