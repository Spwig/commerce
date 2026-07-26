"""
Storefront (non-API) views for the catalog app.

Kept deliberately thin: pages here render a shell and let the existing JSON
endpoints do the work, so the security posture (throttles, uniform 404s, kill
switches) lives in exactly one place.
"""

from django.shortcuts import render


def gift_card_balance_page(request):
    """
    The page a gift card recipient lands on from their delivery email.

    Renders a code entry form; the lookup itself is the throttled
    POST /api/catalog/gift-cards/check-balance/ — uniform 404 for
    unknown/invalid codes, per-anon and per-user rate limits, and the
    SiteSettings kill switch all apply unchanged, because this view never
    touches a gift card itself.

    Deliberately public and code-required. A gift card is a bearer
    instrument: the person entitled to check it is whoever holds the code,
    account or not.
    """
    return render(request, "catalog/gift_card_balance.html")
