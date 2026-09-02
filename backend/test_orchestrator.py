from models import Payment, PaymentJourney
from orchestrator import process_payment


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


result = process_payment(payment)


print("\n")
print("======================================")
print("        RECOVR END-TO-END RESULT")
print("======================================")


print("\nPAYMENT")
print("-------")
print("Payment ID:", result["payment_id"])
print("Amount: ₹", result["amount"])


print("\nDETECTION")
print("---------")
print("Stuck At:", result["detection"]["stuck_at"])


print("\nDIAGNOSIS")
print("---------")
print("Root Cause:", result["diagnosis"]["root_cause"])
print("Confidence:", result["diagnosis"]["confidence"])
print("Severity:", result["diagnosis"]["severity"])


print("\nPRIORITY")
print("--------")
print("Priority:", result["priority"]["priority"])
print("Score:", result["priority"]["priority_score"])


print("\nPOLICY")
print("------")
print("Allowed:", result["policy"]["allowed"])
print("Action:", result["policy"]["action"])
print("Approval Required:", result["policy"]["approval_required"])


print("\nRECOVERY")
print("--------")
print("Executed:", result["recovery"]["executed"])
print("Status:", result["recovery"]["status"])
print("Message:", result["recovery"]["message"])


print("\nAUDIT HISTORY")
print("-------------")

for event in result["audit_history"]:

    print(
        event["event_type"],
        "→",
        event["message"]
    )