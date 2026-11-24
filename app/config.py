"""Application configuration — secrets come from environment."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Local demo defaults. Override via .env — never commit real secrets."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me-infra-monitor")
    # Demo admin: username fixed; password verified against hash only.
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH", "")
    # Optional bootstrap for local demo only (hashed at runtime, never stored).
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # localhost HTTP demo
