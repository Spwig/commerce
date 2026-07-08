#!/bin/bash
#
# Postfix Installation Script for Spwig Email System
# This script installs and configures Postfix to relay emails from the built-in SMTP server
#
# Usage: sudo ./install_postfix.sh
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Spwig Email System - Postfix Setup${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Error: This script must be run as root (use sudo)${NC}"
    exit 1
fi

# Get the system hostname
HOSTNAME=$(hostname -f 2>/dev/null || hostname)
echo -e "${YELLOW}System hostname: ${HOSTNAME}${NC}"

# Prompt for domain name if not provided
if [ -z "$1" ]; then
    echo ""
    read -p "Enter your domain name (e.g., example.com): " DOMAIN
else
    DOMAIN="$1"
fi

if [ -z "$DOMAIN" ]; then
    echo -e "${RED}Error: Domain name is required${NC}"
    exit 1
fi

echo -e "${YELLOW}Configuring Postfix for domain: ${DOMAIN}${NC}"
echo ""

# 1. Install Postfix and dependencies
echo -e "${GREEN}[1/7] Installing Postfix...${NC}"
export DEBIAN_FRONTEND=noninteractive

# Pre-configure Postfix for non-interactive installation
debconf-set-selections <<EOF
postfix postfix/mailname string ${DOMAIN}
postfix postfix/main_mailer_type string 'Internet Site'
EOF

apt-get update -qq
apt-get install -y postfix mailutils libsasl2-modules

echo -e "${GREEN}✓ Postfix installed${NC}"
echo ""

# 2. Backup original configuration
echo -e "${GREEN}[2/7] Backing up original configuration...${NC}"
BACKUP_DIR="/etc/postfix/backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp /etc/postfix/main.cf "$BACKUP_DIR/main.cf.orig" 2>/dev/null || true
cp /etc/postfix/master.cf "$BACKUP_DIR/master.cf.orig" 2>/dev/null || true
echo -e "${GREEN}✓ Backup saved to: ${BACKUP_DIR}${NC}"
echo ""

# 3. Create main.cf configuration
echo -e "${GREEN}[3/7] Configuring Postfix main.cf...${NC}"

cat > /etc/postfix/main.cf <<EOF
# Postfix Main Configuration for Spwig Email System
# Generated on: $(date)

# Basic Settings
myhostname = ${HOSTNAME}
mydomain = ${DOMAIN}
myorigin = \$mydomain

# Network Settings
inet_interfaces = localhost
inet_protocols = ipv4
mydestination = localhost

# Mail Relay - Accept from local SMTP server only
mynetworks = 127.0.0.0/8 [::1]/128
relayhost =

# Disable local delivery (we only relay)
local_recipient_maps =
local_transport = error:local delivery is disabled

# Message Size Limits
message_size_limit = 26214400
mailbox_size_limit = 0

# TLS Settings for outbound connections
smtp_use_tls = yes
smtp_tls_security_level = may
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
smtp_tls_loglevel = 1

# SMTP Server on port 25 (receives from built-in SMTP server on 2525)
smtpd_banner = \$myhostname ESMTP
smtpd_recipient_restrictions = permit_mynetworks,reject_unauth_destination

# Queue Settings
maximal_queue_lifetime = 1h
bounce_queue_lifetime = 1h

# Logging
maillog_file = /var/log/postfix.log

# Disable unnecessary features
smtpd_sasl_auth_enable = no
smtpd_use_tls = no
alias_maps =
alias_database =
EOF

echo -e "${GREEN}✓ main.cf configured${NC}"
echo ""

# 4. Verify master.cf has required services (DO NOT OVERWRITE)
echo -e "${GREEN}[4/7] Verifying Postfix master.cf services...${NC}"

# Check if critical smtp transport service exists
if ! grep -q "^smtp.*unix.*smtp$" /etc/postfix/master.cf; then
    echo -e "${YELLOW}Adding missing smtp unix transport service...${NC}"
    # Use postconf to add the service
    postconf -M smtp/unix="smtp unix - - n - - smtp"
fi

# Verify other critical services exist (they should from default install)
REQUIRED_SERVICES=("cleanup/unix" "qmgr/unix" "pickup/unix" "bounce/unix" "error/unix")
MISSING_SERVICES=()

for service in "${REQUIRED_SERVICES[@]}"; do
    service_name=$(echo $service | cut -d'/' -f1)
    if ! grep -q "^${service_name}.*unix" /etc/postfix/master.cf; then
        MISSING_SERVICES+=($service_name)
    fi
done

if [ ${#MISSING_SERVICES[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠ Warning: Some services may be missing from master.cf${NC}"
    echo -e "${YELLOW}Missing: ${MISSING_SERVICES[*]}${NC}"
    echo -e "${YELLOW}Running postfix upgrade-configuration to restore default services...${NC}"
    postfix upgrade-configuration 2>/dev/null || echo "Upgrade skipped"
fi

echo -e "${GREEN}✓ master.cf verified (using system defaults with required services)${NC}"
echo ""

# 5. Create log directory and set permissions
echo -e "${GREEN}[5/7] Setting up logging...${NC}"
touch /var/log/postfix.log
chown postfix:postfix /var/log/postfix.log
chmod 640 /var/log/postfix.log

# Add logrotate configuration
cat > /etc/logrotate.d/postfix <<EOF
/var/log/postfix.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 640 postfix postfix
    sharedscripts
    postrotate
        /usr/sbin/postfix reload > /dev/null
    endscript
}
EOF

echo -e "${GREEN}✓ Logging configured${NC}"
echo ""

# 6. Reload Postfix configuration
echo -e "${GREEN}[6/7] Reloading Postfix...${NC}"
systemctl enable postfix
systemctl restart postfix

# Wait for Postfix to start
sleep 2

if systemctl is-active --quiet postfix; then
    echo -e "${GREEN}✓ Postfix is running${NC}"
else
    echo -e "${RED}✗ Postfix failed to start${NC}"
    echo -e "${YELLOW}Check logs: journalctl -u postfix -n 50${NC}"
    exit 1
fi
echo ""

# 7. Test configuration
echo -e "${GREEN}[7/7] Testing configuration...${NC}"

# Check if Postfix is listening on port 25
if netstat -tlpn 2>/dev/null | grep -q ':25.*postfix' || ss -tlpn 2>/dev/null | grep -q ':25.*postfix'; then
    echo -e "${GREEN}✓ Postfix listening on port 25${NC}"
else
    echo -e "${YELLOW}⚠ Postfix may not be listening on port 25${NC}"
fi

# Display Postfix status
echo ""
postfix status

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Postfix Installation Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. The built-in SMTP server (port 2525) will relay emails through Postfix (port 25)"
echo "2. Postfix will deliver emails to external mail servers"
echo "3. Monitor logs: tail -f /var/log/postfix.log"
echo "4. Check queue: mailq"
echo ""
echo -e "${YELLOW}Testing:${NC}"
echo "Send a test email through the Spwig wizard to verify the complete email flow"
echo ""
