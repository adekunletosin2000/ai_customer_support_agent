"""
Orchestrator Agent
Main agent that classifies intent and routes to specialized agents using Gemini AI
"""
import config

class OrchestratorAgent:
    """
    Main orchestrator that routes customer queries to appropriate specialized agents
    Uses Gemini AI for intelligent intent classification
    """
    
    def __init__(self):
        """Initialize orchestrator with Gemini model"""
        self.model_name = config.GEMINI_MODEL
        
    def classify_intent(self, message: str) -> str:
        """
        Classify user intent from message using Gemini AI
        
        Intents:
        - ORDER_TRACKING: Questions about order status, delivery
        - RETURNS: Questions about returns, refunds, exchanges
        - PRODUCT_INFO: Questions about products
        - FAQ: General questions about policies
        - GENERAL: Greetings, general conversation, capability questions
        - VISUAL_QUERY: User uploaded an image (Day 3)
        """
        try:
            import google.generativeai as genai
            
            # Configure Gemini
            genai.configure(api_key=config.GEMINI_API_KEY)
            model = genai.GenerativeModel(config.GEMINI_MODEL)
            
            # Use Gemini to classify intent
            prompt = f"""You are an intent classifier for an e-commerce customer support system.

Classify the following customer message into EXACTLY ONE of these categories:

1. ORDER_TRACKING - Questions about order status, delivery, tracking, shipping updates, "where is my package", etc.
2. RETURNS - Questions about returns, refunds, exchanges, damaged items, "I want my money back", etc.
3. PRODUCT_INFO - Questions about products, availability, pricing, stock, "is this available", etc.
4. FAQ - Questions about policies, shipping methods, payment options, "how long does shipping take", etc.
5. GENERAL - Greetings (hi, hello), thanks, general conversation, asking about capabilities

Customer message: "{message}"

Respond with ONLY the category name (e.g., "ORDER_TRACKING"), nothing else."""

            response = model.generate_content(prompt)
            intent = response.text.strip().upper()
            
            # Validate the intent is one we recognize
            valid_intents = ['ORDER_TRACKING', 'RETURNS', 'PRODUCT_INFO', 'FAQ', 'GENERAL', 'VISUAL_QUERY']
            if intent in valid_intents:
                return intent
            else:
                # If Gemini returns something unexpected, try to map it
                intent_lower = intent.lower()
                if 'order' in intent_lower or 'track' in intent_lower:
                    return 'ORDER_TRACKING'
                elif 'return' in intent_lower or 'refund' in intent_lower:
                    return 'RETURNS'
                elif 'product' in intent_lower:
                    return 'PRODUCT_INFO'
                elif 'faq' in intent_lower or 'policy' in intent_lower:
                    return 'FAQ'
                else:
                    return 'GENERAL'
                    
        except Exception as e:
            # Fallback to keyword matching ONLY if Gemini fails
            print(f"⚠️ Gemini intent classification failed: {e}, using keyword fallback")
            message_lower = message.lower()
            
            # Check for greetings first
            if any(word in message_lower for word in ['hello', 'hi ', 'hey', 'greetings']):
                return 'GENERAL'
            elif any(phrase in message_lower for phrase in ['what can you', 'how can you help', 'thank', 'thanks']):
                return 'GENERAL'
            
            # Specific intents
            if any(word in message_lower for word in ['order', 'delivery', 'shipped', 'track', 'status', 'package']):
                return 'ORDER_TRACKING'
            elif any(word in message_lower for word in ['return', 'refund', 'exchange', 'damaged', 'broken']):
                return 'RETURNS'
            elif any(word in message_lower for word in ['product', 'item', 'price', 'available', 'stock']):
                return 'PRODUCT_INFO'
            elif any(word in message_lower for word in ['shipping', 'payment', 'cod', 'emi', 'policy']):
                return 'FAQ'
            else:
                return 'GENERAL'
    
    def route_query(self, message: str, intent: str = None) -> dict:
        """
        Route query to appropriate agent based on intent
        
        Args:
            message: User's message
            intent: Classified intent (optional, will classify if not provided)
        
        Returns:
            Response dictionary with agent output
        """
        if not intent:
            intent = self.classify_intent(message)
        
        # Route to specialized agents
        response = {
            'intent': intent,
            'message': f'Routing to {intent} handler...',
            'success': True
        }
        
        return response
