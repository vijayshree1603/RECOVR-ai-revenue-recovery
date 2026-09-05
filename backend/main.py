"""RECOVR's deterministic, demo-safe revenue recovery API."""
from copy import deepcopy
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from data.payments import payments as seed_payments

payments = deepcopy(seed_payments)
initial_payments = deepcopy(seed_payments)

app = FastAPI(title="RECOVR API", description="Demo-safe payment revenue recovery", version="2.1.0")
app.add_middleware(CORSMiddleware, allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+", allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

STAGES = {"Settlement mismatch": "SETTLEMENT", "Settlement delay": "SETTLEMENT", "Bank confirmation delay": "BANK", "Checkout abandonment": "CHECKOUT", "Subscription payment failure": "SUBSCRIPTION"}
RECOMMENDATIONS = {"Settlement mismatch": "ESCALATE", "Settlement delay": "RETRY", "Bank confirmation delay": "MONITOR", "Checkout abandonment": "RETRY", "Subscription payment failure": "RETRY"}
PLAYBOOKS = {
    "Settlement mismatch": {"name": "Settlement reconciliation", "action": "Escalate to settlement operations", "eta": "30–60 min", "automation": "Guided escalation", "steps": ["Match payment and settlement records", "Create reconciliation case", "Track merchant credit"]},
    "Settlement delay": {"name": "Automated settlement retry", "action": "Retry settlement and verify credit", "eta": "5–12 min", "automation": "Fully automated", "steps": ["Validate settlement state", "Submit safe retry", "Verify merchant credit"]},
    "Bank confirmation delay": {"name": "Bank confirmation watch", "action": "Monitor bank confirmation", "eta": "10–20 min", "automation": "Automated monitoring", "steps": ["Watch bank acknowledgement", "Update payment state", "Trigger recovery when confirmed"]},
    "Checkout abandonment": {"name": "Checkout recovery", "action": "Start safe recovery workflow", "eta": "2–8 min", "automation": "Fully automated", "steps": ["Confirm abandoned session", "Start recovery", "Verify payment completion"]},
    "Subscription payment failure": {"name": "Smart subscription retry", "action": "Retry recurring payment", "eta": "5–15 min", "automation": "Fully automated", "steps": ["Validate mandate state", "Execute smart retry", "Confirm successful collection"]},
}
STAGE_WEIGHT = {"SETTLEMENT": 15, "SUBSCRIPTION": 13, "BANK": 10, "CHECKOUT": 6}
audit_events: list[dict[str, Any]] = []

class MessageResponse(BaseModel):
    message: str
    payment: dict[str, Any] | None = None

class PaymentListResponse(BaseModel):
    payments: list[dict[str, Any]]

class PaymentResponse(BaseModel):
    payment: dict[str, Any]

class SimulationRequest(BaseModel):
    event_type: str

class ApprovalRequest(BaseModel):
    approved: bool = True

def payment_stage(payment: dict[str, Any]) -> str:
    return STAGES.get(payment.get("failure_reason"), "COMPLETED")

def detect_issue(payment: dict[str, Any]) -> dict[str, str]:
    return {"stuck_at": payment_stage(payment), "issue": payment.get("failure_reason", "No issue detected")}

def diagnose_payment(payment: dict[str, Any]) -> dict[str, Any]:
    """Deterministic diagnosis contract; replaceable by an AI provider later."""
    return {"root_cause": payment.get("root_cause"), "confidence": payment.get("diagnosis_confidence"), "recommended_action": RECOMMENDATIONS.get(payment.get("failure_reason"), "MONITOR"), "explanation": payment.get("what_happened")}

def check_recovery_policy(payment: dict[str, Any]) -> dict[str, Any]:
    diagnosis = diagnose_payment(payment)
    if payment["status"] == "RECOVERED": return {"allowed": False, "reason": "Payment is already recovered."}
    if payment["recovery_attempts"] >= payment["max_attempts"]: return {"allowed": False, "reason": "Maximum recovery attempts reached."}
    if not payment["policy_allowed"]: return {"allowed": False, "reason": "Recovery is not permitted by policy."}
    if payment.get("approval_required") and not payment.get("merchant_approved"):
        return {"allowed": False, "reason": "Merchant approval is required before this high-value recovery."}
    return {"allowed": True, "action": diagnosis["recommended_action"], "reason": "Recovery permitted by deterministic policy."}

def add_audit(payment_id: str, event_type: str, description: str, event_status: str = "COMPLETE") -> None:
    audit_events.insert(0, {"id": len(audit_events) + 1, "timestamp": datetime.now().strftime("%H:%M:%S"), "payment_id": payment_id, "event": event_type, "description": description, "status": event_status})

def recovery_status(payment: dict[str, Any]) -> str:
    if payment["status"] == "RECOVERED": return "RECOVERED"
    if payment.get("escalation_created"): return "ESCALATED"
    if payment["status"] == "RECOVERING": return "RECOVERY_IN_PROGRESS"
    return "MONITORING"

def priority(payment: dict[str, Any]) -> dict[str, Any]:
    if payment["status"] == "RECOVERED": return {"score": 0, "label": "RESOLVED", "reasons": ["Payment already recovered"]}
    stage = payment_stage(payment)
    confidence = round((payment.get("diagnosis_confidence") or 0) * 60)
    revenue_impact = round(payment["amount"] / 7500 * 25)
    active_bonus = 5 if payment["status"] == "RECOVERING" else 0
    score = min(100, confidence + revenue_impact + STAGE_WEIGHT.get(stage, 0) + active_bonus)
    label = "CRITICAL" if score >= 82 else "HIGH" if score >= 68 else "MEDIUM"
    return {"score": score, "label": label, "reasons": [f"{int((payment.get('diagnosis_confidence') or 0) * 100)}% diagnosis confidence", f"{title_case(stage)} lifecycle exposure", f"{title_case(payment['payment_method'])} {payment['amount']:,.0f} revenue impact"]}

def serialize(payment: dict[str, Any]) -> dict[str, Any]:
    result = dict(payment)
    result["stuck_at"] = payment_stage(payment)
    result["recovery_status"] = recovery_status(payment)
    result["diagnosis"] = diagnose_payment(payment)
    priority_result = priority(payment)
    result["priority_score"] = priority_result["score"]
    result["priority_label"] = priority_result["label"]
    result["priority_reasons"] = priority_result["reasons"]
    result["playbook"] = PLAYBOOKS.get(payment.get("failure_reason"), {})
    playbook = result["playbook"]
    is_automatable = payment.get("policy_allowed") and payment.get("failure_reason") != "Settlement mismatch"
    result["impact_comparison"] = {
        "without_recovr": f"{payment['amount']:,.0f} remains exposed at {title_case(payment_stage(payment))}",
        "with_recovr": "Merchant credit verified" if payment["status"] == "RECOVERED" else playbook.get("action", "RECOVR monitors the next safe action"),
        "recoverable_amount": payment["amount"] if is_automatable else 0,
        "expected_resolution": playbook.get("eta", "Under review"),
        "automation": playbook.get("automation", "Guided review"),
    }
    journey = payment.get("journey", {})
    result["evidence"] = [
        {"signal": "Payment received", "value": "Confirmed" if journey.get("razorpay_received") else "Pending", "state": "confirmed" if journey.get("razorpay_received") else "pending"},
        {"signal": "Bank confirmation", "value": "Confirmed" if journey.get("bank_confirmed") else "Awaiting bank", "state": "confirmed" if journey.get("bank_confirmed") else "pending"},
        {"signal": "Settlement record", "value": "Mismatch detected" if payment.get("failure_reason") == "Settlement mismatch" else "Pending review" if not journey.get("settlement_completed") else "Confirmed", "state": "risk" if payment.get("failure_reason") == "Settlement mismatch" else "pending" if not journey.get("settlement_completed") else "confirmed"},
    ]
    result["merchant_approved"] = payment.get("merchant_approved", False)
    result["decision_trace"] = [
        {"step": "Detection", "detail": f"Stuck at {payment_stage(payment)}"},
        {"step": "Diagnosis", "detail": f"{payment.get('failure_reason')} · {result['priority_score']}% confidence"},
        {"step": "Policy", "detail": "Recovery permitted" if payment.get("policy_allowed") else "Merchant review required"},
        {"step": "Action", "detail": title_case(recovery_status(payment))},
    ]
    return result

def title_case(value: str) -> str:
    return value.replace("_", " ").title()

def get_payment_or_404(payment_id: str) -> dict[str, Any]:
    payment = next((item for item in payments if item["payment_id"] == payment_id), None)
    if not payment: raise HTTPException(status_code=404, detail="Payment not found")
    return payment

def execute_recovery(payment: dict[str, Any]) -> None:
    policy = check_recovery_policy(payment)
    if not policy["allowed"]: raise HTTPException(status_code=400, detail=policy["reason"])
    if policy["action"] == "ESCALATE":
        payment["escalation_created"] = True
        payment["recovery_action"] = "ESCALATE_SETTLEMENT"
        payment["what_recovr_is_doing"] = "RECOVR escalated the settlement mismatch for investigation."
        payment["next_step"] = "Settlement team investigation"
        add_audit(payment["payment_id"], "ESCALATION", "Settlement case escalated for investigation", "ESCALATED")
        return
    payment["status"] = "RECOVERING"
    payment["recovery_attempts"] += 1
    payment["recovery_action"] = "SIMULATED_AUTOMATED_RECOVERY"
    payment["what_recovr_is_doing"] = "RECOVR has started a simulated automated recovery workflow."
    payment["next_step"] = "Verify recovery outcome"
    add_audit(payment["payment_id"], "RECOVERY_STARTED", "Simulated automated recovery started", "IN_PROGRESS")

def approve_recovery(payment: dict[str, Any], approved: bool) -> None:
    if payment["status"] == "RECOVERED": raise HTTPException(status_code=400, detail="Payment is already recovered")
    if not payment.get("approval_required"): raise HTTPException(status_code=400, detail="This payment does not need merchant approval")
    if not approved: raise HTTPException(status_code=400, detail="Merchant approval was declined")
    payment["merchant_approved"] = True
    payment["what_recovr_is_doing"] = "Merchant approval received. RECOVR is ready to start the safe recovery playbook."
    payment["next_step"] = "Start automated recovery"
    add_audit(payment["payment_id"], "MERCHANT_APPROVAL", "Merchant approved high-value automated recovery", "APPROVED")

def verify_recovery(payment: dict[str, Any]) -> None:
    if payment["status"] == "RECOVERED": raise HTTPException(status_code=400, detail="Payment is already recovered")
    if payment["status"] != "RECOVERING": raise HTTPException(status_code=400, detail="Start recovery before verification")
    payment["status"] = "RECOVERED"
    payment["recovered_amount"] = payment["amount"]
    payment["recovery_action"] = "SIMULATED_RECOVERY_COMPLETED"
    payment["stopping_rule_triggered"] = True
    payment["journey"]["settlement_completed"] = True
    payment["journey"]["merchant_bank_credited"] = True
    payment["what_recovr_is_doing"] = "RECOVR verified the simulated recovery and confirmed merchant credit."
    payment["next_step"] = "No further action required"
    add_audit(payment["payment_id"], "RECOVERY_COMPLETED", "Simulated recovery completed", "RECOVERED")
    add_audit(payment["payment_id"], "VERIFICATION", "Merchant credit verified", "RECOVERED")

def simulate_event(payment: dict[str, Any], event_type: str) -> str:
    """Demo-only event intake. It models real webhook updates without external systems."""
    event_type = event_type.upper()
    if payment["status"] == "RECOVERED": raise HTTPException(status_code=400, detail="Payment is already recovered")
    if event_type == "BANK_CONFIRMED":
        payment["journey"]["bank_confirmed"] = True
        payment["journey"]["razorpay_received"] = True
        payment["status"] = "RECOVERING"
        payment["recovery_action"] = "EVENT_MONITORING"
        payment["what_recovr_is_doing"] = "RECOVR received a simulated bank confirmation and moved the case into active recovery."
        payment["next_step"] = "Await settlement confirmation"
        add_audit(payment["payment_id"], "BANK_CONFIRMATION", "Simulated bank confirmation webhook received", "IN_PROGRESS")
        return "Simulated bank confirmation received. RECOVR moved the case into active recovery."
    if event_type in {"SETTLEMENT_COMPLETED", "RETRY_SUCCEEDED"}:
        payment["status"] = "RECOVERING"
        payment["journey"]["bank_confirmed"] = True
        payment["journey"]["razorpay_received"] = True
        payment["journey"]["settlement_completed"] = True
        payment["journey"]["merchant_bank_credited"] = True
        verify_recovery(payment)
        add_audit(payment["payment_id"], "SIMULATED_WEBHOOK", f"Simulated {event_type.lower().replace('_', ' ')} received", "RECOVERED")
        return "Simulated payment event completed recovery and refreshed every RECOVR view."
    raise HTTPException(status_code=400, detail="Unsupported simulation event")

@app.on_event("startup")
def seed_audit() -> None:
    if audit_events: return
    for payment in payments:
        detection, diagnosis, policy = detect_issue(payment), diagnose_payment(payment), check_recovery_policy(payment)
        add_audit(payment["payment_id"], "DETECTION", f"Payment stuck at {detection['stuck_at']}")
        add_audit(payment["payment_id"], "DIAGNOSIS", f"{detection['issue']} detected · {int(diagnosis['confidence'] * 100)}% confidence")
        add_audit(payment["payment_id"], "POLICY", "Recovery permitted" if policy["allowed"] else policy["reason"])

@app.get("/health")
def health() -> dict[str, str]: return {"status": "healthy", "mode": "simulated"}

@app.get("/payments", response_model=PaymentListResponse)
def list_payments() -> dict[str, list[dict[str, Any]]]: return {"payments": [serialize(payment) for payment in payments]}

@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: str) -> dict[str, dict[str, Any]]: return {"payment": serialize(get_payment_or_404(payment_id))}

