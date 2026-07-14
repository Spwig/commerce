"""
Domain Extraction and Validation Utilities

Utilities for extracting and validating email domains for DNS configuration.
"""

import logging
import re

import requests

logger = logging.getLogger(__name__)


def extract_domain(email: str) -> str | None:
    """
    Extract domain from email address.

    Args:
        email: Email address (e.g., 'shop@example.com')

    Returns:
        Domain name (e.g., 'example.com') or None if invalid

    Examples:
        >>> extract_domain('shop@example.com')
        'example.com'
        >>> extract_domain('user+tag@subdomain.example.com')
        'subdomain.example.com'
    """
    if not email or "@" not in email:
        return None

    try:
        # Split on @ and get domain part
        parts = email.rsplit("@", 1)
        if len(parts) != 2:
            return None

        domain = parts[1].strip().lower()

        # Basic validation
        if not domain or "." not in domain:
            return None

        # Remove any trailing/leading dots
        domain = domain.strip(".")

        return domain if domain else None

    except Exception:
        return None


def normalize_domain(domain: str) -> str:
    """
    Normalize domain name for consistent comparison.

    Args:
        domain: Domain name (e.g., 'WWW.EXAMPLE.COM', 'example.com.')

    Returns:
        Normalized domain (e.g., 'example.com')

    Examples:
        >>> normalize_domain('WWW.EXAMPLE.COM')
        'example.com'
        >>> normalize_domain('  Example.Com.  ')
        'example.com'
        >>> normalize_domain('example.com.')
        'example.com'
    """
    if not domain:
        return ""

    # Lowercase and strip whitespace/dots
    domain = domain.lower().strip().strip(".")

    # Remove www prefix if present
    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def validate_domain(domain: str) -> bool:
    """
    Validate domain name format.

    Args:
        domain: Domain name to validate

    Returns:
        True if domain format is valid, False otherwise

    Examples:
        >>> validate_domain('example.com')
        True
        >>> validate_domain('sub.example.com')
        True
        >>> validate_domain('invalid')
        False
        >>> validate_domain('example..com')
        False
    """
    if not domain:
        return False

    # Normalize first
    domain = normalize_domain(domain)

    # Basic length check
    if len(domain) < 4 or len(domain) > 255:
        return False

    # Must contain at least one dot
    if "." not in domain:
        return False

    # Regex pattern for valid domain
    # Allows: letters, numbers, hyphens, dots
    # Must start/end with alphanumeric
    # TLD must be at least 2 characters
    pattern = r"^([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$"

    if not re.match(pattern, domain):
        return False

    # No consecutive dots
    if ".." in domain:
        return False

    # Each label (part between dots) must be valid
    labels = domain.split(".")
    for label in labels:
        # Label length check (1-63 characters)
        if not label or len(label) > 63:
            return False

        # Label can't start or end with hyphen
        if label.startswith("-") or label.endswith("-"):
            return False

    return True


def get_base_domain(domain: str) -> str | None:
    """
    Extract base domain from subdomain.

    Args:
        domain: Full domain (e.g., 'mail.shop.example.com')

    Returns:
        Base domain (e.g., 'example.com') or None if invalid

    Examples:
        >>> get_base_domain('mail.shop.example.com')
        'example.com'
        >>> get_base_domain('example.com')
        'example.com'
        >>> get_base_domain('example.co.uk')
        'co.uk'  # Note: Doesn't handle complex TLDs perfectly

    Note:
        This is a simplified implementation. For production use with
        complex TLDs (co.uk, com.au, etc.), consider using the 'tldextract'
        library.
    """
    if not domain or not validate_domain(domain):
        return None

    domain = normalize_domain(domain)
    parts = domain.split(".")

    # If only 2 parts, it's already the base domain
    if len(parts) <= 2:
        return domain

    # Return last 2 parts (domain + TLD)
    # Note: This is simplified and doesn't handle .co.uk, .com.au, etc.
    return ".".join(parts[-2:])


def domains_match(domain1: str, domain2: str, strict: bool = False) -> bool:
    """
    Check if two domains match.

    Args:
        domain1: First domain
        domain2: Second domain
        strict: If True, require exact match. If False, allow base domain match.

    Returns:
        True if domains match, False otherwise

    Examples:
        >>> domains_match('example.com', 'EXAMPLE.COM')
        True
        >>> domains_match('mail.example.com', 'example.com', strict=False)
        True
        >>> domains_match('mail.example.com', 'example.com', strict=True)
        False
    """
    if not domain1 or not domain2:
        return False

    # Normalize both
    d1 = normalize_domain(domain1)
    d2 = normalize_domain(domain2)

    if strict:
        return d1 == d2
    else:
        # Check exact match first
        if d1 == d2:
            return True

        # Check if one is subdomain of the other
        base1 = get_base_domain(d1)
        base2 = get_base_domain(d2)

        return base1 == base2 if (base1 and base2) else False


def get_external_ip() -> str | None:
    """
    Detect the server's external (public) IP address.

    Uses multiple reliable external services to detect the public IP address.
    Tries multiple services for redundancy in case one is down.

    Returns:
        External IP address as string, or None if detection fails

    Examples:
        >>> get_external_ip()
        '203.0.113.45'

    Note:
        This function makes HTTP requests to external services.
        For production use, consider caching the result.
    """
    # List of reliable IP detection services
    # These services return just the IP address in plain text
    services = [
        "https://api.ipify.org",  # Most reliable
        "https://icanhazip.com",  # Cloudflare-backed
        "https://ifconfig.me/ip",  # Well-established
        "https://ident.me",  # Simple and fast
        "https://checkip.amazonaws.com",  # AWS-backed
    ]

    for service in services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                ip = response.text.strip()

                # Validate IP format (IPv4)
                if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", ip):
                    # Additional validation: each octet should be 0-255
                    octets = ip.split(".")
                    if all(0 <= int(octet) <= 255 for octet in octets):
                        logger.info(f"Detected external IP: {ip} (via {service})")
                        return ip

        except Exception as e:
            logger.debug(f"Failed to get IP from {service}: {e}")
            continue

    logger.warning("Failed to detect external IP from all services")
    return None


def is_private_ip(ip: str) -> bool:
    """
    Check if an IP address is private (RFC 1918).

    Args:
        ip: IP address to check

    Returns:
        True if IP is private, False otherwise

    Examples:
        >>> is_private_ip('192.168.1.1')
        True
        >>> is_private_ip('10.0.0.1')
        True
        >>> is_private_ip('203.0.113.1')
        False
    """
    if not ip:
        return False

    try:
        octets = [int(x) for x in ip.split(".")]

        # Private ranges:
        # 10.0.0.0 - 10.255.255.255
        # 172.16.0.0 - 172.31.255.255
        # 192.168.0.0 - 192.168.255.255
        # 127.0.0.0 - 127.255.255.255 (loopback)

        if octets[0] == 10:
            return True
        if octets[0] == 172 and 16 <= octets[1] <= 31:
            return True
        if octets[0] == 192 and octets[1] == 168:
            return True
        return octets[0] == 127

    except (ValueError, IndexError):
        return False
