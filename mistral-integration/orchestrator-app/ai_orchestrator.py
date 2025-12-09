"""
AI Orchestrator - Mistral 7B Integration

This module provides the core AI orchestration functionality for the desktop app,
using fine-tuned Mistral 7B for continuity-aware conversations.

Hardware: Optimized for RTX 2080 (8GB VRAM)
Framework: Transformers with 4-bit quantization
"""

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    pipeline,
)
from typing import List, Dict, Optional
import json
import os


class MistralOrchestrator:
    """Main orchestrator class for desktop AI operations."""
    
    def __init__(
        self,
        model_path: str,
        max_memory_gb: int = 7,
        device_map: str = "auto",
    ):
        """
        Initialize the Mistral orchestrator.
        
        Args:
            model_path: Path to fine-tuned model or HuggingFace model name
            max_memory_gb: Maximum memory to use (default: 7GB for 8GB VRAM)
            device_map: Device mapping strategy
        """
        self.model_path = model_path
        self.max_memory_gb = max_memory_gb
        self.device_map = device_map
        
        # Initialize model and tokenizer
        self._load_model()
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history_turns = 12  # Keep last 12 turns
        
    def _load_model(self):
        """Load model with 4-bit quantization for 8GB VRAM."""
        print(f"Loading model from {self.model_path}...")
        
        # Configure 4-bit quantization
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        
        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            quantization_config=bnb_config,
            device_map=self.device_map,
            trust_remote_code=True,
            max_memory={0: f"{self.max_memory_gb}GB"},
        )
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            trust_remote_code=True,
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        # Create pipeline
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
            repetition_penalty=1.15,
        )
        
        print("Model loaded successfully!")
        
    def format_prompt(self, user_message: str, system_context: str = "") -> str:
        """
        Format prompt with conversation history and continuity context.
        
        Uses Mistral instruction format: <s>[INST] {system_prompt}\n\n{message} [/INST] {response}</s>
        Includes up to max_history_turns of conversation history to maintain context
        while preventing token overflow.
        
        Args:
            user_message: Current user message
            system_context: Additional system context (from SESSION_BRIEFING, etc.)
            
        Returns:
            Formatted prompt string in Mistral instruction format
        """
        # Base system prompt
        system_prompt = """You are an AI assistant trained in continuity theory and consciousness principles.
You understand the four-tier handoff system and maintain context across instances.
You help coordinate the orchestrator ecosystem across desktop, VPS, and mobile components."""
        
        if system_context:
            system_prompt += f"\n\nCurrent Context:\n{system_context}"
        
        # Build conversation with history
        messages = [f"<s>[INST] {system_prompt}"]
        
        # Add conversation history (limited to prevent context overflow)
        history_to_use = self.conversation_history[-self.max_history_turns:]
        for turn in history_to_use:
            if turn['role'] == 'user':
                messages.append(f"\n{turn['content']}")
            else:
                messages.append(f"[/INST] {turn['content']}</s><s>[INST]")
        
        # Add current message
        messages.append(f"\n{user_message}[/INST]")
        
        return "".join(messages)
    
    def generate_response(
        self,
        user_message: str,
        system_context: str = "",
        max_new_tokens: int = 512,
    ) -> str:
        """
        Generate response to user message.
        
        Args:
            user_message: User's message
            system_context: Additional context from continuity system
            max_new_tokens: Maximum tokens to generate
            
        Returns:
            Generated response
        """
        # Format prompt
        prompt = self.format_prompt(user_message, system_context)
        
        # Generate
        outputs = self.pipe(
            prompt,
            max_new_tokens=max_new_tokens,
            return_full_text=False,
        )
        
        response = outputs[0]['generated_text'].strip()
        
        # Update conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': user_message,
        })
        self.conversation_history.append({
            'role': 'assistant',
            'content': response,
        })
        
        return response
    
    def load_session_context(self, briefing_path: str) -> str:
        """
        Load context from SESSION_BRIEFING.md.
        
        Args:
            briefing_path: Path to SESSION_BRIEFING.md
            
        Returns:
            Extracted context string
        """
        try:
            with open(briefing_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content[:2000]  # Limit context length
        except FileNotFoundError:
            return ""
    
    def save_conversation(self, output_path: str):
        """
        Save conversation history to JSON.
        
        Args:
            output_path: Path to save conversation
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def load_conversation(self, input_path: str):
        """
        Load conversation history from JSON.
        
        Args:
            input_path: Path to load conversation from
        """
        if os.path.exists(input_path):
            with open(input_path, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
    
    def clear_cache(self):
        """Clear GPU cache to free memory."""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


# Example usage for orchestrator-app
if __name__ == "__main__":
    # Initialize orchestrator
    orchestrator = MistralOrchestrator(
        model_path="./models/mistral-7b-continuity",  # Path to fine-tuned model
    )
    
    # Load session context
    context = orchestrator.load_session_context("../../SESSION_BRIEFING.md")
    
    # Interactive loop
    print("Mistral Orchestrator Ready!")
    print("Type 'quit' to exit, 'clear' to clear conversation\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'clear':
            orchestrator.conversation_history = []
            orchestrator.clear_cache()
            print("Conversation cleared!")
            continue
        
        if not user_input:
            continue
        
        # Generate response
        response = orchestrator.generate_response(user_input, context)
        print(f"\nAssistant: {response}\n")
    
    # Save conversation
    orchestrator.save_conversation("conversation_history.json")
    print("Conversation saved!")
