import os
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext
import json
from typing import Dict, Any, List
from datetime import datetime

# Load environment
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

print("✅ Setup and authentication complete.")

# Retry configuration
retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

class SimplifiedAgentTools:
    """Simplified tools that don't make additional API calls"""
    
    def __init__(self):
        self.knowledge_base = {
            "internet": [
                "Unplug router for 30 seconds and plug back in",
                "Check if cables are properly connected",
                "Restart your device (phone/laptop)",
                "Contact ISP if issue persists"
            ],
            "billing": [
                "Check your last invoice for charges",
                "Verify payment method is up to date",
                "Contact billing department for disputes"
            ],
            "app": [
                "Clear app cache in settings",
                "Update app to latest version",
                "Reinstall the application"
            ],
            "api": [
                "Check API key is valid and not expired",
                "Verify API endpoint URL is correct",
                "Check rate limits",
                "Review error logs"
            ]
        }
    
    def search_knowledge_base(self, category: str) -> str:
        """Search knowledge base for solutions"""
        category = category.lower()
        
        # Find matching category
        for key, solutions in self.knowledge_base.items():
            if key in category or category in key:
                return json.dumps({
                    "category": key,
                    "solutions": solutions,
                    "found": True
                })
        
        return json.dumps({
            "category": "general",
            "solutions": ["Please describe your issue in more detail"],
            "found": False
        })
    
    def escalate_to_human(
        self, 
        reason: str, 
        customer_message: str,
        tool_context: ToolContext
    ) -> str:
        """Escalate issue to human agent"""
        
        if not tool_context.tool_confirmation:
            tool_context.request_confirmation(
                hint=f"🚨 Escalation: {reason}\nMessage: '{customer_message}'\n\nAssign to human?",
                payload={
                    "reason": reason,
                    "message": customer_message,
                    "timestamp": datetime.now().isoformat()
                }
            )
            return json.dumps({
                "status": "awaiting_confirmation",
                "message": "Escalating to human agent..."
            })
        
        if tool_context.tool_confirmation.confirmed:
            agent_id = f"AGENT-{hash(customer_message) % 1000:03d}"
            return json.dumps({
                "status": "escalated",
                "agent_id": agent_id,
                "message": "Connected to human agent"
            })
        
        return json.dumps({
            "status": "cancelled",
            "message": "Continuing with AI assistance"
        })

# Initialize tools
tools_instance = SimplifiedAgentTools()
knowledge_tool = FunctionTool(tools_instance.search_knowledge_base)
escalate_tool = FunctionTool(func=tools_instance.escalate_to_human)

print("✅ Simplified tools created (2 tools, no extra API calls)")

# Create support agent - SINGLE MODEL ONLY
support_agent = LlmAgent(
    model=Gemini(
        model_id="gemini-2.0-flash-exp",
        http_retry_options=retry_config
    ),
    name="Efficient_Support_Agent",
    instruction="""You are a helpful customer support agent. Follow this workflow:

1. **Understand the issue**: Listen to what the customer needs
2. **Categorize**: Determine if it's about internet, billing, app, api, or general support
3. **Search knowledge**: Use search_knowledge_base with the category (e.g., "internet", "billing")
4. **Provide solution**: Give clear, numbered steps from the knowledge base
5. **Escalate if needed**: If customer is frustrated or issue is complex, use escalate_to_human

RESPONSE FORMAT:
"I understand you're having [issue]. Here's how to fix it:

1. [Step from knowledge base]
2. [Step from knowledge base]
3. [Step from knowledge base]

This should take about [time]. [Add escalation note if escalating]"

Be friendly, concise, and helpful. Always use the knowledge base before suggesting escalation.""",
    tools=[knowledge_tool, escalate_tool]
)

print("✅ Efficient support agent created")

# Create session service and runner
session_service = InMemorySessionService()

runner = Runner(
    app_name="multi_agent_support",
    agent=support_agent,
    session_service=session_service
)

print("✅ ADK Runner initialized")

print("\n" + "="*60)
print("🚀 EFFICIENT SUPPORT SYSTEM")
print("="*60)
print("✅ Single Model: gemini-2.0-flash-exp")
print("✅ Optimized: 1 API call per message (vs 8)")
print("✅ 2 Tools:")
print("   1. Knowledge Base Search")
print("   2. Human Escalation")
print("="*60 + "\n")

def get_runner():
    return runner

def get_agent():
    return support_agent

def get_session_service():
    return session_service