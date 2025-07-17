
# AI Services - Neel

"""Reasoning: For this implementation, "reasoning" will be a rule-based inference based on detected emotion and keywords.
 A true AI reasoning engine would be far more complex 
 (e.g., using knowledge graphs or advanced LLMs with retrieval-augmented generation)."""

"""Response Generation: We'll use a simple rule-based approach combined with fetching relevant suggestions. 
For a more "conversational AI," you'd integrate a more advanced LLM 
(like a fine-tuned Llama, Mistral, or even OpenAI's GPT API if you're willing to use external services)."""


import random
from services.data_service import data_service

class AIResponseService:
    def __init__(self):
        self.psychology_books = data_service.get_psychology_books()
        self.meditation_books = data_service.get_meditation_books()

    def _get_relevant_books(self, emotion: str):
        psych_suggestions = []
        meditation_suggestions = []

        # Simple rule-based suggestions based on emotion
        if emotion in ["sadness", "anger"]:
            # Suggest books related to coping, self-compassion, emotional regulation
            psych_suggestions = [b for b in self.psychology_books if b['category'] in ['counselling', 'positive psychology', 'trauma', 'self-compassion']][:2]
            meditation_suggestions = [b for b in self.meditation_books if b['category'] in ['self-compassion', 'stress reduction', 'Buddhist philosophy', 'mindfulness']][:2]
        elif emotion == "joy":
            # Suggest books on deepening well-being, growth
            psych_suggestions = [b for b in self.psychology_books if b['category'] in ['positive psychology', 'general psychology']][:2]
            meditation_suggestions = [b for b in self.meditation_books if b['category'] in ['happiness', 'spiritual enlightenment', 'spiritual growth']][:2]
        else: # neutral/calm
            # General suggestions
            psych_suggestions = random.sample(self.psychology_books, min(2, len(self.psychology_books)))
            meditation_suggestions = random.sample(self.meditation_books, min(2, len(self.meditation_books)))

        return psych_suggestions, meditation_suggestions

    def generate_response(self, user_text: str, detected_emotion: dict) -> dict:
        emotion = detected_emotion["emotion"]
        emojics = detected_emotion["emojics"]
        response_text = ""
        reason_for_emotion = "Based on your words, it seems you're feeling {}. ".format(emotion) # Simplified reasoning

        psych_suggestions, meditation_suggestions = self._get_relevant_books(emotion)

        if emotion == "joy":
            response_text = f"That's wonderful to hear you're feeling {emotion}! {emojics} "
            response_text += "It sounds like you're experiencing a moment of positive well-being. "
            if psych_suggestions or meditation_suggestions:
                response_text += "To deepen this feeling, you might explore some insights from psychology or meditation. "
                if psych_suggestions:
                    response_text += f"For psychology, consider '{psych_suggestions[0]['title']}'. "
                if meditation_suggestions:
                    response_text += f"And for meditation, '{meditation_suggestions[0]['title']}' could be insightful."
        elif emotion == "sadness":
            response_text = f"I'm sorry to hear you're feeling {emotion}. {emojics} It's okay to feel this way. "
            response_text += "Sometimes, understanding our emotions can help. "
            if psych_suggestions or meditation_suggestions:
                response_text += "Perhaps exploring these resources could offer some comfort or perspective: "
                if psych_suggestions:
                    response_text += f"In psychology, '{psych_suggestions[0]['title']}' might provide understanding. "
                if meditation_suggestions:
                    response_text += f"And for inner peace, try '{meditation_suggestions[0]['title']}'. "
            response_text += "Remember, taking a moment to breathe deeply can sometimes help."
        elif emotion == "anger":
            response_text = f"It sounds like you're experiencing some {emotion}. {emojics} That's a powerful emotion. "
            response_text += "It's important to acknowledge these feelings. "
            if psych_suggestions or meditation_suggestions:
                response_text += "Exploring healthy ways to process this emotion is key. "
                if psych_suggestions:
                    response_text += f"For insights into emotional regulation, '{psych_suggestions[0]['title']}' could be useful. "
                if meditation_suggestions:
                    response_text += f"And to find a sense of calm, '{meditation_suggestions[0]['title']}' might offer techniques."
        else: # calm / neutral
            response_text = f"Hello there! {emojics} How can I assist you today? "
            response_text += "I can share insights from psychology and meditation to help with well-being."
            if psych_suggestions and meditation_suggestions:
                response_text += f" For a general read, you might like '{psych_suggestions[0]['title']}' (psychology) or '{meditation_suggestions[0]['title']}' (meditation)."

        return {
            "ai_response": response_text,
            "emojics": emojics,
            "detected_emotion": emotion,
            "reason_for_emotion": reason_for_emotion + "Would you like to elaborate more on why you're feeling this way?",
            "suggested_psych_books": psych_suggestions,
            "suggested_meditation_books": meditation_suggestions
        }

# Global instance
ai_response_service = AIResponseService()