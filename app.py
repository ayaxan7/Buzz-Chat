from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_input = request.form['user_input']
        
        api_url = 'https://api.openai.com/v1/engines/davinci-codex/completions'
        api_key = 'sk-proj-e9VBcBpHNWJC5M1zmhGtT3BlbkFJLBd8DDFgTJ7naiu642wo'  
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        data = {
            'prompt': user_input,
            'max_tokens': 50
        }
        
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        
        bot_reply = response.json()['choices'][0]['text'].strip()
        
        return jsonify({'status': 'OK', 'answer': bot_reply})
    
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'error_message': str(e)})
    
    except Exception as e:
        return jsonify({'status': 'error', 'error_message': f'Unexpected error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
