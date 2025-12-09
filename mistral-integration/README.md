# Mistral 7B Orchestrator Integration

Integration of fine-tuned Mistral 7B across the orchestrator ecosystem (desktop, VPS, Android) with continuity awareness.

## 🚀 Quick Start

```bash
# 1. Generate training data
cd training-data
python generate_training_data.py --output continuity_dataset.json

# 2. Fine-tune Mistral 7B
cd ../fine-tuning
python train_mistral_qlora.py \
    --data_path ../training-data/continuity_dataset.json \
    --output_dir ./models/mistral-7b-continuity

# 3. Deploy to desktop
cd ../orchestrator-app
python orchestrator_api.py --port 5000

# 4. Deploy to VPS
cd ../orchestrator-vps
bash ../deployment/deploy_vps.sh

# 5. Build Android app
# See assistant-mobile/MOBILE_INTEGRATION.md
```

## 📁 Project Structure

```
mistral-integration/
├── fine-tuning/              # QLoRA fine-tuning pipeline
│   ├── train_mistral_qlora.py
│   └── models/               # Output directory for models
├── training-data/            # Training dataset
│   ├── generate_training_data.py
│   └── continuity_dataset.json
├── orchestrator-app/         # Desktop Electron integration
│   ├── ai_orchestrator.py
│   └── orchestrator_api.py
├── orchestrator-vps/         # VPS server integration
│   └── orchestrator_api.py
├── assistant-mobile/         # Android React Native integration
│   ├── MOBILE_INTEGRATION.md
│   └── MobileOrchestrator.tsx
├── deployment/               # Deployment scripts
│   ├── deploy_local.sh
│   └── deploy_vps.sh
├── docs/                     # Documentation
│   └── COMPLETE_GUIDE.md
└── requirements.txt          # Python dependencies
```

## 🎯 Features

### Fine-Tuning
- ✅ 4-bit quantization with QLoRA
- ✅ Optimized for 8GB VRAM (RTX 2080)
- ✅ Training on continuity principles
- ✅ Context-aware handoff system
- ✅ Weights & Biases integration (optional)

### Desktop Orchestrator
- ✅ Mistral 7B with 4-bit quantization
- ✅ REST API with streaming support
- ✅ Conversation history management
- ✅ Session context integration
- ✅ GPU memory optimization

### VPS Orchestrator
- ✅ CPU and GPU support
- ✅ Systemd service
- ✅ Nginx reverse proxy
- ✅ Auto-restart on failure
- ✅ Remote API access

### Mobile Assistant
- ✅ On-device inference (Phi-3/Mistral)
- ✅ LAN-first sync with desktop
- ✅ Fallback to VPS
- ✅ React Native/Expo
- ✅ Conflict-free synchronization

## 📊 Hardware Requirements

| Component | CPU | GPU | RAM | Storage |
|-----------|-----|-----|-----|---------|
| Desktop | i9-9900K | RTX 2080 (8GB) | 56GB | 50GB |
| VPS | 8+ cores | Optional (8GB+) | 16GB | 50GB |
| Android | ARM64 | - | 6GB | 4GB |

## 📖 Documentation

- **[Complete Guide](docs/COMPLETE_GUIDE.md)** - Full documentation with usage, troubleshooting, and maintenance
- **[Mobile Integration](assistant-mobile/MOBILE_INTEGRATION.md)** - Android-specific instructions

## 🔧 Installation

### Prerequisites
- Python 3.8+
- CUDA 11.8+ (for GPU)
- PyTorch 2.0+

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Verify Installation
```bash
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

## 🎓 Training

### Generate Dataset
```bash
cd training-data
python generate_training_data.py --output continuity_dataset.json
```

**Dataset includes:**
- Continuity theory principles
- Four-tier handoff system
- Architecture understanding
- Practical scenarios

### Fine-Tune Model
```bash
cd fine-tuning
python train_mistral_qlora.py \
    --model_name mistralai/Mistral-7B-v0.1 \
    --data_path ../training-data/continuity_dataset.json \
    --output_dir ./models/mistral-7b-continuity \
    --num_epochs 3 \
    --batch_size 4
