"""
GeoIP utility functions

Re-exports from the canonical ip_utils module.
"""
from .utils.ip_utils import (
    get_client_ip,
    is_valid_ip,
    is_private_ip,
    get_ip_prefix,
    anonymize_ip,
    ip_to_int,
    int_to_ip,
    is_in_range,
    get_ip_version,
)

__all__ = [
    'get_client_ip',
    'is_valid_ip',
    'is_private_ip',
    'get_ip_prefix',
    'anonymize_ip',
    'ip_to_int',
    'int_to_ip',
    'is_in_range',
    'get_ip_version',
]
