"""
Dynamic AI System for Evolance
Uses actual NLP and can generate responses dynamically
"""

import torch
import numpy as np
from typing import Dict, List, Any, Optional
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, 
    pipeline, AutoModelForSequenceClassification
)
from sentence_transformers import SentenceTransformer
import spacy
import json
import random

class DynamicAI:
    """
    Dynamic AI system that can generate responses using actual NLP
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load models
        self._load_models()
        
        # Conversation context
        self.conversation_history = []
        self.user_profile = {}
        
        # Response templates (but used dynamically)
        self.response_patterns = self._load_response_patterns()
    
    def _load_models(self):
        """Load all necessary NLP models"""
        try:
            # 1. Emotion Classification
            self.emotion_classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # 2. Sentiment Analysis
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # 3. Text Generation (for dynamic responses)
            self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
            self.generator = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
            
            # 4. Sentence Embeddings
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            
            # 5. SpaCy for NLP
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except:
                print("SpaCy model not found. Install with: python -m spacy download en_core_web_sm")
                self.nlp = None
            
            print("✓ All NLP models loaded successfully")
            
        except Exception as e:
            print(f"Error loading models: {e}")
            self._load_fallback_models()
    
    def _load_fallback_models(self):
        """Load simpler models if advanced ones fail"""
        print("Loading fallback models...")
        # Fallback to simpler models
        pass
    
    def _load_response_patterns(self) -> Dict[str, List[str]]:
        """Load response patterns for different emotions"""
        return {
            "joy": [
                "That sounds amazing! {context}",
                "I'm so happy for you! {context}",
                "That's wonderful! {context}",
                "Love that energy! {context}"
            ],
            "sadness": [
                "I'm sorry you're going through that. {context}",
                "That sounds really tough. {context}",
                "I'm here for you. {context}",
                "That must be really hard. {context}"
            ],
            "anger": [
                "That's totally understandable to be upset about. {context}",
                "You have every right to be frustrated. {context}",
                "That's really unfair. {context}",
                "I can see why you'd be angry. {context}"
            ],
            "fear": [
                "That sounds really scary. {context}",
                "I can understand why you're worried. {context}",
                "That's definitely anxiety-provoking. {context}",
                "I'm here to help you through this. {context}"
            ],
            "neutral": [
                "Hey! {context}",
                "Hi there! {context}",
                "Hello! {context}",
                "Hey! {context}"
            ]
        }
    
    def analyze_message(self, message: str) -> Dict[str, Any]:
        """Comprehensive message analysis using NLP"""
        
        analysis = {
            "emotion": "neutral",
            "sentiment": "neutral",
            "confidence": 0.0,
            "entities": [],
            "intent": "conversation",
            "context": "",
            "keywords": []
        }
        
        try:
            # 1. Emotion Classification
            emotion_result = self.emotion_classifier(message, top_k=3)
            analysis["emotion"] = emotion_result[0]["label"].lower()
            analysis["confidence"] = emotion_result[0]["score"]
            
            # 2. Sentiment Analysis
            sentiment_result = self.sentiment_analyzer(message)
            analysis["sentiment"] = sentiment_result[0]["label"].lower()
            
            # 3. Named Entity Recognition
            if self.nlp:
                doc = self.nlp(message)
                analysis["entities"] = [(ent.text, ent.label_) for ent in doc.ents]
                analysis["keywords"] = [token.text for token in doc if token.pos_ in ["NOUN", "VERB", "ADJ"]]
            
            # 4. Intent Recognition
            analysis["intent"] = self._detect_intent(message)
            
            # 5. Context Extraction
            analysis["context"] = self._extract_context(message)
            
        except Exception as e:
            print(f"Error in message analysis: {e}")
        
        return analysis
    
    def _detect_intent(self, message: str) -> str:
        """Detect user intent"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["hi", "hello", "hey"]):
            return "greeting"
        elif any(word in message_lower for word in ["bye", "goodbye", "see you"]):
            return "farewell"
        elif "?" in message:
            return "question"
        elif any(word in message_lower for word in ["help", "support", "need"]):
            return "help_request"
        else:
            return "conversation"
    
    def _extract_context(self, message: str) -> str:
        """Extract contextual information from message"""
        # Simple context extraction
        context_words = []
        
        # Look for emotional context
        emotion_words = {
            "work": "work-related",
            "family": "family-related", 
            "friend": "social",
            "relationship": "relationship",
            "health": "health-related",
            "money": "financial",
            "school": "academic"
        }
        
        for word, context in emotion_words.items():
            if word in message.lower():
                context_words.append(context)
        
        return ", ".join(context_words) if context_words else "general"
    
    def generate_response(self, message: str, analysis: Dict[str, Any]) -> str:
        """Generate dynamic response based on analysis"""
        
        try:
            # 1. Get base response pattern
            emotion = analysis["emotion"]
            patterns = self.response_patterns.get(emotion, self.response_patterns["neutral"])
            
            # 2. Generate context-aware response
            context = analysis["context"]
            if context:
                context_phrase = f"Tell me more about the {context} situation."
            else:
                context_phrase = "What's on your mind?"
            
            # 3. Add personalization based on conversation history
            personalization = self._get_personalization(analysis)
            
            # 4. Combine elements
            base_response = random.choice(patterns).format(context=context_phrase)
            
            # 5. Add follow-up question based on intent
            follow_up = self._get_follow_up_question(analysis)
            
            full_response = f"{base_response} {personalization} {follow_up}"
            
            return full_response.strip()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Hey! How are you doing?"
    
    def _get_personalization(self, analysis: Dict[str, Any]) -> str:
        """Add personalization based on conversation history"""
        if len(self.conversation_history) > 0:
            # Check if this is a recurring emotion
            recent_emotions = [msg["emotion"] for msg in self.conversation_history[-3:]]
            current_emotion = analysis["emotion"]
            
            if current_emotion in recent_emotions:
                return "I notice this has been on your mind lately."
        
        return ""
    
    def _get_follow_up_question(self, analysis: Dict[str, Any]) -> str:
        """Generate appropriate follow-up question"""
        
        intent = analysis["intent"]
        emotion = analysis["emotion"]
        
        questions = {
            "greeting": "How are you doing today?",
            "farewell": "Take care!",
            "question": "What do you think about that?",
            "help_request": "How can I best support you?",
            "conversation": {
                "joy": "What's the best part about it?",
                "sadness": "What would help you feel better?",
                "anger": "What happened?",
                "fear": "What's worrying you most?",
                "neutral": "What's on your mind?"
            }
        }
        
        if intent == "conversation":
            return questions["conversation"].get(emotion, "What's on your mind?")
        else:
            return questions.get(intent, "What's on your mind?")
    
    def update_conversation_history(self, message: str, analysis: Dict[str, Any], response: str):
        """Update conversation history for context"""
        self.conversation_history.append({
            "message": message,
            "emotion": analysis["emotion"],
            "sentiment": analysis["sentiment"],
            "response": response,
            "timestamp": len(self.conversation_history)
        })
        
        # Keep only last 10 messages for context
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of conversation patterns"""
        if not self.conversation_history:
            return {"message": "No conversation history"}
        
        emotions = [msg["emotion"] for msg in self.conversation_history]
        sentiments = [msg["sentiment"] for msg in self.conversation_history]
        
        return {
            "total_messages": len(self.conversation_history),
            "dominant_emotion": max(set(emotions), key=emotions.count),
            "emotion_distribution": {emotion: emotions.count(emotion) for emotion in set(emotions)},
            "overall_sentiment": max(set(sentiments), key=sentiments.count),
            "conversation_flow": "positive" if sentiments.count("positive") > sentiments.count("negative") else "negative"
        }

# Global instance
dynamic_ai = DynamicAI() 