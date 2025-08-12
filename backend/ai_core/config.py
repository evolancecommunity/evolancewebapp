"""
Evolance AI Core Configuration
Production-ready settings for scalable AI deployment
"""

import os
from typing import Dict, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ModelConfig:
    """Configuration for AI model components"""
    # Core model settings
    model_name: str = "evolance-emotional-llm"
    model_size: str = "7B"  # Start with 7B, scale to 13B, 30B, 70B
    max_context_length: int = 8192
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    
    # Training settings
    learning_rate: float = 1e-5
    batch_size: int = 4
    gradient_accumulation_steps: int = 8
    max_grad_norm: float = 1.0
    
    # Memory settings
    memory_window_size: int = 100
    semantic_network_cache_size: int = 1000
    vector_db_dimensions: int = 768

@dataclass
class EmotionConfig:
    """Configuration for emotion detection and analysis"""
    # Emotion classification
    emotion_classes: list = None
    sentiment_threshold: float = 0.6
    emotion_confidence_threshold: float = 0.7
    
    # Body-emotion mapping
    enable_somatic_mapping: bool = True
    somatic_sensitivity: float = 0.8
    
    def __post_init__(self):
        if self.emotion_classes is None:
            self.emotion_classes = [
                'joy', 'trust', 'fear', 'surprise', 'sadness', 
                'disgust', 'anger', 'anticipation', 'love', 
                'optimism', 'submission', 'awe', 'disappointment', 
                'remorse', 'contempt', 'aggressiveness'
            ]

@dataclass
class MemoryConfig:
    """Configuration for memory management"""
    # Vector database
    vector_db_type: str = "chromadb"  # or "pinecone", "weaviate"
    vector_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    similarity_threshold: float = 0.75
    max_memory_retrieval: int = 5
    
    # Semantic network
    semantic_network_type: str = "mongodb"
    network_update_frequency: int = 1  # Update after each conversation
    max_network_nodes: int = 1000
    
    # Memory consolidation
    consolidation_batch_size: int = 10
    memory_decay_factor: float = 0.95
    retention_period_days: int = 365

@dataclass
class PrivacyConfig:
    """Configuration for privacy and security"""
    # Data handling
    anonymize_personal_data: bool = True
    store_only_emotional_patterns: bool = True
    encryption_enabled: bool = True
    data_retention_days: int = 365
    
    # User control
    allow_data_export: bool = True
    allow_data_deletion: bool = True
    opt_out_tracking: bool = True

@dataclass
class ScalingConfig:
    """Configuration for horizontal scaling"""
    # Load balancing
    enable_load_balancing: bool = True
    max_concurrent_users: int = 10000
    request_timeout: int = 30
    
    # Caching
    enable_redis_cache: bool = True
    cache_ttl_seconds: int = 3600
    cache_max_size: int = 10000
    
    # Database scaling
    enable_database_sharding: bool = True
    shard_by_user_id: bool = True
    max_connections_per_pool: int = 100

class EvolanceConfig:
    """Main configuration class for Evolance AI"""
    
    def __init__(self, config_path: str = None):
        self.model = ModelConfig()
        self.emotion = EmotionConfig()
        self.memory = MemoryConfig()
        self.privacy = PrivacyConfig()
        self.scaling = ScalingConfig()
        
        # Load from environment variables
        self._load_from_env()
        
        # Load from config file if provided
        if config_path:
            self._load_from_file(config_path)
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # Model settings
        if os.getenv("EVOLANCE_MODEL_SIZE"):
            self.model.model_size = os.getenv("EVOLANCE_MODEL_SIZE")
        
        if os.getenv("EVOLANCE_MAX_CONTEXT_LENGTH"):
            self.model.max_context_length = int(os.getenv("EVOLANCE_MAX_CONTEXT_LENGTH"))
        
        # Memory settings
        if os.getenv("EVOLANCE_VECTOR_DB_TYPE"):
            self.memory.vector_db_type = os.getenv("EVOLANCE_VECTOR_DB_TYPE")
        
        # Privacy settings
        if os.getenv("EVOLANCE_ENCRYPTION_ENABLED"):
            self.privacy.encryption_enabled = os.getenv("EVOLANCE_ENCRYPTION_ENABLED").lower() == "true"
    
    def _load_from_file(self, config_path: str):
        """Load configuration from JSON/YAML file"""
        # Implementation for file-based config loading
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "model": self.model.__dict__,
            "emotion": self.emotion.__dict__,
            "memory": self.memory.__dict__,
            "privacy": self.privacy.__dict__,
            "scaling": self.scaling.__dict__
        }
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        # Add validation logic
        return True

# Global configuration instance
config = EvolanceConfig() 