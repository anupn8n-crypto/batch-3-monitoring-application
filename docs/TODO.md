# TODO — Demo Monitoring Infrastructure (Linux Servers)

Incremental implementation checklist for AI-assisted development.  
Stack: **Python + Flask**, local demo only. Keep each step small enough to finish and verify in one short session.

Source of truth: `PRD.md` (problem, users L1/L2/L3, metrics: CPU / memory / network / ports).  
Feature focus: friendly **read-only UI**, **admin sign-in** (hashed password), **add Linux servers**.

**How to use:** complete steps in order; check the box only after the step’s *Done when* criteria pass.

---

## Phase 0 — Project initialization and basic UI

### Step 0.1 — Repository skeleton
- [x] Create local project layout:
  - `app/` (Flask package)
  - `tests/`
  - `docs/`
  - `.github/workflows/`
  - `.gitignore` (venv, `__pycache__`, `.env`, `*.db`, IDE files)
- [x] **Security:** ensure `.env` and any secret files are gitignored from day one
- [x] **Docs:** add root `README.md` with one-line project purpose and “local demo only” note
- [x] **Done when:** empty folders + `.gitignore` + minimal `README.md` exist

### Step 0.2 — Python environment
- [x] Add `requirements.txt` with pinned minimal deps: `Flask`, `python-dotenv`
- [x] Create local venv and install deps (`python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`)
- [x] **Security:** document “never commit `.venv`”
- [x] **Docs:** README section — create venv + install (3–4 lines max)
- [x] **Done when:** `flask --version` (or `python -c "import flask"`) works inside venv

### Step 0.3 — Minimal Flask app boots
- [x] Add `app/__init__.py` with `create_app()` factory
- [x] Add `app/routes.py` with a single `/` route
- [x] Add `run.py` (or `wsgi.py`) entrypoint
- [x] **Security:** set `debug=False` by default; read `FLASK_DEBUG` only from env for local work
- [x] **Docs:** README — how to start: `flask --app run run` (or equivalent), open `http://127.0.0.1:5000`
- [x] **Done when:** home page returns HTTP 200 with plain “Monitoring Demo” text

### Step 0.4 — Basic UI shell (read-only look)
- [x] Add Jinja templates: `base.html`, `index.html`
- [x] Add static CSS for a clean, simple layout (header, main, footer) — no card overload
- [x] Home page shows placeholder panels: CPU, Memory, Network, Ports (static “—” values)
- [x] Banner/label: **Read-only demo**
- [x] **Security:** enable Jinja auto-escaping (Flask default); do not render unsanitized HTML
- [x] **Docs:** short `docs/ui.md` — pages list + read-only intent
- [x] **Done when:** browser shows branded shell with four placeholder metric areas

### Step 0.5 — Config object
- [x] Add `app/config.py` with `SECRET_KEY` from env (fallback only for local demo)
- [x] Load `.env.example` values documented; create local `.env` (not committed)
- [x] **Security:** refuse weak/empty `SECRET_KEY` when `FLASK_ENV=production`; demo may use a documented local default
- [x] **Docs:** `.env.example` with `SECRET_KEY=`, `FLASK_DEBUG=1`
- [x] **Done when:** app reads config via `create_app()` without hard-coded secrets in code

---

## Phase 1 — Sign-in and unit tests

### Step 1.1 — Password hashing helper
- [x] Add dependency: `Werkzeug` (comes with Flask) for `generate_password_hash` / `check_password_hash`
- [x] Add `app/auth_utils.py` with `hash_password()` and `verify_password()`
- [x] **Security:** use pbkdf2/scrypt hash (Werkzeug default); never store plaintext passwords
- [x] **Docs:** note in `docs/security.md` — hashing approach
- [x] **Done when:** helper can hash and verify a sample password in a REPL/one-liner

### Step 1.2 — Unit tests for hashing
- [x] Add `pytest` (+ `pytest-flask` optional) to `requirements.txt` or `requirements-dev.txt`
- [x] Write `tests/test_auth_utils.py`: hash≠plaintext; correct password verifies; wrong password fails
- [x] **Security:** assert plaintext never appears in returned hash string as raw password
- [x] **Docs:** README — `pytest` one-liner
- [x] **Done when:** `pytest tests/test_auth_utils.py` passes

### Step 1.3 — Default admin user (config-based)
- [x] Default username: `admin`
- [x] Store only **hashed** password (env `ADMIN_PASSWORD_HASH` or hash a demo password at startup from `ADMIN_PASSWORD` then prefer hash-only in config)
- [x] Prefer: document generating hash once and putting `ADMIN_PASSWORD_HASH` in `.env`
- [x] **Security:** never log passwords; never commit real `.env`; demo password documented only in README as change-me
- [x] **Docs:** README — how to generate hash + set `.env`
- [x] **Done when:** app knows a single admin identity without plaintext in source

