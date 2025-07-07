"""
RAG-Enhanced Evolance LLM
Uses ChromaDB for retrieval-augmented generation with private conversation data
"""

import json
from typing import Dict, List, Any, Optional
from .llm_integration import evolance_llm
from .private_chroma_db import private_chroma

class RAGEnhancedLLM:
    """
    RAG-enhanced Evolance LLM that uses ChromaDB for context retrieval
    """
    
    def __init__(self):
        self.llm = evolance_llm
        self.chroma = private_chroma
        
    def generate_enhanced_response(
        self, 
        user_message: str, 
        conversation_history: List[Dict[str, Any]] = None,
        user_context: Dict[str, Any] = None,
        user_id: str = "anonymous",
        use_rag: bool = True,
        max_context_examples: int = 3
    ) -> Dict[str, Any]:
        """
        Generate response with RAG enhancement
        
        Args:
            user_message: User's input message
            conversation_history: Previous conversation messages
            user_context: User-specific context
            user_id: User identifier for access control
            use_rag: Whether to use retrieval-augmented generation
            max_context_examples: Maximum number of similar examples to include
        """
        
        # Get base response from LLM
        base_response = self.llm.generate_response(
            user_message, 
            conversation_history, 
            user_context
        )
        
        if not use_rag:
            return base_response
        
        try:
            # Retrieve similar conversations from ChromaDB
            similar_examples = self.chroma.search_similar_conversations(
                user_message, 
                n_results=max_context_examples,
                user_id=user_id
            )
            
            # Get user-specific context
            user_context_data = self.chroma.get_user_context(user_id)
            
            # Enhance response with retrieved context
            enhanced_response = self._enhance_with_rag(
                base_response, 
                similar_examples, 
                user_context_data
            )
            
            # Store the new conversation
            self.chroma.store_conversation(
                user_message=user_message,
                ai_response=enhanced_response["response"],
                emotion=enhanced_response.get("emotion_detected", "neutral"),
                context=enhanced_response.get("context", "general"),
                user_id=user_id
            )
            
            # Update user context if new information is available
            if user_context:
                self.chroma.update_user_context(user_id, user_context)
            
            return enhanced_response
            
        except Exception as e:
            print(f"⚠️  RAG enhancement failed: {str(e)}, using base response")
            return base_response
    
    def _enhance_with_rag(
        self, 
        base_response: Dict[str, Any], 
        similar_examples: List[Dict[str, Any]], 
        user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enhance base response with retrieved context"""
        
        enhanced_response = base_response.copy()
        
        if similar_examples:
            # Add context from similar examples
            context_info = []
            for example in similar_examples:
                if example["type"] == "pattern" and example["metadata"]["type"] == "ai_response":
                    context_info.append({
                        "similar_response": example["text"],
                        "emotion": example["metadata"].get("emotion", "unknown"),
                        "context": example["metadata"].get("context", "general"),
                        "relevance": 1.0 - (example.get("distance", 0.0) or 0.0)
                    })
            
            if context_info:
                # Enhance the response based on similar patterns
                enhanced_response["rag_context"] = {
                    "similar_examples": context_info,
                    "enhancement_applied": True
                }
                
                # Optionally modify response based on similar examples
                best_example = max(context_info, key=lambda x: x["relevance"])
                if best_example["relevance"] > 0.7:  # High similarity threshold
                    enhanced_response["response"] = self._blend_responses(
                        base_response["response"], 
                        best_example["similar_response"]
                    )
        
        # Add user context if available
        if user_context:
            enhanced_response["user_context"] = user_context
        
        return enhanced_response
    
    def _blend_responses(self, base_response: str, similar_response: str) -> str:
        """Blend base response with similar response for better quality"""
        # Simple blending - in practice, you might use more sophisticated methods
        if len(similar_response) > len(base_response) * 1.5:
            # Similar response is much longer, might be more detailed
            return similar_response
        else:
            # Keep base response but ensure it's not too short
            if len(base_response) < 50:
                return similar_response
            return base_response
    
    def get_conversation_insights(self, user_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get insights about user's conversation patterns"""
        if not self.chroma.is_authorized_user(user_id):
            return {"error": "Unauthorized access"}
        
        try:
            # Get user's conversation history
            user_conversations = self.chroma.conversations.query(
                query_texts=["user conversations"],
                where={"user_id": user_id},
                n_results=limit
            )
            
            # Analyze patterns
            emotions = []
            contexts = []
            
            if user_conversations['metadatas']:
                for metadata in user_conversations['metadatas'][0]:
                    emotions.append(metadata.get("emotion", "neutral"))
                    contexts.append(metadata.get("context", "general"))
            
            # Calculate insights
            emotion_counts = {}
            context_counts = {}
            
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            for context in contexts:
                context_counts[context] = context_counts.get(context, 0) + 1
            
            return {
                "total_conversations": len(emotions),
                "emotion_distribution": emotion_counts,
                "context_distribution": context_counts,
                "most_common_emotion": max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else "neutral",
                "most_common_context": max(context_counts.items(), key=lambda x: x[1])[0] if context_counts else "general"
            }
            
        except Exception as e:
            print(f"❌ Failed to get conversation insights: {str(e)}")
            return {"error": str(e)}
    
    def search_emotional_patterns(self, emotion: str, context: str = None, 
                                user_id: str = "anonymous") -> List[Dict[str, Any]]:
        """Search for specific emotional patterns"""
        if not self.chroma.is_authorized_user(user_id):
            return []
        
        try:
            # Build query
            query = f"emotion: {emotion}"
            if context:
                query += f" context: {context}"
            
            results = self.chroma.emotional_patterns.query(
                query_texts=[query],
                n_results=10
            )
            
            patterns = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    patterns.append({
                        "response": doc,
                        "metadata": results['metadatas'][0][i],
                        "relevance": 1.0 - (results['distances'][0][i] if 'distances' in results else 0.0)
                    })
            
            return patterns
            
        except Exception as e:
            print(f"❌ Failed to search emotional patterns: {str(e)}")
            return []
    
    def get_database_health(self) -> Dict[str, Any]:
        """Get database health and statistics"""
        stats = self.chroma.get_database_stats()
        
        health_status = {
            "status": "healthy" if stats else "error",
            "statistics": stats,
            "collections": {
                "conversations": "active",
                "emotional_patterns": "active", 
                "user_contexts": "active"
            }
        }
        
        return health_status

# Global RAG-enhanced LLM instance
rag_enhanced_llm = RAGEnhancedLLM() 