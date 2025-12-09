"""
Orchestrator API - REST API wrapper for Mistral 7B orchestrator

Provides HTTP endpoints for the Electron frontend and external clients.
Supports streaming responses for better UX.
"""

from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import json
import time
from typing import Generator
from ai_orchestrator import MistralOrchestrator

app = Flask(__name__)
CORS(app)  # Enable CORS for Electron frontend

# Initialize orchestrator (lazy loading)
orchestrator = None


def get_orchestrator() -> MistralOrchestrator:
    """Get or create orchestrator instance."""
    global orchestrator
    if orchestrator is None:
        orchestrator = MistralOrchestrator(
            model_path="./models/mistral-7b-continuity",
        )
    return orchestrator


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': orchestrator is not None,
    })


@app.route('/chat', methods=['POST'])
def chat():
    """
    Generate chat response.
    
    Request body:
    {
        "message": "User message",
        "context": "Optional system context",
        "max_tokens": 512
    }
    
    Response:
    {
        "response": "Assistant response",
        "timestamp": "ISO timestamp"
    }
    """
    data = request.json
    user_message = data.get('message', '')
    system_context = data.get('context', '')
    max_tokens = data.get('max_tokens', 512)
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        orch = get_orchestrator()
        response = orch.generate_response(
            user_message,
            system_context,
            max_tokens,
        )
        
        return jsonify({
            'response': response,
            'timestamp': time.time(),
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/chat/stream', methods=['POST'])
def chat_stream():
    """
    Generate streaming chat response.
    
    Request body same as /chat
    
    Response: Server-Sent Events (SSE) stream
    """
    data = request.json
    user_message = data.get('message', '')
    system_context = data.get('context', '')
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    def generate() -> Generator[str, None, None]:
        """Generate streaming response."""
        try:
            orch = get_orchestrator()
            
            # Format prompt
            prompt = orch.format_prompt(user_message, system_context)
            
            # Tokenize
            inputs = orch.tokenizer(prompt, return_tensors="pt").to(orch.model.device)
            
            # Generate with streaming
            from transformers import TextIteratorStreamer
            from threading import Thread
            
            streamer = TextIteratorStreamer(
                orch.tokenizer,
                skip_special_tokens=True,
            )
            
            generation_kwargs = dict(
                inputs,
                streamer=streamer,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
            )
            
            thread = Thread(target=orch.model.generate, kwargs=generation_kwargs)
            thread.start()
            
            # Stream tokens
            full_response = ""
            for token in streamer:
                full_response += token
                yield f"data: {json.dumps({'token': token})}\n\n"
            
            # Update history
            orch.conversation_history.append({
                'role': 'user',
                'content': user_message,
            })
            orch.conversation_history.append({
                'role': 'assistant',
                'content': full_response.strip(),
            })
            
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
    )


@app.route('/conversation', methods=['GET'])
def get_conversation():
    """Get current conversation history."""
    orch = get_orchestrator()
    return jsonify({
        'history': orch.conversation_history,
        'turn_count': len(orch.conversation_history),
    })


@app.route('/conversation', methods=['DELETE'])
def clear_conversation():
    """Clear conversation history."""
    orch = get_orchestrator()
    orch.conversation_history = []
    orch.clear_cache()
    return jsonify({'status': 'cleared'})


@app.route('/conversation/save', methods=['POST'])
def save_conversation():
    """Save conversation to file."""
    data = request.json
    path = data.get('path', 'conversation_history.json')
    
    try:
        orch = get_orchestrator()
        orch.save_conversation(path)
        return jsonify({'status': 'saved', 'path': path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/conversation/load', methods=['POST'])
def load_conversation():
    """Load conversation from file."""
    data = request.json
    path = data.get('path', 'conversation_history.json')
    
    try:
        orch = get_orchestrator()
        orch.load_conversation(path)
        return jsonify({
            'status': 'loaded',
            'path': path,
            'turn_count': len(orch.conversation_history),
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/context/load', methods=['POST'])
def load_context():
    """Load context from SESSION_BRIEFING.md or other file."""
    data = request.json
    path = data.get('path', 'SESSION_BRIEFING.md')
    
    try:
        orch = get_orchestrator()
        context = orch.load_session_context(path)
        return jsonify({
            'status': 'loaded',
            'path': path,
            'context_length': len(context),
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/model/info', methods=['GET'])
def model_info():
    """Get model information."""
    orch = get_orchestrator()
    
    import torch
    
    return jsonify({
        'model_path': orch.model_path,
        'max_memory_gb': orch.max_memory_gb,
        'device': str(orch.model.device) if hasattr(orch.model, 'device') else 'unknown',
        'cuda_available': torch.cuda.is_available(),
        'cuda_memory_allocated': torch.cuda.memory_allocated() / 1e9 if torch.cuda.is_available() else 0,
        'cuda_memory_reserved': torch.cuda.memory_reserved() / 1e9 if torch.cuda.is_available() else 0,
    })


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Orchestrator API Server')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    print(f"Starting Orchestrator API on {args.host}:{args.port}")
    print("Endpoints:")
    print("  POST /chat - Generate chat response")
    print("  POST /chat/stream - Generate streaming chat response")
    print("  GET  /conversation - Get conversation history")
    print("  DELETE /conversation - Clear conversation history")
    print("  GET  /health - Health check")
    print("  GET  /model/info - Model information")
    
    app.run(host=args.host, port=args.port, debug=args.debug)
