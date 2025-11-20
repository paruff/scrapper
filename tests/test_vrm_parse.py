"""Tests for VRM spider parsing logic.

Tests regex extraction of inline JSON models and slug generation.
Uses HTML fixture for offline parse testing.
"""

from pathlib import Path

from vrm_crawl.spiders.vrm import extract_inline_model, generate_property_slug


class TestInlineModelExtraction:
    """Test extraction of inline JSON initialization data."""

    def test_extract_from_fixture(self):
        """Test extraction from sample VA page HTML fixture."""
        fixture_path = Path(__file__).parent / "data" / "va_page_sample.html"
        with open(fixture_path) as f:
            html = f.read()

        result = extract_inline_model(html)

        assert result is not None
        assert "properties" in result
        assert len(result["properties"]) == 2

        # Verify first property
        prop1 = result["properties"][0]
        assert prop1["name"] == "Beach House Paradise"
        assert prop1["city"] == "Virginia Beach"
        assert prop1["bedrooms"] == "4"

        # Verify second property
        prop2 = result["properties"][1]
        assert prop2["name"] == "Mountain Retreat"
        assert prop2["city"] == "Charlottesville"

    def test_extract_no_model(self):
        """Test extraction returns None when no model present."""
        html = "<html><body>No model here</body></html>"
        result = extract_inline_model(html)
        assert result is None

    def test_extract_malformed_json(self):
        """Test extraction handles malformed JSON gracefully."""
        html = """
        <script>
        window.__INITIAL_STATE__ = {invalid json here};
        </script>
        """
        result = extract_inline_model(html)
        assert result is None


class TestSlugGeneration:
    """Test URL slug generation for properties."""

    def test_basic_slug(self):
        """Test basic slug generation."""
        slug = generate_property_slug("Beach House", "Virginia Beach", "VA")
        assert slug == "beach-house-virginia-beach-va"

    def test_slug_with_special_chars(self):
        """Test slug handles special characters."""
        slug = generate_property_slug("O'Malley's Place!", "St. Louis", "MO")
        assert slug == "o-malley-s-place-st-louis-mo"

    def test_slug_with_multiple_spaces(self):
        """Test slug collapses multiple spaces."""
        slug = generate_property_slug("The   Grand  Villa", "New  York", "NY")
        assert slug == "the-grand-villa-new-york-ny"

    def test_slug_with_numbers(self):
        """Test slug preserves numbers."""
        slug = generate_property_slug("Unit 42B", "Austin", "TX")
        assert slug == "unit-42b-austin-tx"

    def test_slug_empty_parts(self):
        """Test slug handles empty string parts."""
        slug = generate_property_slug("", "Miami", "FL")
        assert slug == "miami-fl"


class TestVrmSpiderIntegration:
    """Integration tests for VRM spider (fixture-based)."""

    def test_parse_fixture_properties(self):
        """Test that spider can parse properties from fixture."""
        # This would require Scrapy test harness setup
        # Placeholder for future integration test
        pass
