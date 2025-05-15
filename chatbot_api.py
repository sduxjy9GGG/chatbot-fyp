from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DEEPSEEK_API_KEY = "sk-b5efeb796de44211a4ae1d8603ab2cdd"  

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    # Call DeepSeek API
    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",  # Or use "deepseek-coder" if you want code-based replies
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
