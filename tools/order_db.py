"""
Order Database Tool
Provides ADK tools for querying order information from SQLite database
"""
import sqlite3
from typing import Optional, Dict, Any
import config

def get_order_status(order_id: str) -> Dict[str, Any]:
    """
    Get order status and details by order ID
    
    Args:
        order_id: Order ID (e.g., "ORD12345" or just "12345")
    
    Returns:
        Dictionary with order details or error message
    """
    # Normalize order ID
    if not order_id.startswith("ORD"):
        order_id = f"ORD{order_id}"
    
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM orders WHERE order_id = ?
        """, (order_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return {
                "success": False,
                "error": f"Order {order_id} not found. Please check the order number."
            }
        
        # Convert to dictionary
        order = dict(row)
        
        return {
            "success": True,
            "order": {
                "order_id": order["order_id"],
                "customer_name": order["customer_name"],
                "status": order["status"],
                "order_date": order["order_date"],
                "total_amount": order["total_amount"],
                "items": order["items"],
                "tracking_number": order["tracking_number"],
                "last_scan_location": order["last_scan_location"],
                "estimated_delivery": order["estimated_delivery"],
                "shipping_address": order["shipping_address"]
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Database error: {str(e)}"
        }


def search_orders(customer_name: Optional[str] = None, 
                 customer_email: Optional[str] = None,
                 status: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for orders by customer name, email, or status
    
    Args:
        customer_name: Customer name to search for
        customer_email: Customer email to search for
        status: Order status to filter by
    
    Returns:
        Dictionary with list of matching orders or error message
    """
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM orders WHERE 1=1"
        params = []
        
        if customer_name:
            query += " AND customer_name LIKE ?"
            params.append(f"%{customer_name}%")
        
        if customer_email:
            query += " AND customer_email LIKE ?"
            params.append(f"%{customer_email}%")
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return {
                "success": False,
                "error": "No orders found matching the criteria."
            }
        
        orders = []
        for row in rows:
            order = dict(row)
            orders.append({
                "order_id": order["order_id"],
                "customer_name": order["customer_name"],
                "status": order["status"],
                "order_date": order["order_date"],
                "total_amount": order["total_amount"],
                "items": order["items"]
            })
        
        return {
            "success": True,
            "orders": orders,
            "count": len(orders)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Database error: {str(e)}"
        }
