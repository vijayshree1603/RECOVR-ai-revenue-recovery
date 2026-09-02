from typing import Dict


def calculate_recovery_priority(
    amount: float,
    severity: str,
    recovery_likelihood: float,
    age_hours: float
) -> Dict:

    # Money risk: capped so extremely large payments
    # do not completely dominate the score.
    money_score = min(amount / 1000, 40)

    # Severity score
    severity_scores = {
        "LOW": 5,
        "MEDIUM": 15,
        "HIGH": 25,
        "CRITICAL": 30
    }

    severity_score = severity_scores.get(severity, 10)

    # Recovery likelihood contributes up to 20 points
    likelihood_score = recovery_likelihood * 20

    # Older unresolved payments become more urgent.
    urgency_score = min(age_hours / 24 * 15, 15)

    total_score = (
        money_score
        + severity_score
        + likelihood_score
        + urgency_score
    )

    total_score = min(round(total_score, 2), 100)

    if total_score >= 75:
        priority = "CRITICAL"
    elif total_score >= 50:
        priority = "HIGH"
    elif total_score >= 25:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return {
        "priority_score": total_score,
        "priority": priority,
        "components": {
            "money_score": round(money_score, 2),
            "severity_score": severity_score,
            "likelihood_score": round(likelihood_score, 2),
            "urgency_score": round(urgency_score, 2)
        }
    }