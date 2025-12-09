#!/usr/bin/env python3
"""
Convert fine-tuned Mistral model to GGUF format for mobile deployment.

This script converts the PyTorch model to GGUF format that can be used
with llama.cpp on Android devices.

Requirements:
- llama.cpp repository cloned
- convert.py from llama.cpp

Usage:
    python convert_to_gguf.py \
        --model ./models/mistral-7b-continuity \
        --output ./models/mistral-7b-continuity.gguf
"""

import argparse
import subprocess
import os
import sys


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert Mistral model to GGUF format"
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Path to fine-tuned model directory",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output path for GGUF file",
    )
    parser.add_argument(
        "--llama-cpp-path",
        type=str,
        default="../llama.cpp",
        help="Path to llama.cpp repository",
    )
    parser.add_argument(
        "--quantize",
        type=str,
        choices=["Q4_K_M", "Q4_0", "Q5_K_M", "Q8_0"],
        default="Q4_K_M",
        help="Quantization method (default: Q4_K_M for mobile)",
    )
    return parser.parse_args()


def check_llama_cpp(llama_cpp_path):
    """Check if llama.cpp is available.
    
    Returns:
        tuple: (convert_script_path, quantize_binary_path) on success
        
    Raises:
        RuntimeError: If llama.cpp is not properly set up
    """
    convert_script = os.path.join(llama_cpp_path, "convert.py")
    quantize_binary = os.path.join(llama_cpp_path, "quantize")
    
    if not os.path.exists(convert_script):
        print(f"Error: convert.py not found at {convert_script}")
        print("\nTo setup llama.cpp:")
        print("  git clone https://github.com/ggerganov/llama.cpp")
        print("  cd llama.cpp")
        print("  make")
        raise RuntimeError("llama.cpp not found or not properly set up")
    
    return convert_script, quantize_binary


def convert_to_gguf(model_path, output_path, convert_script):
    """Convert model to GGUF format."""
    print(f"Converting {model_path} to GGUF format...")
    
    cmd = [
        sys.executable,
        convert_script,
        model_path,
        "--outfile", output_path,
        "--outtype", "f16",
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=True)
    
    if result.returncode != 0:
        raise RuntimeError("Conversion failed")
    
    print(f"✓ Converted to {output_path}")
    return output_path


def quantize_model(input_path, output_path, quantize_binary, method):
    """Quantize GGUF model."""
    print(f"Quantizing to {method}...")
    
    # Remove .gguf extension and add quantization suffix
    base_path = output_path.replace(".gguf", "")
    quantized_path = f"{base_path}-{method.lower()}.gguf"
    
    cmd = [
        quantize_binary,
        input_path,
        quantized_path,
        method,
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=True)
    
    if result.returncode != 0:
        raise RuntimeError("Quantization failed")
    
    print(f"✓ Quantized model saved to {quantized_path}")
    
    # Print file sizes
    original_size = os.path.getsize(input_path) / (1024**3)
    quantized_size = os.path.getsize(quantized_path) / (1024**3)
    reduction = ((original_size - quantized_size) / original_size) * 100
    
    print(f"\nFile sizes:")
    print(f"  Original:  {original_size:.2f} GB")
    print(f"  Quantized: {quantized_size:.2f} GB")
    print(f"  Reduction: {reduction:.1f}%")
    
    return quantized_path


def main():
    """Main conversion function."""
    args = parse_args()
    
    # Check llama.cpp
    try:
        convert_script, quantize_binary = check_llama_cpp(args.llama_cpp_path)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Convert to GGUF
    gguf_path = convert_to_gguf(
        args.model,
        args.output,
        convert_script,
    )
    
    # Quantize
    quantized_path = quantize_model(
        gguf_path,
        args.output,
        quantize_binary,
        args.quantize,
    )
    
    print("\n✓ Conversion complete!")
    print(f"\nQuantized model ready for mobile deployment:")
    print(f"  {quantized_path}")
    print("\nNext steps:")
    print("  1. Copy model to Android device")
    print("  2. Update MobileOrchestrator.tsx with model path")
    print("  3. Build and deploy Android app")


if __name__ == "__main__":
    main()
