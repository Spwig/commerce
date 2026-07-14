"""
Management command to run the built-in SMTP server (alias for start_smtp_server).

This is used by supervisor in Docker to manage the SMTP server process.

Usage:
    ./manage.py run_smtp_server
"""

from email_system.management.commands.start_smtp_server import (
    Command,  # noqa: F401  # re-export for Django's command discovery
)

# This is just an alias - all functionality is in start_smtp_server
