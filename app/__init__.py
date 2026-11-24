"""Flask application factory for Infra Monitor (local demo)."""

import os

from flask import Flask

from app.auth_utils import hash_password
from app.config import Config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # Debug only when explicitly enabled via env (default: off).
    app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", "0") in ("1", "true", "True")

    # Prefer precomputed hash; otherwise hash demo password once at startup.
    if not app.config.get("ADMIN_PASSWORD_HASH"):
        demo_pw = app.config.get("ADMIN_PASSWORD") or "admin123"
        app.config["ADMIN_PASSWORD_HASH"] = hash_password(demo_pw)

    from app.routes import bp

    app.register_blueprint(bp)
    return app
