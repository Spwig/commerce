"""
Domain Service — Orchestrator

Coordinates the full domain + SSL configuration pipeline:
1. Validate DNS resolution
2. Write NGINX config (HTTP first, for ACME challenges)
3. Reload NGINX
4. Obtain SSL certificate
5. Write NGINX config (HTTPS)
6. Reload NGINX again
7. Update ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS in .env
8. Sync domain to SiteSettings.site_url and Site.domain
9. Update DynamicAllowedHostsMiddleware cache
10. Verify site reachability
"""

import logging
import os
import socket
import urllib.error
import urllib.request

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from domain_ssl.models import DomainConfiguration
from . import docker_service, nginx_service, ssl_service

logger = logging.getLogger(__name__)

# Cache key for dynamic ALLOWED_HOSTS
DOMAIN_CACHE_KEY = 'domain_ssl:current_domain'
DOMAIN_CACHE_TTL = 300  # 5 minutes


def validate_dns(domain):
    """
    Check if a domain resolves via DNS.

    Returns:
        dict with 'valid', 'resolved_ips', and optionally 'error'
    """
    try:
        results = socket.getaddrinfo(domain, None, socket.AF_INET)
        ips = list({r[4][0] for r in results})
        return {
            'valid': len(ips) > 0,
            'resolved_ips': ips,
        }
    except socket.gaierror as e:
        return {
            'valid': False,
            'resolved_ips': [],
            'error': str(e),
        }


def verify_reachability(domain, use_https=False, timeout=10):
    """
    Verify the site is reachable at the configured domain after changes.

    Makes an HTTP(S) request to the domain and checks for a non-error
    response. Uses a short timeout since the server should respond quickly.

    Returns:
        (reachable, message) tuple
    """
    import ssl as _ssl

    protocol = 'https' if use_https else 'http'
    url = f'{protocol}://{domain}/'

    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Spwig-HealthCheck/1.0')

        # For self-signed certs, skip verification during health check
        ctx = None
        if use_https:
            ctx = _ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = _ssl.CERT_NONE

        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            if resp.status < 500:
                return True, f'Site reachable (HTTP {resp.status})'
            return False, f'Server error (HTTP {resp.status})'
    except urllib.error.HTTPError as e:
        # 3xx, 4xx are fine — the site is responding
        if e.code < 500:
            return True, f'Site reachable (HTTP {e.code})'
        return False, f'Server error (HTTP {e.code})'
    except urllib.error.URLError as e:
        return False, f'Site unreachable: {e.reason}'
    except Exception as e:
        return False, f'Reachability check failed: {e}'


def get_server_ip():
    """
    Detect the server's public (external) IP address.

    Strategy:
    1. Check cache first (avoids repeated external calls)
    2. Cloud provider metadata APIs (instant, no egress)
    3. External "what's my IP" services (works behind NAT)
    4. UDP socket trick as last resort (returns local IP on NAT'd hosts)
    """
    cached = cache.get('domain_ssl:server_public_ip')
    if cached:
        return cached

    ip = None

    # 1. Cloud provider metadata (fast, free, no NAT issues)
    for url in [
        'http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address',  # DigitalOcean
        'http://169.254.169.254/latest/meta-data/public-ipv4',  # AWS
        'http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip',  # GCP
    ]:
        try:
            headers = {'Metadata': 'true', 'Metadata-Flavor': 'Google'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=2) as resp:
                candidate = resp.read().decode().strip()
                if candidate and not candidate.startswith(('10.', '172.', '192.168.')):
                    ip = candidate
                    break
        except Exception:
            continue

    # 2. External IP detection services (works behind NAT)
    if not ip:
        for url in [
            'https://checkip.amazonaws.com',
            'https://api.ipify.org',
            'https://ifconfig.me/ip',
        ]:
            try:
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'Spwig/1.0',
                })
                with urllib.request.urlopen(req, timeout=5) as resp:
                    candidate = resp.read().decode().strip()
                    if candidate:
                        # Basic validation: looks like an IPv4 address
                        parts = candidate.split('.')
                        if len(parts) == 4 and all(
                            p.isdigit() and 0 <= int(p) <= 255 for p in parts
                        ):
                            ip = candidate
                            break
            except Exception:
                continue

    # 3. Last resort: UDP socket (returns local/NAT IP, but better than nothing)
    if not ip:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
            finally:
                s.close()
        except Exception:
            pass

    if ip:
        cache.set('domain_ssl:server_public_ip', ip, timeout=300)

    return ip


