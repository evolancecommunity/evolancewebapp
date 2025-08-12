import os
import json
import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import openai
import google.generativeai as genai
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import chromadb
from chromadb.config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class UserInteraction:
    user_id: str
    message: str
    timestamp: datetime
    emotion: str
    intent: str
    response: str
    user_feedback: Optional[float] = None
    context: Dict[str, Any] = None

@dataclass
class SemanticNode:
    id: str
    concept: str
    embeddings: List[float]
    connections: List[str]
    weight: float
    last_updated: datetime
    usage_count: int = 0

class HybridAISystem:
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.user_interactions = []
        self.semantic_network = {}
        self.emotion_detector = None
        self.intent_classifier = None
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.chroma_client = None
        self.collection = None
        
        # Initialize external APIs
        self._setup_external_apis()
        
        # Initialize ML models
        self._setup_ml_models()
        
        # Initialize ChromaDB
        self._setup_chromadb()
        
        logger.info("Hybrid AI System initialized successfully")

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            config = {
                "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
                "gemini_api_key": os.getenv("GEMINI_API_KEY", ""),
                "use_openai": True,
                "use_gemini": True,
                "fallback_to_local": True,
                "data_collection_enabled": True,
                "semantic_network_enabled": True,
                "emotion_detection_enabled": True,
                "intent_classification_enabled": True,
                "chromadb_path": "./chroma_db",
                "model_cache_dir": "./model_cache"
            }
            # Save default config
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return config

    def _setup_external_apis(self):
        """Setup external API clients"""
        if self.config["use_openai"] and self.config["openai_api_key"]:
            openai.api_key = self.config["openai_api_key"]
            logger.info("OpenAI API configured")
        
        if self.config["use_gemini"] and self.config["gemini_api_key"]:
            genai.configure(api_key=self.config["gemini_api_key"])
            logger.info("Gemini API configured")

    def _setup_ml_models(self):
        """Setup local ML models for fallback and data collection"""
        try:
            # Emotion detection model
            if self.config["emotion_detection_enabled"]:
                self.emotion_detector = pipeline(
                    "text-classification",
                    model="j-hartmann/emotion-english-distilroberta-base"
                )
                logger.info("Emotion detection model loaded")

            # Intent classification model
            if self.config["intent_classification_enabled"]:
                self.intent_classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli"
                )
                logger.info("Intent classification model loaded")

        except Exception as e:
            logger.warning(f"Failed to load ML models: {e}")
            self.emotion_detector = None
            self.intent_classifier = None

    def _setup_chromadb(self):
        """Setup ChromaDB for semantic storage"""
        try:
            self.chroma_client = chromadb.PersistentClient(
                path=self.config["chromadb_path"],
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Create or get collection
            try:
                self.collection = self.chroma_client.get_collection("user_interactions")
            except:
                self.collection = self.chroma_client.create_collection("user_interactions")
            
            logger.info("ChromaDB initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            self.chroma_client = None
            self.collection = None

    async def process_message(self, user_id: str, message: str, context: Dict = None) -> str:
        """Main method to process user messages"""
        try:
            # 1. Analyze message
            emotion = self._detect_emotion(message)
            intent = self._classify_intent(message)
            
            # 2. Generate response using external APIs
            response = await self._generate_response(message, emotion, intent, context)
            
            # 3. Store interaction for training
            if self.config["data_collection_enabled"]:
                self._store_interaction(user_id, message, emotion, intent, response, context)
            
            # 4. Update semantic network
            if self.config["semantic_network_enabled"]:
                self._update_semantic_network(message, emotion, intent)
            
            return response

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return self._get_fallback_response(message)

    def _detect_emotion(self, text: str) -> str:
        """Detect emotion in text using local model"""
        try:
            if self.emotion_detector:
                result = self.emotion_detector(text)
                return result[0]['label']
            else:
                # Simple keyword-based fallback
                text_lower = text.lower()
                if any(word in text_lower for word in ['happy', 'joy', 'excited', 'great']):
                    return 'joy'
                elif any(word in text_lower for word in ['sad', 'depressed', 'unhappy']):
                    return 'sadness'
                elif any(word in text_lower for word in ['angry', 'mad', 'furious']):
                    return 'anger'
                elif any(word in text_lower for word in ['afraid', 'scared', 'fear']):
                    return 'fear'
                else:
                    return 'neutral'
        except Exception as e:
            logger.error(f"Emotion detection error: {e}")
            return 'neutral'

    def _classify_intent(self, text: str) -> str:
        """Classify intent using local model"""
        try:
            if self.intent_classifier:
                # Define intent categories
                candidate_labels = [
                    "question", "statement", "greeting", "farewell", 
                    "request", "complaint", "compliment", "help"
                ]
                result = self.intent_classifier(text, candidate_labels)
                return result['labels'][0]
            else:
                # Simple keyword-based fallback
                text_lower = text.lower()
                if '?' in text:
                    return 'question'
                elif any(word in text_lower for word in ['hello', 'hi', 'hey']):
                    return 'greeting'
                elif any(word in text_lower for word in ['bye', 'goodbye', 'see you']):
                    return 'farewell'
                else:
                    return 'statement'
        except Exception as e:
            logger.error(f"Intent classification error: {e}")
            return 'statement'

    async def _generate_response(self, message: str, emotion: str, intent: str, context: Dict = None) -> str:
        """Generate response using external APIs with fallback"""
        
        # Try OpenAI first
        if self.config["use_openai"] and self.config["openai_api_key"]:
            try:
                response = await self._generate_openai_response(message, emotion, intent, context)
                if response:
                    return response
            except Exception as e:
                logger.warning(f"OpenAI generation failed: {e}")

        # Try Gemini
        if self.config["use_gemini"] and self.config["gemini_api_key"]:
            try:
                response = await self._generate_gemini_response(message, emotion, intent, context)
                if response:
                    return response
            except Exception as e:
                logger.warning(f"Gemini generation failed: {e}")

        # Fallback to local generation
        if self.config["fallback_to_local"]:
            return self._generate_local_response(message, emotion, intent, context)

        return "I'm having trouble generating a response right now. Please try again."

    async def _generate_openai_response(self, message: str, emotion: str, intent: str, context: Dict = None) -> str:
        """Generate response using OpenAI"""
        try:
            system_prompt = f"""You are an emotionally intelligent AI assistant. 
            The user's message shows {emotion} emotion and {intent} intent.
            Respond naturally and empathetically, matching the emotional context.
            Keep responses conversational and helpful."""
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return None

    async def _generate_gemini_response(self, message: str, emotion: str, intent: str, context: Dict = None) -> str:
        """Generate response using Gemini"""
        try:
            model = genai.GenerativeModel('gemini-2.5-pro')
            
            prompt = f"""You are an emotionally intelligent AI assistant. 
            The user's message shows {emotion} emotion and {intent} intent.
            Respond naturally and empathetically, matching the emotional context.
            Keep responses conversational and helpful.
            
            User message: {message}"""
            
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return None

    def _generate_local_response(self, message: str, emotion: str, intent: str, context: Dict = None) -> str:
        """Generate response using local models and semantic network"""
        try:
            # Use semantic network to find relevant responses
            relevant_responses = self._get_semantic_responses(message, emotion)
            
            if relevant_responses:
                # Return the most relevant response
                return relevant_responses[0]
            
            # Fallback to template-based responses
            templates = {
                'joy': [
                    "That sounds wonderful! I'm glad you're feeling positive.",
                    "Your enthusiasm is contagious! What's making you so happy?",
                    "That's fantastic! I love your positive energy."
                ],
                'sadness': [
                    "I'm sorry you're feeling down. Would you like to talk about it?",
                    "It's okay to feel sad sometimes. I'm here to listen.",
                    "I can sense you're having a tough time. What's on your mind?"
                ],
                'anger': [
                    "I can see you're frustrated. What's bothering you?",
                    "It sounds like something's really upsetting you. Want to discuss it?",
                    "I understand you're angry. Let's work through this together."
                ],
                'fear': [
                    "I can sense your worry. What are you afraid of?",
                    "It's natural to feel afraid sometimes. You're not alone.",
                    "I'm here to help you through this. What's causing your concern?"
                ],
                'neutral': [
                    "I understand. Tell me more about that.",
                    "That's interesting. What are your thoughts on this?",
                    "I'm listening. How can I help you with this?"
                ]
            }
            
            import random
            return random.choice(templates.get(emotion, templates['neutral']))
            
        except Exception as e:
            logger.error(f"Local response generation error: {e}")
            return "I'm here to help. What would you like to talk about?"

    def _store_interaction(self, user_id: str, message: str, emotion: str, intent: str, response: str, context: Dict = None):
        """Store user interaction for training data"""
        try:
            interaction = UserInteraction(
                user_id=user_id,
                message=message,
                timestamp=datetime.now(),
                emotion=emotion,
                intent=intent,
                response=response,
                context=context or {}
            )
            
            self.user_interactions.append(interaction)
            
            # Store in ChromaDB
            if self.collection:
                self.collection.add(
                    documents=[message],
                    metadatas=[{
                        'user_id': user_id,
                        'emotion': emotion,
                        'intent': intent,
                        'timestamp': interaction.timestamp.isoformat(),
                        'response': response
                    }],
                    ids=[f"{user_id}_{interaction.timestamp.timestamp()}"]
                )
            
            logger.info(f"Stored interaction for user {user_id}")
            
        except Exception as e:
            logger.error(f"Failed to store interaction: {e}")

    def _update_semantic_network(self, message: str, emotion: str, intent: str):
        """Update semantic network with new interaction"""
        try:
            # Extract key concepts from message
            words = message.lower().split()
            key_concepts = [word for word in words if len(word) > 3]
            
            for concept in key_concepts:
                if concept not in self.semantic_network:
                    # Create new semantic node
                    self.semantic_network[concept] = SemanticNode(
                        id=concept,
                        concept=concept,
                        embeddings=self._get_concept_embeddings(concept),
                        connections=[],
                        weight=1.0,
                        last_updated=datetime.now(),
                        usage_count=1
                    )
                else:
                    # Update existing node
                    node = self.semantic_network[concept]
                    node.usage_count += 1
                    node.weight += 0.1
                    node.last_updated = datetime.now()
                    
                    # Add connections to other concepts in the message
                    for other_concept in key_concepts:
                        if other_concept != concept and other_concept not in node.connections:
                            node.connections.append(other_concept)
            
        except Exception as e:
            logger.error(f"Failed to update semantic network: {e}")

    def _get_concept_embeddings(self, concept: str) -> List[float]:
        """Get embeddings for a concept (simplified version)"""
        # For now, use simple TF-IDF-like embeddings
        # In production, use proper embedding models
        return [hash(concept) % 100 / 100.0 for _ in range(10)]

    def _get_semantic_responses(self, message: str, emotion: str) -> List[str]:
        """Get relevant responses from semantic network"""
        try:
            relevant_responses = []
            
            # Search ChromaDB for similar interactions
            if self.collection:
                results = self.collection.query(
                    query_texts=[message],
                    n_results=5
                )
                
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i]
                    if metadata['emotion'] == emotion:
                        relevant_responses.append(metadata['response'])
            
            return relevant_responses
            
        except Exception as e:
            logger.error(f"Failed to get semantic responses: {e}")
            return []

    def _get_fallback_response(self, message: str) -> str:
        """Get a fallback response when all else fails"""
        fallback_responses = [
            "I'm here to help. What would you like to talk about?",
            "I'm listening. How can I assist you today?",
            "That's interesting. Tell me more about that.",
            "I understand. What's on your mind?",
            "I'm here for you. What would you like to discuss?"
        ]
        
        import random
        return random.choice(fallback_responses)

    def get_training_data(self) -> List[Dict]:
        """Get collected training data for proprietary model development"""
        training_data = []
        
        for interaction in self.user_interactions:
            training_data.append({
                'input': interaction.message,
                'output': interaction.response,
                'emotion': interaction.emotion,
                'intent': interaction.intent,
                'user_id': interaction.user_id,
                'timestamp': interaction.timestamp.isoformat(),
                'feedback': interaction.user_feedback
            })
        
        return training_data

    def export_training_data(self, filepath: str):
        """Export training data to JSON file"""
        try:
            training_data = self.get_training_data()
            with open(filepath, 'w') as f:
                json.dump(training_data, f, indent=2)
            logger.info(f"Training data exported to {filepath}")
        except Exception as e:
            logger.error(f"Failed to export training data: {e}")

    def get_system_stats(self) -> Dict:
        """Get system statistics"""
        return {
            'total_interactions': len(self.user_interactions),
            'semantic_nodes': len(self.semantic_network),
            'chromadb_available': self.collection is not None,
            'emotion_detector_available': self.emotion_detector is not None,
            'intent_classifier_available': self.intent_classifier is not None,
            'openai_configured': bool(self.config["openai_api_key"]),
            'gemini_configured': bool(self.config["gemini_api_key"])
        } 