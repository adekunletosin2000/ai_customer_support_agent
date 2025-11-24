def classify_request(message: str):
    msg = message.lower()
    if any(x in msg for x in ["wifi","router","internet"]):
        return "network_support"
    if any(x in msg for x in ["charge","invoice","billing"]):
        return "billing"
    return "general"
