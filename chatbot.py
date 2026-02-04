import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

class GymChatbot:
    def __init__(self, data_file='data/gym_data.json'):
        # Load gym data
        with open(data_file, 'r') as f:
            self.gym_data = json.load(f)
        
        # Initialize NLTK tools
        self.lemmatizer = WordNetLemmatizer()
        
        # Define keyword patterns for different queries
        self.patterns = {
            'membership': ['membership', 'member', 'plan', 'subscription', 'price', 'cost', 'fee', 'package'],
            'trainer': ['trainer', 'coach', 'personal training', 'pt', 'instructor'],
            'timing': ['time', 'timing', 'hours', 'open', 'close', 'schedule', 'when'],
            'facilities': ['facility', 'facilities', 'equipment', 'amenity', 'amenities', 'what available'],
            'classes': ['class', 'classes', 'group', 'session', 'workout'],
            'contact': ['contact', 'phone', 'email', 'address', 'location', 'reach'],
            'greeting': ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon'],
            'thanks': ['thanks', 'thank you', 'appreciate', 'grateful']
        }
    
    def preprocess_text(self, text):
        """Clean and prepare text for processing"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # Tokenize
        tokens = word_tokenize(text)
        # Lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        return tokens
    
    def detect_intent(self, user_input):
        """Detect what the user is asking about"""
        tokens = self.preprocess_text(user_input)
        
        # Check each pattern category
        for intent, keywords in self.patterns.items():
            for keyword in keywords:
                keyword_tokens = self.preprocess_text(keyword)
                # Check if keyword matches any token
                if any(kt in tokens for kt in keyword_tokens):
                    return intent
        
        return 'unknown'
    
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