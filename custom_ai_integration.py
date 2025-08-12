#!/usr/bin/env python3
"""
Custom Spiritual AI Integration
Replaces OpenAI API with your trained spiritual AI model
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import os
from typing import Optional, Dict, Any
import logging

class CustomSpiritualAI:
    def __init__(self, model_path: str = "./spiritual_ai_model"):
        """Initialize the custom spiritual AI model"""
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.is_loaded = False
        
        # Load model if available
        if os.path.exists(model_path):
            self.load_model()
        else:
            logging.warning(f"Model not found at {model_path}. Using fallback responses.")
    
    def load_model(self):
        """Load the trained spiritual AI model"""
        try:
            print("🔄 Loading custom spiritual AI model...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.is_loaded = True
            print("✅ Custom spiritual AI model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.is_loaded = False
    
    def generate_response(self, message: str, user_context: Optional[Dict[str, Any]] = None, 
                         story_context: Optional[str] = None) -> str:
        """Generate a spiritual AI response"""
        
        if not self.is_loaded:
            return self._fallback_response(message, user_context)
        
        try:
            # Build context-aware input
            input_text = self._build_input_text(message, user_context, story_context)
            
            # Tokenize
            inputs = self.tokenizer.encode(input_text, return_tensors="pt", truncation=True, max_length=512)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 100,  # Generate up to 100 more tokens
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.2
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract assistant response
            if "assistant:" in response:
                response = response.split("assistant:")[-1].strip()
            
            # Clean up response
            response = self._clean_response(response)
            
            return response
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return self._fallback_response(message, user_context)
    
    def _build_input_text(self, message: str, user_context: Optional[Dict[str, Any]] = None, 
                         story_context: Optional[str] = None) -> str:
        """Build context-aware input text"""
        
        # Start with user message
        input_text = f"user: {message}\n"
        
        # Add user context if available
        if user_context:
            if user_context.get('personality_type'):
                input_text += f"context: user has {user_context['personality_type']} personality\n"
            if user_context.get('spiritual_level'):
                input_text += f"context: user's spiritual level is {user_context['spiritual_level']}\n"
            if user_context.get('current_emotion'):
                input_text += f"context: user is feeling {user_context['current_emotion']}\n"
        
        # Add story context if available
        if story_context:
            input_text += f"context: discussing {story_context}\n"
        
        # End with assistant prompt
        input_text += "assistant: "
        
        return input_text
    
    def _clean_response(self, response: str) -> str:
        """Clean and format the response"""
        # Remove any remaining user: prefixes
        if "user:" in response:
            response = response.split("user:")[0].strip()
        
        # Remove extra whitespace
        response = " ".join(response.split())
        
        # Ensure response ends properly
        if not response.endswith(('.', '!', '?')):
            response += "."
        
        return response
    
    def _fallback_response(self, message: str, user_context: Optional[Dict[str, Any]] = None) -> str:
        """Fallback responses when model is not available"""
        
        # Simple keyword-based responses
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['anxious', 'anxiety', 'worried', 'stress']):
            return "I understand you're feeling anxious. Let's take a moment to breathe together. Can you tell me more about what's causing this feeling? Remember, it's okay to feel this way."
        
        elif any(word in message_lower for word in ['peace', 'calm', 'inner peace']):
            return "Inner peace is a journey that begins with self-awareness. Let's explore some practices that might help you connect with your inner self. Meditation and mindfulness can be powerful tools."
        
        elif any(word in message_lower for word in ['negative', 'thoughts', 'thinking']):
            return "Negative thoughts are a common human experience. Let's work together to understand and transform these patterns. Remember, thoughts are not facts - they're just thoughts passing through."
        
        elif any(word in message_lower for word in ['mindfulness', 'meditation']):
            return "Mindfulness is about being present in the moment. Start with simple breathing exercises. Focus on your breath, notice when your mind wanders, and gently bring it back."
        
        elif any(word in message_lower for word in ['lost', 'direction', 'purpose']):
            return "Feeling lost is often a sign of growth and transformation. It's okay to not have all the answers right now. Let's explore what's important to you and what brings you meaning."
        
        else:
            return "I'm here to support you on your spiritual journey. Can you tell me more about what's on your mind? I'm listening with compassion and understanding."

# Integration with existing server
def replace_openai_integration():
    """Replace OpenAI integration with custom AI"""
    
    # Initialize custom AI
    custom_ai = CustomSpiritualAI()
    
    # Test the integration
    test_messages = [
        "I'm feeling anxious about my future",
        "How can I find inner peace?",
        "I'm struggling with negative thoughts",
        "How do I practice mindfulness?"
    ]
    
    print("🧪 Testing Custom Spiritual AI Integration")
    print("=" * 50)
    
    for message in test_messages:
        response = custom_ai.generate_response(message)
        print(f"\n👤 User: {message}")
        print(f"🤖 Custom AI: {response}")
        print("-" * 30)
    
    return custom_ai

if __name__ == "__main__":
    # Test the custom AI
    ai = replace_openai_integration()
    
    print("\n🎉 Custom Spiritual AI Integration Complete!")
    print("🚀 Ready to replace OpenAI in your server!") 