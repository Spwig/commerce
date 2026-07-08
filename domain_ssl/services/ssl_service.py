"""
SSL Service for Domain & SSL

Handles certificate lifecycle: obtain, validate, parse, and renew.
Supports multiple SSL modes via the DomainConfiguration model.
"""

import logging
import os
import re
import subprocess
from datetime import datetime, timezone as dt_timezone

from django.utils import timezone

logger = logging.getLogger(__name__)

# Domain validation for certificate operations
_DOMAIN_RE = re.compile(
    r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*\.[A-Za-z]{2,}$'
)

# Regex to extract key=value from openssl output (handles "CN = value" and "CN=value")
_OPENSSL_KV_RE = re.compile(r'(?:^|,\s*)(\w+)\s*=\s*([^,\n]+)')

# Paths inside the shop/celery container
CERTS_DIR = os.environ.get('CERTS_DIR', '/app/certs')
CERTBOT_WEBROOT = os.environ.get('CERTBOT_WEBROOT', '/app/certbot_webroot')

# Host paths (for Docker-in-Docker certbot runs)
# These match the bind-mount source paths on the host
HOST_CERTS_DIR = os.environ.get('HOST_CERTS_DIR', '/opt/spwig/certs')
HOST_CERTBOT_WEBROOT = os.environ.get('HOST_CERTBOT_WEBROOT', '/opt/spwig/certbot-webroot')


def obtain_letsencrypt_cert(domain, email):
    """
    Obtain a Let's Encrypt certificate via HTTP-01 challenge.

    Runs certbot as a one-off Docker container. The NGINX config must
    already have the ACME challenge location configured and reloaded.

    Returns:
        (success, message) tuple
    """
    from . import docker_service

    logger.info('Obtaining Let\'s Encrypt certificate for %s', domain)

    # Ensure certbot webroot exists
    os.makedirs(CERTBOT_WEBROOT, exist_ok=True)

    success, output = docker_service.run_certbot(
        domain=domain,
        email=email,
        webroot_path=HOST_CERTBOT_WEBROOT,
        certs_path=HOST_CERTS_DIR,
    )

    if success:
        # Copy Let's Encrypt certs to our standard cert location
        _link_letsencrypt_certs(domain)
        return True, 'Certificate obtained successfully'
    else:
        return False, f'Certbot failed: {output}'


def renew_certificates(domain=''):
    """
    Renew all certificates managed by certbot.

    Args:
        domain: Domain name, used to re-link LE certs to standard location

    Returns:
        (success, message) tuple
    """
    from . import docker_service

    success, output = docker_service.run_certbot_renew(
        certs_path=HOST_CERTS_DIR,
        webroot_path=HOST_CERTBOT_WEBROOT,
    )

    if success:
        # Re-link renewed certs to standard location
        if domain:
            _link_letsencrypt_certs(domain)

        # Reload NGINX to pick up renewed certs
        docker_service.reload_nginx()
        return True, 'Renewal completed'
    else:
        return False, f'Renewal failed: {output}'


