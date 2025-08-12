"""
Private ChromaDB Integration for Evolance LLM
Secure, local storage for conversational data with access control
"""

import chromadb
import json
import hashlib
import time
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np

class PrivateChromaDB:
    """
    Secure ChromaDB integration for Evolance LLM
    Stores conversational data locally with access control
    """
    
    def __init__(self, db_path: str = "./private_chroma_db", embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize private ChromaDB
        
        Args:
            db_path: Local path to store ChromaDB data
            embedding_model: Sentence transformer model for embeddings
        """
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client (local only)
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        
        # Load embedding model
        try:
            self.embedding_model = SentenceTransformer(embedding_model)
            print(f"✅ Loaded embedding model: {embedding_model}")
        except Exception as e:
            print(f"⚠️  Could not load {embedding_model}, using default")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize collections
        self._init_collections()
        
        # Access control (simple hash-based for demo)
        self.authorized_users = set()
        self._load_authorized_users()
    
    def _init_collections(self):
        """Initialize ChromaDB collections"""
        try:
            # Main conversations collection
            self.conversations = self.client.get_or_create_collection(
                name="evolance_conversations",
                metadata={"description": "Private conversation storage for Evolance LLM"}
            )
            
            # Emotional patterns collection
            self.emotional_patterns = self.client.get_or_create_collection(
                name="emotional_patterns",
                metadata={"description": "Emotional response patterns and examples"}
            )
            
            # User context collection
            self.user_contexts = self.client.get_or_create_collection(
                name="user_contexts",
                metadata={"description": "User-specific context and preferences"}
            )
            
            print("✅ ChromaDB collections initialized")
            
        except Exception as e:
            print(f"❌ Failed to initialize ChromaDB collections: {str(e)}")
            raise
    
    def _load_authorized_users(self):
        """Load authorized users from secure file"""
        auth_file = self.db_path / "authorized_users.json"
        if auth_file.exists():
            try:
                with open(auth_file, 'r') as f:
                    self.authorized_users = set(json.load(f))
                print(f"✅ Loaded {len(self.authorized_users)} authorized users")
            except Exception as e:
                print(f"⚠️  Could not load authorized users: {str(e)}")
                self.authorized_users = set()
        else:
            print("ℹ️  No authorized users file found, starting fresh")
    
    def _save_authorized_users(self):
        """Save authorized users to secure file"""
        auth_file = self.db_path / "authorized_users.json"
        try:
            with open(auth_file, 'w') as f:
                json.dump(list(self.authorized_users), f)
        except Exception as e:
            print(f"⚠️  Could not save authorized users: {str(e)}")
    
    def add_authorized_user(self, user_id: str):
        """Add a user to the authorized list"""
        user_hash = self._hash_user_id(user_id)
        self.authorized_users.add(user_hash)
        self._save_authorized_users()
        print(f"✅ Added user {user_id} to authorized list")
    
    def remove_authorized_user(self, user_id: str):
        """Remove a user from the authorized list"""
        user_hash = self._hash_user_id(user_id)
        if user_hash in self.authorized_users:
            self.authorized_users.remove(user_hash)
            self._save_authorized_users()
            print(f"✅ Removed user {user_id} from authorized list")
    
    def _hash_user_id(self, user_id: str) -> str:
        """Hash user ID for secure storage"""
        return hashlib.sha256(user_id.encode()).hexdigest()
    
    def is_authorized_user(self, user_id: str) -> bool:
        """Check if user is authorized"""
        user_hash = self._hash_user_id(user_id)
        return user_hash in self.authorized_users
    
    def ingest_generated_data(self, data_file: str = "backend/data/full_training_dataset.json"):
        """Ingest generated training data into ChromaDB"""
        print("🔄 Ingesting generated data into ChromaDB...")
        
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            conversation_docs = []
            conversation_metadatas = []
            conversation_ids = []
            
            emotional_docs = []
            emotional_metadatas = []
            emotional_ids = []
            
            for i, item in enumerate(data):
                if "messages" in item:
                    # Process conversation
                    for j, message in enumerate(item["messages"]):
                        if message["role"] == "user":
                            doc_id = f"conv_{i}_{j}"
                            conversation_docs.append(message["text"])
                            conversation_metadatas.append({
                                "type": "user_message",
                                "emotion": message.get("emotion", "neutral"),
                                "context": message.get("context", "general"),
                                "scenario": item.get("scenario", "unknown"),
                                "timestamp": time.time()
                            })
                            conversation_ids.append(doc_id)
                        else:
                            # AI response
                            doc_id = f"resp_{i}_{j}"
                            emotional_docs.append(message["text"])
                            emotional_metadatas.append({
                                "type": "ai_response",
                                "emotion": message.get("emotion", "empathetic"),
                                "context": message.get("context", "supportive"),
                                "scenario": item.get("scenario", "unknown"),
                                "timestamp": time.time()
                            })
                            emotional_ids.append(doc_id)
            
            # Add to collections
            if conversation_docs:
                self.conversations.add(
                    documents=conversation_docs,
                    metadatas=conversation_metadatas,
                    ids=conversation_ids
                )
                print(f"✅ Added {len(conversation_docs)} conversation documents")
            
            if emotional_docs:
                self.emotional_patterns.add(
                    documents=emotional_docs,
                    metadatas=emotional_metadatas,
                    ids=emotional_ids
                )
                print(f"✅ Added {len(emotional_docs)} emotional pattern documents")
            
            print("✅ Data ingestion completed")
            
        except Exception as e:
            print(f"❌ Failed to ingest data: {str(e)}")
            raise
    
    def store_conversation(self, user_message: str, ai_response: str, emotion: str, 
                          context: str, user_id: str = "anonymous"):
        """Store a new conversation securely"""
        if not self.is_authorized_user(user_id):
            print(f"⚠️  Unauthorized user {user_id} attempted to store conversation")
            return False
        
        try:
            timestamp = time.time()
            
            # Store user message
            user_doc_id = f"user_{user_id}_{timestamp}"
            self.conversations.add(
                documents=[user_message],
                metadatas=[{
                    "type": "user_message",
                    "emotion": emotion,
                    "context": context,
                    "user_id": user_id,
                    "timestamp": timestamp
                }],
                ids=[user_doc_id]
            )
            
            # Store AI response
            ai_doc_id = f"ai_{user_id}_{timestamp}"
            self.emotional_patterns.add(
                documents=[ai_response],
                metadatas=[{
                    "type": "ai_response",
                    "emotion": emotion,
                    "context": context,
                    "user_id": user_id,
                    "timestamp": timestamp
                }],
                ids=[ai_doc_id]
            )
            
            print(f"✅ Stored conversation for user {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to store conversation: {str(e)}")
            return False
    
    def search_similar_conversations(self, query: str, n_results: int = 5, 
                                   user_id: str = "anonymous") -> List[Dict[str, Any]]:
        """Search for similar conversations"""
        if not self.is_authorized_user(user_id):
            print(f"⚠️  Unauthorized user {user_id} attempted to search")
            return []
        
        try:
            # Search conversations
            conv_results = self.conversations.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Search emotional patterns
            pattern_results = self.emotional_patterns.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Combine and format results
            results = []
            
            if conv_results['documents']:
                for i, doc in enumerate(conv_results['documents'][0]):
                    results.append({
                        "text": doc,
                        "metadata": conv_results['metadatas'][0][i],
                        "type": "conversation",
                        "distance": conv_results['distances'][0][i] if 'distances' in conv_results else None
                    })
            
            if pattern_results['documents']:
                for i, doc in enumerate(pattern_results['documents'][0]):
                    results.append({
                        "text": doc,
                        "metadata": pattern_results['metadatas'][0][i],
                        "type": "pattern",
                        "distance": pattern_results['distances'][0][i] if 'distances' in pattern_results else None
                    })
            
            # Sort by relevance (distance)
            results.sort(key=lambda x: x.get('distance', float('inf')))
            
            return results[:n_results]
            
        except Exception as e:
            print(f"❌ Failed to search conversations: {str(e)}")
            return []
    
    def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """Get user-specific context and preferences"""
        if not self.is_authorized_user(user_id):
            return {}
        
        try:
            results = self.user_contexts.query(
                query_texts=[user_id],
                n_results=10
            )
            
            if results['documents']:
                # Combine user context from multiple entries
                context = {}
                for metadata in results['metadatas'][0]:
                    context.update(metadata)
                
                return context
            
            return {}
            
        except Exception as e:
            print(f"❌ Failed to get user context: {str(e)}")
            return {}
    
    def update_user_context(self, user_id: str, context_data: Dict[str, Any]):
        """Update user-specific context"""
        if not self.is_authorized_user(user_id):
            return False
        
        try:
            timestamp = time.time()
            doc_id = f"context_{user_id}_{timestamp}"
            
            self.user_contexts.add(
                documents=[f"User context for {user_id}"],
                metadatas=[{
                    "user_id": user_id,
                    "timestamp": timestamp,
                    **context_data
                }],
                ids=[doc_id]
            )
            
            print(f"✅ Updated context for user {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update user context: {str(e)}")
            return False
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            conv_count = self.conversations.count()
            pattern_count = self.emotional_patterns.count()
            context_count = self.user_contexts.count()
            
            return {
                "conversations": conv_count,
                "emotional_patterns": pattern_count,
                "user_contexts": context_count,
                "total_documents": conv_count + pattern_count + context_count,
                "authorized_users": len(self.authorized_users)
            }
            
        except Exception as e:
            print(f"❌ Failed to get database stats: {str(e)}")
            return {}
    
    def backup_database(self, backup_path: str = None):
        """Create a backup of the database"""
        if backup_path is None:
            backup_path = f"./chroma_backup_{int(time.time())}"
        
        try:
            # ChromaDB automatically handles persistence
            # Just copy the directory
            import shutil
            shutil.copytree(self.db_path, backup_path)
            print(f"✅ Database backed up to {backup_path}")
            
        except Exception as e:
            print(f"❌ Failed to backup database: {str(e)}")

# Global instance
private_chroma = PrivateChromaDB() 