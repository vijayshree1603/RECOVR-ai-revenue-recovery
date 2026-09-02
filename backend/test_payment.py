from models import Payment, PaymentJourney


payment = Payment(
    payment_id="PAY_1001",
    order_id="ORD_5001",
    customer_name="Rahul",
    amount=5000.00,
    payment_method="UPI",

    status="AT_RISK",

    failure_reason="Settlement mismatch",
    root_cause="SETTLEMENT_MISMATCH",
    diagnosis_confidence=0.94,

    journey=PaymentJourney(
        payment_started=True,
        bank_confirmed=True,
        razorpay_received=True,
        settlement_completed=False,
        merchant_bank_credited=False
    ),

    recovery_action="ESCALATE",
    recovery_attempts=0,
    max_attempts=3,
    recovered_amount=0.0,

    policy_allowed=True,
    approval_required=False,
    stopping_rule_triggered=False,

    what_happened=(
        "The customer's payment was successfully processed, "
        "but the settlement has not been completed."
    ),

    what_recovr_is_doing=(
        "RECOVR is investigating the settlement mismatch "
        "and preparing the appropriate recovery action."
    ),

    next_step="Settlement escalation",

    merchant_action_required=False
)


print(payment.model_dump())