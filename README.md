# VRM Properties Scraper

A responsible, rate-limited web scraper for VRM Properties vacation rental listings. Built with Scrapy, this tool extracts property data from VRM Properties state pages and exports to multi-sheet Excel workbooks for research and analysis.

> For AI coding agents: see `.github/copilot-instructions.md` for repo-specific guidance on architecture, workflows, and conventions.

## Features

- **State-based scraping** with configurable state selection (CLI or YAML config)
- **Multi-sheet Excel output** - one worksheet per state with automatic workbook management
- **Inline JSON parsing** - extracts property data from page initialization scripts
- **Rate limiting & throttling** - respectful crawling with configurable delays (2s default)
- **Safety caps** - maximum 250 pages per state to prevent runaway scrapes
- **Robust error handling** - graceful fallbacks for missing data
- **Property slug generation** - URL-friendly identifiers for properties

## Tech Stack

- **Python 3.11+** - Modern Python with type hints
- **Scrapy 2.11** - Production-grade web scraping framework
- **openpyxl 3.1** - Excel workbook generation
- **PyYAML 6.0** - Configuration file parsing
- **pytest** - Testing framework
- **Ruff** - Fast Python linter and formatter
- **mypy** - Static type checking
- **Bandit** - Security vulnerability scanner
- **GitHub Actions** - CI/CD and automated workflows

## Directory Layout

```
vrm_crawl/              # Scrapy project root
├── __init__.py
├── items.py            # Item definitions (placeholder)
├── middlewares.py      # Custom middleware (placeholder)
├── pipelines.py        # MultiSheetExcelPipeline implementation
├── settings.py         # Scrapy settings (throttling, user-agent, caps)
└── spiders/
    ├── __init__.py
    └── vrm.py          # VrmSpider with state filtering & JSON parsing

tests/                  # Test suite
├── __init__.py
├── data/
│   └── va_page_sample.html  # HTML fixture for offline testing
└── test_vrm_parse.py   # Unit tests for regex extraction & slug logic

output/                 # Generated Excel files (gitignored)

.github/workflows/      # CI/CD automation
├── ci.yml              # Lint, format, type check, security scan, tests
├── nightly-scrape.yml  # Scheduled daily scrapes
├── codeql.yml          # CodeQL security analysis
├── gitleaks.yml        # Secret scanning
└── bandit.yml          # Scheduled bandit security scans

requirements.txt        # Runtime dependencies (pinned)
dev-requirements.txt    # Development tools (pinned)
pyproject.toml          # Ruff, mypy, pytest config
mypy.ini                # Type checking configuration
states.yml              # Fallback state list
.gitignore              # Excludes output/, .scrapy, etc.
LICENSE                 # MIT License
README.md               # This file
```

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Git

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/paruff/scrapper.git
   cd scrapper
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install runtime dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development dependencies (optional):**
   ```bash
   pip install -r dev-requirements.txt
   ```

## Running the Scraper

### Basic Usage

Scrape using states from `states.yml` (default: VA, TX, NC, FL, CA):
```bash
scrapy crawl vrm
```

### Custom State Selection

Override states via command-line argument (takes precedence over `states.yml`):
```bash
scrapy crawl vrm -a states=VA,TX,NC
```

### Output

- Excel workbook created in `output/vrm_listings_YYYY-MM-DD.xlsx`
- One worksheet per state (e.g., "VA", "TX", "NC")
- New workbook created daily; existing workbooks are appended

### Sample Scrape (Testing)

Run a quick test scrape to verify setup:
```bash
scrapy crawl vrm -a states=VA -s CLOSESPIDER_PAGECOUNT=5
```

## Excel Schema

Each state worksheet contains the following columns:

| Column    | Description                          | Example                          |
|-----------|--------------------------------------|----------------------------------|
| state     | Two-letter state code                | VA                               |
| name      | Property name                        | Beach House Paradise             |
| city      | City location                        | Virginia Beach                   |
| address   | Street address                       | 123 Ocean Ave                    |
| price     | Rental price                         | $2500/week                       |
| bedrooms  | Number of bedrooms                   | 4                                |
| bathrooms | Number of bathrooms                  | 3                                |
| url       | Property detail page URL             | https://www.vrm.../beach-house   |
| slug      | URL-friendly property identifier     | beach-house-paradise-virginia-beach-va |

## Tests

### Run Tests

Execute the full test suite:
```bash
pytest
```

Run with coverage report:
```bash
pytest --cov=vrm_crawl --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_vrm_parse.py
```

### Test Coverage

- **Regex extraction tests** - Validates inline JSON model parsing from HTML fixtures
- **Slug generation tests** - Ensures proper URL-friendly identifier creation
- **Edge case handling** - Tests malformed JSON, empty fields, special characters

## Compliance / Responsible Use

### Respectful Crawling

This scraper is designed for **ethical, rate-limited data collection**:

- ✅ **Obeys robots.txt** - Respects site crawling rules
- ✅ **Rate limiting** - 2-second delay between requests (configurable via `DOWNLOAD_DELAY`)
- ✅ **Auto-throttling** - Adaptive delays based on server response times
- ✅ **Safety caps** - Max 250 pages per state (`VRM_MAX_PAGES`)
- ✅ **Identifiable user-agent** - `VRMResearchBot/1.0` with contact info
- ✅ **Concurrent request limits** - Max 8 concurrent requests (default: 16)

### User-Agent String

```
VRMResearchBot/1.0 (+https://github.com/paruff/scrapper; respectful-use; contact maintainer)
```

