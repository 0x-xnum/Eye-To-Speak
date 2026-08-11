import time

class ContextPredictor:
    def __init__(self):
        # Intents map blink patterns to high-level categories
        self.intents = {
            "S": "social_comfort",
            "SS": "negative_response",
            "L": "physical_need",
            "LS": "sustenance",
            "LL": "positioning",
            "SL": "gratitude"
        }
        
        self.history = []

    def get_time_of_day(self):
        hour = time.localtime().tm_hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "night"

    def predict_phrase(self, pattern):
        """
        Takes a blink pattern and predicts the user's intended phrase
        based on the pattern's semantic intent and the current context (time of day).
        """
        intent = self.intents.get(pattern)
        if not intent:
            return "Unknown Pattern"
            
        time_of_day = self.get_time_of_day()
        
        # Save to history for potential future context matching
        self.history.append({"intent": intent, "time": time_of_day})
        if len(self.history) > 10:
            self.history.pop(0)
        
        # Predictive Logic based on Intent + Time of Day
        if intent == "physical_need":
            return "I need a nurse"
            
        elif intent == "sustenance":
            if time_of_day == "morning":
                return "I would like breakfast or coffee"
            elif time_of_day == "afternoon":
                return "I would like lunch or water"
            elif time_of_day == "evening":
                return "I would like dinner"
            else:
                return "I need water"
                
        elif intent == "positioning":
            if time_of_day == "night":
                return "Please help me lay down for bed"
            else:
                return "I am uncomfortable, please move me"
                
        elif intent == "social_comfort":
            if time_of_day == "morning":
                return "Good morning, yes"
            else:
                return "Yes"
                
        elif intent == "negative_response":
            return "No"
            
        elif intent == "gratitude":
            if time_of_day == "night":
                return "Thank you, good night"
            else:
                return "Thank you"
                
        return "Unknown Context"
