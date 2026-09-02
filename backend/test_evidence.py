from models import Payment, PaymentJourney
from evidence import build_payment_evidence


payment = Payment(
    payment_id="PAY_1001",
    order_id="ORD_5001",
    customer_name="Rahul",
    amount=5000.00,
    payment_method="UPI",

    status="AT_RISK",

    failure_reason="Settlement mismatch",

    journey=PaymentJourney(
        payment_started=True,
        bank_confirmed=True,
        razorpay_received=True,
        settlement_completed=False,
        merchant_bank_credited=False
    ),

    recovery_attempts=0,
    max_attempts=3
)


evidence = build_payment_evidence(payment)


print("\nRECOVR EVIDENCE")
print("================")

print(evidence)