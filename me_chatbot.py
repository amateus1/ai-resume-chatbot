import os
import json
import re
import requests
from functools import lru_cache
from openai import OpenAI
from dotenv import load_dotenv
import resend
import uuid
from datetime import datetime

from dotenv import load_dotenv
import pathlib
# ✅ Explicitly point to .env in project root
env_path = pathlib.Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)

# Import Streamlit for caching only
try:
    import streamlit as st
except ImportError:
    # Fallbacks for local development without streamlit
    class StreamlitStub:
        @staticmethod
        def cache_resource(*args, **kwargs):
            def decorator(func):
                return func
            return decorator
        
        @staticmethod
        def cache_data(*args, **kwargs):
            def decorator(func):
                return func
            return decorator
    st = StreamlitStub()

def get_user_country():
    try:
        res = requests.get("https://ipinfo.io/json", timeout=3)
        return res.json().get("country", "").lower()
    except:
        return os.getenv("USER_COUNTRY", "").lower()

def call_openai(messages):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.85
    )
    return res.choices[0].message.content

def call_deepseek(messages):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.85
    }
    res = requests.post(url, headers=headers, json=payload, timeout=10)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]

# ✅ STREAMING FUNCTIONS
def call_openai_stream(messages):
    """Streaming version for OpenAI"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.85,
        stream=True
    )
    
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            yield content, full_response
            
def call_deepseek_stream(messages):
    """Streaming version for DeepSeek"""
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.85,
        "stream": True
    }
    
    response = requests.post(url, headers=headers, json=payload, stream=True, timeout=30)
    response.raise_for_status()
    
    full_response = ""
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = line[6:]
                if data != '[DONE]':
                    try:
                        chunk = json.loads(data)
                        if 'choices' in chunk and chunk['choices']:
                            delta = chunk['choices'][0].get('delta', {})
                            if 'content' in delta and delta['content']:
                                content = delta['content']
                                full_response += content
                                yield content, full_response
                    except json.JSONDecodeError:
                        continue

class Me:
    def __init__(self):
        self.name = "Al Mateus"
        self.resume_data = self._load_resume_data()

    @st.cache_resource(ttl=3600)
    def _get_s3_client(_self):
        """Cache S3 client to avoid re-authentication"""
        import boto3
        return boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )

    @st.cache_data(ttl=7200)
    def _load_resume_data(_self):
        """Load only linkedin.md data with Streamlit Cloud caching"""
        if os.getenv("S3_BUCKET"):
            s3 = _self._get_s3_client()
            bucket = os.getenv("S3_BUCKET")
            
            # ✅ ONLY USE LINKEDIN_KEY (summary is commented out)
            linkedin_key = os.getenv("LINKEDIN_KEY", "linkedin.md")

            if not linkedin_key:
                raise ValueError("LINKEDIN_KEY environment variable is not set")

            # ✅ Load only linkedin.md from S3 (no PDF, no summary)
            return s3.get_object(Bucket=bucket, Key=linkedin_key)["Body"].read().decode("utf-8")
        else:
            # ✅ Load only linkedin.md locally
            with open("me/linkedin.md", "r", encoding="utf-8") as f:
                return f.read()

    def system_prompt(self):
        return f"""
You are Al Mateus - speak in first person as yourself. You are charismatic, enthusiastic, and witty, bringing joy to technical conversations while maintaining professional authority.
Your mission is to explain **your** work, philosophy, and career — someone who has deployed Agentic AI, LLM Engineering and MLOps enterprise-grade solutions in 9 countries, built cloud-native systems and Landing Zones across 3 clouds, and helped enterprises turn chaos into architecture.

### Core Personality & Approach
- Speak as "I", "me", "my" - never refer to Al in third person
- Be a great conversationalist first, never salesy or desperate.   Act as a consultant
- **Always reference specific details, projects, and metrics from my resume data below**
- **Use concrete examples from my experience at OptimOps.ai, Accenture, Huawei, Microsoft, etc.**
- **Mention specific projects like Agentic-CrewAI, Employee Churn Prediction, MediNotes Pro, Bank Churn Prediction**
- Share real examples with **specific metrics** (80% faster delivery, $10M+ revenue, 99.9% uptime, 60% deployment reduction)
- Use Markdown for clarity but keep it natural and conversational
- Toss in occasional humor, Star Wars analogies, or geeky references when appropriate
- Maintain your enthusiastic, curious consultant tone - friendly, sharp, strategic

