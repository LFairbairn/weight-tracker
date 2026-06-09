# TODO

> Tracking work in progress. Will migrate to GitHub Issues once initial setup is complete.

---

## Completed
- [x] README: polish with screenshots, Getting Started, corrected API docs, example data section
- [x] Example data: user-a-wegovy/ and user-b-mounjaro-switch/ committed to repo
- [x] Feature: CSV upload + first-time onboarding flow
- [x] Testing: pytest-cov, Vitest + RTL, ruff linting, ESLint in CI, 38 backend tests at 97% coverage
- [x] Frontend: toggle to hide/show main weight line on chart (trend lines viewable in isolation)
- [x] Frontend: projected goal date stat card — calculated from current dose regression
- [x] Frontend: add/edit weight log form — deferred, noted in README as future commercial enhancement
- [x] CI: GitHub Actions workflow — runs pytest on every push to main
- [x] Backend: stats endpoint — rate of loss per dose period, R² linear regression fit per period, overall trend (numpy + scipy)
- [x] Frontend: stat card — rate of loss on current dose (kg/wk)
- [x] Frontend: stat cards — starting weight, total change, % lost, BMI, weekly avg, to goal
- [x] Frontend: per-dose regression trend lines on chart (white dashed, toggleable)
- [x] Frontend: medication name initial shown on dose change annotations
- [x] Frontend: React app scaffold (Vite)
- [x] Frontend: Docker setup
- [x] Frontend: dashboard layout (dark theme, stat cards)
- [x] Frontend: weight chart with ApexCharts
- [x] Frontend: medication dose overlay annotations
- [x] Frontend: CSV import via seed script (61 entries + 4 dose changes)
- [x] Backend: schemas — User, WeightLog, Medication, MedicationDose (Create/Update/Response)
- [x] Backend: routers — users, weight-logs, medications + doses (full CRUD)
- [x] Backend: pytest setup + 6 passing tests (weight logs)
- [x] Backend: database.py — SQLAlchemy connection, session, Base, get_db
- [x] Backend: models — User, WeightLog, Medication, MedicationDose
- [x] Backend: Alembic setup + migration — all 4 tables created in Postgres
- [x] Stack decisions
- [x] README with architecture, data model, API endpoints
- [x] .gitignore
- [x] GitHub repo setup
- [x] Backend folder structure
- [x] uv + pyproject.toml + dependencies installed
- [x] Backend Dockerfile
- [x] docker-compose.yml with backend + Postgres containers
- [x] API health check endpoint working at localhost:8000/health
