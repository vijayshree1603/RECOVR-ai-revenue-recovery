from pydantic import BaseModel
from typing import Optional


class PaymentJourney(BaseModel):
    payment_started: bool = False
    bank_confirmed: bool = False
    razorpay_received: bool = False
    settlement_completed: bool = False
    merchant_bank_credited: bool = False


class Payment(BaseModel):
    payment_id: str
    order_id: str
    customer_name: str
    amount: float
    payment_method: str

    status: str
    failure_reason: Optional[str] = None
    root_cause: Optional[str] = None
    diagnosis_confidence: Optional[float] = None

    journey: PaymentJourney

    recovery_action: Optional[str] = None
    recovery_attempts: int = 0
    max_attempts: int = 3
    recovered_amount: float = 0.0

    policy_allowed: bool = False
    approval_required: bool = False
    stopping_rule_triggered: bool = False

    what_happened: Optional[str] = None
    what_recovr_is_doing: Optional[str] = None
    next_step: Optional[str] = None
    merchant_action_required: bool = False

    escalation_created: bool = False
    stuck_at: Optional[str] = None
    recovery_status: Optional[str] = None
