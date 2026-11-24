"""Local entrypoint for Infra Monitor."""

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") in ("1", "true", "True")
    port = int(os.environ.get("PORT", "5001"))
    # Bind to localhost only for the local demo.
    app.run(host="127.0.0.1", port=port, debug=debug)
