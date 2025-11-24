from agents import intent_agent, sentiment_agent, troubleshooting_agent, escalation_agent, knowledge_search

def test_intent_billing():
    r = intent_agent.run({"text":"I was charged twice this month"})
    assert r['intent'] == 'billing_issue'

def test_sentiment_urgent():
    r = sentiment_agent.run({"text":"I need this fixed now!!!"})
    assert r['urgency'] == 'high'

def test_troubleshoot_router():
    r = troubleshooting_agent.run({"text":"My router has no internet"})
    assert any('Unplug' in step['step'] for step in r['plan'])

def test_escalation_handoff():
    res = {"response":"I lost $200","flags":["escalate"]}
    r = escalation_agent.run({"user_id":"u1","result":res})
    assert r['escalate'] == True
