# Product Requirements Document (PRD)
# Demo Monitoring Infrastructure — Linux Servers

| Field | Value |
| --- | --- |
| **Product** | Demo Monitoring Infrastructure (Linux Servers) |
| **Document type** | Software Specification / PRD |
| **Version** | 0.3 (Draft) |
| **Status** | Draft for review |
| **Owner** | Operations / Platform |
| **Primary audience** | Internal L1 / L2 / L3 teams across Infrastructure and Application Development |
| **Last updated** | 2026-11-24 |

---

## 1. Executive summary

Build a **self-contained demo monitoring stack** that observes one or more Linux servers and shows, in a single dashboard experience — **without SSH or interactive login to each host**:

- Live and historical **host metrics**: CPU, memory, network usage
- **Port usage details**: listening ports, connection state summary, and key service ports
- Disk, load, and **service / process health** for a small set of demo workloads
- **Alerting** with clear severity and acknowledgable incidents
- Optional **log snippets** tied to host or service events

The goal is **demonstration and training**, not production multi-tenant SaaS. The stack must be easy to deploy (ideally one command or compose file), realistic enough to sell the monitoring story, and safe to tear down.

---

## 2. Problem statement

### 2.1 Current state (pain)

Today, operators must **log into each Linux server** (SSH / console) and run ad-hoc commands (`top`, `free`, `vmstat`, `ss`/`netstat`, `iftop`, etc.) to see:

- Real-time **CPU** usage
- Real-time **memory** usage
- Real-time **network** usage
- **Port usage** details (what is listening, what is connected, whether a service port is up)

This does not scale across hosts, is hard to compare side-by-side, leaves no shared historical view, and is unsuitable for demos or training.

### 2.2 Desired state

Operators open a **central dashboard**, select a host (or view the fleet), and see the same real-time signals — plus history and alerts — **without logging into the servers**.

### 2.3 Why a demo infrastructure

Stakeholders also need a repeatable environment to:

1. Show how Linux servers are instrumented once, then observed centrally
2. Visualize resource pressure, network, and port health in real time
3. Demonstrate alert → investigation → resolution **without SSH**
4. Train operators without touching production systems

Without a dedicated demo stack, demos fall back to live SSH sessions — inconsistent, fragile, and a poor product story.

---

## 3. Goals and non-goals

### 3.1 Goals

| ID | Goal |
| --- | --- |
| G0 | Eliminate the need to SSH/login to servers for real-time CPU, memory, network, and port usage checks |
| G1 | Monitor Linux hosts with industry-standard metrics within minutes of boot |
| G2 | Provide Grafana-style (or equivalent) dashboards suitable for live demos |
| G3 | Fire and clear alerts based on configurable thresholds |
| G4 | Simulate load / failure scenarios for demo scripts |
| G5 | Deploy and reset the full stack with documented, repeatable steps |
| G6 | Keep resource footprint suitable for a laptop, small VM, or single demo host |

### 3.2 Non-goals

| ID | Non-goal |
| --- | --- |
| NG1 | Production HA, multi-region, or enterprise scale |
| NG2 | Full APM / distributed tracing product |
| NG3 | Windows, macOS, or network-device monitoring as first-class targets |
| NG4 | Long-term retention, compliance audit packs, or customer data isolation |
| NG5 | Mobile apps or white-label customer portals |

---

## 4. Users and personas

### 4.1 User population

Users are **internal only** — no external customers as end users of this demo stack.

| Dimension | Coverage |
| --- | --- |
| **Support tiers** | L1, L2, L3 |
| **Org groups** | Infrastructure teams **and** Application Development teams |
| **Access intent** | View real-time Linux host health (CPU, memory, network, ports) without SSH; train and demo the same workflow |

### 4.2 Tier personas

| Persona | Typical org | Primary job with this stack | Needs from the UI |
| --- | --- | --- | --- |
| **L1 — Frontline / NOC / service desk** | Infra & App Dev support | First response: confirm host is up, spot obvious CPU/mem/network/port issues, escalate with evidence | Simple fleet overview, clear red/green status, host search, basic alert list, copyable host identity |
| **L2 — Operations / platform / app support** | Infra ops; App Dev support engineers | Diagnose: correlate CPU, memory, network, and port usage; validate service ports; acknowledge alerts; follow runbooks | Host deep-dive dashboards, port usage panel, time-range history, alert detail → host link, runbook alignment |
| **L3 — Subject-matter experts / senior engineers** | Infra architects/SRE; senior App Dev | Deep triage, threshold/tuning feedback, complex multi-host comparison, validate exporter/probe gaps | Full metric detail, PromQL/Explore (or equivalent), alert rule visibility, ability to compare hosts/roles |

