import os
from datetime import timedelta


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


class Config:
    # SQLite is used locally. On Render, DATABASE_URL points to PostgreSQL.
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///employee_management.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY", "college-mini-project-secret-key")
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "college-mini-project-jwt-secret-key",
    )

    # JWT access token is valid for exactly 1 hour.
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # Browser uses JWT cookie; Postman/API clients can use Bearer token header.
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_SECURE = env_bool("JWT_COOKIE_SECURE", False)
    JWT_COOKIE_SAMESITE = "Lax"

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@123")