def configure_domain(domain, ssl_mode, email='', cloudflare_token='',
                     cloudflare_zone_id='', custom_cert_pem='',
                     custom_key_pem=''):
    """
    Full domain configuration pipeline. Called by the Celery task.

    Args:
        domain: FQDN to configure
        ssl_mode: One of DomainConfiguration.SSLMode values
        email: Admin email for Let's Encrypt
        cloudflare_token: Cloudflare API token (for DNS-01/Origin CA)
        cloudflare_zone_id: Cloudflare zone ID
        custom_cert_pem: PEM certificate content (for custom mode)
        custom_key_pem: PEM key content (for custom mode)

    Returns:
        (success, message) tuple
    """
    config = DomainConfiguration.get_instance()

    # Accumulate non-fatal warnings (set_status clears last_error,
    # so we preserve warnings across status transitions)
    warnings = []

    # Store previous domain for rollback
    if config.domain and config.domain != domain:
        config.previous_domain = config.domain

    config.domain = domain
    config.ssl_mode = ssl_mode
    config.admin_email = email
    if cloudflare_token:
        config.cloudflare_api_token = cloudflare_token
    if cloudflare_zone_id:
        config.cloudflare_zone_id = cloudflare_zone_id
    config.save()

    # Step 1: Validate DNS
    config.set_status(DomainConfiguration.Status.VALIDATING_DNS)
    if domain:
        dns_result = validate_dns(domain)
        if not dns_result['valid']:
            config.set_error(
                f'DNS validation failed: {domain} does not resolve. '
                f'Please ensure your A record points to this server.'
            )
            return False, config.last_error

    # Step 2: Write initial NGINX config (HTTP with ACME challenge support)
    config.set_status(DomainConfiguration.Status.CONFIGURING)
    try:
        nginx_service.write_http_config(domain)
    except Exception as e:
        config.set_error(f'Failed to write NGINX config: {e}')
        return False, config.last_error

    # Step 3: Reload NGINX with HTTP config
    try:
        ok, output = docker_service.reload_nginx()
        if not ok:
            config.set_error(f'NGINX reload failed: {output}')
            return False, config.last_error
    except Exception as e:
        config.set_error(f'NGINX reload failed: {e}')
        return False, config.last_error

    # Step 4: Obtain SSL certificate (if SSL mode requires it)
    if ssl_mode == DomainConfiguration.SSLMode.MANAGED_EXTERNALLY:
        # External SSL — verify upstream HTTPS works, no local cert needed
        config.set_status(DomainConfiguration.Status.OBTAINING_CERT)
        if domain:
            ok, cert_info = ssl_service.verify_external_ssl(domain)
            if ok:
                config.cert_domain = cert_info.get('domain', '')
                config.cert_issuer = cert_info.get('issuer', '')
                config.cert_expires_at = cert_info.get('expires_at')
                config.cert_obtained_at = timezone.now()
                config.is_wildcard = cert_info.get('is_wildcard', False)
                config.save()
            else:
                # Not a hard failure — upstream may not be configured yet
                error_msg = cert_info.get('error', 'Unknown error')
                logger.warning(
                    'External SSL verification failed for %s: %s',
                    domain, error_msg,
                )
                warnings.append(
                    f'Warning: External SSL check failed — {error_msg}'
                )
        # Skip steps 5 (no local SSL nginx config needed for external SSL)

    elif ssl_mode != DomainConfiguration.SSLMode.NONE:
        config.set_status(DomainConfiguration.Status.OBTAINING_CERT)

        if ssl_mode == DomainConfiguration.SSLMode.LETSENCRYPT:
            ok, msg = ssl_service.obtain_letsencrypt_cert(domain, email)
        elif ssl_mode == DomainConfiguration.SSLMode.SELF_SIGNED:
            ok, msg = ssl_service.generate_self_signed_cert(domain)
        elif ssl_mode in (
            DomainConfiguration.SSLMode.CUSTOM,
            DomainConfiguration.SSLMode.CLOUDFLARE_ORIGIN,
        ):
            # Certs are uploaded separately via upload-cert endpoint.
            # Only re-save if cert data was passed inline (e.g. API call).
            if custom_cert_pem and custom_key_pem:
                ok, msg = ssl_service.save_custom_cert(custom_cert_pem, custom_key_pem)
            else:
                # Verify certs exist from the prior upload step
                cert_path = os.path.join(ssl_service.CERTS_DIR, 'fullchain.pem')
                if os.path.exists(cert_path) and os.path.getsize(cert_path) > 0:
                    ok, msg = True, 'Using previously uploaded certificate'
                else:
                    ok, msg = False, 'No certificate found. Please upload your certificate and key.'
        else:
            # DNS-01 — future implementation
            ok, msg = False, f'SSL mode {ssl_mode} is not yet supported'

        if not ok:
            config.set_error(msg)
            return False, msg

        # Parse certificate metadata
        cert_info = ssl_service.parse_certificate()
        if cert_info:
            config.cert_domain = cert_info.get('domain', '')
            config.cert_issuer = cert_info.get('issuer', '')
            config.cert_expires_at = cert_info.get('expires_at')
            config.cert_obtained_at = timezone.now()
            config.is_wildcard = cert_info.get('is_wildcard', False)
            config.save()

        # Step 5: Write SSL NGINX config
        try:
            nginx_service.write_ssl_config(domain, ssl_mode=ssl_mode)
        except Exception as e:
            config.set_error(f'Failed to write SSL NGINX config: {e}')
            return False, config.last_error

    # Step 6: Reload NGINX with final config
    config.set_status(DomainConfiguration.Status.RELOADING)
    try:
        ok, output = docker_service.reload_nginx()
        if not ok:
            config.set_error(f'NGINX reload failed: {output}')
            return False, config.last_error
    except Exception as e:
        config.set_error(f'NGINX reload failed: {e}')
        return False, config.last_error

    # Step 7: Update .env file
    _update_env_for_domain(domain, ssl_mode)

    # Step 8: Sync domain to SiteSettings.site_url and Site.domain
    if domain:
        _sync_domain_to_site_settings(domain, ssl_mode)

    # Step 9: Update cache for DynamicAllowedHostsMiddleware
    cache.set(DOMAIN_CACHE_KEY, domain, DOMAIN_CACHE_TTL)

    # Step 10: Verify the site is reachable on the new domain
    # For managed_externally, the local NGINX serves HTTP — the upstream
    # proxy handles HTTPS, so we verify HTTP reachability here.
    if domain:
        reachable, reach_msg = verify_reachability(
            domain,
            use_https=(ssl_mode not in (
                DomainConfiguration.SSLMode.NONE,
                DomainConfiguration.SSLMode.MANAGED_EXTERNALLY,
            )),
        )
        if not reachable:
            logger.warning(
                'Post-config reachability check failed for %s: %s',
                domain, reach_msg,
            )
            warnings.append(f'Warning: {reach_msg}')

    # Done — apply accumulated warnings
    config.set_status(DomainConfiguration.Status.IDLE)
    if warnings:
        config.last_error = '; '.join(warnings)
        config.save(update_fields=['last_error', 'updated_at'])

    logger.info('Domain configuration complete: %s (%s)', domain, ssl_mode)

    if warnings:
        return True, f'Domain configured with warnings: {config.last_error}'
    return True, 'Domain configured successfully'


