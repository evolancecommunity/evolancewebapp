#!/usr/bin/env python3
"""
Dynamic AI Demo
Shows how the AI can generate responses dynamically using NLP
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_dynamic_ai():
    """Demo the dynamic AI capabilities"""
    print("🧠 Dynamic AI System Demo")
    print("=" * 50)
    
    try:
        from ai_core.dynamic_ai import dynamic_ai
        
        print("✓ Dynamic AI loaded successfully")
        print("\nThis AI uses:")
        print("- Real NLP models for emotion detection")
        print("- Dynamic response generation")
        print("- Context awareness")
        print("- Conversation memory")
        print("- Intent recognition")
        
        # Test messages
        test_messages = [
            "I'm feeling really happy about my new job!",
            "I'm so anxious about my presentation tomorrow",
            "I'm really angry with my colleague",
            "I feel so sad and lonely today",
            "Hi there!",
            "I'm worried about my relationship"
        ]
        
        print("\n🔍 Testing Dynamic Response Generation:")
        print("-" * 40)
        
        for message in test_messages:
            print(f"\nUser: {message}")
            
            # Analyze message
            analysis = dynamic_ai.analyze_message(message)
            print(f"Analysis: {analysis['emotion']} (confidence: {analysis['confidence']:.2f})")
            print(f"Sentiment: {analysis['sentiment']}")
            print(f"Intent: {analysis['intent']}")
            print(f"Context: {analysis['context']}")
            
            # Generate response
            response = dynamic_ai.generate_response(message, analysis)
            print(f"AI: {response}")
            
            # Update conversation history
            dynamic_ai.update_conversation_history(message, analysis, response)
        
        # Show conversation summary
        summary = dynamic_ai.get_conversation_summary()
        print(f"\n📊 Conversation Summary:")
        print(f"Total messages: {summary['total_messages']}")
        print(f"Dominant emotion: {summary['dominant_emotion']}")
        print(f"Overall sentiment: {summary['overall_sentiment']}")
        print(f"Conversation flow: {summary['conversation_flow']}")
        
        print("\n🎉 Dynamic AI demo completed!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure you have installed the required dependencies:")
        print("pip install -r requirements_ai.txt")

def interactive_dynamic_demo():
    """Interactive demo of dynamic AI"""
    print("\n🎮 Interactive Dynamic AI Demo")
    print("Chat with the AI and see how it analyzes and responds dynamically.")
    print("Type 'quit' to exit, 'analysis' to see detailed analysis.")
    print("-" * 50)
    
    try:
        from ai_core.dynamic_ai import dynamic_ai
        
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if user_input.lower() == 'analysis':
                # Show detailed analysis of conversation
                summary = dynamic_ai.get_conversation_summary()
                print(f"\n📊 Conversation Analysis:")
                print(f"Total messages: {summary['total_messages']}")
                print(f"Emotion distribution: {summary['emotion_distribution']}")
                print(f"Overall sentiment: {summary['overall_sentiment']}")
                continue
            
            # Analyze message
            analysis = dynamic_ai.analyze_message(user_input)
            
            # Show analysis (optional)
            print(f"[Analysis: {analysis['emotion']} | {analysis['sentiment']} | {analysis['intent']}]")
            
            # Generate response
            response = dynamic_ai.generate_response(user_input, analysis)
            print(f"AI: {response}")
            
            # Update conversation history
            dynamic_ai.update_conversation_history(user_input, analysis, response)
    
    except KeyboardInterrupt:
        print("\n\nDemo ended.")
    except Exception as e:
        print(f"Error in interactive demo: {e}")

def main():
    """Main demo function"""
    print("Dynamic AI System Demo")
    print("Choose an option:")
    print("1. Automated demo (test multiple scenarios)")
    print("2. Interactive demo (chat with dynamic AI)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        demo_dynamic_ai()
    elif choice == "2":
        interactive_dynamic_demo()
    elif choice == "3":
        print("Goodbye! 👋")
    else:
        print("Invalid choice. Running automated demo...")
        demo_dynamic_ai()

if __name__ == "__main__":
    main() 