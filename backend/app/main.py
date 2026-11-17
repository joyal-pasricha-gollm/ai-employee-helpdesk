"""FastAPI application entry point."""

from fastapi import FastAPI

from app.routes import auth

app = FastAPI(
    title="Employee Helpdesk API",
    version="0.1.0",
    description="Backend API for the Employee Helpdesk application.",
)

app.include_router(auth.router)


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    """Return a short message confirming that the API is running."""
    return {"message": "Employee Helpdesk API"}


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Report API liveness. Database checks will be added with database integration."""
    return {"status": "ok"}
