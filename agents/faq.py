"""
FAQ Agent
Specialized agent for handling general knowledge base questions
"""
import config
from tools.knowledge_base import search_knowledge_base

class FAQAgent:
    """
    Agent that handles FAQ and policy questions
    """
    
    def __init__(self):
        """Initialize FAQ agent"""
        self.model_name = config.GEMINI_MODEL
        # Day 2: Add full ADK agent implementation with Gemini for better answers
        
    def process_query(self, message: str) -> dict:
        """
        Process FAQ query by searching knowledge base
        
        Args:
            message: User's question
        
        Returns:
            Dictionary with FAQ answer
        """
        # Search knowledge base
        result = search_knowledge_base(message)
        
        if not result['success']:
            return {
                'success': False,
                'response': result['error']
            }
        
        # Format response from knowledge base
        if result['results']:
            first_result = result['results'][0]
            category = first_result['category'].title()
            content = first_result['content']
            
            response = f"""**{category} Information**

{content}

---
*Is there anything specific you'd like to know about {category.lower()}?*
"""
            
            return {
                'success': True,
                'response': response,
                'category': category
            }
        else:
            return {
                'success': False,
                'response': 'I couldn\'t find specific information about that. Please contact our support team for assistance.'
            }
