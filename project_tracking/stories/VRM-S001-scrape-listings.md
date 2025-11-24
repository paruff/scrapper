# VRM-S001: Parse listings and export Excel

## Context

Scrape state pages from VRM Properties, parse inline JSON, and persist to per-state Excel sheets.

## Goal

Accurately extract properties and generate a daily Excel workbook with one sheet per state.

## Acceptance Criteria

- Inline JSON model is parsed into a list of properties.
- Pagination respects `VRM_MAX_PAGES` per state.
- Excel sheet headers come from the first item key order.

## BDD Scenarios

See `tests/bdd/features/scrape.feature`:

- Extract inline JSON model into properties
- Respect per-state page cap and avoid extra follows
- Write Excel with per-state sheet and ordered headers


