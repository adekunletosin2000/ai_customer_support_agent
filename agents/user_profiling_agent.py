# Minimal user profiling (in-memory)
PROFILES = {}
def update(entry):
    uid = entry.get("user_id")
    if uid not in PROFILES:
        PROFILES[uid] = {"interactions":0}
    PROFILES[uid]["interactions"] += 1
    # naive last_issue detection
    txt = entry.get("text","")
    if "charged" in txt:
        PROFILES[uid]["last_issue"] = "billing_issue"
    return {"profile":PROFILES[uid],"confidence":0.8}
def run(uid):
    return PROFILES.get(uid, {})
