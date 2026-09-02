from models import Payment


def diagnose_payment(payment: Payment, detection_result: dict):

    stuck_at = detection_result["stuck_at"]

    if stuck_at == "PAYMENT_START":
        return {
            "root_cause": "PAYMENT_NOT_STARTED",
            "confidence": 0.98,
            "explanation": (
                "The payment process has not started successfully."
            )
        }

    if stuck_at == "BANK":
        return {
            "root_cause": "BANK_CONFIRMATION_PENDING",
            "confidence": 0.95,
            "explanation": (
                "The payment is waiting for confirmation from the customer's bank."
            )
        }

    if stuck_at == "RAZORPAY":
        return {
            "root_cause": "PAYMENT_PROCESSING_DELAY",
            "confidence": 0.92,
            "explanation": (
                "The bank confirmed the payment, but the payment has not "
                "yet been received by the payment processor."
            )
        }

    if stuck_at == "SETTLEMENT":

        if payment.failure_reason == "Settlement mismatch":
            return {
                "root_cause": "SETTLEMENT_MISMATCH",
                "confidence": 0.94,
                "explanation": (
                    "The payment was successfully processed, but the "
                    "settlement record does not match the payment record."
                )
            }

        return {
            "root_cause": "SETTLEMENT_PENDING",
            "confidence": 0.88,
            "explanation": (
                "The payment was successfully processed, but settlement "
                "has not yet been completed."
            )
        }

    if stuck_at == "MERCHANT_BANK":
        return {
            "root_cause": "MERCHANT_CREDIT_DELAY",
            "confidence": 0.90,
            "explanation": (
                "The payment has been settled, but the amount has not "
                "yet reached the merchant bank account."
            )
        }

    return {
        "root_cause": "UNKNOWN",
        "confidence": 0.50,
        "explanation": (
            "RECOVR could not determine the exact reason for the issue yet."
        )
    }