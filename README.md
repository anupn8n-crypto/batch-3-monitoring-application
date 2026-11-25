# Infra Monitor (Linux demo)

Local Flask demo so internal L1/L2/L3 teams can view Linux host signals (CPU, memory, network, ports) without SSH. **Local demo only — not for production.**

GitHub: https://github.com/anupn8n-crypto/batch-3-monitoring-application  
Development branch: `dev` (open PRs into `main`).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Never commit `.venv` or `.env`.

## Tests

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest tests/test_auth_utils.py tests/test_auth_routes.py
```

## Run

```bash
source .venv/bin/activate
python run.py
```

Open http://127.0.0.1:5001/login

Demo login: **admin** / **admin123** (change via `.env`).

Optional: `FLASK_DEBUG=1 python run.py`

### Generate a password hash

```bash
python -c "from app.auth_utils import hash_password; print(hash_password('your-password'))"
```

Put the result in `.env` as `ADMIN_PASSWORD_HASH=...` and clear `ADMIN_PASSWORD`.

## Docs

- Product: `PRD.md`
- Checklist: `docs/TODO.md`
- UI: `docs/ui.md`
- Security: `docs/security.md`
