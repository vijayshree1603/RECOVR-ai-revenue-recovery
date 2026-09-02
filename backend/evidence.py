from models import Payment
from detection import detect_payment_issue


def build_payment_evidence(payment: Payment):

    detection = detect_payment_issue(payment)

    return {
        "payment": {
            "payment_id": payment.payment_id,
            "order_id": payment.order_id,
            "amount": payment.amount,
            "payment_method": payment.payment_method,
            "status": payment.status
        },

        "journey": {
            "payment_started": payment.journey.payment_started,
            "bank_confirmed": payment.journey.bank_confirmed,
            "razorpay_received": payment.journey.razorpay_received,
            "settlement_completed": payment.journey.settlement_completed,
            "merchant_bank_credited": payment.journey.merchant_bank_credited
        },

        "failure": {
            "failure_reason": payment.failure_reason
        },

        "recovery": {
            "previous_attempts": payment.recovery_attempts,
            "max_attempts": payment.max_attempts
        },

        "detection": {
            "detected": detection["detected"],
            "stuck_at": detection["stuck_at"],
            "message": detection["message"]
        }
    }