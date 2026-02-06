import json     # for read jaosn data 
import nltk
from nltk.tokenize import word_tokenize       # text tokenize (nltk)
from nltk.stem import WordNetLemmatizer    # reduce text complexity (runninngg  -  run)
import re                                # for text cleaning 
from pathlib import Path     
from difflib import SequenceMatcher  # NEW: For fuzzy matching

class GymChatbot:
    def __init__(self, data_file=None):
        # Find data file relative to this script
        if data_file is None:
            data_file = Path(__file__).parent / 'data' / 'gym_data.json'
        
        # Load gym data
        with open(data_file, 'r', encoding='utf-8') as f:
            self.gym_data = json.load(f)
        
        # Initialize NLTK tools
        self.lemmatizer = WordNetLemmatizer()
        
        # Define keyword patterns for different queries
        self.patterns = {
            'membership': ['membership', 'member', 'plan', 'subscription', 'price', 'cost', 'fee', 'package'],
            'trainer': ['trainer', 'coach', 'personal training', 'pt', 'instructor'],
            'timing': ['time', 'timing', 'hours', 'open', 'close', 'schedule', 'when'],
            'facilities': ['facility', 'facilities', 'equipment', 'amenity', 'amenities', 'available'],
            'classes': ['class', 'classes', 'group', 'session', 'workout', 'yoga', 'crossfit', 'hiit', 'spinning'],
            'contact': ['contact', 'phone', 'email', 'address', 'location', 'reach'],
            'greeting': ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon'],
            'thanks': ['thanks', 'thank you', 'appreciate', 'grateful']
        }
        
        # Questions that should ALWAYS go to AI (not handled by rule-based)
        self.ai_triggers = ['name', 'who are you', 'your name', 'discount', 'offer', 'promotion', 
                           'deal', 'cancel', 'refund', 'compare', 'recommend', 'suggest', 'best',
                           'which plan', 'help me', 'created', 'made you', 'bot']
    
    def similarity_score(self, str1, str2):
        """NEW: Calculate similarity between two strings (0 to 1)"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def preprocess_text(self, text):
        """Clean and prepare text for processing"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # Tokenize
        try:
            tokens = word_tokenize(text)
        except:
            # Fallback to simple split if word_tokenize fails
            tokens = text.split()
        # Lemmatize
        try:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        except:
            # If lemmatization fails, use original tokens
            pass
        return tokens
    
    def detect_intent(self, user_input):
        """Detect what the user is asking about"""
        tokens = self.preprocess_text(user_input)
        user_lower = user_input.lower()
        
        # FIRST: Check if this should go to AI (complex questions)
        for trigger in self.ai_triggers:
            if trigger in user_lower:
                return 'unknown'  # This will trigger AI fallback
        
        # SECOND: Try exact matching (original logic)
        for intent, keywords in self.patterns.items():
            for keyword in keywords:
                keyword_tokens = self.preprocess_text(keyword)
                # Check if keyword matches any token
                if any(kt in tokens for kt in keyword_tokens):
                    return intent
        
        # NEW: If no exact match, try fuzzy matching for typos
        best_match_score = 0
        best_intent = 'unknown'
        
        for intent, keywords in self.patterns.items():
            for keyword in keywords:
                for token in tokens:
                    # Skip very short words (less than 4 characters)
                    if len(token) < 4:
                        continue
                    
                    similarity = self.similarity_score(token, keyword)
                    
                    # If similarity is 85% or higher, consider it a match
                    if similarity >= 0.85 and similarity > best_match_score:
                        best_match_score = similarity
                        best_intent = intent
        
        return best_intent
    
    def get_response(self, user_input):
        """Generate appropriate response based on user input"""
        intent = self.detect_intent(user_input)
        
        if intent == 'greeting':
            return "Hello! 👋 Welcome to FitZone Fitness Center! How can I help you today? You can ask me about memberships, trainers, timings, facilities, or classes."
        
        elif intent == 'membership':
            response = "💪 **Membership Plans:**\n\n"
            for plan in self.gym_data['membership']['types']:
                response += f"**{plan['name']}** - {plan['price']}/{plan['duration']}\n"
                response += "Includes: " + ", ".join(plan['features']) + "\n\n"
            return response
        
        elif intent == 'trainer':
            trainer_info = self.gym_data['trainers']
            if trainer_info['available']:
                response = f"🏋️ **Personal Trainers Available!**\n\n"
                response += f"{trainer_info['info']}\n\n"
                response += f"**Specializations:** {', '.join(trainer_info['specializations'])}\n"
                response += f"**Pricing:** {trainer_info['pricing']}\n"
                response += f"**Booking:** {trainer_info['booking']}"
                return response
            else:
                return "Currently, personal trainers are not available."
        
        elif intent == 'timing':
            timings = self.gym_data['timings']
            response = "🕒 **Gym Timings:**\n\n"
            response += f"**Weekdays:** {timings['weekdays']}\n"
            response += f"**Weekends:** {timings['weekends']}\n"
            response += f"**Holidays:** {timings['holidays']}"
            return response
        
        elif intent == 'facilities':
            facilities = self.gym_data['facilities']
            response = "🏢 **Our Facilities:**\n\n"
            response += f"**Equipment:** {', '.join(facilities['equipment'])}\n\n"
            response += f"**Amenities:** {', '.join(facilities['amenities'])}"
            return response
        
        elif intent == 'classes':
            classes = self.gym_data['facilities']['classes']
            response = "🎯 **Available Classes:**\n\n"
            response += ", ".join(classes)
            response += "\n\nAll classes are included in your membership!"
            return response
        
        elif intent == 'contact':
            contact = self.gym_data['contact']
            response = "📞 **Contact Us:**\n\n"
            response += f"**Phone:** {contact['phone']}\n"
            response += f"**Email:** {contact['email']}\n"
            response += f"**Address:** {contact['address']}"
            return response
        
        elif intent == 'thanks':
            return "You're welcome! 😊 Feel free to ask anything else about our gym. Stay fit! 💪"
        
        else:
            return "I'm not sure I understand. You can ask me about:\n• Membership plans\n• Personal trainers\n• Gym timings\n• Facilities & equipment\n• Classes\n• Contact information"

# Test the chatbot (optional - for development)
if __name__ == "__main__":
    bot = GymChatbot()
    print("Gym Chatbot initialized successfully!")
    print(bot.get_response("What are the membership prices?"))
