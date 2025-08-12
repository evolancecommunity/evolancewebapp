#!/usr/bin/env python3
"""
Test script for Progressive Learning System
Demonstrates how the system learns from Gemini interactions and gradually becomes independent.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_core.progressive_learning import ProgressiveLearningSystem
from ai_core.gemini_integration import GeminiEmotionAnalyzer, GeminiCoreAI
import time

def test_progressive_learning():
    """Test the progressive learning system with simulated conversations."""
    
    print("🚀 Testing Progressive Learning System")
    print("=" * 50)
    
    # Initialize systems
    progressive_learning = ProgressiveLearningSystem()
    # Note: We're simulating Gemini responses, so we don't need actual API keys
    # gemini_emotion_analyzer = GeminiEmotionAnalyzer()
    # gemini_core_ai = GeminiCoreAI()
    
    # Simulated conversation data
    test_conversations = [
        {
            "user_message": "I'm feeling really anxious about my upcoming presentation",
            "expected_emotion": "anxiety"
        },
        {
            "user_message": "I'm so happy that I got the promotion!",
            "expected_emotion": "joy"
        },
        {
            "user_message": "I'm frustrated with my colleague's behavior",
            "expected_emotion": "frustration"
        },
        {
            "user_message": "I feel sad and lonely today",
            "expected_emotion": "sadness"
        },
        {
            "user_message": "I'm excited about the new project",
            "expected_emotion": "excitement"
        }
    ]
    
    print(f"📊 Initial Learning Status:")
    initial_status = progressive_learning.get_learning_status()
    print(f"   - Total interactions: {initial_status['total_interactions']}")
    print(f"   - Model confidence: {initial_status['model_confidence']:.3f}")
    print(f"   - Independence threshold: {initial_status['independence_threshold']}")
    print(f"   - Should use own model: {initial_status['should_use_own_model']}")
    print()
    
    # Simulate conversations and learning
    for i, conv in enumerate(test_conversations, 1):
        print(f"💬 Conversation {i}: {conv['user_message']}")
        print(f"   Expected emotion: {conv['expected_emotion']}")
        
        # Simulate Gemini analysis (in real scenario, this would be actual Gemini API calls)
        simulated_emotion_data = {
            "primary_emotion": conv['expected_emotion'],
            "emotion_intensity": 75,
            "secondary_emotions": ["concern", "hope"],
            "emotional_triggers": ["work", "relationships"],
            "reasoning": f"User expresses {conv['expected_emotion']} through their message"
        }
        
        # Simulate Gemini response
        simulated_response = f"I understand you're feeling {conv['expected_emotion']}. Let's explore this together."
        
        # Simulate emolytics update
        simulated_emolytics = {
            "emotional_state": {
                "current_emotion": conv['expected_emotion'],
                "intensity": 75,
                "stability": 60,
                "mood_trend": "variable"
            },
            "recommendations": {
                "immediate_actions": ["Take deep breaths", "Practice mindfulness"],
                "long_term_strategies": ["Regular exercise", "Therapy sessions"],
                "wellness_practices": ["Meditation", "Journaling"]
            },
            "analytics_metrics": {
                "emotional_variability": 65,
                "response_time_to_triggers": "medium",
                "emotional_awareness_score": 70,
                "wellness_progress": 60
            }
        }
        
        # Collect training data
        progressive_learning.collect_training_data(
            conv['user_message'],
            simulated_emotion_data,
            simulated_response,
            simulated_emolytics
        )
        
        print(f"   ✅ Training data collected")
        print()
        
        # Show progress every few interactions
        if i % 2 == 0:
            status = progressive_learning.get_learning_status()
            print(f"📈 Progress Update:")
            print(f"   - Interactions: {status['total_interactions']}")
            print(f"   - Training data: {status['training_data_size']}")
            print()
    
    # Test model training
    print("🎯 Training Models...")
    training_results = progressive_learning.train_models()
    print(f"   Training results: {training_results}")
    print()
    
    # Test trained model predictions
    print("🧪 Testing Trained Model...")
    test_messages = [
        "I'm feeling overwhelmed with work",
        "I'm grateful for my friends",
        "I'm angry about the situation"
    ]
    
    for msg in test_messages:
        prediction = progressive_learning.predict_emotion(msg)
        response = progressive_learning.generate_response(msg, prediction)
        emolytics = progressive_learning.analyze_emolytics(prediction, [])
        
        print(f"   Message: {msg}")
        print(f"   Predicted emotion: {prediction['primary_emotion']} (confidence: {prediction['confidence']:.3f})")
        print(f"   Generated response: {response[:50]}...")
        print(f"   Emolytics model: {emolytics['model_used']}")
        print()
    
    # Final status
    print("📊 Final Learning Status:")
    final_status = progressive_learning.get_learning_status()
    print(f"   - Total interactions: {final_status['total_interactions']}")
    print(f"   - Model confidence: {final_status['model_confidence']:.3f}")
    print(f"   - Should use own model: {final_status['should_use_own_model']}")
    print(f"   - Independence achieved: {progressive_learning.should_use_own_model()}")
    
    if progressive_learning.should_use_own_model():
        print("🎉 SUCCESS: System has achieved independence from Gemini!")
    else:
        print("📚 System is still learning. More interactions needed for independence.")
    
    print("\n" + "=" * 50)
    print("✅ Progressive Learning Test Completed!")

def test_learning_progression():
    """Test the gradual learning progression."""
    
    print("\n🔄 Testing Learning Progression")
    print("=" * 50)
    
    progressive_learning = ProgressiveLearningSystem()
    
    # Simulate gradual learning with more diverse data
    learning_scenarios = [
        # Phase 1: Basic emotions
        {"message": "I'm happy", "emotion": "joy", "count": 20},
        {"message": "I'm sad", "emotion": "sadness", "count": 20},
        {"message": "I'm angry", "emotion": "anger", "count": 20},
        
        # Phase 2: Complex emotions
        {"message": "I'm anxious about the future", "emotion": "anxiety", "count": 15},
        {"message": "I'm grateful for my life", "emotion": "gratitude", "count": 15},
        {"message": "I'm frustrated with myself", "emotion": "frustration", "count": 15},
        
        # Phase 3: Mixed emotions
        {"message": "I'm excited but nervous", "emotion": "excitement", "count": 10},
        {"message": "I'm relieved but worried", "emotion": "relief", "count": 10},
    ]
    
    total_interactions = 0
    
    for scenario in learning_scenarios:
        print(f"📚 Learning phase: {scenario['emotion']} ({scenario['count']} examples)")
        
        for i in range(scenario['count']):
            # Simulate training data
            emotion_data = {
                "primary_emotion": scenario['emotion'],
                "emotion_intensity": 70 + (i % 30),
                "secondary_emotions": ["concern"],
                "emotional_triggers": ["life events"],
                "reasoning": f"User expresses {scenario['emotion']}"
            }
            
            response = f"I understand your {scenario['emotion']}. Let's work through this."
            
            emolytics = {
                "emotional_state": {"current_emotion": scenario['emotion'], "intensity": 70, "stability": 60},
                "recommendations": {"immediate_actions": ["Breathe deeply"]},
                "analytics_metrics": {"emotional_variability": 60, "wellness_progress": 60}
            }
            
            progressive_learning.collect_training_data(
                scenario['message'], emotion_data, response, emolytics
            )
            
            total_interactions += 1
            
            # Check if we should train
            if total_interactions % 50 == 0:
                print(f"   🎯 Training at {total_interactions} interactions...")
                progressive_learning.train_models()
                
                status = progressive_learning.get_learning_status()
                print(f"   📊 Confidence: {status['model_confidence']:.3f}")
                print(f"   🎯 Independence: {status['should_use_own_model']}")
        
        print(f"   ✅ Completed {scenario['count']} examples")
        print()
    
    # Final test with trained model
    print("🧪 Final Model Test:")
    test_message = "I'm feeling a mix of emotions today"
    prediction = progressive_learning.predict_emotion(test_message)
    response = progressive_learning.generate_response(test_message, prediction)
    
    print(f"   Test message: {test_message}")
    print(f"   Prediction: {prediction}")
    print(f"   Response: {response}")
    print(f"   Model used: {prediction.get('model_used', 'unknown')}")
    
    print("\n" + "=" * 50)
    print("✅ Learning Progression Test Completed!")

if __name__ == "__main__":
    print("🧠 Progressive Learning System Test Suite")
    print("This demonstrates how the system learns from Gemini and becomes independent.")
    print()
    
    try:
        test_progressive_learning()
        test_learning_progression()
        
        print("\n🎯 Key Benefits of Progressive Learning:")
        print("1. 🎓 Learns from Gemini's high-quality responses")
        print("2. 📈 Gradually improves accuracy over time")
        print("3. 🚀 Becomes independent when confidence threshold is met")
        print("4. 💰 Reduces dependency on external API costs")
        print("5. 🔒 Maintains privacy by using local models")
        print("6. ⚡ Faster response times with local inference")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc() 