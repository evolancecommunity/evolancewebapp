<<<<<<< HEAD
=======
from transformers import pipeline

>>>>>>> neel
class EmotionService:
    def __init__(self):
        print("Loading emotion.....This might take a moment.")
        # Hi Neel please add your model best suited for emotion detection
<<<<<<< HEAD
        self.classifier("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
=======
        self.classifier = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
>>>>>>> neel
        print("Emotion model loaded")
    def detect_emotion(self, text: str) -> dict:
        """
        Detects emotion from text and returns a primary emotion and score.
        For simplicity, mapping 'POSITIVE' to 'joy', 'NEGATIVE' to 'sadness/anger', 'NEUTRAL' to 'calm'.
        """  
        if not text:
            return {"emotion": "neutral", "score": 1.0, "emojics": "😐"}

        result = self.classifier(text)[0]
        label = result['label']
        score = result['score']

        emotions_map = {
            "POSITIVE": {"emotion": "joy", "emojics": "😊"},
            "NEGATIVE": {"emotion": "sadness", "emojics": "😢"},
            "NEUTRAL": {"emotion": "calm", "emojics": "😐"}
        }

        if label == "NEGATIVE":
            # This is a simplification, in a real scenario you might want to differentiate between sadness and anger, true emotion detection
            if "frustration" in text.lower() or "anger" in text.lower() or "annoyance" in text.lower():
                mapped_emotion = "anger"
                emojics = "😡"
            else:
                mapped_emotion = "sadness"
                emojics = "😞"
        elif label == "POSITIVE":
            mapped_emotion = "joy"
            emojics = "😊"
        else:
            mapped_emotion = "calm"
            emojics = "😐"

        return {"emotion": mapped_emotion, "score": score, "emojics": emojics}
# Global instance of EmotionService to avoid reloading model on every request
emotion_service = EmotionService()