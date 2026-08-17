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

    def predict_phrase(self, pattern, audio_context=""):
        """
        Predicts the user's intended phrase using the semantic intent,
        the time of day, and the ambient audio context (what the caregiver just said).
        """
        intent = self.intents.get(pattern)
        if not intent:
            return "Unknown Pattern"
            
        time_of_day = self.get_time_of_day()
        audio_context = audio_context.lower()
        
        self.history.append({"intent": intent, "time": time_of_day, "audio": audio_context})
        if len(self.history) > 10:
            self.history.pop(0)
            
        # --- 1. Multimodal Audio Context Overrides ---
        if audio_context:
            
            # --- Binary "OR" Questions (e.g. "water or food") ---
            if " or " in audio_context:
                parts = audio_context.split(" or ")
                if len(parts) >= 2:
                    # Extract the word right before and right after " or "
                    opt1 = parts[0].strip().split()[-1]
                    opt2 = parts[1].strip().split()[0].replace('?', '').replace('.', '')
                    
                    if intent == "social_comfort": # User blinked "S" -> Option 1
                        return f"I would prefer {opt1}."
                    elif intent == "negative_response": # User blinked "SS" -> Option 2
                        return f"I would prefer {opt2}."

            if "pain" in audio_context or "hurt" in audio_context or "scale" in audio_context:
                if intent == "social_comfort": # User blinked "Yes"
                    return "Yes, I am in a lot of pain right now."
                elif intent == "negative_response": # User blinked "No"
                    return "No, my pain is manageable."
                    
            if "cold" in audio_context or "blanket" in audio_context:
                if intent == "social_comfort":
                    return "Yes, please get me a blanket."
                elif intent == "negative_response":
                    return "No, my temperature is fine."
                    
            if "drink" in audio_context or "water" in audio_context:
                if intent == "social_comfort":
                    return "Yes, I would love some water."
                elif intent == "negative_response":
                    return "No, I am not thirsty."
        
        # --- 2. Standard Temporal Predictive Logic ---
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
