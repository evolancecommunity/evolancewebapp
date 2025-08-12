#!/usr/bin/env python3
"""
Free AI Training for Spiritual Wellness
Uses Google Colab free GPU to train a spiritual AI model
"""

import json
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
import os
from pathlib import Path
from typing import List, Dict, Any

class FreeSpiritualAITrainer:
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-medium"  # Free, good for conversations
        self.tokenizer = None
        self.model = None
        self.training_data = []
        
    def load_free_model(self):
        """Load a free pre-trained model"""
        print("🔄 Loading free pre-trained model...")
        
        # Use DialoGPT for conversation capabilities
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        
        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        print(f"✅ Loaded model: {self.model_name}")
        return self.model, self.tokenizer
    
    def load_training_data(self, data_path: str = "training_data"):
        """Load the collected training data"""
        print("📊 Loading training data...")
        
        # Load conversation templates
        templates_path = Path(data_path) / "conversation_templates.json"
        if templates_path.exists():
            with open(templates_path, "r") as f:
                templates = json.load(f)
            
            for template in templates:
                conversation = template["conversation"]
                # Format for training
                text = ""
                for turn in conversation:
                    text += f"{turn['role']}: {turn['content']}\n"
                text += "assistant: "  # End with assistant for next token prediction
                
                self.training_data.append({
                    "text": text,
                    "domain": template["domain"],
                    "techniques": template["techniques"]
                })
        
        print(f"✅ Loaded {len(self.training_data)} training examples")
        return self.training_data
    
    def prepare_dataset(self) -> Dataset:
        """Prepare dataset for training"""
        print("🔧 Preparing dataset...")
        
        # Tokenize the training data
        texts = [item["text"] for item in self.training_data]
        
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors="pt"
            )
        
        # Create dataset
        dataset = Dataset.from_dict({"text": texts})
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        
        print(f"✅ Dataset prepared with {len(tokenized_dataset)} examples")
        return tokenized_dataset
    
    def train_model(self, dataset: Dataset, output_dir: str = "spiritual_ai_model"):
        """Train the model using free resources"""
        print("🚀 Starting training...")
        
        # Training arguments optimized for free GPU
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=3,  # Small number for free GPU
            per_device_train_batch_size=2,  # Small batch size
            gradient_accumulation_steps=4,  # Accumulate gradients
            learning_rate=5e-5,
            warmup_steps=100,
            logging_steps=10,
            save_steps=500,
            eval_steps=500,
            evaluation_strategy="steps",
            load_best_model_at_end=True,
            save_total_limit=2,  # Save only 2 checkpoints
            fp16=True,  # Use mixed precision to save memory
            dataloader_pin_memory=False,  # Save memory
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,  # Not masked language modeling
        )
        
        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            data_collator=data_collator,
        )
        
        # Train the model
        trainer.train()
        
        # Save the model
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)
        
        print(f"✅ Training complete! Model saved to {output_dir}")
        return trainer
    
    def create_inference_script(self, model_path: str = "spiritual_ai_model"):
        """Create a simple inference script"""
        inference_script = f'''
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class SpiritualAI:
    def __init__(self, model_path="{model_path}"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        
    def generate_response(self, user_input: str, max_length: int = 100) -> str:
        # Format input
        input_text = f"user: {{user_input}}\\nassistant: "
        
        # Tokenize
        inputs = self.tokenizer.encode(input_text, return_tensors="pt")
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract assistant response
        if "assistant:" in response:
            response = response.split("assistant:")[-1].strip()
        
        return response

# Usage
if __name__ == "__main__":
    ai = SpiritualAI()
    response = ai.generate_response("I'm feeling anxious")
    print(response)
'''
        
        with open("spiritual_ai_inference.py", "w") as f:
            f.write(inference_script)
        
        print("✅ Created inference script: spiritual_ai_inference.py")
        return inference_script

def main():
    """Main training pipeline"""
    print("🌟 Starting Free Spiritual AI Training")
    print("=" * 50)
    
    # Initialize trainer
    trainer = FreeSpiritualAITrainer()
    
    # Load model
    model, tokenizer = trainer.load_free_model()
    
    # Load data
    training_data = trainer.load_training_data()
    
    if not training_data:
        print("❌ No training data found. Run data_collection.py first.")
        return
    
    # Prepare dataset
    dataset = trainer.prepare_dataset()
    
    # Train model
    trainer_instance = trainer.train_model(dataset)
    
    # Create inference script
    trainer.create_inference_script()
    
    print("🎉 Training pipeline complete!")
    print("📁 Model saved to: spiritual_ai_model/")
    print("🐍 Inference script: spiritual_ai_inference.py")
    print("🚀 Ready to integrate with your app!")

if __name__ == "__main__":
    main() 