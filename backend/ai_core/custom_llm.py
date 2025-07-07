"""
Evolance LLM
Proprietary Large Language Model for Emotional Intelligence
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, 
    TrainingArguments, Trainer, DataCollatorForLanguageModeling
)
from datasets import Dataset
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import json
import os
from pathlib import Path

class EmotionalTransformer(nn.Module):
    """
    Evolance transformer architecture optimized for emotional intelligence
    """
    
    def __init__(
        self,
        vocab_size: int = 50257,
        n_positions: int = 2048,
        n_embd: int = 768,
        n_layer: int = 12,
        n_head: int = 12,
        n_inner: int = 3072,
        activation_function: str = "gelu",
        resid_pdrop: float = 0.1,
        embd_pdrop: float = 0.1,
        attn_pdrop: float = 0.1,
        layer_norm_epsilon: float = 1e-5,
        initializer_range: float = 0.02,
        scale_attn_weights: bool = True,
        use_cache: bool = True,
        bos_token_id: int = 50256,
        eos_token_id: int = 50256,
        tie_word_embeddings: bool = False,
        # Emotional intelligence specific parameters
        emotion_embedding_dim: int = 64,
        context_embedding_dim: int = 128,
        personality_embedding_dim: int = 96
    ):
        super().__init__()
        
        self.vocab_size = vocab_size
        self.n_positions = n_positions
        self.n_embd = n_embd
        self.n_layer = n_layer
        self.n_head = n_head
        self.n_inner = n_inner
        self.activation_function = activation_function
        self.resid_pdrop = resid_pdrop
        self.embd_pdrop = embd_pdrop
        self.attn_pdrop = attn_pdrop
        self.layer_norm_epsilon = layer_norm_epsilon
        self.initializer_range = initializer_range
        self.scale_attn_weights = scale_attn_weights
        self.use_cache = use_cache
        self.bos_token_id = bos_token_id
        self.eos_token_id = eos_token_id
        self.tie_word_embeddings = tie_word_embeddings
        
        # Emotional intelligence enhancements
        self.emotion_embedding_dim = emotion_embedding_dim
        self.context_embedding_dim = context_embedding_dim
        self.personality_embedding_dim = personality_embedding_dim
        
        # Token embeddings
        self.wte = nn.Embedding(vocab_size, n_embd)
        self.wpe = nn.Embedding(n_positions, n_embd)
        
        # Emotional intelligence embeddings
        self.emotion_embeddings = nn.Embedding(16, emotion_embedding_dim)  # 16 emotions
        self.context_embeddings = nn.Embedding(10, context_embedding_dim)  # 10 context types
        self.personality_embeddings = nn.Embedding(5, personality_embedding_dim)  # 5 personality traits
        
        # Projection layers for emotional features
        self.emotion_projection = nn.Linear(emotion_embedding_dim, n_embd)
        self.context_projection = nn.Linear(context_embedding_dim, n_embd)
        self.personality_projection = nn.Linear(personality_embedding_dim, n_embd)
        
        # Transformer layers
        self.h = nn.ModuleList([
            EmotionalTransformerBlock(
                n_embd=n_embd,
                n_head=n_head,
                n_inner=n_inner,
                activation_function=activation_function,
                resid_pdrop=resid_pdrop,
                attn_pdrop=attn_pdrop,
                layer_norm_epsilon=layer_norm_epsilon,
                scale_attn_weights=scale_attn_weights
            ) for _ in range(n_layer)
        ])
        
        self.ln_f = nn.LayerNorm(n_embd, eps=layer_norm_epsilon)
        
        # Output projection
        self.lm_head = nn.Linear(n_embd, vocab_size, bias=False)
        
        # Emotional intelligence output heads
        self.emotion_head = nn.Linear(n_embd, 16)  # 16 emotion classes
        self.empathy_head = nn.Linear(n_embd, 1)   # Empathy score
        self.support_head = nn.Linear(n_embd, 10)  # Support strategy classification
        
        # Initialize weights
        self.apply(self._init_weights)
        
        # Tie weights if requested
        if self.tie_word_embeddings:
            self.lm_head.weight = self.wte.weight
    
    def _init_weights(self, module):
        """Initialize the weights"""
        if isinstance(module, (nn.Linear, nn.Embedding)):
            module.weight.data.normal_(mean=0.0, std=self.initializer_range)
        if isinstance(module, nn.Linear) and module.bias is not None:
            module.bias.data.zero_()
    
    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        token_type_ids: Optional[torch.LongTensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        emotion_ids: Optional[torch.LongTensor] = None,
        context_ids: Optional[torch.LongTensor] = None,
        personality_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Tuple[Tuple[torch.Tensor]]] = None,
        use_cache: Optional[bool] = None,
        return_dict: Optional[bool] = None,
    ) -> Dict[str, torch.Tensor]:
        
        return_dict = return_dict if return_dict is not None else True
        use_cache = use_cache if use_cache is not None else self.use_cache
        
        if input_ids is not None and inputs_embeds is not None:
            raise ValueError("You cannot specify both input_ids and inputs_embeds at the same time")
        elif input_ids is not None:
            input_shape = input_ids.size()
            input_ids = input_ids.view(-1, input_shape[-1])
            batch_size = input_ids.shape[0]
        elif inputs_embeds is not None:
            input_shape = inputs_embeds.size()[:-1]
            batch_size = inputs_embeds.shape[0]
        else:
            raise ValueError("You have to specify either input_ids or inputs_embeds")
        
        if token_type_ids is not None:
            token_type_ids = token_type_ids.view(-1, input_shape[-1])
        
        if position_ids is not None:
            position_ids = position_ids.view(-1, input_shape[-1])
        
        if past_key_values is None:
            past_length = 0
            past_key_values = tuple([None] * len(self.h))
        else:
            past_length = past_key_values[0][0].size(-2)
        
        if position_ids is None:
            device = input_ids.device if input_ids is not None else inputs_embeds.device
            position_ids = torch.arange(past_length, input_shape[-1] + past_length, dtype=torch.long, device=device)
            position_ids = position_ids.unsqueeze(0).view(-1, input_shape[-1])
        
        # Prepare attention mask
        if attention_mask is not None:
            attention_mask = attention_mask.view(batch_size, -1)
            attention_mask = attention_mask[:, None, None, :]
            attention_mask = attention_mask.to(dtype=self.dtype)
            attention_mask = (1.0 - attention_mask) * torch.finfo(self.dtype).min
        
        # Get embeddings
        if inputs_embeds is None:
            inputs_embeds = self.wte(input_ids)
        
        position_embeds = self.wpe(position_ids)
        hidden_states = inputs_embeds + position_embeds
        
        # Add emotional intelligence embeddings
        if emotion_ids is not None:
            emotion_embeds = self.emotion_embeddings(emotion_ids)
            emotion_projected = self.emotion_projection(emotion_embeds)
            hidden_states = hidden_states + emotion_projected
        
        if context_ids is not None:
            context_embeds = self.context_embeddings(context_ids)
            context_projected = self.context_projection(context_embeds)
            hidden_states = hidden_states + context_projected
        
        if personality_ids is not None:
            personality_embeds = self.personality_embeddings(personality_ids)
            personality_projected = self.personality_projection(personality_embeds)
            hidden_states = hidden_states + personality_projected
        
        # Apply dropout
        hidden_states = F.dropout(hidden_states, p=self.embd_pdrop, training=self.training)
        
        # Apply transformer layers
        presents = () if use_cache else None
        all_self_attentions = () if return_dict else None
        all_cross_attentions = () if return_dict else None
        all_hidden_states = () if return_dict else None
        
        for i, (block, layer_past) in enumerate(zip(self.h, past_key_values)):
            if return_dict:
                all_hidden_states = all_hidden_states + (hidden_states,)
            
            outputs = block(
                hidden_states,
                layer_past=layer_past,
                attention_mask=attention_mask,
                use_cache=use_cache,
                return_dict=return_dict,
            )
            
            hidden_states = outputs[0]
            if use_cache:
                presents = presents + (outputs[1],)
            
            if return_dict:
                all_self_attentions = all_self_attentions + (outputs[2],)
                if len(outputs) > 3:
                    all_cross_attentions = all_cross_attentions + (outputs[3],)
        
        hidden_states = self.ln_f(hidden_states)
        
        # Get logits
        lm_logits = self.lm_head(hidden_states)
        
        # Get emotional intelligence outputs
        emotion_logits = self.emotion_head(hidden_states)
        empathy_scores = self.empathy_head(hidden_states)
        support_logits = self.support_head(hidden_states)
        
        if not return_dict:
            return tuple(v for v in [lm_logits, presents, all_hidden_states, all_self_attentions] if v is not None)
        
        return {
            "logits": lm_logits,
            "past_key_values": presents,
            "hidden_states": all_hidden_states,
            "attentions": all_self_attentions,
            "emotion_logits": emotion_logits,
            "empathy_scores": empathy_scores,
            "support_logits": support_logits
        }

class EmotionalTransformerBlock(nn.Module):
    """Custom transformer block with emotional intelligence enhancements"""
    
    def __init__(
        self,
        n_embd: int,
        n_head: int,
        n_inner: int,
        activation_function: str,
        resid_pdrop: float,
        attn_pdrop: float,
        layer_norm_epsilon: float,
        scale_attn_weights: bool
    ):
        super().__init__()
        
        self.ln_1 = nn.LayerNorm(n_embd, eps=layer_norm_epsilon)
        self.attn = EmotionalAttention(
            n_embd=n_embd,
            n_head=n_head,
            attn_pdrop=attn_pdrop,
            resid_pdrop=resid_pdrop,
            scale_attn_weights=scale_attn_weights
        )
        self.ln_2 = nn.LayerNorm(n_embd, eps=layer_norm_epsilon)
        self.mlp = EmotionalMLP(
            n_embd=n_embd,
            n_inner=n_inner,
            activation_function=activation_function,
            resid_pdrop=resid_pdrop
        )
    
    def forward(
        self,
        hidden_states: torch.Tensor,
        layer_past: Optional[Tuple[torch.Tensor]] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = False,
        return_dict: Optional[bool] = True,
    ) -> Dict[str, torch.Tensor]:
        
        residual = hidden_states
        hidden_states = self.ln_1(hidden_states)
        attn_outputs = self.attn(
            hidden_states,
            layer_past=layer_past,
            attention_mask=attention_mask,
            use_cache=use_cache,
            return_dict=return_dict,
        )
        attn_output = attn_outputs[0]
        outputs = attn_outputs[1:]
        
        # Residual connection
        hidden_states = attn_output + residual
        
        residual = hidden_states
        hidden_states = self.ln_2(hidden_states)
        feed_forward_hidden_states = self.mlp(hidden_states)
        hidden_states = residual + feed_forward_hidden_states
        
        if use_cache:
            outputs = (hidden_states,) + outputs
        else:
            outputs = (hidden_states,) + outputs[1:]
        
        return outputs

class EmotionalAttention(nn.Module):
    """Attention mechanism with emotional intelligence enhancements"""
    
    def __init__(
        self,
        n_embd: int,
        n_head: int,
        attn_pdrop: float,
        resid_pdrop: float,
        scale_attn_weights: bool
    ):
        super().__init__()
        
        self.n_embd = n_embd
        self.n_head = n_head
        self.attn_pdrop = attn_pdrop
        self.resid_pdrop = resid_pdrop
        self.scale_attn_weights = scale_attn_weights
        
        self.c_attn = nn.Linear(n_embd, 3 * n_embd, bias=True)
        self.c_proj = nn.Linear(n_embd, n_embd, bias=True)
        self.c_proj = nn.utils.weight_norm(self.c_proj, name='weight', dim=1)
        
        # Emotional attention bias
        self.emotion_bias = nn.Parameter(torch.zeros(n_head))
        
    def forward(
        self,
        hidden_states: torch.Tensor,
        layer_past: Optional[Tuple[torch.Tensor]] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = False,
        return_dict: Optional[bool] = True,
    ) -> Dict[str, torch.Tensor]:
        
        batch_size, seq_len, n_embd = hidden_states.size()
        
        # Project to query, key, value
        qkv = self.c_attn(hidden_states)
        q, k, v = qkv.split(self.n_embd, dim=2)
        
        # Reshape for multi-head attention
        q = q.view(batch_size, seq_len, self.n_head, n_embd // self.n_head).transpose(1, 2)
        k = k.view(batch_size, seq_len, self.n_head, n_embd // self.n_head).transpose(1, 2)
        v = v.view(batch_size, seq_len, self.n_head, n_embd // self.n_head).transpose(1, 2)
        
        # Add emotional bias to attention
        if layer_past is not None:
            past_key, past_value = layer_past
            k = torch.cat((past_key, k), dim=-2)
            v = torch.cat((past_value, v), dim=-2)
        
        present = (k, v) if use_cache else None
        
        # Compute attention scores
        attn_weights = torch.matmul(q, k.transpose(-2, -1))
        
        if self.scale_attn_weights:
            attn_weights = attn_weights / (float(n_embd // self.n_head) ** 0.5)
        
        # Add emotional bias
        attn_weights = attn_weights + self.emotion_bias.view(1, self.n_head, 1, 1)
        
        if attention_mask is not None:
            attn_weights = attn_weights + attention_mask
        
        attn_weights = F.softmax(attn_weights, dim=-1)
        attn_weights = F.dropout(attn_weights, p=self.attn_pdrop, training=self.training)
        
        # Apply attention to values
        attn_output = torch.matmul(attn_weights, v)
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, seq_len, n_embd)
        attn_output = self.c_proj(attn_output)
        attn_output = F.dropout(attn_output, p=self.resid_pdrop, training=self.training)
        
        outputs = (attn_output,)
        if use_cache:
            outputs += (present,)
        
        return outputs

class EmotionalMLP(nn.Module):
    """MLP with emotional intelligence enhancements"""
    
    def __init__(
        self,
        n_embd: int,
        n_inner: int,
        activation_function: str,
        resid_pdrop: float
    ):
        super().__init__()
        
        self.c_fc = nn.Linear(n_embd, n_inner, bias=True)
        self.c_proj = nn.Linear(n_inner, n_embd, bias=True)
        self.c_proj = nn.utils.weight_norm(self.c_proj, name='weight', dim=1)
        self.act = self._get_activation_function(activation_function)
        self.dropout = nn.Dropout(resid_pdrop)
    
    def _get_activation_function(self, activation_function: str):
        if activation_function == "gelu":
            return F.gelu
        elif activation_function == "relu":
            return F.relu
        elif activation_function == "silu":
            return F.silu
        else:
            raise ValueError(f"Unsupported activation function: {activation_function}")
    
    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        hidden_states = self.c_fc(hidden_states)
        hidden_states = self.act(hidden_states)
        hidden_states = self.c_proj(hidden_states)
        hidden_states = self.dropout(hidden_states)
        return hidden_states

class EvolanceLLMTrainer:
    """Trainer for the Evolance LLM"""
    
    def __init__(self, model_config: Dict[str, Any]):
        self.config = model_config
        self.model = None
        self.tokenizer = None
        self.trainer = None
        
    def initialize_model(self):
        """Initialize the Evolance LLM model"""
        self.model = EmotionalTransformer(
            vocab_size=self.config.get("vocab_size", 50257),
            n_positions=self.config.get("n_positions", 2048),
            n_embd=self.config.get("n_embd", 768),
            n_layer=self.config.get("n_layer", 12),
            n_head=self.config.get("n_head", 12),
            n_inner=self.config.get("n_inner", 3072)
        )
        
        # Initialize tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        print("✓ Evolance LLM model initialized")
    
    def prepare_training_data(self, data_path: str) -> Dataset:
        """Prepare training data for emotional intelligence"""
        
        # Load emotional conversation data
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        # Format data for training
        formatted_data = []
        for conversation in data:
            # Add emotional context to each message
            for message in conversation["messages"]:
                text = message["text"]
                emotion = message.get("emotion", "neutral")
                context = message.get("context", "general")
                
                # Create training example with emotional context
                formatted_text = f"<emotion>{emotion}</emotion><context>{context}</context>{text}"
                formatted_data.append({"text": formatted_text})
        
        return Dataset.from_list(formatted_data)
    
    def train(self, train_dataset: Dataset, output_dir: str):
        """Train the Evolance LLM"""
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            save_steps=10000,
            save_total_limit=2,
            prediction_loss_only=True,
            learning_rate=5e-5,
            warmup_steps=1000,
            logging_steps=100,
            gradient_accumulation_steps=4,
            fp16=True if torch.cuda.is_available() else False,
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )
        
        # Initialize trainer
        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
            tokenizer=self.tokenizer,
        )
        
        # Train the model
        print("🚀 Starting Evolance LLM training...")
        self.trainer.train()
        
        # Save the model
        self.trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)
        
        print(f"✓ Evolance LLM trained and saved to {output_dir}")

# Global trainer instance
llm_trainer = EvolanceLLMTrainer({
    "vocab_size": 50257,
    "n_positions": 2048,
    "n_embd": 768,
    "n_layer": 12,
    "n_head": 12,
    "n_inner": 3072
}) 