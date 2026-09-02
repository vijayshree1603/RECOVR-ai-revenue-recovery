from models import Payment, PaymentJourney
from detection import detect_payment_issue


def create_payment(payment_id, journey):
    return Payment(
        payment_id=payment_id,
        order_id="ORD_" + payment_id,
        customer_name="Test Customer",
        amount=5000.00,
        payment_method="UPI",
        status="PROCESSING",
        journey=journey
    )


test_cases = [

    (
        "Payment Not Started",
        PaymentJourney(
            payment_started=False,
            bank_confirmed=False,
            razorpay_received=False,
            settlement_completed=False,
            merchant_bank_credited=False
        )
    ),

    (
        "Waiting For Bank",
        PaymentJourney(
            payment_started=True,
            bank_confirmed=False,
            razorpay_received=False,
            settlement_completed=False,
            merchant_bank_credited=False
        )
    ),

    (
        "Waiting For Razorpay",
        PaymentJourney(
            payment_started=True,
            bank_confirmed=True,
            razorpay_received=False,
            settlement_completed=False,
            merchant_bank_credited=False
        )
    ),

    (
        "Stuck At Settlement",
        PaymentJourney(
            payment_started=True,
            bank_confirmed=True,
            razorpay_received=True,
            settlement_completed=False,
            merchant_bank_credited=False
        )
    ),

    (
        "Payment Completed",
        PaymentJourney(
            payment_started=True,
            bank_confirmed=True,
            razorpay_received=True,
            settlement_completed=True,
            merchant_bank_credited=True
        )
    )
]


for name, journey in test_cases:

    payment = create_payment(
        payment_id=name.replace(" ", "_").upper(),
        journey=journey
    )

    result = detect_payment_issue(payment)

    print("\n--------------------------------")
    print(name)
    print("--------------------------------")
    print("Detected:", result["detected"])
    print("Stuck At:", result["stuck_at"])
    print("Message:", result["message"])