### 4.3 Cross-cutting personas

| Persona | Need |
| --- | --- |
| **Infrastructure group** | Reliable Linux server visibility across demo/lab hosts they own; standard ops triage path for L1→L2→L3 |
| **Application Development group** | See whether *their* app hosts/ports are healthy without waiting on infra SSH; share the same dashboards during incidents and demos |
| **Demo / training lead** (any tier) | Scripted failure scenarios, predictable alerts, reset path for internal enablement sessions |
| **Implementing engineer** | Clear architecture, ports, configs, and acceptance criteria to build and hand over the stack |

### 4.4 Escalation model (supported by the product)

```text
L1  →  Detect / confirm symptom on dashboard (no SSH)
      →  Capture host, metric, alert screenshot/link
L2  →  Diagnose with host detail (CPU / mem / net / ports)
      →  Apply runbook; escalate if unresolved
L3  →  Deep analysis, rule/threshold gaps, exporter/probe issues
      →  Feed improvements back into demo config / runbooks
```

**Product implication:** dashboards and alerts must be usable by L1 without PromQL expertise, while still giving L2/L3 enough depth that they do not fall back to SSH solely to *view* usage.

---

## 5. Scope

### 5.1 In scope (MVP)

- Linux target hosts (Ubuntu 22.04 / RHEL-compatible recommended for demos)
- Host metrics **visible without SSH**:
  - CPU (utilization, load)
  - Memory (used / available / cache)
  - Network usage (bytes in/out, errors/drops if available)
  - **Port usage details** (listening ports, TCP connection counts by state, status of configured critical ports)
  - Disk usage/I/O, uptime
- Node exporter (or equivalent) on each monitored host; enable collectors needed for network/port visibility
- Metrics store + query (e.g. Prometheus)
- Visualization (e.g. Grafana) with at least:
  - Fleet overview (all hosts) — CPU, memory, network at a glance
  - Single-host deep dive — including **Ports / network connections** panel
  - Alert / incident board
- Alert rules for: high CPU, high memory, low disk space, host down / scrape failure, critical port down (optional but Should)
- Demo “chaos” helpers: CPU burn, fill disk (safe path), stop a demo service (to show port/service impact)
- Docker Compose (or equivalent) for the monitoring plane
- README: deploy, demo script, reset

### 5.2 Out of scope (later / optional)

- Kubernetes cluster monitoring
- Synthetic HTTP checks beyond a single demo URL
- SSO / RBAC beyond a shared demo login
- Anomaly ML / forecasting
- Auto-remediation / runbook automation
- Inventory CMDB integration

---

## 6. Success metrics (demo quality)

| Metric | Target |
| --- | --- |
| Time to first dashboard after clone | ≤ 15 minutes on a prepared host |
| Hosts visible after agent install | ≤ 2 minutes |
| Real-time CPU / memory / network / ports without SSH | Achieved for all MVP hosts from the central UI |
| Metric freshness on dashboards | ≤ 30 seconds behind wall clock (demo scrape intervals OK) |
| Alert latency (threshold breach → UI) | ≤ 60 seconds (demo-tuned scrape/eval intervals OK) |
| Demo script completion (healthy → incident → recover) | ≤ 10 minutes |
| Stack teardown / reset | ≤ 5 minutes without leftover demo load processes |

---

## 7. User journeys

### 7.1 Happy path — replace SSH with the dashboard

1. Presenter states the old workflow: SSH → `top` / `free` / `ss` on each box.
2. Opens overview dashboard instead — all demo Linux hosts **Up** with CPU, memory, network.
3. Drills into one host: CPU, memory, network usage, and **port usage** panels — no login to the server.
4. Optionally compares two hosts side-by-side to show multi-host visibility SSH cannot give easily.

### 7.2 Incident path — disk pressure

