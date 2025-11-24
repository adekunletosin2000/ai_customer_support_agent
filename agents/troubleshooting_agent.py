# Minimal troubleshooting agent returning a step plan
def run(request):
    text = request.get("text","").lower()
    if "router" in text or "internet" in text or "wifi" in text:
        plan = [
            {"step":"Unplug router for 15 seconds and plug back in","expected":"LED lights back to normal","check_question":"Did this fix the issue? (yes/no)"},
            {"step":"Reboot your device (phone/computer)","expected":"Device reconnects","check_question":"Did device reconnect? (yes/no)"},
            {"step":"If still failing, collect error messages and escalate for deeper diagnostics","expected":"Support scheduled","check_question":"Do you want me to escalate? (yes/no)"}
        ]
        return {"agent_name":"Troubleshooting","plan":plan,"confidence":0.9,"explain":"Router troubleshooting plan."}
    return {"agent_name":"Troubleshooting","plan":[{"step":"Collect more details","expected":"More info","check_question":"Please provide model and error text."}],"confidence":0.6}
