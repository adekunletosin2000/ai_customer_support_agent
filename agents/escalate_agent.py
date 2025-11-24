def check_escalation(message: str, sentiment: str):
    if sentiment=="negative":
        return True
    return False
