from agents.intent_agent import detect_intent
from agents.classifier_agent import classify_request
from agents.sentiment_agent import analyze_sentiment
from agents.search_agent import search_kb
from agents.troubleshoot_agent import troubleshoot_issue
from agents.escalate_agent import check_escalation
from agents.response_agent import generate_response
from agents.analytics_agent import update_analytics
from agents.user_profile_agent import update_profile
from agents.verifier_agent import verify_output

def run_orchestration(message:str):
    intent=detect_intent(message)
    category=classify_request(message)
    sentiment=analyze_sentiment(message)
    kb=search_kb(message)
    troubleshooting=troubleshoot_issue(message)
    escalation=check_escalation(message,sentiment)
    response=generate_response(message,intent,category,kb,troubleshooting,escalation)
    final=verify_output(response)
    update_analytics(message,intent,category,sentiment)
    update_profile(message)
    return {
        "intent":intent,"category":category,"sentiment":sentiment,
        "kb":kb,"troubleshooting":troubleshooting,
        "escalation":escalation,"final_response":final
    }
