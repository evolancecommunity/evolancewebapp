"""
Evolance Personal Semantic Network
Individual user emotional profiles that evolve over time
"""

import json
import time
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import numpy as np
from .semantic_network import CoreSemanticNetwork, EmotionNode, ConceptNode
from .config import config

@dataclass
class PersonalEmotionNode:
    """Personal emotion node for a specific user"""
    emotion: str
    frequency: int = 0
    intensity_sum: float = 0.0
    last_occurrence: float = 0.0
    triggers: List[str] = None
    coping_effectiveness: Dict[str, float] = None  # strategy -> effectiveness
    
    def __post_init__(self):
        if self.triggers is None:
            self.triggers = []
        if self.coping_effectiveness is None:
            self.coping_effectiveness = {}
    
    @property
    def average_intensity(self) -> float:
        return self.intensity_sum / max(self.frequency, 1)
    
    @property
    def days_since_last(self) -> float:
        return (time.time() - self.last_occurrence) / (24 * 3600)

@dataclass
class PersonalConceptNode:
    """Personal concept node for a specific user"""
    concept: str
    category: str
    emotional_associations: Dict[str, float]  # emotion -> strength
    frequency: int = 0
    last_mentioned: float = 0.0
    user_notes: str = ""
    importance_score: float = 0.0
    
    def update_importance(self):
        """Update importance based on frequency and recency"""
        recency_factor = 1.0 / (1.0 + self.days_since_last)
        self.importance_score = self.frequency * recency_factor
    
    @property
    def days_since_last(self) -> float:
        return (time.time() - self.last_mentioned) / (24 * 3600)

@dataclass
class EmotionalPattern:
    """Patterns in user's emotional life"""
    pattern_type: str  # "trigger", "coping", "cycle", "trend"
    description: str
    confidence: float  # 0 to 1
    frequency: int
    last_observed: float
    examples: List[str] = None
    
    def __post_init__(self):
        if self.examples is None:
            self.examples = []

