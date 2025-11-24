# Escalation agent: prepare handoff
def run(request):
    result = request.get("result",{})
    summary = result.get("response","No response provided")
    handoff = f"""ESCALATION HANDOFF
Summary: {summary}
Flags: {result.get('flags',[])}
User: {request.get('user_id')}
"""
    return {"escalate":True,"priority":"high","handoff":handoff,"contact_info":"support-team@example.com"}
