def generate_response(message,intent,category,kb,troubleshooting,escalation):
    if escalation:
        return "I am escalating this to a human agent."
    if troubleshooting:
        return troubleshooting
    if kb:
        return kb
    return "Thanks! I can help with that."
