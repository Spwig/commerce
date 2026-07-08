"""
Dynamic ALLOWED_HOSTS Middleware

Augments Django's static ALLOWED_HOSTS with the domain stored in
DomainConfiguration. This ensures the new domain works immediately
after configuration, before the container restarts with the updated .env.

Reads from cache (5 min TTL) with DB fallback.
"""

import logging

from django.conf import settings

logger = logging.getLogger(__name__)

# Track which dynamic domains we've added to avoid unbounded growth
_dynamic_hosts = set()


class DynamicAllowedHostsMiddleware:
    """
    Adds the configured domain from DomainConfiguration to ALLOWED_HOSTS
    so Django accepts requests on the new domain immediately.

    Must be placed after SecurityMiddleware and before CommonMiddleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Read host directly from META to avoid DisallowedHost from get_host()
        host = request.META.get('HTTP_HOST', request.META.get('SERVER_NAME', ''))
        host = host.split(':')[0]

        # If the host is already allowed, skip the DB/cache lookup
        if host not in settings.ALLOWED_HOSTS:
            try:
                from domain_ssl.services.domain_service import get_current_domain
                domain = get_current_domain()
                if domain and domain not in settings.ALLOWED_HOSTS:
                    # Remove any previously added dynamic host first
                    for old_host in list(_dynamic_hosts):
                        if old_host in settings.ALLOWED_HOSTS:
                            settings.ALLOWED_HOSTS.remove(old_host)
                        _dynamic_hosts.discard(old_host)

                    settings.ALLOWED_HOSTS.append(domain)
                    _dynamic_hosts.add(domain)
            except (ImportError, RuntimeError):
                # ImportError: app not ready yet during startup
                # RuntimeError: DB not available
                pass
            except Exception:
                logger.debug(
                    'DynamicAllowedHostsMiddleware: failed to check domain',
                    exc_info=True,
                )

        return self.get_response(request)
