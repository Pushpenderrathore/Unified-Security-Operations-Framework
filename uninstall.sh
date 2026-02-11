#!/bin/bash

set -e

INSTALL_DIR="/opt/unified-soc"
SERVICE_FILE="/etc/systemd/system/unified-soc.service"

echo "[*] Uninstalling Unified SOC Framework..."

# Must be root
if [ "$EUID" -ne 0 ]; then
  echo "[!] Please run as root (sudo)"
  exit 1
fi

# Stop service if running
if systemctl is-active --quiet unified-soc; then
  echo "[*] Stopping service..."
  systemctl stop unified-soc
fi

# Disable service if enabled
if systemctl is-enabled --quiet unified-soc; then
  echo "[*] Disabling service..."
  systemctl disable unified-soc
fi

# Remove service file
if [ -f "$SERVICE_FILE" ]; then
  echo "[*] Removing systemd service file..."
  rm -f "$SERVICE_FILE"
fi

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
  echo "[*] Removing installation directory..."
  rm -rf "$INSTALL_DIR"
fi

# Reload systemd
echo "[*] Reloading systemd..."
systemctl daemon-reload
systemctl reset-failed

echo ""
echo "✅ Unified SOC Framework successfully uninstalled."
