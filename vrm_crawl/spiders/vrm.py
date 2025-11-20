"""VRM Properties Spider.

Scrapes property listings from VRM Properties website with state-based filtering,
JSON inline model parsing, and configurable safety limits.
"""

import json
import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import scrapy
import yaml


def extract_inline_model(html: str) -> dict[str, Any] | None:
    """Extract inline JSON model from VRM page initialization script.

    Searches for pattern: window.__INITIAL_STATE__ = {...};
    or similar initialization patterns in script tags.

    Args:
        html: Raw HTML content from response

    Returns:
        Parsed JSON dict if found, None otherwise
    """
    # Pattern to match inline initialization with JSON
    pattern = r"window\.__INITIAL_STATE__\s*=\s*({.*?});"
    match = re.search(pattern, html, re.DOTALL)

    if match:
        try:
            json_str = match.group(1)
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    return None


def generate_property_slug(name: str, city: str, state: str) -> str:
    """Generate URL-friendly slug for property.

    Args:
        name: Property name
        city: City name
        state: State code

    Returns:
        Slugified string: "name-city-state" in lowercase with hyphens
    """
    parts = [name, city, state]
    # Convert to lowercase, replace spaces/special chars with hyphens
    slug_parts = []
    for part in parts:
        cleaned = re.sub(r"[^a-z0-9]+", "-", part.lower()).strip("-")
        if cleaned:  # Only add non-empty parts
            slug_parts.append(cleaned)
    return "-".join(slug_parts)


class VrmSpider(scrapy.Spider):
    """Spider for scraping VRM Properties listings.

    Supports state filtering via command-line argument with precedence:
    1. Command-line `-a states=VA,TX,NC`
    2. Fallback to states.yml config file

    Parses property data from inline JSON models in page scripts.
    Respects VRM_MAX_PAGES safety cap from settings.
    """

    name = "vrm"
    allowed_domains = ["vacationrentalmanagers.com"]

    def __init__(self, states: str | None = None, *args, **kwargs):
        """Initialize spider with state filtering.

        Args:
            states: Comma-separated state codes (e.g., "VA,TX,NC")
        """
        super().__init__(*args, **kwargs)

        # State selection precedence: CLI arg > states.yml
        if states:
            self.states = [s.strip().upper() for s in states.split(",")]
            self.logger.info(f"Using states from CLI: {self.states}")
        else:
            self.states = self._load_states_from_yaml()
            self.logger.info(f"Using states from states.yml: {self.states}")

        self.page_count: dict[str, int] = {}  # Track pages per state
        self.max_pages = 250  # Default, will be overridden from settings if available

    def _load_states_from_yaml(self) -> list:
        """Load state codes from states.yml fallback config.

        Returns:
            List of state codes
        """
        yaml_path = Path(__file__).parent.parent.parent / "states.yml"
        try:
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
                return data.get("states", ["VA"])
        except Exception as e:
            self.logger.warning(f"Failed to load states.yml: {e}, using default ['VA']")
            return ["VA"]

    def start_requests(self) -> Iterator[scrapy.Request]:
        """Generate start requests for each configured state.

        Yields:
            Scrapy Request objects for state listing pages
        """
        # Get max_pages from settings (now settings are available via crawler)
        self.max_pages = self.crawler.settings.getint("VRM_MAX_PAGES", 250)

        for state in self.states:
            self.page_count[state] = 0
            url = f"https://www.vacationrentalmanagers.com/{state.lower()}"
            yield scrapy.Request(
                url=url, callback=self.parse, meta={"state": state}, dont_filter=True
            )

    def parse(self, response) -> Iterator[dict[str, Any]]:
        """Parse VRM listing page.

        Extracts property data from inline JSON model and yields items.
        Follows pagination links up to max_pages limit.

        Args:
            response: Scrapy response object

        Yields:
            Property item dicts
        """
        state = response.meta.get("state", "Unknown")
        self.page_count[state] = self.page_count.get(state, 0) + 1

        self.logger.info(f"Parsing {state} page {self.page_count[state]}: {response.url}")

        # Extract inline JSON model
        inline_data = extract_inline_model(response.text)

        if inline_data:
            # Parse properties from inline data structure
            # Adjust path based on actual JSON structure
            properties = inline_data.get("properties", [])

            for prop in properties:
                item = {
                    "state": state,
                    "name": prop.get("name", ""),
                    "city": prop.get("city", ""),
                    "address": prop.get("address", ""),
                    "price": prop.get("price", ""),
                    "bedrooms": prop.get("bedrooms", ""),
                    "bathrooms": prop.get("bathrooms", ""),
                    "url": prop.get("url", ""),
                }

                # Generate slug
                if item["name"] and item["city"]:
                    item["slug"] = generate_property_slug(item["name"], item["city"], state)

                yield item

        # Check pagination limit
        if self.page_count[state] >= self.max_pages:
            self.logger.warning(f"Reached max pages ({self.max_pages}) for state {state}")
            return

        # Follow pagination (adjust selector based on actual site structure)
        next_page = response.css("a.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, meta={"state": state})
