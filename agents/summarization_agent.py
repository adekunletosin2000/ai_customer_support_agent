# Simple summarization agent (extractive short summary)
def run(request):
    result = request.get("result",{})
    response = result.get("response","")
    summary = response if len(response)<120 else response[:117]+"..."
    key_facts = [response]
    return {"summary":summary,"key_facts":key_facts,"next_action":"ask for confirmation","confidence":0.9}
