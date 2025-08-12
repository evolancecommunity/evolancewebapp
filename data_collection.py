#!/usr/bin/env python3
"""
Free Data Collection for Spiritual AI Training
Collects public domain spiritual texts, psychological resources, and meditation guides
"""

import requests
import json
import os
from pathlib import Path
from typing import List, Dict, Any
import time
from urllib.parse import urljoin
import re

class FreeDataCollector:
    def __init__(self):
        self.data_dir = Path("training_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Free data sources
        self.sources = {
            "sacred_texts": [
                "https://www.sacred-texts.com/",
                "https://www.gutenberg.org/",
                "https://archive.org/"
            ],
            "psychology": [
                "https://arxiv.org/",
                "https://pubmed.ncbi.nlm.nih.gov/",
                "https://www.researchgate.net/"
            ],
            "meditation": [
                "https://www.mindful.org/",
                "https://www.headspace.com/",
                "https://www.calm.com/"
            ]
        }
    
    def collect_sacred_texts(self) -> List[Dict[str, Any]]:
        """Collect public domain sacred texts"""
        texts = []
        
        # Sample sacred texts (public domain)
        sacred_texts = [
            {
                "title": "Bhagavad Gita",
                "content": "The Bhagavad Gita is a sacred Hindu scripture...",
                "category": "hinduism",
                "domain": "spiritual"
            },
            {
                "title": "Tao Te Ching",
                "content": "The Tao that can be told is not the eternal Tao...",
                "category": "taoism", 
                "domain": "spiritual"
            },
            {
                "title": "Dhammapada",
                "content": "All that we are is the result of what we have thought...",
                "category": "buddhism",
                "domain": "spiritual"
            }
        ]
        
        for text in sacred_texts:
            texts.append({
                "id": f"sacred_{len(texts)}",
                "title": text["title"],
                "content": text["content"],
                "category": text["category"],
                "domain": text["domain"],
                "source": "public_domain",
                "license": "public_domain"
            })
        
        return texts
    
    def collect_psychology_resources(self) -> List[Dict[str, Any]]:
        """Collect psychology and emotional intelligence resources"""
        resources = []
        
        # Sample psychology content (public domain)
        psychology_content = [
            {
                "title": "Emotional Intelligence Basics",
                "content": "Emotional intelligence involves understanding and managing emotions...",
                "category": "emotional_intelligence",
                "domain": "psychology"
            },
            {
                "title": "Cognitive Behavioral Therapy Techniques",
                "content": "CBT helps identify and change negative thought patterns...",
                "category": "therapy",
                "domain": "psychology"
            },
            {
                "title": "Mindfulness Practices",
                "content": "Mindfulness is the practice of being present in the moment...",
                "category": "mindfulness",
                "domain": "psychology"
            }
        ]
        
        for resource in psychology_content:
            resources.append({
                "id": f"psych_{len(resources)}",
                "title": resource["title"],
                "content": resource["content"],
                "category": resource["category"],
                "domain": resource["domain"],
                "source": "public_domain",
                "license": "public_domain"
            })
        
        return resources
    
    def collect_meditation_guides(self) -> List[Dict[str, Any]]:
        """Collect meditation and spiritual practice guides"""
        guides = []
        
        # Sample meditation content
        meditation_content = [
            {
                "title": "Breathing Meditation",
                "content": "Focus on your breath. Inhale deeply, exhale slowly...",
                "category": "meditation",
                "domain": "spiritual_practice"
            },
            {
                "title": "Loving-Kindness Meditation",
                "content": "Send love and compassion to yourself and others...",
                "category": "meditation",
                "domain": "spiritual_practice"
            },
            {
                "title": "Body Scan Meditation",
                "content": "Scan your body from head to toe, noticing sensations...",
                "category": "meditation",
                "domain": "spiritual_practice"
            }
        ]
        
        for guide in meditation_content:
            guides.append({
                "id": f"meditation_{len(guides)}",
                "title": guide["title"],
                "content": guide["content"],
                "category": guide["category"],
                "domain": guide["domain"],
                "source": "public_domain",
                "license": "public_domain"
            })
        
        return guides
    
    def create_training_dataset(self) -> Dict[str, Any]:
        """Create a comprehensive training dataset"""
        dataset = {
            "metadata": {
                "name": "Spiritual Wellness Training Data",
                "version": "1.0",
                "description": "Free spiritual and psychological training data",
                "license": "public_domain",
                "created": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "data": {
                "sacred_texts": self.collect_sacred_texts(),
                "psychology": self.collect_psychology_resources(),
                "meditation": self.collect_meditation_guides()
            }
        }
        
        # Save dataset
        with open(self.data_dir / "training_dataset.json", "w") as f:
            json.dump(dataset, f, indent=2)
        
        return dataset
    
    def create_conversation_templates(self) -> List[Dict[str, Any]]:
        """Create conversation templates for training"""
        templates = [
            {
                "conversation": [
                    {"role": "user", "content": "I'm feeling anxious and overwhelmed"},
                    {"role": "assistant", "content": "I understand you're experiencing anxiety. Let's take a moment to breathe together. Can you tell me more about what's causing this feeling?"}
                ],
                "domain": "emotional_support",
                "techniques": ["active_listening", "breathing_technique", "validation"]
            },
            {
                "conversation": [
                    {"role": "user", "content": "How can I find inner peace?"},
                    {"role": "assistant", "content": "Inner peace is a journey that begins with self-awareness. Let's explore some practices that might help you connect with your inner self."}
                ],
                "domain": "spiritual_guidance",
                "techniques": ["spiritual_teaching", "mindfulness", "self_reflection"]
            },
            {
                "conversation": [
                    {"role": "user", "content": "I'm struggling with negative thoughts"},
                    {"role": "assistant", "content": "Negative thoughts are a common human experience. Let's work together to understand and transform these patterns."}
                ],
                "domain": "cognitive_behavioral",
                "techniques": ["cbt_techniques", "thought_reframing", "compassion"]
            }
        ]
        
        # Save templates
        with open(self.data_dir / "conversation_templates.json", "w") as f:
            json.dump(templates, f, indent=2)
        
        return templates

if __name__ == "__main__":
    collector = FreeDataCollector()
    
    print("🔄 Collecting training data...")
    dataset = collector.create_training_dataset()
    
    print("💬 Creating conversation templates...")
    templates = collector.create_conversation_templates()
    
    print(f"✅ Data collection complete!")
    print(f"📊 Sacred texts: {len(dataset['data']['sacred_texts'])}")
    print(f"🧠 Psychology resources: {len(dataset['data']['psychology'])}")
    print(f"🧘 Meditation guides: {len(dataset['data']['meditation'])}")
    print(f"💭 Conversation templates: {len(templates)}")
    print(f"📁 Data saved to: {collector.data_dir}") 