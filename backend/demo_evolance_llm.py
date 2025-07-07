#!/usr/bin/env python3
"""
Demo Evolance LLM
Showcases our proprietary emotional intelligence language model
"""

import sys
import os
from pathlib import Path

# Add the ai_core module to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai_core'))

from llm_integration import evolance_llm

def print_banner():
    """Print demo banner"""
    print("=" * 60)
    print("🧠 EVOLANCE LLM DEMO")
    print("   Proprietary Emotional Intelligence Language Model")
    print("=" * 60)

def print_model_info():
    """Display model information"""
    print("\n📊 MODEL INFORMATION:")
    print("-" * 30)
    
    info = evolance_llm.get_model_info()
    
    print(f"Status: {info['status']}")
    print(f"Model Type: {info['model_type']}")
    print(f"Specialized For: {info['specialized_for']}")
    
    if info['status'] == 'loaded':
        print(f"Features: {', '.join(info.get('features', []))}")
        print(f"Training Examples: {info.get('training_examples', 'unknown')}")
    else:
        print("⚠️  Using fallback system (Evolance LLM not trained yet)")

def interactive_demo():
    """Interactive demo of the custom LLM"""
    print("\n💬 INTERACTIVE DEMO")
    print("-" * 20)
    print("Chat with our Evolance LLM! Type 'quit' to exit.")
    print("The AI will respond with emotional intelligence and understanding.")
    print()
    
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Thanks for trying our Evolance LLM! Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Generate response
            print("🤖 AI is thinking...")
            response_data = evolance_llm.generate_response(
                user_input, 
                conversation_history=conversation_history
            )
            
            # Display response
            print(f"AI: {response_data['response']}")
            
            # Show emotional analysis (optional)
            if response_data.get('model_used') == 'evolance_llm':
                emotion = response_data.get('emotion_detected', 'unknown')
                confidence = response_data.get('confidence', 0.0)
                print(f"   [Detected emotion: {emotion} (confidence: {confidence:.2f})]")
            
            # Update conversation history
            conversation_history.append({
                "role": "user",
                "text": user_input,
                "emotion": response_data.get('emotion_detected', 'neutral'),
                "context": response_data.get('context', 'general')
            })
            
            conversation_history.append({
                "role": "assistant",
                "text": response_data['response']
            })
            
            # Keep only last 6 messages
            if len(conversation_history) > 6:
                conversation_history = conversation_history[-6:]
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Let's continue...\n")

def test_scenarios():
    """Test specific emotional scenarios"""
    print("\n🧪 TESTING EMOTIONAL SCENARIOS")
    print("-" * 35)
    
    test_cases = [
        {
            "scenario": "Work Stress",
            "message": "I'm completely overwhelmed with my workload. My boss keeps adding more tasks and I can't keep up.",
            "expected_emotion": "stressed"
        },
        {
            "scenario": "Relationship Issues", 
            "message": "My partner and I had a huge fight last night. I feel like we're growing apart and I don't know what to do.",
            "expected_emotion": "sad"
        },
        {
            "scenario": "Personal Achievement",
            "message": "I finally finished that project I've been working on for months! I'm so proud of myself and excited about what's next.",
            "expected_emotion": "happy"
        },
        {
            "scenario": "Health Concerns",
            "message": "I've been feeling really tired lately and I'm worried something might be wrong. I'm scared to go to the doctor.",
            "expected_emotion": "anxious"
        },
        {
            "scenario": "Loneliness",
            "message": "I feel so alone lately. Everyone seems to have their own lives and I'm just here by myself.",
            "expected_emotion": "lonely"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['scenario']}")
        print(f"   Message: {test_case['message']}")
        print(f"   Expected Emotion: {test_case['expected_emotion']}")
        
        # Generate response
        response_data = evolance_llm.generate_response(test_case['message'])
        
        print(f"   AI Response: {response_data['response']}")
        print(f"   Detected Emotion: {response_data.get('emotion_detected', 'unknown')}")
        print(f"   Model Used: {response_data.get('model_used', 'unknown')}")
        
        # Check if emotion detection was correct
        detected = response_data.get('emotion_detected', 'unknown')
        expected = test_case['expected_emotion']
        
        if detected == expected:
            print("   ✅ Emotion detection: CORRECT")
        else:
            print(f"   ⚠️  Emotion detection: {detected} (expected: {expected})")
        
        print("-" * 50)

def compare_models():
    """Compare Evolance LLM with fallback system"""
    print("\n⚖️  MODEL COMPARISON")
    print("-" * 20)
    
    test_message = "I'm feeling really anxious about my presentation tomorrow. I keep thinking about all the things that could go wrong."
    
    print(f"Test Message: {test_message}")
    print()
    
    # Test with Evolance LLM
    print("🤖 Evolance LLM Response:")
    response_data = evolance_llm.generate_response(test_message)
    print(f"   Response: {response_data['response']}")
    print(f"   Emotion: {response_data.get('emotion_detected', 'unknown')}")
    print(f"   Model: {response_data.get('model_used', 'unknown')}")
    print()
    
    # Test fallback (if Evolance LLM is loaded, this will be the same)
    print("🔄 Fallback System Response:")
    fallback_data = evolance_llm._fallback_response(test_message)
    print(f"   Response: {fallback_data['response']}")
    print(f"   Emotion: {fallback_data.get('emotion_detected', 'unknown')}")
    print(f"   Model: {fallback_data.get('model_used', 'unknown')}")

def main():
    """Main demo function"""
    print_banner()
    
    # Show model info
    print_model_info()
    
    # Menu
    while True:
        print("\n🎯 DEMO OPTIONS:")
        print("1. Interactive Chat Demo")
        print("2. Test Emotional Scenarios") 
        print("3. Compare Models")
        print("4. Exit")
        
        try:
            choice = input("\nSelect an option (1-4): ").strip()
            
            if choice == "1":
                interactive_demo()
            elif choice == "2":
                test_scenarios()
            elif choice == "3":
                compare_models()
            elif choice == "4":
                print("\n👋 Thanks for exploring our Evolance LLM! Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 