import json
import pickle
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

class ProgressiveLearningSystem:
    def __init__(self, model_dir: str = "ai_models"):
        """Initialize the progressive learning system."""
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        
        # Core models
        self.emotion_classifier = None
        self.response_generator = None
        self.emolytics_analyzer = None
        
        # Training data storage
        self.training_data = {
            "emotion_data": [],
            "conversation_pairs": [],
            "emolytics_patterns": []
        }
        
        # Learning metrics
        self.learning_metrics = {
            "total_interactions": 0,
            "model_confidence": 0.0,
            "last_training": None,
            "training_frequency": 100,  # Retrain every 100 interactions
            "independence_threshold": 0.85  # Confidence threshold for independence
        }
        
        # Load existing models if available
        self.load_models()
    
    def load_models(self):
        """Load existing trained models."""
        try:
            if os.path.exists(f"{self.model_dir}/emotion_classifier.pkl"):
                self.emotion_classifier = joblib.load(f"{self.model_dir}/emotion_classifier.pkl")
                print("✅ Loaded existing emotion classifier")
            
            if os.path.exists(f"{self.model_dir}/response_generator.pkl"):
                self.response_generator = joblib.load(f"{self.model_dir}/response_generator.pkl")
                print("✅ Loaded existing response generator")
                
            if os.path.exists(f"{self.model_dir}/emolytics_analyzer.pkl"):
                self.emolytics_analyzer = joblib.load(f"{self.model_dir}/emolytics_analyzer.pkl")
                print("✅ Loaded existing emolytics analyzer")
                
        except Exception as e:
            print(f"⚠️ Could not load existing models: {e}")
    
    def save_models(self):
        """Save trained models."""
        try:
            if self.emotion_classifier:
                joblib.dump(self.emotion_classifier, f"{self.model_dir}/emotion_classifier.pkl")
            
            if self.response_generator:
                joblib.dump(self.response_generator, f"{self.model_dir}/response_generator.pkl")
                
            if self.emolytics_analyzer:
                joblib.dump(self.emolytics_analyzer, f"{self.model_dir}/emolytics_analyzer.pkl")
                
            # Save training data
            with open(f"{self.model_dir}/training_data.json", 'w') as f:
                json.dump(self.training_data, f, indent=2)
                
            # Save learning metrics
            with open(f"{self.model_dir}/learning_metrics.json", 'w') as f:
                json.dump(self.learning_metrics, f, indent=2)
                
            print("✅ Models and data saved successfully")
            
        except Exception as e:
            print(f"❌ Error saving models: {e}")
    
    def collect_training_data(self, user_message: str, gemini_emotion_data: Dict, 
                            gemini_response: str, gemini_emolytics: Dict):
        """Collect training data from Gemini interactions."""
        
        # Store emotion classification data
        emotion_sample = {
            "text": user_message,
            "primary_emotion": gemini_emotion_data.get("primary_emotion", "neutral"),
            "intensity": gemini_emotion_data.get("emotion_intensity", 50),
            "secondary_emotions": gemini_emotion_data.get("secondary_emotions", []),
            "triggers": gemini_emotion_data.get("emotional_triggers", []),
            "timestamp": datetime.now().isoformat()
        }
        self.training_data["emotion_data"].append(emotion_sample)
        
        # Store conversation pairs for response generation
        conversation_sample = {
            "user_input": user_message,
            "ai_response": gemini_response,
            "emotion_context": gemini_emotion_data,
            "timestamp": datetime.now().isoformat()
        }
        self.training_data["conversation_pairs"].append(conversation_sample)
        
        # Store emolytics patterns
        emolytics_sample = {
            "emotion_data": gemini_emotion_data,
            "emolytics_update": gemini_emolytics,
            "timestamp": datetime.now().isoformat()
        }
        self.training_data["emolytics_patterns"].append(emolytics_sample)
        
        # Update metrics
        self.learning_metrics["total_interactions"] += 1
        
        # Check if it's time to retrain
        if self.learning_metrics["total_interactions"] % self.learning_metrics["training_frequency"] == 0:
            self.train_models()
    
    def train_emotion_classifier(self):
        """Train emotion classification model."""
        if len(self.training_data["emotion_data"]) < 50:
            print("⚠️ Need more training data for emotion classifier")
            return
        
        # Prepare training data
        texts = [sample["text"] for sample in self.training_data["emotion_data"]]
        emotions = [sample["primary_emotion"] for sample in self.training_data["emotion_data"]]
        
        # Vectorize text
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        X = vectorizer.fit_transform(texts)
        y = emotions
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        self.emotion_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.emotion_classifier.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.emotion_classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"🎯 Emotion classifier trained - Accuracy: {accuracy:.3f}")
        
        # Save vectorizer
        joblib.dump(vectorizer, f"{self.model_dir}/emotion_vectorizer.pkl")
        
        return accuracy
    
    def train_response_generator(self):
        """Train response generation model using patterns."""
        if len(self.training_data["conversation_pairs"]) < 50:
            print("⚠️ Need more training data for response generator")
            return
        
        # Create response templates based on patterns
        response_patterns = defaultdict(list)
        
        for sample in self.training_data["conversation_pairs"]:
            emotion = sample["emotion_context"].get("primary_emotion", "neutral")
            response_patterns[emotion].append(sample["ai_response"])
        
        # Store patterns
        self.response_patterns = dict(response_patterns)
        
        # Create a simple classifier for response selection
        texts = [sample["user_input"] for sample in self.training_data["conversation_pairs"]]
        emotions = [sample["emotion_context"].get("primary_emotion", "neutral") 
                   for sample in self.training_data["conversation_pairs"]]
        
        vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        X = vectorizer.fit_transform(texts)
        
        self.response_classifier = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
        self.response_classifier.fit(X, emotions)
        
        print(f"🎯 Response generator trained with {len(response_patterns)} emotion patterns")
        
        # Save components
        joblib.dump(vectorizer, f"{self.model_dir}/response_vectorizer.pkl")
        joblib.dump(self.response_patterns, f"{self.model_dir}/response_patterns.pkl")
        
        return True
    
    def train_emolytics_analyzer(self):
        """Train emolytics analysis model."""
        if len(self.training_data["emolytics_patterns"]) < 30:
            print("⚠️ Need more training data for emolytics analyzer")
            return
        
        # Extract patterns from emolytics data
        self.emolytics_patterns = {
            "emotion_to_wellness": defaultdict(list),
            "trigger_patterns": defaultdict(list),
            "recommendation_patterns": defaultdict(list)
        }
        
        for sample in self.training_data["emolytics_patterns"]:
            emotion = sample["emotion_data"].get("primary_emotion", "neutral")
            emolytics = sample["emolytics_update"]
            
            # Map emotions to wellness scores
            if "emotional_state" in emolytics:
                wellness_score = emolytics["emotional_state"].get("stability", 50)
                self.emolytics_patterns["emotion_to_wellness"][emotion].append(wellness_score)
            
            # Map triggers to recommendations
            triggers = sample["emotion_data"].get("emotional_triggers", [])
            recommendations = emolytics.get("recommendations", {}).get("immediate_actions", [])
            
            for trigger in triggers:
                self.emolytics_patterns["trigger_patterns"][trigger].extend(recommendations)
        
        print(f"🎯 Emolytics analyzer trained with {len(self.emolytics_patterns['emotion_to_wellness'])} emotion patterns")
        
        # Save patterns
        joblib.dump(self.emolytics_patterns, f"{self.model_dir}/emolytics_patterns.pkl")
        
        return True
    
    def train_models(self):
        """Train all models with collected data."""
        print("🚀 Starting model training...")
        
        # Train emotion classifier
        emotion_accuracy = self.train_emotion_classifier()
        
        # Train response generator
        response_success = self.train_response_generator()
        
        # Train emolytics analyzer
        emolytics_success = self.train_emolytics_analyzer()
        
        # Update learning metrics
        self.learning_metrics["last_training"] = datetime.now().isoformat()
        if emotion_accuracy:
            self.learning_metrics["model_confidence"] = emotion_accuracy
        
        # Save models
        self.save_models()
        
        print("✅ Model training completed!")
        
        return {
            "emotion_accuracy": emotion_accuracy,
            "response_success": response_success,
            "emolytics_success": emolytics_success
        }
    
    def predict_emotion(self, text: str) -> Dict:
        """Predict emotion using trained model."""
        if not self.emotion_classifier:
            return {"primary_emotion": "neutral", "confidence": 0.0}
        
        try:
            # Load vectorizer
            vectorizer = joblib.load(f"{self.model_dir}/emotion_vectorizer.pkl")
            X = vectorizer.transform([text])
            
            # Predict
            emotion = self.emotion_classifier.predict(X)[0]
            confidence = max(self.emotion_classifier.predict_proba(X)[0])
            
            return {
                "primary_emotion": emotion,
                "confidence": confidence,
                "model_used": "trained"
            }
        except Exception as e:
            print(f"❌ Error in emotion prediction: {e}")
            return {"primary_emotion": "neutral", "confidence": 0.0}
    
    def generate_response(self, user_message: str, emotion_data: Dict) -> str:
        """Generate response using trained model."""
        if not hasattr(self, 'response_patterns'):
            return "I'm still learning. Please continue our conversation."
        
        try:
            # Load vectorizer and classifier
            vectorizer = joblib.load(f"{self.model_dir}/response_vectorizer.pkl")
            X = vectorizer.transform([user_message])
            
            # Predict emotion
            predicted_emotion = self.response_classifier.predict(X)[0]
            
            # Get response pattern
            if predicted_emotion in self.response_patterns:
                responses = self.response_patterns[predicted_emotion]
                # Return a random response from the pattern
                return np.random.choice(responses)
            else:
                return "I understand. Please tell me more about how you're feeling."
                
        except Exception as e:
            print(f"❌ Error in response generation: {e}")
            return "I'm here to support you. How are you feeling?"
    
    def analyze_emolytics(self, emotion_data: Dict, conversation_context: List[Dict]) -> Dict:
        """Analyze emolytics using trained model."""
        if not hasattr(self, 'emolytics_patterns'):
            return self._default_emolytics(emotion_data)
        
        try:
            emotion = emotion_data.get("primary_emotion", "neutral")
            
            # Get wellness score pattern
            wellness_scores = self.emolytics_patterns["emotion_to_wellness"].get(emotion, [50])
            avg_wellness = np.mean(wellness_scores) if wellness_scores else 50
            
            # Get recommendation patterns
            triggers = emotion_data.get("emotional_triggers", [])
            recommendations = []
            
            for trigger in triggers:
                if trigger in self.emolytics_patterns["trigger_patterns"]:
                    recommendations.extend(self.emolytics_patterns["trigger_patterns"][trigger])
            
            # Remove duplicates and limit
            recommendations = list(set(recommendations))[:3]
            
            return {
                "emotional_state": {
                    "current_emotion": emotion,
                    "intensity": emotion_data.get("emotion_intensity", 50),
                    "stability": avg_wellness,
                    "mood_trend": "stable"
                },
                "recommendations": {
                    "immediate_actions": recommendations,
                    "long_term_strategies": [],
                    "wellness_practices": []
                },
                "analytics_metrics": {
                    "emotional_variability": 50,
                    "response_time_to_triggers": "medium",
                    "emotional_awareness_score": 50,
                    "wellness_progress": avg_wellness
                },
                "model_used": "trained"
            }
            
        except Exception as e:
            print(f"❌ Error in emolytics analysis: {e}")
            return self._default_emolytics(emotion_data)
    
    def _default_emolytics(self, emotion_data: Dict) -> Dict:
        """Default emolytics when model is not ready."""
        return {
            "emotional_state": {
                "current_emotion": emotion_data.get("primary_emotion", "neutral"),
                "intensity": emotion_data.get("emotion_intensity", 50),
                "stability": 50,
                "mood_trend": "stable"
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
            },
            "model_used": "default"
        }
    
    def should_use_own_model(self) -> bool:
        """Determine if we should use our own model instead of Gemini."""
        return self.learning_metrics["model_confidence"] >= self.learning_metrics["independence_threshold"]
    
    def get_learning_status(self) -> Dict:
        """Get current learning status and metrics."""
        return {
            "total_interactions": self.learning_metrics["total_interactions"],
            "model_confidence": self.learning_metrics["model_confidence"],
            "independence_threshold": self.learning_metrics["independence_threshold"],
            "should_use_own_model": self.should_use_own_model(),
            "last_training": self.learning_metrics["last_training"],
            "training_data_size": {
                "emotion_data": len(self.training_data["emotion_data"]),
                "conversation_pairs": len(self.training_data["conversation_pairs"]),
                "emolytics_patterns": len(self.training_data["emolytics_patterns"])
            }
        } 