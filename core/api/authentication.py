from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from admin_api.authentication import MobileTokenAuthentication


class HeadlessAPIMixin:
    """Mixin for public storefront API views accessed by headless frontends.

    Authentication order: mobile token, then DRF token (both for headless
    clients), then session — so a customer logged in to the storefront in a
    browser is recognised by the cart/checkout APIs instead of being treated
    as an anonymous visitor with a separate session cart. DRF enforces CSRF
    only on session-AUTHENTICATED unsafe requests (anonymous storefront
    POSTs remain CSRF-exempt, as before), and every storefront JS caller
    sends X-CSRFToken from the base template's csrf-token meta tag, so
    token-based headless clients remain CSRF-free.

    Also stamps every response with strict no-cache headers. Cart, checkout,
    account, and similar endpoints are per-visitor and must never be served
    from a CDN cache. Cloudflare APO in particular caches JSON responses
    aggressively and ignores client-side Cache-Control, so this header must
    be set server-side to opt out.

    Apply to any ViewSet or APIView that serves the public storefront API:

        class CartViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
            ...
    """

    authentication_classes = [MobileTokenAuthentication, TokenAuthentication, SessionAuthentication]

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        # Belt-and-braces against Cloudflare APO and other intermediate caches.
        # `private` = browser may cache for this user only, no shared caches.
        # `no-store` = don't write to any cache.
        # `must-revalidate` + `max-age=0` = if anything cached it anyway, treat
        # it as immediately stale.
        response["Cache-Control"] = "private, no-store, no-cache, must-revalidate, max-age=0"
        response["Pragma"] = "no-cache"
        return response
