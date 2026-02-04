from flask import Flask, render_template, request, jsonify
from chatbot import GymChatbot
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize chatbot
chatbot = GymChatbot()

@app.route('/')
def home():
    """Render the main website page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chatbot requests"""
    try:
        # Get user message from request
        user_message = request.json.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get chatbot response
        bot_response = chatbot.get_response(user_message)
        
        # Return response as JSON
        return jsonify({
            'response': bot_response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/health')
def health():
    """Health check endpoint for deployment"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)