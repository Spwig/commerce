---
slug: ssl-setup
title_i18n_key: SSL Setup
category: store-config
component: domain_ssl
keywords:
  - SSL
  - HTTPS
  - certificate
  - TLS
  - Let's Encrypt
  - Cloudflare
  - Origin CA
  - custom certificate
  - security
  - encryption
  - domain
  - self-signed
url_patterns:
  - /admin/core/sitesettings/
related:
  - cdn-setup
published: true
---

SSL (Secure Sockets Layer) encrypts the connection between your customers' browsers and your store. When SSL is active, your store's URL begins with `https://` and browsers display a padlock icon. SSL is essential for accepting payments, protecting customer data, and ranking well in search engines.

Spwig supports several SSL modes to fit different hosting setups. This guide explains each mode and helps you choose the right one.

## Choosing an SSL Mode

| Mode | Best for | Certificate cost | Renewal |
|------|----------|-----------------|---------|
| **Let's Encrypt** | Most stores | Free | Automatic |
| **Cloudflare Origin CA** | Stores using Cloudflare proxy | Free | Manual (up to 15 years) |
| **Custom Certificate** | Stores with purchased certificates | Varies | Manual |
| **Managed Externally** | Load balancers, Cloudflare Flexible | N/A | N/A |
| **Self-Signed** | Development and testing | Free | Manual |
| **None (HTTP)** | Local development only | N/A | N/A |

If you are unsure which mode to use, **Let's Encrypt** is the best choice for most stores. It is free, automatic, and trusted by all browsers.

## Let's Encrypt

Let's Encrypt provides free, trusted SSL certificates that renew automatically every 60-90 days. This is the recommended option for most merchants.

**Requirements:**
- Your domain must point to your server (A record in DNS)
- Port 80 must be accessible from the internet (for certificate verification)
- An email address for certificate expiry notifications

**Setup steps:**
1. Go to **Settings > Site Settings** and open the **Domain & SSL** tab
2. Enter your domain name
3. Select **Let's Encrypt**
4. Enter your admin email address
5. Click **Apply Configuration**

Spwig handles everything else automatically: verifying your domain, obtaining the certificate, configuring NGINX, and setting up automatic renewal.

## Cloudflare Origin CA

Cloudflare Origin CA certificates encrypt the connection between Cloudflare's edge servers and your store. These certificates are free and can last up to 15 years, but they are **only trusted by Cloudflare** -- browsers connecting directly to your server will see a certificate warning.

This mode is ideal if you use Cloudflare as a proxy (orange cloud enabled) for your domain. Cloudflare presents its own trusted certificate to visitors, and the Origin CA certificate secures the connection between Cloudflare and your server.

**Requirements:**
- A Cloudflare account with your domain added
- An Origin CA certificate and private key generated from the Cloudflare dashboard
- Cloudflare SSL/TLS mode set to **Full (Strict)**

**Generating the Origin CA certificate:**
1. Log in to your Cloudflare dashboard
2. Select your domain
3. Go to **SSL/TLS > Origin Server**
4. Click **Create Certificate**
5. Choose RSA or ECC (RSA is most compatible)
6. Add your domain (e.g., `example.com` and `*.example.com`)
7. Choose a validity period (15 years is recommended)
8. Click **Create** and copy both the certificate and private key

**Setting up in Spwig:**
1. Go to **Settings > Site Settings** and open the **Domain & SSL** tab
2. Enter your domain name
3. Select **Cloudflare Origin CA**
4. Paste the certificate into the **Certificate (PEM)** field
5. Paste the private key into the **Private Key (PEM)** field
6. Click **Apply Configuration**

**After configuration:**
- In Cloudflare, set SSL/TLS mode to **Full (Strict)**
- Enable the Cloudflare proxy (orange cloud) for your domain's DNS record
- Your store will be accessible via HTTPS with Cloudflare's trusted certificate

## Custom Certificate

Use this mode if you have purchased an SSL certificate from a certificate authority (CA) such as DigiCert, Sectigo, or GoDaddy, or if your hosting provider has issued one for you.

**Setup steps:**
1. Go to **Settings > Site Settings** and open the **Domain & SSL** tab
2. Enter your domain name
3. Select **Custom Certificate**
4. Paste your certificate chain (including intermediate certificates) into the **Certificate (PEM)** field
5. Paste your private key into the **Private Key (PEM)** field
6. Click **Apply Configuration**

Your certificate should include the full chain: your domain certificate followed by any intermediate certificates. The private key should be in PEM format (beginning with `-----BEGIN PRIVATE KEY-----` or `-----BEGIN RSA PRIVATE KEY-----`).

## Managed Externally

Choose this mode when SSL is terminated by an external service before traffic reaches your server. In this setup, your server only receives plain HTTP traffic -- no certificate is installed on the server itself.

**Common scenarios:**
- **Cloudflare Flexible SSL** -- Cloudflare encrypts browser-to-Cloudflare traffic, but sends HTTP to your server
- **Cloud load balancers** -- AWS ALB, Google Cloud Load Balancer, or DigitalOcean Load Balancer terminates SSL and forwards HTTP
- **Reverse proxy** -- Another server in front of Spwig handles SSL

**Setup steps:**
1. Go to **Settings > Site Settings** and open the **Domain & SSL** tab
2. Enter your domain name
3. Select **Managed Externally**
4. Click **Apply Configuration**

Spwig will configure NGINX to serve HTTP only and trust the `X-Forwarded-Proto` header from your proxy to correctly detect HTTPS visitors.

## Self-Signed Certificate

Self-signed certificates encrypt the connection but are not trusted by browsers. Visitors will see a security warning that they must bypass manually. This mode is suitable for development servers and internal testing only.

**Setup steps:**
1. Go to **Settings > Site Settings** and open the **Domain & SSL** tab
2. Enter your domain name
3. Select **Self-Signed**
4. Click **Apply Configuration**

Spwig generates a self-signed certificate automatically. Do not use this mode for a production store.

## Troubleshooting

**Certificate not working after configuration:**
- Verify your domain's A record points to your server's IP address
- Ensure ports 80 and 443 are open in your firewall
- Wait a few minutes for DNS changes to propagate

**Let's Encrypt fails to issue a certificate:**
- Check that your domain resolves to this server's IP address
- Ensure port 80 is not blocked by a firewall
- If you are behind Cloudflare, temporarily set DNS to "DNS only" (grey cloud) during certificate issuance

**Cloudflare shows "Error 526" (Invalid SSL Certificate):**
- Ensure you selected **Cloudflare Origin CA** mode (not Managed Externally)
- Check that your Cloudflare SSL/TLS mode is set to **Full (Strict)**
- Verify the Origin CA certificate has not expired

**Browser shows "Not Secure" despite having SSL:**
- Some pages may load images or scripts over HTTP (mixed content). Check your browser's developer console for mixed content warnings.
- Ensure your site URL in Settings uses `https://`
