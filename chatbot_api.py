from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allows communication with Flutter frontend

# ✅ Paste your DeepSeek API key here
DEEPSEEK_API_KEY = "sk-b5efeb796de44211a4ae1d8603ab2cdd"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    print("📩 Received message:", user_message)

    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",  # Or "deepseek-coder" if needed
                "messages": [
                    {"role": "system", "content": "You are a helpful stock market assistant."},
                    {"role": "user", "content": user_message}
                ]
            },
            timeout=15  # Prevents app from hanging
        )

        if response.status_code == 200:
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
            return jsonify({"reply": reply})
        else:
            print("❌ DeepSeek API returned:", response.status_code)
            return jsonify({"reply": f"❌ DeepSeek error: {response.status_code}"}), 500

    except requests.exceptions.Timeout:
        print("⚠️ DeepSeek API timed out")
        return jsonify({"reply": "⏳ DeepSeek API timed out. Please try again."}), 500

    except Exception as e:
        print("❌ Exception while calling DeepSeek:", str(e))
        return jsonify({"reply": "⚠️ Server error while contacting DeepSeek."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