```

**Training time:** ~2-4 hours on RTX 2080

## 🚢 Deployment

### Desktop (Local)
```bash
cd deployment
bash deploy_local.sh
```

Then start the API:
```bash
cd ../orchestrator-app
python orchestrator_api.py --host 127.0.0.1 --port 5000
```

### VPS (Remote)
```bash
# Upload model to VPS
scp -r fine-tuning/models/mistral-7b-continuity user@vps:/path/to/models/

# On VPS
cd deployment
bash deploy_vps.sh
```

### Android (Mobile)
See [assistant-mobile/MOBILE_INTEGRATION.md](assistant-mobile/MOBILE_INTEGRATION.md)

## 🌐 API Usage

### Desktop API

**Chat:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is continuity theory?"}'
```

**Streaming:**
```bash
curl -X POST http://localhost:5000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain the handoff system"}' \
  --no-buffer
```

### VPS API

**Generate:**
```bash
curl -X POST http://your-vps-ip/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "[INST] What is continuity? [/INST]"}'
```

### Python SDK

```python
from ai_orchestrator import MistralOrchestrator

orch = MistralOrchestrator(model_path="./models/mistral-7b-continuity")
response = orch.generate_response("What is the four-tier handoff system?")
print(response)
```

## 🔍 Troubleshooting

### Out of Memory
- Reduce batch size: `--batch_size 2`
- Reduce sequence length: `--max_seq_length 1024`
- Clear GPU cache periodically

### Slow Inference
- Enable 4-bit quantization
- Use GPU for desktop/VPS
- Use smaller model for mobile (Phi-3 Mini)

### Connection Issues
- Check firewall settings (port 5000)
- Verify API is running
- Check network connectivity

See [Complete Guide](docs/COMPLETE_GUIDE.md) for detailed troubleshooting.

## 📈 Performance

| Platform | Hardware | Time (512 tokens) | Throughput |
|----------|----------|-------------------|------------|
| Desktop | RTX 2080 (4-bit) | ~2-3s | 170-250 tok/s |
| VPS (GPU) | T4 (4-bit) | ~1-2s | 250-350 tok/s |
| VPS (CPU) | 8 cores | ~8-12s | 40-60 tok/s |
| Mobile | ARM64 (Phi-3) | ~10-15s | 17-25 tok/s |

## 🧪 Testing

```bash
# Test desktop orchestrator
cd orchestrator-app
python -c "
from ai_orchestrator import MistralOrchestrator
orch = MistralOrchestrator(model_path='../fine-tuning/models/mistral-7b-continuity')
print(orch.generate_response('Test question'))
"

# Test VPS API
curl http://localhost:5000/health

# Test mobile sync
# See mobile app testing section
```

## 🤝 Integration with AI Continuity System

This integration follows the AI Continuity System principles:

- **SESSION_BRIEFING.md** - Quick context for fresh instances
- **SESSION_LOG.md** - Detailed work history
- **PROJECT_CONTEXT.md** - Architecture and decisions
- **PORTFOLIO_CONTEXT.md** - Ecosystem view

The model is trained to understand and maintain these documents.

## 📝 Maintenance

### Weekly
- Review conversation logs
- Monitor GPU memory usage
- Check API error rates

### Monthly
- Re-train with expanded dataset
- Update dependencies
- Backup model checkpoints

### Backups
```bash
# Backup model
tar -czf mistral-continuity-backup.tar.gz fine-tuning/models/

# Backup conversations
cp orchestrator-app/conversation_history.json backups/
```

## 🔗 References

- [Mistral AI](https://mistral.ai/)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [Transformers Library](https://huggingface.co/docs/transformers/)
- [AI Continuity System](https://github.com/sirspyr0/ai-continuity-system)

## 📄 License

See [LICENSE](../LICENSE) in repository root.

## 🐛 Issues & Support

For issues, questions, or contributions:
1. Check [Complete Guide](docs/COMPLETE_GUIDE.md)
2. Review [Troubleshooting](#troubleshooting)
3. Open GitHub issue with details

## 🙏 Acknowledgments

- Mistral AI for the base model
- Hugging Face for transformers and PEFT
- The AI Continuity System research project
