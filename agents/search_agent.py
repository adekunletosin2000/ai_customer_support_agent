import json
def search_kb(query: str):
    with open("knowledge_base/data.json","r") as f:
        kb=json.load(f)
    q=query.lower()
    for item in kb:
        if item["keyword"] in q:
            return item["answer"]
    return None
