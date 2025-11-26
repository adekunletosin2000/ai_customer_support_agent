"""
Knowledge Base Tool
Provides ADK tools for searching FAQ markdown files
"""
import os
from typing import List, Dict, Any
import config

def search_knowledge_base(query: str, category: str = None) -> Dict[str, Any]:
    """
    Search knowledge base for answers to FAQ questions
    
    Args:
        query: Search query (keywords from customer question)
        category: Optional category to search in (shipping, returns, payment)
    
    Returns:
        Dictionary with matching FAQ content or error message
    """
    try:
        knowledge_files = []
        
        if category:
            # Search specific category
            file_path = os.path.join(config.KNOWLEDGE_BASE_PATH, f"{category.lower()}.md")
            if os.path.exists(file_path):
                knowledge_files.append((category, file_path))
            else:
                return {
                    "success": False,
                    "error": f"Category '{category}' not found. Available: shipping, returns, payment"
                }
        else:
            # Search all categories
            for filename in os.listdir(config.KNOWLEDGE_BASE_PATH):
                if filename.endswith('.md'):
                    category_name = filename.replace('.md', '')
                    file_path = os.path.join(config.KNOWLEDGE_BASE_PATH, filename)
                    knowledge_files.append((category_name, file_path))
        
        if not knowledge_files:
            return {
                "success": False,
                "error": "No knowledge base files found"
            }
        
        # Search for query in files
        results = []
        query_lower = query.lower()
        
        for category_name, file_path in knowledge_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Simple keyword matching
                if query_lower in content.lower():
                    # Extract relevant section
                    lines = content.split('\n')
                    relevant_lines = []
                    
                    for i, line in enumerate(lines):
                        if query_lower in line.lower():
                            # Get context: 2 lines before and 5 lines after
                            start = max(0, i - 2)
                            end = min(len(lines), i + 6)
                            relevant_lines.extend(lines[start:end])
                    
                    if relevant_lines:
                        results.append({
                            "category": category_name,
                            "content": '\n'.join(relevant_lines),
                            "full_content": content
                        })
        
        if not results:
            # No exact match, return most relevant category
            # For shipping-related queries
            if any(word in query_lower for word in ['ship', 'deliver', 'track']):
                file_path = os.path.join(config.KNOWLEDGE_BASE_PATH, 'shipping.md')
                with open(file_path, 'r') as f:
                    return {
                        "success": True,
                        "results": [{
                            "category": "shipping",
                            "content": f.read(),
                            "note": "General shipping information (no exact match found)"
                        }]
                    }
            # For return-related queries
            elif any(word in query_lower for word in ['return', 'refund', 'exchange']):
                file_path = os.path.join(config.KNOWLEDGE_BASE_PATH, 'returns.md')
                with open(file_path, 'r') as f:
                    return {
                        "success": True,
                        "results": [{
                            "category": "returns",
                            "content": f.read(),
                            "note": "General returns information (no exact match found)"
                        }]
                    }
            # For payment-related queries
            elif any(word in query_lower for word in ['pay', 'card', 'upi', 'cod', 'emi']):
                file_path = os.path.join(config.KNOWLEDGE_BASE_PATH, 'payment.md')
                with open(file_path, 'r') as f:
                    return {
                        "success": True,
                        "results": [{
                            "category": "payment",
                            "content": f.read(),
                            "note": "General payment information (no exact match found)"
                        }]
                    }
            else:
                return {
                    "success": False,
                    "error": "No relevant information found. Please rephrase your question or contact support."
                }
        
        return {
            "success": True,
            "results": results
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Knowledge base error: {str(e)}"
        }
