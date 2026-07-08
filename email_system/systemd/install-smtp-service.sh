#!/bin/bash
# Installation script for Spwig SMTP Server systemd service
#
# Usage:
#   sudo ./install-smtp-service.sh [/path/to/shop]
#
# If no path is provided, it will use the current directory

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Error: This script must be run as root (use sudo)${NC}"
   exit 1
fi

# Get shop directory
SHOP_DIR="${1:-$(dirname "$(dirname "$(dirname "$(realpath "$0")")")")}"
SHOP_DIR=$(realpath "$SHOP_DIR")

echo -e "${GREEN}Spwig SMTP Server Installation${NC}"
echo "================================"
echo ""
echo "Shop directory: $SHOP_DIR"
echo ""

# Verify shop directory exists
if [ ! -f "$SHOP_DIR/manage.py" ]; then
    echo -e "${RED}Error: manage.py not found in $SHOP_DIR${NC}"
    echo "Please provide the correct path to your Spwig installation"
    exit 1
fi

# Find venv directory
VENV_DIR=""
for venv_name in shop_venv venv env .venv; do
    if [ -f "$SHOP_DIR/$venv_name/bin/python" ]; then
        VENV_DIR="$SHOP_DIR/$venv_name"
        break
    fi
done

if [ -z "$VENV_DIR" ]; then
    echo -e "${RED}Error: Python virtual environment not found${NC}"
    echo "Please ensure shop_venv exists in $SHOP_DIR"
    exit 1
fi

echo "Virtual environment: $VENV_DIR"
echo ""

# Get the user running the shop (from parent directory owner)
SHOP_USER=$(stat -c '%U' "$SHOP_DIR")
SHOP_GROUP=$(stat -c '%G' "$SHOP_DIR")

echo "Running as user: $SHOP_USER:$SHOP_GROUP"
echo ""

# Create service file from template
SERVICE_FILE="/etc/systemd/system/spwig-smtp.service"
TEMPLATE_FILE="$SHOP_DIR/email_system/systemd/spwig-smtp.service"

if [ ! -f "$TEMPLATE_FILE" ]; then
    echo -e "${RED}Error: Service template not found at $TEMPLATE_FILE${NC}"
    exit 1
fi

echo "Creating systemd service file..."

# Replace placeholders in template
sed -e "s|/path/to/shop|$SHOP_DIR|g" \
    -e "s|User=www-data|User=$SHOP_USER|g" \
    -e "s|Group=www-data|Group=$SHOP_GROUP|g" \
    "$TEMPLATE_FILE" > "$SERVICE_FILE"

echo -e "${GREEN}✓${NC} Created $SERVICE_FILE"
echo ""

# Reload systemd
echo "Reloading systemd daemon..."
systemctl daemon-reload
echo -e "${GREEN}✓${NC} Systemd reloaded"
echo ""

# Ask if user wants to enable and start the service
read -p "Do you want to enable the service to start on boot? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl enable spwig-smtp.service
    echo -e "${GREEN}✓${NC} Service enabled"
fi

read -p "Do you want to start the service now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl start spwig-smtp.service
    echo -e "${GREEN}✓${NC} Service started"
    echo ""
    echo "Checking service status..."
    sleep 2
    systemctl status spwig-smtp.service --no-pager -l
fi

echo ""
echo -e "${GREEN}Installation complete!${NC}"
echo ""
echo "Useful commands:"
echo "  sudo systemctl status spwig-smtp     # Check service status"
echo "  sudo systemctl start spwig-smtp      # Start the service"
echo "  sudo systemctl stop spwig-smtp       # Stop the service"
echo "  sudo systemctl restart spwig-smtp    # Restart the service"
echo "  sudo journalctl -u spwig-smtp -f     # View logs (follow mode)"
echo ""
