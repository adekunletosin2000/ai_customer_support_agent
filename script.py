import os

structure = [
    # Backend
    "backend/app",
    "backend/app/routers",
    "backend/app/agents",
    "backend/app/utils",
    "backend/app/models",
    "backend/tests",

    # Frontend
    "frontend/src/pages",
    "frontend/src/components",
    "frontend/src/styles",
    "frontend/src/utils",
    "frontend/public",

    # Data
    "data/knowledge_base",
    "data/embeddings",

    # Docs & Demo
    "docs",
    "demo/sample_inputs"
]

files = [
    # Backend main files
    "backend/app/main.py",
    "backend/app/orchestrator.py",
    "backend/app/config.py",
    "backend/app/requirements.txt",

    # Router files
    "backend/app/routers/classify.py",
    "backend/app/routers/search.py",
    "backend/app/routers/respond.py",
    "backend/app/routers/sentiment.py",
    "backend/app/routers/troubleshoot.py",
    "backend/app/routers/summarize.py",
    "backend/app/routers/escalate.py",
    "backend/app/routers/analytics.py",

    # Agent files
    "backend/app/agents/classifier_agent.py",
    "backend/app/agents/intent_agent.py",
    "backend/app/agents/sentiment_agent.py",
    "backend/app/agents/knowledge_agent.py",
    "backend/app/agents/response_agent.py",
    "backend/app/agents/troubleshooting_agent.py",
    "backend/app/agents/escalation_agent.py",
    "backend/app/agents/summarization_agent.py",
    "backend/app/agents/analytics_agent.py",
    "backend/app/agents/user_profile_agent.py",
    "backend/app/agents/orchestrator_agent.py",

    # Utils
    "backend/app/utils/embeddings.py",
    "backend/app/utils/vectorstore.py",
    "backend/app/utils/prompts.py",
    "backend/app/utils/helpers.py",

    # Models
    "backend/app/models/request_models.py",
    "backend/app/models/response_models.py",
    "backend/app/models/knowledge_schema.py",

    # Tests
    "backend/tests/test_agents.py",
    "backend/tests/test_api.py",

    # Frontend
    "frontend/src/pages/index.jsx",
    "frontend/src/pages/demo.jsx",
    "frontend/src/components/ChatWindow.jsx",
    "frontend/src/components/MessageBubble.jsx",
    "frontend/src/components/AgentTimeline.jsx",
    "frontend/src/components/LoadingIndicator.jsx",
    "frontend/src/components/Header.jsx",
    "frontend/src/styles/globals.css",
    "frontend/src/styles/chat.css",
    "frontend/src/utils/api.js",
    "frontend/src/config.js",

    # Data files
    "data/knowledge_base/faq.json",
    "data/knowledge_base/product_guides.json",
    "data/knowledge_base/troubleshooting_steps.json",

    # Docs
    "docs/architecture_diagram.png",
    "docs/agents_overview.md",
    "docs/api_endpoints.md",
    "docs/prompt_library.md",
    "docs/pitch_deck.pptx",

    # Demo
    "demo/sample_inputs/lost_password.json",
    "demo/sample_inputs/billing_issue.json",
    "demo/sample_inputs/app_not_loading.json",

    # Main README
    "README.md"
]

# CREATE FOLDERS
for path in structure:
    os.makedirs(path, exist_ok=True)

# CREATE FILES
for file in files:
    with open(file, "w") as f:
        f.write("")

print("Project structure created successfully!")
