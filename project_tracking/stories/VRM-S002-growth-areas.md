# Story VRM-S002: Economic Growth Areas for Real Estate Investment

**Feature**: VRM-F002 (Economic Growth Areas)  
**Priority**: Medium  
**Status**: Done

## Context

Residential real estate investors need to identify economically growing areas to make informed investment decisions. By providing data on areas with strong economic indicators (employment growth, GDP growth, population trends), investors can target properties in markets with higher growth potential.

## Goal

As a residential real estate investor,  
I want a list of economically growing areas,  
So that I can find properties in those areas.

## Acceptance Criteria

- [x] Given a state code, the system provides a list of economically growing areas
- [x] Each area includes cities, growth indicators, and key economic sectors
- [x] Growth indicators include employment growth, GDP growth, and population trends
- [x] Users can query growth areas via CLI tool
- [x] Users can query growth areas programmatically via Python API
- [x] System supports VA, TX, NC, FL, and CA states
- [x] System returns empty list for unsupported states
- [x] All supported states can be listed

## BDD Scenarios

See `tests/bdd/features/growth_areas.feature` for Gherkin scenarios:
- Request growth areas for Virginia
- Request growth areas for Texas
- Request growth areas for unsupported state
- Get all supported states

## Implementation Notes

- Data module: `vrm_crawl/growth_areas.py`
- CLI tool: `get_growth_areas.py`
- Unit tests: `tests/test_growth_areas.py`
- BDD tests: `tests/bdd/steps/test_growth_areas_steps.py`
- Economic data based on employment, GDP, and population trends

## Usage Examples

```bash
# Get growth areas for a state
python get_growth_areas.py VA

# List all supported states
python get_growth_areas.py --list
```

```python
# Programmatic usage
from vrm_crawl.growth_areas import get_growth_areas

areas = get_growth_areas('TX')
for area in areas:
    print(f"{area['area']}: {', '.join(area['cities'])}")
```
