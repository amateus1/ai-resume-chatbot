import os
from pathlib import Path
from functools import lru_cache
from pypdf import PdfReader

# Assuming you already have these helpers in your project:
# - get_user_country()
# - call_openai()
# - call_deepseek()

class Me:
    def __init__(self):
        self.name = "Al Mateus"
        self.summary, self.resume = self._load_resume()

    @lru_cache(maxsize=1)
    def _load_resume(self):
        summary = ""
        resume_text = ""

        base_dir = Path(__file__).resolve().parent

        # --- Load summary.txt (always used) ---
        summary_path = base_dir / "summary.txt"
        if not summary_path.exists():
            summary_path = base_dir / "me" / "summary.txt"

        if summary_path.exists():
            with open(summary_path, "r", encoding="utf-8") as f:
                summary = f.read()
        else:
            summary = "Summary file not found."

        # --- Load linkedin.pdf (conditionally used) ---
        resume_path = base_dir / "linkedin.pdf"
        if not resume_path.exists():
            resume_path = base_dir / "me" / "linkedin.pdf"

        if resume_path.exists():
            try:
                reader = PdfReader(str(resume_path))
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        resume_text += text + "\n"
            except Exception as e:
                resume_text = f"Could not read LinkedIn PDF: {e}"
        else:
            resume_text = "LinkedIn PDF not found."

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

        if include_resume:
            base_prompt += f"\n\n### 📄 Resume Details\n{self.resume}"

        return base_prompt

    def chat(self, message, history):
        # Trigger resume only if user asks about work/career specifics
        keywords = [
            "resume", "cv", "job", "project", "experience",
            "certification", "education", "career", "work history"
        ]
        include_resume = any(word in message.lower() for word in keywords)

        messages = [{"role": "system", "content": self.system_prompt(include_resume)}]
        messages.append({"role": "user", "content": message})

        user_country = get_user_country()
        if user_country == "cn" or not os.getenv("OPENAI_API_KEY"):
            return call_deepseek(messages)
        else:
            return call_openai(messages)

