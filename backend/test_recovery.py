from models import Payment, PaymentJourney
from recovery import execute_recovery_action


payment = Payment(
    payment_id="PAY_RETRY_001",
    order_id="ORD_RETRY_001",
    customer_name="Test Customer",
    amount=5000.00,
    payment_method="UPI",
    status="AT_RISK",

    journey=PaymentJourney(
        payment_started=True,
        bank_confirmed=True,
        razorpay_received=False,
        settlement_completed=False,
        merchant_bank_credited=False
    ),

    recovery_attempts=0,
    max_attempts=3
)


retry_policy = {
    "allowed": True,
    "action": "RETRY",
    "reason": "Retry is allowed.",
    "approval_required": False
}


print("\nRECOVERY SAFETY TEST")
print("====================")


for attempt in range(1, 5):

    result = execute_recovery_action(
        payment,
        retry_policy
    )

    print("\nAttempt:", attempt)
    print("Executed:", result["executed"])
    print("Action:", result["action"])
    print("Status:", result["status"])
    print("Attempts Used:", payment.recovery_attempts)
    print(
        "Stopping Rule:",
        payment.stopping_rule_triggered
    )