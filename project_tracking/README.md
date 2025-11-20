# Project Tracking (Stories, Features, Tasks)

This repository includes a file-based tracking approach that AI agents can read directly without external access.

- Use `project_tracking/backlog.yml` to list Features and Stories with status and priority.
- Add one Markdown file per story under `project_tracking/stories/` with context and acceptance criteria.
- Keep acceptance criteria synchronized with BDD `.feature` files under `tests/bdd/features/`.

You can still use GitHub Issues/Projects for collaboration; this directory ensures agents have local access to the authoritative backlog.

## Conventions

- Feature IDs: `VRM-F###` (e.g., `VRM-F001`).
- Story IDs: `VRM-S###` mapped to features (e.g., `VRM-S010`).
- Task IDs: optional `VRM-T###` referenced inside story pages.

## Lifecycle

1. Author a story in `stories/` with “Context”, “Goal”, and “Acceptance Criteria”.
2. Link to or add a Gherkin scenario in `tests/bdd/features/`.
3. Implement code and steps until the BDD scenarios pass in CI.
4. Update `backlog.yml` status to `done`.

## Try It

- See `project_tracking/backlog.yml` and `project_tracking/stories/VRM-S001-scrape-listings.md`.
