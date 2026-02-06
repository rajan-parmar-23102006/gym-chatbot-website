# Download NLTK data automatically on server startup
import nltk
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (find it relative to this script)
env_path = Path(__file__).parent / '.env'    # __file__ --> current path
load_dotenv(dotenv_path=env_path) 

# Debug: Check if API key is loaded
if os.getenv('GROQ_API_KEY'):
    print("[OK] GROQ_API_KEY found in environment")  
else:
    print("[WARNING] GROQ_API_KEY NOT found! Check your .env file")

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt') #       Checks if NLTK data exists
except LookupError:
    print("Downloading NLTK data...")
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    print("NLTK data downloaded successfully!")

from flask import Flask, render_template, request, jsonify
from chatbot import GymChatbot

# Try to import AI chatbot (optional - works without it too)
try:
    from chatbot_ai import GymChatbotAI
    AI_AVAILABLE = True
    print("[OK] AI Chatbot loaded successfully!")
except Exception as e:
    AI_AVAILABLE = False
    print(f"[WARNING] AI Chatbot not available: {e}")
    print("   Running with rule-based chatbot only.")

# Initialize Flask app
app = Flask(__name__)

# Initialize chatbots
rule_chatbot = GymChatbot()  # Fast, rule-based (always available)
ai_chatbot = None

if AI_AVAILABLE:
    try:
        ai_chatbot = GymChatbotAI()
        print("[OK] AI Chatbot initialized!")
    except Exception as e:
        print(f"[WARNING] Could not initialize AI chatbot: {e}")
        AI_AVAILABLE = False


def get_smart_response(user_message):
    """
    HYBRID APPROACH - Best of both worlds!
    1. Try rule-based first (instant, free, no API calls)
    2. If rule-based doesn't understand → use AI
    """
    global AI_AVAILABLE, ai_chatbot
    
    # First, try rule-based chatbot (fast & free)
    rule_response = rule_chatbot.get_response(user_message)
    
    # Check if rule-based understood the question
    if "I'm not sure I understand" in rule_response:
        # Rule-based didn't understand → Use AI if available
        if AI_AVAILABLE and ai_chatbot:
            try:
                print(f"[AI] Processing: {user_message}")
                ai_response = ai_chatbot.get_response(user_message)
                return ai_response
            except Exception as e:
                print(f"[ERROR] AI Error: {e}")
                # Fall back to rule-based response
                return rule_response
        else:
            print(f"[WARNING] AI not available, AI_AVAILABLE={AI_AVAILABLE}, ai_chatbot={ai_chatbot}")
            # No AI available, return rule-based response
            return rule_response
    else:
        # Rule-based understood → use its response (faster!)
        return rule_response

@app.route('/')
def home():
    """Render the main website page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chatbot requests - uses HYBRID approach"""
    try:
        # Get user message from request
        user_message = request.json.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get smart response (hybrid: rule-based + AI fallback)
        bot_response = get_smart_response(user_message)
        
        # Return response as JSON
        return jsonify({
            'response': bot_response,
            'status': 'success'
        })
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/health')
def health():
    """Health check endpoint for deployment"""
    return jsonify({'status': 'healthy'}), 200   # okay 

if __name__ == '__main__':   # starting point of web app 
    # Run the app         
    port = int(os.environ.get('PORT', 5000))      # on which port our website is live 
    app.run(host='0.0.0.0', port=port, debug=False)    #  debug=False --> production server  , true --> developmnent server (show all codes (security risk ))
     
    
