"""
VisionSupport AI - Streamlit Chat Interface
Main application file
"""
import streamlit as st
import config
from agents.orchestrator import OrchestratorAgent
from agents.order_tracking import OrderTrackingAgent
from agents.faq import FAQAgent

# Page configuration
st.set_page_config(
    page_title=config.STREAMLIT_PAGE_TITLE,
    page_icon=config.STREAMLIT_PAGE_ICON,
    layout=config.STREAMLIT_LAYOUT
)

# Custom CSS for better chat UI
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .main {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🤖 VisionSupport AI")
st.markdown("*AI-powered customer support with visual intelligence*")

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Hi! I'm VisionSupport AI. I can help you with:\n\n" +
                   "📦 Order tracking and delivery status\n" +
                   "↩️ Returns and refunds\n" +
                   "❓ Shipping, payment, and general FAQs\n" +
                   "📸 Visual product support (coming in Day 3!)\n\n" +
                   "How can I help you today?"
    })

# Initialize agents
if 'orchestrator' not in st.session_state:
    try:
        # Validate config first (will raise error if GEMINI_API_KEY not set)
        config.validate_config()
        st.session_state.orchestrator = OrchestratorAgent()
        st.session_state.order_agent = OrderTrackingAgent()
        st.session_state.faq_agent = FAQAgent()
    except ValueError as e:
        st.error(f"⚠️ Configuration Error: {str(e)}")
        st.info("💡 Please copy `.env.template` to `.env` and add your Gemini API key")
        st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process with orchestrator
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Classify intent
                intent = st.session_state.orchestrator.classify_intent(prompt)
                
                # Route to appropriate agent
                if intent == 'ORDER_TRACKING':
                    result = st.session_state.order_agent.process_query(prompt)
                elif intent == 'FAQ':
                    result = st.session_state.faq_agent.process_query(prompt)
                elif intent == 'GENERAL':
                    # Handle general conversation with Gemini
                    try:
                        import google.generativeai as genai
                        
                        # Configure Gemini
                        genai.configure(api_key=config.GEMINI_API_KEY)
                        model = genai.GenerativeModel(config.GEMINI_MODEL)
                        
                        # Build context from chat history
                        conversation_context = ""
                        if len(st.session_state.messages) > 1:
                            # Get last 3 exchanges for context
                            recent = st.session_state.messages[-6:]
                            for msg in recent:
                                role = "Customer" if msg["role"] == "user" else "Agent"
                                conversation_context += f"{role}: {msg['content']}\n"
                        
                        # Create system prompt
                        system_prompt = f"""You are VisionSupport AI, a friendly e-commerce customer support assistant.

Your capabilities:
- Order tracking and delivery status
- Returns and refunds processing  
- Shipping and payment policy questions
- Product information

Context of conversation so far:
{conversation_context}

Customer's current message: {prompt}

Provide a helpful, conversational response. If they're asking about capabilities, be specific about what you can help with. If it's a greeting, be warm and welcoming. Keep responses concise (2-3 sentences max)."""
                        
                        # Generate response
                        response = model.generate_content(system_prompt)
                        result = {
                            'success': True,
                            'response': response.text
                        }
                    except Exception as e:
                        # Fallback to basic responses if Gemini fails
                        if any(word in prompt.lower() for word in ['hello', 'hi', 'hey']):
                            result = {
                                'success': True,
                                'response': "Hello! 👋 I'm VisionSupport AI. I can help with order tracking, returns, and policy questions. What would you like help with?"
                            }
                        else:
                            result = {
                                'success': True,
                                'response': f"I'm here to help with e-commerce support. You can ask about orders, returns, shipping, or payment policies. (Note: AI service temporarily unavailable - {str(e)})"
                            }
                else:
                    # For other intents, show placeholder (will implement on Day 2-3)
                    result = {
                        'success': True,
                        'response': f"I understand you're asking about {intent}. This feature is coming soon!"
                    }
                
                # Display response
                response_text = result.get('response', 'Sorry, I encountered an error.')
                st.markdown(response_text)
                
                # Add to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text
                })
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    **VisionSupport AI** is an AI-powered customer support agent for e-commerce.
    
    **Features:**
    - 🤖 Multi-agent architecture
    - 👁️ Visual intelligence (Day 3)
    - 🎭 Sentiment analysis (Day 4)
    - 💾 Memory & context awareness
    
    **Status:** Day 1 - Foundation ✅
    """)
    
    st.header("🧪 Test Queries")
    st.markdown("""
    Try asking:
    - "Where's my order ORD12345?"
    - "What's your shipping policy?"
    - "How do I return an item?"
    - "What payment methods do you accept?"
    """)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
