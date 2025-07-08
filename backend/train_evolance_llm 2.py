#!/usr/bin/env python3
"""
Train Evolance LLM
Trains our proprietary emotional intelligence language model
"""

import os
import sys
import torch
import json
from pathlib import Path

# Add the ai_core module to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai_core'))

from evolance_llm import llm_trainer, EmotionalTransformer
from training_data_generator import generate_training_data
from datasets import Dataset

def setup_training_environment():
    """Setup the training environment"""
    print("🔧 Setting up training environment...")
    
    # Create data directory
    data_dir = Path("backend/data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for GPU
    if torch.cuda.is_available():
        print(f"✓ GPU available: {torch.cuda.get_device_name(0)}")
        device = torch.device("cuda")
    else:
        print("⚠️  No GPU detected, using CPU (training will be slower)")
        device = torch.device("cpu")
    
    return device

def prepare_training_data():
    """Prepare training data for the LLM"""
    print("📊 Preparing training data...")
    
    # Generate training data if it doesn't exist
    data_file = Path("backend/data/full_training_dataset.json")
    if not data_file.exists():
        print("🔄 Generating training data...")
        generate_training_data()
    
    # Load the dataset
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    # Format data for training
    formatted_data = []
    for item in data:
        if "messages" in item:
            # Format conversation data
            conversation_text = ""
            for message in item["messages"]:
                if message["role"] == "user":
                    emotion = message.get("emotion", "neutral")
                    context = message.get("context", "general")
                    conversation_text += f"<emotion>{emotion}</emotion><context>{context}</context>User: {message['text']}\n"
                else:
                    conversation_text += f"Assistant: {message['text']}\n"
            
            formatted_data.append({"text": conversation_text.strip()})
    
    print(f"✓ Prepared {len(formatted_data)} training examples")
    return formatted_data

def train_evolance_llm():
    """Train the Evolance LLM"""
    print("🚀 Starting Evolance LLM Training")
    print("=" * 50)
    
    # Setup environment
    device = setup_training_environment()
    
    # Initialize model
    print("\n🧠 Initializing Evolance LLM model...")
    llm_trainer.initialize_model()
    
    # Prepare training data
    print("\n📊 Preparing training data...")
    training_data = prepare_training_data()
    
    # Create dataset
    dataset = Dataset.from_list(training_data)
    
    # Train the model
    print("\n🎯 Starting training...")
    output_dir = "backend/models/evolance_llm"
    
    try:
        llm_trainer.train(dataset, output_dir)
        print(f"\n✅ Evolance LLM training completed successfully!")
        print(f"✅ Model saved to: {output_dir}")
        
        # Save training info
        training_info = {
            "model_type": "EmotionalTransformer",
            "training_examples": len(training_data),
            "vocab_size": llm_trainer.config.get("vocab_size", 50257),
            "embedding_dim": llm_trainer.config.get("n_embd", 768),
            "layers": llm_trainer.config.get("n_layer", 12),
            "heads": llm_trainer.config.get("n_head", 12),
            "specialized_for": "emotional_intelligence",
            "features": [
                "emotion_awareness",
                "context_understanding", 
                "empathy_generation",
                "support_strategies",
                "personality_adaptation"
            ]
        }
        
        with open(f"{output_dir}/training_info.json", 'w') as f:
            json.dump(training_info, f, indent=2)
        
        print(f"✅ Training info saved to: {output_dir}/training_info.json")
        
    except Exception as e:
        print(f"\n❌ Training failed: {str(e)}")
        raise

def test_evolance_llm():
    """Test the trained Evolance LLM"""
    print("\n🧪 Testing Evolance LLM...")
    
    model_path = "backend/models/evolance_llm"
    
    if not Path(model_path).exists():
        print("❌ No trained model found. Please run training first.")
        return
    
    # Load the trained model
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path)
        
        # Test prompts
        test_prompts = [
            "<emotion>sad</emotion><context>relationships</context>User: I feel so lonely lately.\nAssistant:",
            "<emotion>anxious</emotion><context>work</context>User: I'm worried about my presentation tomorrow.\nAssistant:",
            "<emotion>happy</emotion><context>personal_growth</context>User: I finally achieved my goal!\nAssistant:"
        ]
        
        print("\n📝 Testing model responses:")
        print("-" * 40)
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\nTest {i}:")
            print(f"Prompt: {prompt}")
            
            # Generate response
            inputs = tokenizer(prompt, return_tensors="pt")
            
            with torch.no_grad():
                outputs = model.generate(
                    inputs["input_ids"],
                    max_length=100,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            print(f"Response: {response}")
        
        print("\n✅ Evolance LLM testing completed!")
        
    except Exception as e:
        print(f"❌ Testing failed: {str(e)}")

def main():
    """Main training function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Train Evolance LLM")
    parser.add_argument("--train", action="store_true", help="Train the Evolance LLM")
    parser.add_argument("--test", action="store_true", help="Test the trained LLM")
    parser.add_argument("--both", action="store_true", help="Train and test the LLM")
    
    args = parser.parse_args()
    
    if args.train or args.both:
        train_evolance_llm()
    
    if args.test or args.both:
        test_evolance_llm()
    
    if not any([args.train, args.test, args.both]):
        print("Usage: python train_evolance_llm.py --train --test --both")
        print("  --train: Train the Evolance LLM")
        print("  --test:  Test the trained LLM")
        print("  --both:  Train and test the LLM")

if __name__ == "__main__":
    main() 