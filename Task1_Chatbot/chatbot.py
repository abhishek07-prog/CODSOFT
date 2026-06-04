import random
from datetime import datetime

class Chatbot:
    def __init__(self, name="ChatBot"):
        self.name = name
        self.conversation_count = 0
        self.user_name = None

        print(f" {self.name} initialized successfully!")

    #Responses

    greetings = [
        "Hello there! How can I help you today?",
        "Hi! It's great to meet you! What can I do for you?",
        "Hey! Welcome! How are you doing?",
        "Greetings! Nice to see you! What's on your mind?",
    ]

    how_are_you = [
        "I'm doing great, thanks for asking! :)",
        "I'm functioning perfectly! Ready to help you.",
        "All systems go! How can I assist you?",
        "I'm excellent! Hope you're having a great day too!",
    ]

    farewells = [
        "Goodbye! It was nice talking to you! :)",
        "See you later! Take care!",
        "Bye for now! Come back anytime!",
        "Farewell! Hope I helped you today!",
    ]

    help_responses = [
        "I can help you with:\n"
        "⦁ Answering questions\n"
        "⦁ Having a conversation\n"
        "⦁ Providing information\n"
        "Just type what you need!",

        "I'm here to help! You can ask me about:\n"
        "⦁ Weather, time, date\n"
        "⦁ General knowledge\n"
        "⦁ Or just chat! :)",

        "Here's what I can do:\n"
        "1. Answer questions\n"
        "2. Have a friendly chat\n"
        "3. Tell you the time or date\n"
        "Just ask!",
    ]

    time_responses = [
        "The current time is ",
        "Right now it's ",
        "It's ",
    ]

    thanks_responses = [
        "You're welcome! Happy to help! :)",
        "No problem at all! Anything else?",
        "Glad I could help! Feel free to ask more!",
        "You're welcome! That's what I'm here for!",
    ]

    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛😂",
        "Why did the Python developer go broke? Because he didn't know how to 'close' his files! 💸",
        "A SQL Query walks into a bar, walks up to two tables and asks... 'Can I join you?' 🍺😂",
        "Why do Java developers wear glasses? Because they can't C#! 👓😂",
        "What do you call a fake noodle? An impasta! 🍝😂",
    ]

    #Keyword matching rules

    def process_input(self, user_message):
        self.conversation_count +=1
        message = user_message.lower().strip()

        if not message:
            return "Please say something!"

        #Rule 1: greetings
        if self._match_keywords(message, ["hello", "hi", "hey", "greetings", "hey there", "hi there"]):
            return self._get_random_response(self.greetings)

        #Rule 2: How are You
        if self._match_keywords(message, ["how are you", "how do you do", "how are you doing"]):
            return self._get_random_response(self.how_are_you)

        #Rule 3: Farewells 
        if self._match_keywords(message, ["bye","goodbye","see you","later","farewell","take care"]):
            return self._get_random_response(self.farewells) 

        #Rule 4: Help
        if self._match_keywords(message, ["help","what can you do","commands","instructions"]):
            return self._get_random_response(self.help_responses)

        #Rule 5: Thank You
        if self._match_keywords(message, ["thanks","thank you","thx","appreciate","grateful"]):
            return self._get_random_response(self.thanks_responses)

        #Rule 6: Ask for time
        if self._match_keywords(message, ["time","what time is it","current time"]):
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}"

        #Rule 7: Ask for Date
        if self._match_keywords(message, ["date","what date is it","today","current_date"]):
            current_date = datetime.now().strftime("%B %d, %Y")
            return f"Today's date is {current_date}"

        #Rule 8: Tell a joke
        if self._match_keywords(message, ["joke","funny","make me laugh","tell me a joke"]):
            return self._get_random_response(self.jokes)

        #Rule 9: About Bot
        if self._match_keywords(message, ["who are you","what are you","about you","your name"]):
            return (
                f"I'm {self.name}, a friendly rule-based chatbot! \n"
                f"I was built using Python and customtkinter.\n"
                f"I can chat, answer questions, tell jokes, and more!"
            )

        #Default: Fallback Response
        return self._get_fallback()

    #Helper Functions

    def _match_keywords(self, message, keywords):
        for keyword in keywords:
            if keyword in message:
                return True
        return False
        
    def _get_random_response(self, response_list):
        return random.choice(response_list)

    def _get_fallback(self):
        fallbacks = [
            "I'm not sure I understand that. Can you try asking differently?",
            "Interesting! Tell me more about that.",
            "Hmm, I'm not sure how to respond to that. Try asking about something else!",
            "I hear you! But I'm having trouble understanding. Can you rephrase?",
            "That's a new one! Could you tell me what you need help with?",
            "I see! Would you like to hear a joke instead?",
        ]
        return self._get_random_response(fallbacks)

    #Utility methods

    def get_conversation_count(self):
        #Return how many messages have been exchanged
        return self.conversation_count

    def reset(self):
        #Reset the chatbot's session
        self.conversation_count = 0
        self.user_name = None
        print(f"{self.name} session reset!")