### Usage Guidelines

- **Research & analysis only** - Not for commercial republication
- **Respect site terms of service** - Review VRM Properties TOS before use
- **Monitor impact** - Check server logs; reduce rate if causing issues
- **Disable in production** - Use `SCRAPE_DISABLE=true` env var to prevent accidental runs

### Nightly Scrape Safety

The `nightly-scrape.yml` workflow includes a `SCRAPE_DISABLE` gate:
- Set repository secret `SCRAPE_DISABLE=true` to disable scheduled scrapes
- Useful for maintenance periods or when scraping is temporarily undesired

## Common Pitfalls

### 1. Malformed State Codes
**Problem:** States must be uppercase two-letter codes.  
**Solution:** Use `VA,TX,NC` not `va,tx,nc` or full names.

### 2. Output Directory Missing
**Problem:** `output/` directory not created.  
**Solution:** Pipeline auto-creates `output/` on first run. Check permissions.

### 3. Robots.txt Blocking
**Problem:** `ROBOTSTXT_OBEY=True` may block scraping if site disallows.  
**Solution:** Review robots.txt. Override with `ROBOTSTXT_OBEY=False` (not recommended).

### 4. Page Count Exceeds Limit
**Problem:** Spider stops after 250 pages per state.  
**Solution:** Increase `VRM_MAX_PAGES` in `settings.py` (use cautiously).

### 5. JSON Parsing Fails
**Problem:** Inline model pattern doesn't match page structure.  
**Solution:** Update regex in `extract_inline_model()` to match actual site format.

### 6. Excel File Locked
**Problem:** Cannot write to Excel file while it's open.  
**Solution:** Close Excel before running scraper.

## Development Tooling

### Linting

Run Ruff linter:
```bash
ruff check .
```

Auto-fix issues:
```bash
ruff check --fix .
```

### Formatting

Check formatting:
```bash
ruff format --check .
```

Auto-format code:
```bash
ruff format .
```

### Type Checking

Run mypy (non-blocking; allows dynamic Scrapy code):
```bash
mypy vrm_crawl
```

### Security Scanning

Run Bandit security scanner:
```bash
bandit -r vrm_crawl/
```

Run Gitleaks secret scanning:
```bash
gitleaks detect --source . --verbose
```

## Jenkins Pipelines (IDP Golden Path)

This repo includes Jenkins pipelines that mirror the GitHub Actions workflows:

- `Jenkinsfile` (CI for PRs/branches):
   - Setup Python venv, install deps
   - Ruff lint and format check
   - mypy (non-blocking), bandit (non-blocking)
   - pytest with JUnit + coverage XML
   - Archives `coverage.xml` and any `output/` files

- `Jenkinsfile.nightly` (scheduled sample scrape):
   - Cron trigger around 2 AM UTC (`H 2 * * *`)
   - Respects `SCRAPE_DISABLE=true` to skip safely
   - Env knobs: `SCRAPE_STATES` (default `VA,TX,NC`), `CLOSESPIDER_PAGECOUNT` (default `5`)
   - Archives `output/` results

Jenkins hints:

- Agents must have `python3` available. Pipelines create `.venv` in workspace.
- Install JUnit plugin to visualize test results.
- Optionally install coverage publishers; pipeline archives `coverage.xml` regardless.

## Advanced Security

### GitHub Actions Workflows

1. **ci.yml** - Runs on every PR:
   - Lint (Ruff)
   - Format check (Ruff)
   - Type check (mypy, non-blocking)
   - Security scan (Bandit, non-blocking)
   - Unit tests (pytest)
   - Sample scrape job (validates spider execution)

2. **nightly-scrape.yml** - Scheduled daily at 2 AM UTC:
   - Scrapes VA, TX, NC states
   - Uploads Excel artifacts
   - Gated by `SCRAPE_DISABLE` environment variable

3. **codeql.yml** - Weekly CodeQL analysis:
   - Python security vulnerability scanning
   - Automated alerts for new issues

4. **gitleaks.yml** - Secret scanning:
   - Detects hardcoded credentials, API keys, tokens
   - Runs on push and PR events

5. **bandit.yml** - Monthly scheduled security audit:
   - Full Bandit scan with SARIF output
   - Uploads results to GitHub Security tab

### Dependabot

Automated dependency updates configured via `dependabot.yml`:
- Weekly pip dependency updates
- Weekly GitHub Actions version updates

## Roadmap Ideas

Future enhancements under consideration:

- [ ] **Dataclasses** - Replace dict items with typed `PropertyItem` dataclass
- [ ] **CSV/Parquet export** - Additional output formats beyond Excel
- [ ] **Database storage** - PostgreSQL/SQLite pipeline for persistent storage
- [ ] **Image downloading** - Fetch property photos with Scrapy `ImagesPipeline`
- [ ] **Geolocation enrichment** - Add lat/lon via geocoding API
- [ ] **Incremental scraping** - Track seen properties; only scrape new/updated
- [ ] **Multi-site support** - Generalize to other vacation rental platforms
- [ ] **API mode** - FastAPI wrapper for on-demand scraping
- [ ] **Docker deployment** - Containerized scraper with docker-compose
- [ ] **Monitoring & alerting** - Prometheus metrics + Grafana dashboards

## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Phil Ruff

---

**Disclaimer:** This scraper is provided for educational and research purposes. Users are responsible for ensuring compliance with applicable laws, terms of service, and ethical guidelines when scraping web data.
