"""
Built-in SMTP Server for Spwig E-commerce Platform

This package provides a built-in SMTP server with DKIM signing capabilities
for sending transactional emails. The server is designed to work out-of-the-box
with zero configuration and integrates with Postfix as a relay MTA.

Components:
- dkim_handler: DKIM key management and email signing
- server: aiosmtpd-based SMTP server
- postfix: Postfix integration and configuration
"""

__version__ = "1.0.0"
