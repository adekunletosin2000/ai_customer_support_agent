import os
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext
import google.generativeai as genai
import json
from typing import Dict, Any, List
from datetime import datetime

# Load environment
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Configure both ADK and direct genai
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

print("✅ Setup and authentication complete.")

# Retry configuration for ADK
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# ============================================================================
# ENHANCED TOOLS USING ORCHESTRATOR LOGIC
# ============================================================================

class EnhancedAgentTools:
    """Enhanced tools that combine ADK structure with Orchestrator intelligence"""
    
    def __init__(self):
        self.knowledge_base = {
            "internet_issues": [
                "Unplug router for 30 seconds and plug back in",
                "Check if cables are properly connected",
                "Restart your device (phone/laptop)",
                "Contact ISP if issue persists"
            ],
            "billing_issues": [
                "Check your last invoice for charges",
                "Verify payment method is up to date",
                "Contact billing department for disputes"
            ],
            "app_problems": [
                "Clear app cache in settings",
                "Update app to latest version",
                "Reinstall the application",
                "Check if device meets minimum requirements"
            ]
        }
        self.conversation_history = []
    
    def detect_intent(self, message: str) -> str:
        """
        Detect customer intent using AI analysis.
        Classifies messages as: technical_support, billing_inquiry, general_question, complaint, or feature_request.
        
        Args:
            message: The customer's message text
            
        Returns:
            JSON string with intent, confidence, and keywords
        """
        prompt = f"""Analyze this customer message and identify the primary intent.
        
Customer Message: "{message}"

Classify as: technical_support, billing_inquiry, general_question, complaint, or feature_request

Return JSON:
{{
    "intent": "intent_type",
    "confidence": 0.95,
    "keywords": ["list", "of", "key", "words"]
}}"""
        
        try:
            response = model.generate_content(prompt)
            result = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
            return json.dumps(result)
        except:
            return json.dumps({"intent": "general_question", "confidence": 0.5, "keywords": []})
    
    def classify_issue(self, message: str) -> str:
        """
        Classify customer issues into categories with AI.
        Determines category, priority level, and appropriate department.
        
        Args:
            message: The customer's message text
            
        Returns:
            JSON string with category, priority, department, and confidence
        """
        prompt = f"""Categorize this support request.
        
Message: "{message}"

Categories: internet, billing, app, hardware, account
Priority: low, medium, high, urgent
Department: tech_support, billing, customer_service

Return JSON:
{{
    "category": "category_name",
    "priority": "priority_level",
    "department": "department_name",
    "confidence": 0.9
}}"""
        
        try:
            response = model.generate_content(prompt)
            result = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
            return json.dumps(result)
        except:
            return json.dumps({
                "category": "general", 
                "priority": "medium", 
                "department": "customer_service",
                "confidence": 0.5
            })
    
    def analyze_sentiment(self, message: str) -> str:
        """
        Analyze customer sentiment and urgency using AI.
        Detects emotional tone, urgency level, and provides emotion score.
        
        Args:
            message: The customer's message text
            
        Returns:
            JSON string with sentiment, urgency, emotion_score, and detected_emotions
        """
        prompt = f"""Analyze the emotional tone of this message.
        
Message: "{message}"

Determine sentiment (positive, neutral, negative, angry, frustrated), 
urgency (low, medium, high), and emotion score (-1.0 to 1.0)

Return JSON:
{{
    "sentiment": "sentiment_type",
    "urgency": "urgency_level",
    "emotion_score": 0.5,
    "detected_emotions": ["emotion1", "emotion2"]
}}"""
        
        try:
            response = model.generate_content(prompt)
            result = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
            return json.dumps(result)
        except:
            return json.dumps({
                "sentiment": "neutral", 
                "urgency": "medium", 
                "emotion_score": 0.0,
                "detected_emotions": []
            })
    
    def search_knowledge_base(self, query: str) -> str:
        """
        Search knowledge base for solutions with AI assistance.
        Finds relevant solutions from internal documentation and FAQs.
        
        Args:
            query: The search query or problem description
            
        Returns:
            JSON string with solutions, sources, and confidence score
        """
        # First, do direct keyword matching
        solutions = []
        for key, value in self.knowledge_base.items():
            if any(word in query.lower() for word in key.split('_')):
                solutions.extend(value)
        
        # If no direct match, use AI to find relevant solutions
        if not solutions:
            prompt = f"""Given this customer query: "{query}"
            
Which of these categories is most relevant?
- internet_issues
- billing_issues  
- app_problems
- general_support

Return only the category name."""
            
            try:
                response = model.generate_content(prompt)
                category = response.text.strip().lower()
                if category in self.knowledge_base:
                    solutions = self.knowledge_base[category]
            except:
                pass
        
        if not solutions:
            solutions = ["No specific solution found. Connecting you with a specialist..."]
        
        return json.dumps({
            "solutions": solutions,
            "sources": ["Internal KB", "FAQ Database"],
            "confidence": 0.85 if len(solutions) > 1 else 0.5
        })
    
    def generate_troubleshooting_steps(self, message: str, category: str) -> str:
        """
        Generate step-by-step troubleshooting guide using AI.
        Creates clear, actionable steps for resolving customer issues.
        
        Args:
            message: The customer's problem description
            category: The problem category (e.g., 'internet', 'billing', 'app')
            
        Returns:
            JSON string with steps, estimated_time, and difficulty level
        """
        prompt = f"""Create step-by-step troubleshooting for this problem.
        
Problem: "{message}"
Category: {category}

Provide 3-5 clear, actionable steps with estimated time.

Return JSON:
{{
    "steps": ["Step 1: Action", "Step 2: Action", "Step 3: Action"],
    "estimated_time": "5-10 minutes",
    "difficulty": "easy/medium/hard"
}}"""
        
        try:
            response = model.generate_content(prompt)
            result = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
            return json.dumps(result)
        except:
            return json.dumps({
                "steps": ["Please contact support for assistance"],
                "estimated_time": "Varies",
                "difficulty": "medium"
            })
    
    def check_escalation(self, sentiment: str, priority: str) -> str:
        """
        Determine if issue requires escalation to human agent.
        Analyzes sentiment and priority to decide escalation level.
        
        Args:
            sentiment: The detected sentiment (e.g., 'angry', 'frustrated', 'neutral')
            priority: The issue priority (e.g., 'urgent', 'high', 'medium', 'low')
            
        Returns:
            JSON string with should_escalate, escalation_reason, escalation_level, and recommended_action
        """
        should_escalate = (
            sentiment in ["angry", "frustrated", "negative"] or
            priority in ["urgent", "high"]
        )
        
        return json.dumps({
            "should_escalate": should_escalate,
            "escalation_reason": "High priority or negative sentiment detected" if should_escalate else None,
            "escalation_level": "tier_2" if should_escalate else "tier_1",
            "recommended_action": "Transfer to human agent" if should_escalate else "Continue with AI"
        })
    
    def escalate_to_human(
        self, 
        reason: str, 
        customer_message: str,
        tool_context: ToolContext
    ) -> str:
        """
        Escalate issue to human agent with approval workflow.
        Pauses execution to wait for human agent availability.
        
        Args:
            reason: Reason for escalation (e.g., 'angry_customer', 'complex_issue')
            customer_message: The original customer message
            tool_context: Context for handling human-in-the-loop
            
        Returns:
            JSON string with escalation status and agent details
        """
        
        # SCENARIO 1: First call - request human agent confirmation
        if not tool_context.tool_confirmation:
            tool_context.request_confirmation(
                hint=f"🚨 Escalation Required: {reason}\nCustomer message: '{customer_message}'\n\nAssign to human agent?",
                payload={
                    "reason": reason,
                    "customer_message": customer_message,
                    "timestamp": datetime.now().isoformat()
                }
            )
            return json.dumps({
                "status": "awaiting_agent",
                "message": "Your request is being escalated to a human specialist. Please wait...",
                "estimated_wait": "2-5 minutes"
            })
        
        # SCENARIO 2: Human agent confirmed - complete escalation
        if tool_context.tool_confirmation.confirmed:
            # In a real system, this would assign to an actual agent
            agent_id = f"AGENT-{hash(customer_message) % 1000:03d}"
            return json.dumps({
                "status": "escalated",
                "agent_id": agent_id,
                "agent_name": "Human Support Specialist",
                "message": "You've been connected to a human agent who will assist you shortly.",
                "escalation_reason": reason
            })
        else:
            # Human agent declined or unavailable
            return json.dumps({
                "status": "escalation_failed",
                "message": "Unable to connect to human agent at this time. We'll continue with AI assistance.",
                "fallback_action": "Provide extended troubleshooting"
            })

