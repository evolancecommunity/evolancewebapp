"""
Evolance AI Engine
Main orchestrator for the proprietary emotional intelligence AI system
"""

import time
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .config import config
from .semantic_network import CoreSemanticNetwork, core_network
from .personal_network import PersonalSemanticNetwork
from .emotion_detector import EmotionDetector, emotion_detector
from .memory_manager import MemoryManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ConversationContext:
    """Context for a conversation turn"""
    user_id: str
    message: str
    timestamp: float
    session_id: str
    conversation_history: List[Dict[str, Any]]
    user_profile: Dict[str, Any]
    emotional_state: Dict[str, Any]
    memory_context: Dict[str, Any]

@dataclass
class AIResponse:
    """AI response with full context"""
    response_text: str
    emotion_detected: str
    confidence: float
    personalized_elements: List[str]
    coping_suggestions: List[str]
    follow_up_questions: List[str]
    memory_updated: bool
    response_time: float

class EvolanceAIEngine:
    """
    Main AI engine for Evolance
    Orchestrates all components for emotionally intelligent conversations
    """
    
    def __init__(self):
        self.core_network = core_network
        self.emotion_detector = emotion_detector
        
        # User sessions
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
        
        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # Performance metrics
        self.metrics = {
            "total_conversations": 0,
            "average_response_time": 0.0,
            "emotion_detection_accuracy": 0.0,
            "user_satisfaction": 0.0
        }
        
        logger.info("Evolance AI Engine initialized")
    
    async def process_message(self, user_id: str, message: str, 
                            session_id: str = None) -> AIResponse:
        """
        Process a user message and generate an emotionally intelligent response
        """
        start_time = time.time()
        
        try:
            # Create or get user session
            if user_id not in self.user_sessions:
                await self._initialize_user_session(user_id)
            
            session = self.user_sessions[user_id]
            
            # Create conversation context
            context = ConversationContext(
                user_id=user_id,
                message=message,
                timestamp=time.time(),
                session_id=session_id or f"session_{int(time.time())}",
                conversation_history=session.get("conversation_history", []),
                user_profile=session.get("user_profile", {}),
                emotional_state=session.get("emotional_state", {}),
                memory_context=session.get("memory_context", {})
            )
            
            # Step 1: Emotion Detection
            emotion_result = await self._detect_emotions(message, context)
            
            # Step 2: Memory Retrieval
            memory_context = await self._retrieve_memory_context(message, user_id)
            
            # Step 3: Personal Network Update
            await self._update_personal_network(message, emotion_result, user_id)
            
            # Step 4: Generate Response
            response = await self._generate_response(message, emotion_result, 
                                                   memory_context, context)
            
            # Step 5: Update Session
            await self._update_session(user_id, message, response, emotion_result)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Create AI response
            ai_response = AIResponse(
                response_text=response["text"],
                emotion_detected=emotion_result.primary_emotion,
                confidence=emotion_result.confidence,
                personalized_elements=response.get("personalized_elements", []),
                coping_suggestions=response.get("coping_suggestions", []),
                follow_up_questions=response.get("follow_up_questions", []),
                memory_updated=True,
                response_time=response_time
            )
            
            # Update metrics
            self._update_metrics(response_time)
            
            logger.info(f"Processed message for user {user_id} in {response_time:.2f}s")
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error processing message for user {user_id}: {e}")
            return self._generate_error_response()
    
    async def _initialize_user_session(self, user_id: str):
        """Initialize a new user session"""
        logger.info(f"Initializing session for user {user_id}")
        
        # Initialize personal network
        personal_network = PersonalSemanticNetwork(user_id, self.core_network)
        
        # Initialize memory manager
        memory_manager = MemoryManager(user_id)
        
        # Create session
        self.user_sessions[user_id] = {
            "personal_network": personal_network,
            "memory_manager": memory_manager,
            "conversation_history": [],
            "user_profile": {},
            "emotional_state": {},
            "memory_context": {},
            "session_start": time.time(),
            "message_count": 0
        }
    
    async def _detect_emotions(self, message: str, context: ConversationContext) -> Any:
        """Detect emotions in user message"""
        # Run emotion detection in thread pool
        loop = asyncio.get_event_loop()
        emotion_result = await loop.run_in_executor(
            self.executor,
            self.emotion_detector.detect_emotions,
            message
        )
        
        return emotion_result
    
    async def _retrieve_memory_context(self, message: str, user_id: str) -> Dict[str, Any]:
        """Retrieve relevant memory context"""
        session = self.user_sessions[user_id]
        memory_manager = session["memory_manager"]
        personal_network = session["personal_network"]
        
        # Get memory context
        memory_context = memory_manager.get_memory_context(message, personal_network)
        
        return memory_context
    
    async def _update_personal_network(self, message: str, emotion_result: Any, user_id: str):
        """Update personal network with new information"""
        session = self.user_sessions[user_id]
        personal_network = session["personal_network"]
        
        # Process conversation data
        conversation_data = {
            "emotions": {emotion_result.primary_emotion: emotion_result.confidence},
            "concepts": emotion_result.triggers,
            "coping_strategies": [],
            "coping_effectiveness": 0.5
        }
        
        personal_network.process_conversation(conversation_data)
    
    async def _generate_response(self, message: str, emotion_result: Any, 
                               memory_context: Dict[str, Any], 
                               context: ConversationContext) -> Dict[str, Any]:
        """Generate emotionally intelligent response"""
        
        # Build prompt with context
        prompt = self._build_response_prompt(message, emotion_result, memory_context, context)
        
        # Generate response using LLM (improved conversational responses)
        response = await self._generate_llm_response(prompt)
        
        # Enhance with personalization
        enhanced_response = self._enhance_with_personalization(
            response, memory_context, context
        )
        
        return enhanced_response
    
    def _build_response_prompt(self, message: str, emotion_result: Any,
                             memory_context: Dict[str, Any], 
                             context: ConversationContext) -> str:
        """Build comprehensive prompt for LLM"""
        
        prompt_parts = []
        
        # System instruction
        prompt_parts.append("""You are Evolance, an emotionally intelligent AI companion focused on mental wellness. 
Your role is to provide empathetic, supportive, and personalized responses. Always:
1. Acknowledge and validate the user's emotions
2. Use their personal context when available
3. Offer helpful coping strategies when appropriate
4. Maintain a warm, caring tone
5. Remember their past experiences and preferences""")
        
        # User's emotional state
        prompt_parts.append(f"\nUser's current emotional state: {emotion_result.primary_emotion} (confidence: {emotion_result.confidence:.2f})")
        
        # Personal context
        if memory_context.get("personal_context"):
            personal = memory_context["personal_context"]
            if personal.get("relevant_patterns"):
                prompt_parts.append(f"\nRelevant patterns: {personal['relevant_patterns'][:2]}")
            if personal.get("coping_recommendations"):
                prompt_parts.append(f"\nEffective coping strategies: {personal['coping_recommendations']}")
        
        # Recent memories
        if memory_context.get("relevant_memories"):
            memories = memory_context["relevant_memories"][:2]
            prompt_parts.append(f"\nRelevant past experiences: {memories}")
        
        # Current message
        prompt_parts.append(f"\nUser message: {message}")
        
        # Response guidelines
        prompt_parts.append("""\nGenerate a response that:
1. Acknowledges their emotion
2. Shows understanding of their personal context
3. Offers appropriate support or coping strategies
4. Maintains continuity with past conversations
5. Encourages further engagement""")
        
        return "\n".join(prompt_parts)
    
    async def _generate_llm_response(self, prompt: str) -> Dict[str, Any]:
        """Generate response using LLM (improved conversational responses)"""
        
        # This would use the actual LLM model
        # For now, return intelligent, personalized responses
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Extract emotion and context from the prompt
        emotion = "neutral"
        if "joy" in prompt.lower() or "happy" in prompt.lower():
            emotion = "joy"
        elif "sadness" in prompt.lower() or "sad" in prompt.lower():
            emotion = "sadness"
        elif "fear" in prompt.lower() or "anxious" in prompt.lower():
            emotion = "fear"
        elif "anger" in prompt.lower() or "angry" in prompt.lower():
            emotion = "anger"
        elif "surprise" in prompt.lower():
            emotion = "surprise"
        elif "love" in prompt.lower():
            emotion = "love"
        
        # Generate personalized responses based on emotion
        responses = {
            "joy": [
                "That's awesome! What's got you in such a good mood?",
                "Love that energy! What's making you smile today?",
                "That's great to hear! Tell me more about what's going well."
            ],
            "sadness": [
                "I'm sorry you're having a rough time. Want to talk about it?",
                "That sounds really tough. What's going on?",
                "I'm here if you want to vent. What happened?"
            ],
            "fear": [
                "That sounds really scary. What's worrying you?",
                "I can tell you're anxious. What's on your mind?",
                "That's definitely stressful. Want to talk through it?"
            ],
            "anger": [
                "You sound really frustrated. What happened?",
                "That's totally understandable to be mad about. What's going on?",
                "I can hear you're upset. Want to tell me about it?"
            ],
            "surprise": [
                "Wow! That's unexpected. What happened?",
                "No way! Tell me more about that.",
                "That's crazy! What's the story there?"
            ],
            "love": [
                "That's so sweet! What kind of love are you feeling?",
                "Aww, that's beautiful! Tell me more about it.",
                "Love is amazing! What's making your heart happy?"
            ],
            "neutral": [
                "Hey! How's it going?",
                "Hi there! What's up?",
                "Hey! How are you doing?"
            ]
        }
        
        # Get personalized coping strategies based on emotion
        coping_strategies = {
            "joy": ["share it with friends", "enjoy the moment", "spread the good vibes"],
            "sadness": ["talk to someone you trust", "do something you enjoy", "be kind to yourself"],
            "fear": ["take deep breaths", "talk it out", "distract yourself with something fun"],
            "anger": ["take a break", "go for a walk", "vent to a friend"],
            "surprise": ["take a moment to process", "talk about it", "go with the flow"],
            "love": ["enjoy the feeling", "spend time with loved ones", "appreciate the moment"],
            "neutral": ["just be yourself", "do what feels right", "connect with others"]
        }
        
        # Get follow-up questions based on emotion
        follow_up_questions = {
            "joy": ["What's the best part of your day?", "Who else knows about this?"],
            "sadness": ["What would help right now?", "Want to talk about it?"],
            "fear": ["What's the worst that could happen?", "What would make you feel better?"],
            "anger": ["What set you off?", "How can you cool down?"],
            "surprise": ["What's the full story?", "How do you feel about it now?"],
            "love": ["What kind of love is it?", "How does it feel?"],
            "neutral": ["What's on your mind?", "How are you really doing?"]
        }
        
        import random
        response_text = random.choice(responses[emotion])
        coping = coping_strategies[emotion]
        questions = follow_up_questions[emotion]
        
        return {
            "text": response_text,
            "personalized_elements": [f"emotion-specific response for {emotion}", "contextual coping strategies"],
            "coping_suggestions": coping,
            "follow_up_questions": questions
        }
    
    def _enhance_with_personalization(self, response: Dict[str, Any], 
                                    memory_context: Dict[str, Any],
                                    context: ConversationContext) -> Dict[str, Any]:
        """Enhance response with personalization elements"""
        
        enhanced = response.copy()
        
        # Add personal touches based on memory context
        if memory_context.get("personal_context", {}).get("coping_recommendations"):
            personal_coping = memory_context["personal_context"]["coping_recommendations"]
            if personal_coping:
                enhanced["coping_suggestions"].extend([
                    rec["strategies"] for rec in personal_coping
                ])
        
        # Add user-specific language patterns
        if context.user_profile.get("preferred_style"):
            style = context.user_profile["preferred_style"]
            if style == "formal":
                enhanced["text"] = enhanced["text"].replace("I'm", "I am")
            elif style == "casual":
                enhanced["text"] = enhanced["text"].replace("I am", "I'm")
        
        return enhanced
    
    async def _update_session(self, user_id: str, message: str, response: Dict[str, Any], 
                            emotion_result: Any):
        """Update user session with new information"""
        session = self.user_sessions[user_id]
        
        # Add to conversation history
        session["conversation_history"].append({
            "timestamp": time.time(),
            "user_message": message,
            "ai_response": response["text"],
            "emotion": emotion_result.primary_emotion,
            "confidence": emotion_result.confidence
        })
        
        # Update emotional state
        session["emotional_state"] = {
            "current_emotion": emotion_result.primary_emotion,
            "intensity": emotion_result.intensity,
            "valence": emotion_result.valence,
            "arousal": emotion_result.arousal,
            "body_sensations": emotion_result.body_sensations
        }
        
        # Update message count
        session["message_count"] += 1
        
        # Consolidate memories periodically
        if session["message_count"] % 5 == 0:  # Every 5 messages
            memory_manager = session["memory_manager"]
            personal_network = session["personal_network"]
            memory_manager.consolidate_memories(personal_network)
    
    def _update_metrics(self, response_time: float):
        """Update performance metrics"""
        self.metrics["total_conversations"] += 1
        
        # Update average response time
        current_avg = self.metrics["average_response_time"]
        total_convs = self.metrics["total_conversations"]
        self.metrics["average_response_time"] = (
            (current_avg * (total_convs - 1) + response_time) / total_convs
        )
    
    def _generate_error_response(self) -> AIResponse:
        """Generate response for error cases"""
        return AIResponse(
            response_text="I'm having trouble processing that right now. Could you try rephrasing your message?",
            emotion_detected="neutral",
            confidence=0.0,
            personalized_elements=[],
            coping_suggestions=[],
            follow_up_questions=["How can I help you today?"],
            memory_updated=False,
            response_time=0.0
        )
    
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user profile"""
        if user_id not in self.user_sessions:
            return {"error": "User session not found"}
        
        session = self.user_sessions[user_id]
        personal_network = session["personal_network"]
        
        return personal_network.get_user_summary()
    
    async def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """Export all user data for portability"""
        if user_id not in self.user_sessions:
            return {"error": "User session not found"}
        
        session = self.user_sessions[user_id]
        personal_network = session["personal_network"]
        memory_manager = session["memory_manager"]
        
        return {
            "user_profile": personal_network.export_network(),
            "memories": memory_manager.export_memories(),
            "conversation_history": session["conversation_history"],
            "export_timestamp": time.time()
        }
    
    async def delete_user_data(self, user_id: str) -> bool:
        """Delete all user data"""
        if user_id not in self.user_sessions:
            return False
        
        session = self.user_sessions[user_id]
        memory_manager = session["memory_manager"]
        
        # Delete memories
        memory_manager.delete_all_memories()
        
        # Remove session
        del self.user_sessions[user_id]
        
        logger.info(f"Deleted all data for user {user_id}")
        return True
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        return {
            "metrics": self.metrics,
            "active_users": len(self.user_sessions),
            "system_health": "healthy",
            "uptime": time.time() - getattr(self, '_start_time', time.time())
        }
    
    async def shutdown(self):
        """Graceful shutdown of the AI engine"""
        logger.info("Shutting down Evolance AI Engine")
        
        # Consolidate all pending memories
        for user_id, session in self.user_sessions.items():
            memory_manager = session["memory_manager"]
            personal_network = session["personal_network"]
            memory_manager.consolidate_memories(personal_network)
        
        # Shutdown thread pool
        self.executor.shutdown(wait=True)
        
        logger.info("Evolance AI Engine shutdown complete")

# Global AI engine instance
ai_engine = EvolanceAIEngine() 