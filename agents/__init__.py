"""
Agents package for VisionSupport AI  
Contains specialized agents for different customer support tasks
"""

from .orchestrator import OrchestratorAgent
from .order_tracking import OrderTrackingAgent
from .faq import FAQAgent
# Future agents (Day 3-4):
# from .visual import VisualAgent
# from .returns import ReturnsAgent  
# from .sentiment import SentimentMonitor

__all__ = [
    'OrchestratorAgent',
    'OrderTrackingAgent',
    'FAQAgent',
]
