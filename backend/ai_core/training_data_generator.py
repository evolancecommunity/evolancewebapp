"""
Training Data Generator for Evolance Custom LLM
Generates emotional intelligence conversation datasets
"""

import json
import random
from typing import List, Dict, Any
from pathlib import Path

class EmotionalTrainingDataGenerator:
    """Generates training data for emotional intelligence LLM"""
    
    def __init__(self):
        self.emotions = [
            "happy", "sad", "angry", "anxious", "excited", 
            "frustrated", "grateful", "lonely", "confident", "insecure",
            "peaceful", "stressed", "hopeful", "disappointed", "proud", "ashamed"
        ]
        
        self.contexts = [
            "work", "relationships", "health", "family", "friendship",
            "personal_growth", "crisis", "celebration", "daily_life", "reflection"
        ]
        
        self.personality_traits = [
            "introvert", "extrovert", "analytical", "emotional", "practical"
        ]
        
        self.conversation_templates = self._load_conversation_templates()
    
    def _load_conversation_templates(self) -> List[Dict[str, Any]]:
        """Load conversation templates for different scenarios"""
        return [
            {
                "scenario": "stress_at_work",
                "context": "work",
                "conversations": [
                    {
                        "user": "I'm feeling really overwhelmed with my workload lately. I can't seem to catch up.",
                        "emotion": "stressed",
                        "ai_response": "That sounds really tough. Work stress can be so draining. What's been the most challenging part for you?",
                        "ai_emotion": "empathetic",
                        "ai_context": "supportive_listening"
                    },
                    {
                        "user": "My boss keeps adding more tasks and I'm afraid to say no.",
                        "emotion": "anxious",
                        "ai_response": "It's totally normal to feel that way. Setting boundaries at work can be really hard. Have you thought about how you might approach that conversation?",
                        "ai_emotion": "understanding",
                        "ai_context": "problem_solving"
                    }
                ]
            },
            {
                "scenario": "relationship_issues",
                "context": "relationships",
                "conversations": [
                    {
                        "user": "My partner and I had a big fight last night. I feel like we're growing apart.",
                        "emotion": "sad",
                        "ai_response": "I'm sorry you're going through that. Relationship struggles can be really painful. What happened that made you feel like you're growing apart?",
                        "ai_emotion": "caring",
                        "ai_context": "emotional_support"
                    },
                    {
                        "user": "I don't know if I should try to work things out or just end it.",
                        "emotion": "confused",
                        "ai_response": "That's such a difficult decision to make. It sounds like you're really torn. What would you ideally want to happen?",
                        "ai_emotion": "neutral",
                        "ai_context": "exploration"
                    }
                ]
            },
            {
                "scenario": "personal_achievement",
                "context": "personal_growth",
                "conversations": [
                    {
                        "user": "I finally finished that project I've been working on for months! I'm so proud of myself.",
                        "emotion": "proud",
                        "ai_response": "That's amazing! You should definitely be proud - that's a huge accomplishment. What was the most rewarding part of finishing it?",
                        "ai_emotion": "excited",
                        "ai_context": "celebration"
                    },
                    {
                        "user": "I never thought I could do it, but I actually did!",
                        "emotion": "excited",
                        "ai_response": "That's the best feeling, isn't it? Proving to yourself that you're capable of more than you thought. What do you think you'll tackle next?",
                        "ai_emotion": "enthusiastic",
                        "ai_context": "encouragement"
                    }
                ]
            },
            {
                "scenario": "health_concerns",
                "context": "health",
                "conversations": [
                    {
                        "user": "I've been feeling really tired lately and I'm worried something might be wrong.",
                        "emotion": "worried",
                        "ai_response": "That's definitely concerning. Our bodies often give us signals when something's not right. Have you noticed any other symptoms?",
                        "ai_emotion": "concerned",
                        "ai_context": "health_support"
                    },
                    {
                        "user": "I'm scared to go to the doctor. What if it's something serious?",
                        "emotion": "fearful",
                        "ai_response": "I understand that fear - it's completely normal. But getting checked out is the best way to take care of yourself. Would it help to think about what you'd want to know?",
                        "ai_emotion": "calming",
                        "ai_context": "reassurance"
                    }
                ]
            },
            {
                "scenario": "loneliness",
                "context": "daily_life",
                "conversations": [
                    {
                        "user": "I feel so alone lately. Everyone seems to have their own lives and I'm just... here.",
                        "emotion": "lonely",
                        "ai_response": "That feeling of loneliness can be so heavy. It's like you're surrounded by people but still feel isolated. What kind of connection are you craving right now?",
                        "ai_emotion": "understanding",
                        "ai_context": "emotional_support"
                    },
                    {
                        "user": "I don't know how to reach out to people. I'm afraid they don't really want to hear from me.",
                        "emotion": "insecure",
                        "ai_response": "That fear of rejection is so real. But you know what? Most people actually appreciate when someone reaches out. What's one small way you could connect with someone today?",
                        "ai_emotion": "encouraging",
                        "ai_context": "motivation"
                    }
                ]
            }
        ]
    
    def generate_conversation_dataset(self, num_conversations: int = 1000) -> List[Dict[str, Any]]:
        """Generate a dataset of emotional conversations"""
        
        dataset = []
        
        for _ in range(num_conversations):
            # Select random template
            template = random.choice(self.conversation_templates)
            
            # Generate variations
            for conversation in template["conversations"]:
                # Create multiple variations
                for _ in range(3):  # 3 variations per conversation
                    variation = self._create_conversation_variation(conversation, template)
                    dataset.append(variation)
        
        return dataset
    
    def _create_conversation_variation(self, conversation: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
        """Create a variation of a conversation"""
        
        # Add some randomness to responses
        response_variations = {
            "That sounds really tough. Work stress can be so draining. What's been the most challenging part for you?": [
                "Work stress is no joke. I can hear how overwhelmed you're feeling. What's been the hardest part?",
                "That sounds exhausting. Being overwhelmed at work can really take a toll. What's been the biggest challenge?",
                "I can imagine how draining that must be. Work stress can be so persistent. What's been the most difficult aspect?"
            ],
            "It's totally normal to feel that way. Setting boundaries at work can be really hard. Have you thought about how you might approach that conversation?": [
                "That's completely understandable. Workplace boundaries are tricky. How do you think you might handle that?",
                "You're not alone in feeling that way. Work boundaries can be really challenging. What approach feels right to you?",
                "That's a really common struggle. Setting limits at work takes courage. How might you want to address this?"
            ]
        }
        
        user_message = conversation["user"]
        ai_response = conversation["ai_response"]
        
        # Add variation to AI response if available
        if ai_response in response_variations:
            ai_response = random.choice(response_variations[ai_response])
        
        return {
            "messages": [
                {
                    "role": "user",
                    "text": user_message,
                    "emotion": conversation["emotion"],
                    "context": template["context"]
                },
                {
                    "role": "assistant", 
                    "text": ai_response,
                    "emotion": conversation["ai_emotion"],
                    "context": conversation["ai_context"]
                }
            ],
            "scenario": template["scenario"],
            "context": template["context"]
        }
    
    def generate_emotional_responses(self, num_responses: int = 500) -> List[Dict[str, Any]]:
        """Generate emotional response patterns"""
        
        responses = []
        
        # Happy responses
        happy_patterns = [
            "That's wonderful! I'm so happy for you.",
            "That's fantastic news! You must be thrilled.",
            "How exciting! That's something to celebrate.",
            "That's amazing! I can feel your joy.",
            "That's brilliant! You deserve this happiness."
        ]
        
        # Sad responses
        sad_patterns = [
            "I'm so sorry you're going through this.",
            "That sounds really difficult. I'm here for you.",
            "I can hear how much this hurts. You're not alone.",
            "That's heartbreaking. I wish I could make it better.",
            "I'm sorry you're feeling this way. It's okay to not be okay."
        ]
        
        # Anxious responses
        anxious_patterns = [
            "I understand that worry. It's completely normal to feel that way.",
            "That anxiety makes total sense given the situation.",
            "I can hear how concerned you are. What's the worst that could happen?",
            "That nervousness is valid. What would help you feel more grounded?",
            "I get why you're feeling anxious. Let's break this down together."
        ]
        
        # Angry responses
        angry_patterns = [
            "That's completely unfair. You have every right to be angry.",
            "I can hear how frustrated you are. That situation sounds infuriating.",
            "That's outrageous. Anyone would be mad about that.",
            "I understand your anger. That's not okay what happened.",
            "You're absolutely right to be upset. That's unacceptable."
        ]
        
        emotion_patterns = {
            "happy": happy_patterns,
            "sad": sad_patterns,
            "anxious": anxious_patterns,
            "angry": angry_patterns
        }
        
        for emotion, patterns in emotion_patterns.items():
            for pattern in patterns:
                responses.append({
                    "emotion": emotion,
                    "response": pattern,
                    "context": "emotional_support"
                })
        
        return responses
    
    def save_dataset(self, dataset: List[Dict[str, Any]], filepath: str):
        """Save the generated dataset to a file"""
        
        output_path = Path(filepath)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(dataset, f, indent=2)
        
        print(f"✓ Dataset saved to {filepath}")
        print(f"✓ Generated {len(dataset)} conversation examples")

def generate_training_data():
    """Generate training data for the custom LLM"""
    
    generator = EmotionalTrainingDataGenerator()
    
    # Generate conversation dataset
    print("🔄 Generating emotional conversation dataset...")
    conversations = generator.generate_conversation_dataset(num_conversations=2000)
    
    # Generate emotional responses
    print("🔄 Generating emotional response patterns...")
    responses = generator.generate_emotional_responses(num_responses=1000)
    
    # Combine datasets
    full_dataset = conversations + [{"emotional_responses": responses}]
    
    # Save datasets
    generator.save_dataset(conversations, "backend/data/emotional_conversations.json")
    generator.save_dataset(responses, "backend/data/emotional_responses.json")
    generator.save_dataset(full_dataset, "backend/data/full_training_dataset.json")
    
    print("✓ Training data generation complete!")
    print(f"✓ Generated {len(conversations)} conversations")
    print(f"✓ Generated {len(responses)} emotional responses")

if __name__ == "__main__":
    generate_training_data() 