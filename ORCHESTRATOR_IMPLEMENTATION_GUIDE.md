# Orchestrator System: Implementation Guide

This guide provides step-by-step instructions for building and deploying the Orchestrator System from scratch, or contributing to its further development.

## Table of Contents
1. [Prerequisites & Setup](#prerequisites--setup)
2. [Component Installation](#component-installation)
3. [Model Selection & Deployment](#model-selection--deployment)
4. [Integration & Testing](#integration--testing)
5. [Extending the System](#extending-the-system)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites & Setup

### System Requirements

**Minimum**:
- 16GB RAM
- 8GB GPU VRAM (for inference) OR 32GB+ CPU RAM
- 100GB storage (for models + data)
- Linux (Ubuntu 20.04+) or Windows 10/11

**Recommended** (for production):
- 32GB+ RAM
- 24GB+ GPU VRAM (RTX 4090, A100, H100)
- 500GB+ NVMe storage
- Linux server environment

### Development Tools

```bash
# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python 3.10+
sudo apt-get install -y python3.10 python3.10-venv python3.10-dev

# Install CUDA (for GPU support)
wget https://developer.nvidia.com/download/cuda-12-1-0-x86_64-linux
bash cuda-installer.sh

# Install git
sudo apt-get install -y git

# Clone the repository
git clone https://github.com/sirspyr0/ai-continuity-system.git
cd ai-continuity-system
```

### Environment Setup

```bash
# Create Python virtual environment
python3.10 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install base requirements
pip install --upgrade pip setuptools wheel
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers accelerate bitsandbytes

# Create directories
mkdir -p models data logs
```

---

## Component Installation

### 1. Desktop Orchestrator (orchestrator-app)

**Recommended for**: Interactive AI assistance, primary development hub

#### Step 1: Install Dependencies

```bash
cd orchestrator-app
npm install
```

#### Step 2: Choose & Setup Model

**Option A: Ollama (Easiest)**
```bash
# Download and install Ollama
curl https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# In another terminal, pull a model
ollama pull qwen2.5:7b
# or
ollama pull mistral
```

**Option B: Local Fine-tune (Advanced)**
```bash
# See fine-tuning section below
cd ../fine-tuning
python train_mistral_qlora.py \
    --model_name mistralai/Mixtral-8x7B \
    --data_path ../training-data/continuity_dataset.json \
    --output_dir ./models/mistral-finetuned
```

#### Step 3: Configure Backend

Edit `ai_orchestrator.py`:
```python
# Set model endpoint
OLLAMA_ENDPOINT = "http://localhost:11434/v1/chat/completions"
MODEL_NAME = "qwen2.5:7b"  # Change based on what you pulled

# Set workspace path
DEFAULT_WORKSPACE = "C:/Users/yourname/path/to/projects"

# Configure tools
TOOLS_CONFIG = {
    'ripgrep_path': 'C:/path/to/rg.exe',  # Windows
    'python_enabled': True,
    'shell_enabled': True,
    'guardrails': True  # Block destructive commands
}
```

#### Step 4: Run Application

```bash
# Start the app
npm start

# App opens at http://localhost:3000
```

**Files Created**:
- `memory_log.jsonl`: Append-only chat history
- `SESSION_LOG.md`: Session documentation (create manually)
- `SESSION_BRIEFING.md`: Daily context (create manually)

---

### 2. VPS Orchestrator (orchestrator-vps)

**Recommended for**: Persistent hub, backup processing, remote access

#### Step 1: Server Setup

```bash
# SSH into your VPS
ssh user@your-vps-ip

# Install dependencies
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3.10 python3.10-venv git nginx supervisor

# Clone repository
git clone https://github.com/sirspyr0/ai-continuity-system.git
cd ai-continuity-system/orchestrator-vps
```

#### Step 2: Setup Python Environment

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements-mistral.txt

# Additional requirements
pip install flask flask-cors gunicorn
```

#### Step 3: Configure API

Edit `orchestrator_api.py`:
```python
# Database configuration
DB_PATH = "/home/user/orchestrator/data.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Model configuration
MODEL_PATH = "/home/user/orchestrator/models/mistral-7b"
USE_GPU = True  # Set to False for CPU-only
QUANTIZE = True  # 4-bit quantization

# API configuration
FLASK_HOST = "127.0.0.1"  # Nginx handles external traffic
FLASK_PORT = 5000
```

#### Step 4: Setup Systemd Service

Create `/etc/systemd/system/orchestrator.service`:
```ini
[Unit]
Description=Orchestrator VPS API
After=network.target

[Service]
Type=notify
User=orchestrator
WorkingDirectory=/home/orchestrator/ai-continuity-system/orchestrator-vps
Environment="PATH=/home/orchestrator/ai-continuity-system/orchestrator-vps/venv/bin"
ExecStart=/home/orchestrator/ai-continuity-system/orchestrator-vps/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:5000 \
    orchestrator_api:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable orchestrator
sudo systemctl start orchestrator
sudo systemctl status orchestrator
```

#### Step 5: Setup Nginx Reverse Proxy

Create `/etc/nginx/sites-available/orchestrator`:
```nginx
server {
    listen 80;
    server_name your-vps-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # SSL configuration (with Let's Encrypt)
    # See certbot documentation
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/orchestrator /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 6: Test API

```bash
curl -X GET http://your-vps-domain.com/health
# Should return: {"status": "healthy", ...}
```

---

### 3. Mobile Orchestrator (assistant-mobile)

**Recommended for**: Mobile access, on-device reasoning, distributed testing

#### Step 1: Setup Expo Project

```bash
cd assistant-mobile
npm install

# Setup for Android
npm install expo-dev-client
```

#### Step 2: Download On-Device Model

```bash
# Download Phi-3 Mini GGUF (quantized)
mkdir -p models
cd models

# Q4_K_M quantization (~2GB)
wget https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf

cd ..
```

#### Step 3: Configure Mobile App

Edit `MobileOrchestrator.tsx`:
```typescript
// LAN Discovery
const DESKTOP_IP = "192.168.1.100";  // Your desktop IP
const DESKTOP_PORT = 5000;
const DESKTOP_URL = `http://${DESKTOP_IP}:${DESKTOP_PORT}`;

// VPS Fallback
const VPS_URL = "https://your-vps-domain.com";

// Model paths
const LOCAL_MODEL_PATH = "../models/Phi-3-mini-q4.gguf";
const MODEL_CONTEXT_SIZE = 4096;

// Timeouts
const LAN_TIMEOUT = 5000;        // 5s for LAN
const VPS_TIMEOUT = 30000;       // 30s for cloud
```

#### Step 4: Build Android APK

```bash
# For development
npx expo start --android

# For production
eas build --platform android --profile production
```

Or manually:
```bash
# Install APK on device
adb install -r app-release.apk
```

---

## Model Selection & Deployment

### Model Comparison

| Model | Size | VRAM | Speed | Quality | License | Link |
|-------|------|------|-------|---------|---------|------|
| **Phi-3 Mini** | 3.8B | 2GB | ⚡⚡⚡ | Good | MIT | [HF Link](https://huggingface.co/microsoft/Phi-3-mini) |
| **Qwen 2.5** | 7B | 4GB | ⚡⚡ | Excellent | Apache | [HF Link](https://huggingface.co/Qwen/Qwen2.5-7B) |
| **Mistral 7B** | 7B | 4GB | ⚡⚡ | Very Good | Apache | [HF Link](https://huggingface.co/mistralai/Mistral-7B) |
| **Mixtral 8x7B** | 46B (12B active) | 6GB | ⚡⚡ | Excellent | Apache | [HF Link](https://huggingface.co/mistralai/Mixtral-8x7B) |
| **Llama 2 13B** | 13B | 8GB | ⚡ | Excellent | Meta | [HF Link](https://huggingface.co/meta-llama/Llama-2-13b) |

**Recommendations**:
- **Mobile**: Phi-3 Mini (on-device)
- **Desktop**: Qwen 2.5 or Mixtral (via Ollama)
- **VPS**: Qwen 2.5 or Llama 2 13B (CPU or GPU)
- **Best Balance**: Mixtral 8x7B (fits RTX 2080 with Q4 quantization)

### Fine-Tuning for Continuity

If you want to fine-tune a model on your continuity documents:

```bash
cd fine-tuning

# Step 1: Generate training data
python generate_training_data.py \
    --output continuity_dataset.json \
    --add-custom-examples

# Step 2: Fine-tune
python train_mistral_qlora.py \
    --model_name mistralai/Mixtral-8x7B \
    --data_path ../training-data/continuity_dataset.json \
    --output_dir ./models/mistral-continuity \
    --num_epochs 3 \
    --batch_size 4 \
    --learning_rate 2e-4 \
    --use_peft true \
    --peft_r 32 \
    --peft_alpha 64

# Step 3: Convert to GGUF for deployment
python convert_to_gguf.py \
    --model_path ./models/mistral-continuity \
    --output_path ../orchestrator-app/models/mistral-continuity.gguf \
    --quantization q4_k_m
```

---

## Integration & Testing

### Testing Desktop ↔ VPS Sync

```bash
# Terminal 1: Start VPS API (locally or SSH tunnel)
python orchestrator_vps/orchestrator_api.py --port 5000

# Terminal 2: Test Desktop → VPS
cd orchestrator-app
python -c "
import requests
response = requests.post(
    'http://localhost:5000/chat',
    json={'message': 'What is continuity theory?'}
)
print(response.json())
"
```

### Testing Mobile Sync

```bash
# Build and install on Android device
cd assistant-mobile
npx eas build --platform android
adb install app.apk

# Enable USB debugging on Android
# Then test through app UI

# Monitor logs
adb logcat | grep "OrchestratorSync"
```

### End-to-End Testing

```bash
# Create test script
cat > test_e2e.py << 'EOF'
import requests
import json
from datetime import datetime

def test_desktop_api():
    """Test Desktop Orchestrator"""
    # Test local chat
    response = requests.post(
        'http://localhost:3000/api/chat',
        json={'message': 'Hello, what is continuity?'}
    )
    assert response.status_code == 200
    print("✓ Desktop API working")

def test_vps_api():
    """Test VPS Orchestrator"""
    response = requests.post(
        'http://your-vps/chat',
        json={'message': 'Explain the four-tier handoff system'}
    )
    assert response.status_code == 200
    print("✓ VPS API working")

def test_sync():
    """Test Desktop ↔ VPS Sync"""
    # Push data
    requests.post(
        'http://your-vps/sync/push',
        json={'device_id': 'desktop-1', 'messages': [...]}
    )
    # Pull data
    response = requests.get(
        'http://your-vps/sync/pull?device_id=mobile-1'
    )
    assert response.status_code == 200
    print("✓ Sync working")

if __name__ == '__main__':
    test_desktop_api()
    test_vps_api()
    test_sync()
    print("\n✓ All tests passed!")
EOF

python test_e2e.py
```

---

## Extending the System

### Adding New Tools to Desktop Orchestrator

Edit `orchestrator-app/ai_orchestrator.py`:

```python
# Register new tool
@app.route('/api/tools/mytool', methods=['POST'])
def my_tool(request):
    """Example: custom analysis tool"""
    data = request.json
    # Your logic here
    return {'result': ...}

# Tell model about it in system prompt
SYSTEM_PROMPT = """
You have access to:
- search: Find files
- run: Execute Python
- shell: Run commands
- write: Create files
- mytool: My custom analysis
"""
```

### Adding Custom Training Data

Edit `training-data/generate_training_data.py`:

```python
def create_custom_examples():
    """Add examples specific to your workflow"""
    return [
        {
            "instruction": "How should I approach debugging this error?",
            "response": "1. Check the error message carefully\n2. Search similar issues\n..."
        },
        # Add more...
    ]
```

### Implementing Autonomous Agent Mode

**Warning: Requires careful safety design**

```python
# In orchestrator-app/ai_orchestrator.py
class AutonomousOrchestrator:
    def __init__(self):
        self.max_steps = 10  # Prevent infinite loops
        self.allowed_tools = ['search', 'read', 'python']
        self.blocked_commands = ['rm', 'del', 'format']
    
    def run_autonomous(self, goal):
        """Run agent toward goal with safety constraints"""
        for step in range(self.max_steps):
            # Model decides what tool to call
            action = self.model.decide_action(goal, history)
            
            # Verify action is safe
            if not self.is_safe(action):
                self.log_blocked_action(action)
                continue
            
            # Execute
            result = self.execute_tool(action['tool'], action['args'])
            
            # Log to SESSION_LOG
            self.log_step(step, action, result)
            
            # Check for goal completion
            if self.is_goal_met(goal, result):
                return result
        
        return {"status": "max_steps_reached"}
```

---

## Troubleshooting

### Common Issues

#### Desktop App Blank Screen
```
Issue: Electron app shows blank window
Solutions:
1. Check that model is loaded: ollama list
2. Check API endpoint in ai_orchestrator.py
3. Look at console: npm start (will show errors)
4. Verify PORT is not in use: netstat -an | grep 3000
```

#### Slow Inference
```
Issue: Model responses take 30+ seconds
Solutions:
1. Check GPU is being used: nvidia-smi
2. Verify quantization is applied (Q4_K_M, not full precision)
3. Consider using faster model (Phi-3 vs Llama 13B)
4. Add more VRAM or use cloud API for interactive use
```

#### Mobile Won't Connect to Desktop
```
Issue: Mobile app can't find desktop on LAN
Solutions:
1. Ensure both on same WiFi network
2. Check desktop IP: ipconfig (Windows) or ifconfig (Linux)
3. Update DESKTOP_IP in MobileOrchestrator.tsx
4. Check firewall allows port 5000
5. Test: curl http://desktop-ip:5000/health
```

#### Sync Conflicts
```
Issue: Multiple devices have conflicting updates
Solutions:
1. Check timestamp accuracy (sync uses this as tie-breaker)
2. Review conflict log: sqlite3 data.db "SELECT * FROM conflicts"
3. Manual merge in SESSION_LOG.md
4. Device with newer timestamp wins (by design)
```

### Performance Tuning

```bash
# Monitor GPU memory
watch -n 1 'nvidia-smi'

# Monitor inference speed
# Add logging to orchestrator_api.py:
import time
start = time.time()
response = model.generate(...)
elapsed = time.time() - start
print(f"Generated {len(response.split())} tokens in {elapsed:.2f}s")
print(f"Speed: {len(response.split())/elapsed:.0f} tokens/sec")
```

### Debug Logging

Enable detailed logging:

```bash
# Desktop
export DEBUG=*
npm start

# VPS
export LOG_LEVEL=DEBUG
python orchestrator_api.py

# Mobile
adb logcat | grep orchestrator
```

---

## Next Steps

1. **Start with Desktop Orchestrator** - Get interactive chat working
2. **Test with different models** - Find what works on your hardware
3. **Setup SESSION_LOG.md** - Start documenting your work
4. **Deploy VPS** - Add persistent storage
5. **Build Mobile App** - Extend to Android
6. **Implement Learning** - Build continuity analysis
7. **Extend Tools** - Add domain-specific capabilities

---

## Getting Help

- Check `orchestrator-app/PROJECT_CONTEXT.md` for desktop specifics
- See `assistant-mobile/MOBILE_INTEGRATION.md` for mobile setup
- Review `ORCHESTRATOR_SYSTEM_ARCHITECTURE.md` for design details
- Open issues on GitHub

---

**Last Updated**: December 10, 2025  
**Contributors**: sirspyr0 + Copilot  
**License**: MIT
