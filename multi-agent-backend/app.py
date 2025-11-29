from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import json
from datetime import datetime
from typing import Dict, Any, List
import logging
import sys
import os
import warnings
import threading

# CRITICAL FIX 1: Suppress runtime warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", message=".*Event loop is closed.*")

# CRITICAL FIX 2: Set event loop policy for Windows
if sys.platform == 'win32':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Import from main.py  
from main import get_runner, get_agent, get_session_service

# Import Google Genai types
try:
    from google.genai.types import Part, Content
    USE_GENAI_TYPES = True
    print("✅ Google Genai types imported successfully")
except ImportError:
    USE_GENAI_TYPES = False
    print("⚠️ Could not import google.genai.types")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Suppress excessive logging from dependencies
logging.getLogger("httpcore").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("anyio").setLevel(logging.CRITICAL)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Get runner and session service from main.py
runner = get_runner()
agent = get_agent()
session_service = get_session_service()

# In-memory storage for sessions
active_sessions: Dict[str, Dict[str, Any]] = {}

print("✅ Flask API initialized with ADK Runner")


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Hybrid Multi-Agent Support System",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(active_sessions)
    }), 200


@app.route('/api/chat/start', methods=['POST'])
def start_chat():
    """Initialize a new chat session"""
    try:
        data = request.json or {}
        
        # Generate IDs
        session_id = str(uuid.uuid4())
        user_id = data.get('user_id', str(uuid.uuid4()))
        
        # CRITICAL: Register session with ADK's session service
        # This must be done synchronously in the main thread
        try:
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(session_service.create_session(
                    app_name="multi_agent_support",
                    user_id=user_id,
                    session_id=session_id
                ))
                logger.info(f"✅ ADK session registered: {session_id}")
            finally:
                loop.close()
        except Exception as session_error:
            logger.warning(f"⚠️ ADK session registration warning: {session_error}")
            # Continue anyway - we'll track in active_sessions
        
        # Store in active_sessions
        active_sessions[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "message_count": 0,
            "conversation_history": []
        }
        
        logger.info(f"✅ New session created: {session_id} for user: {user_id}")
        
        return jsonify({
            "session_id": session_id,
            "user_id": user_id,
            "message": "Chat session created successfully",
            "timestamp": datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        logger.error(f"❌ Error creating session: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": "Failed to create session",
            "details": str(e)
        }), 500


@app.route('/api/chat/message', methods=['POST'])
def send_message():
    """Send a message to the support agent"""
    try:
        data = request.json
        
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
        
        # Check if session exists - with auto-recovery
        if session_id not in active_sessions:
            logger.warning(f"⚠️ Session {session_id} not found, attempting recovery...")
            
            # Register with ADK session service
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(session_service.create_session(
                        app_name="multi_agent_support",
                        user_id=user_id,
                        session_id=session_id
                    ))
                    logger.info(f"✅ ADK session registered during recovery: {session_id}")
                finally:
                    loop.close()
            except Exception as recovery_error:
                logger.warning(f"⚠️ Session recovery warning: {recovery_error}")
            
            # Store in active_sessions
            active_sessions[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "message_count": 0,
                "conversation_history": [],
                "recovered": True
            }
            logger.info(f"✅ Session {session_id} recovered")
        
        # Verify user_id matches session
        if active_sessions[session_id]["user_id"] != user_id:
            return jsonify({
                "error": "Invalid user_id for this session"
            }), 403
        
        logger.info(f"📨 Processing message for session {session_id[:8]}...: {message[:50]}...")
        
        # Create proper message object with role attribute
        if USE_GENAI_TYPES:
            message_obj = Content(
                role="user",
                parts=[Part(text=message)]
            )
        else:
            class SimpleMessage:
                def __init__(self, text):
                    self.role = "user"
                    self.parts = [type('Part', (), {'text': text})()]
            message_obj = SimpleMessage(message)
        
        # Run the agent - let the event loop errors print but don't crash
        final_response = None
        responses = []
        
        try:
            # Call runner.run() - it will work despite the event loop cleanup errors
            for response_event in runner.run(
                user_id=user_id,
                session_id=session_id,
                new_message=message_obj
            ):
                responses.append(response_event)
                logger.info(f"📦 Event #{len(responses)}: {type(response_event).__name__}")
            
            final_response = responses[-1] if responses else None
            logger.info(f"✅ Collected {len(responses)} response events. Using final event for response extraction.")
            
        except Exception as e:
            # Log but don't fail - the responses list might still have valid data
            logger.warning(f"⚠️ Exception during runner execution: {e}")
            final_response = responses[-1] if responses else None
        
        # Extract the agent's text response with comprehensive fallbacks
        agent_response_text = ""
        if final_response:
            try:
                # Log the response structure for debugging
                logger.info(f"Response type: {type(final_response)}")
                
                # Try multiple extraction strategies
                if hasattr(final_response, 'content'):
                    content = final_response.content
                    if hasattr(content, 'parts') and content.parts:
                        # Extract text from parts
                        text_parts = []
                        for part in content.parts:
                            if hasattr(part, 'text') and part.text:
                                text_parts.append(str(part.text))
                        agent_response_text = ' '.join(text_parts)
                    elif isinstance(content, str):
                        agent_response_text = content
                    elif hasattr(content, 'text'):
                        agent_response_text = str(content.text)
                
                # Fallback strategies
                if not agent_response_text and hasattr(final_response, 'response'):
                    agent_response_text = str(final_response.response)
                
                if not agent_response_text and hasattr(final_response, 'agent_response'):
                    agent_response_text = str(final_response.agent_response)
                
                if not agent_response_text and hasattr(final_response, 'text'):
                    agent_response_text = str(final_response.text)
                
                # Clean up the response
                if agent_response_text:
                    agent_response_text = agent_response_text.strip()
                    logger.info(f"Extracted response: {agent_response_text[:100]}...")
                else:
                    logger.warning(f"Could not extract text from response")
                    
            except Exception as extract_error:
                logger.error(f"Error extracting response text: {extract_error}")
                agent_response_text = ""
        else:
            logger.warning("No final response received from agent")
        
        # Fallback message only if extraction truly failed
        if not agent_response_text or len(agent_response_text.strip()) == 0:
            agent_response_text = "I apologize, but I encountered an issue processing your request. Could you please try rephrasing your question?"
            logger.warning("Using fallback response message")
        
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
            "content": agent_response_text,
            "timestamp": datetime.now().isoformat()
        })
        message_count = active_sessions[session_id]["message_count"]
        
        # Extract metadata
        metadata = {
            "tools_used": [],
            "escalation_status": "none"
        }
        
        if "escalat" in agent_response_text.lower():
            metadata["escalation_status"] = "pending"
        
        logger.info(f"✅ Response generated for session {session_id[:8]}...")
        
        return jsonify({
            "agent_response": agent_response_text,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata,
            "message_count": message_count
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error processing message: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": "Failed to process message",
            "details": str(e)
        }), 500


@app.route('/api/chat/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """Get conversation history for a session"""
    try:
        if session_id not in active_sessions:
            return jsonify({"error": "Session not found"}), 404
        
        session_data = active_sessions[session_id].copy()
        
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
    """End a chat session"""
    try:
        if session_id not in active_sessions:
            return jsonify({"error": "Session not found"}), 404
        
        session_data = active_sessions[session_id]
        summary = {
            "total_messages": session_data.get("message_count", 0),
            "duration": session_data.get("created_at"),
            "ended_at": datetime.now().isoformat()
        }
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
    """Get all active sessions (admin endpoint)"""
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
    print("   GET    /health")
    print("="*60)
    print("⚙️  Configuration:")
    print("   - Event loop policy: WindowsSelectorEventLoop")
    print("   - Runtime warnings: SUPPRESSED")
    print("   - Debug mode: OFF (production)")
    print("⚠️  Note: Event loop cleanup errors may appear")
    print("   (These are harmless and don't affect functionality)")
    print("="*60 + "\n")
    
    # Production-ready configuration
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True,
        use_reloader=False
    )