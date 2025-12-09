#!/bin/bash
# Deploy Mistral orchestrator to local machine (Windows/Linux)
# Optimized for RTX 2080 with 8GB VRAM

set -e

echo "=== Mistral Orchestrator Deployment ==="
echo "Target: Local Machine (RTX 2080 - 8GB VRAM)"
echo ""

# Configuration
MODEL_NAME="mistralai/Mistral-7B-v0.1"
OUTPUT_DIR="./models/mistral-7b-continuity"
TRAINING_DATA="../training-data/continuity_dataset.json"

# Check if running on Windows (Git Bash/WSL) or Linux
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    PYTHON="python"
else
    PYTHON="python3"
fi

# Step 1: Check CUDA availability
echo "Step 1: Checking CUDA availability..."
$PYTHON -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')" || {
    echo "Error: PyTorch not installed or CUDA not available"
    echo "Please install PyTorch with CUDA support first"
    exit 1
}

# Step 2: Install dependencies
echo ""
echo "Step 2: Installing dependencies..."
pip install -r ../requirements.txt

# Step 3: Generate training data
echo ""
echo "Step 3: Generating training data..."
if [ ! -f "$TRAINING_DATA" ]; then
    $PYTHON ../training-data/generate_training_data.py --output "$TRAINING_DATA"
else
    echo "Training data already exists: $TRAINING_DATA"
fi

# Step 4: Fine-tune model
echo ""
echo "Step 4: Fine-tuning Mistral 7B with QLoRA..."
echo "This will take several hours depending on your hardware."
echo "Press Ctrl+C to cancel, or wait 5 seconds to continue..."
sleep 5

$PYTHON ../fine-tuning/train_mistral_qlora.py \
    --model_name "$MODEL_NAME" \
    --data_path "$TRAINING_DATA" \
    --output_dir "$OUTPUT_DIR" \
    --num_epochs 3 \
    --batch_size 4 \
    --gradient_accumulation_steps 4 \
    --learning_rate 2e-4 \
    --max_seq_length 2048 \
    --lora_r 64 \
    --lora_alpha 16

# Step 5: Test model
echo ""
echo "Step 5: Testing fine-tuned model..."
$PYTHON -c "
from ai_orchestrator import MistralOrchestrator

orch = MistralOrchestrator(model_path='$OUTPUT_DIR')
response = orch.generate_response('What is continuity theory?')
print('Test Response:', response)
"

# Step 6: Create startup script
echo ""
echo "Step 6: Creating startup script..."
cat > start_orchestrator.sh << 'EOF'
#!/bin/bash
# Start Orchestrator API Server
python orchestrator_api.py --host 127.0.0.1 --port 5000
EOF
chmod +x start_orchestrator.sh

# Windows batch file
cat > start_orchestrator.bat << 'EOF'
@echo off
REM Start Orchestrator API Server
python orchestrator_api.py --host 127.0.0.1 --port 5000
pause
EOF

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "Model saved to: $OUTPUT_DIR"
echo ""
echo "To start the orchestrator:"
echo "  Linux/Mac: ./start_orchestrator.sh"
echo "  Windows:   start_orchestrator.bat"
echo ""
echo "API will be available at: http://127.0.0.1:5000"
echo ""
echo "Endpoints:"
echo "  POST /chat - Generate chat response"
echo "  POST /chat/stream - Streaming response"
echo "  GET /conversation - Get conversation history"
echo "  GET /health - Health check"
echo ""
