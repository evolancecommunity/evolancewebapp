import os
import sys
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

# Import the hybrid AI system
from ai_core.hybrid_ai_system import HybridAISystem

logger = logging.getLogger(__name__)

class EvolanceHybridAI:
    """Integration layer between Evolance backend and hybrid AI system"""
    
    def __init__(self):
        self.hybrid_system = None
        self.user_sessions = {}
        self.checkin_schedules = {}
        self.reminder_schedules = {}
        
    async def initialize(self):
        """Initialize the hybrid AI system"""
        try:
            self.hybrid_system = HybridAISystem()
            logger.info("Hybrid AI system initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize hybrid AI system: {e}")
            return False
    
    async def process_chat_message(self, user_id: str, message: str, context: Dict = None) -> Dict[str, Any]:
        """Process chat message using hybrid AI system"""
        try:
            if not self.hybrid_system:
                await self.initialize()
            
            # Process message through hybrid system
            response = await self.hybrid_system.process_message(
                user_id=user_id,
                message=message,
                context=context or {}
            )
            
            # Check for crisis indicators
            crisis_detected = await self._check_crisis_indicators(message, user_id)
            
            return {
                "response": response,
                "emotion": self.hybrid_system._detect_emotion(message),
                "intent": self.hybrid_system._classify_intent(message),
                "crisis_detected": crisis_detected,
                "crisis_resources": self._get_crisis_resources() if crisis_detected else None,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing chat message: {e}")
            return {
                "response": "I'm having trouble processing that right now. Could you try rephrasing?",
                "emotion": "neutral",
                "intent": "statement",
                "crisis_detected": False,
                "crisis_resources": None,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def get_emotional_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user's emotional profile and graphs"""
        try:
            if not self.hybrid_system:
                await self.initialize()
            
            # Get training data for this user
            training_data = self.hybrid_system.get_training_data()
            user_data = [item for item in training_data if item.get('user_id') == user_id]
            
            # Calculate emotional trends
            emotions = [item.get('emotion', 'neutral') for item in user_data[-50:]]  # Last 50 interactions
            emotion_counts = {}
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            # Calculate fulfillment trend
            fulfillment_trend = self._calculate_fulfillment_trend(user_data)
            
            return {
                "emotional_fingerprint": emotion_counts,
                "fulfillment_trend": fulfillment_trend,
                "total_interactions": len(user_data),
                "recent_emotions": emotions[-10:],  # Last 10 emotions
                "dominant_emotion": max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else "neutral",
                "emotional_balance_score": self._calculate_emotional_balance(emotion_counts),
                "growth_milestones": self._get_growth_milestones(user_data)
            }
            
        except Exception as e:
            logger.error(f"Error getting emotional profile: {e}")
            return {
                "emotional_fingerprint": {},
                "fulfillment_trend": "stable",
                "total_interactions": 0,
                "recent_emotions": [],
                "dominant_emotion": "neutral",
                "emotional_balance_score": 50,
                "growth_milestones": []
            }
    
    async def get_avatar_state(self, user_id: str) -> Dict[str, Any]:
        """Get avatar visualization state based on user's emotional state"""
        try:
            profile = await self.get_emotional_profile(user_id)
            dominant_emotion = profile.get('dominant_emotion', 'neutral')
            
            # Map emotions to chakra colors
            chakra_colors = {
                'joy': {'primary': '#FFD700', 'secondary': '#FFA500', 'chakra': 'solar_plexus'},
                'sadness': {'primary': '#4169E1', 'secondary': '#1E90FF', 'chakra': 'throat'},
                'anger': {'primary': '#DC143C', 'secondary': '#FF4500', 'chakra': 'root'},
                'fear': {'primary': '#9932CC', 'secondary': '#8A2BE2', 'chakra': 'crown'},
                'love': {'primary': '#FF69B4', 'secondary': '#FF1493', 'chakra': 'heart'},
                'surprise': {'primary': '#00CED1', 'secondary': '#20B2AA', 'chakra': 'third_eye'},
                'neutral': {'primary': '#808080', 'secondary': '#A9A9A9', 'chakra': 'balanced'}
            }
            
            color_scheme = chakra_colors.get(dominant_emotion, chakra_colors['neutral'])
            
            return {
                "primary_color": color_scheme['primary'],
                "secondary_color": color_scheme['secondary'],
                "active_chakra": color_scheme['chakra'],
                "glow_intensity": min(profile.get('emotional_balance_score', 50) / 10, 10),
                "animation_state": "pulse" if profile.get('emotional_balance_score', 50) > 70 else "gentle",
                "emotional_state": dominant_emotion,
                "fulfillment_level": profile.get('emotional_balance_score', 50)
            }
            
        except Exception as e:
            logger.error(f"Error getting avatar state: {e}")
            return {
                "primary_color": "#808080",
                "secondary_color": "#A9A9A9",
                "active_chakra": "balanced",
                "glow_intensity": 5,
                "animation_state": "gentle",
                "emotional_state": "neutral",
                "fulfillment_level": 50
            }
    
    async def generate_checkin_message(self, user_id: str) -> Dict[str, Any]:
        """Generate AI friend check-in message"""
        try:
            if not self.hybrid_system:
                await self.initialize()
            
            profile = await self.get_emotional_profile(user_id)
            recent_emotions = profile.get('recent_emotions', [])
            
            # Generate contextual check-in based on recent emotions
            if recent_emotions:
                last_emotion = recent_emotions[-1]
                if last_emotion in ['sadness', 'fear', 'anger']:
                    message = "I noticed you've been feeling a bit down lately. How are you doing today? Would you like to talk about what's on your mind?"
                    tone = "caring"
                elif last_emotion == 'joy':
                    message = "I'm so glad to see your positive energy! What's been bringing you joy lately?"
                    tone = "celebratory"
                else:
                    message = "How are you feeling today? I'm here to listen and support you."
                    tone = "gentle"
            else:
                message = "Hello! I wanted to check in and see how you're doing. How has your day been?"
                tone = "friendly"
            
            return {
                "message": message,
                "tone": tone,
                "timestamp": datetime.utcnow().isoformat(),
                "type": "checkin"
            }
            
        except Exception as e:
            logger.error(f"Error generating checkin message: {e}")
            return {
                "message": "How are you feeling today? I'm here to listen.",
                "tone": "gentle",
                "timestamp": datetime.utcnow().isoformat(),
                "type": "checkin"
            }
    
    async def generate_memory_reminder(self, user_id: str) -> Dict[str, Any]:
        """Generate memory/milestone reminder"""
        try:
            if not self.hybrid_system:
                await self.initialize()
            
            # Get user's training data for milestone detection
            training_data = self.hybrid_system.get_training_data()
            user_data = [item for item in training_data if item.get('user_id') == user_id]
            
            if len(user_data) < 5:
                return None  # Not enough data for meaningful reminders
            
            # Find positive milestones
            positive_interactions = [
                item for item in user_data 
                if item.get('emotion') in ['joy', 'love'] and 
                item.get('feedback', 0) > 0.7
            ]
            
            if positive_interactions:
                # Select a random positive memory
                import random
                memory = random.choice(positive_interactions)
                
                return {
                    "type": "milestone_reminder",
                    "title": "Remember this moment of growth",
                    "message": f"Remember when you said: '{memory.get('input', '')[:100]}...' and felt {memory.get('emotion', 'positive')}? That was a beautiful moment of your journey.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "memory_date": memory.get('timestamp', ''),
                    "emotion": memory.get('emotion', 'joy')
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error generating memory reminder: {e}")
            return None
    
    async def _check_crisis_indicators(self, message: str, user_id: str) -> bool:
        """Check for crisis indicators in message"""
        crisis_keywords = [
            'suicide', 'kill myself', 'want to die', 'end it all', 'no reason to live',
            'self harm', 'cut myself', 'hurt myself', 'better off dead',
            'can\'t take it anymore', 'give up', 'hopeless', 'worthless'
        ]
        
        message_lower = message.lower()
        for keyword in crisis_keywords:
            if keyword in message_lower:
                logger.warning(f"Crisis indicators detected for user {user_id}")
                return True
        
        return False
    
    def _get_crisis_resources(self) -> Dict[str, Any]:
        """Get crisis resources and helpline information"""
        return {
            "crisis_lifeline": {
                "name": "988 Suicide & Crisis Lifeline",
                "phone": "988",
                "text": "Text HOME to 988",
                "website": "https://988lifeline.org"
            },
            "crisis_text_line": {
                "name": "Crisis Text Line",
                "text": "Text HOME to 741741",
                "website": "https://www.crisistextline.org"
            },
            "emergency": {
                "message": "If you're in immediate danger, please call 911 or go to your nearest emergency room.",
                "phone": "911"
            },
            "disclaimer": "Evolance is a growth tool, not a replacement for professional mental health care. If you're experiencing a crisis, please reach out to the resources above or a mental health professional."
        }
    
    def _calculate_fulfillment_trend(self, user_data: List[Dict]) -> str:
        """Calculate fulfillment trend from user data"""
        if len(user_data) < 10:
            return "stable"
        
        # Calculate average feedback scores over time
        recent_data = user_data[-10:]
        older_data = user_data[-20:-10] if len(user_data) >= 20 else user_data[:10]
        
        recent_avg = sum(item.get('feedback', 0.5) for item in recent_data) / len(recent_data)
        older_avg = sum(item.get('feedback', 0.5) for item in older_data) / len(older_data)
        
        if recent_avg > older_avg + 0.1:
            return "ascending"
        elif recent_avg < older_avg - 0.1:
            return "descending"
        else:
            return "stable"
    
    def _calculate_emotional_balance(self, emotion_counts: Dict[str, int]) -> int:
        """Calculate emotional balance score (0-100)"""
        if not emotion_counts:
            return 50
        
        total = sum(emotion_counts.values())
        positive_emotions = emotion_counts.get('joy', 0) + emotion_counts.get('love', 0)
        negative_emotions = emotion_counts.get('sadness', 0) + emotion_counts.get('fear', 0) + emotion_counts.get('anger', 0)
        
        if total == 0:
            return 50
        
        positive_ratio = positive_emotions / total
        negative_ratio = negative_emotions / total
        
        # Balance score: higher for more positive emotions, lower for more negative
        balance_score = int((positive_ratio - negative_ratio + 1) * 50)
        return max(0, min(100, balance_score))
    
    def _get_growth_milestones(self, user_data: List[Dict]) -> List[Dict]:
        """Get user's growth milestones"""
        milestones = []
        
        if len(user_data) >= 10:
            milestones.append({
                "type": "first_steps",
                "title": "First Steps on the Path",
                "description": "Completed your first 10 interactions",
                "achieved_at": user_data[9].get('timestamp', ''),
                "icon": "🌱"
            })
        
        if len(user_data) >= 50:
            milestones.append({
                "type": "dedicated_journey",
                "title": "Dedicated Journey",
                "description": "Completed 50 interactions",
                "achieved_at": user_data[49].get('timestamp', ''),
                "icon": "💜"
            })
        
        # Add emotion-specific milestones
        emotion_counts = {}
        for item in user_data:
            emotion = item.get('emotion', 'neutral')
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        for emotion, count in emotion_counts.items():
            if count >= 5:
                milestones.append({
                    "type": f"emotion_mastery_{emotion}",
                    "title": f"Emotional Awareness: {emotion.title()}",
                    "description": f"Explored {emotion} emotions {count} times",
                    "achieved_at": user_data[-1].get('timestamp', ''),
                    "icon": "🧘"
                })
        
        return milestones

# Global instance
evolance_ai = EvolanceHybridAI() 