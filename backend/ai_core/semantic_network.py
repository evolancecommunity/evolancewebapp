"""
Evolance Core Semantic Network
The foundation of emotional intelligence - maps emotions, concepts, and relationships
"""

import json
import networkx as nx
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import numpy as np
from .config import config

@dataclass
class EmotionNode:
    """Represents an emotion in the semantic network"""
    name: str
    category: str  # primary, secondary, mixed
    valence: float  # -1 to 1 (negative to positive)
    arousal: float  # 0 to 1 (calm to excited)
    intensity: float  # 0 to 1
    body_regions: List[str]  # chest, head, stomach, etc.
    synonyms: List[str]
    antonyms: List[str]
    triggers: List[str]
    coping_strategies: List[str]

@dataclass
class ConceptNode:
    """Represents a concept or entity in the semantic network"""
    name: str
    category: str  # work, family, health, hobby, etc.
    emotional_associations: Dict[str, float]  # emotion -> strength
    frequency: int
    last_mentioned: float
    user_specific: bool = False

@dataclass
class Relationship:
    """Represents a relationship between nodes"""
    source: str
    target: str
    relationship_type: str  # triggers, evokes, helps, hinders, etc.
    strength: float  # 0 to 1
    bidirectional: bool = False
    context: Dict[str, Any] = None

