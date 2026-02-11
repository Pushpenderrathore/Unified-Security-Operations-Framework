#!/bin/bash

set -e

PROJECT_NAME="Unified-Security-Operations-Framework"
INSTALL_DIR="/opt/unified-soc"
SERVICE_FILE="/etc/systemd/system/unified-soc.service"

echo "[*] Installing Unified SOC Framework..."

# Check root
if [ "$EUID" -ne 0 ]; then
  echo "[!] Please run as root (sudo)"
  exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 is not installed."
    exit 1
fi

# Create install directory
echo "[*] Creating install directory..."
mkdir -p $INSTALL_DIR
cp -r . $INSTALL_DIR

cd $INSTALL_DIR

# Create virtual environment
echo "[*] Creating virtual environment..."
python3 -m venv venv

# Install dependencies
echo "[*] Installing dependencies..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Create systemd service
echo "[*] Creating systemd service..."

cat > $SERVICE_FILE <<EOF
[Unit]
Description=Unified SOC Framework Daemon
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/soc_daemon.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
systemctl daemon-reload
systemctl enable unified-soc
systemctl restart unified-soc

echo ""
echo "✅ Installation Complete!"
echo "Check status with:"
echo "sudo systemctl status unified-soc"
