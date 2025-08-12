"""
Evolance Memory Management System
Handles short-term and long-term memory for personalized AI interactions
"""

import time
import hashlib
import json
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, asdict
from collections import deque
import numpy as np

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("Warning: ChromaDB not available. Using in-memory storage.")

from .config import config
from .personal_network import PersonalSemanticNetwork

@dataclass
class MemoryEntry:
    """A single memory entry"""
    id: str
    user_id: str
    content: str
    emotion: str
    intensity: float
    concepts: List[str]
    timestamp: float
    memory_type: str  # "conversation", "pattern", "insight"
    importance: float
    context: Dict[str, Any]
    embedding: Optional[List[float]] = None

@dataclass
class ConversationMemory:
    """Memory for a single conversation"""
    conversation_id: str
    user_id: str
    messages: List[Dict[str, Any]]
    summary: str
    emotions: List[str]
    concepts: List[str]
    start_time: float
    end_time: float
    importance_score: float

class MemoryManager:
    """
    Manages both short-term and long-term memory for Evolance
    Combines vector storage with semantic networks
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        
        # Short-term memory (current session)
        self.short_term_memory = deque(maxlen=config.model.memory_window_size)
        self.current_conversation = None
        
        # Long-term memory (vector database)
        self.vector_db = None
        self._initialize_vector_db()
        
        # Memory consolidation
        self.consolidation_queue = []
        self.last_consolidation = time.time()
        
        # Memory statistics
        self.memory_stats = {
            "total_memories": 0,
            "conversations": 0,
            "patterns_detected": 0,
            "last_access": time.time()
        }
    
    def _initialize_vector_db(self):
        """Initialize vector database for long-term memory"""
        if CHROMADB_AVAILABLE:
            try:
                # Create persistent ChromaDB client
                self.vector_db = chromadb.PersistentClient(
                    path=f"./data/memory/{self.user_id}",
                    settings=Settings(
                        anonymized_telemetry=False,
                        allow_reset=True
                    )
                )
                
                # Get or create collection for this user
                self.memory_collection = self.vector_db.get_or_create_collection(
                    name=f"user_{self.user_id}_memories",
                    metadata={"user_id": self.user_id, "type": "emotional_memories"}
                )
                
            except Exception as e:
                print(f"Warning: Could not initialize ChromaDB: {e}")
                self.vector_db = None
        else:
            # Fallback to in-memory storage
            self.memory_collection = None
            self.in_memory_storage = []
    
    def add_to_short_term(self, message: Dict[str, Any]):
        """Add message to short-term memory"""
        memory_entry = {
            "timestamp": time.time(),
            "content": message.get("content", ""),
            "emotion": message.get("emotion", "neutral"),
            "intensity": message.get("intensity", 0.5),
            "concepts": message.get("concepts", []),
            "user_id": message.get("user_id", self.user_id),
            "message_type": message.get("type", "user")
        }
        
        self.short_term_memory.append(memory_entry)
        
        # Update current conversation
        if self.current_conversation is None:
            self.current_conversation = ConversationMemory(
                conversation_id=f"conv_{int(time.time())}",
                user_id=self.user_id,
                messages=[],
                summary="",
                emotions=[],
                concepts=[],
                start_time=time.time(),
                end_time=0,
                importance_score=0.0
            )
        
        self.current_conversation.messages.append(memory_entry)
        self.current_conversation.emotions.append(memory_entry["emotion"])
        self.current_conversation.concepts.extend(memory_entry["concepts"])
    
    def get_short_term_context(self, max_messages: int = 10) -> List[Dict[str, Any]]:
        """Get recent context from short-term memory"""
        return list(self.short_term_memory)[-max_messages:]
    
    def end_conversation(self):
        """End current conversation and prepare for consolidation"""
        if self.current_conversation:
            self.current_conversation.end_time = time.time()
            
            # Generate conversation summary
            summary = self._generate_conversation_summary(self.current_conversation)
            self.current_conversation.summary = summary
            
            # Calculate importance score
            importance = self._calculate_conversation_importance(self.current_conversation)
            self.current_conversation.importance_score = importance
            
            # Add to consolidation queue
            self.consolidation_queue.append(self.current_conversation)
            
            # Update statistics
            self.memory_stats["conversations"] += 1
            self.current_conversation = None
    
    def _generate_conversation_summary(self, conversation: ConversationMemory) -> str:
        """Generate a summary of the conversation"""
        if not conversation.messages:
            return "Empty conversation"
        
        # Extract key information
        emotions = list(set(conversation.emotions))
        concepts = list(set(conversation.concepts))
        
        # Count message types
        user_messages = [m for m in conversation.messages if m.get("message_type") == "user"]
        ai_messages = [m for m in conversation.messages if m.get("message_type") == "ai"]
        
        # Generate summary
        summary_parts = []
        
        if emotions:
            primary_emotion = max(set(conversation.emotions), key=conversation.emotions.count)
            summary_parts.append(f"Primary emotion: {primary_emotion}")
        
        if concepts:
            summary_parts.append(f"Topics discussed: {', '.join(concepts[:5])}")
        
        summary_parts.append(f"User messages: {len(user_messages)}")
        summary_parts.append(f"AI responses: {len(ai_messages)}")
        
        duration = conversation.end_time - conversation.start_time
        summary_parts.append(f"Duration: {duration:.1f} seconds")
        
        return "; ".join(summary_parts)
    
    def _calculate_conversation_importance(self, conversation: ConversationMemory) -> float:
        """Calculate importance score for conversation"""
        importance = 0.0
        
        # Factor 1: Emotional intensity
        if conversation.emotions:
            avg_intensity = np.mean([
                msg.get("intensity", 0.5) for msg in conversation.messages
                if msg.get("message_type") == "user"
            ])
            importance += avg_intensity * 0.4
        
        # Factor 2: Conversation length
        message_count = len(conversation.messages)
        importance += min(message_count / 20, 1.0) * 0.2
        
        # Factor 3: Unique concepts discussed
        unique_concepts = len(set(conversation.concepts))
        importance += min(unique_concepts / 10, 1.0) * 0.2
        
        # Factor 4: Emotional diversity
        unique_emotions = len(set(conversation.emotions))
        importance += min(unique_emotions / 5, 1.0) * 0.2
        
        return min(importance, 1.0)
    
    def consolidate_memories(self, personal_network: PersonalSemanticNetwork):
        """Consolidate memories from queue to long-term storage"""
        if not self.consolidation_queue:
            return
        
        for conversation in self.consolidation_queue:
            # Create memory entry
            memory_entry = MemoryEntry(
                id=f"mem_{int(time.time())}_{hash(conversation.conversation_id) % 10000}",
                user_id=self.user_id,
                content=conversation.summary,
                emotion=conversation.emotions[0] if conversation.emotions else "neutral",
                intensity=np.mean([msg.get("intensity", 0.5) for msg in conversation.messages]),
                concepts=list(set(conversation.concepts)),
                timestamp=conversation.start_time,
                memory_type="conversation",
                importance=conversation.importance_score,
                context={
                    "conversation_id": conversation.conversation_id,
                    "message_count": len(conversation.messages),
                    "duration": conversation.end_time - conversation.start_time
                }
            )
            
            # Store in vector database
            self._store_memory(memory_entry)
            
            # Update personal network
            self._update_personal_network(conversation, personal_network)
        
        # Clear consolidation queue
        self.consolidation_queue.clear()
        self.last_consolidation = time.time()
    
    def _store_memory(self, memory_entry: MemoryEntry):
        """Store memory in vector database"""
        if self.memory_collection and CHROMADB_AVAILABLE:
            try:
                # Generate embedding (placeholder - would use actual embedding model)
                embedding = self._generate_embedding(memory_entry.content)
                memory_entry.embedding = embedding
                
                # Store in ChromaDB
                self.memory_collection.add(
                    documents=[memory_entry.content],
                    metadatas=[{
                        "user_id": memory_entry.user_id,
                        "emotion": memory_entry.emotion,
                        "intensity": memory_entry.intensity,
                        "concepts": json.dumps(memory_entry.concepts),
                        "timestamp": memory_entry.timestamp,
                        "memory_type": memory_entry.memory_type,
                        "importance": memory_entry.importance
                    }],
                    ids=[memory_entry.id],
                    embeddings=[embedding]
                )
                
                self.memory_stats["total_memories"] += 1
                
            except Exception as e:
                print(f"Error storing memory in ChromaDB: {e}")
                # Fallback to in-memory storage
                self.in_memory_storage.append(asdict(memory_entry))
        else:
            # Use in-memory storage
            self.in_memory_storage.append(asdict(memory_entry))
            self.memory_stats["total_memories"] += 1
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text (placeholder implementation)"""
        # This would use a proper embedding model like sentence-transformers
        # For now, return a simple hash-based embedding
        hash_value = hashlib.md5(text.encode()).hexdigest()
        embedding = [float(int(hash_value[i:i+2], 16)) / 255.0 for i in range(0, 32, 2)]
        return embedding[:config.memory.vector_db_dimensions]
    
    def _update_personal_network(self, conversation: ConversationMemory, 
                               personal_network: PersonalSemanticNetwork):
        """Update personal network with conversation data"""
        
        # Process conversation data
        conversation_data = {
            "emotions": conversation.emotions,
            "concepts": conversation.concepts,
            "coping_strategies": [],  # Would extract from AI responses
            "coping_effectiveness": 0.5  # Would be determined by user feedback
        }
        
        personal_network.process_conversation(conversation_data)
    
    def retrieve_relevant_memories(self, query: str, max_results: int = 5) -> List[MemoryEntry]:
        """Retrieve memories relevant to current query"""
        
        if self.memory_collection and CHROMADB_AVAILABLE:
            try:
                # Generate query embedding
                query_embedding = self._generate_embedding(query)
                
                # Search in ChromaDB
                results = self.memory_collection.query(
                    query_embeddings=[query_embedding],
                    n_results=max_results,
                    where={"user_id": self.user_id}
                )
                
                # Convert to MemoryEntry objects
                memories = []
                for i in range(len(results["ids"][0])):
                    memory = MemoryEntry(
                        id=results["ids"][0][i],
                        user_id=self.user_id,
                        content=results["documents"][0][i],
                        emotion=results["metadatas"][0][i].get("emotion", "neutral"),
                        intensity=results["metadatas"][0][i].get("intensity", 0.5),
                        concepts=json.loads(results["metadatas"][0][i].get("concepts", "[]")),
                        timestamp=results["metadatas"][0][i].get("timestamp", time.time()),
                        memory_type=results["metadatas"][0][i].get("memory_type", "conversation"),
                        importance=results["metadatas"][0][i].get("importance", 0.5),
                        context={}
                    )
                    memories.append(memory)
                
                return memories
                
            except Exception as e:
                print(f"Error retrieving memories from ChromaDB: {e}")
                return self._retrieve_from_memory(query, max_results)
        else:
            return self._retrieve_from_memory(query, max_results)
    
    def _retrieve_from_memory(self, query: str, max_results: int) -> List[MemoryEntry]:
        """Retrieve memories from in-memory storage"""
        # Simple keyword-based retrieval
        query_words = set(query.lower().split())
        
        relevant_memories = []
        for memory_dict in self.in_memory_storage:
            memory = MemoryEntry(**memory_dict)
            
            # Calculate relevance score
            memory_words = set(memory.content.lower().split())
            overlap = len(query_words.intersection(memory_words))
            relevance = overlap / max(len(query_words), 1)
            
            if relevance > 0.1:  # Minimum relevance threshold
                relevant_memories.append((memory, relevance))
        
        # Sort by relevance and return top results
        relevant_memories.sort(key=lambda x: x[1], reverse=True)
        return [memory for memory, _ in relevant_memories[:max_results]]
    
    def get_memory_context(self, query: str, personal_network: PersonalSemanticNetwork) -> Dict[str, Any]:
        """Get comprehensive memory context for a query"""
        
        # Get relevant memories
        relevant_memories = self.retrieve_relevant_memories(query)
        
        # Get short-term context
        short_term_context = self.get_short_term_context()
        
        # Get personal network context
        # Extract concepts from query for personal network lookup
        query_concepts = self._extract_concepts_from_query(query)
        personal_context = personal_network.get_emotional_context([], query_concepts)
        
        return {
            "relevant_memories": [asdict(memory) for memory in relevant_memories],
            "short_term_context": short_term_context,
            "personal_context": personal_context,
            "memory_stats": self.memory_stats
        }
    
    def _extract_concepts_from_query(self, query: str) -> List[str]:
        """Extract concepts from query text"""
        # Simple concept extraction - would use more sophisticated NLP
        words = query.lower().split()
        
        # Common concept words
        concept_indicators = [
            "work", "family", "friend", "health", "sleep", "exercise",
            "hobby", "music", "art", "reading", "cooking", "travel"
        ]
        
        concepts = []
        for word in words:
            if word in concept_indicators:
                concepts.append(word)
        
        return concepts
    
    def cleanup_old_memories(self, days_threshold: int = 365):
        """Clean up old, low-importance memories"""
        cutoff_time = time.time() - (days_threshold * 24 * 3600)
        
        if self.memory_collection and CHROMADB_AVAILABLE:
            try:
                # ChromaDB doesn't have built-in deletion by metadata
                # Would need to implement custom cleanup logic
                pass
            except Exception as e:
                print(f"Error cleaning up ChromaDB memories: {e}")
        else:
            # Clean up in-memory storage
            self.in_memory_storage = [
                memory for memory in self.in_memory_storage
                if memory["timestamp"] > cutoff_time or memory["importance"] > 0.7
            ]
    
    def export_memories(self) -> Dict[str, Any]:
        """Export all memories for user data portability"""
        if self.memory_collection and CHROMADB_AVAILABLE:
            try:
                # Get all memories from ChromaDB
                results = self.memory_collection.get(
                    where={"user_id": self.user_id}
                )
                
                memories = []
                for i in range(len(results["ids"])):
                    memory = {
                        "id": results["ids"][i],
                        "content": results["documents"][i],
                        "metadata": results["metadatas"][i]
                    }
                    memories.append(memory)
                
                return {
                    "user_id": self.user_id,
                    "memories": memories,
                    "statistics": self.memory_stats
                }
                
            except Exception as e:
                print(f"Error exporting ChromaDB memories: {e}")
                return {"user_id": self.user_id, "memories": [], "statistics": self.memory_stats}
        else:
            return {
                "user_id": self.user_id,
                "memories": self.in_memory_storage,
                "statistics": self.memory_stats
            }
    
    def delete_all_memories(self):
        """Delete all memories for user data deletion"""
        if self.memory_collection and CHROMADB_AVAILABLE:
            try:
                # Delete collection
                self.vector_db.delete_collection(f"user_{self.user_id}_memories")
                # Recreate empty collection
                self.memory_collection = self.vector_db.create_collection(
                    name=f"user_{self.user_id}_memories",
                    metadata={"user_id": self.user_id, "type": "emotional_memories"}
                )
            except Exception as e:
                print(f"Error deleting ChromaDB memories: {e}")
        
        # Clear in-memory storage
        self.in_memory_storage.clear()
        
        # Reset statistics
        self.memory_stats = {
            "total_memories": 0,
            "conversations": 0,
            "patterns_detected": 0,
            "last_access": time.time()
        } 