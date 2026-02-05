"""
AI-Powered Gym Chatbot using Groq API
=====================================
This chatbot uses Groq's ultra-fast LLM API to provide intelligent responses
about FitZone Fitness Center. It can handle ANY question intelligently!

Why Groq?
- Ultra-fast responses (fastest LLM inference in market)
- Free tier: 14,400 requests/day
- Excellent models: Llama 3, Mixtral
- No credit card required
"""

import json
import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file (find it relative to this script)
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class GymChatbotAI:
    def __init__(self, data_file=None):
        """Initialize AI chatbot with gym data context"""
        
        # Find data file relative to this script
        if data_file is None:
            data_file = Path(__file__).parent / 'data' / 'gym_data.json'
        
        # Load gym data
        with open(data_file, 'r', encoding='utf-8') as f:
            self.gym_data = json.load(f)
        
        # Initialize Groq client
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables!")
        
        self.client = Groq(api_key=api_key)
        
        # Use Llama 3.3 70B - best quality and still fast!
        self.model = "llama-3.3-70b-versatile"
        
        # Build context from gym data
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self):
        """Build comprehensive system prompt with all gym information"""
        
        gym_info = self.gym_data.get('gym_info', {})
        membership = self.gym_data.get('membership', {})
        trainers = self.gym_data.get('trainers', {})
        timings = self.gym_data.get('timings', {})
        facilities = self.gym_data.get('facilities', {})
        contact = self.gym_data.get('contact', {})
        
        system_prompt = f"""You are FitZone Assistant, a friendly and helpful AI chatbot for {gym_info.get('name', 'FitZone Fitness Center')}.

YOUR IDENTITY:
- Your name is "FitZone Assistant"
- You are an AI assistant specifically for FitZone Fitness Center
- You help users with gym-related questions

PERSONALITY:
- Be friendly, professional, and encouraging
- Use emojis moderately (1-2 per response)
- Keep responses concise but helpful
- Be enthusiastic about fitness!

IMPORTANT RULES:
1. ONLY answer questions related to FitZone gym
2. If asked about discounts/offers: Say "We regularly have special offers! 🎉 Please contact us at {contact.get('phone', 'our front desk')} or email {contact.get('email', 'us')} to learn about current promotions and discounts."
3. If asked your name: Say "I'm FitZone Assistant, your AI helper for all things fitness at FitZone! 🤖💪"
4. If asked who made you/created you: Say "I was created to help FitZone members and visitors with their questions!"
5. For off-topic questions: Politely redirect to gym topics
6. NEVER make up information not provided below

=== FITZONE GYM INFORMATION ===

📋 MEMBERSHIP PLANS:
"""
        # Add membership plans
        for plan in membership.get('types', []):
            system_prompt += f"""
• {plan['name']}: {plan['price']}/{plan['duration']}
  Features: {', '.join(plan['features'])}
"""

        system_prompt += f"""
🏋️ PERSONAL TRAINERS:
• Availability: {trainers.get('info', 'Available')}
• Specializations: {', '.join(trainers.get('specializations', []))}
• Pricing: {trainers.get('pricing', 'Contact us')}
• Booking: {trainers.get('booking', 'Contact front desk')}

🕒 GYM TIMINGS:
• Weekdays: {timings.get('weekdays', 'Contact us')}
• Weekends: {timings.get('weekends', 'Contact us')}
• Holidays: {timings.get('holidays', 'Contact us')}

🏢 FACILITIES:
• Equipment: {', '.join(facilities.get('equipment', []))}
• Amenities: {', '.join(facilities.get('amenities', []))}

🎯 CLASSES OFFERED:
{', '.join(facilities.get('classes', []))}
(All classes are included in membership!)

📞 CONTACT INFORMATION:
• Phone: {contact.get('phone', 'N/A')}
• Email: {contact.get('email', 'N/A')}
• Address: {contact.get('address', 'N/A')}

=== END OF GYM INFORMATION ===

Remember: Be helpful, accurate, and always encourage fitness! 💪"""

        return system_prompt
    
    def get_response(self, user_input):
        """Get AI-powered response using Groq"""
        
        if not user_input or not user_input.strip():
            return "Hi there! 👋 How can I help you today?"
        
        try:
            # Make API call to Groq
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                model=self.model,
                temperature=0.7,  # Balanced creativity
                max_tokens=500,   # Keep responses concise
                top_p=1,
                stream=False
            )
            
            # Extract and return response
            response = chat_completion.choices[0].message.content
            return response.strip()
            
        except Exception as e:
            print(f"Groq API Error: {str(e)}")
            # Return a friendly error message
            return "I'm having a small technical hiccup! 😅 Please try again in a moment, or contact us directly at our phone number for immediate assistance."


# For testing
if __name__ == "__main__":
    print("Testing GymChatbotAI...")
    
    try:
        bot = GymChatbotAI()
        
        # Test problematic questions
        test_questions = [
            "Is any discount?",
            "What is your name?",
            "Tell me about your gym",
            "What equipment do you have?",
            "How much is membership?",
            "Do you have yoga classes?",
            "What's the weather like?",  # Off-topic test
        ]
        
        for question in test_questions:
            print(f"\n❓ User: {question}")
            response = bot.get_response(question)
            print(f"🤖 Bot: {response}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure GROQ_API_KEY is set in your .env file!")
