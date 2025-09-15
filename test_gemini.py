#!/usr/bin/env python3
"""
Test script for Gemini integration
"""

import os
import sys
sys.path.append('.')

from ai_core.gemini_integration import GeminiEmotionAnalyzer, GeminiCoreAI

def test_gemini_integration():
    """Test Gemini integration with mock API key"""
    
    # Mock API key for testing
    mock_api_key = "test-api-key"
    
    try:
        # Test emotion analyzer
        print("Testing GeminiEmotionAnalyzer...")
        analyzer = GeminiEmotionAnalyzer(mock_api_key)
        
        # Test emotion analysis
        test_message = "I'm feeling really anxious about my upcoming presentation tomorrow"
        emotion_data = analyzer.analyze_conversation_emotion(test_message)
        print(f"Emotion analysis result: {emotion_data}")
        
        # Test response generation
        response = analyzer.generate_emotional_response(test_message, emotion_data)
        print(f"Generated response: {response}")
        
        # Test core AI
        print("\nTesting GeminiCoreAI...")
        core_ai = GeminiCoreAI(mock_api_key)
        
        # Test emolytics update
        user_id = "test-user-123"
        conversation_context = [{"user_message": test_message, "timestamp": "2024-01-01T00:00:00"}]
        emolytics_update = core_ai.update_emolytics(user_id, emotion_data, conversation_context)
        print(f"Emolytics update: {emolytics_update}")
        
        print("\n✅ Gemini integration test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing Gemini integration: {e}")
        print("This is expected if no valid API key is provided")

if __name__ == "__main__":
    test_gemini_integration() 