1. Presenter runs demo helper: fill `/var/demo-fill` (capped).
2. Disk usage crosses threshold; alert fires (Warning → Critical as configured).
3. Presenter shows alert detail + affected host panel.
4. Presenter clears fill; alert resolves; dashboard returns to healthy.

### 7.3 Incident path — host / exporter down

1. Stop node exporter or pause the target container/VM network path.
2. Scrape failure / host-down alert appears on alert board.
3. Restore exporter; alert clears.

### 7.4 Internal L1 → L2 → L3 triage path

1. **L1** sees alert or ticket symptom → opens fleet overview → confirms host status, CPU/mem/network/ports at a glance → escalates with dashboard link (no SSH).
2. **L2** opens host detail → correlates panels and critical ports → acknowledges alert (if supported) → follows runbook.
3. **L3** (if needed) uses deep metrics / Explore, compares hosts, adjusts thresholds or probes, updates runbook feedback.

---

## 8. Functional requirements

### 8.1 Host monitoring

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-M1 | Collect CPU utilization (% busy / idle / iowait) per host | Must |
| FR-M2 | Collect memory used / available / cache | Must |
| FR-M3 | Collect filesystem usage % for root and at least one data mount | Must |
| FR-M4 | Collect network bytes in/out (and errors/drops if available) for primary interface | Must |
| FR-M5 | Collect load average and uptime | Must |
| FR-M6 | Collect disk I/O (read/write rates) | Should |
| FR-M7 | Label metrics with `instance`, `hostname`, `env=demo` | Must |
| FR-M8 | Support ≥ 3 Linux targets in one demo without config rewrite beyond a targets list | Must |
| FR-M9 | Expose **port usage details** without SSH: listening TCP/UDP ports (or equivalent table/panel) | Must |
| FR-M10 | Expose TCP connection counts by state (e.g. established, time-wait, listen) | Must |
| FR-M11 | Track up/down (or response) for a configurable list of **critical ports** per host (e.g. 22, 80, 443, app port) | Should |
| FR-M12 | All FR-M1–M11 data must be viewable from the central UI with **no server login** | Must |

### 8.2 Discovery & configuration

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-D1 | Targets defined in a single config file or compose override | Must |
| FR-D2 | Documented static scrape config (file SD acceptable; Consul optional later) | Must |
| FR-D3 | Health of scrape targets visible in monitoring UI | Must |

### 8.3 Dashboards

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-UI1 | Fleet overview: status, CPU, memory, network, disk per host | Must |
| FR-UI2 | Host detail dashboard with time-range selector covering CPU, memory, network, ports | Must |
| FR-UI3 | Pre-provisioned dashboards (no manual import for MVP demo) | Must |
| FR-UI4 | Dark/light theme acceptable; default chosen for projector readability | Should |
| FR-UI5 | Deep link from alert to host dashboard | Should |
| FR-UI6 | Dedicated **Port usage** panel/table on host detail (listen ports and/or connection summary) | Must |
| FR-UI7 | Network usage panel with live throughput suitable for replacing `iftop`/`nload`-style SSH checks | Must |
| FR-UI8 | L1-friendly fleet view: searchable hosts, clear Up/Down, top CPU/mem/network signals without query language | Must |
| FR-UI9 | L2/L3 host deep dive and time-range history sufficient for triage without SSH for viewing | Must |
| FR-UI10 | Shared access model suitable for both Infrastructure and Application Development internal users (single demo login or documented group access) | Must |

### 8.4 Alerting

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-A1 | Alert: HostDown / scrape failure | Must |
| FR-A2 | Alert: CPU > threshold for sustained window (default 80% / 2m for demo) | Must |
| FR-A3 | Alert: Memory > threshold (default 85%) | Must |
| FR-A4 | Alert: Disk > threshold (default 85% on `/`) | Must |
| FR-A5 | Alert severity labels: `warning`, `critical` | Must |
| FR-A6 | Alertmanager (or equivalent) with UI and at least one receiver (webhook or email stub) | Must |
| FR-A7 | Silence / inhibit support documented for live demos | Should |
| FR-A8 | Alert: CriticalPortDown when a configured port fails check | Should |

### 8.5 Demo tooling

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-T1 | Script: generate CPU load for N seconds | Must |
| FR-T2 | Script: allocate/fill disk under a safe demo path with hard cap | Must |
| FR-T3 | Script: stop/start a labeled demo systemd unit or container | Must |
| FR-T4 | Script: reset all demo load artifacts | Must |
| FR-T5 | Optional log generator writing to a watched file | Could |

