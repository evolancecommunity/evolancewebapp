#!/usr/bin/env python3
"""
Test RAG-Enhanced Evolance LLM Integration
Demonstrates ChromaDB integration with retrieval-augmented generation
"""

import sys
import os
from pathlib import Path

# Add ai_core to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai_core'))

from ai_core.rag_enhanced_llm import rag_enhanced_llm
from ai_core.private_chroma_db import private_chroma
from ai_core.training_data_generator import generate_training_data

def setup_test_environment():
    """Setup test environment with data and authorized users"""
    print("🔧 Setting up RAG test environment...")
    
    # Generate training data if needed
    data_file = Path("backend/data/full_training_dataset.json")
    if not data_file.exists():
        print("📊 Generating training data...")
        generate_training_data()
    
    # Ingest data into ChromaDB
    print("🗄️  Ingesting data into ChromaDB...")
    private_chroma.ingest_generated_data()
    
    # Add test users
    test_users = ["test_user_1", "test_user_2", "demo_user"]
    for user in test_users:
        private_chroma.add_authorized_user(user)
    
    print("✅ Test environment setup complete")

def test_basic_rag():
    """Test basic RAG functionality"""
    print("\n🧪 Testing Basic RAG Functionality")
    print("-" * 40)
    
    test_cases = [
        {
            "user_id": "test_user_1",
            "message": "I'm feeling really anxious about my presentation tomorrow.",
            "expected_emotion": "anxious"
        },
        {
            "user_id": "test_user_2", 
            "message": "I had a fight with my partner and I feel so sad.",
            "expected_emotion": "sad"
        },
        {
            "user_id": "demo_user",
            "message": "I finally finished my big project! I'm so proud of myself.",
            "expected_emotion": "proud"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"User: {case['user_id']}")
        print(f"Message: {case['message']}")
        
        # Test with RAG enabled
        response_with_rag = rag_enhanced_llm.generate_enhanced_response(
            user_message=case['message'],
            user_id=case['user_id'],
            use_rag=True
        )
        
        print(f"Response (with RAG): {response_with_rag['response']}")
        print(f"Detected Emotion: {response_with_rag.get('emotion_detected', 'unknown')}")
        print(f"Model Used: {response_with_rag.get('model_used', 'unknown')}")
        
        # Check if RAG context was added
        if 'rag_context' in response_with_rag:
            rag_info = response_with_rag['rag_context']
            print(f"RAG Enhancement: {rag_info.get('enhancement_applied', False)}")
            print(f"Similar Examples Found: {len(rag_info.get('similar_examples', []))}")
        
        print("-" * 50)

def test_rag_vs_no_rag():
    """Compare responses with and without RAG"""
    print("\n⚖️  Comparing RAG vs No-RAG Responses")
    print("-" * 40)
    
    test_message = "I'm feeling overwhelmed with work and don't know how to handle it."
    user_id = "test_user_1"
    
    print(f"Test Message: {test_message}")
    print(f"User: {user_id}")
    
    # Test without RAG
    print("\n🤖 Response WITHOUT RAG:")
    response_no_rag = rag_enhanced_llm.generate_enhanced_response(
        user_message=test_message,
        user_id=user_id,
        use_rag=False
    )
    print(f"Response: {response_no_rag['response']}")
    print(f"Emotion: {response_no_rag.get('emotion_detected', 'unknown')}")
    
    # Test with RAG
    print("\n🧠 Response WITH RAG:")
    response_with_rag = rag_enhanced_llm.generate_enhanced_response(
        user_message=test_message,
        user_id=user_id,
        use_rag=True
    )
    print(f"Response: {response_with_rag['response']}")
    print(f"Emotion: {response_with_rag.get('emotion_detected', 'unknown')}")
    
    # Show RAG context
    if 'rag_context' in response_with_rag:
        rag_info = response_with_rag['rag_context']
        print(f"RAG Enhancement Applied: {rag_info.get('enhancement_applied', False)}")
        if 'similar_examples' in rag_info:
            print(f"Similar Examples Used: {len(rag_info['similar_examples'])}")
            for i, example in enumerate(rag_info['similar_examples'][:2], 1):
                print(f"  Example {i}: {example['similar_response'][:100]}...")

def test_conversation_insights():
    """Test conversation insights and analytics"""
    print("\n📊 Testing Conversation Insights")
    print("-" * 40)
    
    user_id = "test_user_1"
    
    # Generate some conversation data first
    test_messages = [
        "I'm anxious about my job interview",
        "I feel sad about my relationship",
        "I'm excited about my new project",
        "I'm worried about my health"
    ]
    
    print(f"Generating conversation data for user {user_id}...")
    for message in test_messages:
        rag_enhanced_llm.generate_enhanced_response(
            user_message=message,
            user_id=user_id,
            use_rag=True
        )
    
    # Get insights
    insights = rag_enhanced_llm.get_conversation_insights(user_id)
    
    print(f"\nInsights for user {user_id}:")
    print(f"Total Conversations: {insights.get('total_conversations', 0)}")
    print(f"Emotion Distribution: {insights.get('emotion_distribution', {})}")
    print(f"Context Distribution: {insights.get('context_distribution', {})}")
    print(f"Most Common Emotion: {insights.get('most_common_emotion', 'unknown')}")
    print(f"Most Common Context: {insights.get('most_common_context', 'unknown')}")

def test_emotional_pattern_search():
    """Test searching for specific emotional patterns"""
    print("\n🔍 Testing Emotional Pattern Search")
    print("-" * 40)
    
    user_id = "test_user_1"
    
    # Search for anxious patterns
    print("Searching for 'anxious' emotional patterns...")
    anxious_patterns = rag_enhanced_llm.search_emotional_patterns(
        emotion="anxious",
        user_id=user_id
    )
    
    print(f"Found {len(anxious_patterns)} anxious patterns:")
    for i, pattern in enumerate(anxious_patterns[:3], 1):
        print(f"  {i}. {pattern['response'][:100]}...")
        print(f"     Relevance: {pattern['relevance']:.2f}")
    
    # Search for sad patterns in work context
    print("\nSearching for 'sad' patterns in work context...")
    sad_work_patterns = rag_enhanced_llm.search_emotional_patterns(
        emotion="sad",
        context="work",
        user_id=user_id
    )
    
    print(f"Found {len(sad_work_patterns)} sad work patterns:")
    for i, pattern in enumerate(sad_work_patterns[:2], 1):
        print(f"  {i}. {pattern['response'][:100]}...")

def test_database_health():
    """Test database health and statistics"""
    print("\n🏥 Testing Database Health")
    print("-" * 40)
    
    health = rag_enhanced_llm.get_database_health()
    
    print(f"Status: {health.get('status', 'unknown')}")
    print(f"Statistics: {health.get('statistics', {})}")
    print(f"Collections: {health.get('collections', {})}")

def interactive_rag_demo():
    """Interactive demo of RAG-enhanced LLM"""
    print("\n💬 Interactive RAG Demo")
    print("-" * 20)
    print("Chat with the RAG-enhanced Evolance LLM!")
    print("Type 'quit' to exit, 'insights' to see your conversation insights.")
    print()
    
    user_id = "demo_user"
    conversation_history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Thanks for trying the RAG-enhanced LLM!")
                break
            
            if user_input.lower() == 'insights':
                insights = rag_enhanced_llm.get_conversation_insights(user_id)
                print(f"\n📊 Your Conversation Insights:")
                print(f"Total conversations: {insights.get('total_conversations', 0)}")
                print(f"Emotion distribution: {insights.get('emotion_distribution', {})}")
                continue
            
            if not user_input:
                continue
            
            # Generate RAG-enhanced response
            print("🤖 AI is thinking with RAG...")
            response = rag_enhanced_llm.generate_enhanced_response(
                user_message=user_input,
                conversation_history=conversation_history,
                user_id=user_id,
                use_rag=True
            )
            
            print(f"AI: {response['response']}")
            
            # Show RAG info if available
            if 'rag_context' in response:
                rag_info = response['rag_context']
                if rag_info.get('enhancement_applied', False):
                    print(f"   [RAG: Used {len(rag_info.get('similar_examples', []))} similar examples]")
            
            # Update conversation history
            conversation_history.append({
                "role": "user",
                "text": user_input
            })
            conversation_history.append({
                "role": "assistant", 
                "text": response['response']
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

def main():
    """Main test function"""
    print("🚀 RAG-Enhanced Evolance LLM Integration Test")
    print("=" * 50)
    
    # Setup environment
    setup_test_environment()
    
    # Run tests
    test_basic_rag()
    test_rag_vs_no_rag()
    test_conversation_insights()
    test_emotional_pattern_search()
    test_database_health()
    
    # Interactive demo
    print("\n" + "=" * 50)
    interactive_rag_demo()
    
    print("\n✅ RAG integration test completed!")

if __name__ == "__main__":
    main() 