### Step 1.4 — Login page UI
- [x] Routes: `GET /login`, `POST /login`
- [x] Template: username + password form
- [x] **Security:** CSRF protection (Flask-WTF) **or** same-site session cookies + document CSRF follow-up if deferred; set `HttpOnly` session cookie; `SESSION_COOKIE_SAMESITE=Lax`
- [x] **Docs:** update `docs/ui.md` with `/login`
- [x] **Done when:** login form renders and rejects empty submit gracefully

### Step 1.5 — Session sign-in / sign-out
- [x] On valid credentials: set session user; redirect to home
- [x] On invalid: generic error (“Invalid credentials”) — no user enumeration
- [x] Add `POST /logout` (or GET with care) clearing session
- [x] Show username + Logout when authenticated; Login link when not
- [x] **Security:** regenerate session on login; constant-time verify via Werkzeug; rate-limit note for later (demo OK to skip code, document risk)
- [x] **Docs:** `docs/security.md` — session rules
- [x] **Done when:** login → home shows admin; logout clears access

### Step 1.6 — Protect routes (read-only app after login)
- [x] Require login for dashboard (`/`) and future server pages
- [x] Unauthenticated users redirect to `/login`
- [x] Entire metrics UI remains **read-only** (no edit controls yet except auth + later “add server” for admin)
- [x] **Security:** `@login_required` decorator; no metrics APIs public
- [x] **Docs:** note access model for L1/L2/L3 — shared admin demo login for MVP
- [x] **Done when:** hitting `/` logged out redirects to login

### Step 1.7 — Unit tests for auth routes
- [ ] `tests/test_auth_routes.py`: login success, login failure, logout, protected redirect
- [ ] Use Flask test client; no real browser required
- [ ] **Security:** failure test ensures no stack trace/password in response body
- [ ] **Docs:** mention auth tests in README
- [ ] **Done when:** `pytest` passes for auth utils + auth routes

---

## Phase 2 — CI/CD (GitHub Actions)

### Step 2.1 — Test workflow
- [ ] Add `.github/workflows/ci.yml`
- [ ] On push/PR: checkout, setup Python, install deps, run `pytest`
- [ ] **Security:** do not print secrets; use dummy `SECRET_KEY` / `ADMIN_PASSWORD_HASH` in CI env
- [ ] **Docs:** `docs/ci.md` — what CI runs
- [ ] **Done when:** workflow file is valid YAML and mirrors local `pytest`

### Step 2.2 — Lint (lightweight)
- [ ] Add `ruff` or `flake8` to dev deps
- [ ] CI job or step: lint `app/` and `tests/`
- [ ] **Security:** none beyond keeping deps pinned
- [ ] **Docs:** one line in `docs/ci.md`
- [ ] **Done when:** lint runs clean on current code

### Step 2.3 — Dependency audit note
- [ ] Document running `pip audit` locally (optional CI step)
- [ ] **Security:** record in `docs/security.md`
- [ ] **Done when:** doc section exists (CI step optional for demo)

---

## Phase 3 — Add Linux servers (inventory)

### Step 3.1 — Server model (local storage)
- [ ] Simple persistence: SQLite via SQLAlchemy **or** JSON file under `data/servers.json`
- [ ] Fields (minimal): `id`, `name`, `host` (hostname/IP), `created_at`
- [ ] **Security:** validate host (no shell metacharacters); never store SSH passwords in MVP unless explicitly required later
- [ ] **Docs:** `docs/servers.md` — fields + storage location
- [ ] **Done when:** can create/read a server record in code/tests

### Step 3.2 — Unit tests for validation
- [ ] Reject empty name/host; reject obviously invalid host strings
- [ ] **Security:** tests for injection-like host strings
- [ ] **Done when:** validation tests pass

### Step 3.3 — Add server form (admin only)
- [ ] Page `GET/POST /servers/new` (or modal on `/servers`)
- [ ] After login, admin can add a Linux server to the monitor list
- [ ] Flash success; redirect to server list
- [ ] **Security:** login required; CSRF on form; sanitize display of name/host
- [ ] **Docs:** update `docs/ui.md` + `docs/servers.md`
- [ ] **Done when:** authenticated user can add a server and see it listed

### Step 3.4 — Server list UI (read-only metrics placeholders)
- [ ] `/servers` table: name, host, status placeholder
- [ ] L1-friendly: clear empty state (“No servers yet”)
- [ ] **Security:** no inline JS with unsanitized host
- [ ] **Docs:** screenshot optional; describe list for L1/L2
- [ ] **Done when:** list page shows added servers