class CoreSemanticNetwork:
    """
    Evolance's core semantic network - the foundation of emotional intelligence
    Based on Plutchik's Wheel of Emotions, Russell's Circumplex, and psychological research
    """
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.emotion_nodes: Dict[str, EmotionNode] = {}
        self.concept_nodes: Dict[str, ConceptNode] = {}
        self.relationships: List[Relationship] = []
        
        # Initialize the core network
        self._initialize_emotions()
        self._initialize_concepts()
        self._initialize_relationships()
    
    def _initialize_emotions(self):
        """Initialize the core emotion nodes based on Plutchik's Wheel"""
        
        # Primary emotions (Plutchik's 8)
        primary_emotions = [
            EmotionNode(
                name="joy",
                category="primary",
                valence=0.8,
                arousal=0.6,
                intensity=0.7,
                body_regions=["chest", "face", "whole_body"],
                synonyms=["happiness", "elation", "delight"],
                antonyms=["sadness", "grief"],
                triggers=["success", "achievement", "social_connection"],
                coping_strategies=["gratitude", "celebration", "sharing"]
            ),
            EmotionNode(
                name="trust",
                category="primary",
                valence=0.6,
                arousal=0.3,
                intensity=0.5,
                body_regions=["chest", "heart"],
                synonyms=["confidence", "faith", "reliance"],
                antonyms=["distrust", "suspicion"],
                triggers=["reliability", "consistency", "support"],
                coping_strategies=["open_communication", "building_rapport"]
            ),
            EmotionNode(
                name="fear",
                category="primary",
                valence=-0.7,
                arousal=0.8,
                intensity=0.8,
                body_regions=["chest", "stomach", "throat"],
                synonyms=["anxiety", "worry", "terror"],
                antonyms=["courage", "confidence"],
                triggers=["uncertainty", "threat", "loss"],
                coping_strategies=["deep_breathing", "grounding", "safety_planning"]
            ),
            EmotionNode(
                name="surprise",
                category="primary",
                valence=0.0,  # Can be positive or negative
                arousal=0.9,
                intensity=0.6,
                body_regions=["head", "chest"],
                synonyms=["shock", "amazement", "astonishment"],
                antonyms=["expectation", "anticipation"],
                triggers=["unexpected_events", "sudden_changes"],
                coping_strategies=["processing", "adaptation"]
            ),
            EmotionNode(
                name="sadness",
                category="primary",
                valence=-0.8,
                arousal=0.2,
                intensity=0.7,
                body_regions=["chest", "head", "limbs"],
                synonyms=["grief", "sorrow", "melancholy"],
                antonyms=["joy", "happiness"],
                triggers=["loss", "failure", "disappointment"],
                coping_strategies=["self_compassion", "support_seeking", "expression"]
            ),
            EmotionNode(
                name="disgust",
                category="primary",
                valence=-0.6,
                arousal=0.4,
                intensity=0.5,
                body_regions=["stomach", "throat", "face"],
                synonyms=["revulsion", "aversion", "contempt"],
                antonyms=["attraction", "desire"],
                triggers=["unpleasant_sensations", "moral_violations"],
                coping_strategies=["avoidance", "cleansing", "reframing"]
            ),
            EmotionNode(
                name="anger",
                category="primary",
                valence=-0.5,
                arousal=0.9,
                intensity=0.8,
                body_regions=["chest", "head", "arms"],
                synonyms=["rage", "fury", "irritation"],
                antonyms=["calmness", "peace"],
                triggers=["injustice", "frustration", "threat"],
                coping_strategies=["timeout", "physical_exercise", "communication"]
            ),
            EmotionNode(
                name="anticipation",
                category="primary",
                valence=0.4,
                arousal=0.7,
                intensity=0.6,
                body_regions=["stomach", "chest"],
                synonyms=["expectation", "hope", "excitement"],
                antonyms=["surprise", "disappointment"],
                triggers=["future_events", "possibilities"],
                coping_strategies=["planning", "preparation", "optimism"]
            )
        ]
        
        # Add primary emotions to the network
        for emotion in primary_emotions:
            self.emotion_nodes[emotion.name] = emotion
            self.graph.add_node(emotion.name, type="emotion", data=asdict(emotion))
        
        # Add mixed emotions (Plutchik's combinations)
        self._add_mixed_emotions()
    
    def _add_mixed_emotions(self):
        """Add mixed emotions based on Plutchik's combinations"""
        
        mixed_emotions = [
            EmotionNode(
                name="love",
                category="mixed",
                valence=0.9,
                arousal=0.5,
                intensity=0.8,
                body_regions=["chest", "heart", "face"],
                synonyms=["affection", "adoration", "devotion"],
                antonyms=["hate", "indifference"],
                triggers=["intimacy", "connection", "care"],
                coping_strategies=["expression", "quality_time", "appreciation"]
            ),
            EmotionNode(
                name="optimism",
                category="mixed",
                valence=0.7,
                arousal=0.6,
                intensity=0.6,
                body_regions=["chest", "stomach"],
                synonyms=["hope", "confidence", "positivity"],
                antonyms=["pessimism", "despair"],
                triggers=["possibilities", "progress", "support"],
                coping_strategies=["goal_setting", "positive_reframing"]
            ),
            EmotionNode(
                name="submission",
                category="mixed",
                valence=0.2,
                arousal=0.4,
                intensity=0.5,
                body_regions=["chest", "head"],
                synonyms=["acceptance", "resignation", "yielding"],
                antonyms=["resistance", "defiance"],
                triggers=["authority", "inevitability", "peace"],
                coping_strategies=["mindfulness", "acceptance_practice"]
            ),
            EmotionNode(
                name="awe",
                category="mixed",
                valence=0.6,
                arousal=0.8,
                intensity=0.7,
                body_regions=["head", "chest"],
                synonyms=["wonder", "amazement", "reverence"],
                antonyms=["indifference", "cynicism"],
                triggers=["grandeur", "beauty", "mystery"],
                coping_strategies=["appreciation", "contemplation"]
            ),
            EmotionNode(
                name="disappointment",
                category="mixed",
                valence=-0.6,
                arousal=0.3,
                intensity=0.6,
                body_regions=["chest", "head"],
                synonyms=["letdown", "frustration", "discouragement"],
                antonyms=["satisfaction", "fulfillment"],
                triggers=["failed_expectations", "unmet_goals"],
                coping_strategies=["realistic_expectations", "alternative_planning"]
            ),
            EmotionNode(
                name="remorse",
                category="mixed",
                valence=-0.7,
                arousal=0.5,
                intensity=0.7,
                body_regions=["chest", "stomach"],
                synonyms=["guilt", "regret", "contrition"],
                antonyms=["pride", "satisfaction"],
                triggers=["harmful_actions", "moral_violations"],
                coping_strategies=["apology", "amends", "forgiveness"]
            ),
            EmotionNode(
                name="contempt",
                category="mixed",
                valence=-0.5,
                arousal=0.3,
                intensity=0.5,
                body_regions=["face", "chest"],
                synonyms=["scorn", "disdain", "disrespect"],
                antonyms=["respect", "admiration"],
                triggers=["inferiority", "moral_superiority"],
                coping_strategies=["empathy", "understanding", "humility"]
            ),
            EmotionNode(
                name="aggressiveness",
                category="mixed",
                valence=-0.3,
                arousal=0.9,
                intensity=0.8,
                body_regions=["arms", "chest", "head"],
                synonyms=["assertiveness", "determination", "drive"],
                antonyms=["passivity", "submission"],
                triggers=["challenges", "goals", "competition"],
                coping_strategies=["channeled_energy", "constructive_action"]
            )
        ]
        
        # Add mixed emotions to the network
        for emotion in mixed_emotions:
            self.emotion_nodes[emotion.name] = emotion
            self.graph.add_node(emotion.name, type="emotion", data=asdict(emotion))
    
    def _initialize_concepts(self):
        """Initialize core concept nodes"""
        
        core_concepts = [
            # Work-related concepts
            ConceptNode("work", "occupation", {"stress": 0.8, "achievement": 0.6}, 0, 0),
            ConceptNode("deadline", "work", {"stress": 0.9, "anxiety": 0.7}, 0, 0),
            ConceptNode("colleague", "work", {"trust": 0.5, "stress": 0.3}, 0, 0),
            ConceptNode("boss", "work", {"fear": 0.6, "respect": 0.4}, 0, 0),
            
            # Family-related concepts
            ConceptNode("family", "relationships", {"love": 0.8, "support": 0.7}, 0, 0),
            ConceptNode("mother", "family", {"love": 0.9, "trust": 0.8}, 0, 0),
            ConceptNode("father", "family", {"respect": 0.7, "love": 0.6}, 0, 0),
            ConceptNode("sibling", "family", {"love": 0.6, "competition": 0.4}, 0, 0),
            
            # Health-related concepts
            ConceptNode("health", "wellness", {"concern": 0.6, "care": 0.7}, 0, 0),
            ConceptNode("sleep", "health", {"rest": 0.8, "anxiety": 0.3}, 0, 0),
            ConceptNode("exercise", "health", {"energy": 0.8, "accomplishment": 0.6}, 0, 0),
            ConceptNode("meditation", "health", {"calm": 0.9, "peace": 0.8}, 0, 0),
            
            # Social concepts
            ConceptNode("friend", "relationships", {"joy": 0.7, "support": 0.8}, 0, 0),
            ConceptNode("social_event", "social", {"anxiety": 0.5, "excitement": 0.6}, 0, 0),
            ConceptNode("conversation", "social", {"connection": 0.6, "anxiety": 0.3}, 0, 0),
            
            # Hobby concepts
            ConceptNode("painting", "hobby", {"joy": 0.8, "creativity": 0.9}, 0, 0),
            ConceptNode("music", "hobby", {"joy": 0.7, "calm": 0.6}, 0, 0),
            ConceptNode("reading", "hobby", {"escape": 0.7, "learning": 0.6}, 0, 0),
            ConceptNode("cooking", "hobby", {"accomplishment": 0.6, "creativity": 0.5}, 0, 0),
        ]
        
        for concept in core_concepts:
            self.concept_nodes[concept.name] = concept
            self.graph.add_node(concept.name, type="concept", data=asdict(concept))
    
    def _initialize_relationships(self):
        """Initialize core relationships between emotions and concepts"""
        
        # Work relationships
        self._add_relationship("work", "stress", "triggers", 0.8)
        self._add_relationship("deadline", "anxiety", "triggers", 0.9)
        self._add_relationship("deadline", "fear", "triggers", 0.7)
        self._add_relationship("achievement", "joy", "evokes", 0.8)
        self._add_relationship("achievement", "pride", "evokes", 0.7)
        
        # Family relationships
        self._add_relationship("family", "love", "evokes", 0.8)
        self._add_relationship("family", "support", "provides", 0.7)
        self._add_relationship("mother", "love", "evokes", 0.9)
        self._add_relationship("mother", "trust", "builds", 0.8)
        
        # Health relationships
        self._add_relationship("exercise", "energy", "increases", 0.8)
        self._add_relationship("exercise", "joy", "evokes", 0.6)
        self._add_relationship("meditation", "calm", "promotes", 0.9)
        self._add_relationship("meditation", "anxiety", "reduces", 0.7)
        
        # Hobby relationships
        self._add_relationship("painting", "joy", "evokes", 0.8)
        self._add_relationship("painting", "creativity", "expresses", 0.9)
        self._add_relationship("music", "calm", "promotes", 0.7)
        self._add_relationship("music", "joy", "evokes", 0.6)
        
        # Coping strategy relationships
        self._add_relationship("deep_breathing", "anxiety", "reduces", 0.8)
        self._add_relationship("deep_breathing", "calm", "promotes", 0.9)
        self._add_relationship("exercise", "stress", "reduces", 0.7)
        self._add_relationship("social_connection", "loneliness", "reduces", 0.8)
    
    def _add_relationship(self, source: str, target: str, rel_type: str, strength: float):
        """Add a relationship between two nodes"""
        relationship = Relationship(source, target, rel_type, strength)
        self.relationships.append(relationship)
        
        # Add to graph
        self.graph.add_edge(source, target, type=rel_type, strength=strength)
    
    def get_emotion_info(self, emotion_name: str) -> Optional[EmotionNode]:
        """Get information about a specific emotion"""
        return self.emotion_nodes.get(emotion_name)
    
    def get_concept_info(self, concept_name: str) -> Optional[ConceptNode]:
        """Get information about a specific concept"""
        return self.concept_nodes.get(concept_name)
    
    def find_related_emotions(self, concept: str) -> List[Tuple[str, float]]:
        """Find emotions related to a concept"""
        if concept not in self.graph:
            return []
        
        related = []
        for neighbor in self.graph.neighbors(concept):
            if self.graph.nodes[neighbor].get("type") == "emotion":
                # Get the strongest relationship
                max_strength = 0
                for edge_data in self.graph.get_edge_data(concept, neighbor).values():
                    max_strength = max(max_strength, edge_data.get("strength", 0))
                related.append((neighbor, max_strength))
        
        return sorted(related, key=lambda x: x[1], reverse=True)
    
    def find_related_concepts(self, emotion: str) -> List[Tuple[str, float]]:
        """Find concepts related to an emotion"""
        if emotion not in self.graph:
            return []
        
        related = []
        for neighbor in self.graph.neighbors(emotion):
            if self.graph.nodes[neighbor].get("type") == "concept":
                # Get the strongest relationship
                max_strength = 0
                for edge_data in self.graph.get_edge_data(emotion, neighbor).values():
                    max_strength = max(max_strength, edge_data.get("strength", 0))
                related.append((neighbor, max_strength))
        
        return sorted(related, key=lambda x: x[1], reverse=True)
    
    def get_coping_strategies(self, emotion: str) -> List[str]:
        """Get coping strategies for a specific emotion"""
        emotion_node = self.get_emotion_info(emotion)
        if emotion_node:
            return emotion_node.coping_strategies
        return []
    
    def get_body_mapping(self, emotion: str) -> List[str]:
        """Get body regions associated with an emotion"""
        emotion_node = self.get_emotion_info(emotion)
        if emotion_node:
            return emotion_node.body_regions
        return []
    
    def analyze_text_emotions(self, text: str) -> Dict[str, float]:
        """Analyze text and return emotion probabilities"""
        # This will be implemented with NLP models
        # For now, return placeholder
        return {"joy": 0.3, "sadness": 0.1, "anxiety": 0.2}
    
    def get_emotional_context(self, concepts: List[str]) -> Dict[str, Any]:
        """Get emotional context for a set of concepts"""
        context = {
            "primary_emotions": [],
            "coping_strategies": [],
            "body_sensations": [],
            "emotional_intensity": 0.0
        }
        
        for concept in concepts:
            related_emotions = self.find_related_emotions(concept)
            for emotion, strength in related_emotions[:3]:  # Top 3 emotions
                context["primary_emotions"].append({
                    "emotion": emotion,
                    "strength": strength,
                    "body_regions": self.get_body_mapping(emotion),
                    "coping_strategies": self.get_coping_strategies(emotion)
                })
        
        return context
    
    def export_network(self) -> Dict[str, Any]:
        """Export the network for persistence"""
        return {
            "emotions": {name: asdict(emotion) for name, emotion in self.emotion_nodes.items()},
            "concepts": {name: asdict(concept) for name, concept in self.concept_nodes.items()},
            "relationships": [asdict(rel) for rel in self.relationships]
        }

# Global instance
core_network = CoreSemanticNetwork() 