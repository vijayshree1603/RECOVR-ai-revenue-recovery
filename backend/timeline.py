from models import Payment
from detection import detect_payment_issue


def build_payment_timeline(payment: Payment):

    detection = detect_payment_issue(payment)

    journey = payment.journey

    stages = [
        {
            "stage": "PAYMENT_STARTED",
            "label": "Payment Started",
            "completed": journey.payment_started
        },
        {
            "stage": "BANK_CONFIRMED",
            "label": "Bank Confirmed",
            "completed": journey.bank_confirmed
        },
        {
            "stage": "RAZORPAY_RECEIVED",
            "label": "Payment Received",
            "completed": journey.razorpay_received
        },
        {
            "stage": "SETTLEMENT",
            "label": "Settlement",
            "completed": journey.settlement_completed
        },
        {
            "stage": "MERCHANT_BANK",
            "label": "Merchant Bank",
            "completed": journey.merchant_bank_credited
        }
    ]

    stuck_at = detection["stuck_at"]

    for stage in stages:

        if stage["stage"] == stuck_at:
            stage["status"] = "STUCK"
        elif stage["completed"]:
            stage["status"] = "COMPLETED"
        else:
            stage["status"] = "PENDING"

    return {
        "payment_id": payment.payment_id,
        "amount": payment.amount,
        "detected": detection["detected"],
        "stuck_at": stuck_at,
        "message": detection["message"],
        "timeline": stages
    }