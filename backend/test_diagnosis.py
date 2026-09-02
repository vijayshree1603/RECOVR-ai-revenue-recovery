from models import Payment, PaymentJourney
from detection import detect_payment_issue
from diagnosis import diagnose_payment


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
    )
)


detection_result = detect_payment_issue(payment)

diagnosis_result = diagnose_payment(
    payment,
    detection_result
)


print("\nDETECTION")
print("---------" )
print(detection_result)

print("\nDIAGNOSIS")
print("---------")
print(diagnosis_result)