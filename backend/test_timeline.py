from models import Payment, PaymentJourney
from timeline import build_payment_timeline


payment = Payment(
    payment_id="PAY_1001",
    order_id="ORD_5001",
    customer_name="Rahul",
    amount=5000.00,
    payment_method="UPI",
    status="AT_RISK",

    journey=PaymentJourney(
        payment_started=True,
        bank_confirmed=True,
        razorpay_received=True,
        settlement_completed=False,
        merchant_bank_credited=False
    )
)


result = build_payment_timeline(payment)


print("\nPAYMENT:", result["payment_id"])
print("AMOUNT: ₹", result["amount"])
print("STUCK AT:", result["stuck_at"])
print("\nPAYMENT JOURNEY:\n")


for stage in result["timeline"]:
    print(
        stage["label"],
        "→",
        stage["status"]
    )