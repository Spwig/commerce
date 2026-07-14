"""
GeoIP utility functions

Re-exports from the canonical ip_utils module.
"""

from .utils.ip_utils import (
    anonymize_ip,
    get_client_ip,
    get_ip_prefix,
    get_ip_version,
    int_to_ip,
    ip_to_int,
    is_in_range,
    is_private_ip,
    is_valid_ip,
)

__all__ = [
    "get_client_ip",
    "is_valid_ip",
    "is_private_ip",
    "get_ip_prefix",
    "anonymize_ip",
    "ip_to_int",
    "int_to_ip",
    "is_in_range",
    "get_ip_version",
]
