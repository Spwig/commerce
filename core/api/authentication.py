from admin_api.authentication import MobileTokenAuthentication
from rest_framework.authentication import TokenAuthentication


class HeadlessAPIMixin:
    """Mixin for public storefront API views accessed by headless frontends.

    Excludes SessionAuthentication so that CSRF is never enforced on API
    requests.  Token-based auth (Bearer / Token) still works for endpoints
    that require an authenticated customer.

    Also stamps every response with strict no-cache headers. Cart, checkout,
    account, and similar endpoints are per-visitor and must never be served
    from a CDN cache. Cloudflare APO in particular caches JSON responses
    aggressively and ignores client-side Cache-Control, so this header must
    be set server-side to opt out.

    Apply to any ViewSet or APIView that serves the public storefront API:

        class CartViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
            ...
    """

    authentication_classes = [MobileTokenAuthentication, TokenAuthentication]

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        # Belt-and-braces against Cloudflare APO and other intermediate caches.
        # `private` = browser may cache for this user only, no shared caches.
        # `no-store` = don't write to any cache.
        # `must-revalidate` + `max-age=0` = if anything cached it anyway, treat
        # it as immediately stale.
        response['Cache-Control'] = 'private, no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        return response