### 8.6 Operations of the stack

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-O1 | Single entrypoint to start monitoring plane (`docker compose up -d` or make target) | Must |
| FR-O2 | Documented ports, credentials, and data volumes | Must |
| FR-O3 | Default credentials clearly marked **demo-only** | Must |
| FR-O4 | Retention configurable; default short (e.g. 7 days or less) | Should |

---

## 9. Non-functional requirements

| ID | Area | Requirement |
| --- | --- | --- |
| NFR-1 | Performance | Scrape interval default 15s (demo-friendly); stack usable on 2 vCPU / 4 GB RAM host monitoring ≤ 5 targets |
| NFR-2 | Reliability | Monitoring plane survives target host restarts; dashboards reload after brief outage |
| NFR-3 | Security | Bind admin UIs to localhost or private network by default; no public exposure in docs without warning |
| NFR-4 | Security | No collection of SSH keys, passwords, or PII; metrics only |
| NFR-5 | Usability | Presenter can run full demo without editing PromQL live; ops can answer CPU/mem/net/ports questions without SSH |
| NFR-9 | Access model | Day-to-day metric inspection uses the monitoring UI only; SSH remains for remediation, not for viewing usage |
| NFR-6 | Maintainability | Config as code (YAML); dashboards versioned in repo |
| NFR-7 | Portability | Works on Linux demo host with Docker Engine; agent install docs for bare-metal Linux targets |
| NFR-8 | Observability of self | Monitoring plane exposes its own health (Prometheus `/ -/healthy`, Grafana health) |

---

## 10. Proposed architecture (reference)

> Architecture is **recommended for MVP**, not locked. Alternatives (Zabbix, Netdata, Elastic Stack) may be substituted if they meet the same FR/NFR set.

```
┌─────────────────────────────┐     scrape      ┌──────────────────────┐
│  Linux target(s)            │◄───────────────│  Prometheus          │
│  - node_exporter            │                 │  - alert rules       │
│    (cpu/mem/net/netdev/     │                 └──────────┬───────────┘
│     + netstat/sockstat)     │                            │
│  - (optional) blackbox or   │                            │
│    port probe for critical  │                            ▼
│    ports                    │                 ┌──────────────────────┐
│  - (optional) demo app      │                 │  Alertmanager        │
│  - demo load scripts        │                 │  → webhook / email   │
└─────────────────────────────┘                 └──────────────────────┘
┌─────────────────────────────┐                 ┌──────────────────────┐
│  Operator / Presenter       │────────────────►│  Grafana             │
│  Browser (NO SSH needed     │   dashboards    │  CPU · Mem · Net ·   │
│  for viewing usage)         │                 │  Ports               │
└─────────────────────────────┘                 └──────────────────────┘
```

### 10.1 Components (MVP recommendation)

