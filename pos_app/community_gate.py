"""
Community edition POS gate.

Under the Community licence, POS is not enabled. Users navigating to any POS
admin URL see an "Upgrade to enable POS" page instead of the POS UI itself.

Wired up in two places:
- ``pos_upgrade_required_view`` — the view that renders the upgrade CTA
- ``POSCommunityGateMiddleware`` — intercepts POS admin paths for Community users

Fork-and-patch is fine: this is a runtime check, not code stripping. Merchants
with a paid licence bypass the gate.
"""

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


# Path prefixes intercepted by the middleware. Anything under these paths that
# is not the upgrade page itself is redirected to the upgrade page for
# Community users.
POS_ADMIN_PREFIXES = (
    "/admin/pos_app/",
    "/admin/pos/",
    "/pos/",
)

# Public upgrade landing on the Spwig marketplace. Configurable so self-hosted
# marketplaces can point at their own upgrade flow.
DEFAULT_POS_UPGRADE_URL = "https://updates.spwig.com/upgrade/pos/"


def pos_upgrade_url() -> str:
    return getattr(settings, "POS_UPGRADE_URL", DEFAULT_POS_UPGRADE_URL)


@staff_member_required
def pos_upgrade_required_view(request):
    """Render the upgrade CTA page. Staff-only — defence in depth for
    the URL-routed view; the middleware never invokes this for anon."""
    return render(
        request,
        "pos/upgrade_required.html",
        {"pos_upgrade_url": pos_upgrade_url()},
        status=200,
    )


class POSCommunityGateMiddleware:
    """
    Redirect POS admin URLs to the upgrade page for Community-edition installs.

    Runs after AuthenticationMiddleware so ``request.user`` is available. Only
    active for authenticated staff — anonymous and non-staff users hit the
    normal auth flow first.
    """

    UPGRADE_PATH = "/pos-upgrade/"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = self._strip_language_prefix(request.path)

        # Let the upgrade page itself and static assets through
        if path == self.UPGRADE_PATH or path.startswith("/static/"):
            return self.get_response(request)

        # Only gate POS paths
        if not any(path.startswith(prefix) for prefix in POS_ADMIN_PREFIXES):
            return self.get_response(request)

        # Only gate authenticated staff — anonymous users hit auth first
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return self.get_response(request)
        if not getattr(user, "is_staff", False):
            return self.get_response(request)

        # Community edition → redirect to upgrade page
        try:
            from core.license import get_license_manager
            if get_license_manager().is_community():
                return pos_upgrade_required_view(request)
        except Exception:
            # Never break the request cycle if the licence check errors
            pass

        return self.get_response(request)

    @staticmethod
    def _strip_language_prefix(path: str) -> str:
        """Strip /en/, /de/, /zh-hans/ language codes so path matches ignore them."""
        if len(path) > 3 and path[3] == "/" and path[1:3].isalpha():
            return path[3:]
        # Longer codes like /zh-hans/
        if len(path) > 4 and path[0] == "/":
            parts = path.split("/", 2)
            if len(parts) >= 3 and 2 <= len(parts[1]) <= 7:
                return "/" + (parts[2] if parts[2] else "")
        return path
