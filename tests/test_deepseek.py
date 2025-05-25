import os
import requests

def test_deepseek_connectivity():
    try:
        res = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "Hello"}]
            },
            timeout=10
        )
        assert res.status_code == 200
        print("✅ DeepSeek API test passed.")
    except Exception as e:
        print("❌ DeepSeek API test failed:", e)

if __name__ == "__main__":
    test_deepseek_connectivity()
