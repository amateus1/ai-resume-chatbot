class Me:
    def __init__(self):
        self.name = "Al Mateus"
        self.summary, self.resume = self._load_resume()

    @lru_cache(maxsize=1)
    def _load_resume(self):
        summary = ""
        resume_text = ""

        # Load short executive bio (always used)
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            summary = f.read()

        # Load resume PDF (conditionally used)
        from pypdf import PdfReader
        reader = PdfReader("me/Al_Mateus_09-25-v4_compressed.pdf")
        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text + "\n"

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
