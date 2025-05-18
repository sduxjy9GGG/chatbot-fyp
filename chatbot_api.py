from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from Flutter

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    print("📩 Received message:", user_message)  # <-- Debug print

    # ✅ Temporary dummy reply to test
    return jsonify({"reply": f"✅ Got your message: {user_message}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