# Initialize enhanced tools
enhanced_tools = EnhancedAgentTools()

# Create ADK Function Tools with enhanced capabilities
intent_tool = FunctionTool(enhanced_tools.detect_intent)
classifier_tool = FunctionTool(enhanced_tools.classify_issue)
sentiment_tool = FunctionTool(enhanced_tools.analyze_sentiment)
knowledge_tool = FunctionTool(enhanced_tools.search_knowledge_base)
troubleshooting_tool = FunctionTool(enhanced_tools.generate_troubleshooting_steps)
escalation_check_tool = FunctionTool(enhanced_tools.check_escalation)
escalate_human_tool = FunctionTool(func=enhanced_tools.escalate_to_human)

print("✅ Enhanced AI-powered tools created (7 tools)")

# ============================================================================
# CREATE HYBRID ADK AGENT
# ============================================================================

support_agent = LlmAgent(
    model=Gemini(
        model_id="gemini-1.5-flash-latest",
        http_retry_options=retry_config
    ),
    name="Hybrid_Multi_Agent_Support_System",
    instruction="""You are an advanced multi-agent customer support system powered by Google ADK and AI orchestration.

WORKFLOW - Follow this exact sequence:
1. 🎯 detect_intent - Understand what the customer wants
2. 📋 classify_issue - Categorize the problem (category, priority, department)
3. 💭 analyze_sentiment - Check customer emotion and urgency
4. 🔍 search_knowledge_base - Find relevant solutions
5. 🛠️ generate_troubleshooting_steps - Create step-by-step guide (use message and category from classify_issue)
6. ⚠️ check_escalation - Determine if human intervention needed (use sentiment and priority)
7. 🚨 escalate_to_human - If should_escalate=true, transfer to human agent (use reason and customer message)

ESCALATION RULES:
- If check_escalation indicates should_escalate=true, call escalate_to_human
- Provide the escalation_reason from check_escalation and the original customer message
- Wait for human agent assignment confirmation
- Inform customer about the escalation and expected wait time

RESPONSE GUIDELINES:
- Use ALL tools in sequence for complete analysis
- Be empathetic if sentiment is negative
- Provide clear, numbered steps from troubleshooting
- Handle escalations professionally and promptly
- Keep responses friendly and professional
- Include estimated time for solutions

FORMAT:
"I understand [issue]. Here's how I can help:

[Troubleshooting steps from tool]

This should take approximately [time]. [Escalation note if needed]"

Always use the tools to make informed decisions.""",
    tools=[
        intent_tool,
        classifier_tool, 
        sentiment_tool, 
        knowledge_tool,
        troubleshooting_tool,
        escalation_check_tool,
        escalate_human_tool
    ]
)

