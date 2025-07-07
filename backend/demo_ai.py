#!/usr/bin/env python3
"""
Evolance AI Quick Demo
Simple demonstration of the AI system capabilities
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def quick_demo():
    """Quick demonstration of the AI system"""
    print("🧠 Evolance AI Quick Demo")
    print("=" * 40)
    
    try:
        # Import AI components
        from ai_core.emotion_detector import emotion_detector
        from ai_core.semantic_network import core_network
        from ai_core.ai_engine import ai_engine
        
        print("✓ AI components loaded successfully")
        
        # Demo 1: Emotion Detection
        print("\n🔍 Demo 1: Emotion Detection")
        test_messages = [
            "I'm feeling really happy today!",
            "I'm so anxious about my presentation",
            "I'm absolutely furious with my boss"
        ]
        
        for message in test_messages:
            result = emotion_detector.detect_emotions(message)
            print(f"  '{message}'")
            print(f"    → Emotion: {result.primary_emotion}")
            print(f"    → Confidence: {result.confidence:.2f}")
            print(f"    → Intensity: {result.intensity:.2f}")
            print(f"    → Body sensations: {result.body_sensations}")
            print()
        
        # Demo 2: Semantic Network
        print("🧠 Demo 2: Semantic Network")
        emotion = "fear"
        fear_info = core_network.get_emotion_info(emotion)
        coping_strategies = core_network.get_coping_strategies(emotion)
        body_regions = core_network.get_body_mapping(emotion)
        
        print(f"  Emotion: {fear_info.name}")
        print(f"  Valence: {fear_info.valence:.2f} (negative)")
        print(f"  Arousal: {fear_info.arousal:.2f} (high)")
        print(f"  Coping strategies: {coping_strategies}")
        print(f"  Body regions: {body_regions}")
        print()
        
        # Demo 3: AI Engine (Full Response)
        print("🤖 Demo 3: Full AI Response")
        user_message = "I'm feeling overwhelmed with work and my relationship is suffering"
        
        print(f"  User: {user_message}")
        response = await ai_engine.process_message("demo_user", user_message)
        
        print(f"  AI detected: {response.emotion_detected} (confidence: {response.confidence:.2f})")
        print(f"  AI response: {response.response_text}")
        print(f"  Coping suggestions: {response.coping_suggestions}")
        print(f"  Response time: {response.response_time:.2f}s")
        
        print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure you have installed the required dependencies:")
        print("pip install -r requirements_ai.txt")

def interactive_demo():
    """Interactive demo mode"""
    print("\n🎮 Interactive Demo Mode")
    print("Chat with the AI system. Type 'quit' to exit.")
    print("-" * 40)
    
    try:
        from ai_core.ai_engine import ai_engine
        from ai_core.emotion_detector import emotion_detector
        
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Thanks for trying Evolance AI! 👋")
                break
            
            # Quick emotion detection (but don't always show it)
            emotion_result = emotion_detector.detect_emotions(user_input)
            
            # Only show emotion detection for strong emotions or when debugging
            if emotion_result.confidence > 0.8 and emotion_result.primary_emotion != "neutral":
                print(f"AI detected: {emotion_result.primary_emotion} (confidence: {emotion_result.confidence:.2f})")
            
            # Full AI response (async)
            async def get_response():
                return await ai_engine.process_message("demo_user", user_input)
            
            response = asyncio.run(get_response())
            print(f"AI: {response.response_text}")
            
            # Only show coping suggestions occasionally, not every time
            if emotion_result.confidence > 0.7 and emotion_result.primary_emotion in ["sadness", "fear", "anger"]:
                print(f"💡 Maybe try: {', '.join(response.coping_suggestions[:1])}")
    
    except KeyboardInterrupt:
        print("\n\nDemo ended.")
    except Exception as e:
        print(f"Error in interactive demo: {e}")

def main():
    """Main demo function"""
    print("Welcome to Evolance AI Demo!")
    print("Choose an option:")
    print("1. Quick demo (automated)")
    print("2. Interactive demo (chat)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        asyncio.run(quick_demo())
    elif choice == "2":
        interactive_demo()
    elif choice == "3":
        print("Goodbye! 👋")
    else:
        print("Invalid choice. Running quick demo...")
        asyncio.run(quick_demo())

if __name__ == "__main__":
    main() 