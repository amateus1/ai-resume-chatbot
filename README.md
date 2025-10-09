markdown

# 🤖 AI Resume Chatbot

**`ai-resume-chatbot`** is an AI-powered, location-aware virtual assistant that represents **Al Mateus** — a global Agentic, LLM Engineering, MLOps and DevSecOps consultant — in an interactive, conversational format. Built using **Streamlit**, it dynamically serves resume information and switches between **OpenAI** and **DeepSeek** depending on user region (global vs. China).

[![CI/CD](https://github.com/yourusername/ai-resume-chatbot/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/ai-resume-chatbot/actions)
[![Streamlit App](https://img.shields.io/badge/Live%20App-Streamlit-orange?logo=streamlit)](https://yourapp.streamlit.app)

---

## 🧠 Features

- 🌍 **AI Resume Agent**: Chat with Al Mateus' professional experience via LLM
- 🔁 **Smart LLM Switching**: Uses OpenAI outside China, DeepSeek inside
- 🔒 **Secure Resume Files**: Loaded privately from AWS S3 (not public)
- 📬 **Notifications**: Resend for email, Pushover for mobile alerts
- 🔐 **Secrets Managed**: Streamlit Secrets Manager handles all credentials
- ⚙️ **CI/CD with GitHub Actions**: Linting, secret scanning, LLM API testing
- 🗣️ **Multi-language Support**: English, Chinese, and Spanish interfaces
- 💬 **Real-time Streaming**: Live typing responses for natural conversation
- 🧠 **Conversation Memory**: Remembers context and user details within session
- 💾 **Persistent Chat Storage**: All conversations saved to S3 as JSON files
- 📧 **Smart Email Capture**: Automatic email detection in chat + optional prompts
- 🎨 **Custom UI Styling**: Optimized chat bubbles and responsive design
- 🔄 **Session Management**: Unique session IDs for tracking conversations
- 🌐 **Auto Keep-alive**: Silent ping system to maintain app responsiveness

---

## 🛠️ Tech Stack

| Layer            | Tech                         |
|------------------|------------------------------|
| Frontend         | Streamlit                    |
| LLM APIs         | OpenAI GPT-4o, DeepSeek Chat |
| Backend Logic    | Python, PDF parsing, Boto3   |
| File Storage     | AWS S3 (private)             |
| Notifications    | Resend, Pushover             |
| CI/CD            | GitHub Actions               |
| Data Persistence | JSON files in S3 bucket      |
| Session Management| UUID-based tracking          |

---

## 🚀 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/ai-resume-chatbot.git
cd ai-resume-chatbot

2. Install Requirements
bash

pip install -r requirements.txt

3. Set Up Environment Variables

Add your credentials via environment variables or in Streamlit Cloud Secrets:
env

OPENAI_API_KEY = "sk-..."
DEEPSEEK_API_KEY = "..."
AWS_ACCESS_KEY_ID = "..."
AWS_SECRET_ACCESS_KEY = "..."
AWS_REGION = "us-east-1"
S3_BUCKET = "your-bucket-name"
LINKEDIN_KEY = "me/linkedin.md"
RESEND_API_KEY = "..."
PUSHOVER_TOKEN = "..."
PUSHOVER_USER = "..."

4. Run Locally
bash

streamlit run app.py

📄 Project Structure
text

├── app.py                 # Streamlit frontend with chat interface
├── me_chatbot.py          # Chat logic, API switching & S3 storage
├── requirements.txt       # Python dependencies
├── chats/                 # Local chat storage (development)
├── tests/
│   ├── test_openai.py
│   └── test_deepseek.py
└── .github/workflows/
    └── ci.yml             # GitHub Actions CI/CD pipeline

🔄 Key Capabilities
💬 Smart Chat Features

    Real-time Streaming: Responses appear as they're generated

    Conversation Memory: AI remembers context within the same session

    Multi-language UI: Switch between English, Chinese, and Spanish

    Contextual Prompts: Menu buttons for quick access to projects, experience, skills

💾 Data Management

    S3 Chat Storage: All conversations saved to ai-resume-chatbot/chats/ as JSON

    Session Tracking: Unique UUIDs for each chat session

    Structured Data: JSON format includes timestamps, language, and full history

🎨 User Experience

    Custom Styling: Optimized chat bubbles and responsive design

    Email Intelligence: Automatic detection + smart prompting after 3 messages

    Keep-alive System: Silent background pinging to prevent cold starts

    Error Resilience: Graceful fallbacks for API failures

🔒 Security & Performance

    Location-aware LLMs: Automatic China routing to DeepSeek

    Secure Credentials: All secrets managed through environment variables

    Cached Resources: Resume data cached for performance

    Error Handling: Robust exception handling throughout

🧪 CI/CD (GitHub Actions)

This repo uses GitHub Actions to:

    ✅ Lint code with flake8 and black

    ✅ Scan for committed secrets with detect-secrets

    ✅ Test OpenAI and DeepSeek API access

View CI results: [CI Dashboard]
🌐 Live Demo

Try the app live: almateus.me
📜 License

MIT License — use, modify, and share freely.
🤝 Contact

Built by Al Mateus
✉️ al@optimops.ai
🌐 LinkedIn