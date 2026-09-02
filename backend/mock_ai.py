from typing import Dict


def mock_ai_diagnosis(evidence: Dict):

    stuck_at = evidence["detection"]["stuck_at"]
    failure_reason = evidence["failure"]["failure_reason"]

    if stuck_at == "PAYMENT_START":
        return {
            "root_cause": "PAYMENT_NOT_STARTED",
            "confidence": 0.98,
            "severity": "LOW",
            "reason": "The payment process did not start successfully.",
            "recommended_action": "NO_ACTION"
        }

    if stuck_at == "BANK":
        return {
            "root_cause": "BANK_CONFIRMATION_PENDING",
            "confidence": 0.95,
            "severity": "MEDIUM",
            "reason": "The payment is waiting for confirmation from the customer's bank.",
            "recommended_action": "MONITOR"
        }

    if stuck_at == "RAZORPAY":
        return {
            "root_cause": "PAYMENT_PROCESSING_DELAY",
            "confidence": 0.92,
            "severity": "MEDIUM",
            "reason": "The bank confirmed the payment, but the payment processor has not received the confirmation yet.",
            "recommended_action": "RETRY"
        }

    if stuck_at == "SETTLEMENT":

        if failure_reason == "Settlement mismatch":
            return {
                "root_cause": "SETTLEMENT_MISMATCH",
                "confidence": 0.94,
                "severity": "HIGH",
                "reason": "The payment was processed successfully, but the settlement information does not match the payment record.",
                "recommended_action": "ESCALATE"
            }

        return {
            "root_cause": "SETTLEMENT_PENDING",
            "confidence": 0.88,
            "severity": "MEDIUM",
            "reason": "The payment was processed successfully, but settlement has not been completed.",
            "recommended_action": "MONITOR"
        }

    if stuck_at == "MERCHANT_BANK":
        return {
            "root_cause": "MERCHANT_CREDIT_DELAY",
            "confidence": 0.90,
            "severity": "HIGH",
            "reason": "The payment has been settled, but the merchant bank account has not been credited yet.",
            "recommended_action": "ESCALATE"
        }

    return {
        "root_cause": "UNKNOWN",
        "confidence": 0.50,
        "severity": "UNKNOWN",
        "reason": "The available evidence is not sufficient to determine the exact cause.",
        "recommended_action": "HUMAN_REVIEW"
    }