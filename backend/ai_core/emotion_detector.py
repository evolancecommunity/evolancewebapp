"""
Evolance Emotion Detection System
Advanced emotion analysis using multiple NLP techniques
"""

import re
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from collections import defaultdict
import time

# We'll use transformers for emotion classification
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: Transformers not available. Using rule-based emotion detection.")

from .config import config

@dataclass
class EmotionResult:
    """Result of emotion detection"""
    primary_emotion: str
    confidence: float
    all_emotions: Dict[str, float]
    intensity: float
    valence: float
    arousal: float
    body_sensations: List[str]
    triggers: List[str]
    context: Dict[str, Any]

class EmotionDetector:
    """
    Advanced emotion detection system for Evolance
    Combines multiple techniques for robust emotion analysis
    """
    
    def __init__(self):
        self.emotion_keywords = self._load_emotion_keywords()
        self.intensity_indicators = self._load_intensity_indicators()
        self.body_sensation_patterns = self._load_body_patterns()
        
        # Initialize ML models if available
        self.sentiment_pipeline = None
        self.emotion_classifier = None
        self._initialize_models()
    
    def _load_emotion_keywords(self) -> Dict[str, List[str]]:
        """Load emotion keywords for rule-based detection"""
        return {
            "joy": [
                "happy", "excited", "thrilled", "delighted", "ecstatic", "elated",
                "joyful", "cheerful", "pleased", "content", "satisfied", "grateful",
                "blessed", "fortunate", "lucky", "amazing", "wonderful", "fantastic",
                "great", "awesome", "brilliant", "excellent", "perfect"
            ],
            "sadness": [
                "sad", "depressed", "melancholy", "grief", "sorrow", "heartbroken",
                "devastated", "crushed", "hopeless", "despair", "lonely", "isolated",
                "abandoned", "rejected", "worthless", "useless", "empty", "numb",
                "bad", "terrible", "awful", "miserable", "unhappy"
            ],
            "anger": [
                "angry", "furious", "rage", "irritated", "annoyed", "frustrated",
                "mad", "livid", "outraged", "enraged", "hostile", "aggressive",
                "bitter", "resentful", "hate", "despise", "loathe", "disgusted",
                "upset", "pissed", "fuming", "seething"
            ],
            "fear": [
                "afraid", "scared", "terrified", "panicked", "anxious", "worried",
                "nervous", "tense", "stressed", "overwhelmed", "frightened", "horrified",
                "petrified", "alarmed", "distressed", "uneasy", "apprehensive",
                "anxiety", "panic", "dread", "fearful"
            ],
            "trust": [
                "trust", "confident", "secure", "safe", "protected", "supported",
                "reliable", "dependable", "faithful", "loyal", "devoted", "committed"
            ],
            "surprise": [
                "surprised", "shocked", "amazed", "astonished", "stunned", "bewildered",
                "confused", "perplexed", "puzzled", "startled", "taken_aback",
                "wow", "omg", "unexpected", "sudden"
            ],
            "disgust": [
                "disgusted", "repulsed", "revolted", "sickened", "nauseated", "appalled",
                "horrified", "offended", "outraged", "contempt", "scorn"
            ],
            "anticipation": [
                "excited", "eager", "enthusiastic", "hopeful", "optimistic", "looking_forward",
                "anticipating", "expecting", "waiting", "prepared", "ready"
            ],
            "love": [
                "love", "adore", "cherish", "treasure", "affection", "fondness",
                "devotion", "passion", "romance", "intimacy", "connection"
            ],
            "optimism": [
                "optimistic", "hopeful", "positive", "confident", "assured", "certain",
                "upbeat", "cheerful", "bright", "promising", "encouraging"
            ],
            "neutral": [
                "hi", "hello", "hey", "goodbye", "bye", "thanks", "thank you",
                "okay", "ok", "fine", "alright", "sure", "yes", "no", "maybe",
                "how", "what", "when", "where", "why", "who", "which", "are", "is", "am",
                "doing", "going", "feeling", "thinking", "wondering", "asking"
            ]
        }
    
    def _load_intensity_indicators(self) -> Dict[str, List[str]]:
        """Load intensity indicators for emotion analysis"""
        return {
            "high_intensity": [
                "extremely", "absolutely", "completely", "totally", "utterly",
                "incredibly", "massively", "overwhelmingly", "intensely", "deeply"
            ],
            "medium_intensity": [
                "very", "quite", "rather", "pretty", "fairly", "somewhat",
                "moderately", "reasonably", "adequately"
            ],
            "low_intensity": [
                "slightly", "a_bit", "somewhat", "kind_of", "sort_of",
                "mildly", "gently", "softly"
            ],
            "negation": [
                "not", "no", "never", "none", "neither", "nor", "hardly",
                "barely", "scarcely", "rarely"
            ]
        }
    
    def _load_body_patterns(self) -> Dict[str, List[str]]:
        """Load body sensation patterns"""
        return {
            "chest": [
                "chest", "heart", "breast", "lungs", "ribs", "sternum",
                "heart_racing", "heart_pounding", "chest_tight", "chest_heavy"
            ],
            "head": [
                "head", "brain", "mind", "thoughts", "headache", "migraine",
                "dizzy", "lightheaded", "foggy", "clear_minded"
            ],
            "stomach": [
                "stomach", "gut", "belly", "abdomen", "nausea", "butterflies",
                "knot_in_stomach", "stomach_churning", "digestive"
            ],
            "throat": [
                "throat", "neck", "voice", "choking", "lump_in_throat",
                "tight_throat", "dry_throat"
            ],
            "limbs": [
                "arms", "legs", "hands", "feet", "fingers", "toes",
                "shaking", "trembling", "weak", "strong", "energetic"
            ]
        }
    
    def _initialize_models(self):
        """Initialize ML models for emotion detection"""
        if not TRANSFORMERS_AVAILABLE:
            return
        
        try:
            # Sentiment analysis pipeline
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Emotion classification pipeline
            self.emotion_classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                device=0 if torch.cuda.is_available() else -1
            )
            
        except Exception as e:
            print(f"Warning: Could not initialize ML models: {e}")
            self.sentiment_pipeline = None
            self.emotion_classifier = None
    
    def detect_emotions(self, text: str, context: Dict[str, Any] = None) -> EmotionResult:
        """
        Detect emotions in text using multiple techniques
        Returns comprehensive emotion analysis
        """
        
        # Preprocess text
        processed_text = self._preprocess_text(text)
        
        # Get emotion scores from different methods
        rule_based_scores = self._rule_based_detection(processed_text)
        ml_scores = self._ml_based_detection(processed_text) if self.emotion_classifier else {}
        
        # Combine scores
        combined_scores = self._combine_scores(rule_based_scores, ml_scores)
        
        # Get primary emotion
        primary_emotion = max(combined_scores.items(), key=lambda x: x[1])[0]
        confidence = combined_scores[primary_emotion]
        
        # Calculate intensity and dimensions
        intensity = self._calculate_intensity(processed_text, combined_scores)
        valence, arousal = self._calculate_dimensions(primary_emotion, intensity)
        
        # Detect body sensations
        body_sensations = self._detect_body_sensations(processed_text)
        
        # Identify triggers
        triggers = self._identify_triggers(processed_text, context)
        
        return EmotionResult(
            primary_emotion=primary_emotion,
            confidence=confidence,
            all_emotions=combined_scores,
            intensity=intensity,
            valence=valence,
            arousal=arousal,
            body_sensations=body_sensations,
            triggers=triggers,
            context=context or {}
        )
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for emotion detection"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove punctuation that might interfere
        text = re.sub(r'[^\w\s]', ' ', text)
        
        return text
    
    def _rule_based_detection(self, text: str) -> Dict[str, float]:
        """Rule-based emotion detection using keywords"""
        scores = defaultdict(float)
        words = text.split()
        
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in words:
                    # Base score for keyword match
                    base_score = 0.3
                    
                    # Check for intensity modifiers
                    intensity_multiplier = self._get_intensity_multiplier(text, keyword)
                    
                    # Check for negation
                    negation_factor = self._get_negation_factor(text, keyword)
                    
                    scores[emotion] += base_score * intensity_multiplier * negation_factor
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            scores = {emotion: score / total_score for emotion, score in scores.items()}
        else:
            # If no emotion detected, default to neutral
            scores = {"neutral": 1.0}
        
        return dict(scores)
    
    def _ml_based_detection(self, text: str) -> Dict[str, float]:
        """ML-based emotion detection using transformers"""
        if not self.emotion_classifier:
            return {}
        
        try:
            results = self.emotion_classifier(text, top_k=5)
            scores = {}
            
            for result in results:
                emotion = result['label'].lower()
                score = result['score']
                
                # Map ML model emotions to our emotion set
                mapped_emotion = self._map_ml_emotion(emotion)
                if mapped_emotion:
                    scores[mapped_emotion] = score
            
            return scores
            
        except Exception as e:
            print(f"ML emotion detection failed: {e}")
            return {}
    
    def _map_ml_emotion(self, ml_emotion: str) -> Optional[str]:
        """Map ML model emotions to our emotion set"""
        mapping = {
            'joy': 'joy',
            'sadness': 'sadness',
            'anger': 'anger',
            'fear': 'fear',
            'surprise': 'surprise',
            'disgust': 'disgust',
            'love': 'love',
            'optimism': 'optimism',
            'trust': 'trust',
            'anticipation': 'anticipation'
        }
        return mapping.get(ml_emotion)
    
    def _combine_scores(self, rule_scores: Dict[str, float], ml_scores: Dict[str, float]) -> Dict[str, float]:
        """Combine rule-based and ML-based scores"""
        combined = defaultdict(float)
        
        # Add rule-based scores
        for emotion, score in rule_scores.items():
            combined[emotion] += score * 0.4  # 40% weight
        
        # Add ML-based scores
        for emotion, score in ml_scores.items():
            combined[emotion] += score * 0.6  # 60% weight
        
        # Normalize
        total = sum(combined.values())
        if total > 0:
            combined = {emotion: score / total for emotion, score in combined.items()}
        
        return dict(combined)
    
    def _get_intensity_multiplier(self, text: str, keyword: str) -> float:
        """Get intensity multiplier based on modifiers around keyword"""
        words = text.split()
        try:
            keyword_index = words.index(keyword)
            
            # Check words before and after keyword
            for i in range(max(0, keyword_index - 2), min(len(words), keyword_index + 3)):
                if i == keyword_index:
                    continue
                
                word = words[i]
                if word in self.intensity_indicators["high_intensity"]:
                    return 2.0
                elif word in self.intensity_indicators["medium_intensity"]:
                    return 1.5
                elif word in self.intensity_indicators["low_intensity"]:
                    return 0.7
            
            return 1.0
            
        except ValueError:
            return 1.0
    
    def _get_negation_factor(self, text: str, keyword: str) -> float:
        """Get negation factor based on negating words around keyword"""
        words = text.split()
        try:
            keyword_index = words.index(keyword)
            
            # Check words before keyword for negation
            for i in range(max(0, keyword_index - 3), keyword_index):
                if words[i] in self.intensity_indicators["negation"]:
                    return 0.3  # Reduce score for negation
            
            return 1.0
            
        except ValueError:
            return 1.0
    
    def _calculate_intensity(self, text: str, emotion_scores: Dict[str, float]) -> float:
        """Calculate overall emotional intensity"""
        # Base intensity from emotion scores
        base_intensity = max(emotion_scores.values()) if emotion_scores else 0.0
        
        # Intensity from text features
        text_intensity = 0.0
        
        # Exclamation marks
        exclamation_count = text.count('!')
        text_intensity += min(exclamation_count * 0.1, 0.3)
        
        # ALL CAPS words
        caps_words = re.findall(r'\b[A-Z]{2,}\b', text)
        text_intensity += min(len(caps_words) * 0.05, 0.2)
        
        # Intensity words
        intensity_words = sum(1 for word in text.split() 
                            if word in self.intensity_indicators["high_intensity"])
        text_intensity += min(intensity_words * 0.1, 0.3)
        
        # Combine base and text intensity
        return min(base_intensity + text_intensity, 1.0)
    
    def _calculate_dimensions(self, primary_emotion: str, intensity: float) -> Tuple[float, float]:
        """Calculate valence and arousal dimensions"""
        # Base dimensions for emotions (from Russell's circumplex)
        emotion_dimensions = {
            "joy": (0.8, 0.6),
            "sadness": (-0.8, 0.2),
            "anger": (-0.5, 0.9),
            "fear": (-0.7, 0.8),
            "surprise": (0.0, 0.9),
            "disgust": (-0.6, 0.4),
            "trust": (0.6, 0.3),
            "anticipation": (0.4, 0.7),
            "love": (0.9, 0.5),
            "optimism": (0.7, 0.6)
        }
        
        base_valence, base_arousal = emotion_dimensions.get(primary_emotion, (0.0, 0.5))
        
        # Adjust based on intensity
        valence = base_valence * intensity
        arousal = base_arousal * intensity
        
        return valence, arousal
    
    def _detect_body_sensations(self, text: str) -> List[str]:
        """Detect body sensations mentioned in text"""
        sensations = []
        
        for body_part, patterns in self.body_sensation_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    sensations.append(body_part)
                    break
        
        return list(set(sensations))
    
    def _identify_triggers(self, text: str, context: Dict[str, Any] = None) -> List[str]:
        """Identify potential emotional triggers"""
        triggers = []
        
        # Common trigger words
        trigger_words = [
            "because", "since", "when", "after", "before", "during",
            "due_to", "caused_by", "triggered_by", "made_me", "got_me"
        ]
        
        words = text.split()
        for i, word in enumerate(words):
            if word in trigger_words and i + 1 < len(words):
                # Extract potential trigger
                trigger = " ".join(words[i+1:i+3])  # Next 2 words
                triggers.append(trigger)
        
        return triggers
    
    def get_sentiment(self, text: str) -> Dict[str, float]:
        """Get sentiment analysis using ML model"""
        if not self.sentiment_pipeline:
            return {"positive": 0.5, "negative": 0.5, "neutral": 0.0}
        
        try:
            result = self.sentiment_pipeline(text)[0]
            label = result['label'].lower()
            score = result['score']
            
            if label == 'positive':
                return {"positive": score, "negative": 1-score, "neutral": 0.0}
            elif label == 'negative':
                return {"positive": 1-score, "negative": score, "neutral": 0.0}
            else:
                return {"positive": 0.0, "negative": 0.0, "neutral": score}
                
        except Exception as e:
            print(f"Sentiment analysis failed: {e}")
            return {"positive": 0.5, "negative": 0.5, "neutral": 0.0}

# Global emotion detector instance
emotion_detector = EmotionDetector() 