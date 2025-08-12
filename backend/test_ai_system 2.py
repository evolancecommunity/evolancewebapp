#!/usr/bin/env python3
"""
Evolance AI System Testing Script
Interactive testing for all AI components
"""

import asyncio
import time
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_core_components():
    """Test core AI components"""
    print("🧠 Testing Core AI Components...")
    
    try:
        # Test configuration
        from ai_core.config import config
        print("✓ Configuration loaded successfully")
        print(f"  - Model size: {config.model.model_size}")
        print(f"  - Max context: {config.model.max_context_length}")
        print(f"  - Vector DB: {config.memory.vector_db_type}")
        
        # Test semantic network
        from ai_core.semantic_network import core_network
        print("✓ Core semantic network loaded")
        print(f"  - Emotions: {len(core_network.emotion_nodes)}")
        print(f"  - Concepts: {len(core_network.concept_nodes)}")
        
        # Test emotion detection
        from ai_core.emotion_detector import emotion_detector
        print("✓ Emotion detector initialized")
        
        # Test personal network
        from ai_core.personal_network import PersonalSemanticNetwork
        personal_net = PersonalSemanticNetwork("test_user", core_network)
        print("✓ Personal network created")
        
        # Test memory manager
        from ai_core.memory_manager import MemoryManager
        memory_mgr = MemoryManager("test_user")
        print("✓ Memory manager initialized")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing core components: {e}")
        return False

def test_emotion_detection():
    """Test emotion detection with sample texts"""
    print("\n🔍 Testing Emotion Detection...")
    
    try:
        from ai_core.emotion_detector import emotion_detector
        
        test_cases = [
            "I'm feeling really happy today!",
            "I'm so anxious about my presentation tomorrow",
            "I'm absolutely furious with my boss",
            "I feel so sad and lonely right now",
            "I'm excited about the new opportunity",
            "I'm terrified of what might happen",
            "I'm disgusted by that behavior",
            "I'm surprised by the unexpected news"
        ]
        
        for text in test_cases:
            result = emotion_detector.detect_emotions(text)
            print(f"  '{text}' → {result.primary_emotion} (confidence: {result.confidence:.2f})")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing emotion detection: {e}")
        return False

def test_semantic_network():
    """Test semantic network functionality"""
    print("\n🧠 Testing Semantic Network...")
    
    try:
        from ai_core.semantic_network import core_network
        
        # Test emotion info
        joy_info = core_network.get_emotion_info("joy")
        print(f"✓ Joy emotion info: {joy_info.name}, valence: {joy_info.valence}")
        
        # Test concept relationships
        work_emotions = core_network.find_related_emotions("work")
        print(f"✓ Work-related emotions: {work_emotions[:3]}")
        
        # Test coping strategies
        fear_coping = core_network.get_coping_strategies("fear")
        print(f"✓ Fear coping strategies: {fear_coping}")
        
        # Test body mappings
        anger_body = core_network.get_body_mapping("anger")
        print(f"✓ Anger body regions: {anger_body}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing semantic network: {e}")
        return False

def test_personal_network():
    """Test personal network functionality"""
    print("\n👤 Testing Personal Network...")
    
    try:
        from ai_core.semantic_network import core_network
        from ai_core.personal_network import PersonalSemanticNetwork
        
        # Create personal network
        personal_net = PersonalSemanticNetwork("test_user", core_network)
        
        # Test onboarding
        onboarding_data = {
            "stressors": ["work deadlines", "public speaking"],
            "supports": ["family", "friends"],
            "hobbies": ["painting", "music"],
            "coping_strategies": ["deep breathing", "exercise"],
            "coping_style": "active",
            "awareness_level": "high",
            "support_network": ["sister", "best friend"],
            "goals": ["reduce anxiety", "improve sleep"],
            "values": ["family", "creativity"]
        }
        
        personal_net.process_onboarding(onboarding_data)
        print("✓ Onboarding processed successfully")
        
        # Test conversation processing
        conversation_data = {
            "emotions": {"anxiety": 0.8, "stress": 0.6},
            "concepts": ["work", "deadline", "presentation"],
            "coping_strategies": ["deep breathing"],
            "coping_effectiveness": 0.7
        }
        
        personal_net.process_conversation(conversation_data)
        print("✓ Conversation processed successfully")
        
        # Get user summary
        summary = personal_net.get_user_summary()
        print(f"✓ User summary generated: {summary['network_size']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing personal network: {e}")
        return False

