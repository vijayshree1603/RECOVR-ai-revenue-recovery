payments = [
    {
        "payment_id": "PAY_1001",
        "order_id": "ORD_1001",
        "customer_name": "Rahul",
        "amount": 5000,
        "payment_method": "UPI",

        "status": "AT_RISK",
        "failure_reason": "Settlement mismatch",
        "root_cause": "Settlement processing failure",
        "diagnosis_confidence": 0.94,

        "journey": {
            "payment_started": True,
            "bank_confirmed": True,
            "razorpay_received": True,
            "settlement_completed": False,
            "merchant_bank_credited": False
        },

        "recovery_action": "ESCALATE_SETTLEMENT",
        "recovery_attempts": 1,
        "max_attempts": 3,
        "recovered_amount": 0.0,

        "policy_allowed": True,
        "approval_required": True,
        "stopping_rule_triggered": False,

        "what_happened": "The customer's payment was successfully processed, but the settlement has not been completed.",
        "what_recovr_is_doing": "RECOVR detected a settlement mismatch and escalated the payment for investigation.",
        "next_step": "Settlement team investigation",
        "merchant_action_required": False,

        "escalation_created": True
    },

    {
        "payment_id": "PAY_1002",
        "order_id": "ORD_1002",
        "customer_name": "Priya",
        "amount": 2500,
        "payment_method": "CARD",

        "status": "AT_RISK",
        "failure_reason": "Bank confirmation delay",
        "root_cause": "Delayed bank confirmation",
        "diagnosis_confidence": 0.89,

        "journey": {
            "payment_started": True,
            "bank_confirmed": False,
            "razorpay_received": False,
            "settlement_completed": False,
            "merchant_bank_credited": False
        },

        "recovery_action": "MONITOR_BANK_CONFIRMATION",
        "recovery_attempts": 0,
        "max_attempts": 3,
        "recovered_amount": 0.0,

        "policy_allowed": True,
        "approval_required": False,
        "stopping_rule_triggered": False,

        "what_happened": "The payment was initiated successfully, but confirmation from the customer's bank has not been received.",
        "what_recovr_is_doing": "RECOVR is monitoring the bank confirmation and will trigger recovery if the payment remains unresolved.",
        "next_step": "Continue monitoring bank confirmation",
        "merchant_action_required": False,

        "escalation_created": False
    },

    {
        "payment_id": "PAY_1003",
        "order_id": "ORD_1003",
        "customer_name": "Arjun",
        "amount": 3200,
        "payment_method": "UPI",

        "status": "RECOVERING",
        "failure_reason": "Settlement delay",
        "root_cause": "Delayed settlement processing",
        "diagnosis_confidence": 0.91,

        "journey": {
            "payment_started": True,
            "bank_confirmed": True,
            "razorpay_received": True,
            "settlement_completed": False,
            "merchant_bank_credited": False
        },

        "recovery_action": "RETRY_SETTLEMENT",
        "recovery_attempts": 1,
        "max_attempts": 3,
        "recovered_amount": 0.0,

        "policy_allowed": True,
        "approval_required": False,
        "stopping_rule_triggered": False,

        "what_happened": "The payment was received, but settlement to the merchant account was delayed.",
        "what_recovr_is_doing": "RECOVR has initiated an automated recovery workflow for the delayed settlement.",
        "next_step": "Retry settlement processing",
        "merchant_action_required": False,

        "escalation_created": False
    },

    {
        "payment_id": "PAY_1004",
        "order_id": "ORD_1004",
        "customer_name": "Sneha",
        "amount": 1800,
        "payment_method": "CARD",

        "status": "RECOVERED",
        "failure_reason": "Settlement mismatch",
        "root_cause": "Settlement processing failure",
        "diagnosis_confidence": 0.96,

        "journey": {
            "payment_started": True,
            "bank_confirmed": True,
            "razorpay_received": True,
            "settlement_completed": True,
            "merchant_bank_credited": True
        },

        "recovery_action": "SETTLEMENT_RETRY_SUCCESS",
        "recovery_attempts": 1,
        "max_attempts": 3,
        "recovered_amount": 1800.0,

        "policy_allowed": True,
        "approval_required": False,
        "stopping_rule_triggered": True,

        "what_happened": "The payment was successfully processed but initially failed to settle.",
        "what_recovr_is_doing": "RECOVR successfully completed the recovery process and confirmed the payment settlement.",
        "next_step": "No further action required",
        "merchant_action_required": False,

        "escalation_created": False
    },

    {
        "payment_id": "PAY_1005",
        "order_id": "ORD_1005",
        "customer_name": "Karthik",
        "amount": 7500,
        "payment_method": "UPI",

        "status": "AT_RISK",
        "failure_reason": "Checkout abandonment",
        "root_cause": "Incomplete checkout",
        "diagnosis_confidence": 0.87,

        "journey": {
            "payment_started": True,
            "bank_confirmed": False,
            "razorpay_received": False,
            "settlement_completed": False,
            "merchant_bank_credited": False
        },

        "recovery_action": "MONITOR_CHECKOUT",
        "recovery_attempts": 0,
        "max_attempts": 3,
        "recovered_amount": 0.0,

        "policy_allowed": True,
        "approval_required": True,
        "stopping_rule_triggered": False,

        "what_happened": "The customer started the checkout process but the payment was not completed.",
        "what_recovr_is_doing": "RECOVR detected an incomplete checkout and is monitoring the payment for further activity.",
        "next_step": "Continue monitoring checkout",
        "merchant_action_required": False,

        "escalation_created": False
    },

    {
        "payment_id": "PAY_1006",
        "order_id": "ORD_1006",
        "customer_name": "Ananya",
        "amount": 4500,
        "payment_method": "CARD",

        "status": "RECOVERING",
        "failure_reason": "Subscription payment failure",
        "root_cause": "Recurring payment failure",
        "diagnosis_confidence": 0.92,

        "journey": {
            "payment_started": True,
            "bank_confirmed": False,
            "razorpay_received": False,
            "settlement_completed": False,
            "merchant_bank_credited": False
        },

        "recovery_action": "RETRY_SUBSCRIPTION_PAYMENT",
        "recovery_attempts": 1,
        "max_attempts": 3,
        "recovered_amount": 0.0,

        "policy_allowed": True,
        "approval_required": False,
        "stopping_rule_triggered": False,

        "what_happened": "A recurring subscription payment could not be completed successfully.",
        "what_recovr_is_doing": "RECOVR is attempting to recover the failed recurring payment automatically.",
        "next_step": "Retry subscription payment",
        "merchant_action_required": False,

        "escalation_created": False
    }
]
