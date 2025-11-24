def verify_output(final_response):
    bad=["unknown","undefined","cannot help"]
    for b in bad:
        if b in final_response.lower():
            return "Let me double check that for you."
    return final_response
