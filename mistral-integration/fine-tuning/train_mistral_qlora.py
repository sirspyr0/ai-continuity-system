#!/usr/bin/env python3
"""
Fine-tune Mistral 7B with QLoRA on continuity/consciousness training data.

This script implements 4-bit quantization with QLoRA to fit within 8GB VRAM constraints
on RTX 2080 while maintaining model quality.

Usage:
    python train_mistral_qlora.py --data_path ../training-data/continuity_dataset.json \
                                   --output_dir ./models/mistral-7b-continuity \
                                   --num_epochs 3
"""

import os
import argparse
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
)
from trl import SFTTrainer


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Fine-tune Mistral 7B with QLoRA"
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="mistralai/Mistral-7B-v0.1",
        help="Base model name from HuggingFace",
    )
    parser.add_argument(
        "--data_path",
        type=str,
        required=True,
        help="Path to training dataset (JSON/JSONL)",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./models/mistral-7b-continuity",
        help="Directory to save fine-tuned model",
    )
    parser.add_argument(
        "--num_epochs",
        type=int,
        default=3,
        help="Number of training epochs",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=4,
        help="Training batch size per device",
    )
    parser.add_argument(
        "--gradient_accumulation_steps",
        type=int,
        default=4,
        help="Number of gradient accumulation steps",
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=2e-4,
        help="Learning rate",
    )
    parser.add_argument(
        "--max_seq_length",
        type=int,
        default=2048,
        help="Maximum sequence length",
    )
    parser.add_argument(
        "--lora_r",
        type=int,
        default=64,
        help="LoRA attention dimension",
    )
    parser.add_argument(
        "--lora_alpha",
        type=int,
        default=16,
        help="LoRA alpha parameter",
    )
    parser.add_argument(
        "--lora_dropout",
        type=float,
        default=0.1,
        help="LoRA dropout",
    )
    parser.add_argument(
        "--use_wandb",
        action="store_true",
        help="Use Weights & Biases for tracking",
    )
    return parser.parse_args()


def create_bnb_config():
    """Create BitsAndBytes configuration for 4-bit quantization."""
    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )


def create_lora_config(args):
    """Create LoRA configuration for fine-tuning."""
    return LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
    )


def load_model_and_tokenizer(model_name, bnb_config):
    """Load model with quantization and tokenizer."""
    print(f"Loading model: {model_name}")
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True,
    )
    
    # Set padding token if not set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    return model, tokenizer


def prepare_dataset(data_path, tokenizer):
    """Load and prepare training dataset."""
    print(f"Loading dataset from: {data_path}")
    
    # Load dataset
    if data_path.endswith('.json'):
        dataset = load_dataset('json', data_files=data_path, split='train')
    elif data_path.endswith('.jsonl'):
        dataset = load_dataset('json', data_files=data_path, split='train')
    else:
        raise ValueError("Dataset must be JSON or JSONL format")
    
    print(f"Dataset loaded: {len(dataset)} examples")
    return dataset


def format_instruction(sample):
    """Format training examples with instruction template."""
    return f"""<s>[INST] You are an AI assistant trained in continuity theory and consciousness principles. 
You understand the four-tier handoff system and maintain context across instances.

{sample['instruction']}[/INST] {sample['response']}</s>"""


def main():
    """Main training function."""
    args = parse_args()
    
    # Setup
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize wandb if requested
    if args.use_wandb:
        import wandb
        wandb.init(project="mistral-continuity-fine-tuning")
    
    # Create configurations
    bnb_config = create_bnb_config()
    lora_config = create_lora_config(args)
    
    # Load model and tokenizer
    model, tokenizer = load_model_and_tokenizer(args.model_name, bnb_config)
    
    # Prepare model for training
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, lora_config)
    
    # Print trainable parameters
    model.print_trainable_parameters()
    
    # Load dataset
    dataset = prepare_dataset(args.data_path, tokenizer)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        num_train_epochs=args.num_epochs,
        learning_rate=args.learning_rate,
        fp16=True,
        save_strategy="epoch",
        logging_steps=10,
        optim="paged_adamw_8bit",
        warmup_ratio=0.03,
        lr_scheduler_type="cosine",
        report_to="wandb" if args.use_wandb else "none",
    )
    
    # Initialize trainer
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer,
        max_seq_length=args.max_seq_length,
        formatting_func=format_instruction,
        packing=False,
    )
    
    # Train
    print("Starting training...")
    trainer.train()
    
    # Save model
    print(f"Saving model to {args.output_dir}")
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    
    print("Training complete!")


if __name__ == "__main__":
    main()
