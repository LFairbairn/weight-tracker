# TODO

> Tracking work in progress. Will migrate to GitHub Issues once initial setup is complete.

---

## Up Next
- [ ] Backend: schemas (request/response shapes)
- [ ] Backend: routers (weight, medications, users, stats)
- [ ] Backend: pytest setup + first tests
- [ ] Frontend: React app scaffold
- [ ] Frontend: Docker setup
- [ ] Frontend: dashboard layout
- [ ] Frontend: weight chart with ApexCharts
- [ ] Frontend: medication dose overlay annotations
- [ ] Frontend: CSV import flow
- [ ] CI: GitHub Actions workflow

## Completed
- [x] Backend: database.py — SQLAlchemy connection, session, Base
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
