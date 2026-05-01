# TODO

> Tracking work in progress. Will migrate to GitHub Issues once initial setup is complete.

---

## Up Next
- [ ] CI: GitHub Actions workflow
- [ ] Backend: stats endpoint — rate of loss per dose period, R² linear regression fit per period, overall trend
- [ ] Frontend: waist measurement chart or toggle
- [ ] Frontend: add/edit weight log form
- [x] Frontend: stat cards — starting weight, total change, % lost, BMI, weekly avg, to goal

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
