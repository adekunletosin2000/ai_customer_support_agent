# 🚀 Hybrid Multi-Agent Support System

A production-ready customer support system combining Google ADK (Agent Development Kit) with AI orchestration for intelligent, multi-tool agent workflows.

## 📋 Features

- ✅ **7 AI-Powered Tools**: Intent detection, issue classification, sentiment analysis, knowledge search, troubleshooting generation, escalation check, and human escalation
- ✅ **Human-in-the-Loop**: Seamless escalation to human agents when needed
- ✅ **RESTful API**: Flask-based API ready for React frontend integration
- ✅ **Session Management**: Maintains conversation context across multiple interactions
- ✅ **Real-time Analysis**: Processes customer sentiment, priority, and intent in real-time
- ✅ **Extensible Architecture**: Easy to add new tools and capabilities

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   Flask API     │ ◄── app.py (REST endpoints)
│   (app.py)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ADK Runner +   │ ◄── main.py (Agent logic + Tools)
│  Agent Logic    │
│   (main.py)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Google Gemini  │
│   AI Models     │
└─────────────────┘
```

## 📁 File Structure

```
project/
├── main.py              # Agent logic, tools, and ADK configuration
├── app.py               # Flask REST API server
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create from .env.example)
├── .env.example         # Environment template
└── README.md           # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9+
- Google AI API Key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

### 2. Installation

```bash
# Clone the repository
git clone <your-repo>
cd <your-repo>

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Google API key
GOOGLE_API_KEY=your_actual_api_key_here
```

### 4. Run the System

#### Option A: Run Backend Only (for testing)

```bash
# Test the agent logic
python main.py

# Or run the Flask API
python app.py
```

#### Option B: Run for Production

```bash
# Using gunicorn (recommended for production)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

The API will be available at `http://localhost:5000`

## 📡 API Endpoints

### Health Check
```http
GET /health
```

### Start Chat Session
```http
POST /api/chat/start
Content-Type: application/json

{
  "user_id": "optional_user_id"
}
```

### Send Message
```http
POST /api/chat/message
Content-Type: application/json

{
  "session_id": "uuid",
  "user_id": "uuid",
  "message": "My internet is not working!"
}
```

### Get Chat History
```http
GET /api/chat/history/<session_id>
```

### End Chat Session
```http
POST /api/chat/end/<session_id>
```

### Get Active Sessions (Admin)
```http
GET /api/sessions/active
```

### Confirm Escalation (Human-in-the-Loop)
```http
POST /api/escalation/confirm
Content-Type: application/json

{
  "session_id": "uuid",
  "confirmed": true,
  "agent_id": "optional_agent_id"
}
```

## 🛠️ Agent Workflow

The agent follows this sequence for every customer message:

1. **🎯 Intent Detection**: Classifies the message intent (technical_support, billing_inquiry, etc.)
2. **📋 Issue Classification**: Categorizes the issue and determines priority
3. **💭 Sentiment Analysis**: Analyzes customer emotion and urgency
4. **🔍 Knowledge Search**: Searches internal knowledge base for solutions
5. **🛠️ Troubleshooting**: Generates step-by-step resolution guide
6. **⚠️ Escalation Check**: Determines if human intervention is needed
7. **🚨 Human Escalation**: Transfers to human agent if necessary (human-in-the-loop)

## 🧪 Testing

### Test the Agent Logic
```bash
python main.py
```

This will run test cases with sample customer messages.

### Test the API with cURL

```bash
# Start a session
curl -X POST http://localhost:5000/api/chat/start \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'

# Send a message (replace with actual session_id and user_id)
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "user_id": "YOUR_USER_ID",
    "message": "My internet is not working!"
  }'
```

### Test with Postman

Import the following endpoints into Postman:
- Base URL: `http://localhost:5000`
- Use the endpoints documented above

## 🔧 Configuration

### Retry Configuration
The system uses exponential backoff for API retries:
```python
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)
```

### Knowledge Base
Edit the knowledge base in `main.py`:
```python
self.knowledge_base = {
    "internet_issues": [...],
    "billing_issues": [...],
    "app_problems": [...]
}
```

### AI Model
Change the Gemini model in `main.py`:
```python
model = genai.GenerativeModel('gemini-1.5-flash')  # or gemini-1.5-pro
```

## 🔌 React Frontend Integration

### Example React Code

```javascript
// Start a chat session
const startChat = async () => {
  const response = await fetch('http://localhost:5000/api/chat/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: 'user123' })
  });
  const data = await response.json();
  return { sessionId: data.session_id, userId: data.user_id };
};

// Send a message
const sendMessage = async (sessionId, userId, message) => {
  const response = await fetch('http://localhost:5000/api/chat/message', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      user_id: userId,
      message: message
    })
  });
  const data = await response.json();
  return data.agent_response;
};
```

## 📊 Monitoring & Logging

The system includes built-in logging:
```python
logger.info(f"New session created: {session_id}")
logger.error(f"Error processing message: {str(e)}")
```

View logs in the console when running the Flask app.

## 🚀 Production Deployment

### Using Docker (Recommended)

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t support-system .
docker run -p 5000:5000 --env-file .env support-system
```

### Using Cloud Platforms

- **Google Cloud Run**: Deploy directly from GitHub
- **AWS Elastic Beanstalk**: Use the EB CLI
- **Heroku**: Push to Heroku git remote

## 🔒 Security Considerations

1. **API Key Protection**: Never commit `.env` file to version control
2. **CORS Configuration**: Update `CORS_ORIGINS` in production
3. **Rate Limiting**: Add rate limiting middleware (e.g., Flask-Limiter)
4. **Authentication**: Implement JWT or OAuth for production
5. **HTTPS**: Always use HTTPS in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'google.adk'`
- **Solution**: Install google-adk: `pip install google-adk`

**Issue**: `API Key Error`
- **Solution**: Check your `.env` file and ensure `GOOGLE_API_KEY` is set correctly

**Issue**: `CORS Error in React`
- **Solution**: Ensure Flask-CORS is installed and configured correctly in `app.py`

**Issue**: `Session Not Found`
- **Solution**: Make sure to call `/api/chat/start` before sending messages

## 📧 Support

For questions or issues:
- Open an issue on GitHub
- Contact: your-email@example.com

## 🎉 Acknowledgments

- Google ADK Team for the Agent Development Kit
- Google AI for Gemini models
- Flask and React communities

---

**Built with ❤️ using Google ADK, Flask, and Gemini AI**