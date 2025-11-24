# Safety filter: simple regex masks and keyword checks
import re
def _mask_pii(text):
    # mask simple credit card-like sequences (very naive)
    masked = re.sub(r"\b\d{4}-?\d{4}-?\d{4}-?\d{4}\b","[CARD]", text)
    masked = re.sub(r"\b\d{16}\b","[CARD]", masked)
    return masked

def run(request):
    text = request.get("text","")
    lowered = text.lower()
    decision = "allow"
    reason = ""
    if any(k in lowered for k in ["bomb","kill","illegal","attack"]):
        decision = "block"
        reason = "Illegal/dangerous content"
    masked = _mask_pii(text)
    return { "decision":decision, "masked_text":masked, "reason":reason }
