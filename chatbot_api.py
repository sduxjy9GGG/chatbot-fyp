from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 🔑 Only change this line (replace with new API key)
DEEPSEEK_API_KEY = 'sk-baa39588b9d5418d84336d0a1780b1f2'  # <<< UPDATE THIS

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Call DeepSeek API
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
            },
            timeout=10  # Prevents hanging
        )

        # Success case
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            return jsonify({"reply": reply})
        
        # Handle API errors
        return jsonify({
            "error": f"DeepSeek API Error {response.status_code}",
            "details": response.text  # Returns actual API error message
        }), response.status_code

    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
