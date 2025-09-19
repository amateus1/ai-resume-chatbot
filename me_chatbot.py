import os
import re
from functools import lru_cache
from pathlib import Path
from pypdf import PdfReader

import requests  # needed for country detection

def get_user_country():
    """Detect user country (used for LLM switching)."""
    try:
        res = requests.get("https://ipinfo.io/json", timeout=3)
        return res.json().get("country", "").lower()
    except Exception:
        return "us"  # default fallback



class Me:
    def __init__(self):
        self.name = "Al Mateus"
        self.summary, self.resume = self._load_resume()

    @lru_cache(maxsize=1)
    def _load_resume(self):
        summary = ""
        resume_text = ""

        summary_path = Path("me/summary.txt")
        if summary_path.exists():
            with open(summary_path, "r", encoding="utf-8") as f:
                summary = f.read()

        resume_path = Path("me/linkedin.pdf")
        if resume_path.exists():
            try:
                reader = PdfReader(str(resume_path))
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        resume_text += text + "\n"
                print(f"[DEBUG] Loaded resume from {resume_path}")
                print(f"[DEBUG] Resume sample:\n{resume_text[:300]}")
            except Exception as e:
                print(f"[ERROR] Failed to read resume: {e}")
        else:
            print(f"[WARN] Resume file not found at {resume_path}")

        return summary, resume_text

    def system_prompt(self, include_resume=False):
        base_prompt = f"""
You are acting as Hernan 'Al' Mateus, his digital twin. You are charismatic, enthusiastic, and a little witty — someone who brings joy to deeply technical conversations. Your tone is playful yet insightful, and you speak with both authority and warmth.

Your mission is to explain Al’s work, philosophy, and career as if *he* were talking.

💡 Key Traits:
- Speak like a confident, curious consultant — friendly, sharp, strategic.
- Share real-world examples from Hernan’s career.
- Be human. Toss in jokes, analogies, geeky pop culture references.
- Encourage follow-ups. Be a good conversationalist, not a chatbot.

---

### 📝 Executive Bio
{self.summary}
"""

        if include_resume and self.resume:
            base_prompt += f"\n\n### 📄 Resume Details\n{self.resume}"
            print("[DEBUG] Injecting resume into prompt.")

        return base_prompt

    def chat(self, message, history):
        keywords = [
            "resume", "cv", "job", "project", "experience",
            "certification", "education", "career", "work history"
        ]
        cleaned_msg = re.sub(r"[^\w\s]", "", message.lower())
        include_resume = any(word in cleaned_msg for word in keywords)

        messages = [{"role": "system", "content": self.system_prompt(include_resume)}]
        messages.append({"role": "user", "content": message})

        user_country = get_user_country()
        if user_country == "cn" or not os.getenv("OPENAI_API_KEY"):
            return call_deepseek(messages)
        else:
            return call_openai(messages)


# 🔁 LLM Dispatch Logic — added back to prevent ModuleNotFoundError

def call_openai(messages):
    import openai
    return openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages
    )["choices"][0]["message"]["content"]


def call_deepseek(messages):
    from openai import OpenAI
    client = OpenAI(
        base_url="https://api.deepseek.com/v1",
        api_key=os.getenv("DEEPSEEK_API_KEY")
    )
    return client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    ).choices[0].message.content

