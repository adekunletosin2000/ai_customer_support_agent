# 📁 Project Structure & File Overview

## Complete File List

```
hybrid-support-system/
│
├── 🐍 Backend (Python)
│   ├── main.py                  # Agent logic, tools, orchestrator
│   ├── app.py                   # Flask REST API server
│   ├── test_api.py              # API testing script
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables (create this)
│   └── .env.example             # Environment template
│
├── ⚛️ Frontend (React)
│   └── ChatComponent.jsx        # Example React chat component
│
└── 📚 Documentation
    ├── README.md                # Complete documentation
    └── PROJECT_STRUCTURE.md     # This file
```

---

## 📄 File Descriptions

### 1. **main.py** - Agent Logic & Orchestrator
**Purpose**: Core agent system with AI-powered tools  
**Key Components**:
- `EnhancedAgentTools` class with 7 AI tools
- Google ADK Agent configuration
- Tool definitions (intent, classification, sentiment, etc.)
- Human-in-the-loop escalation logic
- Session management
- Export functions for Flask

**When to modify**:
- Add new tools/capabilities
- Change agent behavior
- Modify knowledge base
- Update AI model configurations

---

### 2. **app.py** - Flask REST API
**Purpose**: HTTP API server for frontend communication  
**Key Components**:
- 7 REST endpoints
- Session management
- Error handling
- CORS configuration
- Request/response validation

**Endpoints**:
```
GET    /health
POST   /api/chat/start
POST   /api/chat/message
GET    /api/chat/history/<session_id>
POST   /api/chat/end/<session_id>
GET    /api/sessions/active
POST   /api/escalation/confirm
```

**When to modify**:
- Add new API endpoints
- Change request/response formats
- Implement authentication
- Add rate limiting

---

### 3. **test_api.py** - Testing Script
**Purpose**: Automated testing of all API endpoints  
**Key Features**:
- Complete test suite
- Tests all endpoints
- Provides detailed output
- Error handling

**How to use**:
```bash
# Make sure Flask server is running first
python app.py

# In another terminal
python test_api.py
```

---

### 4. **requirements.txt** - Dependencies
**Purpose**: Python package dependencies  
**Key Packages**:
- `flask` - Web framework
- `flask-cors` - CORS support
- `google-generativeai` - Gemini AI
- `google-adk` - Agent Development Kit
- `python-dotenv` - Environment variables

**How to use**:
```bash
pip install -r requirements.txt
```

---

### 5. **.env** - Environment Variables
**Purpose**: Store sensitive configuration  
**Required Variables**:
```bash
GOOGLE_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

**⚠️ IMPORTANT**: 
- Never commit this file to Git
- Create from `.env.example`
- Add to `.gitignore`

---

### 6. **.env.example** - Environment Template
**Purpose**: Template for environment variables  
**How to use**:
```bash
cp .env.example .env
# Then edit .env with your actual values
```

---

### 7. **ChatComponent.jsx** - React Frontend
**Purpose**: Example React component for chat UI  
**Key Features**:
- Session management
- Message display
- Real-time typing indicator
- Escalation status display
- Responsive design

**How to integrate**:
```jsx
import ChatComponent from './ChatComponent';

function App() {
  return <ChatComponent />;
}
```

---

### 8. **README.md** - Documentation
**Purpose**: Complete project documentation  
**Sections**:
- Quick start guide
- API documentation
- Configuration options
- Deployment instructions
- Troubleshooting

---

## 🔄 Data Flow

```
┌─────────────────┐
│  React Frontend │
│ ChatComponent   │
└────────┬────────┘
         │ 1. POST /api/chat/message
         │    { session_id, user_id, message }
         ▼
┌─────────────────┐
│   Flask API     │
│    app.py       │
│                 │
│  - Validates    │
│  - Routes       │
│  - Logs         │
└────────┬────────┘
         │ 2. runner.run()
         ▼
┌─────────────────┐
│  ADK Agent      │
│   main.py       │
│                 │
│  🎯 detect_intent
│  📋 classify_issue
│  💭 analyze_sentiment
│  🔍 search_knowledge_base
│  🛠️ generate_troubleshooting
│  ⚠️ check_escalation
│  🚨 escalate_to_human
└────────┬────────┘
         │ 3. AI calls
         ▼
┌─────────────────┐
│  Gemini API     │
│  Google AI      │
└────────┬────────┘
         │ 4. AI responses
         ▼
┌─────────────────┐
│  Flask API      │
│  Returns JSON   │
└────────┬────────┘
         │ 5. Response
         ▼
┌─────────────────┐
│  React Frontend │
│  Displays chat  │
└─────────────────┘
```

---

## 🚀 Quick Start Commands

### Setup
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API key

# 4. Test agent logic
python main.py

# 5. Start Flask server
python app.py

# 6. Test API (in new terminal)
python test_api.py
```

### React Frontend
```bash
# In your React project
npm install

# Copy ChatComponent.jsx to your src folder
# Import and use in your app

npm start
```

---

## 🎯 Development Workflow

### Adding a New Tool

1. **In main.py**:
```python
def new_tool(self, param: str) -> str:
    """Tool description"""
    # Your logic here
    return json.dumps(result)

# Create FunctionTool
new_tool_func = FunctionTool(enhanced_tools.new_tool)

# Add to agent tools list
tools=[..., new_tool_func]
```

2. **Update agent instruction**:
```python
instruction="""
...
8. 🆕 new_tool - Description
...
"""
```

### Adding a New API Endpoint

1. **In app.py**:
```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    """Endpoint description"""
    try:
        # Your logic
        return jsonify({...}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

2. **Test it**:
```bash
curl -X POST http://localhost:5000/api/new-endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

---

## 📊 Monitoring & Debugging

### View Logs
```bash
# Flask logs are in console
python app.py

# For production with gunicorn
gunicorn --log-level debug app:app
```

### Debug Mode
```python
# In app.py, enable debug mode
app.run(debug=True)
```

### Test Individual Tools
```python
# In main.py
if __name__ == "__main__":
    tools = EnhancedAgentTools()
    result = tools.detect_intent("test message")
    print(result)
```

---

## 🔒 Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] API key is not hardcoded
- [ ] CORS is configured for production domains
- [ ] HTTPS is enabled in production
- [ ] Rate limiting is implemented
- [ ] Input validation is in place
- [ ] Error messages don't leak sensitive info

---

## 📦 Deployment Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] Environment variables configured
- [ ] Database/session storage configured (if needed)
- [ ] Logging configured
- [ ] Error handling tested
- [ ] API endpoints documented
- [ ] Frontend build created
- [ ] CORS configured for production
- [ ] Health check endpoint working
- [ ] Monitoring/alerting set up

---

## 🤝 Contributing

1. Create feature branch from `main`
2. Make changes
3. Test locally with `test_api.py`
4. Update documentation if needed
5. Submit pull request

---

## 📞 Support & Resources

- **Google ADK Docs**: https://github.com/google/genai-adk
- **Gemini API Docs**: https://ai.google.dev/docs
- **Flask Docs**: https://flask.palletsprojects.com/
- **React Docs**: https://react.dev/

---

**Last Updated**: November 2024  
**Version**: 1.0.0