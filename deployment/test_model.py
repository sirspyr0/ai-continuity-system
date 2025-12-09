#!/usr/bin/env python3
"""
Test fine-tuned Mistral model with continuity-focused prompts.

Usage:
    python test_model.py --model ./models/mistral-7b-continuity
"""

import argparse
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'orchestrator-app'))

from ai_orchestrator import MistralOrchestrator


TEST_PROMPTS = [
    "What is continuity theory?",
    "Explain the four-tier handoff system.",
    "How should an AI instance begin work when it starts fresh?",
    "What should be included in a SESSION_LOG.md entry?",
    "How do you maintain context across AI instances?",
]


def test_model(model_path: str, interactive: bool = False):
    """Test model with predefined or interactive prompts."""
    print("Loading model...")
    print(f"Model path: {model_path}\n")
    
    try:
        orch = MistralOrchestrator(model_path=model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return False
    
    print("Model loaded successfully!\n")
    print("=" * 80)
    
    if interactive:
        print("Interactive mode - Type 'quit' to exit\n")
        while True:
            prompt = input("\nYou: ").strip()
            if prompt.lower() in ['quit', 'exit', 'q']:
                break
            
            if not prompt:
                continue
            
            print("\nAssistant: ", end="", flush=True)
            response = orch.generate_response(prompt)
            print(response)
            print("\n" + "-" * 80)
    else:
        print("Running test prompts...\n")
        for i, prompt in enumerate(TEST_PROMPTS, 1):
            print(f"\n[Test {i}/{len(TEST_PROMPTS)}]")
            print(f"Prompt: {prompt}")
            print(f"\nResponse:")
            
            response = orch.generate_response(prompt)
            print(response)
            print("\n" + "-" * 80)
    
    return True


def main():
    """Main test function."""
    parser = argparse.ArgumentParser(
        description="Test fine-tuned Mistral model"
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Path to fine-tuned model",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode",
    )
    args = parser.parse_args()
    
    if not os.path.exists(args.model):
        print(f"Error: Model not found at {args.model}")
        sys.exit(1)
    
    success = test_model(args.model, args.interactive)
    
    if not success:
        sys.exit(1)
    
    print("\n✓ Testing complete!")


if __name__ == "__main__":
    main()