def generate_self_signed_cert(domain):
    """
    Generate a self-signed certificate for development/testing.

    Returns:
        (success, message) tuple
    """
    # Validate domain to prevent subject injection
    if not _DOMAIN_RE.match(domain):
        return False, f'Invalid domain format: {domain}'

    cert_dir = CERTS_DIR
    os.makedirs(cert_dir, exist_ok=True)

    cert_path = os.path.join(cert_dir, 'fullchain.pem')
    key_path = os.path.join(cert_dir, 'privkey.pem')

    cmd = [
        'openssl', 'req', '-x509', '-nodes',
        '-days', '365',
        '-newkey', 'rsa:2048',
        '-keyout', key_path,
        '-out', cert_path,
        '-subj', f'/CN={domain}',
        '-addext', f'subjectAltName=DNS:{domain},DNS:localhost,IP:127.0.0.1',
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return False, f'OpenSSL failed: {result.stderr}'

        os.chmod(key_path, 0o600)
        os.chmod(cert_path, 0o644)

        logger.info('Generated self-signed certificate for %s', domain)
        return True, 'Self-signed certificate generated'
    except Exception as e:
        return False, str(e)


def save_custom_cert(cert_pem, key_pem):
    """
    Save a custom certificate and key uploaded by the merchant.

    Returns:
        (success, message) tuple
    """
    cert_dir = CERTS_DIR
    os.makedirs(cert_dir, exist_ok=True)

    cert_path = os.path.join(cert_dir, 'fullchain.pem')
    key_path = os.path.join(cert_dir, 'privkey.pem')

    try:
        with open(cert_path, 'w') as f:
            f.write(cert_pem)
        with open(key_path, 'w') as f:
            f.write(key_pem)

        os.chmod(key_path, 0o600)
        os.chmod(cert_path, 0o644)

        return True, 'Custom certificate saved'
    except Exception as e:
        return False, str(e)


def parse_certificate(cert_path=None):
    """
    Parse a PEM certificate and return metadata.

    Returns:
        dict with domain, issuer, expires_at, is_wildcard, or None on failure
    """
    if cert_path is None:
        cert_path = os.path.join(CERTS_DIR, 'fullchain.pem')

    if not os.path.exists(cert_path):
        return None

    try:
        # Use openssl to extract certificate info
        result = subprocess.run(
            ['openssl', 'x509', '-in', cert_path, '-noout',
             '-subject', '-issuer', '-dates'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return None

        output = result.stdout
        info = {}

        for line in output.strip().split('\n'):
            if line.startswith('subject='):
                content = line.split('=', 1)[1]
                kvs = dict(_OPENSSL_KV_RE.findall(content))
                cn = kvs.get('CN', '').strip()
                if cn:
                    info['domain'] = cn
            elif line.startswith('issuer='):
                content = line.split('=', 1)[1]
                kvs = dict(_OPENSSL_KV_RE.findall(content))
                info['issuer'] = (
                    kvs.get('O', '').strip()
                    or kvs.get('CN', '').strip()
                )
            elif line.startswith('notAfter='):
                date_str = line.split('=', 1)[1].strip()
                try:
                    clean_date = date_str.replace(' GMT', '').replace(' UTC', '')
                    expires = datetime.strptime(
                        clean_date, '%b %d %H:%M:%S %Y'
                    )
                    info['expires_at'] = expires.replace(
                        tzinfo=dt_timezone.utc
                    )
                except ValueError:
                    logger.warning(
                        'Could not parse certificate date: %s', date_str
                    )

        info['is_wildcard'] = info.get('domain', '').startswith('*.')
        return info if 'domain' in info else None

    except Exception as e:
        logger.error('Failed to parse certificate: %s', e)
        return None


def verify_external_ssl(domain, timeout=10):
    """
    Verify that HTTPS works on a domain managed by an external proxy
    (e.g., Cloudflare, load balancer). Connects to the domain on port 443,
    retrieves the TLS certificate, and parses its metadata.

    Returns:
        (valid, info_dict) where info_dict has 'domain', 'issuer',
        'expires_at', 'is_wildcard'. If invalid, info_dict has 'error'.
    """
    import ssl
    import socket as _socket

    info = {}

    try:
        # Connect and get the PEM certificate from the remote server
        pem_cert = ssl.get_server_certificate((domain, 443), timeout=timeout)
    except (_socket.timeout, _socket.gaierror, ConnectionRefusedError, OSError) as e:
        return False, {'error': f'Cannot connect to {domain}:443 — {e}'}
    except Exception as e:
        return False, {'error': f'SSL connection failed: {e}'}

    # Parse the PEM certificate using openssl (available in the container)
    try:
        result = subprocess.run(
            ['openssl', 'x509', '-noout', '-subject', '-issuer', '-dates'],
            input=pem_cert, capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return False, {'error': f'Certificate parsing failed: {result.stderr}'}

        for line in result.stdout.strip().split('\n'):
            if line.startswith('subject='):
                content = line.split('=', 1)[1]
                kvs = dict(_OPENSSL_KV_RE.findall(content))
                cn = kvs.get('CN', '').strip()
                if cn:
                    info['domain'] = cn
            elif line.startswith('issuer='):
                content = line.split('=', 1)[1]
                kvs = dict(_OPENSSL_KV_RE.findall(content))
                info['issuer'] = (
                    kvs.get('O', '').strip()
                    or kvs.get('CN', '').strip()
                )
            elif line.startswith('notAfter='):
                date_str = line.split('=', 1)[1].strip()
                try:
                    clean_date = date_str.replace(' GMT', '').replace(' UTC', '')
                    expires = datetime.strptime(clean_date, '%b %d %H:%M:%S %Y')
                    info['expires_at'] = expires.replace(tzinfo=dt_timezone.utc)
                except ValueError:
                    pass

        info['is_wildcard'] = info.get('domain', '').startswith('*.')

        # Check validity
        expires_at = info.get('expires_at')
        if expires_at and expires_at > datetime.now(dt_timezone.utc):
            return True, info
        elif expires_at:
            info['error'] = 'Certificate has expired'
            return False, info
        else:
            info['error'] = 'Could not determine certificate expiry'
            return False, info

    except Exception as e:
        return False, {'error': f'Certificate parsing failed: {e}'}


def _link_letsencrypt_certs(domain):
    """
    Copy/link Let's Encrypt certs to standard location.
    Certbot stores certs at /etc/letsencrypt/live/{domain}/
    """
    le_dir = os.path.join(CERTS_DIR, 'live', domain)
    if not os.path.isdir(le_dir):
        # Certs may be at the top level already
        return

    cert_dir = CERTS_DIR
    for filename in ('fullchain.pem', 'privkey.pem'):
        src = os.path.join(le_dir, filename)
        dst = os.path.join(cert_dir, filename)
        if os.path.exists(src):
            # Copy rather than symlink for simplicity across containers
            with open(src, 'r') as f:
                content = f.read()
            with open(dst, 'w') as f:
                f.write(content)
