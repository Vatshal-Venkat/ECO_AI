# ECO_AI
# 📘 ECO AI Assistant – Teamcenter ECO Automation (PoC)

The **ECO AI Assistant** is a full-stack **Engineering Change Order automation system** built as a proof of concept.  
It includes:

- **FastAPI backend** (mock Teamcenter + AI services)
- **Streamlit Dashboard** (interactive ECO console)
- **Gemini AI integration** (summaries, impact analysis)
- **Mock Teamcenter logic** (create, promote, impact items)
- **SQLite persistence**
- **ECO Insights Dashboard** (visual analytics)

---

## 🚀 Features

### 🔧 Teamcenter-like ECO Operations
- Create ECO  
- Fetch ECO details  
- Promote / Demote  
- Add / Remove impacted items  
- List all ECOs  
- Mock file attachments  

### 🤖 AI-Powered Processing (Gemini)
- ECO summarization  
- BOM-based impact analysis  
- Weighted risk scoring  

### 📊 Interactive Dashboard (Streamlit)
- KPI cards  
- Multi-ring impact visualization  
- Risk progress gauge  
- Bar & donut charts  
- ECO list explorer  
- Teamcenter action console  

### 🗄️ Local Database (SQLite)
- `eco_master` and `eco_bom` tables  
- Migration-ready structure  

---

## 🏗️ Project Structure

ECO_AI/
│── main.py # FastAPI backend
│── eco_ui.py # Streamlit UI
│── eco_insights_utils.py # Analytics + SVG charts
│── mock_teamcenter.py # Mock Teamcenter server
│── teamcenter_client.py # Real Teamcenter REST client (optional)
│── gemini_client.py # Gemini API wrapper with rate-limit logic
│── db.py # SQLite helper
│── init_db.py # DB initialization
│── eco_ui.css # Custom premium UI theme
│── .env # API keys & config
│── requirements.txt
│── README.md


========================================================


---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone <repo-url>
cd ECO_AI
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows
pip install -r requirements.txt
GOOGLE_API_KEY=your_gemini_api_key

# Required only if using real Teamcenter REST APIs
TC_URL=http://teamcenter.server
TC_USERNAME=username
TC_PASSWORD=password
```

python init_db.py


uvicorn main:app --reload --port 8000

streamlit run eco_ui.py




=========================================================================

❤️ Credits

Developed by Venkat Vatshal

ECO AI Assistant — © 2025

