from typing import Dict


def evaluate_policy(
    recommended_action: str,
    confidence: float,
    recovery_attempts: int,
    max_attempts: int,
    payment_recovered: bool,
    stopping_rule_triggered: bool
) -> Dict:

    # Already recovered — no further action needed
    if payment_recovered:
        return {
            "allowed": False,
            "action": "NO_ACTION",
            "reason": "Payment has already been recovered.",
            "approval_required": False
        }

    # Safety stop has already been triggered
    if stopping_rule_triggered:
        return {
            "allowed": False,
            "action": "HUMAN_REVIEW",
            "reason": "A stopping rule has been triggered.",
            "approval_required": True
        }

    # Low-confidence AI recommendations should not
    # automatically trigger financial actions.
    if confidence < 0.70:
        return {
            "allowed": False,
            "action": "HUMAN_REVIEW",
            "reason": "AI confidence is too low for automated action.",
            "approval_required": True
        }

    # RETRY policy
    if recommended_action == "RETRY":

        if recovery_attempts >= max_attempts:
            return {
                "allowed": False,
                "action": "HUMAN_REVIEW",
                "reason": "Maximum recovery attempts have been reached.",
                "approval_required": True
            }

        return {
            "allowed": True,
            "action": "RETRY",
            "reason": "Retry is within the allowed recovery policy.",
            "approval_required": False
        }

    # ESCALATE policy
    if recommended_action == "ESCALATE":

        return {
            "allowed": True,
            "action": "ESCALATE",
            "reason": "Escalation is allowed for this unresolved payment.",
            "approval_required": False
        }

    # MONITOR policy
    if recommended_action == "MONITOR":

        return {
            "allowed": True,
            "action": "MONITOR",
            "reason": "The payment should be monitored rather than actively recovered.",
            "approval_required": False
        }

    # Unknown or unsupported recommendation
    return {
        "allowed": False,
        "action": "HUMAN_REVIEW",
        "reason": "The recommended action is not supported by the current policy.",
        "approval_required": True
    }