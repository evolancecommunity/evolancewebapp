import google.generativeai as genai
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class GeminiEmotionAnalyzer:
    def __init__(self, api_key: str):
        """Initialize Gemini for emotion analysis and conversational AI."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.emotion_history = []
        
    def analyze_conversation_emotion(self, user_message: str, conversation_context: Optional[List[Dict]] = None) -> Dict:
        """
        Analyze user message for emotions and reasoning.
        Returns structured emotion data for emolytics.
        """
        if conversation_context is None:
            conversation_context = []
        prompt = f"""
        Analyze this user message for emotional content and reasoning.
        
        User Message: "{user_message}"
        
        Previous Context: {conversation_context[-3:] if conversation_context else "None"}
        
        Respond ONLY with a valid JSON object in the following format:
        {{
            "primary_emotion": "emotion_name",
            "emotion_intensity": 0-100,
            "secondary_emotions": ["emotion1", "emotion2"],
            "reasoning": "why they feel this way",
            "emotional_triggers": ["trigger1", "trigger2"],
            "confidence_score": 0-100,
            "timestamp": "current_timestamp"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            print("Gemini raw response:", response.text)  # Debug print
            emotion_data = json.loads(response.text)
            emotion_data['timestamp'] = datetime.now().isoformat()
            
            # Store in history for pattern analysis
            self.emotion_history.append(emotion_data)
            
            return emotion_data
            
        except Exception as e:
            print(f"Error analyzing emotion: {e}")
            return {
                "primary_emotion": "neutral",
                "emotion_intensity": 50,
                "secondary_emotions": [],
                "reasoning": "Unable to analyze",
                "emotional_triggers": [],
                "confidence_score": 0,
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_emotional_response(self, user_message: str, emotion_data: Dict, user_profile: Optional[Dict] = None) -> str:
        """
        Generate emotionally intelligent response based on user's emotional state.
        """
        if user_profile is None:
            user_profile = {}
        prompt = f"""
        You are an emotionally intelligent AI assistant for Evolance and your name is EV, an emotional wellness platform.
        
        User's emotional state: {emotion_data}
        User message: "{user_message}"
        User profile: {user_profile or {}}
        
        Generate a supportive, empathetic response that:
        1. Acknowledges their emotional state
        2. Provides emotional support
        3. Offers practical guidance if appropriate
        4. Maintains a warm, caring tone
        5. Encourages emotional awareness
        
        Keep the response conversational and under 150 words.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm here to support you. How are you feeling right now?"
    
    def analyze_emotional_patterns(self, user_id: str, time_period: str = "7d") -> Dict:
        """
        Analyze emotional patterns over time for emolytics insights.
        """
        if not self.emotion_history:
            return {"patterns": [], "insights": "No emotional data available"}
        
        recent_emotions = self.emotion_history[-50:]  # Last 50 interactions
        
        prompt = f"""
        Analyze these emotional data points for patterns and insights:
        {recent_emotions}
        
        Provide JSON response with:
        {{
            "dominant_emotions": ["emotion1", "emotion2"],
            "emotional_trends": "description of trends",
            "triggers_identified": ["trigger1", "trigger2"],
            "wellness_suggestions": ["suggestion1", "suggestion2"],
            "emotional_stability_score": 0-100,
            "recommendations": ["recommendation1", "recommendation2"]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"Error analyzing patterns: {e}")
            return {"patterns": [], "insights": "Unable to analyze patterns"}

class GeminiCoreAI:
    def __init__(self, api_key: str):
        """Initialize Gemini for core AI processing and emolytics updates."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
    
    def update_emolytics(self, user_id: str, emotion_data: Dict, conversation_context: List[Dict]) -> Dict:
        """
        Update user's emolytics based on conversation and emotion analysis.
        """
        prompt = f"""
        Update the user's emotional analytics based on this interaction:
        
        User ID: {user_id}
        Emotion Data: {emotion_data}
        Conversation Context: {conversation_context[-5:] if conversation_context else []}
        
        Generate updated emolytics data:
        {{
            "emotional_state": {{
                "current_emotion": "emotion_name",
                "intensity": 0-100,
                "stability": 0-100,
                "mood_trend": "improving/declining/stable"
            }},
            "emotional_insights": {{
                "primary_triggers": ["trigger1", "trigger2"],
                "coping_patterns": ["pattern1", "pattern2"],
                "emotional_strengths": ["strength1", "strength2"],
                "growth_areas": ["area1", "area2"]
            }},
            "recommendations": {{
                "immediate_actions": ["action1", "action2"],
                "long_term_strategies": ["strategy1", "strategy2"],
                "wellness_practices": ["practice1", "practice2"]
            }},
            "analytics_metrics": {{
                "emotional_variability": 0-100,
                "response_time_to_triggers": "fast/medium/slow",
                "emotional_awareness_score": 0-100,
                "wellness_progress": 0-100
            }}
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"Error updating emolytics: {e}")
            return {
                "emotional_state": {
                    "current_emotion": emotion_data.get("primary_emotion", "neutral"),
                    "intensity": emotion_data.get("emotion_intensity", 50),
                    "stability": 50,
                    "mood_trend": "stable"
                },
                "emotional_insights": {
                    "primary_triggers": [],
                    "coping_patterns": [],
                    "emotional_strengths": [],
                    "growth_areas": []
                },
                "recommendations": {
                    "immediate_actions": [],
                    "long_term_strategies": [],
                    "wellness_practices": []
                },
                "analytics_metrics": {
                    "emotional_variability": 50,
                    "response_time_to_triggers": "medium",
                    "emotional_awareness_score": 50,
                    "wellness_progress": 50
                }
            } 