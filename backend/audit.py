from datetime import datetime
from typing import Dict, List


def create_audit_event(
    event_type: str,
    message: str,
    details: Dict = None
) -> Dict:

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "event_type": event_type,
        "message": message,
        "details": details or {}
    }


def add_audit_event(
    history: List[Dict],
    event_type: str,
    message: str,
    details: Dict = None
):

    event = create_audit_event(
        event_type=event_type,
        message=message,
        details=details
    )

    history.append(event)

    return event