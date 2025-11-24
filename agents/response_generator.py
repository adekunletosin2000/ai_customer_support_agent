# Minimal response generator using templates
def run(request):
    text = request.get("text","")
    if "charged" in text.lower() or "refund" in text.lower():
        resp = "Sorry about that — I can help. Can you confirm the last 4 digits of the card used, or the order number?"
        flags = []
        if "lost" in text.lower() or "stolen" in text.lower():
            flags = ["escalate"]
        return {"agent_name":"ResponseGenerator","response":resp,"confidence":0.9,"explain":"Billing template used.","flags":flags}
    if any(k in text.lower() for k in ["internet","wifi","router","connection"]):
        resp = "I can help troubleshoot your connection. First: unplug the router for 15 seconds and plug it back in. Did that help?"
        return {"agent_name":"ResponseGenerator","response":resp,"confidence":0.85,"explain":"Troubleshooting template used.","flags":[]}
    return {"agent_name":"ResponseGenerator","response":"Thanks for the message — can you tell me a bit more about the issue?","confidence":0.7,"explain":"Fallback question."}
