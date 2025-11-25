# 🤖 VisionSupport AI

> AI-powered customer support agent with visual intelligence and sentiment analysis
>
> **Capstone Project** for Google AI Agents Intensive Course (Nov 2025)  
> **Track:** Enterprise Agents

---

## 🌟 Features

### Core Capabilities
- 🤖 **Multi-Agent Architecture** - Specialized agents for different support tasks
- 📦 **Order Tracking** - Real-time order status and delivery information
- ↩️ **Returns & Refunds** - Automated return processing
- ❓ **FAQ Support** - Instant answers from knowledge base
- 👁️ **Visual Intelligence** (Coming Day 3) - Upload product images for support
- 🎭 **Sentiment Analysis** (Coming Day 4) - Auto-escalates frustrated customers

### Technology Stack
- **Agent Framework:** Google ADK (Agent Development Kit)
- **LLM:** Gemini 2.0 Flash (with Vision API)
- **Frontend:** Streamlit
- **Database:** SQLite
- **Language:** Python 3.11+

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Google Gemini API key ([get one here](https://ai.google.dev/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai_customer_support_agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy template
   cp .env.template .env
   
   # Edit .env and add your Gemini API key
   # GEMINI_API_KEY=your_api_key_here
   ```

5. **Initialize database (already done if you cloned the repo)**
   ```bash
   python data/mock_orders.py
   python data/mock_products.py
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

---

## 🧪 Try These Test Queries

Once the app is running, try asking:

- **Order Tracking:**
  - "Where's my order ORD12345?"
  - "Track order 12346"
  - "What's the status of my order #12347?"

- **FAQ Support:**
  - "What are your shipping options?"
  - "How do I return an item?"
  - "What payment methods do you accept?"
  - "Do you offer EMI?"

---

## 📁 Project Structure

```
ai_customer_support_agent/
├── agents/                 # Specialized AI agents
│   ├── orchestrator.py    # Intent classification & routing
│   ├── order_tracking.py  # Order status queries
│   └── faq.py             # Knowledge base Q&A
│
├── tools/                  # Custom ADK tools
│   ├── order_db.py        # Database queries
│   └── knowledge_base.py  # FAQ search
│
├── data/                   # Mock data & database
│   ├── ecommerce.db       # SQLite database
│   ├── mock_orders.py     # Order data generator
│   ├── mock_products.py   # Product data generator
│   └── knowledge_base/    # FAQ markdown files
│       ├── shipping.md
│       ├── returns.md
│       └── payment.md
│
├── app.py                  # Streamlit UI
├── config.py               # Configuration & constants
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (not in git)
```

---

## 🏗️ Architecture

### Multi-Agent System

```
User Query
    ↓
Orchestrator Agent (Intent Classification)
    ↓
    ├─→ Order Tracking Agent → Order Database
    ├─→ FAQ Agent → Knowledge Base
    ├─→ Returns Agent (Day 3) → Returns Processing
    ├─→ Visual Agent (Day 3) → Gemini Vision API
    └─→ Sentiment Monitor (Day 4) → Human Escalation
```

### Current Status (Day 1 ✅)
- ✅ Project structure setup
- ✅ Database with 20 orders, 20 products
- ✅ 3 FAQ pages (shipping, returns, payment)
- ✅ Basic agents (Orchestrator, Order Tracking, FAQ)
- ✅ Streamlit chat interface
- ⏳ Gemini integration (add API key needed)
- ⏳ Visual intelligence (Day 3)
- ⏳ Sentiment analysis (Day 4)

---

## 🛣️ Roadmap

| Day | Focus | Status |
|-----|-------|--------|
| **Day 1** | Foundation & Setup | ✅ **COMPLETE** |
| **Day 2** | Core Agent Implementation | ⏳ Planned |
| **Day 3** | Visual Intelligence ⭐ | ⏳ Planned |
| **Day 4** | Sentiment & Memory | ⏳ Planned |
| **Day 5** | Polish & Testing | ⏳ Planned |
| **Day 6** | Documentation & Video | ⏳ Planned |
| **Day 7** | Final Submission | ⏳ Planned |

**Submission Deadline:** Dec 1, 2025, 11:59 AM PT

---

## 📊 Database Schema

### Orders Table
```sql
orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    customer_name TEXT,
    customer_email TEXT,
    order_date TEXT,
    status TEXT,
    total_amount REAL,
    shipping_address TEXT,
    tracking_number TEXT,
    last_scan_location TEXT,
    estimated_delivery TEXT,
    items TEXT
)
```

### Products Table
```sql
products (
    product_id TEXT PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    description TEXT,
    in_stock BOOLEAN,
    image_url TEXT,
    rating REAL
)
```

---

## 🔧 Configuration

Edit `config.py` to customize:
- Gemini model selection
- Database paths
- Agent timeouts
- Sentiment thresholds
- UI settings

---

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found" error
- Make sure you've copied `.env.template` to `.env`
- Add your actual API key to the `.env` file
- Restart the Streamlit app

### Database not found
```bash
python data/mock_orders.py
python data/mock_products.py
```

### Dependencies issues
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📝 License

This project is created for the Google AI Agents Intensive Course Capstone.

---

## 🙏 Acknowledgments

- Google AI Agents Team for the amazing course
- Kaggle for hosting the competition
- Gemini API team

---

**Built with ❤️ for the Google AI Agents Intensive Capstone**
