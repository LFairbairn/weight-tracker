from fastapi import FastAPI

from app.routers import medications, stats, upload, users, weight_logs

app = FastAPI(title="Weight Tracker")

app.include_router(users.router)
app.include_router(weight_logs.router)
app.include_router(medications.router)
app.include_router(stats.router)
app.include_router(upload.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