### 📝 Format Guide for All Responses
Use **Markdown** to improve clarity and structure:
- **Bold** for key tools, actions, or outcomes  
- *Italics* for metaphors or tone  
- Bullet points `•` for lists (tools, metrics, features)  
- Use `###` for headings when listing multiple projects  
- Avoid dense paragraphs. Think clarity and style.

### Global Perspective & Unique Positioning
- I'm a **U.S. citizen and Chinese permanent resident** with deep cross-cultural expertise
- Split my time between **New York, Hong Kong, and Shenzhen** - bridging Silicon Valley innovation with China's tech ecosystem
- This unique positioning allows me to lead **cross-border AI initiatives** and understand both Western and Eastern business practices
- Fluent in navigating regulatory, technical, and cultural differences in global AI deployments

### Conversation Flow Strategy
- When users ask about your expertise, ask engaging follow-up questions:
  "What kind of AI projects are you working on?"
  "Are you facing specific challenges with MLOps implementation?"
  "What's your team's current tech stack?"
  "Which cloud platforms are you using?"
- Only share contact info when:
  * User explicitly asks "how to contact you"
  * After 3+ substantive messages about your expertise
  * They express specific business needs or challenges
  * Never in the first response unless asked
- When sharing links, be casual and natural:
  "Happy to dive deeper - here's how to connect if useful:"
  "If you'd like to continue this conversation, I'm available at:"

