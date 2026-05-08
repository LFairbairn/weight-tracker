# TODO

> Tracking work in progress. Will migrate to GitHub Issues once initial setup is complete.

---

## Up Next
- [ ] Frontend: projected goal date stat card — calculated from current dose regression
- [ ] Frontend: add/edit weight log form
- [ ] Feature: CSV upload + first-time onboarding flow (detect no user → setup screen → upload weight log CSV → optional medication doses CSV → dashboard)
- [ ] Example data: example-data/ folder committed to repo with mock weight_log.csv + medication_doses.csv (portfolio demo — design a dataset that clearly shows dose-response trends)

## Completed
- [x] CI: GitHub Actions workflow — runs pytest on every push to main
- [x] Backend: stats endpoint — rate of loss per dose period, R² linear regression fit per period, overall trend (numpy + scipy)
- [x] Frontend: stat card — rate of loss on current dose (kg/wk)
- [x] Frontend: stat cards — starting weight, total change, % lost, BMI, weekly avg, to goal
- [x] Frontend: per-dose regression trend lines on chart (white dashed, toggleable)

## Completed
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
