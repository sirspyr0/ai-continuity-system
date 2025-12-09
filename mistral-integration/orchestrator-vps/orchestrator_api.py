"""
VPS Orchestrator API - Remote server for orchestrator ecosystem

Provides remote AI capabilities and backup processing for the orchestrator system.
Optimized for CPU or cloud GPU instances.
"""

from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    pipeline,
)
import json
import time
import os
from typing import List, Dict, Optional

app = Flask(__name__)
CORS(app)

# Global orchestrator instance
orchestrator = None


class VPSOrchestrator:
    """VPS orchestrator optimized for server deployment."""
    
    def __init__(
        self,
        model_path: str,
        use_gpu: bool = True,
        quantize: bool = True,
    ):
        """
        Initialize VPS orchestrator.
        
        Args:
            model_path: Path to fine-tuned model
            use_gpu: Whether to use GPU (if available)
            quantize: Whether to use quantization
        """
        self.model_path = model_path
        self.use_gpu = use_gpu and torch.cuda.is_available()
        self.quantize = quantize
        
        self._load_model()
        
    def _load_model(self):
        """Load model with appropriate configuration for VPS."""
        print(f"Loading model from {self.model_path}...")
        print(f"Using GPU: {self.use_gpu}, Quantization: {self.quantize}")
        
        if self.use_gpu and self.quantize:
            # Use 4-bit quantization on GPU
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
            )
        elif self.use_gpu:
            # Use full precision on GPU
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                device_map="auto",
                torch_dtype=torch.float16,
                trust_remote_code=True,
            )
        else:
            # CPU inference
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                device_map="cpu",
                torch_dtype=torch.float32,
                trust_remote_code=True,
            )
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            trust_remote_code=True,
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
        )
        
        print("Model loaded successfully!")
    
    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 512,
    ) -> str:
        """Generate response to prompt."""
        outputs = self.pipe(
            prompt,
            max_new_tokens=max_new_tokens,
            return_full_text=False,
        )
        return outputs[0]['generated_text'].strip()


def get_orchestrator() -> VPSOrchestrator:
    """Get or create orchestrator instance."""
    global orchestrator
    if orchestrator is None:
        model_path = os.environ.get(
            'MODEL_PATH',
            './models/mistral-7b-continuity'
        )
        use_gpu = os.environ.get('USE_GPU', 'true').lower() == 'true'
        quantize = os.environ.get('QUANTIZE', 'true').lower() == 'true'
        
        orchestrator = VPSOrchestrator(
            model_path=model_path,
            use_gpu=use_gpu,
            quantize=quantize,
        )
    return orchestrator


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': orchestrator is not None,
        'gpu_available': torch.cuda.is_available(),
    })


@app.route('/generate', methods=['POST'])
def generate():
    """
    Generate response to prompt.
    
    Request body:
    {
        "prompt": "Formatted prompt",
        "max_tokens": 512
    }
    """
    data = request.json
    prompt = data.get('prompt', '')
    max_tokens = data.get('max_tokens', 512)
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    try:
        orch = get_orchestrator()
        response = orch.generate(prompt, max_tokens)
        
        return jsonify({
            'response': response,
            'timestamp': time.time(),
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/info', methods=['GET'])
def info():
    """Get server and model information."""
    orch = get_orchestrator()
    
    info_dict = {
        'model_path': orch.model_path,
        'use_gpu': orch.use_gpu,
        'quantize': orch.quantize,
        'cuda_available': torch.cuda.is_available(),
    }
    
    if torch.cuda.is_available():
        info_dict.update({
            'cuda_device_count': torch.cuda.device_count(),
            'cuda_device_name': torch.cuda.get_device_name(0),
            'cuda_memory_allocated': torch.cuda.memory_allocated() / 1e9,
            'cuda_memory_reserved': torch.cuda.memory_reserved() / 1e9,
        })
    
    return jsonify(info_dict)


@app.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Clear GPU cache."""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        return jsonify({'status': 'cleared'})
    return jsonify({'status': 'no_gpu'})


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='VPS Orchestrator API')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--workers', type=int, default=1, help='Number of workers')
    args = parser.parse_args()
    
    print(f"Starting VPS Orchestrator API on {args.host}:{args.port}")
    print("Environment variables:")
    print(f"  MODEL_PATH: {os.environ.get('MODEL_PATH', './models/mistral-7b-continuity')}")
    print(f"  USE_GPU: {os.environ.get('USE_GPU', 'true')}")
    print(f"  QUANTIZE: {os.environ.get('QUANTIZE', 'true')}")
    
    # For production, use gunicorn:
    # gunicorn -w 4 -b 0.0.0.0:5000 orchestrator_api:app
    
    app.run(host=args.host, port=args.port, debug=False)
