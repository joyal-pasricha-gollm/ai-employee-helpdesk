"""FastAPI application entry point."""

import logging

from fastapi import FastAPI

from app.routes import ai, auth, feedback

# Show INFO-level app events (logins, AI analysis, decisions) in the server console.
# Log messages never contain passwords, tokens or ticket text.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = FastAPI(
    title="Employee Helpdesk API",
    version="0.1.0",
    description="Backend API for the Employee Helpdesk application.",
)

app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(feedback.router)


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    """Return a short message confirming that the API is running."""
    return {"message": "Employee Helpdesk API"}


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Report API liveness. Database checks will be added with database integration."""
    return {"status": "ok"}
