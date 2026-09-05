# RECOVR — AI Revenue Recovery Platform

> Detect stuck payments, explain the root cause, choose a safe recovery playbook, and show a merchant exactly what happened.

RECOVR is a merchant-side revenue-operations platform built for the Razorpay Buildathon. It turns payment exceptions into an explainable workflow: detection, diagnosis, policy decision, recovery, verification, audit, and analytics.

## Why RECOVR

Merchants often discover payment failures too late, then manually reconcile bank, gateway, and settlement information. RECOVR makes that process proactive and understandable.

- Identifies where a payment is stuck in its lifecycle.
- Explains the diagnosis with deterministic evidence and confidence.
- Prioritizes the cases with the highest revenue impact.
- Selects safe, issue-specific recovery playbooks.
- Requires merchant approval for selected high-value actions.
- Keeps every decision and event visible in an audit trail.

## Product flow

```text
Payment event
  → Detection
  → Diagnosis + evidence
  → Policy guardrail
  → Recovery / escalation
  → Verification
  → Audit log + updated analytics
```

## Key capabilities

### Smart priority queue

RECOVR ranks unresolved cases by a deterministic score based on diagnosis confidence, payment amount, lifecycle exposure, and recovery state. The queue labels cases as `CRITICAL`, `HIGH`, `MEDIUM`, or `RESOLVED`.

### Explainable decision trace

Every case displays the exact path behind the recommendation:

1. Detection — stuck lifecycle stage
2. Diagnosis — root cause and confidence
3. Policy — allowed action or guardrail
4. Action — monitoring, recovery, or escalation

### Recovery playbooks

Each issue maps to a clear operational playbook with automation level, expected resolution time, and execution steps.

| Issue | Playbook | Safe action |
|---|---|---|
| Settlement mismatch | Settlement reconciliation | Escalate for investigation |
| Settlement delay | Automated settlement retry | Retry and verify credit |
| Bank confirmation delay | Bank confirmation watch | Monitor confirmation |
| Checkout abandonment | Checkout recovery | Start recovery workflow |
| Subscription payment failure | Smart subscription retry | Retry recurring payment |

### Safe event simulator

The app simulates bank and settlement webhook events without contacting any payment provider. Events update the same backend payment state used by the dashboard, analytics, payment drawer, and audit log.

### Merchant approval guardrail

Karthik’s ₹7,500 checkout recovery requires merchant approval before the automatic recovery can start. This demonstrates bounded automation for financially sensitive actions.

### Interactive analytics

- Click an outcome segment (`At risk`, `Recovering`, or `Recovered`) to inspect a matching payment.
- Click a lifecycle leak segment (`Checkout`, `Bank`, `Settlement`, or `Subscription`) to open an affected payment.
- Compare original revenue at risk against revenue currently protected by RECOVR.

## Demo data

The baseline dataset contains exactly six payments.

| Payment | Customer | Amount | Method | Status | Stuck at | Recovery state |
|---|---|---:|---|---|---|---|
| PAY_1001 | Rahul | ₹5,000 | UPI | At risk | Settlement | Escalated |
| PAY_1002 | Priya | ₹2,500 | Card | At risk | Bank | Monitoring |
| PAY_1003 | Arjun | ₹3,200 | UPI | Recovering | Settlement | Recovery in progress |
| PAY_1004 | Sneha | ₹1,800 | Card | Recovered | Settlement | Recovered |
| PAY_1005 | Karthik | ₹7,500 | UPI | At risk | Checkout | Approval required |
| PAY_1006 | Ananya | ₹4,500 | Card | Recovering | Subscription | Recovery in progress |

Baseline metrics: **₹24,500 monitored · ₹15,000 at risk · 2 active recoveries · ₹1,800 recovered**.

## Architecture

```text
React dashboard (Vite)
    │  HTTP / JSON
    ▼
FastAPI API
    ├── deterministic detection and diagnosis
    ├── policy / approval guardrails
    ├── demo-safe recovery engine
    ├── event simulator
    ├── in-memory audit ledger
    └── analytics + priority queue
```

### Stack

- **Frontend:** React, JSX, CSS, Vite
- **Backend:** Python, FastAPI, Pydantic
- **State:** In-memory demo state, resettable via API

## Run locally

### Backend

```powershell
cd backend
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

API runs at `http://127.0.0.1:8000`.

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

No additional runtime dependencies are required if `node_modules` and the backend virtual environment already exist.

## API reference

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | API readiness check |
| `GET` | `/payments` | List all payments with computed intelligence |
| `GET` | `/payments/{payment_id}` | View a single payment case |
| `POST` | `/payments/{payment_id}/recover` | Start safe simulated recovery or escalation |
| `POST` | `/payments/{payment_id}/approve` | Record merchant approval for a guarded recovery |
| `POST` | `/payments/{payment_id}/verify` | Verify and complete recovery |
| `POST` | `/payments/{payment_id}/simulate-event` | Simulate a payment webhook event |
| `GET` | `/analytics` | Live metrics, distributions, and priority queue |
| `GET` | `/audit` | Timestamped RECOVR decision trail |
| `POST` | `/demo/reset` | Restore the original six-payment baseline |

### Example: simulate a bank confirmation

```powershell
Invoke-RestMethod -Method Post `
  -ContentType 'application/json' `
  -Body '{"event_type":"BANK_CONFIRMED"}' `
  http://127.0.0.1:8000/payments/PAY_1002/simulate-event
```

## Five-minute demo path

1. Click **LIVE DEMO → Open guide**.
2. Open Rahul’s case and explain Settlement mismatch, evidence, and the decision trace.
3. Open Karthik’s case; approve the safe recovery, start it, then simulate a payment event.
4. Open Analytics and click a lifecycle leak segment.
5. Finish in Audit Log and show the complete system trail.
6. Use **Reset demo data** before another presentation.

## Safety and limitations

RECOVR intentionally performs **no real financial transaction**. Recovery actions, approvals, and webhooks are deterministic demo simulations. The application keeps state in memory; restarting the FastAPI process restores the baseline demo data. A production version would replace the simulator with authenticated provider webhooks, durable storage, idempotency, role-based authorization, and real reconciliation services.

## Build verification

```powershell
cd frontend
npm run build
```

The frontend production build is verified as part of the project workflow.