@app.post("/payments/{payment_id}/recover", response_model=MessageResponse)
def recover(payment_id: str) -> dict[str, Any]:
    payment = get_payment_or_404(payment_id); execute_recovery(payment)
    return {"message": "Simulated recovery action initiated", "payment": serialize(payment)}

@app.post("/payments/{payment_id}/approve", response_model=MessageResponse)
def approve(payment_id: str, payload: ApprovalRequest) -> dict[str, Any]:
    payment = get_payment_or_404(payment_id)
    approve_recovery(payment, payload.approved)
    return {"message": "Merchant approval recorded. Recovery is ready to begin.", "payment": serialize(payment)}

@app.post("/payments/{payment_id}/verify", response_model=MessageResponse)
def verify(payment_id: str) -> dict[str, Any]:
    payment = get_payment_or_404(payment_id); verify_recovery(payment)
    return {"message": "Simulated recovery verified", "payment": serialize(payment)}

@app.post("/payments/{payment_id}/simulate-event", response_model=MessageResponse)
def simulate_payment_event(payment_id: str, payload: SimulationRequest) -> dict[str, Any]:
    payment = get_payment_or_404(payment_id)
    message = simulate_event(payment, payload.event_type)
    return {"message": message, "payment": serialize(payment)}

@app.post("/demo/reset")
def reset_demo() -> dict[str, str]:
    """Restore the deterministic six-payment demo baseline for another presentation."""
    payments[:] = deepcopy(initial_payments)
    audit_events.clear()
    seed_audit()
    return {"message": "Demo reset to the original six-payment baseline."}

