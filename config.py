"""
Configuration file for VisionSupport AI
Loads environment variables and defines constants
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# App Configuration
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "True") == "True"

# Gemini Model Configuration
GEMINI_MODEL = "gemini-2.0-flash-exp"  # Fast model for general agents
GEMINI_VISION_MODEL = "gemini-2.0-flash-exp"  # Same model supports vision

# Database Configuration
DATABASE_PATH = "data/ecommerce.db"

# Knowledge Base Configuration
KNOWLEDGE_BASE_PATH = "data/knowledge_base"

# Agent Configuration
MAX_AGENT_ITERATIONS = 5  # Prevent infinite loops
AGENT_TIMEOUT_SECONDS = 30

# Session Configuration
SESSION_TIMEOUT_MINUTES = 30

# Sentiment Thresholds
SENTIMENT_ANGRY_THRESHOLD = 0.7  # Escalate if anger > 0.7
SENTIMENT_FRUSTRATED_THRESHOLD = 0.6  # Offer human help if frustration > 0.6

# UI Configuration
STREAMLIT_PAGE_TITLE = "VisionSupport AI"
STREAMLIT_PAGE_ICON = "🤖"
STREAMLIT_LAYOUT = "wide"

def validate_config():
    """Validate that required configuration is present"""
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY not found. Please copy .env.template to .env and add your API key"
        )
    return True
