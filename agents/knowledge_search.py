# Simple in-memory KB using TF-IDF (no external vector DB)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

KB_DOCS = [
    {"id":"kb-1","text":"If you were charged twice, contact billing with order id or last 4 digits of card."},
    {"id":"kb-2","text":"To reset your router, unplug it for 15 seconds and plug it back in."},
    {"id":"kb-3","text":"Change password via Settings > Account > Change Password."},
    {"id":"kb-4","text":"Refunds typically take 5-7 business days to appear."},
]

VEC = None
DOC_TEXTS = [d["text"] for d in KB_DOCS]

def _ensure_vec():
    global VEC
    if VEC is None:
        VEC = TfidfVectorizer().fit_transform(DOC_TEXTS)

def run(request):
    query = request.get("text","")
    _ensure_vec()
    q_vec = TfidfVectorizer().fit(DOC_TEXTS + [query]).transform([query])
    # fallback: compute cosine with stored docs via linear_kernel using combined vectorizer
    # Simpler approach: vectorize docs + query with same vectorizer:
    vec = TfidfVectorizer().fit(DOC_TEXTS + [query])
    doc_matrix = vec.transform(DOC_TEXTS)
    q = vec.transform([query])
    sims = linear_kernel(q, doc_matrix).flatten()
    idxs = np.argsort(-sims)[:3]
    results = []
    for i in idxs:
        results.append({"id":KB_DOCS[i]["id"],"passage":KB_DOCS[i]["text"],"score":float(sims[i])})
    return {"results":results,"confidence":0.9,"explain":"TF-IDF similarity results."}
