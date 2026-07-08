---
slug: domain-ssl-configuration
title_i18n_key: Domain & SSL Configuration
category: getting-started
component: management
keywords:
  - domain
  - SSL
  - HTTPS
  - certificate
  - Let's Encrypt
  - custom domain
  - configure domain
  - DNS
  - A record
  - self-signed
  - renew certificate
url_patterns: []
related:
  - installation-guide
  - system-requirements
  - store-settings
published: true
---

This guide explains how to connect a custom domain to your Spwig store and set up SSL certificates for secure HTTPS access. You can configure a domain during installation or add one later.

## Adding a domain after installation

If you installed Spwig without a domain (using the server's IP address), you can add one at any time.

### Step 1: Set up DNS

With your domain registrar or DNS provider:

1. Create an **A record** pointing your domain (or subdomain) to your server's IP address
2. If using a subdomain like `shop.example.com`, create the A record for `shop`
3. Wait for DNS propagation — this typically takes 5–60 minutes

Verify the DNS record is working:

```bash
dig +short shop.example.com
```

This should return your server's IP address.

### Step 2: Run the domain configuration script

SSH into your server and navigate to your Spwig installation directory:

```bash
./configure-domain.sh
```

The script will:

1. Ask for your domain name
2. Verify DNS is pointing to your server
3. Update the store's configuration
4. Obtain a free SSL certificate from Let's Encrypt
5. Configure the web server to use HTTPS
6. Restart the relevant services

Your store is now accessible at `https://yourdomain.com`.

### Step 3: Update store settings

After adding a domain, log into your admin panel and go to **Store Settings**. Verify that the **Store URL** matches your new domain. This ensures emails, invoices, and links use the correct address.

## SSL certificates

### Automatic SSL (Let's Encrypt)

In **standalone mode**, the installer automatically obtains a free SSL certificate from Let's Encrypt. These certificates:

- Are trusted by all major browsers
- Are valid for 90 days
- Renew automatically — a renewal check runs daily, and certificates are renewed when they have less than 30 days remaining
- Cover your exact domain (e.g. `shop.example.com`)

You do not need to manage renewal manually.

### Self-signed certificates

In some situations, Spwig uses a self-signed certificate instead:

- **Local mode** installations (development/testing)
- When Let's Encrypt cannot reach your server (firewall blocking port 80, DNS not yet propagated)
- When no domain is configured (IP-only access)

Self-signed certificates encrypt traffic but are not trusted by browsers — visitors will see a security warning. This is acceptable for testing but should not be used in production.

### Sidecar mode SSL

In **sidecar mode**, your existing web server (Apache, Nginx, Caddy, etc.) handles SSL termination. Spwig runs on an HTTP port behind your proxy. Configure SSL on your main web server as you normally would.

The installer generates a proxy configuration block you can add to your web server. For Nginx, it looks similar to:

```nginx
location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## Changing your domain

To switch to a different domain:

1. Set up DNS for the new domain (A record pointing to your server)
2. Run `./configure-domain.sh` again with the new domain
3. The script updates all configuration, obtains a new certificate, and restarts services
4. Update **Store Settings** in the admin panel with the new URL

Your old domain will stop working once the configuration is updated.

## Troubleshooting

### "DNS validation failed"

The configure-domain script checks that your domain points to your server before requesting a certificate. If this check fails:

- Verify the A record is correct with `dig +short yourdomain.com`
- Wait a few more minutes for DNS propagation
- Check that you are configuring the exact domain or subdomain (not a wildcard)

### "Let's Encrypt rate limit reached"

Let's Encrypt limits certificate requests to 5 per domain per week. If you hit this limit:

- Wait 7 days before trying again
- Use a different subdomain in the meantime
- The store remains accessible via HTTP or with a self-signed certificate while you wait

### "Port 80 is not reachable"

Let's Encrypt must connect to your server on port 80 to verify domain ownership. Ensure:

- Your firewall allows inbound TCP on port 80
- No other application is blocking port 80
- Your cloud provider's security group or network firewall allows port 80

### Certificate renewal failures

If automatic renewal fails, the certificate will expire after 90 days. To renew manually:

```bash
docker exec spwig_nginx certbot renew
docker exec spwig_nginx nginx -s reload
```

Check the renewal log for details if this fails. The most common cause is port 80 being blocked by a firewall change after the initial installation.
