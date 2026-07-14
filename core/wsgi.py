"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

# Force core.settings - prevent bypass via DJANGO_SETTINGS_MODULE override
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

# =============================================================================
# Code Integrity Verification
# =============================================================================
# In production (protected builds), verify that compiled files haven't been
# tampered with before starting the application.
#
# Set SPWIG_SKIP_INTEGRITY_CHECK=true to disable (e.g., for development)
# =============================================================================
if not os.environ.get("SPWIG_SKIP_INTEGRITY_CHECK"):
    try:
        from core.integrity_check import verify_or_die

        # Verify integrity of compiled files against manifest
        verify_or_die(os.path.dirname(os.path.dirname(__file__)))
    except ImportError:
        # integrity_check module not present - likely unprotected build
        pass
    except Exception as e:
        # Log but don't crash for other errors (manifest may not exist in dev)
        import sys

        print(f"Integrity check warning: {e}", file=sys.stderr)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
