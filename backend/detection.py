from models import Payment


def detect_payment_issue(payment: Payment):

    journey = payment.journey

    # Payment has not even started
    if not journey.payment_started:
        return {
            "detected": True,
            "stuck_at": "PAYMENT_START",
            "message": "The payment has not started yet."
        }

    # Payment started but bank did not confirm
    if not journey.bank_confirmed:
        return {
            "detected": True,
            "stuck_at": "BANK",
            "message": "The payment is waiting for bank confirmation."
        }

    # Bank confirmed but Razorpay did not receive it
    if not journey.razorpay_received:
        return {
            "detected": True,
            "stuck_at": "RAZORPAY",
            "message": "The payment was confirmed by the bank but has not been received by Razorpay."
        }

    # Payment received but settlement is incomplete
    if not journey.settlement_completed:
        return {
            "detected": True,
            "stuck_at": "SETTLEMENT",
            "message": "The payment was received successfully but settlement has not been completed."
        }

    # Settlement completed but merchant bank not credited
    if not journey.merchant_bank_credited:
        return {
            "detected": True,
            "stuck_at": "MERCHANT_BANK",
            "message": "The payment has been settled but has not yet been credited to the merchant bank."
        }

    # Everything completed
    return {
        "detected": False,
        "stuck_at": None,
        "message": "Payment journey completed successfully."
    }