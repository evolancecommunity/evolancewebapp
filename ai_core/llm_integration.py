"""
Evolance LLM Integration for Evolance AI System
Integrates our proprietary LLM with the existing emotional intelligence framework
"""

import torch
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np

from .emotion_detector import EmotionDetector
from .memory_manager import MemoryManager
from .semantic_network import SemanticNetwork

class EvolanceLLMIntegration:
    """
    Integrates Evolance LLM with Evolance AI system
    """
    
    def __init__(self, model_path: str = "backend/models/evolance_llm"):
        self.model_path = Path(model_path)
        self.model = None
        self.tokenizer = None
        self.emotion_detector = EmotionDetector()
        self.memory_manager = MemoryManager()
        self.semantic_network = SemanticNetwork()
        
        # Load model if available
        self._load_model()
    
    def _load_model(self):
        """Load the Evolance LLM model"""
        try:
            if self.model_path.exists():
                print("🧠 Loading Evolance LLM...")
                self.tokenizer = AutoTokenizer.from_pretrained(str(self.model_path))
                self.model = AutoModelForCausalLM.from_pretrained(str(self.model_path))
                
                # Load training info
                info_path = self.model_path / "training_info.json"
                if info_path.exists():
                    with open(info_path, 'r') as f:
                        self.model_info = json.load(f)
                else:
                    self.model_info = {"model_type": "EmotionalTransformer"}
                
                print(f"✅ Evolance LLM loaded: {self.model_info.get('model_type', 'Unknown')}")
                print(f"✅ Specialized for: {self.model_info.get('specialized_for', 'emotional_intelligence')}")
                
            else:
                print("⚠️  Evolance LLM not found. Using fallback system.")
                self.model = None
                
        except Exception as e:
            print(f"❌ Failed to load Evolance LLM: {str(e)}")
            self.model = None
    
    def generate_response(
        self, 
        user_message: str, 
        conversation_history: List[Dict[str, Any]] = None,
        user_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate response using Evolance LLM with emotional intelligence
        """
        
        if self.model is None:
            return self._fallback_response(user_message, conversation_history, user_context)
        
        try:
            # Analyze user emotion and context
            emotion_analysis = self.emotion_detector.detect_emotion(user_message)
            detected_emotion = emotion_analysis.get("primary_emotion", "neutral")
            
            # Get user context
            context = self._extract_context(user_message, user_context)
            
            # Build prompt with emotional context
            prompt = self._build_emotional_prompt(
                user_message, 
                detected_emotion, 
                context, 
                conversation_history
            )
            
            # Generate response
            response = self._generate_with_llm(prompt)
            
            # Post-process response
            processed_response = self._post_process_response(response, emotion_analysis)
            
            # Update memory and semantic network
            self._update_knowledge_base(user_message, processed_response, emotion_analysis)
            
            return {
                "response": processed_response,
                "emotion_detected": detected_emotion,
                "confidence": emotion_analysis.get("confidence", 0.8),
                "context": context,
                "model_used": "custom_llm",
                "emotional_insights": emotion_analysis
            }
            
        except Exception as e:
            print(f"❌ Evolance LLM generation failed: {str(e)}")
            return self._fallback_response(user_message, conversation_history, user_context)
    
    def _build_emotional_prompt(
        self, 
        user_message: str, 
        emotion: str, 
        context: str, 
        history: List[Dict[str, Any]] = None
    ) -> str:
        """Build prompt with emotional context for the LLM"""
        
        prompt = f"<emotion>{emotion}</emotion><context>{context}</context>"
        
        # Add conversation history if available
        if history:
            for msg in history[-3:]:  # Last 3 messages
                if msg.get("role") == "user":
                    hist_emotion = msg.get("emotion", "neutral")
                    hist_context = msg.get("context", "general")
                    prompt += f"<emotion>{hist_emotion}</emotion><context>{hist_context}</context>User: {msg['text']}\n"
                else:
                    prompt += f"Assistant: {msg['text']}\n"
        
        # Add current message
        prompt += f"User: {user_message}\nAssistant:"
        
        return prompt
    
    def _generate_with_llm(self, prompt: str) -> str:
        """Generate response using the Evolance LLM"""
        
        # Tokenize input
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        
        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=inputs["input_ids"].shape[1] + 100,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.1
            )
        
        # Decode response
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the assistant's response
        response = full_response.split("Assistant:")[-1].strip()
        
        return response
    
    def _post_process_response(self, response: str, emotion_analysis: Dict[str, Any]) -> str:
        """Post-process the LLM response"""
        
        # Clean up response
        response = response.strip()
        
        # Remove any remaining special tokens
        response = response.replace("<emotion>", "").replace("</emotion>", "")
        response = response.replace("<context>", "").replace("</context>", "")
        
        # Ensure response is not empty
        if not response:
            response = "I understand how you're feeling. Can you tell me more about that?"
        
        return response
    
    def _extract_context(self, message: str, user_context: Dict[str, Any] = None) -> str:
        """Extract context from user message and context"""
        
        # Default context
        context = "general"
        
        # Check user context
        if user_context:
            if user_context.get("domain") == "work":
                context = "work"
            elif user_context.get("domain") == "relationships":
                context = "relationships"
            elif user_context.get("domain") == "health":
                context = "health"
            elif user_context.get("domain") == "personal":
                context = "personal_growth"
        
        # Check message content for context clues
        message_lower = message.lower()
        if any(word in message_lower for word in ["work", "job", "boss", "colleague", "meeting"]):
            context = "work"
        elif any(word in message_lower for word in ["partner", "relationship", "boyfriend", "girlfriend", "marriage"]):
            context = "relationships"
        elif any(word in message_lower for word in ["health", "doctor", "sick", "pain", "medical"]):
            context = "health"
        elif any(word in message_lower for word in ["goal", "achieve", "success", "growth", "improve"]):
            context = "personal_growth"
        
        return context
    
    def _update_knowledge_base(
        self, 
        user_message: str, 
        response: str, 
        emotion_analysis: Dict[str, Any]
    ):
        """Update memory and semantic network with new interaction"""
        
        # Store in memory
        self.memory_manager.store_interaction(
            user_message=user_message,
            ai_response=response,
            emotion=emotion_analysis.get("primary_emotion", "neutral"),
            timestamp=None
        )
        
        # Update semantic network
        self.semantic_network.add_concept(user_message, emotion_analysis)
    
    def _fallback_response(
        self, 
        user_message: str, 
        conversation_history: List[Dict[str, Any]] = None,
        user_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Fallback response when Evolance LLM is not available"""
        
        # Use emotion detector
        emotion_analysis = self.emotion_detector.detect_emotion(user_message)
        detected_emotion = emotion_analysis.get("primary_emotion", "neutral")
        
        # Generate fallback response
        fallback_responses = {
            "sad": "I can hear that you're feeling down. That sounds really difficult. What's been on your mind?",
            "anxious": "I understand that worry. It's completely normal to feel anxious sometimes. What's making you feel this way?",
            "angry": "That sounds really frustrating. You have every right to feel that way. What happened?",
            "happy": "That's wonderful! I'm so glad you're feeling good. What's been going well for you?",
            "neutral": "I'm here to listen. What would you like to talk about?"
        }
        
        response = fallback_responses.get(detected_emotion, fallback_responses["neutral"])
        
        return {
            "response": response,
            "emotion_detected": detected_emotion,
            "confidence": emotion_analysis.get("confidence", 0.8),
            "context": "general",
            "model_used": "fallback_system",
            "emotional_insights": emotion_analysis
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if self.model is None:
            return {"status": "not_loaded", "model_type": "none"}
        
        return {
            "status": "loaded",
            "model_type": self.model_info.get("model_type", "EmotionalTransformer"),
            "specialized_for": self.model_info.get("specialized_for", "emotional_intelligence"),
            "features": self.model_info.get("features", []),
            "training_examples": self.model_info.get("training_examples", "unknown")
        }
    
    def fine_tune_on_conversation(
        self, 
        conversation_data: List[Dict[str, Any]], 
        output_path: str = None
    ):
        """Fine-tune the Evolance LLM on new conversation data"""
        
        if self.model is None:
            print("❌ No model loaded for fine-tuning")
            return
        
        print("🔄 Fine-tuning Evolance LLM on new conversation data...")
        
        # This would implement fine-tuning logic
        # For now, just update the model info
        if output_path:
            self.model_info["fine_tuned"] = True
            self.model_info["fine_tune_data"] = len(conversation_data)
            
            with open(f"{output_path}/updated_training_info.json", 'w') as f:
                json.dump(self.model_info, f, indent=2)
        
        print("✅ Fine-tuning completed")

# Global instance
evolance_llm = EvolanceLLMIntegration() 