class PersonalSemanticNetwork:
    """
    Personal semantic network for individual users
    Builds and maintains user-specific emotional knowledge
    """
    
    def __init__(self, user_id: str, core_network: CoreSemanticNetwork):
        self.user_id = user_id
        self.core_network = core_network
        
        # Personal nodes
        self.emotions: Dict[str, PersonalEmotionNode] = {}
        self.concepts: Dict[str, PersonalConceptNode] = {}
        self.patterns: List[EmotionalPattern] = []
        
        # User profile
        self.profile = {
            "onboarding_complete": False,
            "preferred_coping_style": "unknown",
            "emotional_awareness_level": "unknown",
            "support_network": [],
            "goals": [],
            "values": []
        }
        
        # Conversation history (abstracted)
        self.conversation_summaries = []
        self.mood_trends = []
        
        # Initialize from core network
        self._initialize_from_core()
    
    def _initialize_from_core(self):
        """Initialize personal network with core network structure"""
        # Add core emotions with zero frequency
        for emotion_name in self.core_network.emotion_nodes:
            self.emotions[emotion_name] = PersonalEmotionNode(emotion=emotion_name)
        
        # Add core concepts with zero frequency
        for concept_name, concept_data in self.core_network.concept_nodes.items():
            self.concepts[concept_name] = PersonalConceptNode(
                concept=concept_name,
                category=concept_data.category,
                emotional_associations=concept_data.emotional_associations.copy()
            )
    
    def process_onboarding(self, onboarding_data: Dict[str, Any]):
        """Process user onboarding data to build initial profile"""
        
        # Extract key information
        if "stressors" in onboarding_data:
            for stressor in onboarding_data["stressors"]:
                self._add_concept(stressor, "stressor", {"stress": 0.8, "anxiety": 0.6})
        
        if "supports" in onboarding_data:
            for support in onboarding_data["supports"]:
                self._add_concept(support, "support", {"joy": 0.7, "trust": 0.8})
        
        if "hobbies" in onboarding_data:
            for hobby in onboarding_data["hobbies"]:
                self._add_concept(hobby, "hobby", {"joy": 0.8, "relaxation": 0.6})
        
        if "coping_strategies" in onboarding_data:
            for strategy in onboarding_data["coping_strategies"]:
                self._add_concept(strategy, "coping", {"calm": 0.7, "relief": 0.6})
        
        # Update profile
        self.profile.update({
            "onboarding_complete": True,
            "preferred_coping_style": onboarding_data.get("coping_style", "unknown"),
            "emotional_awareness_level": onboarding_data.get("awareness_level", "unknown"),
            "support_network": onboarding_data.get("support_network", []),
            "goals": onboarding_data.get("goals", []),
            "values": onboarding_data.get("values", [])
        })
    
    def _add_concept(self, concept_name: str, category: str, emotional_assocs: Dict[str, float]):
        """Add a new concept to the personal network"""
        if concept_name not in self.concepts:
            self.concepts[concept_name] = PersonalConceptNode(
                concept=concept_name,
                category=category,
                emotional_associations=emotional_assocs
            )
    
    def process_conversation(self, conversation_data: Dict[str, Any]):
        """Process a conversation to update the personal network"""
        
        # Extract emotions mentioned
        detected_emotions = conversation_data.get("emotions", {})
        for emotion, intensity in detected_emotions.items():
            self._update_emotion(emotion, intensity)
        
        # Extract concepts mentioned
        mentioned_concepts = conversation_data.get("concepts", [])
        for concept in mentioned_concepts:
            self._update_concept(concept)
        
        # Extract coping strategies
        coping_mentioned = conversation_data.get("coping_strategies", [])
        for strategy in coping_mentioned:
            self._update_coping_strategy(strategy, conversation_data.get("coping_effectiveness", 0.5))
        
        # Update patterns
        self._detect_patterns(conversation_data)
        
        # Store conversation summary
        summary = {
            "timestamp": time.time(),
            "primary_emotion": max(detected_emotions.items(), key=lambda x: x[1])[0] if detected_emotions else None,
            "concepts_discussed": mentioned_concepts,
            "coping_mentioned": coping_mentioned,
            "overall_sentiment": conversation_data.get("sentiment", 0.0)
        }
        self.conversation_summaries.append(summary)
    
    def _update_emotion(self, emotion: str, intensity: float):
        """Update emotion frequency and intensity"""
        if emotion in self.emotions:
            self.emotions[emotion].frequency += 1
            self.emotions[emotion].intensity_sum += intensity
            self.emotions[emotion].last_occurrence = time.time()
        else:
            # New emotion for this user
            self.emotions[emotion] = PersonalEmotionNode(
                emotion=emotion,
                frequency=1,
                intensity_sum=intensity,
                last_occurrence=time.time()
            )
    
    def _update_concept(self, concept: str):
        """Update concept frequency and recency"""
        if concept in self.concepts:
            self.concepts[concept].frequency += 1
            self.concepts[concept].last_mentioned = time.time()
            self.concepts[concept].update_importance()
        else:
            # New concept for this user
            self.concepts[concept] = PersonalConceptNode(
                concept=concept,
                category="unknown",
                emotional_associations={},
                frequency=1,
                last_mentioned=time.time()
            )
    
    def _update_coping_strategy(self, strategy: str, effectiveness: float):
        """Update coping strategy effectiveness"""
        # Find which emotion this coping strategy was used for
        # For now, assume it was for the most recent emotion
        recent_emotions = sorted(self.emotions.items(), key=lambda x: x[1].last_occurrence, reverse=True)
        if recent_emotions:
            emotion_name = recent_emotions[0][0]
            if emotion_name in self.emotions:
                self.emotions[emotion_name].coping_effectiveness[strategy] = effectiveness
    
    def _detect_patterns(self, conversation_data: Dict[str, Any]):
        """Detect emotional patterns in user behavior"""
        
        # Pattern 1: Frequent emotion-concept associations
        for emotion, emotion_data in self.emotions.items():
            if emotion_data.frequency >= 3:  # Pattern threshold
                # Check if this emotion is often associated with specific concepts
                for concept, concept_data in self.concepts.items():
                    if concept_data.frequency >= 2:
                        # This could be a trigger pattern
                        pattern = EmotionalPattern(
                            pattern_type="trigger",
                            description=f"{concept} often triggers {emotion}",
                            confidence=min(emotion_data.frequency / 10, 1.0),
                            frequency=min(emotion_data.frequency, concept_data.frequency),
                            last_observed=time.time(),
                            examples=[f"User mentioned {concept} and felt {emotion}"]
                        )
                        self._add_pattern_if_new(pattern)
        
        # Pattern 2: Effective coping strategies
        for emotion, emotion_data in self.emotions.items():
            effective_strategies = [
                strategy for strategy, effectiveness in emotion_data.coping_effectiveness.items()
                if effectiveness >= 0.7
            ]
            if effective_strategies:
                pattern = EmotionalPattern(
                    pattern_type="coping",
                    description=f"Effective coping for {emotion}: {', '.join(effective_strategies)}",
                    confidence=0.8,
                    frequency=len(effective_strategies),
                    last_observed=time.time(),
                    examples=effective_strategies
                )
                self._add_pattern_if_new(pattern)
    
    def _add_pattern_if_new(self, pattern: EmotionalPattern):
        """Add pattern if it's not already present"""
        existing_patterns = [p.description for p in self.patterns]
        if pattern.description not in existing_patterns:
            self.patterns.append(pattern)
    
    def get_emotional_context(self, current_emotions: List[str], current_concepts: List[str]) -> Dict[str, Any]:
        """Get personalized emotional context for current situation"""
        
        context = {
            "user_emotional_profile": {},
            "relevant_patterns": [],
            "personalized_suggestions": [],
            "emotional_history": {},
            "coping_recommendations": []
        }
        
        # Get user's emotional profile for current emotions
        for emotion in current_emotions:
            if emotion in self.emotions:
                emotion_data = self.emotions[emotion]
                context["user_emotional_profile"][emotion] = {
                    "frequency": emotion_data.frequency,
                    "average_intensity": emotion_data.average_intensity,
                    "days_since_last": emotion_data.days_since_last,
                    "effective_coping": [
                        strategy for strategy, effectiveness in emotion_data.coping_effectiveness.items()
                        if effectiveness >= 0.7
                    ]
                }
        
        # Get relevant patterns
        for pattern in self.patterns:
            if any(emotion in pattern.description for emotion in current_emotions):
                context["relevant_patterns"].append(asdict(pattern))
        
        # Get personalized suggestions based on history
        for concept in current_concepts:
            if concept in self.concepts:
                concept_data = self.concepts[concept]
                if concept_data.importance_score > 0.5:
                    context["personalized_suggestions"].append({
                        "concept": concept,
                        "importance": concept_data.importance_score,
                        "emotional_associations": concept_data.emotional_associations
                    })
        
        # Get coping recommendations
        for emotion in current_emotions:
            if emotion in self.emotions:
                effective_coping = [
                    strategy for strategy, effectiveness in self.emotions[emotion].coping_effectiveness.items()
                    if effectiveness >= 0.7
                ]
                if effective_coping:
                    context["coping_recommendations"].append({
                        "emotion": emotion,
                        "strategies": effective_coping
                    })
        
        return context
    
    def get_user_summary(self) -> Dict[str, Any]:
        """Get a summary of the user's emotional profile"""
        
        # Most frequent emotions
        frequent_emotions = sorted(
            self.emotions.items(),
            key=lambda x: x[1].frequency,
            reverse=True
        )[:5]
        
        # Most important concepts
        important_concepts = sorted(
            self.concepts.items(),
            key=lambda x: x[1].importance_score,
            reverse=True
        )[:10]
        
        # Recent patterns
        recent_patterns = sorted(
            self.patterns,
            key=lambda x: x.last_observed,
            reverse=True
        )[:5]
        
        return {
            "user_id": self.user_id,
            "profile": self.profile,
            "frequent_emotions": [
                {
                    "emotion": emotion,
                    "frequency": data.frequency,
                    "average_intensity": data.average_intensity
                }
                for emotion, data in frequent_emotions
            ],
            "important_concepts": [
                {
                    "concept": concept,
                    "category": data.category,
                    "importance": data.importance_score,
                    "frequency": data.frequency
                }
                for concept, data in important_concepts
            ],
            "recent_patterns": [asdict(pattern) for pattern in recent_patterns],
            "conversation_count": len(self.conversation_summaries),
            "network_size": {
                "emotions": len(self.emotions),
                "concepts": len(self.concepts),
                "patterns": len(self.patterns)
            }
        }
    
    def export_network(self) -> Dict[str, Any]:
        """Export the personal network for persistence"""
        return {
            "user_id": self.user_id,
            "profile": self.profile,
            "emotions": {name: asdict(emotion) for name, emotion in self.emotions.items()},
            "concepts": {name: asdict(concept) for name, concept in self.concepts.items()},
            "patterns": [asdict(pattern) for pattern in self.patterns],
            "conversation_summaries": self.conversation_summaries,
            "mood_trends": self.mood_trends
        }
    
    def import_network(self, network_data: Dict[str, Any]):
        """Import personal network from persistence"""
        self.user_id = network_data["user_id"]
        self.profile = network_data["profile"]
        
        # Import emotions
        for name, data in network_data["emotions"].items():
            self.emotions[name] = PersonalEmotionNode(**data)
        
        # Import concepts
        for name, data in network_data["concepts"].items():
            self.concepts[name] = PersonalConceptNode(**data)
        
        # Import patterns
        self.patterns = [EmotionalPattern(**data) for data in network_data["patterns"]]
        
        # Import conversation history
        self.conversation_summaries = network_data["conversation_summaries"]
        self.mood_trends = network_data["mood_trends"] 