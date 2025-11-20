## VRM Scraper: Copilot Instructions

These instructions help AI coding agents work productively in this Scrapy-based project. Focus on patterns that already exist; avoid speculative refactors.

**Architecture**
- **Scrapy project:** Code lives under `vrm_crawl/` with spider `spiders/vrm.py`, pipeline `pipelines.py`, and settings `settings.py`. Entry via `scrapy crawl vrm` per `scrapy.cfg`.
- **Data source:** Pages per state on `vacationrentalmanagers.com/{state}`. The spider parses an inline JSON model from page scripts.
- **Excel output:** `MultiSheetExcelPipeline` writes to `output/vrm_listings_YYYY-MM-DD.xlsx` with one sheet per state; headers come from dict key order of the first item per sheet.

**Data Flow**
- **State selection precedence:** CLI `-a states=VA,TX` overrides YAML; otherwise falls back to `states.yml`.
- **Inline JSON extraction:** `extract_inline_model(html)` matches `window.__INITIAL_STATE__ = { ... };` and returns a dict or `None`.
- **Item shape:** Built in `spiders/vrm.py` inside `parse()` using insertion-ordered keys: `state, name, city, address, price, bedrooms, bathrooms, url[, slug]`.
- **Slug generation:** `generate_property_slug(name, city, state)` lowercases, replaces non-alphanumerics with hyphens, collapses repeats.
- **Safety caps:** Per-state page limit from `settings.VRM_MAX_PAGES` (default 250). Pagination follows `a.next-page` selector.

**Developer Workflows**
- **Run crawler:** `scrapy crawl vrm` (optionally `-a states=VA,TX` and/or `-s CLOSESPIDER_PAGECOUNT=5` for smoke runs). Output goes to `output/`.
- **Tests:** `pytest` (see `tests/test_vrm_parse.py` for expectations). No network in tests; use fixtures under `tests/data/`.
- **Lint & format:** `ruff check .` and `ruff format .` (config in `pyproject.toml`).
- **Type checks:** `mypy vrm_crawl` (errors are non-blocking per README intent).
- **Security scans:** `bandit -r vrm_crawl/` and `gitleaks detect --source .`.

**Project Conventions**
- **Respectful crawling defaults:** `ROBOTSTXT_OBEY=True`, `DOWNLOAD_DELAY=2.0`, `AUTOTHROTTLE_ENABLED=True`, user agent set in `settings.py`. Maintain these unless explicitly changing behavior.
- **Item/column order matters:** Excel headers come from `list(item.keys())`. Preserve key insertion order in `vrm.py` when adding fields to avoid column churn.
- **Config surface:** Prefer adding tunables to `settings.py` (e.g., `VRM_MAX_PAGES`) and reference via `self.crawler.settings.get*` inside spiders.
- **Parsing strategy:** Favor updating `extract_inline_model()` and subsequent dict pathing over brittle CSS/XPath scraping if the inline model exists.
- **State codes:** Expect uppercase two-letter codes; normalize inputs (`VA`, not `va` or `Virginia`).

**Extending the Spider**
- **Adding fields:**
  - Parse from the inline JSON dict in `parse()`.
  - Insert new keys in the desired column order when building `item`.
  - Pipeline requires no change; it writes whatever keys are present, with the first-item header defining the sheet schema.
- **Changing JSON location:** If site changes script structure, first update `extract_inline_model()` regex and adapt downstream dict access in `parse()`.
- **Pagination:** If `a.next-page` changes, adjust the selector in `parse()` without altering the cap logic.

**Testing Guidance**
- **Unit tests cover:** inline model extraction and slug logic. Keep compatibility with `tests/data/va_page_sample.html` or update fixture + tests together.
- **Add tests for new fields:** Use a minimal HTML fixture embedding an inline model string that reflects new keys you consume.

**CI/Automation Notes**
- Workflows (described in `README.md`) run lint, format check, mypy, bandit, pytest, and optional sample scrapes. Nightly jobs are gated by `SCRAPE_DISABLE`.
- Avoid network-dependent unit tests; rely on fixtures to keep CI stable and respectful.

**Key Files**
- Spider: `vrm_crawl/spiders/vrm.py` (state handling, parsing, slugging)
- Pipeline: `vrm_crawl/pipelines.py` (Excel multi-sheet writer)
- Settings: `vrm_crawl/settings.py` (throttling, caps, user agent)
- Tests & fixtures: `tests/test_vrm_parse.py`, `tests/data/va_page_sample.html`
- Runtime deps: `requirements.txt`; Dev tools: `dev-requirements.txt`; Config: `pyproject.toml`, `mypy.ini`

---

### How to Add a New Field (Example)

Goal: add a `sleeps` column parsed from the inline JSON model.

1) Update `vrm_crawl/spiders/vrm.py` to include the field in item construction (keep key order):

```diff
@@ def parse(self, response) -> Iterator[dict[str, Any]]:
-                item = {
+                item = {
                     "state": state,
                     "name": prop.get("name", ""),
                     "city": prop.get("city", ""),
                     "address": prop.get("address", ""),
                     "price": prop.get("price", ""),
+                    "sleeps": prop.get("sleeps", ""),
                     "bedrooms": prop.get("bedrooms", ""),
                     "bathrooms": prop.get("bathrooms", ""),
                     "url": prop.get("url", ""),
                 }
```

2) Adjust tests/fixtures to reflect the new field:

- In `tests/data/va_page_sample.html`, add `"sleeps": "8"` (and a value for the second property) inside each property object of the `window.__INITIAL_STATE__` JSON.
- In `tests/test_vrm_parse.py`, add an assertion to verify extraction:

```python
prop1 = result["properties"][0]
assert prop1["sleeps"] == "8"
```

3) Smoke-test locally (limits to the first page):

```bash
scrapy crawl vrm -a states=VA -s CLOSESPIDER_PAGECOUNT=1
```

Notes:
- Keep the `sleeps` key in the exact position you want it to appear as a column; Excel headers come from `list(item.keys())` of the FIRST item written to each sheet.
- The pipeline requires no changes; it writes whatever keys are present.

### Troubleshooting

- Inline model not found: If `extract_inline_model` returns `None`, the site may have changed the init variable name or format. Update the regex in `extract_inline_model()` to match the new pattern (e.g., `__PRELOADED_STATE__`). Keep `re.DOTALL` and non-greedy matching.
- Pagination broken: If pages stop early or loop, update the next-link selector in `parse()` (currently `a.next-page`) to the current site markup.
- Columns shifted/missing in Excel: This usually means the first item for a state had a different key order or missing keys. Ensure the first yielded item contains the full, ordered set of keys you want as headers.
- Excel file locked: Close the workbook before running; `openpyxl` cannot write to an open file.
- Hitting page cap: Increase `VRM_MAX_PAGES` in `settings.py` if you intentionally need more pages (use cautiously).
- Robots/Throttling: Scraper respects robots.txt and uses delays. If blocked, review robots first; only set `ROBOTSTXT_OBEY=False` if you have permission. Adjust `DOWNLOAD_DELAY`/autothrottle settings in `settings.py` as needed.
- YAML state loading: `_load_states_from_yaml()` falls back to `["VA"]` if `states.yml` cannot be read. Verify the file exists at repo root and has the `states:` list.

