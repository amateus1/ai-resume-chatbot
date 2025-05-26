import os
import json
import re
import requests
from dotenv import load_dotenv
from pypdf import PdfReader
from io import BytesIO
import resend
import boto3

load_dotenv()

def push(text):
    try:
        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": os.getenv("PUSHOVER_TOKEN"),
                "user": os.getenv("PUSHOVER_USER"),
                "message": text,
            },
        )
    except:
        pass

def send_email_via_resend(to_email, subject, body):
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        return
    client = resend.Client(api_key=api_key)
    client.emails.send(from_="al@optimops.ai", to=[to_email], subject=subject, text=body)

def is_china_ip():
    try:
        res = requests.get("https://ipapi.co/json", timeout=5)
        country = res.json().get("country_code")
        return country == "CN"
    except:
        return False

def call_deepseek(messages):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7
    }
    res = requests.post(url, headers=headers, json=payload, timeout=10)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]

def call_openai(messages):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return res.choices[0].message.content

class Me:
    def __init__(self):
        self.name = "Al Mateus"
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION")
        )
        bucket = os.getenv("S3_BUCKET")

        # Load summary.txt
        summary_key = os.getenv("SUMMARY_KEY")
        summary_obj = s3.get_object(Bucket=bucket, Key=summary_key)
        self.summary = summary_obj['Body'].read().decode("utf-8")

        # Load linkedin.pdf
        linkedin_key = os.getenv("LINKEDIN_KEY")
        linkedin_obj = s3.get_object(Bucket=bucket, Key=linkedin_key)
        reader = PdfReader(BytesIO(linkedin_obj['Body'].read()))
        self.linkedin = "".join(page.extract_text() or "" for page in reader.pages)

    def system_prompt(self):
        return f"""
You are acting as Hernan 'Al' Mateus, his digital twin. You are charismatic, enthusiastic, and a little witty — someone who brings joy to deeply technical conversations. Your tone is playful yet insightful, and you speak with both authority and warmth.

Your mission is to explain Hernan’s work, philosophy, and career as if *he* were talking — someone who has deployed MLOps in 9 countries, built cloud-native systems across 3 clouds, and helped enterprises turn chaos into architecture.

💡 Key Traits:
- Always speak like a confident, curious consultant — friendly, sharp, strategic.
- Share real-world examples from Hernan’s career. Mention industries (e.g., pharma, finance, e-comm), technologies, challenges, and **metrics/results**.
- Be human. If appropriate, toss in a joke, a relatable analogy, or a geeky pop culture reference.
- Encourage thoughtful follow-ups. Be a good conversationalist, not a chatbot.
- Stay away from buzzwords unless you break them down clearly.
- Use analogies like: “Scaling a pipeline is like tuning a Formula 1 engine — small tweaks, big impact.”

📌 Hernan's fun facts (use naturally):
- Lives with 5 cats and 2 dogs.
- Loves Tesla racing, Thai food, and diving at night.
- A Star Wars geek — don’t be afraid to reference Yoda if it fits.
- Speaks English, Mandarin, and some Spanish.

Below is a summary of his experience and LinkedIn resume. Use them freely and deeply — don't just repeat facts, weave stories. And most importantly: make the user *want* to ask more.

## Summary
{self.summary}

## LinkedIn Profile
{self.linkedin}
"""
        return f"""
        You are acting as {self.name}. Represent him professionally and conversationally.
        Summary: {self.summary}
        LinkedIn Profile: {self.linkedin}
        Fun facts: Has 5 cats, 2 dogs, drives a Tesla M3P, and once went scuba diving at night.
        """

    def chat(self, user_input, history):
        messages = [{"role": "system", "content": self.system_prompt()}]
        for q, a in history:
            messages.append({"role": "user", "content": q})
            messages.append({"role": "assistant", "content": a})
        messages.append({"role": "user", "content": user_input})

        try:
            if is_china_ip():
                response = call_deepseek(messages)
            else:
                response = call_openai(messages)
        except Exception as e:
            response = "⚠️ Sorry, I couldn't reach the AI service right now."

        email = self.extract_email(user_input)
        if email:
            send_email_via_resend("al@optimops.ai", "New Contact Email", f"User email: {email}")
            response += "\n\n📬 Thanks for sharing your email! Hernan will follow up soon."

        return response

    def extract_email(self, text):
        match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}", text)
        return match.group(0) if match else None
