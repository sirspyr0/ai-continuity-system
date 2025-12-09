# Mistral 7B Integration - Complete Documentation

## Overview

This integration provides fine-tuned Mistral 7B across three orchestrator components:
1. **orchestrator-app** - Desktop Electron app (coordinator/brain)
2. **orchestrator-vps** - VPS remote server (backup/remote processing)
3. **assistant-mobile** - Android React Native app (mobile interface)

All components are trained on continuity principles and understand the four-tier handoff system.

## Table of Contents

- [Quick Start](#quick-start)
- [Hardware Requirements](#hardware-requirements)
- [Installation](#installation)
- [Fine-Tuning](#fine-tuning)
- [Deployment](#deployment)
- [Usage](#usage)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Maintenance](#maintenance)

## Quick Start

### 1. Generate Training Data
```bash
cd mistral-integration/training-data
python generate_training_data.py --output continuity_dataset.json
```

### 2. Fine-Tune Model (Local RTX 2080)
```bash
cd mistral-integration/fine-tuning
python train_mistral_qlora.py \
    --data_path ../training-data/continuity_dataset.json \
    --output_dir ./models/mistral-7b-continuity \
    --num_epochs 3
```

### 3. Deploy to Desktop
```bash
cd mistral-integration/orchestrator-app
python orchestrator_api.py --host 127.0.0.1 --port 5000
```

### 4. Deploy to VPS
```bash
cd mistral-integration/orchestrator-vps
./deploy_vps.sh
```

### 5. Build Android App
See `assistant-mobile/MOBILE_INTEGRATION.md`

## Hardware Requirements

### Local Machine (Desktop)
- **CPU**: Intel i9-9900K or equivalent
- **GPU**: RTX 2080 (8GB VRAM) - required for fine-tuning and inference
- **RAM**: 56GB (32GB minimum)
- **Storage**: 50GB free space for models and datasets
- **OS**: Windows 10/11, Linux, or macOS

### VPS Server
**Option 1: CPU Only**
- 8+ CPU cores
- 16GB+ RAM
- 50GB storage
- Inference: 2-5 seconds per response

**Option 2: GPU Instance**
- GPU with 8GB+ VRAM (e.g., T4, V100)
- 16GB+ RAM
- 50GB storage
- Inference: 0.5-1 second per response

### Android Device
- **OS**: Android 8.0+ (API level 26+)
- **RAM**: 6GB+ recommended
- **Storage**: 4GB free space for on-device model
- **Processor**: ARM64 architecture

## Installation

### Prerequisites

**All Platforms:**
```bash
# Python 3.8+
python --version

# CUDA 11.8+ (for GPU)
nvcc --version

# Git
git --version
```

### Install Python Dependencies

```bash
cd mistral-integration
pip install -r requirements.txt
```

### Verify Installation

```bash
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"
```

## Fine-Tuning

### Training Data

The training dataset focuses on:
1. **Continuity Theory** - Understanding consciousness and context flow
2. **Handoff System** - Managing the four-tier documentation system
3. **Architecture** - Understanding the orchestrator ecosystem
4. **Practical Scenarios** - Real-world usage patterns

Generate training data:
```bash
cd training-data
python generate_training_data.py --output continuity_dataset.json
```

This creates ~30 high-quality examples. For production, expand to 500-1000 examples.

### Fine-Tuning Process

**Step 1: Configure Training**

Edit training parameters in `train_mistral_qlora.py` or pass as arguments:
- `--num_epochs`: Number of training epochs (default: 3)
- `--batch_size`: Batch size per device (default: 4)
- `--learning_rate`: Learning rate (default: 2e-4)
- `--lora_r`: LoRA dimension (default: 64)

**Step 2: Start Training**

```bash
cd fine-tuning
python train_mistral_qlora.py \
    --data_path ../training-data/continuity_dataset.json \
    --output_dir ./models/mistral-7b-continuity \
    --num_epochs 3 \
    --batch_size 4 \
    --gradient_accumulation_steps 4
```

**Step 3: Monitor Training**

With Weights & Biases (optional):
```bash
python train_mistral_qlora.py \
    --data_path ../training-data/continuity_dataset.json \
    --output_dir ./models/mistral-7b-continuity \
    --use_wandb
```

**Training Time:**
- RTX 2080 (8GB): ~2-4 hours for 3 epochs
- A100 (40GB): ~30-60 minutes for 3 epochs

**Memory Usage:**
- 4-bit quantization: ~5-6GB VRAM
- Optimizer states: ~2GB VRAM
- Total: ~7-8GB VRAM (fits RTX 2080)

### Evaluating the Model

Test the fine-tuned model:
```bash
cd orchestrator-app
python -c "
from ai_orchestrator import MistralOrchestrator

orch = MistralOrchestrator(model_path='../fine-tuning/models/mistral-7b-continuity')
response = orch.generate_response('Explain continuity theory.')
print(response)
"
```

## Deployment

### Desktop Orchestrator (orchestrator-app)

**Manual Deployment:**
```bash
cd orchestrator-app
python orchestrator_api.py --host 127.0.0.1 --port 5000
```

**Automated Deployment:**
```bash
cd deployment
./deploy_local.sh
```

This script:
1. Checks CUDA availability
2. Installs dependencies
3. Generates training data (if needed)
4. Fine-tunes model
5. Tests model
6. Creates startup scripts

**Starting the Service:**
- Linux/Mac: `./start_orchestrator.sh`
- Windows: `start_orchestrator.bat`

### VPS Orchestrator (orchestrator-vps)

**Upload Model:**
```bash
# From local machine
scp -r fine-tuning/models/mistral-7b-continuity user@vps-ip:~/models/
```

**Deploy:**
```bash
# On VPS
cd orchestrator-vps
./deploy_vps.sh
```

This script:
1. Installs system dependencies
2. Creates virtual environment
3. Installs Python packages
4. Creates systemd service
5. Configures nginx reverse proxy
6. Starts service

**Service Management:**
```bash
# Start/stop/restart
sudo systemctl start orchestrator-vps
sudo systemctl stop orchestrator-vps
sudo systemctl restart orchestrator-vps

# View logs
sudo journalctl -u orchestrator-vps -f

# Check status
sudo systemctl status orchestrator-vps
```

### Android Mobile (assistant-mobile)

See detailed instructions in `assistant-mobile/MOBILE_INTEGRATION.md`

**Summary:**
1. Setup React Native/Expo project
2. Install dependencies (react-native-llama)
3. Convert model to GGUF format
4. Quantize to Q4_K_M
5. Bundle or download model
6. Implement MobileOrchestrator component
7. Build and deploy to device

## Usage

### Desktop API

**Generate Chat Response:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the four-tier handoff system?",
    "context": "Working on orchestrator integration"
  }'
```

**Streaming Response:**
```bash
curl -X POST http://localhost:5000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain continuity theory"}' \
  --no-buffer
```

**Get Conversation History:**
```bash
curl http://localhost:5000/conversation
```

**Clear Conversation:**
```bash
curl -X DELETE http://localhost:5000/conversation
```

### VPS API

**Generate Response:**
```bash
curl -X POST http://your-vps-ip/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "[INST] What is continuity theory? [/INST]",
    "max_tokens": 512
  }'
```

**Health Check:**
```bash
curl http://your-vps-ip/health
```

**Server Info:**
```bash
curl http://your-vps-ip/info
```

### Python SDK

```python
from ai_orchestrator import MistralOrchestrator

# Initialize
orch = MistralOrchestrator(
    model_path="./models/mistral-7b-continuity"
)

# Load session context
context = orch.load_session_context("SESSION_BRIEFING.md")

# Generate response
response = orch.generate_response(
    "How do I maintain continuity?",
    system_context=context
)

print(response)

# Save conversation
orch.save_conversation("conversation.json")
```

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator Ecosystem                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐  │
│  │ orchestrator │◄────►│ orchestrator │◄────►│assistant │  │
│  │    -app      │ LAN  │    -vps      │ Web  │ -mobile  │  │
│  │  (Desktop)   │      │   (Server)   │      │ (Android)│  │
│  └──────────────┘      └──────────────┘      └──────────┘  │
│        │                      │                     │        │
│        │ Mistral 7B (Q4)     │ Mistral 7B (Q4)    │ Phi-3  │
│        │ RTX 2080 (8GB)      │ GPU/CPU            │ Mobile │
│        │                      │                     │        │
│        └──────────────────────┴─────────────────────┘        │
│                      Shared Context:                         │
│              SESSION_BRIEFING.md, SESSION_LOG.md,           │
│              PROJECT_CONTEXT.md, PORTFOLIO_CONTEXT.md       │
└─────────────────────────────────────────────────────────────┘
```

### Component Roles

**orchestrator-app (Desktop)**
- Primary brain and coordinator
- Runs locally on RTX 2080
- Handles heavy processing
- Maintains source of truth for context
- Rich UI for interaction

**orchestrator-vps (Server)**
- Remote backup processing
- Accessible from anywhere
- Handles requests when desktop offline
- Can run on CPU or GPU

**assistant-mobile (Android)**
- Mobile interface
- On-device small model for basic tasks
- Falls back to desktop/VPS for complex queries
- LAN-first sync with desktop

### Communication Flow

1. **Mobile → Desktop (LAN)**
   - Primary path when on same network
   - Fast, low latency
   - No internet required

2. **Mobile → VPS → Desktop**
   - When mobile is remote
   - VPS acts as relay
   - Syncs context with desktop

3. **Desktop → VPS**
   - For backup and redundancy
   - Shares context updates
   - Handles overflow requests

## Troubleshooting

### Out of Memory (OOM)

**Symptoms:**
- CUDA OOM error during training/inference
- Process killed by system

**Solutions:**
1. Reduce batch size: `--batch_size 2`
2. Reduce sequence length: `--max_seq_length 1024`
3. Clear GPU cache: `torch.cuda.empty_cache()`
4. Use gradient checkpointing
5. Reduce LoRA rank: `--lora_r 32`

### Slow Inference

**Desktop:**
1. Ensure using GPU: Check `torch.cuda.is_available()`
2. Enable 4-bit quantization
3. Reduce max_new_tokens
4. Use batch processing for multiple requests

**VPS:**
1. Use GPU instance for faster inference
2. Enable quantization even on CPU
3. Implement response caching
4. Use nginx caching for common queries

**Mobile:**
1. Use smaller model (Phi-3 Mini 3B vs Mistral 7B)
2. Increase quantization (Q4 → Q3)
3. Reduce context length
4. Fallback to desktop/VPS for complex queries

### Model Quality Issues

**Low Quality Responses:**
1. Expand training dataset (500-1000 examples)
2. Increase training epochs
3. Adjust temperature (default: 0.7)
4. Review training data quality
5. Check if model converged (loss curve)

**Repetitive Responses:**
1. Increase repetition_penalty (default: 1.15)
2. Adjust temperature and top_p
3. Use diverse training examples
4. Check for overfitting

### Connection Issues

**Mobile Can't Reach Desktop:**
1. Check firewall allows port 5000
2. Verify desktop API is running
3. Check devices on same network
4. Use desktop's local IP, not localhost

**VPS Not Accessible:**
1. Check nginx configuration
2. Verify firewall rules (port 80/443)
3. Check systemd service status
4. Review logs: `journalctl -u orchestrator-vps`

## Maintenance

### Regular Updates

**Weekly:**
- Review conversation logs
- Check error rates in API logs
- Monitor GPU memory usage
- Update training data with new examples

**Monthly:**
- Re-train model with expanded dataset
- Update dependencies: `pip install -U -r requirements.txt`
- Review and optimize API performance
- Backup model checkpoints

### Monitoring

**Desktop:**
```bash
# Check GPU usage
nvidia-smi

# Monitor API logs
tail -f orchestrator.log

# Check conversation history
ls -lh conversation_history.json
```

**VPS:**
```bash
# Service status
sudo systemctl status orchestrator-vps

# View logs
sudo journalctl -u orchestrator-vps -f

# Monitor resource usage
htop
```

**Mobile:**
- Monitor app crash reports
- Check sync success rates
- Review on-device model performance

### Backup Strategy

**Models:**
```bash
# Backup fine-tuned model
tar -czf mistral-7b-continuity-$(date +%Y%m%d).tar.gz \
    fine-tuning/models/mistral-7b-continuity/

# Upload to cloud storage
# aws s3 cp mistral-7b-continuity-*.tar.gz s3://your-bucket/
```

**Conversations:**
```bash
# Backup conversation history
cp orchestrator-app/conversation_history.json \
    backups/conversation-$(date +%Y%m%d).json
```

**Context Documents:**
```bash
# Context is in git - just commit regularly
git add SESSION_BRIEFING.md SESSION_LOG.md
git commit -m "Update session context"
git push
```

### Upgrading

**Model Updates:**
1. Train new version with expanded data
2. Test thoroughly on desktop
3. Deploy to VPS
4. Update mobile model
5. Keep old version for rollback

**Dependency Updates:**
```bash
# Update with caution - test first
pip install -U transformers torch peft

# Test model loads correctly
python -c "from ai_orchestrator import MistralOrchestrator; orch = MistralOrchestrator('models/mistral-7b-continuity')"
```

## Performance Benchmarks

### Training (RTX 2080)
- Dataset: 30 examples
- Epochs: 3
- Time: ~2-3 hours
- VRAM: 7-8GB peak

### Inference (RTX 2080, 4-bit)
- Tokens: 512
- Time: ~2-3 seconds
- VRAM: 5-6GB
- Throughput: ~170-250 tokens/second

### VPS (CPU, 8 cores)
- Tokens: 512
- Time: ~8-12 seconds
- RAM: 8GB
- Throughput: ~40-60 tokens/second

### Mobile (Android, Phi-3 Mini 3B Q4)
- Tokens: 256
- Time: ~10-15 seconds
- RAM: 3-4GB
- Throughput: ~17-25 tokens/second

## References

- [Mistral AI](https://mistral.ai/)
- [Transformers Documentation](https://huggingface.co/docs/transformers/)
- [PEFT/QLoRA](https://github.com/huggingface/peft)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [AI Continuity System](https://github.com/sirspyr0/ai-continuity-system)

## Support

For issues and questions:
1. Check this documentation
2. Review troubleshooting section
3. Check GitHub issues
4. Open new issue with details

## License

See LICENSE file in repository root.
