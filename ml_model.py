from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

def get_event_emotion(event_text:str = ""):
    """
    Analyzes the sentiment of the given event text and returns the sentiment label.
    
    Args:
        event_text (str): The text of the event to analyze.
        
    Returns:
        str: The sentiment label (e.g., 'POSITIVE', 'NEGATIVE', 'NEUTRAL').
    """
    if not event_text:
        return "NEUTRAL"
    
    result = sentiment_pipeline(event_text)
    return result[0]['label']
