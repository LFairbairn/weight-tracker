# Weight Tracker

A personal weight tracking app with medication dose overlay — visualise how medication adjustments correlate with your weight loss over time.

---

## Features

- Log weight entries with notes
- Visualise weight over time with adjustable chart scales (1 week → all time)
- Overlay medication dose changes as annotations on the chart
- BMI auto-calculation
- Goal progress tracking
- Linear regression trend projections (full history + rolling window)
- Per-dose weight loss statistics
- Historic data import

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + FastAPI |
| Database | PostgreSQL |
| Frontend | React |
| Charting | ApexCharts (react-apexcharts) |
| Infrastructure | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Backend Testing | pytest |
| Frontend Testing | Vitest + React Testing Library |

---

## Architecture

```mermaid
graph TD
    subgraph Docker Compose
        FE[Frontend Container\nReact app]
        BE[Backend Container\nFastAPI]
        DB[(Database Container\nPostgres)]
    end

    User([User / Browser]) -->|HTTP requests| FE
    FE -->|REST API calls\nJSON| BE
    BE -->|SQL queries| DB
    DB -->|query results| BE
    BE -->|JSON responses| FE
    FE -->|renders UI| User
```

---

## User Flow

```mermaid
flowchart TD
    A([User opens app]) --> B[Dashboard]

    B --> C[View weight chart]
    C --> C1[Adjust time scale\n1w / 1m / 3m / 6m / 1y / all]
    C --> C2[See medication dose\nchange annotations]
    C --> C3[View trend projection\nfull history + rolling window]

    B --> D[Log weight entry]
    D --> D1[Enter weight + optional notes]
    D1 --> D2[Entry saved → chart updates]

    B --> E[Manage medications]
    E --> E1[Add medication]
    E --> E2[Log dose change]
    E2 --> E3[Dose marker appears on chart]

    B --> F[View stats]
    F --> F1[Current weight + trend]
    F --> F2[BMI card]
    F --> F3[Goal progress bar]
    F --> F4[Per-dose weight loss breakdown]
    F --> F5[Waist measurement chart\nwith medication overlay]

    B --> G[Import historic data]
    G --> G1[Bulk upload past entries]
    G1 --> D2
```

---

## Project Structure

```
weight-tracker/
├── backend/
│   ├── Dockerfile
│   └── ...
├── frontend/
│   ├── Dockerfile
│   └── ...
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

---

## Data Model

| Table | Fields |
|---|---|
| `users` | id, name, height, target_weight, weight_unit (kg/lbs/st), measurement_unit (cm/inches), created_at |
| `weight_logs` | id, user_id, date, weight_kg, waist_cm, notes |
| `medications` | id, user_id, name, start_date |
| `medication_doses` | id, medication_id, dose, unit (mg/ml), date_changed |

> All measurements stored internally in base units (kg, cm). Display units are converted at the app layer based on user preference.

---

## API Endpoints

### Users
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/users/me` | Get current user profile |
| PUT | `/api/users/me` | Update height, units (kg/lbs), target weight |

### Weight Logs
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/weight` | Paginated weight history |
| POST | `/api/weight` | Log a new weight entry |
| PUT | `/api/weight/{id}` | Edit an entry |
| DELETE | `/api/weight/{id}` | Remove an entry |

### Medications
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/medications` | List all medications |
| POST | `/api/medications` | Add a new medication |
| PUT | `/api/medications/{id}` | Update medication name/notes |
| DELETE | `/api/medications/{id}` | Remove a medication |
| POST | `/api/medications/{id}/doses` | Log a dose change |
| GET | `/api/medications/{id}/doses` | Get dose history |

### Stats & Trends
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/stats/summary` | Current weight, BMI, total lost, % to goal |
| GET | `/api/stats/trend` | Linear regression projection + R² score |
| GET | `/api/stats/chart` | Combined chart payload (weights + dose markers + trend line) |

---

## Authentication & Multi-User

**Stage 1 (current):** Single-user, no authentication required. The app works immediately on open — no sign-up, no login screen. Data is stored in a self-hosted Postgres instance. Device backups (iOS/Android) handle data persistence across phone upgrades.

**Stage 2 (future consideration):** If opened to other users, authentication could be added at that point. The data model is designed to support this — every table includes a `user_id` field — but no auth system will be built in Stage 1.

---

## Getting Started

> Setup instructions will be added as the project is built out.