@app.get("/audit")
def audit() -> dict[str, list[dict[str, Any]]]: return {"events": audit_events}

@app.get("/analytics")
def analytics() -> dict[str, Any]:
    total_revenue = sum(payment["amount"] for payment in payments)
    revenue_at_risk = sum(payment["amount"] for payment in payments if payment["status"] == "AT_RISK")
    revenue_recovering = sum(payment["amount"] for payment in payments if payment["status"] == "RECOVERING")
    recovered_revenue = sum(payment["recovered_amount"] for payment in payments)
    outcomes = [{"label": label, "value": sum(1 for payment in payments if payment["status"] == key)} for key, label in [("AT_RISK", "At risk"), ("RECOVERING", "Recovering"), ("RECOVERED", "Recovered")]]
    stages = [{"label": stage.title(), "value": sum(1 for payment in payments if payment_stage(payment) == stage)} for stage in ["CHECKOUT", "BANK", "SETTLEMENT", "SUBSCRIPTION"]]
    priority_queue = sorted([serialize(payment) for payment in payments if payment["status"] != "RECOVERED"], key=lambda item: item["priority_score"], reverse=True)
    baseline_risk = sum(payment["amount"] for payment in initial_payments if payment["status"] == "AT_RISK")
    return {"total_payments": len(payments), "total_revenue": total_revenue, "revenue_at_risk": revenue_at_risk, "baseline_revenue_at_risk": baseline_risk, "revenue_recovering": revenue_recovering, "recovered_revenue": recovered_revenue, "active_recoveries": sum(1 for payment in payments if payment["status"] == "RECOVERING"), "recovery_rate": round(recovered_revenue / total_revenue * 100, 1), "risk_rate": round(revenue_at_risk / total_revenue * 100, 1), "status_distribution": outcomes, "recovery_outcomes": outcomes, "stage_distribution": stages, "priority_queue": priority_queue}
