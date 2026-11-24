# Security notes (local demo)

- Passwords verified with Werkzeug `check_password_hash` (pbkdf2/scrypt). Plaintext is never stored in source.
- Prefer `ADMIN_PASSWORD_HASH` in `.env`. `ADMIN_PASSWORD` is only a local bootstrap and is hashed in memory at startup.
- Session cookie: `HttpOnly`, `SameSite=Lax`. Bound to `127.0.0.1` only.
- Login failures return a generic **Invalid credentials** message.
- Do not commit `.env` or `.venv`. Change the demo password before any shared lab use.
- Debug mode is off unless `FLASK_DEBUG=1`.
