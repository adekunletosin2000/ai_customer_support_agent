def summarize_text(text: str):
    words=text.split()
    return " ".join(words[:15])+"..." if len(words)>15 else text
