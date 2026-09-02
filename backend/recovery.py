from typing import Dict


def execute_recovery_action(
    payment,
    policy_result: Dict
) -> Dict:

    action = policy_result["action"]

    # Policy blocked the action
    if not policy_result["allowed"]:
        return {
            "executed": False,
            "action": action,
            "status": "BLOCKED",
            "message": policy_result["reason"],
            "recovered_amount": 0.0
        }

    # Stop if maximum recovery attempts have been reached
    if payment.recovery_attempts >= payment.max_attempts:
        payment.stopping_rule_triggered = True

        return {
            "executed": False,
            "action": "HUMAN_REVIEW",
            "status": "STOPPED",
            "message": (
                "RECOVR stopped automatic recovery because "
                "the maximum number of attempts has been reached."
            ),
            "recovered_amount": 0.0
        }

    # Retry
    if action == "RETRY":

        payment.recovery_attempts += 1

        # Trigger stopping rule after the final allowed attempt
        if payment.recovery_attempts >= payment.max_attempts:
            payment.stopping_rule_triggered = True

        return {
            "executed": True,
            "action": "RETRY",
            "status": "ATTEMPTED",
            "message": (
                "RECOVR attempted the recovery process."
            ),
            "recovered_amount": 0.0,
            "recovery_attempts": payment.recovery_attempts,
            "stopping_rule_triggered": payment.stopping_rule_triggered
        }

    # Escalation
    if action == "ESCALATE":

        # Prevent duplicate escalation
        if getattr(payment, "escalation_created", False):
            return {
                "executed": False,
                "action": "ESCALATE",
                "status": "ALREADY_ESCALATED",
                "message": (
                    "An escalation already exists for this payment."
                ),
                "recovered_amount": 0.0
            }

        payment.escalation_created = True

        return {
            "executed": True,
            "action": "ESCALATE",
            "status": "ESCALATED",
            "message": (
                "RECOVR escalated the payment for further investigation."
            ),
            "recovered_amount": 0.0
        }

    # Monitoring
    if action == "MONITOR":

        return {
            "executed": True,
            "action": "MONITOR",
            "status": "MONITORING",
            "message": (
                "RECOVR will continue monitoring the payment."
            ),
            "recovered_amount": 0.0
        }

    # Human review
    if action == "HUMAN_REVIEW":

        return {
            "executed": False,
            "action": "HUMAN_REVIEW",
            "status": "WAITING_FOR_REVIEW",
            "message": (
                "This payment requires human review before further action."
            ),
            "recovered_amount": 0.0
        }

    # No action
    if action == "NO_ACTION":

        return {
            "executed": False,
            "action": "NO_ACTION",
            "status": "NO_ACTION",
            "message": (
                "No recovery action is required."
            ),
            "recovered_amount": 0.0
        }

    return {
        "executed": False,
        "action": "UNKNOWN",
        "status": "ERROR",
        "message": "Unknown recovery action.",
        "recovered_amount": 0.0
    }