| Component | Role |
| --- | --- |
| **Prometheus** | Metrics TSDB, scrape, recording/alert rules |
| **Alertmanager** | Route, group, silence alerts |
| **Grafana** | Dashboards and demo UI (replaces SSH for viewing) |
| **node_exporter** | Linux host metrics; enable `netdev` + `netstat`/`sockstat` (or equivalent) for port/connection views |
| **blackbox_exporter** (optional) | Probe configured critical TCP ports for up/down |
| **Docker Compose** | Packaging for monitoring plane |
| **demo-scripts/** | Chaos / load / reset helpers |

### 10.2 Suggested ports (demo defaults)

| Service | Port |
| --- | --- |
| Grafana | 3000 |
| Prometheus | 9090 |
| Alertmanager | 9093 |
| node_exporter | 9100 |

---

## 11. Data model (conceptual)

### 11.1 Metric labels

- `job` — e.g. `node`
- `instance` — `host:9100`
- `hostname` — human-readable
- `env` — `demo`
- `role` — optional (`app`, `db`, `web`)

### 11.2 Alert payload (minimum fields)

- `alertname`
- `severity`
- `instance` / `hostname`
- `summary`
- `description`
- `startsAt` / `endsAt`
- `status` (`firing` | `resolved`)

### 11.3 Retention

- Default metrics retention: **7 days** (configurable)
- Demo does not require backups of TSDB

---

## 12. Alert rule specifications (defaults)

| Alert | Condition (illustrative) | For | Severity |
| --- | --- | --- | --- |
| HostDown | `up{job="node"} == 0` | 1m | critical |
| HighCPU | CPU busy > 80% | 2m | warning; > 95% critical |
| HighMemory | MemUsed / MemTotal > 85% | 2m | warning |
| DiskAlmostFull | FS used > 85% on `/` | 2m | warning; > 95% critical |
| CriticalPortDown | Probe of configured port fails | 1m | critical |

Exact PromQL to be finalized in implementation; thresholds must be overridable via config.

---

## 13. Demo script (acceptance narrative)

**Title:** “Linux server from healthy to incident and back”

1. Contrast: “Previously we’d SSH and run `top` / `free` / `ss`.”
2. Show fleet overview — all green (CPU, memory, network).
3. Open host A detail — CPU, memory, **network usage**, **port usage** panels.
4. Run `demo-scripts/cpu-burn.sh 180` — watch CPU rise — HighCPU fires.
5. Acknowledge / discuss alert routing.
6. Stop burn — alert resolves.
7. Run disk fill (capped) — DiskAlmostFull fires — clear fill — resolves.
8. Stop demo service / critical port — show port panel + CriticalPortDown (if enabled) — restart — resolves.
9. Stop node_exporter on host B — HostDown — restart — resolves.
10. Reset scripts — confirm clean state. **No SSH used for any viewing step.**

**Pass criteria:** Each step produces visible UI evidence within the latency targets in §6.

---

## 14. Installation & environments

| Environment | Purpose |
| --- | --- |
| **local-demo** | Engineer laptop / single VM; Compose stack + 1–2 exporters |
| **lab** | Shared training lab; 3+ Linux VMs as targets |
| **show-floor** | Hardened network binding; pre-seeded dashboards; longer scrape only if projector needs stability |

### 14.1 Prerequisites (MVP)

- Linux host with Docker + Compose plugin
- Outbound ability for image pulls (or pre-loaded images for offline demos)
- Target Linux hosts reachable on port 9100 from Prometheus

---

## 15. Security & compliance (demo-aware)

- Default passwords must be changed for any shared lab; document in README.
- Do not expose Grafana/Prometheus to the public internet for demos.
- Disk-fill script must refuse to run outside approved path and hard size cap.
- CPU-burn script must be time-bounded.
- Collect only system metrics; no application secrets.

---

## 16. Documentation deliverables

| Doc | Content |
| --- | --- |
| `README.md` | Quick start, ports, credentials, reset |
| `docs/ARCHITECTURE.md` | Component diagram and data flow |
| `docs/DEMO_SCRIPT.md` | Presenter talk track + commands |
| `docs/RUNBOOKS.md` | Trainee triage for each alert |
| `docs/CONFIGURATION.md` | Thresholds, targets, retention |

---

## 17. Implementation phases

### Phase 0 — Spec & repo skeleton
- This PRD accepted
- Repo layout, Compose stub, empty dashboards folder

### Phase 1 — MVP monitoring plane
- Prometheus + Grafana + Alertmanager via Compose
- node_exporter on ≥1 Linux target
- Fleet + host dashboards provisioned
- Core alert rules + webhook receiver (e.g. Discord/Slack webhook or local webhook catcher)

### Phase 2 — Demo reliability
- Chaos/load/reset scripts with safety caps
- Documented 10-minute demo script
- Self-monitoring and health checks

### Phase 3 — Polish (optional)
- Log panel (Loki or file-tail sidecar)
- Multi-host lab inventory file
- Offline image bundle
- Simple status page for non-technical audience

---

## 18. Acceptance criteria (MVP)

MVP is **done** when all of the following are true:

1. `docker compose up -d` brings up Prometheus, Alertmanager, and Grafana with provisioned dashboards.
2. At least one Linux host with node_exporter appears as **Up** and populates fleet + host dashboards.
3. From the UI alone (no SSH), an operator can see real-time **CPU**, **memory**, **network usage**, and **port usage** for that host.
4. HighCPU, HighMemory, DiskAlmostFull, and HostDown alerts can each be demonstrated end-to-end.
5. Demo scripts exist for CPU burn, capped disk fill, service stop/start, and full reset.
6. README enables a new engineer to complete the §13 demo script without undocumented steps.
7. Default bind/credentials guidance prevents accidental public exposure.

---

## 19. Open questions

| # | Question | Impact | Proposed default |
| --- | --- | --- | --- |
| Q1 | Fixed stack (Prometheus/Grafana) vs allow Zabbix/Netdata? | Architecture | Prometheus + Grafana + Alertmanager |
| Q2 | How many Linux targets in the “official” demo? | Sizing, inventory | 3 (web, app, db roles) |
| Q3 | Alert notification channel for live demos? | Alertmanager config | Webhook to a demo catcher + optional email |
| Q4 | Include logs (Loki) in MVP? | Scope/time | No — Phase 3 |
| Q5 | Bare-metal only, containers as targets, or both? | Agent docs | Both; prioritize bare-metal/VM Linux |
| Q6 | Offline / air-gapped demo required? | Packaging | Not MVP; document image save/load |
| Q7 | Auth model for Grafana? | Security | Shared demo login for MVP; document path to group/SSO later for Infra + App Dev |
| Q8 | Branding / custom UI skin needed? | Frontend work | Stock Grafana with named demo dashboards |
| Q9 | Port usage depth: listening table only vs full `ss`-like detail vs critical-port probes? | Exporters, privacy | Listen + connection-state summary + critical-port probes |
| Q10 | Which critical ports are in the default demo inventory? | Alert/probe config | 22, 80, 443, plus one demo app port |
| Q11 | Separate dashboard folders/permissions for Infra vs App Dev, or one shared set? | UX, access | One shared demo folder; role tags (`role=web\|app\|db`) for filtering |
| Q12 | Do L1 users get alert notifications directly, or only ticket + UI? | Alert routing | UI + webhook stub for MVP; map to real channels later |

---

## 20. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Demo laptop too weak | Publish minimum specs; allow remote lab Compose host |
| Alerts too slow for stage | Shorten `for:` and scrape interval in `demo` profile |
| Disk fill escapes safety | Hard path allowlist + max bytes + dry-run flag |
| Network blocked between Prometheus and exporters | Preflight connectivity check script |
| Dashboard drift | Provision dashboards from git only |

---

## 21. Glossary

| Term | Meaning |
| --- | --- |
| **Monitoring plane** | Prometheus, Alertmanager, Grafana (and add-ons) |
| **Target** | Linux host being scraped |
| **Exporter** | Process exposing metrics (node_exporter) |
| **Scrape** | Prometheus pull of `/metrics` |
| **Silence** | Temporary suppression of alerts during demos |

---

## 22. Revision history

| Version | Date | Author | Notes |
| --- | --- | --- | --- |
| 0.1 | 2026-11-24 | Draft | Initial PRD for Demo Monitoring Infrastructure (Linux servers) |
| 0.2 | 2026-11-24 | Draft | Problem centered on SSH-for-metrics pain; port usage elevated to MVP Must |
| 0.3 | 2026-11-24 | Draft | Users defined as internal L1/L2/L3 across Infra and App Dev; escalation UX requirements added |

---

## Appendix A — Suggested repository layout

```text
.
├── PRD.md
├── README.md
├── docker-compose.yml
├── prometheus/
│   ├── prometheus.yml
│   └── rules/
│       └── linux-hosts.yml
├── alertmanager/
│   └── alertmanager.yml
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   └── dashboards/
│   └── dashboards/
│       ├── fleet-overview.json
│       └── host-detail.json
├── demo-scripts/
│   ├── cpu-burn.sh
│   ├── disk-fill.sh
│   ├── service-toggle.sh
│   └── reset.sh
└── docs/
    ├── ARCHITECTURE.md
    ├── DEMO_SCRIPT.md
    ├── RUNBOOKS.md
    └── CONFIGURATION.md
```

## Appendix B — Sample presenter talking points

- “Today people SSH and run `top`, `free`, `ss`. That doesn’t scale.”
- “We instrument once; after that, CPU, memory, network, and ports are on the dashboard — no login to look.”
- “One overview answers: is the fleet healthy?”
- “Alerts are threshold + duration so brief spikes don’t page you.”
- “Here’s a controlled failure; watch the signal path from host → Prometheus → Alertmanager → dashboard.”
- “Reset returns us to a clean demo in under five minutes.”
