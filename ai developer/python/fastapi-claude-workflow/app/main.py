from fastapi import FastAPI
import datetime

app = FastAPI(title="Claude Code Checkpoint API")

# Application version and start time for uptime calculations
APP_VERSION = "0.1.0"
START_TIME = datetime.datetime.utcnow()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/health-details")
def health_details():
    """Return basic health info including status, version, and uptime in seconds."""
    now = datetime.datetime.utcnow()
    uptime_seconds = int((now - START_TIME).total_seconds())
    return {
        "status": "ok",
        "version": APP_VERSION,
        "uptime_seconds": uptime_seconds,
    }