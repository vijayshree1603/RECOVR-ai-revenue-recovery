from policy import evaluate_policy


test_cases = [

    {
        "name": "Normal Escalation",
        "recommended_action": "ESCALATE",
        "confidence": 0.94,
        "recovery_attempts": 0,
        "max_attempts": 3,
        "payment_recovered": False,
        "stopping_rule_triggered": False
    },

    {
        "name": "Maximum Retry Reached",
        "recommended_action": "RETRY",
        "confidence": 0.95,
        "recovery_attempts": 3,
        "max_attempts": 3,
        "payment_recovered": False,
        "stopping_rule_triggered": False
    },

    {
        "name": "Low AI Confidence",
        "recommended_action": "RETRY",
        "confidence": 0.55,
        "recovery_attempts": 0,
        "max_attempts": 3,
        "payment_recovered": False,
        "stopping_rule_triggered": False
    },

    {
        "name": "Already Recovered",
        "recommended_action": "RETRY",
        "confidence": 0.95,
        "recovery_attempts": 0,
        "max_attempts": 3,
        "payment_recovered": True,
        "stopping_rule_triggered": False
    }
]


for test in test_cases:

    result = evaluate_policy(
        recommended_action=test["recommended_action"],
        confidence=test["confidence"],
        recovery_attempts=test["recovery_attempts"],
        max_attempts=test["max_attempts"],
        payment_recovered=test["payment_recovered"],
        stopping_rule_triggered=test["stopping_rule_triggered"]
    )

    print("\n--------------------------------")
    print(test["name"])
    print("--------------------------------")

    print("Allowed:", result["allowed"])
    print("Action:", result["action"])
    print("Reason:", result["reason"])
    print("Approval Required:", result["approval_required"])