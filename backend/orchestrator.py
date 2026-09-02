from models import Payment
from detection import detect_payment_issue
from evidence import build_payment_evidence
from mock_ai import mock_ai_diagnosis
from priority import calculate_recovery_priority
from policy import evaluate_policy
from recovery import execute_recovery_action
from audit import add_audit_event


def process_payment(payment: Payment):

    audit_history = []

    # ------------------------------------------------
    # 1. DETECTION
    # ------------------------------------------------

    detection = detect_payment_issue(payment)

    add_audit_event(
        audit_history,
        "DETECTION",
        detection["message"],
        {
            "stuck_at": detection["stuck_at"]
        }
    )

    # ------------------------------------------------
    # 2. EVIDENCE
    # ------------------------------------------------

    evidence = build_payment_evidence(payment)

    add_audit_event(
        audit_history,
        "EVIDENCE",
        "Payment evidence collected.",
        {
            "payment_id": payment.payment_id
        }
    )

    # ------------------------------------------------
    # 3. AI DIAGNOSIS
    # ------------------------------------------------

    diagnosis = mock_ai_diagnosis(evidence)

    add_audit_event(
        audit_history,
        "DIAGNOSIS",
        diagnosis["reason"],
        {
            "root_cause": diagnosis["root_cause"],
            "confidence": diagnosis["confidence"]
        }
    )

    # ------------------------------------------------
    # 4. PRIORITY
    # ------------------------------------------------

    priority = calculate_recovery_priority(
        amount=payment.amount,
        severity=diagnosis["severity"],
        recovery_likelihood=0.85,
        age_hours=12
    )

    add_audit_event(
        audit_history,
        "PRIORITY",
        "Recovery priority calculated.",
        {
            "priority": priority["priority"],
            "priority_score": priority["priority_score"]
        }
    )

    # ------------------------------------------------
    # 5. POLICY
    # ------------------------------------------------

    policy = evaluate_policy(
        recommended_action=diagnosis["recommended_action"],
        confidence=diagnosis["confidence"],
        recovery_attempts=payment.recovery_attempts,
        max_attempts=payment.max_attempts,
        payment_recovered=False,
        stopping_rule_triggered=payment.stopping_rule_triggered
    )

    add_audit_event(
        audit_history,
        "POLICY",
        policy["reason"],
        {
            "action": policy["action"],
            "allowed": policy["allowed"],
            "approval_required": policy["approval_required"]
        }
    )

    # ------------------------------------------------
    # 6. RECOVERY
    # ------------------------------------------------

    recovery = execute_recovery_action(
        payment,
        policy
    )

    add_audit_event(
        audit_history,
        "RECOVERY",
        recovery["message"],
        {
            "action": recovery["action"],
            "status": recovery["status"]
        }
    )

    # ------------------------------------------------
    # 7. FINAL RESULT
    # ------------------------------------------------

    return {
        "payment_id": payment.payment_id,
        "amount": payment.amount,

        "detection": detection,

        "evidence": evidence,

        "diagnosis": diagnosis,

        "priority": priority,

        "policy": policy,

        "recovery": recovery,

        "audit_history": audit_history
    }