from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import json
from datetime import datetime
from typing import Dict, Any, List
import logging

# Import from main.py
from main import get_runner, get_agent, get_session_service

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get runner and session service from main.py
runner = get_runner()
agent = get_agent()
session_service = get_session_service()

# In-memory storage for sessions (for demo purposes)
# In production, use Redis or a database
active_sessions: Dict[str, Dict[str, Any]] = {}

print("✅ Flask API initialized with ADK Runner")

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Hybrid Multi-Agent Support System",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/chat/start', methods=['POST'])
def start_chat():
    """
    Initialize a new chat session
    
    Request body:
    {
        "user_id": "optional_user_id"
    }
    
    Returns:
    {
        "session_id": "uuid",
        "user_id": "uuid",
        "message": "Session created"
    }
    """
    try:
        data = request.json or {}
        
        # Generate IDs
        session_id = str(uuid.uuid4())
        user_id = data.get('user_id', str(uuid.uuid4()))
        
        # Store session info
        active_sessions[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "message_count": 0,
            "conversation_history": []
        }
        
        logger.info(f"New session created: {session_id} for user: {user_id}")
        
        return jsonify({
            "session_id": session_id,
            "user_id": user_id,
            "message": "Chat session created successfully",
            "timestamp": datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        return jsonify({
            "error": "Failed to create session",
            "details": str(e)
        }), 500


@app.route('/api/chat/message', methods=['POST'])
def send_message():
    """
    Send a message to the support agent
    
    Request body:
    {
        "session_id": "required_session_id",
        "user_id": "required_user_id",
        "message": "User's message text",
        "metadata": {  // Optional
            "source": "web/mobile/api",
            "user_info": {}
        }
    }
    
    Returns:
    {
        "agent_response": "Agent's reply",
        "session_id": "uuid",
        "timestamp": "iso_timestamp",
        "metadata": {
            "tools_used": [...],
            "escalation_status": "none/pending/escalated"
        }
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        session_id = data.get('session_id')
        user_id = data.get('user_id')
        message = data.get('message')
        
        if not all([session_id, user_id, message]):
            return jsonify({
                "error": "Missing required fields",
                "required": ["session_id", "user_id", "message"]
            }), 400
        
        # Check if session exists
        if session_id not in active_sessions:
            return jsonify({
                "error": "Invalid session_id",
                "message": "Session not found. Please start a new chat."
            }), 404
        
        # Verify user_id matches session
        if active_sessions[session_id]["user_id"] != user_id:
            return jsonify({
                "error": "Invalid user_id for this session"
            }), 403
        
        logger.info(f"Processing message for session {session_id}: {message[:50]}...")
        
        # Run the agent
        response = runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=message
        )
        
        # Update session info
        active_sessions[session_id]["message_count"] += 1
        active_sessions[session_id]["last_activity"] = datetime.now().isoformat()
        active_sessions[session_id]["conversation_history"].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        active_sessions[session_id]["conversation_history"].append({
            "role": "agent",
            "content": response.agent_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Extract metadata from response
        metadata = {
            "tools_used": getattr(response, 'tools_used', []),
            "escalation_status": "none"  # Will be enhanced based on agent response
        }
        
        # Check if escalation mentioned in response
        if "escalat" in response.agent_response.lower():
            metadata["escalation_status"] = "pending"
        
        logger.info(f"Response generated for session {session_id}")
        
        return jsonify({
            "agent_response": response.agent_response,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata,
            "message_count": active_sessions[session_id]["message_count"]
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({
            "error": "Failed to process message",
            "details": str(e)
        }), 500


@app.route('/api/chat/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """
    Get conversation history for a session
    
    Returns:
    {
        "session_id": "uuid",
        "conversation_history": [...],
        "message_count": 10,
        "created_at": "iso_timestamp"
    }
    """
    try:
        if session_id not in active_sessions:
            return jsonify({
                "error": "Session not found"
            }), 404
        
        session_data = active_sessions[session_id]
        
        return jsonify({
            "session_id": session_id,
            "user_id": session_data["user_id"],
            "conversation_history": session_data.get("conversation_history", []),
            "message_count": session_data.get("message_count", 0),
            "created_at": session_data.get("created_at"),
            "last_activity": session_data.get("last_activity")
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return jsonify({
            "error": "Failed to fetch conversation history",
            "details": str(e)
        }), 500


@app.route('/api/chat/end/<session_id>', methods=['POST'])
def end_chat(session_id):
    """
    End a chat session
    
    Returns:
    {
        "message": "Session ended",
        "session_id": "uuid",
        "summary": {...}
    }
    """
    try:
        if session_id not in active_sessions:
            return jsonify({
                "error": "Session not found"
            }), 404
        
        # Get session summary before deletion
        session_data = active_sessions[session_id]
        summary = {
            "total_messages": session_data.get("message_count", 0),
            "duration": session_data.get("created_at"),
            "ended_at": datetime.now().isoformat()
        }
        
        # Remove session
        del active_sessions[session_id]
        
        logger.info(f"Session {session_id} ended")
        
        return jsonify({
            "message": "Chat session ended successfully",
            "session_id": session_id,
            "summary": summary
        }), 200
        
    except Exception as e:
        logger.error(f"Error ending session: {str(e)}")
        return jsonify({
            "error": "Failed to end session",
            "details": str(e)
        }), 500


@app.route('/api/sessions/active', methods=['GET'])
def get_active_sessions():
    """
    Get all active sessions (admin endpoint)
    
    Returns:
    {
        "active_sessions": 5,
        "sessions": [...]
    }
    """
    try:
        sessions_list = [
            {
                "session_id": sid,
                "user_id": data["user_id"],
                "message_count": data.get("message_count", 0),
                "created_at": data.get("created_at"),
                "last_activity": data.get("last_activity")
            }
            for sid, data in active_sessions.items()
        ]
        
        return jsonify({
            "active_sessions": len(sessions_list),
            "sessions": sessions_list,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching active sessions: {str(e)}")
        return jsonify({
            "error": "Failed to fetch active sessions",
            "details": str(e)
        }), 500


@app.route('/api/escalation/confirm', methods=['POST'])
def confirm_escalation():
    """
    Confirm or reject an escalation request (human-in-the-loop)
    
    Request body:
    {
        "session_id": "uuid",
        "confirmed": true/false,
        "agent_id": "optional_agent_id"
    }
    
    Returns:
    {
        "status": "confirmed/rejected",
        "message": "..."
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        session_id = data.get('session_id')
        confirmed = data.get('confirmed', False)
        agent_id = data.get('agent_id')
        
        if not session_id:
            return jsonify({"error": "session_id is required"}), 400
        
        # In a real implementation, this would interact with the tool_context
        # For now, we'll store the confirmation status
        
        logger.info(f"Escalation {'confirmed' if confirmed else 'rejected'} for session {session_id}")
        
        return jsonify({
            "status": "confirmed" if confirmed else "rejected",
            "message": f"Escalation {'approved' if confirmed else 'rejected'} successfully",
            "session_id": session_id,
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error confirming escalation: {str(e)}")
        return jsonify({
            "error": "Failed to confirm escalation",
            "details": str(e)
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "message": str(error)
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": str(error)
    }), 500


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 FLASK API SERVER STARTING")
    print("="*60)
    print("📍 Server: http://localhost:5000")
    print("📡 Endpoints:")
    print("   POST   /api/chat/start")
    print("   POST   /api/chat/message")
    print("   GET    /api/chat/history/<session_id>")
    print("   POST   /api/chat/end/<session_id>")
    print("   GET    /api/sessions/active")
    print("   POST   /api/escalation/confirm")
    print("   GET    /health")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )