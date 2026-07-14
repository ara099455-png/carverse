"""CarVerse configuration. Swap DB by changing one line."""
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "carverse-dev-secret")

    # SQLite (default) — for PostgreSQL just set env var:
    # DATABASE_URL=postgresql://user:pass@localhost/carverse
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///carverse.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin key (used by admin panel via X-Admin-Key header)
    ADMIN_KEY = os.environ.get("ADMIN_KEY", "carverse")