### Step 3.5 — Tests for server routes
- [ ] Add server while logged in; unauthenticated cannot add; validation errors
- [ ] **Done when:** `pytest` green

---

## Phase 4 — Metrics views (replace SSH for viewing)

### Step 4.1 — Metrics abstraction
- [ ] `app/metrics.py` interface: `get_cpu`, `get_memory`, `get_network`, `get_ports` for a server
- [ ] First implementation: **safe mock/demo provider** (deterministic fake data) so UI works offline
- [ ] **Security:** mock path only; no subprocess yet
- [ ] **Docs:** `docs/metrics.md` — provider interface + mock behavior
- [ ] **Done when:** dashboard shows non-empty mock values per server

### Step 4.2 — Server detail page (read-only)
- [ ] `/servers/<id>` — CPU, Memory, Network, Ports panels
- [ ] Read-only: no edit of metrics; display only
- [ ] **Security:** 404 for unknown id; no path traversal
- [ ] **Docs:** map panels to PRD pain (no SSH for viewing)
- [ ] **Done when:** detail page renders mock metrics

### Step 4.3 — Optional local collector (demo)
- [ ] If time: provider that reads **localhost** only (psutil) for the Cursor machine
- [ ] Gate behind config `METRICS_PROVIDER=mock|local`
- [ ] **Security:** no remote SSH command execution in MVP; document risk if added later
- [ ] **Docs:** minimal setup for `local` provider
- [ ] **Done when:** switching env shows real local CPU/mem on one machine

### Step 4.4 — Port usage panel
- [ ] Show listening ports / connection summary (mock or local via psutil)
- [ ] **Security:** do not expose process command lines with secrets
- [ ] **Done when:** Ports panel has tabular demo data

### Step 4.5 — Metrics tests
- [ ] Unit tests for mock provider shape; route tests for detail page
- [ ] **Done when:** `pytest` green

---

## Phase 5 — Polish for L1 / L2 / L3 demo

### Step 5.1 — Fleet overview
- [ ] Home page lists all servers with at-a-glance CPU/mem/network (read-only)
- [ ] **Docs:** L1 uses overview; L2 opens detail
- [ ] **Done when:** overview usable with 0 and N servers

### Step 5.2 — Flash messages and empty states
- [ ] Friendly empty states and error messages (no stack traces in UI)
- [ ] **Security:** generic errors to client
- [ ] **Done when:** UX checked manually once

### Step 5.3 — Final local runbook
- [ ] `docs/DEMO.md` — 5-minute path: venv, env, run, login, add server, view metrics
- [ ] Keep steps minimal (local Cursor host only)
- [ ] **Security:** remind change default demo password
- [ ] **Done when:** a new teammate can follow DEMO.md without extra help

### Step 5.4 — Align PRD acceptance (demo subset)
- [ ] Cross-check: no SSH needed to *view* demo metrics; admin login; add Linux server; read-only UI
- [ ] Update `PRD.md` status notes or link to this TODO if needed
- [ ] **Done when:** checklist in DEMO.md matches working app

---

## Phase 6 — Hardening (still demo-sized)

### Step 6.1 — Headers
- [ ] Add basic security headers (e.g. `X-Content-Type-Options=nosniff`, `X-Frame-Options=DENY`)
- [ ] **Docs:** list headers in `docs/security.md`
- [ ] **Done when:** headers visible on a response

### Step 6.2 — Remove debug from default run
- [ ] Confirm production-like local defaults: debug off unless env set
- [ ] **Done when:** README warns about debug mode

### Step 6.3 — CI green on main path
- [ ] Ensure GitHub Actions runs lint + tests on PR
- [ ] **Done when:** workflow documented and locally reproducible

---

## Suggested first coding session (smallest slice)

1. [ ] Phase 0.1–0.4 (init + basic UI)
2. [ ] Phase 1.1–1.2 (hash helpers + unit tests)
3. [ ] Stop, commit if requested, then continue 1.3–1.7

---

## Out of scope for this TODO (per demo constraints)

- Production HA, SSO, multi-tenant SaaS
- Remote SSH-based collection / agent install automation
- Full Prometheus/Grafana stack (unless later explicitly added)
- Public internet deployment

---

## Progress log

| Date | Step | Notes |
| --- | --- | --- |
| 2026-11-24 | 0.1–0.3 | Skeleton, venv, Flask boots; `/` returns `200 Monitoring Demo` |
| 2026-11-24 | 0.4–0.5 + login UI | Infra Monitor dark login (admin/hash), overview shell; http://127.0.0.1:5001/login |
| 2026-11-24 | 1.2 | `tests/test_auth_utils.py` + `requirements-dev.txt`; pytest green |
