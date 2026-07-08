---
slug: installation-guide
title_i18n_key: Installation Guide
category: getting-started
component: core
keywords:
  - install
  - setup
  - self-hosted
  - server
  - Docker
  - deployment
  - getting started
  - first install
  - VPS
  - cloud
url_patterns: []
related:
  - system-requirements
  - domain-ssl-configuration
  - upgrades-maintenance
  - maintenance-mode
published: true
---

This guide walks you through installing Spwig on your own server. The entire process is automated — a single command handles Docker setup, database creation, service configuration, and SSL certificates.

## Before you begin

You need:

- A server running **Ubuntu 22.04 or 24.04** (Debian 12 also supported)
- **Root or sudo access** to the server
- At least **4 GB RAM** and **20 GB disk space** (8 GB RAM recommended)
- A **license token** from your Spwig purchase (check your email receipt)
- Optionally, a **domain name** pointed at your server's IP address

> **Tip:** You can install without a domain and add one later using the domain configuration tool. Your store will be accessible via the server's IP address in the meantime.

## Running the installer

Connect to your server via SSH and run the install command from your purchase confirmation email. It looks like this:

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash -s -- --token YOUR_LICENSE_TOKEN
```

Replace `YOUR_LICENSE_TOKEN` with the token from your email.

The installer runs through eight phases automatically:

1. **Pre-flight checks** — verifies your server meets the requirements (OS, disk, RAM, ports)
2. **Token validation** — confirms your license and extracts your store configuration
3. **Mode detection** — determines the best installation mode for your server (see below)
4. **Configuration** — generates secure passwords, database credentials, and service configuration
5. **Image download** — pulls the Spwig application images from the registry
6. **Service startup** — starts the database, cache, application, and background workers in order
7. **SSL setup** — obtains an SSL certificate if you have a domain configured
8. **Finalisation** — creates your admin account and generates convenience scripts

The process takes 5–15 minutes depending on your server's internet speed.

## Installation modes

The installer automatically detects your server environment and selects the best mode. You can also specify one manually with the `--mode` flag.

### Standalone mode

**Best for:** Dedicated servers and VPS instances where Spwig is the only web application.

- Uses ports 80 and 443 directly
- Handles SSL certificates automatically via Let's Encrypt
- This is the most common and recommended mode

### Sidecar mode

**Best for:** Servers that already run another web application (WordPress, a company website, etc.) on ports 80/443.

- Spwig runs on an alternate port (auto-detected, typically 8080 or 8443)
- The installer generates an nginx proxy configuration block for you to add to your existing web server
- Your existing web server handles SSL and proxies traffic to Spwig

### Local mode

**Best for:** Development and testing on your own computer.

- Accessible only at `localhost` or `127.0.0.1`
- Uses a self-signed SSL certificate (your browser will show a security warning — this is normal)
- Debug features are enabled
- No license validation required

## What happens during installation

### Docker

If Docker is not already installed, the installer offers to install it for you. Spwig runs entirely inside Docker containers — nothing is installed directly on your server's operating system outside of Docker.

### Services created

The installer creates these services:

| Service | Purpose |
|---------|---------|
| **Database** (PostgreSQL 16) | Stores all your store data — products, orders, customers, settings |
| **Cache** (Redis) | Speeds up page loads and manages background task queues |
| **Connection pooler** (PgBouncer) | Manages database connections efficiently |
| **Object storage** (MinIO) | Stores uploaded images, files, and media |
| **Application** (Spwig) | The store itself — admin panel and storefront |
| **Web server** (Nginx) | Serves your store to visitors with compression and caching |
| **Background worker** (Celery) | Processes emails, translations, analytics, and other background tasks |
| **Task scheduler** (Celery Beat) | Runs scheduled tasks like automated backups and email campaigns |
| **Translator** | AI-powered translation service for multilingual stores |
| **Upgrader** | Handles component updates from the Spwig marketplace |

### Admin account

At the end of installation, you are prompted to create an admin account. This is the account you will use to log into your store's admin panel.

### Maintenance mode

Your store starts in **maintenance mode** — visitors see a "Coming Soon" page. This gives you time to configure your store (add products, set up payment methods, customise your theme) before going live.

When you are ready, run the convenience script the installer created:

```bash
./go-live.sh
```

Or disable maintenance mode from **Admin > Store Settings > Maintenance**.

## After installation

Once the installer finishes, you will see a summary with:

- Your store's URL
- Your admin panel URL (typically `https://yourdomain.com/en/admin/`)
- The location of your configuration files
- Available convenience scripts

### Convenience scripts

The installer creates these scripts in your installation directory:

- **`./go-live.sh`** — takes your store out of maintenance mode
- **`./configure-domain.sh`** — adds or changes your domain and obtains an SSL certificate

### Next steps

1. Log into your admin panel
2. Complete the **Setup Wizard** — it guides you through store name, currency, timezone, and basic settings
3. Add your products
4. Configure a payment method
5. Choose and customise a theme
6. Run `./go-live.sh` when ready

## Installing on cloud marketplaces

Spwig is available as a one-click application on several cloud providers:

- **DigitalOcean** — deploy from the DigitalOcean Marketplace
- **Akamai (Linode)** — deploy from the Linode Marketplace
- **Vultr** — deploy from the Vultr Marketplace

These marketplace images come with the installer pre-loaded. After creating the server, SSH in and follow the on-screen instructions to complete setup with your license token.

## Getting help

If the installation fails or you encounter an error:

1. Run the **diagnostic tool**: `./doctor.sh` (created during installation)
2. The doctor checks all services, connectivity, SSL, and common issues
3. Use `./doctor.sh --fix` to attempt automatic repairs
4. Contact Spwig support with the doctor output if the issue persists
