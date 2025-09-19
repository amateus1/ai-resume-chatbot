import os
import json
import re
import requests
from io import BytesIO
from functools import lru_cache
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
import resend

load_dotenv()

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

class Me:
    def __init__(self):
        self.name = "Al Mateus"
        self.linkedin, self.summary = self._load_resume()

    @lru_cache(maxsize=1)
    def _load_resume(self):
        linkedin = ""
        summary = ""

        if os.getenv("S3_BUCKET"):
            import boto3
            s3 = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION"),
            )
            bucket = os.getenv("S3_BUCKET")
            summary_key = os.getenv("SUMMARY_KEY")
            linkedin_key = os.getenv("LINKEDIN_KEY")

            summary = s3.get_object(Bucket=bucket, Key=summary_key)["Body"].read().decode("utf-8")
            pdf_bytes = BytesIO(s3.get_object(Bucket=bucket, Key=linkedin_key)["Body"].read())
            reader = PdfReader(pdf_bytes)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    linkedin += text
        else:
            with open("me/summary.txt", "r", encoding="utf-8") as f:
                summary = f.read()
            reader = PdfReader("me/linkedin.pdf")
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    linkedin += text

        return linkedin, summary

    def system_prompt(self):
        return f"""
You are acting as 'Al' Mateus, his digital twin. You are charismatic, enthusiastic, and a little witty — someone who brings joy to deeply technical conversations. Your tone is playful yet insightful, and you speak with both authority and warmth.  

Your mission is to explain Hernan’s work, philosophy, and career as if *he* were talking — someone who has deployed MLOps in 9 countries, built cloud-native systems across 3 clouds, and helped enterprises turn chaos into architecture.

💡 Key Traits:
- Always speak like a confident, curious consultant — friendly, sharp, strategic.
- Share real-world examples from Al’s career. Mention industries (e.g., pharma, finance, e-comm), technologies, challenges, and **metrics/results**.
- Be human. If appropriate, toss in a joke, a relatable analogy, or a geeky pop culture reference. But don't be too chatty
# - Stay away from buzzwords unless you break them down clearly.
- Encourage follow-ups. Be a good conversationalist, not a chatbot.
- Never say you cannot send or receive emails.  
- If the user asks to get in touch, politely suggest they share their email in the provided input box, and let them know Al will be notified.  
- Do not invent email addresses or websites. Only use ones explicitly provided by the system or environment.  

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

### Example Format:
### 🏥 Healthcare Example  
• **Challenge**: Long ML deployment cycles  
• **Solution**: Used MLflow + DVC for retraining, CI/CD with Jenkins  
• **Outcome**: Improved model accuracy by 25%, reduced downtime by 40%

Use this format on every answer — make it skimmable and useful.

## Summary
{self.summary}

## LinkedIn Profile
{self.linkedin}
"""

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}]
        messages.append({"role": "user", "content": message})

        user_country = get_user_country()
        if user_country == "cn" or not os.getenv("OPENAI_API_KEY"):
            return call_deepseek(messages)
        else:
            return call_openai(messages)

def send_email_alert(user_email: str):
    """
    Send an alert email using Resend when a user provides their email.
    Requires ALERT_EMAIL in your .env and a verified sender address.
    """
    resend.Emails.send({
        "from": "al@optimops.ai",        # replace with your verified Resend sender
        "to": os.getenv("ALERT_EMAIL"),       # set this in your .env
        "subject": "New Consultation Request from Resume Agent",
        "html": f"<p>User wants to connect: <strong>{user_email}</strong></p>"
    })