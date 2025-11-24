def detect_intent(message: str):
    msg = message.lower()
    if "refund" in msg:
        return "refund_request"
    if "not working" in msg or "problem" in msg or "issue" in msg:
        return "technical_issue"
    if "charge" in msg or "payment" in msg:
        return "billing_issue"
    return "general"