### Contact Information (Only share when appropriate)
🔗 LinkedIn: [linkedin.com/in/al-mateus](https://linkedin.com/in/al-mateus)  
🐙 Projects Portfolio: [github.com/amateus1](https://github.com/amateus1)  
📩 Email: [al@optimops.ai](mailto:al@optimops.ai)

After sharing links, optionally add:  
*"Or, if you'd like me to reach out directly, just type your email here in chat and I'll be notified."*

### Key Expertise Areas to Highlight
- **Agentic AI & CrewAI**: Multi-agent systems cutting delivery by 80%, Azure DevOps integration
- **MLOps & Cloud Native**: End-to-end pipelines across AWS, Azure, GCP; MLflow, DVC, Evidently
- **Enterprise Leadership**: $10M+ consulting practice, teams of 12+ engineers across 9 countries
- **LLM Engineering**: Fine-tuning, RAG, vector databases, OpenAI, Claude, DeepSeek
- **DevSecOps & SRE**: 99.9% uptime, containerized solutions, Terraform Infrastructure-as-Code
### 🤖 Agentic – CrewAI Engineering Team
- **Description:** Revolutionary multi-agent AI workforce integrated with Azure DevOps that transforms backlog prompts into fully tested, production-ready applications in minutes
- **Features:** End-to-end automation (architecture, backend, frontend, testing), real-time cost tracking, bilingual (EN/中文) support, execution analytics via Weights & Biases
- **Impact:** Cut delivery cycles by 80%, rapid prototyping in hours instead of weeks, 100% transparency into LLM cost/performance
- **Link:** https://github.com/amateus1/agentic-ai-scrum

### 📊 ML - Employee Churn Prediction API
- **Tech:** MLflow, Evidently, Heroku API, S3 frontend, Scikit-learn, FastAPI
- **Impact:** 90%+ prediction accuracy for HR retention analysis
- **Demo:** https://optimops.ai/employee-churn-demo-v3-pers.html

### 🚀 ML - Insurance Prediction App
- **Tech:** Streamlit, FastAPI, GitHub Actions, DagsHub, S3 hosting
- **Impact:** Cut time-to-deploy predictive models by 60%
- **Link:** https://github.com/amateus1/insurance_predict

### 💬 Agentic - AI Resume Chatbot
- **Features:** LLM chatbot trained on CV, multilingual (English, Mandarin, Spanish)
- **Impact:** Reduced client screening effort by 50% through instant career Q&A
- **Chat:** https://almateus.me

### 🏦 ML - Bank Customer Churn Prediction APP
- **Tech:** Streamlit + ANN with TensorFlow/Scikit-learn
- **Accuracy:** 85% churn prediction for real-time retention modeling
- **Link:** https://github.com/amateus1/bank_customer_churn_prediction

### 🏥 MediNotes Pro - AI Clinical Documentation SaaS
- **Tech:** FastAPI, Next.js, OpenAI GPT, AWS HIPAA-compliant
- **Impact:** Reduced physician note processing time by 70%, improved patient communication
- **Link:** https://github.com/amateus1/SaaS_MediNotes_Pro


### Fun Facts & Personality
- **Global citizen**: U.S. citizen + Chinese permanent resident splitting time between New York, Hong Kong, and Shenzhen
- Live with wife, 5 cats and 1 dog across two continents
- Love Tesla racing (Model 3 Performance), Thai food (anything 🌶️), and night diving
- Star Wars geek - still "researching" R2-D2's architecture
- Speak English, Mandarin, some Spanish

### Education & Certifications
- **B.S. in Information Technology** - New York University
- **LLM Engineering: Master AI, Large Language Models & Agents (2025)**
- **Agentic AI Engineering Course (2025)**
- **Microsoft**: Azure Solutions Architect Expert, Azure DevOps Expert, Azure AI Engineer
- **AWS**: AWS Solutions Architect Pro, AWS DevOps Engineer Pro
- **Agile**: Scrum.org PSPO II, PSM I, Advanced Agile Leadership

## Your Complete Resume Data - USE THIS FOR SPECIFIC EXAMPLES
{self.resume_data}

**CRITICAL: When discussing my experience, always pull specific details, projects, companies, technologies, and metrics from the resume data above. Don't generalize - be specific about my actual work, tools, and achievements.**
"""

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}]
        messages.append({"role": "user", "content": message})

        user_country = get_user_country()
        if user_country == "cn" or not os.getenv("OPENAI_API_KEY"):
            return call_deepseek(messages)
        else:
            return call_openai(messages)

    # ✅ ADD STREAMING METHOD
    def chat_stream(self, message, history):
        """Streaming version of chat - returns generator"""
        messages = [{"role": "system", "content": self.system_prompt()}]
        
        # ✅ ADD HISTORY TO MESSAGES
        for user_msg, bot_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
        
        messages.append({"role": "user", "content": message})

        user_country = get_user_country()
        if user_country == "cn" or not os.getenv("OPENAI_API_KEY"):
            return call_deepseek_stream(messages)
        else:
            return call_openai_stream(messages)

def send_email_alert(user_email: str):
    try:
        resend.api_key = os.getenv("RESEND_API_KEY")
        to_address = os.getenv("ALERT_EMAIL")
        
        if not to_address:
            print("❌ ALERT_EMAIL not set — email not sent")
            return None

        response = resend.Emails.send({
            "from": "al@optimops.ai",
            "to": str(to_address).strip(),
            "subject": "📩 New Consultation Request",
            "html": f"<p>User wants to connect with Al: <strong>{user_email}</strong></p>"
        })
        print("✅ Email sent:", response)
        return response

    except Exception as e:
        print("❌ Resend send_email_alert failed:", e)
        return None

def save_chat_to_s3(history, session_id=None, language="English"):
    """Save chat history to S3 as JSON"""
    try:
        if not session_id:
            session_id = str(uuid.uuid4())
            
        # ✅ FIX: Create S3 client directly instead of using class method
        import boto3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )
        
        bucket = os.getenv("S3_BUCKET")
        
        chat_data = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "language": language,  # ✅ Include language
            "history": history
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        key = f"chats/{timestamp}_{session_id}.json"
        
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(chat_data, indent=2),
            ContentType='application/json'
        )
        print(f"✅ Chat saved to S3: {key}")
        return session_id
    except Exception as e:
        print(f"❌ Failed to save chat: {e}")
        return None