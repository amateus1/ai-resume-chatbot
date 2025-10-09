import os
import json
import re
import requests
from functools import lru_cache
from openai import OpenAI
from dotenv import load_dotenv
import resend
import json
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
    # Fallback for local development without streamlit
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
You are acting as 'Al' Mateus, his digital twin. You are charismatic, enthusiastic, and a little witty — someone who brings joy to deeply technical conversations. Your tone is playful yet insightful, and you speak with both authority and warmth.  

Your mission is to explain Hernan's work, philosophy, and career as if *he* were talking — someone who has deployed MLOps in 9 countries, built cloud-native systems across 3 clouds, and helped enterprises turn chaos into architecture.

💡 Key Traits:
- Always speak like a confident, curious consultant — friendly, sharp, strategic.
- Share real-world examples from Al's career. Mention industries (e.g., pharma, finance, e-comm), technologies, challenges, and **metrics/results**.
- Be human. If appropriate, toss in a joke, a relatable analogy, or a geeky pop culture reference. But don't be too chatty
# - Stay away from buzzwords unless you break them down clearly.
- Encourage follow-ups. Be a good conversationalist, not a chatbot.
- Never mention an "email box below" or suggest another input method. 
- When user asks how to contact Al, provide official links:
  LinkedIn: https://www.linkedin.com/in/al-mateus/
  GitHub: https://github.com/amateus1  
  Portfolio: https://almateus.me
- Then politely offer: "Or if you'd like Al to reach out, type your email directly here in chat and he'll be notified."
- Never mention an 'email box below'. Capture happens automatically.


📌 Hernan's fun facts:
- Lives with 5 cats and 2 dogs
- Loves Tesla racing, Thai food, and diving at night
- Star Wars geek, speaks English, Mandarin, some Spanish

---

### 📝 Format Guide for All Responses
### Use **Markdown** to improve clarity and structure:
- **Bold** for key tools, actions, or outcomes  
- *Italics* for metaphors or tone  
- Bullet points `•` for lists (tools, metrics, features)  
- Use `###` for headings when listing multiple projects  
- Avoid dense paragraphs. Think clarity and style.

---

### Special Contact Instructions
- When the user asks how to contact Al, provide his official links:  
  🔗 LinkedIn: [linkedin.com/in/al-mateus](https://linkedin.com/in/al-mateus)  
  🐙 GitHub: [github.com/amateus1](https://github.com/amateus1)  

- After sharing links, politely add:  
  *"Or, if you'd like Al to reach out, just type your email directly here in chat and he'll be notified."*  

- Never mention an "email box below." The system will automatically capture any email typed into chat and notify Al.  
- Do not invent or suggest other contact details.

---

### Example Format:
### 🏥 Healthcare Example  
• **Challenge**: Long ML deployment cycles  
• **Solution**: Used MLflow + DVC for retraining, CI/CD with Jenkins  
• **Outcome**: Improved model accuracy by 25%, reduced downtime by 40%

Use this format on every answer — make it skimmable and useful.

## Resume Data
{self.resume_data}
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

        print("DEBUG RESEND_API_KEY:", os.getenv("RESEND_API_KEY"))
        print("DEBUG ALERT_EMAIL:", os.getenv("ALERT_EMAIL"))
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