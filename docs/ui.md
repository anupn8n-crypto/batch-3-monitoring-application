# UI pages

Local demo UI for **Infra Monitor** (Flask + Jinja). Read-only metrics views after sign-in.

| Path | Purpose |
| --- | --- |
| `/login` | Sign in (default user `admin`) |
| `/` | Fleet overview — CPU / Memory / Network / Ports placeholders |
| `POST /logout` | Clear session |

**Intent:** L1/L2/L3 can view host signals without SSH. Metrics panels are display-only.
