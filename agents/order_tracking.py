"""
Order Tracking Agent
Specialized agent for handling order status queries
"""
import config
from tools.order_db import get_order_status, search_orders
import re

class OrderTrackingAgent:
    """
    Agent that handles order tracking and delivery status queries
    """
    
    def __init__(self):
        """Initialize order tracking agent"""
        self.model_name = config.GEMINI_MODEL
        # Day 2: Add full ADK agent implementation
        
    def extract_order_id(self, message: str) -> str:
        """
        Extract order ID from message
        Looks for patterns like: ORD12345, #12345, order 12345
        """
        # Try to find ORD followed by numbers
        match = re.search(r'ORD\d+', message, re.IGNORECASE)
        if match:
            return match.group(0).upper()
        
        # Try to find # followed by numbers
        match = re.search(r'#(\d+)', message)
        if match:
            return f"ORD{match.group(1)}"
        
        # Try to find standalone numbers (5 digits)
        match = re.search(r'\b(\d{5})\b', message)
        if match:
            return f"ORD{match.group(1)}"
        
        return None
    
    def process_query(self, message: str) -> dict:
        """
        Process order tracking query
        
        Args:
            message: User's message asking about order
        
        Returns:
            Dictionary with order information
        """
        # Extract order ID
        order_id = self.extract_order_id(message)
        
        if not order_id:
            return {
                'success': False,
                'response': 'I couldn\'t find an order number in your message. Please provide your order ID (e.g., ORD12345).'
            }
        
        # Get order status from database
        result = get_order_status(order_id)
        
        if not result['success']:
            return {
                'success': False,
                'response': result['error']
            }
        
        # Format response
        order = result['order']
        response = f"""**Order #{order['order_id']}**

📦 Status: **{order['status']}**
📅 Order Date: {order['order_date']}
🚚 Tracking: {order['tracking_number']}
📍 Last Scan: {order['last_scan_location']}
⏰ Estimated Delivery: {order['estimated_delivery']}

**Items:** {order['items']}
**Total:** ₹{order['total_amount']}

**Shipping to:**
{order['shipping_address']}
"""
        
        return {
            'success': True,
            'response': response,
            'order_data': order
        }
