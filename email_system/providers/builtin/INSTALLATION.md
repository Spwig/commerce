# Built-in SMTP Server - Installation Guide

Complete guide for setting up the Spwig built-in SMTP server for sending transactional emails.

## Table of Contents
1. [Requirements](#requirements)
2. [Installation Steps](#installation-steps)
3. [DKIM Key Generation](#dkim-key-generation)
4. [DNS Configuration](#dns-configuration)
5. [Systemd Service Setup](#systemd-service-setup)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## Requirements

### Software Requirements
- **Python 3.10+** with virtual environment
- **Postfix** (or another MTA) for mail relay
- **PostgreSQL** (already required by Spwig)
- **Root/sudo access** for systemd service installation

### Python Dependencies
Already included in Spwig:
- `aiosmtpd==1.4.6` - Async SMTP server
- `dkimpy==1.1.8` - DKIM signing
- `dnspython==2.8.0` - DNS validation

### Network Requirements
- **Port 2525** available (internal SMTP server)
- **Port 25** (Postfix outbound SMTP)
- **Port 53** (DNS resolution)

---

## Installation Steps

### Step 1: Verify Installation

The built-in SMTP provider is automatically installed with Spwig. Verify it's available:

```bash
cd /path/to/shop
./shop_venv/bin/python manage.py shell -c "
from email_system.providers.registry import ProviderRegistry
providers = ProviderRegistry.list_providers()
builtin = [p for p in providers if p['key'] == 'builtin_smtp']
print('Built-in provider installed:', len(builtin) > 0)
"
```

### Step 2: Install Postfix (if not already installed)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postfix
```

**RHEL/CentOS:**
```bash
sudo yum install postfix
sudo systemctl enable postfix
sudo systemctl start postfix
```

During installation, select **"Internet Site"** when prompted.

### Step 3: Configure Postfix

Edit `/etc/postfix/main.cf`:

```bash
sudo nano /etc/postfix/main.cf
```

Add/modify these settings:

```ini
# Allow relay from localhost (Spwig SMTP server)
inet_interfaces = loopback-only
mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128

# Set hostname
myhostname = shop.yourdomain.com
mydomain = yourdomain.com
myorigin = $mydomain

# Accept mail from localhost on port 25
smtpd_relay_restrictions = permit_mynetworks, reject_unauth_destination
```

Restart Postfix:

```bash
sudo systemctl restart postfix
```

---

## DKIM Key Generation

DKIM (DomainKeys Identified Mail) signs your emails to prove they're from you.

### Generate Keys

```bash
cd /path/to/shop
./shop_venv/bin/python manage.py generate_dkim_keys \
    --domain yourdomain.com \
    --selector mail \
    --account "Built-in SMTP Server"
```

**Options:**
- `--domain`: Your sending domain (e.g., `shop.example.com`)
- `--selector`: DKIM selector name (default: `mail`)
- `--account`: EmailAccount name to attach keys to
- `--force`: Regenerate if keys already exist

### View Generated Keys

```bash
./shop_venv/bin/python manage.py shell -c "
from email_system.models import EmailAccount
account = EmailAccount.objects.get(provider_key='builtin_smtp')
creds = account.get_credentials()
print('DKIM Public Key:')
print(creds.get('dkim_public_key', 'Not generated'))
"
```

---

## DNS Configuration

### Required DNS Records

You must add **4 types** of DNS records for proper email delivery:

#### 1. MX Record (Mail Exchange)

Points to your mail server.

**Type:** `MX`
**Name:** `@` (or your domain)
**Priority:** `10`
**Value:** `shop.yourdomain.com` (your server hostname)

#### 2. SPF Record (Sender Policy Framework)

Authorizes your server to send email for your domain.

**Type:** `TXT`
**Name:** `@` (or your domain)
**Value:**
```
v=spf1 ip4:YOUR_SERVER_IP include:_spf.google.com ~all
```

Replace `YOUR_SERVER_IP` with your actual server IP address. If you use Gmail/GSuite, keep the `include:_spf.google.com` part.

#### 3. DKIM Record (DomainKeys Identified Mail)

Contains your public key for signature verification.

**Type:** `TXT`
**Name:** `mail._domainkey` (where `mail` is your selector)
**Value:**
```
v=DKIM1; k=rsa; p=YOUR_PUBLIC_KEY_HERE
```

Get your public key from the "Generate Keys" step above, then add it to your DNS:

```bash
./shop_venv/bin/python manage.py shell -c "
from email_system.smtp_server.dkim_handler import DKIMHandler
from email_system.models import EmailAccount
account = EmailAccount.objects.get(provider_key='builtin_smtp')
creds = account.get_credentials()
public_key = creds.get('dkim_public_key')
print(f'v=DKIM1; k=rsa; p={public_key}')
"
```

#### 4. DMARC Record (Domain-based Message Authentication)

Tells receivers what to do with failed authentication.

**Type:** `TXT`
**Name:** `_dmarc`
**Value:**
```
v=DMARC1; p=quarantine; rua=mailto:postmaster@yourdomain.com; ruf=mailto:postmaster@yourdomain.com; fo=1; adkim=r; aspf=r
```

### DNS Provider-Specific Instructions

See the wizard's DNS tab for provider-specific instructions (Cloudflare, GoDaddy, Namecheap, Route 53, etc.).

### Verify DNS Propagation

Wait 5-60 minutes for DNS propagation, then verify:

```bash
# Check MX record
dig MX yourdomain.com +short

# Check SPF record
dig TXT yourdomain.com +short | grep spf

# Check DKIM record
dig TXT mail._domainkey.yourdomain.com +short

# Check DMARC record
dig TXT _dmarc.yourdomain.com +short
```

---

## Systemd Service Setup

### Automatic Installation (Recommended)

Use the provided installation script:

```bash
cd /path/to/shop
sudo ./email_system/systemd/install-smtp-service.sh
```

The script will:
1. Detect your shop directory and virtual environment
2. Create the systemd service file
3. Reload systemd
4. Optionally enable and start the service

### Manual Installation

If you prefer to install manually:

1. **Copy and customize the service file:**

```bash
sudo cp email_system/systemd/spwig-smtp.service /etc/systemd/system/
sudo sed -i 's|/path/to/shop|/actual/path/to/shop|g' /etc/systemd/system/spwig-smtp.service
sudo sed -i 's|User=www-data|User=your-user|g' /etc/systemd/system/spwig-smtp.service
```

2. **Reload systemd:**

```bash
sudo systemctl daemon-reload
```

3. **Enable and start the service:**

```bash
sudo systemctl enable spwig-smtp
sudo systemctl start spwig-smtp
```

4. **Check status:**

```bash
sudo systemctl status spwig-smtp
```

### Service Management Commands

```bash
# Start the service
sudo systemctl start spwig-smtp

# Stop the service
sudo systemctl stop spwig-smtp

# Restart the service
sudo systemctl restart spwig-smtp

# View status
sudo systemctl status spwig-smtp

# View logs (live)
sudo journalctl -u spwig-smtp -f

# View last 100 lines of logs
sudo journalctl -u spwig-smtp -n 100
```

---

## Testing

### Test 1: SMTP Server Running

```bash
# Check if server is listening on port 2525
sudo netstat -tulpn | grep 2525
# OR
sudo ss -tulpn | grep 2525
```

Expected output: `127.0.0.1:2525` in LISTEN state

### Test 2: Send Test Email

Use the wizard's "Test Send" feature (Step 5) or send via Django shell:

```bash
./shop_venv/bin/python manage.py shell
```

```python
from email_system.models import EmailAccount
from email_system.providers.registry import ProviderRegistry

# Get built-in account
account = EmailAccount.objects.get(provider_key='builtin_smtp')

# Get provider class
ProviderClass = ProviderRegistry.get_provider('builtin_smtp')
provider = ProviderClass(
    credentials=account.get_credentials(),
    config={}
)

# Send test message
from email_system.providers.base import EmailMessage

message = EmailMessage(
    to=['your-email@example.com'],
    subject='Test from Spwig SMTP Server',
    html_body='<p>This is a test email from your Spwig built-in SMTP server!</p>',
    text_body='This is a test email from your Spwig built-in SMTP server!',
    from_email=account.from_email,
    from_name=account.from_name
)

result = provider.send(message)
print(f"Success: {result['success']}")
print(f"Message ID: {result.get('message_id')}")
```

### Test 3: Check DKIM Signature

Send a test email to yourself and view the email source. Look for:

```
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/simple;
  d=yourdomain.com; s=mail;
```

### Test 4: Use Mail Tester

Send an email to the address provided by [mail-tester.com](https://www.mail-tester.com/) and check your score. Aim for 10/10.

---

## Troubleshooting

### SMTP Server Won't Start

**Check logs:**
```bash
sudo journalctl -u spwig-smtp -n 50 --no-pager
```

**Common issues:**
- Port 2525 already in use → Change port in `email_system/smtp_server/server.py`
- Permission denied → Ensure user in systemd service file has access to shop directory
- Missing encryption key → Check `.env` file has `EMAIL_ENCRYPTION_KEY`

### Emails Not Sending

**Check Postfix status:**
```bash
sudo systemctl status postfix
sudo tail -f /var/log/mail.log
```

**Check Postfix queue:**
```bash
sudo mailq
```

**Common issues:**
- Postfix not running → `sudo systemctl start postfix`
- Firewall blocking port 25 → `sudo ufw allow 25/tcp`
- ISP blocking port 25 → Use SMTP relay (Gmail, SendGrid, etc.)

### DKIM Signature Invalid

**Verify DNS record:**
```bash
dig TXT mail._domainkey.yourdomain.com +short
```

**Common issues:**
- DNS not propagated yet → Wait up to 1 hour
- Wrong selector → Check account credentials for `dkim_selector`
- Public key truncated → Some DNS providers split long TXT records

**Fix truncated TXT records:**
Some DNS providers require splitting long records:
```
"v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A..." "MIIBCgKCAQEA1234567890..."
```

### Low Spam Score

1. **Add PTR (reverse DNS) record** - Contact your hosting provider
2. **Warm up your IP** - Start with low volume, gradually increase
3. **Monitor blacklists**: Check [MXToolbox](https://mxtoolbox.com/blacklists.aspx)
4. **Ensure all DNS records are correct** (MX, SPF, DKIM, DMARC)

### Permission Denied Errors

**Ensure correct permissions:**
```bash
cd /path/to/shop
sudo chown -R your-user:your-group .
chmod -R 755 .
```

---

## Advanced Configuration

### Using a Different Port

Edit `email_system/smtp_server/server.py`:

```python
SMTP_PORT = 2525  # Change to your desired port
```

Restart the service after changing.

### Using SMTP Relay (for restricted ISPs)

If your ISP blocks port 25, configure Postfix to relay through Gmail/SendGrid:

**Edit `/etc/postfix/main.cf`:**
```ini
relayhost = [smtp.gmail.com]:587
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_tls_security_level = may
```

**Create `/etc/postfix/sasl_passwd`:**
```
[smtp.gmail.com]:587 your-email@gmail.com:your-app-password
```

**Hash and reload:**
```bash
sudo postmap /etc/postfix/sasl_passwd
sudo systemctl reload postfix
```

---

## Support

For issues or questions:
1. Check logs: `sudo journalctl -u spwig-smtp -f`
2. Verify DNS: Use wizard's DNS Assistant
3. Test connectivity: `telnet localhost 2525`
4. Review Spwig documentation

---

**Last Updated:** 2025-10-28
**Version:** 1.0.0
