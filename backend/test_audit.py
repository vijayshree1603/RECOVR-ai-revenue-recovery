from audit import add_audit_event


history = []


add_audit_event(
    history,
    "PAYMENT_RECEIVED",
    "Payment was received successfully.",
    {
        "amount": 5000,
        "payment_method": "UPI"
    }
)


add_audit_event(
    history,
    "DETECTION",
    "Payment appears to be stuck at settlement.",
    {
        "stuck_at": "SETTLEMENT"
    }
)


add_audit_event(
    history,
    "DIAGNOSIS",
    "Settlement mismatch detected.",
    {
        "root_cause": "SETTLEMENT_MISMATCH",
        "confidence": 0.94
    }
)


add_audit_event(
    history,
    "POLICY",
    "Escalation was allowed.",
    {
        "action": "ESCALATE",
        "approval_required": False
    }
)


add_audit_event(
    history,
    "RECOVERY",
    "Payment was escalated for investigation.",
    {
        "action": "ESCALATE",
        "status": "ESCALATED"
    }
)


print("\nRECOVR AUDIT HISTORY")
print("====================")


for event in history:

    print("\nTime:", event["timestamp"])
    print("Event:", event["event_type"])
    print("Message:", event["message"])
    print("Details:", event["details"])