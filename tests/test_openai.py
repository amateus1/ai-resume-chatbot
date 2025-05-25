import os
from openai import OpenAI

def test_openai_connectivity():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        models = client.models.list()
        assert models.data, "No models returned"
        print("✅ OpenAI API test passed.")
    except Exception as e:
        print("❌ OpenAI API test failed:", e)

if __name__ == "__main__":
    test_openai_connectivity()
