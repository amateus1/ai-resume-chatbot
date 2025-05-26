import os
import json
import re
import requests
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
import resend

load_dotenv()

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
        self.linkedin = ""
        self.summary = ""

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

            self.summary = s3.get_object(Bucket=bucket, Key=summary_key)["Body"].read().decode("utf-8")
            reader = PdfReader(s3.get_object(Bucket=bucket, Key=linkedin_key)["Body"])
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    self.linkedin += text
        else:
            with open("me/summary.txt", "r", encoding="utf-8") as f:
                self.summary = f.read()
            reader = PdfReader("me/linkedin.pdf")
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    self.linkedin += text

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

## Summary
{self.summary}

## LinkedIn Profile
{self.linkedin}
"""

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}]
        messages.append({"role": "user", "content": message})

        # Automatic switch: use DeepSeek for China or if OPENAI_API_KEY is unavailable
        country = os.getenv("USER_COUNTRY", "").lower()
        if country == "china" or not os.getenv("OPENAI_API_KEY"):
            return call_deepseek(messages)
        else:
            return call_openai(messages)
