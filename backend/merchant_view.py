def create_merchant_view(result):

    diagnosis = result["diagnosis"]
    detection = result["detection"]
    recovery = result["recovery"]
    policy = result["policy"]

    stuck_at = detection["stuck_at"]

    stuck_at_labels = {
        "PAYMENT_START": "Payment initiation",
        "BANK": "Customer bank confirmation",
        "RAZORPAY": "Payment processing",
        "SETTLEMENT": "Settlement",
        "MERCHANT_BANK": "Merchant bank credit"
    }

    stuck_at_text = stuck_at_labels.get(
        stuck_at,
        stuck_at
    )

    if recovery["status"] == "ESCALATED":
        what_recovr_is_doing = (
            "RECOVR is investigating the issue and has "
            "escalated it for further resolution."
        )

        merchant_action = "No action required"

    elif recovery["status"] == "ATTEMPTED":
        what_recovr_is_doing = (
            "RECOVR has attempted an automated recovery."
        )

        merchant_action = "No action required"

    elif recovery["status"] == "MONITORING":
        what_recovr_is_doing = (
            "RECOVR is monitoring the payment for further changes."
        )

        merchant_action = "No action required"

    elif recovery["status"] in ["STOPPED", "WAITING_FOR_REVIEW"]:

        what_recovr_is_doing = (
            "RECOVR has stopped automatic recovery and "
            "requires human review."
        )

        merchant_action = "Review required"

    else:
        what_recovr_is_doing = (
            "RECOVR is monitoring the payment."
        )

        merchant_action = "No action required"

    return {
        "payment_id": result["payment_id"],
        "amount": result["amount"],

        "status": "Attention required",

        "where_payment_is_stuck": stuck_at_text,

        "what_happened": diagnosis["reason"],

        "what_recovr_is_doing": what_recovr_is_doing,

        "merchant_action": merchant_action,

        "technical_details": {
            "root_cause": diagnosis["root_cause"],
            "confidence": diagnosis["confidence"],
            "severity": diagnosis["severity"],
            "policy_action": policy["action"],
            "recovery_status": recovery["status"]
        }
    }