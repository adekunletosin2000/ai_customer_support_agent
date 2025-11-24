def troubleshoot_issue(message: str):
    msg=message.lower()
    if "router" in msg:
        return "Restart the router using the reset button for 10 seconds."
    return None