print("✅ Hybrid support agent created with 7 AI-powered tools")

# Create session service and runner - FIXED VERSION
session_service = InMemorySessionService()

# CRITICAL FIX: Use app_name and agent parameters instead of app
runner = Runner(
    app_name="multi_agent_support",
    agent=support_agent,
    session_service=session_service
)

print("✅ ADK Runner initialized")

print("\n" + "="*60)
print("🚀 HYBRID MULTI-AGENT SUPPORT SYSTEM")
print("="*60)
print("✅ Google ADK Framework + AI Orchestration")
print("✅ 7 Enhanced AI Tools:")
print("   1. Intent Detection (AI-powered)")
print("   2. Issue Classifier (AI-powered)")
print("   3. Sentiment Analysis (AI-powered)")
print("   4. Knowledge Search (AI-enhanced)")
print("   5. Troubleshooting Generator (AI-powered)")
print("   6. Escalation Checker (Rule-based + AI)")
print("   7. Human Escalation (Human-in-the-loop)")
print("="*60 + "\n")

# ============================================================================
# EXPORT FOR FLASK
# ============================================================================

def get_runner():
    """Export runner for Flask app"""
    return runner

def get_agent():
    """Export agent for Flask app"""
    return support_agent

def get_session_service():
    """Export session service for Flask app"""
    return session_service

# ============================================================================
# TEST FUNCTION
# ============================================================================

def test_hybrid_system():
    """Test the hybrid system"""
    import uuid
    
    test_messages = [
        "My internet is not working at all! I've been trying for hours!",
        "I was charged twice on my last bill",
        "How do I reset my password?"
    ]
    
    session_id = str(uuid.uuid4())
    
    for message in test_messages:
        print(f"\n📨 User: {message}")
        print("-" * 60)
        
        response = runner.run(
            user_id="test_user",
            session_id=session_id,
            new_message=message
        )
        
        print(f"🤖 Agent: {response.agent_response}")
        print("="*60)

if __name__ == "__main__":
    test_hybrid_system()