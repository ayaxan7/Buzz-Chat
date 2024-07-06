from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os
import logging

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key securely using an environment variable
openai.api_key = os.getenv('sk-proj-e9VBcBpHNWJC5M1zmhGtT3BlbkFJLBd8DDFgTJ7naiu642wo')

# Configure logging
logging.basicConfig(level=logging.INFO)  # Adjust level as needed

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/api', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            raise ValueError('Invalid request format or missing message field.')

        user_message = data['message']

        # Basic input validation
        if not isinstance(user_message, str) or len(user_message.strip()) == 0:
            raise ValueError('Message should be a non-empty string.')

        # Perform AI response generation
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=user_message,
            max_tokens=150
        )
        openai_response = response.choices[0].text.strip()

        # Log successful interaction
        logging.info(f"User message: {user_message}, AI response: {openai_response}")

        return jsonify({'message': openai_response}), 200

    except ValueError as ve:
        error_message = str(ve)
        logging.error(f"ValueError: {error_message}")
        return jsonify({'error': error_message}), 400

    except Exception as e:
        error_message = str(e)
        logging.error(f"Exception: {error_message}")
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
