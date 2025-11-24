"""Economic Growth Areas Module.

Provides data on economically growing areas for residential real estate investment.
Data based on employment growth, GDP growth, and population trends.
"""

from typing import Any

# Economic growth data by state (top growing metro areas)
# Data based on recent economic indicators: employment growth, GDP growth, population trends
GROWTH_AREAS_DATA: dict[str, list[dict[str, Any]]] = {
    "VA": [
        {
            "area": "Northern Virginia",
            "cities": ["Arlington", "Alexandria", "Fairfax"],
            "growth_indicators": {
                "employment_growth": "High",
                "gdp_growth": "High",
                "population_trend": "Growing",
            },
            "key_sectors": ["Technology", "Government", "Professional Services"],
        },
        {
            "area": "Richmond Metro",
            "cities": ["Richmond", "Henrico", "Chesterfield"],
            "growth_indicators": {
                "employment_growth": "Medium",
                "gdp_growth": "Medium",
                "population_trend": "Growing",
            },
            "key_sectors": ["Finance", "Healthcare", "Manufacturing"],
        },
    ],
    "TX": [
        {
            "area": "Austin Metro",
            "cities": ["Austin", "Round Rock", "Cedar Park"],
            "growth_indicators": {
                "employment_growth": "Very High",
                "gdp_growth": "Very High",
                "population_trend": "Rapidly Growing",
            },
            "key_sectors": ["Technology", "Healthcare", "Education"],
        },
        {
            "area": "Dallas-Fort Worth",
            "cities": ["Dallas", "Fort Worth", "Plano", "Irving"],
            "growth_indicators": {
                "employment_growth": "High",
                "gdp_growth": "High",
                "population_trend": "Growing",
            },
            "key_sectors": ["Technology", "Finance", "Healthcare"],
        },
        {
            "area": "Houston Metro",
            "cities": ["Houston", "The Woodlands", "Sugar Land"],
            "growth_indicators": {
                "employment_growth": "High",
                "gdp_growth": "High",
                "population_trend": "Growing",
            },
            "key_sectors": ["Energy", "Healthcare", "Aerospace"],
        },
    ],
    "NC": [
        {
            "area": "Research Triangle",
            "cities": ["Raleigh", "Durham", "Chapel Hill", "Cary"],
            "growth_indicators": {
                "employment_growth": "Very High",
                "gdp_growth": "High",
                "population_trend": "Rapidly Growing",
            },
            "key_sectors": ["Technology", "Research", "Healthcare"],
        },
        {
            "area": "Charlotte Metro",
            "cities": ["Charlotte", "Concord", "Gastonia"],
            "growth_indicators": {
                "employment_growth": "High",
                "gdp_growth": "High",
                "population_trend": "Growing",
            },
            "key_sectors": ["Finance", "Technology", "Healthcare"],
        },
    ],
    "FL": [
        {
            "area": "Tampa Bay",
            "cities": ["Tampa", "St. Petersburg", "Clearwater"],
            "growth_indicators": {
                "employment_growth": "High",
                "gdp_growth": "High",
                "population_trend": "Growing",
            },
            "key_sectors": ["Healthcare", "Finance", "Tourism"],
        },
        {
            "area": "Orlando Metro",
            "cities": ["Orlando", "Kissimmee", "Sanford"],
            "growth_indicators": {
                "employment_growth": "High",
                "gdp_growth": "Medium",
                "population_trend": "Growing",
            },
            "key_sectors": ["Tourism", "Technology", "Healthcare"],
        },
        {
            "area": "Miami Metro",
            "cities": ["Miami", "Fort Lauderdale", "West Palm Beach"],
            "growth_indicators": {
                "employment_growth": "Medium",
                "gdp_growth": "Medium",
                "population_trend": "Growing",
            },
            "key_sectors": ["Finance", "Tourism", "International Trade"],
        },
    ],
    "CA": [
        {
            "area": "Bay Area",
            "cities": ["San Francisco", "San Jose", "Oakland", "Fremont"],
            "growth_indicators": {
                "employment_growth": "High",
                "gdp_growth": "Very High",
                "population_trend": "Stable",
            },
            "key_sectors": ["Technology", "Finance", "Professional Services"],
        },
        {
            "area": "Sacramento Metro",
            "cities": ["Sacramento", "Roseville", "Folsom"],
            "growth_indicators": {
                "employment_growth": "Medium",
                "gdp_growth": "Medium",
                "population_trend": "Growing",
            },
            "key_sectors": ["Government", "Healthcare", "Agriculture"],
        },
        {
            "area": "Inland Empire",
            "cities": ["Riverside", "San Bernardino", "Ontario"],
            "growth_indicators": {
                "employment_growth": "Medium",
                "gdp_growth": "Medium",
                "population_trend": "Growing",
            },
            "key_sectors": ["Logistics", "Manufacturing", "Healthcare"],
        },
    ],
}


def get_growth_areas(state: str) -> list[dict[str, Any]]:
    """Get economically growing areas for a given state.

    Args:
        state: Two-letter state code (e.g., 'VA', 'TX', 'NC', 'FL', 'CA')

    Returns:
        List of growth area dictionaries with area name, cities, indicators, and sectors.
        Returns empty list if state not found.

    Examples:
        >>> areas = get_growth_areas('VA')
        >>> len(areas) > 0
        True
        >>> areas[0]['area']
        'Northern Virginia'
    """
    state_upper = state.upper()
    return GROWTH_AREAS_DATA.get(state_upper, [])


def get_all_supported_states() -> list[str]:
    """Get list of all states with growth area data.

    Returns:
        List of two-letter state codes

    Examples:
        >>> states = get_all_supported_states()
        >>> 'VA' in states
        True
        >>> 'TX' in states
        True
    """
    return sorted(GROWTH_AREAS_DATA.keys())


def format_growth_areas(state: str) -> str:
    """Format growth areas for display.

    Args:
        state: Two-letter state code

    Returns:
        Formatted string with growth area information

    Examples:
        >>> output = format_growth_areas('VA')
        >>> 'Northern Virginia' in output
        True
    """
    areas = get_growth_areas(state)

    if not areas:
        return f"No growth area data available for state: {state}"

    output_lines = [f"\n=== Economically Growing Areas in {state.upper()} ===\n"]

    for idx, area in enumerate(areas, 1):
        output_lines.append(f"{idx}. {area['area']}")
        output_lines.append(f"   Cities: {', '.join(area['cities'])}")
        output_lines.append("   Growth Indicators:")
        for indicator, value in area["growth_indicators"].items():
            output_lines.append(f"     - {indicator.replace('_', ' ').title()}: {value}")
        output_lines.append(f"   Key Sectors: {', '.join(area['key_sectors'])}")
        output_lines.append("")

    return "\n".join(output_lines)