def test_memory_manager():
    """Test memory management functionality"""
    print("\n💾 Testing Memory Manager...")
    
    try:
        from ai_core.memory_manager import MemoryManager
        from ai_core.personal_network import PersonalSemanticNetwork
        from ai_core.semantic_network import core_network
        
        # Create memory manager
        memory_mgr = MemoryManager("test_user")
        personal_net = PersonalSemanticNetwork("test_user", core_network)
        
        # Test adding messages to short-term memory
        test_messages = [
            {
                "content": "I'm feeling anxious about my presentation",
                "emotion": "anxiety",
                "intensity": 0.8,
                "concepts": ["work", "presentation"],
                "user_id": "test_user",
                "type": "user"
            },
            {
                "content": "Let's try some deep breathing exercises",
                "emotion": "calm",
                "intensity": 0.6,
                "concepts": ["coping", "breathing"],
                "user_id": "test_user",
                "type": "ai"
            }
        ]
        
        for msg in test_messages:
            memory_mgr.add_to_short_term(msg)
        
        print("✓ Messages added to short-term memory")
        
        # Test memory context retrieval
        context = memory_mgr.get_memory_context("presentation anxiety", personal_net)
        print(f"✓ Memory context retrieved: {len(context.get('relevant_memories', []))} memories")
        
        # Test conversation ending
        memory_mgr.end_conversation()
        print("✓ Conversation ended and queued for consolidation")
        
        # Test memory consolidation
        memory_mgr.consolidate_memories(personal_net)
        print("✓ Memories consolidated")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing memory manager: {e}")
        return False

async def test_ai_engine():
    """Test the main AI engine"""
    print("\n🤖 Testing AI Engine...")
    
    try:
        from ai_core.ai_engine import ai_engine
        
        # Test message processing
        test_messages = [
            "I'm feeling really anxious about my presentation tomorrow",
            "I'm so happy about getting the promotion!",
            "I'm really angry with my colleague for taking credit for my work",
            "I feel so sad and lonely today"
        ]
        
        for message in test_messages:
            print(f"\n  Testing: '{message}'")
            response = await ai_engine.process_message("test_user", message)
            print(f"    Detected emotion: {response.emotion_detected}")
            print(f"    Confidence: {response.confidence:.2f}")
            print(f"    Response time: {response.response_time:.2f}s")
            print(f"    Coping suggestions: {response.coping_suggestions[:2]}")
        
        # Test user profile
        profile = await ai_engine.get_user_profile("test_user")
        print(f"\n✓ User profile retrieved: {profile['network_size']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing AI engine: {e}")
        return False

def test_integration():
    """Test full system integration"""
    print("\n🔗 Testing Full System Integration...")
    
    try:
        # Test complete workflow
        from ai_core.ai_engine import ai_engine
        from ai_core.emotion_detector import emotion_detector
        from ai_core.semantic_network import core_network
        
        # Simulate user interaction
        user_message = "I'm feeling overwhelmed with work and my relationship is suffering"
        
        # 1. Emotion detection
        emotion_result = emotion_detector.detect_emotions(user_message)
        print(f"✓ Emotion detected: {emotion_result.primary_emotion}")
        
        # 2. Semantic network lookup
        coping_strategies = core_network.get_coping_strategies(emotion_result.primary_emotion)
        print(f"✓ Coping strategies: {coping_strategies[:3]}")
        
        # 3. Body sensations
        body_regions = emotion_result.body_sensations
        print(f"✓ Body sensations: {body_regions}")
        
        print("✓ Full integration test completed")
        return True
        
    except Exception as e:
        print(f"✗ Error testing integration: {e}")
        return False

def interactive_test():
    """Interactive testing mode"""
    print("\n🎮 Interactive Testing Mode")
    print("Type messages to test the AI system. Type 'quit' to exit.")
    
    try:
        from ai_core.ai_engine import ai_engine
        from ai_core.emotion_detector import emotion_detector
        
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            # Quick emotion detection
            emotion_result = emotion_detector.detect_emotions(user_input)
            print(f"AI detected: {emotion_result.primary_emotion} (confidence: {emotion_result.confidence:.2f})")
            
            # Full AI response (async)
            async def get_response():
                return await ai_engine.process_message("interactive_user", user_input)
            
            response = asyncio.run(get_response())
            print(f"AI Response: {response.response_text}")
            
            if response.coping_suggestions:
                print(f"Coping suggestions: {', '.join(response.coping_suggestions[:2])}")
    
    except KeyboardInterrupt:
        print("\n\nInteractive testing ended.")
    except Exception as e:
        print(f"Error in interactive testing: {e}")

def main():
    """Main testing function"""
    print("🧠 Evolance AI System Testing Suite")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("ai_core"):
        print("❌ Error: ai_core directory not found!")
        print("Please run this script from the backend directory.")
        return
    
    # Run all tests
    tests = [
        ("Core Components", test_core_components),
        ("Emotion Detection", test_emotion_detection),
        ("Semantic Network", test_semantic_network),
        ("Personal Network", test_personal_network),
        ("Memory Manager", test_memory_manager),
        ("AI Engine", lambda: asyncio.run(test_ai_engine())),
        ("Integration", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} test passed")
            else:
                print(f"✗ {test_name} test failed")
        except Exception as e:
            print(f"✗ {test_name} test error: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The AI system is working correctly.")
        
        # Offer interactive testing
        choice = input("\nWould you like to try interactive testing? (y/n): ")
        if choice.lower() in ['y', 'yes']:
            interactive_test()
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 