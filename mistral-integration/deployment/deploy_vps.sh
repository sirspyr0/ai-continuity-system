#!/bin/bash
# Deploy Mistral orchestrator to VPS
# Supports both CPU and GPU instances

set -e

echo "=== VPS Orchestrator Deployment ==="
echo ""

# Configuration
MODEL_PATH="${MODEL_PATH:-./models/mistral-7b-continuity}"
USE_GPU="${USE_GPU:-true}"
QUANTIZE="${QUANTIZE:-true}"
PORT="${PORT:-5000}"
WORKERS="${WORKERS:-4}"

# Check if model exists
if [ ! -d "$MODEL_PATH" ]; then
    echo "Error: Model not found at $MODEL_PATH"
    echo "Please upload your fine-tuned model to the VPS first"
    exit 1
fi

# Step 1: Install system dependencies
echo "Step 1: Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    sudo apt-get update
    sudo apt-get install -y python3-pip python3-venv nginx
elif command -v yum &> /dev/null; then
    # CentOS/RHEL
    sudo yum install -y python3-pip python3-virtualenv nginx
fi

# Step 2: Create virtual environment
echo ""
echo "Step 2: Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 3: Install Python dependencies
echo ""
echo "Step 3: Installing Python dependencies..."
pip install --upgrade pip
pip install -r ../requirements.txt
pip install gunicorn flask-cors

# Step 4: Check GPU availability
echo ""
echo "Step 4: Checking GPU availability..."
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Step 5: Create systemd service
echo ""
echo "Step 5: Creating systemd service..."
sudo tee /etc/systemd/system/orchestrator-vps.service > /dev/null << EOF
[Unit]
Description=Orchestrator VPS API
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment="MODEL_PATH=$MODEL_PATH"
Environment="USE_GPU=$USE_GPU"
Environment="QUANTIZE=$QUANTIZE"
ExecStart=$(pwd)/venv/bin/gunicorn -w $WORKERS -b 0.0.0.0:$PORT orchestrator_api:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Step 6: Configure nginx reverse proxy
echo ""
echo "Step 6: Configuring nginx..."
sudo tee /etc/nginx/sites-available/orchestrator > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeout for long-running requests
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/orchestrator /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# Step 7: Configure firewall
echo ""
echo "Step 7: Configuring firewall..."
if command -v ufw &> /dev/null; then
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
elif command -v firewall-cmd &> /dev/null; then
    sudo firewall-cmd --permanent --add-service=http
    sudo firewall-cmd --permanent --add-service=https
    sudo firewall-cmd --reload
fi

# Step 8: Start service
echo ""
echo "Step 8: Starting service..."
sudo systemctl daemon-reload
sudo systemctl enable orchestrator-vps
sudo systemctl start orchestrator-vps

# Wait for service to start
sleep 5

# Check service status
echo ""
echo "Service Status:"
sudo systemctl status orchestrator-vps --no-pager

# Test endpoint
echo ""
echo "Testing API endpoint..."
curl -s http://localhost:$PORT/health | python3 -m json.tool || echo "API not responding"

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "Service: orchestrator-vps"
echo "Status: sudo systemctl status orchestrator-vps"
echo "Logs: sudo journalctl -u orchestrator-vps -f"
echo ""
echo "API available at:"
echo "  Local: http://localhost:$PORT"
echo "  Public: http://YOUR_VPS_IP"
echo ""
echo "Endpoints:"
echo "  POST /generate - Generate response"
echo "  GET /health - Health check"
echo "  GET /info - Server information"
echo ""
echo "To enable HTTPS, install certbot and run:"
echo "  sudo certbot --nginx -d your-domain.com"
echo ""
