from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = "sk-b5efeb796de44211a4ae1d8603ab2cdd"  # ✅ Replace with your DeepSeek API key

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful stock market assistant."},
                {"role": "user", "content": user_message}
            ]
        }
    )

    if response.status_code == 200:
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    else:
        return jsonify({"reply": f"❌ DeepSeek error: {response.status_code}"}), 500

@app.route('/')
def home():
    return "✅ Flask + DeepSeek is Live!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
