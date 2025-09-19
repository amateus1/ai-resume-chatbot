import os
import resend
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

def test_resend():
    try:
        response = resend.Emails.send({
            "from": "al@optimops.ai",   # must be verified in Resend
            "to": os.getenv("ALERT_EMAIL"),     # your destination email
            "subject": "✅ Resend test email",
            "html": "<p>Hello! This is a test email sent via Resend Python SDK.</p>"
        })
        print("Email sent successfully:", response)
    except Exception as e:
        print("Error sending email:", e)

if __name__ == "__main__":
    test_resend()
