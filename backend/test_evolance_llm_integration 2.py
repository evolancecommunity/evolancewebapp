#!/usr/bin/env python3
"""
Integrated Test for Evolance LLM
Runs end-to-end test: data generation, training, loading, and response generation
"""

import os
import sys
from pathlib import Path
import time

# Add ai_core to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai_core'))

from ai_core.training_data_generator import generate_training_data
from ai_core.llm_integration import evolance_llm

MODEL_DIR = Path("backend/models/evolance_llm")
DATA_FILE = Path("backend/data/full_training_dataset.json")

# 1. Generate data if needed
def ensure_data():
    if not DATA_FILE.exists():
        print("[DATA] Generating training data...")
        generate_training_data()
    else:
        print("[DATA] Training data already exists.")

# 2. Train model if needed
def ensure_model():
    if not MODEL_DIR.exists():
        print("[MODEL] Training Evolance LLM (this may take a while)...")
        os.system("python backend/train_evolance_llm.py --train")
    else:
        print("[MODEL] Trained model already exists.")

# 3. Integrated test cases
def integrated_test():
    print("\n[TEST] Running integrated test cases...")
    test_cases = [
        {
            "input": "I'm feeling really anxious about my new job.",
            "expected_emotion": "anxious"
        },
        {
            "input": "I had a fight with my partner and feel sad.",
            "expected_emotion": "sad"
        },
        {
            "input": "I finally finished my project and I'm so proud!",
            "expected_emotion": "proud"
        },
        {
            "input": "I've been feeling tired and worried about my health.",
            "expected_emotion": "worried"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nCase {i}: {case['input']}")
        response = evolance_llm.generate_response(case['input'])
        print(f"  AI Response: {response['response']}")
        print(f"  Detected Emotion: {response.get('emotion_detected', 'unknown')}")
        print(f"  Model Used: {response.get('model_used', 'unknown')}")
        # Optionally assert expected emotion
        expected = case['expected_emotion']
        detected = response.get('emotion_detected', 'unknown')
        if expected == detected:
            print("  ✅ Emotion detection: CORRECT")
        else:
            print(f"  ⚠️  Emotion detection: {detected} (expected: {expected})")

if __name__ == "__main__":
    print("=== Evolance LLM Integrated Test ===")
    ensure_data()
    ensure_model()
    # Wait a moment for model to be ready (if just trained)
    time.sleep(2)
    integrated_test()
    print("\n=== Integrated Test Complete ===") 