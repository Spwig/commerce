---
slug: system-requirements
title_i18n_key: System Requirements
category: getting-started
component: core
keywords:
  - requirements
  - server
  - RAM
  - disk
  - CPU
  - VPS
  - hosting
  - minimum specs
  - recommended specs
  - resource tiers
  - translator
url_patterns: []
related:
  - installation-guide
  - domain-ssl-configuration
  - shop-dashboard
published: true
---

Spwig runs on most modern Linux servers. This page covers the minimum and recommended specifications, what happens on smaller servers, and which cloud providers work well.

## Minimum requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| **Operating system** | Ubuntu 22.04 LTS, Ubuntu 24.04 LTS, or Debian 12 | Ubuntu 24.04 LTS |
| **RAM** | 4 GB | 8 GB or more |
| **Disk space** | 20 GB | 40 GB or more |
| **CPU** | 1 vCPU | 2+ vCPUs |
| **Architecture** | x86_64 (AMD64) | x86_64 |
| **Network** | Public IP address (for standalone mode) | Static public IP |
| **Ports** | 80 and 443 (standalone) or any alternate port (sidecar) | 80 and 443 |

> **Note:** ARM-based servers (e.g. AWS Graviton, Oracle Ampere) are not currently supported.

## Resource tiers

The installer automatically detects your server's available RAM and selects the appropriate resource tier.

### Standard tier (6 GB+ RAM)

All services run with full capabilities:

- AI-powered **translation service** enabled — translate product descriptions, page content, and SEO text into multiple languages directly from your admin panel
- Full memory allocation for the application, database, and background workers
- Background worker concurrency optimised for your CPU count

### Small tier (4–6 GB RAM)

The installer adapts to conserve memory:

- AI translation service is **disabled** to save approximately 2 GB of RAM. You can still manage translations manually or use external translation tools — only the built-in AI translator is affected.
- Application and worker memory limits are reduced
- All other features work identically to the standard tier

> **Tip:** If you start on a small server and later upgrade to 6 GB+ RAM, re-run the installer to enable the translation service.

## Recommended cloud providers

Spwig works on any Linux server that meets the requirements. These providers are tested and offer good value:

| Provider | Recommended plan | RAM | Disk | Approximate cost |
|----------|-----------------|-----|------|-----------------|
| **DigitalOcean** | Basic Droplet | 4 GB | 80 GB | $24/month |
| **Linode (Akamai)** | Shared 4 GB | 4 GB | 80 GB | $24/month |
| **Vultr** | Cloud Compute | 4 GB | 100 GB | $24/month |
| **Hetzner** | CX31 | 8 GB | 80 GB | €8/month |
| **OVH** | Starter VPS | 4 GB | 80 GB | €7/month |

For stores expecting significant traffic or large product catalogs (10,000+ products), start with 8 GB RAM and 2+ vCPUs.

## Disk space usage

A fresh Spwig installation uses approximately 8 GB of disk space:

| Component | Size |
|-----------|------|
| Docker images | ~4 GB |
| Database (empty store) | ~200 MB |
| AI translation models (if enabled) | ~2 GB |
| Application and configuration files | ~500 MB |
| Operating system and Docker engine | ~3 GB |

Plan additional space for:

- **Product images and media** — depends on your catalog size. Budget 1–5 GB for a typical store with hundreds of products.
- **Database growth** — grows with orders, customers, and analytics data. A store processing 100 orders per day typically grows by ~1 GB per year.
- **Backups** — if storing backups locally, each full backup is roughly the size of your database plus media. With a 30-day retention policy, budget 2–3× your current data size.

## Domain and DNS

A domain name is optional during installation but required for production use. You need:

- A domain or subdomain (e.g. `shop.example.com`)
- An **A record** pointing to your server's public IP address
- DNS propagation completed (typically 5–60 minutes after adding the record)

The installer obtains a free SSL certificate from Let's Encrypt automatically when a valid domain is detected. You can also add a domain after installation using the `./configure-domain.sh` script.

## Firewall

If your server has a firewall (most cloud providers enable one by default), ensure these ports are open:

| Port | Protocol | Purpose |
|------|----------|---------|
| **22** | TCP | SSH access (for you to manage the server) |
| **80** | TCP | HTTP (required for Let's Encrypt certificate validation) |
| **443** | TCP | HTTPS (your store's secure traffic) |

In sidecar mode, open whichever alternate port the installer assigns instead of 80/443.

## Software prerequisites

The installer handles all software installation automatically. For reference, these are the components it installs or verifies:

- **Docker Engine** — container runtime (installed automatically if missing)
- **Docker Compose** — service orchestration (included with Docker Engine)
- **curl** — used by the installer itself (present on virtually all Linux systems)

No other software needs to be pre-installed. Spwig does not require you to install Python, Node.js, PostgreSQL, Redis, or Nginx manually — everything runs inside Docker containers.
