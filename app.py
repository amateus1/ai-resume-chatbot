import os
import re
import requests
from functools import lru_cache
from pathlib import Path
from pypdf import PdfReader

# -----------------------------
# Country detection (for LLM routing)
# -----------------------------
def get_user_country() -> str:
    """Return 2-letter country code in lower case; fallback to 'us'."""
    try:
        r = requests.get("https://ipinfo.io/json", timeout=3)
        return (r.json().get("country") or "").lower() or "us"
    except Exception:
        return "us"

# -----------------------------
# LLM dispatch (OpenAI v1 SDK + DeepSeek)
# -----------------------------
def call_openai(messages):
    """OpenAI Chat Completions (v1 SDK)."""
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.85,
    )
    return resp.choices[0].message.content

def call_deepseek(messages):
    """DeepSeek via OpenAI-compatible client endpoint."""
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
    )
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.85,
    )
    return resp.choices[0].message.content

# -----------------------------
# Main persona class
# -----------------------------
class Me:
    def __init__(self):
        self.name = "Al Mateus"
        self.summary, self.resume = self._load_resume()

    @lru_cache(maxsize=1)
    def _load_resume(self):
        """Load executive bio (summary.txt) and LinkedIn resume PDF text."""
        summary_text = ""
        resume_text = ""

        # --- summary.txt (root or me/) ---
        base = Path(__file__).resolve().parent
        summary_paths = [base / "summary.txt", base / "me" / "summary.txt"]
        for p in summary_paths:
            if p.exists():
                with open(p, "r", encoding="utf-8") as f:
                    summary_text = f.read()
                break
        if not summary_text:
            print("[WARN] summary.txt not found (root or me/).")

        # --- linkedin.pdf (root or me/) ---
        resume_paths = [base / "linkedin.pdf", base / "me" / "linkedin.pdf"]
        for p in resume_paths:
            if p.exists():
                try:
                    reader = PdfReader(str(p))
                    for page in reader.pages:
                        try:
                            t = page.extract_text()
                        except Exception:
                            t = None
                        if t:
                            resume_text += t + "\n"
                    print(f"[DEBUG] Loaded resume from {p}")
                except Exception as e:
                    print(f"[ERROR] Failed to read LinkedIn PDF: {e}")
                break
        if not resume_text:
            print("[WARN] linkedin.pdf not found or empty (root or me/).")

        # Small preview for server logs (no UI impact)
        if resume_text:
            print("[DEBUG] Resume sample:", resume_text[:300].replace("\n", " "))

        return summary_text, resume_text

    def system_prompt(self, include_resume: bool = False):
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
        # Make resume usage explicit so the model doesn't ignore it.
        if include_resume and self.resume:
            base_prompt += f"""

### 📄 Resume Details  
Use this information when answering questions about certifications, projects, work history, or education.  
Do not ignore this content — it is Hernan 'Al' Mateus’s actual resume data.

{self.resume}
"""
            print("[DEBUG] Injecting resume into prompt.")

        return base_prompt

    def chat(self, message, history):
        # Keyword triggers for resume context (keep as-is + robust matching)
        keywords = [
            # English
            "resume", "cv", "job", "project", "experience",
            "certification", "certifications", "education", "career", "work history",
            # Chinese
            "简历", "经历", "工作经验", "教育背景", "项目经验", "认证",
            # Spanish
            "currículum", "trabajo", "proyecto", "experiencia", "certificación", "educación", "carrera"
        ]
        cleaned = re.sub(r"[^\w\s]", "", (message or "").lower())
        include_resume = any(k in cleaned for k in keywords)
        print(f"[DEBUG] include_resume={include_resume}")

        messages = [
            {"role": "system", "content": self.system_prompt(include_resume)},
            {"role": "user", "content": message},
        ]

        # Location-based routing (CN → DeepSeek; otherwise OpenAI). Keep logic intact.
        country = get_user_country()
        if country == "cn" or not os.getenv("OPENAI_API_KEY"):
            return call_deepseek(messages)
        else:
            return call_openai(messages)
