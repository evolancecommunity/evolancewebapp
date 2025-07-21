from backend.server  import UserInput, AIResponse, EmotionData
from backend.services.emotion_service import emotion_service
from backend.services.ai_response_service import ai_response_service
from backend.models.data import PSYCHOLOGY_BOOKS, MEDITATION_BOOKS
from typing import Tuple

def generate_ai_response_text_and_emojics(user_input_message: str, detected_emotion:str) -> Tuple[str, str]:
    """
    Placeholder for generating the AI's textual response and specific emojics based on detected emotion.
    In a real AI, this would be a complex NLP model (e.g., LLM).
    Returns (ai_response_text, emojics_for_response)
    """
    text_lower  = user_input_message.lower()

    # Default response and emojics 
    ai_response_text = "Thank you for sharing. How can I assist you further?"
    emojics = "😊" 

    if detected_emotion == "joy":
        ai_response_text = "That's wonderful to hear! What made you feel so good?"
        emojics = "😄"

    elif detected_emotion == "sadness":
        ai_response_text ="I hear that you're feeling sad. Please tell me more, I'm here to listen." 
        emojics = "😔"   

    elif detected_emotion == "anger":
        ai_response_text = "I understand you're feeling angry. Please explain what's bothering you, and I'll do my best to assist." 
        emojics = "😠"

    elif detected_emotion =="calm":
        ai_response_text = "Alright. What's on your mind today?" 
        emojics = "😌"     

    if "hello" in text_lower or "hi" in text_lower:
        ai_response_text = "Hello there! How can I assist you today?"
        emojics = "👋"
    elif "help" in text_lower:
        ai_response_text = "I can help with various topics. What do you need assistance with?"  
        emojics = "💡"

    elif "bye" in text_lower or "goodbye" in text_lower:
        ai_response_text ="Goodbye! Have a great day."
        emojics = "👋"

    return ai_response_text, emojics

def process_user_input_for_ai_response(user_input: UserInput) -> AIResponse:
    """
    Orchestrates the full AI response generation, including emotion detection,
    reasoning, AI text, emojics, and book suggestions.The reason is directly from the EmotionService.
    """    
    
     # 1. Detect Emotion and Reason using the EmotionService
     # 2. Generate AI's Textual Response and Emojics based on detected emotion
     # 3. Get Book Suggestions
     # 4. Compile AIResponse

    detected_emotion_result = emotion_service.detect_emotion(user_input.message)
    detected_emotion_label = detected_emotion_result["emotion"]
    emotion_score = detected_emotion_result["score"]

    full_ai_response_data = ai_response_service.generate_response(user_input.message, detected_emotion_result)

    psychology_books = PSYCHOLOGY_BOOKS(detected_emotion_result)
    meditation_books = MEDITATION_BOOKS(detected_emotion_result)

    return AIResponse(
        ai_response = full_ai_response_data["ai_response"],
        emojics = full_ai_response_data["emojics"],
        detected_emotion = full_ai_response_data["detected_emotion"],
        reason_for_emotion = full_ai_response_data["reason_for_emotion"],
        suggested_psychology_books = psychology_books,
        suggested_meditation_books = meditation_books
    )
    
    







