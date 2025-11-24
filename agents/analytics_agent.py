analytics_log=[]
def update_analytics(message,intent,category,sentiment):
    analytics_log.append({
        "message":message,
        "intent":intent,
        "category":category,
        "sentiment":sentiment
    })
