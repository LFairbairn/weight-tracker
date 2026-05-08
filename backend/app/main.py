from fastapi import FastAPI

from app.routers import users, weight_logs, medications, stats

app = FastAPI(title="Weight Tracker")

app.include_router(users.router)
app.include_router(weight_logs.router)
app.include_router(medications.router)
app.include_router(stats.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
