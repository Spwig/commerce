"""
IP utility functions for GeoIP
"""

import ipaddress
import logging

logger = logging.getLogger(__name__)


def get_client_ip(request) -> str:
    """
    Get the client's real IP address from the request

    Args:
        request: Django request object

    Returns:
        IP address as string or None
    """
    # List of headers to check for the real IP
    # Cloudflare headers first (they contain the actual visitor IP),
    # before X-Real-IP/X-Forwarded-For which may contain edge server IPs
    headers_to_check = [
        "HTTP_CF_CONNECTING_IP",  # Cloudflare (actual visitor IP)
        "HTTP_TRUE_CLIENT_IP",  # Cloudflare Enterprise
        "HTTP_X_REAL_IP",
        "HTTP_X_FORWARDED_FOR",
        "HTTP_X_CLIENT_IP",
        "HTTP_X_CLUSTER_CLIENT_IP",
        "HTTP_FORWARDED_FOR",
        "HTTP_FORWARDED",
        "REMOTE_ADDR",
    ]

    for header in headers_to_check:
        ip = request.META.get(header)
        if ip:
            # X-Forwarded-For can contain multiple IPs
            if "," in ip:
                ip = ip.split(",")[0].strip()

            # Validate IP
            if is_valid_ip(ip) and not is_private_ip(ip):
                return ip

    # Fallback to REMOTE_ADDR
    ip = request.META.get("REMOTE_ADDR")
    if ip and is_valid_ip(ip):
        # Return even if private (for development)
        return ip

    return None


def is_valid_ip(ip: str) -> bool:
    """
    Check if IP address is valid

    Args:
        ip: IP address string

    Returns:
        True if valid, False otherwise
    """
    if not ip:
        return False

    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_private_ip(ip: str) -> bool:
    """
    Check if IP address is private/internal

    Args:
        ip: IP address string

    Returns:
        True if private, False otherwise
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        return False


def get_ip_prefix(ip: str, ipv4_prefix_length: int = 24, ipv6_prefix_length: int = 48) -> str:
    """
    Get IP prefix for caching

    Args:
        ip: IP address
        ipv4_prefix_length: Prefix length for IPv4 (default /24)
        ipv6_prefix_length: Prefix length for IPv6 (default /48)

    Returns:
        IP prefix string
    """
    try:
        addr = ipaddress.ip_address(ip)
        if addr.version == 4:
            network = ipaddress.ip_network(f"{ip}/{ipv4_prefix_length}", strict=False)
        else:
            network = ipaddress.ip_network(f"{ip}/{ipv6_prefix_length}", strict=False)
        return str(network)
    except Exception as e:
        logger.warning(f"Failed to get IP prefix for {ip}: {e}")
        return ip


def anonymize_ip(ip: str) -> str:
    """
    Anonymize IP address for privacy

    Args:
        ip: IP address

    Returns:
        Anonymized IP address
    """
    try:
        addr = ipaddress.ip_address(ip)
        if addr.version == 4:
            # Zero out last octet
            parts = str(addr).split(".")
            parts[3] = "0"
            return ".".join(parts)
        else:
            # Zero out last 80 bits for IPv6
            network = ipaddress.ip_network(f"{ip}/48", strict=False)
            return str(network.network_address)
    except Exception as e:
        logger.error(f"Failed to anonymize IP {ip}: {e}")
        return ip


def ip_to_int(ip: str) -> int:
    """
    Convert IP address to integer

    Args:
        ip: IP address

    Returns:
        Integer representation of IP
    """
    try:
        return int(ipaddress.ip_address(ip))
    except ValueError:
        return 0


def int_to_ip(ip_int: int, version: int = 4) -> str:
    """
    Convert integer to IP address

    Args:
        ip_int: Integer representation of IP
        version: IP version (4 or 6)

    Returns:
        IP address string
    """
    try:
        if version == 4:
            return str(ipaddress.IPv4Address(ip_int))
        else:
            return str(ipaddress.IPv6Address(ip_int))
    except ValueError:
        return ""


def is_in_range(ip: str, ip_range: str) -> bool:
    """
    Check if IP is in a given range

    Args:
        ip: IP address
        ip_range: IP range in CIDR notation

    Returns:
        True if IP is in range, False otherwise
    """
    try:
        addr = ipaddress.ip_address(ip)
        network = ipaddress.ip_network(ip_range, strict=False)
        return addr in network
    except ValueError:
        return False


def get_ip_version(ip: str) -> int:
    """
    Get IP version (4 or 6)

    Args:
        ip: IP address

    Returns:
        4 for IPv4, 6 for IPv6, 0 for invalid
    """
    try:
        return ipaddress.ip_address(ip).version
    except ValueError:
        return 0
