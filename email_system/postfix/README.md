# Postfix Integration for Spwig Email System

This directory contains Postfix configuration for the built-in SMTP server email relay.

## Architecture

```
Django App
    ↓
Built-in SMTP Server (port 2525)
    ↓ DKIM Signing
    ↓
Postfix (port 25)
    ↓
External Mail Servers
```

## Quick Installation

### Option 1: Automated Script (Recommended)

```bash
# From the Spwig repo root
cd email_system/postfix
sudo ./install_postfix.sh your-domain.com
```

The script will:
1. Install Postfix and dependencies
2. Backup original configuration
3. Configure Postfix for localhost relay
4. Set up logging and log rotation
5. Start and enable Postfix service
6. Test the configuration

### Option 2: Manual Installation

If you prefer to configure Postfix manually:

#### 1. Install Postfix

```bash
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y postfix mailutils
```

#### 2. Configure Postfix

Edit `/etc/postfix/main.cf`:

```
# Basic Settings
myhostname = your-hostname.example.com
mydomain = example.com
myorigin = $mydomain

# Network Settings - localhost only
inet_interfaces = localhost
inet_protocols = ipv4
mydestination = localhost

# Relay from built-in SMTP server
mynetworks = 127.0.0.0/8 [::1]/128
relayhost =

# Disable local delivery
local_recipient_maps =
local_transport = error:local delivery is disabled

# Message limits
message_size_limit = 26214400

# TLS for outbound connections
smtp_use_tls = yes
smtp_tls_security_level = may
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt

# Logging
maillog_file = /var/log/postfix.log
```

#### 3. Restart Postfix

```bash
sudo systemctl restart postfix
sudo systemctl enable postfix
```

#### 4. Verify Installation

```bash
# Check if Postfix is running
sudo systemctl status postfix

# Check if listening on port 25
sudo netstat -tlpn | grep :25
# or
sudo ss -tlpn | grep :25

# View logs
sudo tail -f /var/log/postfix.log
```

## Configuration Details

### Port Configuration

- **Port 2525**: Built-in SMTP server (aiosmtpd) - receives from Django app
- **Port 25**: Postfix - receives from built-in SMTP server, relays to external servers

### Security

- **Localhost only**: Postfix only listens on 127.0.0.1 (not accessible from network)
- **No authentication**: Not needed since only local built-in SMTP server connects
- **TLS enabled**: For outbound connections to external mail servers

### Queue Settings

- **maximal_queue_lifetime**: 1 hour (faster failure for undeliverable emails)
- **bounce_queue_lifetime**: 1 hour (quicker bounce notifications)

These short queue times are intentional - emails that can't be delivered within an hour are likely to have incorrect recipient addresses or DNS issues that need merchant attention.

## Monitoring

### Check Queue Status

```bash
# View mail queue
mailq

# or
postqueue -p

# Flush queue (retry pending messages)
postfix flush
```

### View Logs

```bash
# Real-time log monitoring
tail -f /var/log/postfix.log

# or use journalctl
journalctl -u postfix -f

# Search for specific email
grep "recipient@example.com" /var/log/postfix.log
```

### Common Log Entries

**Successful delivery:**
```
status=sent (250 2.0.0 OK)
```

**Temporary failure (will retry):**
```
status=deferred (Connection timed out)
```

**Permanent failure:**
```
status=bounced (User unknown)
```

## Troubleshooting

### Postfix Not Starting

```bash
# Check configuration syntax
sudo postfix check

# View detailed error logs
sudo journalctl -u postfix -n 100

# Check permissions
ls -l /var/spool/postfix
```

### Emails Stuck in Queue

```bash
# View queue
mailq

# View specific message details
postcat -q QUEUE_ID

# Manually retry delivery
postqueue -f

# Delete all queued messages
sudo postsuper -d ALL
```

### Connection Refused from Built-in SMTP Server

```bash
# Verify Postfix is listening on port 25
sudo netstat -tlpn | grep :25

# Check Postfix logs for errors
sudo tail -f /var/log/postfix.log

# Restart Postfix
sudo systemctl restart postfix
```

### DNS/TLS Issues

```bash
# Test DNS resolution
dig example.com MX

# Test TLS connection to external mail server
openssl s_client -connect gmail-smtp-in.l.google.com:25 -starttls smtp

# Check Postfix TLS logs
grep TLS /var/log/postfix.log
```

## Testing Email Flow

### Test End-to-End Delivery

1. **Start both servers:**

```bash
# Terminal 1: Built-in SMTP server (from the Spwig repo root)
./shop_venv/bin/python manage.py start_smtp_server

# Terminal 2: Monitor Postfix logs
sudo tail -f /var/log/postfix.log
```

2. **Send test email through wizard:**
   - Navigate to: Admin → Email System → Add Email Account
   - Follow wizard to Step 5 (Test)
   - Send test email

3. **Monitor the flow:**

```bash
# Watch both servers process the email:
# 1. Built-in SMTP server receives from Django (port 2525)
# 2. Built-in SMTP server adds DKIM signature
# 3. Built-in SMTP server relays to Postfix (port 25)
# 4. Postfix delivers to external mail server
```

## Bounce Handling

Postfix will generate bounce messages for failed deliveries. These are logged in `/var/log/postfix.log`.

Future enhancement (Phase 4a.5.4-5): Parse bounce messages and update EmailOutbox records.

## Performance Tuning

For high-volume email sending, adjust these settings in `/etc/postfix/main.cf`:

```
# Increase concurrent deliveries
default_destination_concurrency_limit = 20

# Increase connection cache
smtp_connection_cache_destinations = 1000

# Connection reuse
smtp_connection_cache_time_limit = 60s
```

Then reload: `sudo postfix reload`

## Uninstallation

To remove Postfix:

```bash
sudo systemctl stop postfix
sudo systemctl disable postfix
sudo apt-get remove --purge postfix
sudo rm -rf /var/spool/postfix
sudo rm -f /var/log/postfix.log
```

## Production Deployment

For production deployment (Docker/systemd):

1. Include Postfix in Docker container or install on host
2. Configure Postfix to start automatically via systemd
3. Set up log aggregation (e.g., rsyslog, syslog-ng)
4. Configure monitoring alerts for queue size and delivery failures
5. Set up SPF/DKIM/DMARC DNS records for your domain

## Support

For issues with Postfix integration:

1. Check `/var/log/postfix.log` for errors
2. Run `postfix check` to validate configuration
3. Verify both servers are running (ports 2525 and 25)
4. Test DNS resolution for recipient domains
5. Check firewall rules (if sending from non-localhost)

---

**Last Updated**: 2025-10-28
**Version**: 1.0.0
