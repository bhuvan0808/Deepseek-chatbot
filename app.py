from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# Configure your DeepSeek API key here
DEEPSEEK_API_KEY = ""
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    
    # Store conversation history in session
    if 'history' not in session:
        session['history'] = []
    
    # Call DeepSeek API
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-r1",
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        ai_response = response.json()['choices'][0]['message']['content']
        
        # Add to history
        session['history'].append({
            'user': user_message,
            'ai': ai_response
        })
        session.modified = True
        
        return jsonify({'response': ai_response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(session.get('history', []))

if __name__ == '__main__':
    app.run(debug=True)