def get_current_domain():
    """
    Get the currently configured domain. Used by middleware.
    Reads from cache first, then DB.
    """
    domain = cache.get(DOMAIN_CACHE_KEY)
    if domain is not None:
        return domain

    try:
        config = DomainConfiguration.objects.filter(pk=1).values_list(
            'domain', flat=True
        ).first()
        domain = config or ''
        cache.set(DOMAIN_CACHE_KEY, domain, DOMAIN_CACHE_TTL)
        return domain
    except Exception:
        return ''


def _sync_domain_to_site_settings(domain, ssl_mode):
    """
    Sync the configured domain to SiteSettings.site_url and Site.domain.

    SiteSettings.site_url is the master — set by the setup wizard initially,
    then kept in sync whenever the domain changes via domain_ssl.
    Site.domain (django.contrib.sites) is used by allauth for OAuth callbacks.
    """
    protocol = 'https' if ssl_mode != DomainConfiguration.SSLMode.NONE else 'http'
    site_url = f'{protocol}://{domain}'

    try:
        from core.models import SiteSettings
        site_settings = SiteSettings.objects.filter(pk=1).first()
        if site_settings:
            site_settings.site_url = site_url
            site_settings.save(update_fields=['site_url'])
            logger.info('Updated SiteSettings.site_url to %s', site_url)
    except Exception as e:
        logger.warning('Failed to update SiteSettings.site_url: %s', e)

    try:
        from django.contrib.sites.models import Site
        site = Site.objects.filter(pk=1).first()
        if site:
            site.domain = domain
            site.save(update_fields=['domain'])
            logger.info('Updated Site.domain to %s', domain)
    except Exception as e:
        logger.warning('Failed to update Site.domain: %s', e)


def _update_env_for_domain(domain, ssl_mode):
    """Update ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS in .env."""
    if not domain:
        return

    # Build ALLOWED_HOSTS value
    hosts = f'localhost,127.0.0.1,{domain}'
    docker_service.update_env_file('ALLOWED_HOSTS', hosts)

    # Build CSRF_TRUSTED_ORIGINS
    protocol = 'https' if ssl_mode != DomainConfiguration.SSLMode.NONE else 'http'
    origins = f'{protocol}://{domain},http://{domain}'
    docker_service.update_env_file('DJANGO_CSRF_TRUSTED_ORIGINS', origins)
